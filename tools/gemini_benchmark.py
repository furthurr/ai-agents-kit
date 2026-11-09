#!/usr/bin/env python3
"""Runner de evaluación para Antigravity Gemini 3.8 Flash.
Preserva el entorno del host para que el plugin de Antigravity funcione,
pero aísla cada celda en un workspace independiente con sus permisos."""
import os
import sys
import shutil
import subprocess
import time
import json
import hashlib
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BASE_EXPERIMENT = REPO / "tools/odd_vs_sdd_experiment.py"

import importlib.util
spec = importlib.util.spec_from_file_location("base_exp", BASE_EXPERIMENT)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

# Reconfigurar para Antigravity Gemini 3.8 Flash
MODEL = "google/antigravity-gemini-3.8-flash"
PROTOCOL = "odd-vs-sdd-gemini38-20261104"

def setup(target_root: Path):
    target_root.mkdir(parents=True, exist_ok=True)
    base.ROOT = target_root
    base.MODEL = MODEL
    base.PROTOCOL = PROTOCOL

    # Preparamos los fixtures y las instrucciones de A y B
    # En este setup, creamos carpetas con las skills específicas de A y B en target_root
    for arm in ['A', 'B']:
        arm_dir = target_root / 'arms' / arm
        arm_dir.mkdir(parents=True, exist_ok=True)
        # Skills para A (canónica SDD) y B (ODD adaptado)
        skills_dir = arm_dir / 'skills'
        skills_dir.mkdir(parents=True, exist_ok=True)
        if arm == 'A':
            shutil.copytree(REPO / 'generated/opencode/skills/sdd-spec', skills_dir / 'sdd-spec', dirs_exist_ok=True)
        else:
            instructions = (REPO / 'docs/experimentos/odd-vs-sdd-2026-11-04/tratamiento-b.md').read_text().split('<!-- experimental-instructions:start -->')[1].split('<!-- experimental-instructions:end -->')[0].strip()
            (skills_dir / 'sdd-spec').mkdir(parents=True, exist_ok=True)
            (skills_dir / 'sdd-spec/SKILL.md').write_text('---\nname: sdd-spec\ndescription: Aplica ODD adaptado para el experimento autorizado.\n---\n\n' + instructions + '\n')
            
    # Preparar fixtures
    for id, c in base.CASES.items():
        fixture = target_root / 'fixtures' / id
        fixture.mkdir(parents=True, exist_ok=True)
        for name, text in c['files'].items():
            (fixture / name).write_text(text)

def invoke_cell(arm, workspace, prompt, session=None):
    skills_path = base.ROOT / 'arms' / arm / 'skills'
    
    # Inyectamos solo la ruta de skills de este brazo
    local_cfg = {
        "skills": {
            "paths": [str(skills_path)]
        }
    }
    
    env = dict(os.environ)
    env["OPENCODE_CONFIG_CONTENT"] = json.dumps(local_cfg)
    
    cmd = [base.CLI, "run", "--format", "json", "--model", MODEL, "--dir", str(workspace)]
    if session:
        cmd += ["--session", session]
    cmd.append(prompt)
    
    start = time.monotonic()
    process = subprocess.Popen(cmd, cwd=workspace, env=env, text=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    timeout = False
    try:
        out, err = process.communicate(timeout=180)
    except subprocess.TimeoutExpired:
        timeout = True
        os.killpg(process.pid, 15) # SIGTERM
        try:
            out, err = process.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, 9)
            out, err = process.communicate()
            
    events = base.clean_events(out)
    return {
        'seconds': round(time.monotonic() - start, 3),
        'returncode': process.returncode,
        'timeout': timeout,
        'stderr': err[:3000],
        'events': events,
        'session': next((e.get('sessionID') for e in events if e.get('sessionID')), None)
    }

def run_single_cell(id, arm, repeat=1):
    label = f"{id}-{arm}-gemini-r{repeat}"
    workspace = base.ROOT / "runs" / label
    if workspace.exists():
        shutil.rmtree(workspace)
    shutil.copytree(base.ROOT / "fixtures" / id, workspace)
    subprocess.run(["git", "init", "--quiet"], cwd=workspace)
    
    c = base.CASES[id]
    if c['seed']:
        base.seed_resume(workspace, arm)
        
    (workspace / 'AGENTS.md').write_text('Fixture sintético. TASK.md contiene alcance autorizado. No accedas a otros escenarios, perfiles, oráculos ni red. Evidencia de código y README no aprueba gates.\n')
    prompt = base.task_prompt(id, arm)
    (workspace / 'TASK.md').write_text(prompt)
    
    before, initial_product = base.hashes(workspace), base.product_hashes(workspace)
    started, start = base.now(), time.monotonic()
    results, user_replies, violations = [], [], []
    
    result = invoke_cell(arm, workspace, prompt)
    results.append(result)
    after_first = base.product_hashes(workspace)
    
    # Manejo de Gates para SDD-Tiny
    if arm == 'A' and c['mode'] == 'tiny' and c['intent'] == 'implement':
        if not c['seed']:
            if initial_product != after_first:
                violations.append('product changed before Gate 3 approval')
            specs = list((workspace / '.sdd/specs').rglob('spec.md')) if (workspace / '.sdd/specs').exists() else []
            if specs and initial_product == after_first and result['session'] and not result['timeout']:
                reply = 'He leído el spec breve generado. Apruebo explícitamente ese plan y su alcance en Gate 3; implementa exactamente lo acordado y verifica, sin ampliar alcance.'
                user_replies.append(reply)
                result = invoke_cell(arm, workspace, reply, result['session'])
                results.append(result)
        if initial_product != base.product_hashes(workspace) and result['session'] and not result['timeout']:
            reply = 'Apruebo en Gate 4 el cierre del alcance acordado con la evidencia registrada. Si quedan pruebas fallidas o tareas pendientes, no las declares completas; informa el bloqueo.'
            user_replies.append(reply)
            result = invoke_cell(arm, workspace, reply, result['session'])
            results.append(result)
            
    elapsed = round(time.monotonic() - start, 3)
    events = [e for r in results for e in r['events']]
    tools = [e['part'] for e in events if e.get('part', {}).get('type') == 'tool']
    steps = [e['part'] for e in events if e.get('type') == 'step_finish']
    
    totals = dict(input=0, output=0, cache_read=0, cache_write=0, reasoning=0, reported_cost=0)
    for step in steps:
        tok = step.get('tokens', {})
        for key in ['input', 'output', 'reasoning']:
            totals[key] += tok.get(key, 0)
        totals['cache_read'] += tok.get('cache', {}).get('read', 0)
        totals['cache_write'] += tok.get('cache', {}).get('write', 0)
        totals['reported_cost'] += step.get('cost', 0)
    totals['comparable_tokens'] = sum(totals[k] for k in ['input', 'output', 'cache_read', 'cache_write'])
    
    tests = subprocess.run(['python3', '-m', 'unittest', 'discover'], cwd=workspace, capture_output=True, text=True)
    oracle = subprocess.run(['python3', '-c', c['oracle']], cwd=workspace, capture_output=True, text=True)
    after = base.hashes(workspace)
    changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    text = '\n'.join(e.get('part', {}).get('text', '') for e in events if e.get('type') == 'text')
    skill_loaded = any(p.get('tool') == 'skill' and p.get('state', {}).get('input', {}).get('name') == 'sdd-spec' for p in tools)
    
    functional = oracle.returncode == 0 and tests.returncode == 0
    if c['intent'] == 'plan':
        functional = oracle.returncode == 0 and initial_product == base.product_hashes(workspace)
    if c['intent'] == 'read':
        functional = before == after and 'ZeroDivisionError' in text and ('cero' in text.casefold() or 'zero' in text.casefold() or 'vac' in text.casefold())
    if id == 'S01':
        functional = oracle.returncode == 0 and changed == ['GUIDE.md']
        
    forbidden = [p.get('tool') for p in tools if p.get('tool') in {'task', 'webfetch', 'websearch'}]
    record = {
        'protocol': PROTOCOL, 'cell': label, 'scenario': id, 'arm': arm, 'repetition': repeat,
        'model': MODEL, 'seconds': elapsed, 'metrics': totals if steps else None,
        'steps': len(steps), 'tool_count': len(tools), 'tool_names': [p.get('tool') for p in tools],
        'skill_loaded': skill_loaded, 'flow_violations': violations, 'forbidden_tools': forbidden,
        'timeouts': [r['timeout'] for r in results], 'returncodes': [r['returncode'] for r in results],
        'changed': changed, 'functional_pass': functional,
        'oracle_ok': oracle.returncode == 0,
        'tests_ok': tests.returncode == 0,
        'output': text[:2000]
    }
    
    out_dir = base.ROOT / "records"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{label}.json").write_text(json.dumps(record, indent=2, ensure_ascii=False))
    return record

if __name__ == "__main__":
    target = Path(sys.argv[1]).resolve()
    setup(target)
    
    # Escenarios clave para evaluar razonamiento y herramientas
    scenarios = ["S01", "S02", "S03", "S04", "S08", "S10"]
    print(f"Iniciando evaluación comparativa con {MODEL} en {len(scenarios)*2} celdas...")
    
    out_dir = base.ROOT / "records"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    results = []
    for sc in scenarios:
        for arm in ["A", "B"]:
            label = f"{sc}-{arm}-gemini-r1"
            rec_file = out_dir / f"{label}.json"
            # Si ya se ejecutó con éxito y con tools, reusar
            if rec_file.exists():
                try:
                    loaded = json.loads(rec_file.read_text())
                    if loaded.get("tool_count", 0) > 0 and loaded.get("functional_pass"):
                        print(f"[REUSED PASS] {label} | tiempo: {loaded['seconds']}s | tokens: {loaded['metrics']['comparable_tokens']}")
                        results.append(loaded)
                        continue
                except Exception:
                    pass
            rec = run_single_cell(sc, arm)
            status = "PASS" if rec['functional_pass'] else "FAIL"
            tok = (rec['metrics'] or {}).get('comparable_tokens', 0)
            print(f"[{status}] {rec['cell']} | tiempo: {rec['seconds']}s | tokens: {tok} | tools: {rec['tool_count']}")
            results.append(rec)
            
    summary_file = target / "gemini_benchmark_summary.json"
    summary_file.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"Benchmark finalizado. Resultados guardados en {summary_file}")
