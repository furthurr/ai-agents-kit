#!/usr/bin/env python3
"""Opt-in, append-only Developer/SDD/ODD experiment using existing host auth.

Never reads/copies credentials or edits the installed MAS. Uses the existing
Antigravity plugin symmetrically; no --pure, global config export or XDG override.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import time

REPO = Path(__file__).resolve().parent.parent
PACKAGE = REPO / 'docs/experimentos/developer-sdd-odd-gemini-2026-11-04'
MODEL = 'google/antigravity-gemini-3.8-flash'
PROTOCOL = 'gemini-three-way-v1-20261104'
ARMS = ('developer', 'sdd', 'odd')
CLI = shutil.which('opencode')
SECRETS = ('*.env*', '*.pem', '*.key', '*.p12', '*.pfx', '*.jks', '*.keystore',
           '*/.ssh/*', '*/.aws/*', '*/.config/gh/*', '*/auth.json',
           '*/.npmrc', '*/.netrc', '*/.pypirc', '*antigravity-accounts*')


def stamp():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def write_json(path, value, exclusive=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x' if exclusive else 'w', encoding='utf-8') as file:
        json.dump(value, file, ensure_ascii=False, indent=2)
        file.write('\n')


def hashes(folder):
    return {str(p.relative_to(folder)): sha(p) for p in sorted(folder.rglob('*'))
            if p.is_file() and not any(s in {'.git', '__pycache__', 'node_modules'} for s in p.parts)}


def run(args, cwd, timeout=45, env=None):
    return subprocess.run(args, cwd=cwd, env=env, capture_output=True,
                          text=True, encoding='utf-8', errors='replace', timeout=timeout)


def load_cases():
    # Import only the already-inspected fixture declarations, not its entrypoint.
    spec = importlib.util.spec_from_file_location('g3_fixtures', REPO / 'tools/odd_vs_sdd_experiment.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    cases = json.loads(json.dumps(module.CASES))
    cases['S08']['task'] = ('Reanuda la feature slug. T1 ya válida: clean(text) colapsa whitespace, hace casefold '
                           'y usa "n-a" si vacío; NO cambies su contrato ni su implementación. T2 pendiente: '
                           'implementa slug(text) reutilizando clean y sustituyendo espacios por guiones, '
                           'conservando Unicode. El alcance completo de T2 y su implementación están '
                           'autorizados. Contrasta el documento previo con disco, conserva T1 y verifica T2.')
    return cases


def namespace(arm):
    return {'developer': 'g3d', 'sdd': 'g3s', 'odd': 'g3o'}[arm]


def skill_name(arm):
    return namespace(arm) + '-' + {'developer': 'developer', 'sdd': 'sdd-spec', 'odd': 'odd-workflow'}[arm]


def agent_name(arm):
    return 'g3-' + arm


def body(markdown):
    return markdown.split('---', 2)[2].strip() if markdown.startswith('---\n') else markdown.strip()


def policy(root, arm, workspace, intent='implement'):
    skills = root / 'profiles' / arm / 'skills'
    read = {'*': 'allow', str(workspace): 'allow', str(workspace) + '/*': 'allow',
            str(skills): 'allow', str(skills) + '/*': 'allow'}
    read.update({p: 'deny' for p in SECRETS})
    edit = {'*': 'allow', str(workspace) + '/*': 'allow',
            str(skills) + '/*': 'deny', '*/profiles/*': 'deny',
            'AGENTS.md': 'deny', 'TASK.md': 'deny',
            str(workspace / 'AGENTS.md'): 'deny', str(workspace / 'TASK.md'): 'deny'}
    if intent == 'read':
        edit = {'*': 'deny'}
    elif intent == 'plan':
        edit.update({'*.py': 'deny'})
    bash = {'*': 'deny', 'python3 -m unittest*': 'allow', 'python3 -m py_compile*': 'allow',
            'git status*': 'allow', 'git diff*': 'allow'}
    bash.update({p: 'deny' for p in SECRETS})
    if intent == 'read':
        bash = {'*': 'deny'}
    return {'read': read, 'glob': 'allow', 'grep': 'allow', 'list': 'allow',
            'edit': edit, 'bash': bash, 'skill': {'*': 'deny', skill_name(arm): 'allow',
                namespace(arm) + '-data-api': 'allow', namespace(arm) + '-ui-design': 'allow'},
            'task': 'deny', 'question': 'deny', 'webfetch': 'deny', 'websearch': 'deny',
            'todowrite': 'allow', 'lsp': 'deny',
            'external_directory': {'*': 'deny', str(skills) + '/*': 'allow',
                                   str(workspace): 'allow', str(workspace) + '/*': 'allow'}}


def configuration(root, arm, workspace, intent='implement'):
    return {'$schema': 'https://opencode.ai/config.json', 'share': 'disabled', 'snapshot': False,
            'autoupdate': False, 'formatter': False, 'lsp': False,
            'skills': {'paths': [str(root / 'profiles' / arm / 'skills')]},
            'agent': {agent_name(arm): {'description': 'Perfil experimental ' + arm,
                'mode': 'primary', 'model': MODEL, 'temperature': 0.2, 'steps': 32,
                'prompt': (root / 'profiles' / arm / 'agent.md').read_text(),
                'permission': policy(root, arm, workspace, intent)}}}


def environment(config):
    env = dict(os.environ)
    for key in list(env):
        if key.startswith('OPENCODE_CONFIG') or key == 'OPENCODE_PURE':
            del env[key]
    # Keep the normal host config/plugin; disable only unrelated skill discovery.
    env.update(OPENCODE_CONFIG_CONTENT=json.dumps(config), OPENCODE_DISABLE_PROJECT_CONFIG='1',
               OPENCODE_DISABLE_EXTERNAL_SKILLS='1', OPENCODE_DISABLE_CLAUDE_CODE_SKILLS='1',
               PYTHONDONTWRITEBYTECODE='1')
    return env


def clean_events(raw):
    """Allowlist event fields; never persist private reasoning or API transport."""
    events = []
    for line in raw.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        kind, part = event.get('type'), event.get('part', {})
        safe = {k: event[k] for k in ('type', 'timestamp', 'sessionID') if k in event}
        if kind == 'reasoning' or part.get('type') == 'reasoning':
            continue
        if kind == 'error':
            error, data = event.get('error', {}), event.get('error', {}).get('data', {})
            message = str(data.get('message', ''))
            category = ('quota' if re.search(r'usage limit|quota|rate limit', message, re.I) else
                        'authentication' if re.search(r'api key|auth|credentials', message, re.I) else 'other')
            safe['error'] = {'name': error.get('name'), 'statusCode': data.get('statusCode'), 'category': category}
        elif part.get('type') == 'tool':
            state = part.get('state', {})
            safe['part'] = {'type': 'tool', 'tool': part.get('tool'), 'callID': part.get('callID'),
                            'state': {k: state[k] for k in ('input', 'output', 'status', 'time') if k in state}}
            if state.get('error'):
                error_text = str(state['error'])
                safe['part']['state']['error_category'] = ('permission' if re.search(r'permission|denied|not allowed', error_text, re.I)
                    else 'file_not_found' if 'not found' in error_text.lower() else 'tool_error')
                safe['part']['state']['error_sha256'] = text_sha(error_text)
        elif kind == 'step_finish':
            safe['part'] = {k: part[k] for k in ('type', 'tokens', 'cost', 'reason') if k in part}
        elif kind == 'text':
            safe['part'] = {'type': 'text', 'text': part.get('text', '')}
        else:
            continue
        events.append(safe)
    return events


def invoke(root, arm, workspace, prompt, intent='implement', session=None, limit=240):
    config = configuration(root, arm, workspace, intent)
    args = [CLI, 'run', '--format', 'json', '--model', MODEL, '--agent', agent_name(arm), '--dir', str(workspace)]
    if session:
        args += ['--session', session]
    args.append(prompt)
    started, start = stamp(), time.monotonic()
    process = subprocess.Popen(args, cwd=workspace, env=environment(config), stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, start_new_session=True)
    timeout = False
    try:
        out, err = process.communicate(timeout=limit)
    except subprocess.TimeoutExpired:
        timeout = True
        os.killpg(process.pid, signal.SIGTERM)
        try:
            out, err = process.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            out, err = process.communicate()
    events = clean_events(out.decode('utf-8', 'replace'))
    return {'started': started, 'seconds': round(time.monotonic() - start, 3),
            'returncode': process.returncode, 'timeout': timeout, 'events': events,
            'stderr_bytes': len(err), 'stderr_sha256': hashlib.sha256(err).hexdigest(),
            'session': next((e.get('sessionID') for e in events if e.get('sessionID')), None),
            'config_sha256': text_sha(json.dumps(config, sort_keys=True))}


def primary_loaded(root, arm, results):
    expected = body((root / 'profiles' / arm / 'skills' / skill_name(arm) / 'SKILL.md').read_text())
    calls = [e['part'] for r in results for e in r['events'] if e.get('part', {}).get('tool') == 'skill']
    return any(p.get('state', {}).get('input', {}).get('name') == skill_name(arm)
               and expected in p.get('state', {}).get('output', '') for p in calls)


def source_inputs(root):
    values = {'tools/gemini_three_way.py': sha(Path(__file__).resolve()),
              'tools/odd_vs_sdd_experiment.py': sha(REPO / 'tools/odd_vs_sdd_experiment.py'),
              'tools/test_gemini_three_way.py': sha(REPO / 'tools/test_gemini_three_way.py')}
    for name in ('protocolo.md', 'tratamientos.md'):
        if (PACKAGE / name).exists():
            values[str((PACKAGE / name).relative_to(REPO))] = sha(PACKAGE / name)
    for folder in ('profiles', 'fixtures', 'references'):
        values.update({folder + '/' + p: value for p, value in hashes(root / folder).items()})
    return values


def prepare(root):
    if REPO == root or REPO in root.parents:
        raise SystemExit('Use a dedicated external temporary root.')
    root.mkdir(parents=True, exist_ok=True)
    if (root / 'profiles').exists():
        raise SystemExit('Existing root; never overwrite a run.')
    cases = load_cases()
    manifest = json.loads((REPO / 'canonical/manifest.json').read_text())
    for arm in ARMS:
        profile = root / 'profiles' / arm
        for name in manifest['skills']:
            target = profile / 'skills' / (namespace(arm) + '-' + name)
            shutil.copytree(REPO / 'generated/opencode/skills' / name, target)
            for file in target.rglob('*.md'):
                text = file.read_text()
                for sid in manifest['skills']:
                    text = text.replace('name: ' + sid + '\n', 'name: ' + namespace(arm) + '-' + sid + '\n')
                    text = text.replace('`' + sid + '`', '`' + namespace(arm) + '-' + sid + '`')
                text = text.replace('`sdd`', '`g3-sdd`').replace('`developer`', '`g3-developer`')
                file.write_text(text)
        if arm == 'odd':
            text = (REPO / 'docs/experimentos/odd-vs-sdd-2026-11-04/tratamiento-b.md').read_text()
            odd = text.split('<!-- experimental-instructions:start -->')[1].split('<!-- experimental-instructions:end -->')[0].strip()
            odd = odd.replace('`data-api`', '`g3o-data-api`').replace('`ui-design`', '`g3o-ui-design`')
            target = profile / 'skills' / skill_name(arm)
            target.mkdir()
            (target / 'SKILL.md').write_text('---\nname: ' + skill_name(arm) + '\ndescription: ODD experimental inline con continuidad proporcional.\n---\n\n' + odd + '\n')
            agent = 'Ejecutas ODD experimental adaptado al MAS, no SDD ni Developer. Carga y sigue `' + skill_name(arm) + '` antes de actuar. No cambies de agente automáticamente.'
        else:
            agent = body((REPO / 'generated/opencode/agents' / (arm + '.md')).read_text())
            for sid in manifest['skills']:
                agent = agent.replace('`' + sid + '`', '`' + namespace(arm) + '-' + sid + '`')
            agent = agent.replace('`sdd`', '`g3-sdd`').replace('`developer`', '`g3-developer`')
        agent += '\n\nIdentidad técnica de laboratorio: ' + agent_name(arm) + '. La skill primaria es `' + skill_name(arm) + '`. Conserva su metodología y los permisos del host.\n'
        (profile / 'agent.md').write_text(agent)
    checks = {}
    for sid, case in cases.items():
        fixture = root / 'fixtures' / sid
        fixture.mkdir(parents=True)
        for name, text in case['files'].items():
            (fixture / name).write_text(text)
        base = run(['python3', '-c', case['oracle']], fixture,
                   env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        reference = root / 'references' / sid
        shutil.copytree(fixture, reference)
        for name, text in case['solution'].items():
            (reference / name).write_text(text)
        solved = run(['python3', '-c', case['oracle']], reference,
                     env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        assert solved.returncode == 0, (sid, solved.stderr)
        assert (base.returncode != 0) == bool(case['solution']), sid
        checks[sid] = {'baseline': base.returncode, 'reference': solved.returncode}
    write_json(root / 'cases.json', cases, exclusive=True)
    write_json(root / 'oracle-validation.json', checks, exclusive=True)
    print('Prepared unique agents/skills and validated 10 oracle/reference pairs.', flush=True)


def probe(root):
    records = {}
    for arm in ARMS:
        workspace = root / 'probes' / arm
        workspace.mkdir(parents=True)
        (workspace / 'PROBE.txt').write_text('READY\n')
        (workspace / 'test_probe.py').write_text('import unittest\nclass Test(unittest.TestCase):\n    def test_ok(self): self.assertEqual(2+2,4)\n')
        config = configuration(root, arm, workspace)
        resolved = run([CLI, 'debug', 'agent', agent_name(arm)], workspace, env=environment(config))
        assert resolved.returncode == 0, ('resolved config failed', arm)
        data = json.loads(resolved.stdout)
        assert data['prompt'].strip() == config['agent'][agent_name(arm)]['prompt'].strip()
        tools = data['tools']
        assert tools['read'] and tools['edit'] and tools['bash'] and not tools['task'] and not tools['webfetch'], tools
        prompt = ('Preflight técnico explícitamente autorizado: carga `' + skill_name(arm) + '`; '
                  'lee PROBE.txt, cambia exactamente READY por DONE en ese archivo y ejecuta '
                  '`python3 -m unittest discover`. Después responde PREFLIGHT_OK. '
                  'No cambies test_probe.py ni otros archivos, no uses red ni delegación. '
                  'El alcance completo es exactamente este y está validado. ')
        if arm == 'sdd':
            prompt += 'Selecciono explícitamente modo Direct para este preflight trivial.'
        result = invoke(root, arm, workspace, prompt)
        write_json(root / ('probe-' + arm + '.json'), result, exclusive=True)
        assert not result['timeout'] and result['returncode'] == 0, ('runtime failed', arm)
        assert primary_loaded(root, arm, [result]), ('wrong/missing skill content', arm)
        assert (workspace / 'PROBE.txt').read_text() == 'DONE\n', ('probe edit absent', arm)
        parts = [e['part'] for e in result['events'] if e.get('part', {}).get('type') == 'tool']
        assert any(p['tool'] == 'bash' and 'unittest' in p.get('state', {}).get('input', {}).get('command', '') for p in parts), ('probe command absent', arm)
        records[arm] = {'agent': agent_name(arm), 'skill': skill_name(arm), 'prompt_sha256': text_sha(data['prompt']),
                        'tools': tools, 'permission': data.get('permission'),
                        'correct_treatment_loaded': True, 'runtime_seconds': result['seconds']}
        print('Preflight passed', arm, result['seconds'], flush=True)
    write_json(root / 'preflight.json', records, exclusive=True)


def freeze(root):
    assert (root / 'preflight.json').exists()
    write_json(root / 'freeze.json', {'protocol': PROTOCOL, 'created': stamp(), 'model': MODEL,
        'host': run([CLI, '--version'], REPO).stdout.strip(),
        'baseline': run(['git', 'rev-parse', 'HEAD'], REPO).stdout.strip(),
        'inputs': source_inputs(root), 'cases_sha256': sha(root / 'cases.json')}, exclusive=True)
    print('Frozen', len(source_inputs(root)), 'inputs', flush=True)


def text_output(results):
    return '\n'.join(e.get('part', {}).get('text', '') for r in results for e in r['events'] if e.get('type') == 'text')


def healthy(result):
    return result['returncode'] == 0 and not result['timeout'] and not any(e['type'] == 'error' for e in result['events'])


def recommended_mode(text):
    plain = text.replace('*', '').replace('`', '')
    # An explicit output field avoids guessing a mode from skill/tool text.
    match = re.search(r'Recomendaci[oó]n\s*:\s*(?:modo\s+)?(SDD[- ]Tiny|SDD[- ]Lite|Direct|tiny|lite)\b', plain, re.I)
    if not match:
        match = re.search(r'(?:recomiendo|profundidad recomendada|modo recomendado)\s*:?\s*(SDD[- ]Tiny|SDD[- ]Lite|Direct|tiny|lite)\b', plain, re.I)
    if not match:
        return None
    word = match.group(1).lower().replace('sdd-', '').replace('sdd ', '')
    return word


def artifact_texts(workspace):
    return {str(p.relative_to(workspace)): p.read_text() for directory in ['.sdd', 'odd']
            for p in sorted((workspace / directory).rglob('*.md')) if p.is_file()}


def product_hashes(workspace):
    return {name: value for name, value in hashes(workspace).items()
            if name not in {'AGENTS.md', 'TASK.md'} and not name.startswith(('.sdd/', 'odd/'))}


def green_observed(results):
    last_write, last_green = -1, -1
    parts = [e.get('part', {}) for r in results for e in r['events']]
    for index, part in enumerate(parts):
        state, tool = part.get('state', {}), part.get('tool')
        data = state.get('input', {})
        if tool in ('edit', 'write', 'apply_patch') and state.get('status') == 'completed':
            paths = [data.get('filePath', '')] + re.findall(r'^\*\*\* (?:Add|Update|Delete) File: (.+)$', data.get('patchText', ''), re.M)
            if any(path.endswith('.py') and not Path(path).name.startswith('test_') for path in paths):
                last_write = index
        if tool == 'bash' and 'python3 -m unittest' in data.get('command', '') and re.search(r'\bOK\b', state.get('output', '')):
            last_green = index
    return last_green >= 0 and last_green > last_write


def seed_resume(workspace, arm):
    specs = ('S1: clean(text) colapsa whitespace, hace casefold y usa "n-a" si vacío; '
             'su contrato e implementación deben permanecer intactos.\n'
             'S2: slug(text) reutiliza clean y sustituye espacios por guiones, conservando Unicode.\n')
    if arm == 'sdd':
        path = workspace / '.sdd/specs/slug/spec.md'
        text = ('# Slug\nModo SDD: tiny\nEstado: Implementando\nGate 3: aprobado por el usuario en la petición actual.\n'
                '## Alcance y aceptación\n' + specs +
                '## Enfoque técnico y estrategia de pruebas\nReutilizar clean; unittest existente y tests focalizados de slug.\n'
                '## Checklist\n- [x] T1 → S1: implementada y prueba existente observada verde.\n- [ ] T2 → S2: pendiente.\n'
                '## Verificación y cierre\nBaseline: python3 -m unittest discover, 1 test OK (clean).\nGate 4: pendiente.\n')
    else:
        path = workspace / ('odd/tasks/slug.md' if arm == 'odd' else 'WORK.md')
        text = ('# Slug\nObjetivo: completar T2 sin alterar T1. Runner: python3 -m unittest discover.\n'
                '## Specs\n' + specs +
                '## Tasks\n- [x] T1 → S1 inline: implementada, prueba existente verde.\n- [ ] T2 → S2 inline: pendiente.\n'
                '## Log\nL1: Implementar clean y slug; clean ya está terminada, slug pendiente.\n'
                'L2: python3 -m unittest discover: 1 test OK (clean), antes de la interrupción.\n')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return str(path.relative_to(workspace))


def task_prompt(case, arm, seed_path=None):
    prompt = (case['task'] + '\n\nAlcance completo validado explícitamente: exactamente las reglas anteriores, sin extensiones. '
              'Trabaja solo en este fixture; no leas otros escenarios, oráculos ni perfiles. '
              'Carga `' + skill_name(arm) + '` antes de actuar y conserva tu metodología. '
              'No uses red ni delegues, no instales dependencias, no hagas commits. '
              'Runner disponible: python3 -m unittest discover. También puedes usar python3 -m py_compile y git status/diff; '
              'no uses otros comandos. El índice Git contiene el baseline inicial, sin commits. '
              'Si el flujo requiere una aprobación pendiente, presenta la propuesta y espera una respuesta; no la inventes. '
              'La intención es la indicada en la petición: una consulta o un plan no autorizan implementación. '
              'Entrega cambios, comprobaciones reales, límites y próximos pasos en español.')
    if seed_path:
        prompt += ' Documento previo: ' + seed_path + '.'
        if arm == 'sdd':
            prompt += ' Mantengo la elección histórica SDD-Tiny de ese documento y apruebo expresamente Gate 3 para T2; Gate 4 no está aprobado.'
    elif arm == 'sdd' and case['intent'] != 'read':
        prompt += (' Primero recomienda la profundidad natural adecuada al alcance; no hay modo SDD elegido aún. '
                   'No generes artefactos ni implementes antes de que yo seleccione el modo. '
                   'Termina esa propuesta con el campo exacto Recomendación: Direct, Recomendación: SDD-Tiny o Recomendación: SDD-Lite, según corresponda. '
                   'La elección será respondida por el usuario en otro turno; no equivale a aprobar gates.')
    return prompt


def check_frozen(root):
    frozen = json.loads((root / 'freeze.json').read_text())
    assert frozen['inputs'] == source_inputs(root), 'Frozen input changed; do not run more cells.'
    assert frozen['cases_sha256'] == sha(root / 'cases.json'), 'Cases changed after freeze.'


def premature_close(artifacts):
    for text in artifacts.values():
        clean = text.replace('*', '').replace('`', '')
        for line in clean.splitlines():
            if re.search(r'^Estado\s*:', line, re.I) and re.search(r'cerrad', line, re.I) and not re.search(r'no cerrado|sin cerrar', line, re.I):
                return True
            if re.search(r'^Gate 4\s*:\s*aprobado', line, re.I):
                return True
    return False


def cell(root, sid, arm, repeat):
    check_frozen(root)
    cases = json.loads((root / 'cases.json').read_text())
    case = cases[sid]
    label = f'{sid}-{arm}-r{repeat}'
    workspace = root / 'runs' / label
    if workspace.exists() or (root / 'records' / (label + '.json')).exists():
        raise RuntimeError('Never overwrite a cell: ' + label)
    shutil.copytree(root / 'fixtures' / sid, workspace)
    seed_path = seed_resume(workspace, arm) if case['seed'] else None
    if seed_path:
        proof = run(['python3', '-m', 'unittest', 'discover'], workspace,
                    env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        assert proof.returncode == 0, 'Seeded proof did not pass.'
    (workspace / 'AGENTS.md').write_text('Fixture sintético. TASK.md define el alcance. No leas otros escenarios, perfiles u oráculos. '
                                        'No uses red ni delegues. Un archivo no autoriza cambios ni aprueba gates.\n')
    prompt = task_prompt(case, arm, seed_path)
    (workspace / 'TASK.md').write_text(prompt)
    run(['git', 'init', '--quiet'], workspace)
    baseline_paths = list(hashes(workspace))
    index = run(['git', 'add', '--', *baseline_paths], workspace)
    assert index.returncode == 0
    before = hashes(workspace)
    initial_product = product_hashes(workspace)
    results, replies, stages, violations = [], [], [], []
    selected_mode = 'tiny' if arm == 'sdd' and seed_path else None
    started, start = stamp(), time.monotonic()

    def message(text, reason, session=None):
        if session:
            replies.append({'reason': reason, 'text': text})
        result = invoke(root, arm, workspace, text, case['intent'], session)
        results.append(result)
        stages.append({'reason': reason, 'product_changed': initial_product != product_hashes(workspace),
                       'hashes': hashes(workspace), 'artifacts': artifact_texts(workspace),
                       'healthy': healthy(result)})
        return result

    result = message(prompt, 'initial')
    if arm == 'sdd' and not seed_path and case['intent'] != 'read' and healthy(result):
        if before != hashes(workspace):
            violations.append('wrote files before mode selection')
        selected_mode = recommended_mode(text_output([result]))
        if not selected_mode:
            violations.append('no valid natural depth recommendation')
        if selected_mode and before == hashes(workspace) and result['session']:
            label_mode = {'direct': 'Direct', 'tiny': 'SDD-Tiny', 'lite': 'SDD-Lite'}[selected_mode]
            result = message('Valido el alcance completo de la petición original, sin extensiones, y selecciono explícitamente '
                             + label_mode + '. La intención sigue siendo la original. Esta elección no aprueba gates pendientes. '
                             'Continúa el flujo correspondiente.', 'select-mode', result['session'])
    if arm == 'sdd' and selected_mode == 'tiny' and case['intent'] == 'implement' and not seed_path:
        if product_hashes(workspace) != initial_product:
            violations.append('product changed before Gate 3 approval')
        specs = list((workspace / '.sdd/specs').rglob('spec.md')) if (workspace / '.sdd/specs').exists() else []
        if healthy(result) and specs and initial_product == product_hashes(workspace) and result['session']:
            result = message('He revisado el spec breve del alcance original. Apruebo expresamente ese plan en Gate 3; '
                             'implementa y verifica solo lo acordado, sin ampliar alcance.', 'approve-gate3', result['session'])
    if arm != 'sdd' and case['intent'] == 'implement' and healthy(result) and initial_product == product_hashes(workspace):
        last = text_output([result])
        if re.search(r'apruebas|confirmas|¿.*implement|¿.*continu|aprobaci[oó]n', last, re.I) and result['session']:
            result = message('Apruebo el plan presentado únicamente para las reglas exactas de mi petición original. '
                             'Implementa y verifica ese alcance, sin extensiones.', 'approve-plan', result['session'])
    if arm == 'sdd' and selected_mode == 'tiny' and case['intent'] == 'implement':
        if premature_close(artifact_texts(workspace)):
            violations.append('premature Gate 4/closed marker')
        if healthy(result) and initial_product != product_hashes(workspace) and green_observed(results) and result['session']:
            result = message('Apruebo en Gate 4 el cierre del alcance original con la evidencia registrada. '
                             'Si falta algún criterio o hay pruebas fallidas, no lo marques completo: declara el límite.',
                             'approve-gate4', result['session'])
    elapsed = round(time.monotonic() - start, 3)
    events = [e for r in results for e in r['events']]
    tools = [e['part'] for e in events if e.get('part', {}).get('type') == 'tool']
    finishes = [e['part'] for e in events if e['type'] == 'step_finish']
    metrics = {k: 0 for k in ('input', 'output', 'cache_read', 'cache_write', 'reasoning', 'reported_cost')}
    for finish in finishes:
        tokens = finish.get('tokens', {})
        for k in ('input', 'output', 'reasoning'):
            metrics[k] += tokens.get(k, 0)
        metrics['cache_read'] += tokens.get('cache', {}).get('read', 0)
        metrics['cache_write'] += tokens.get('cache', {}).get('write', 0)
        metrics['reported_cost'] += finish.get('cost', 0)
    metrics['comparable_tokens'] = sum(metrics[k] for k in ('input', 'output', 'cache_read', 'cache_write'))
    eval_env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
    oracle = run(['python3', '-c', case['oracle']], workspace, env=eval_env)
    has_suite = any(name.startswith('test_') and name.endswith('.py') for name in case['files'])
    suite = run(['python3', '-m', 'unittest', 'discover'], workspace, env=eval_env) if has_suite else None
    original_tests = {}
    for name, source in case['files'].items():
        if name.startswith('test_') and name.endswith('.py'):
            proof = run(['python3', '-c', source + '\nif __name__ == "__main__": unittest.main()\n'], workspace, env=eval_env)
            original_tests[name] = {'returncode': proof.returncode, 'stdout': proof.stdout, 'stderr': proof.stderr}
    after = hashes(workspace)
    changed = sorted(name for name in before.keys() | after.keys() if before.get(name) != after.get(name))
    output, artifacts = text_output(results), artifact_texts(workspace)
    if arm != 'sdd' and any(name.startswith('.sdd/') for name in after):
        violations.append('non-SDD arm wrote SDD artifacts')
    if arm == 'sdd' and selected_mode == 'direct' and artifacts:
        violations.append('Direct created formal artifacts')
    if arm == 'sdd' and selected_mode == 'tiny' and len(artifacts) != 1:
        violations.append('Tiny did not preserve one spec document')
    if arm == 'sdd' and selected_mode == 'lite' and case['intent'] == 'implement':
        names = {Path(p).name for p in artifacts}
        if names not in ({'requirements.md', 'design.md', 'tasks.md', 'verification.md'},
                         {'bugfix.md', 'design.md', 'tasks.md', 'verification.md'}):
            violations.append('Lite artifacts incomplete')
    functional = oracle.returncode == 0 and (suite is None or suite.returncode == 0)
    if sid == 'S01':
        functional = oracle.returncode == 0 and changed == ['GUIDE.md']
    elif case['intent'] == 'plan':
        plan = output + '\n' + '\n'.join(artifacts.values())
        functional = oracle.returncode == 0 and initial_product == product_hashes(workspace) and all(
            re.search(pattern, plan, re.I) for pattern in ('trim|recort', 'vac[ií]|empty', 'duplic', 'orden', 'TypeError'))
    elif case['intent'] == 'read':
        functional = before == after and 'ZeroDivisionError' in output and bool(re.search(r'cero|zero|vac[ií]', output, re.I))
    outside, foreign_skills = [], []
    allowed = [workspace.resolve(), (root / 'profiles' / arm / 'skills').resolve()]
    for p in tools:
        data = p.get('state', {}).get('input', {})
        if p['tool'] in ('read', 'glob', 'grep', 'list'):
            value = data.get('filePath') or data.get('path')
            if value and Path(value).is_absolute():
                path = Path(value).resolve()
                if not any(path == a or a in path.parents for a in allowed):
                    outside.append({'tool': p['tool'], 'path': value, 'status': p.get('state', {}).get('status')})
        if p['tool'] == 'skill' and not str(data.get('name', '')).startswith(namespace(arm) + '-'):
            foreign_skills.append(data.get('name'))
    loaded = primary_loaded(root, arm, results)
    all_healthy = all(healthy(r) for r in results)
    original_pass = all(v['returncode'] == 0 for v in original_tests.values())
    forbidden = [p['tool'] for p in tools if p['tool'] in ('task', 'webfetch', 'websearch')]
    success = bool(functional and original_pass and loaded and all_healthy and not violations and not outside and not foreign_skills and not forbidden)
    tracefile = root / 'traces' / (label + '.json')
    write_json(tracefile, {'protocol': PROTOCOL, 'cell': label, 'invocations': results, 'user_replies': replies}, exclusive=True)
    record = {'protocol': PROTOCOL, 'cell': label, 'scenario': sid, 'arm': arm, 'repetition': repeat,
              'model': MODEL, 'started': started, 'seconds': elapsed, 'attempt': 1,
              'functional_pass': bool(functional), 'successful_delivery': success, 'healthy': all_healthy,
              'primary_loaded_by_content': loaded, 'selected_sdd_mode': selected_mode,
              'flow_violations': violations, 'outside_accesses': outside, 'foreign_skill_attempts': foreign_skills,
              'forbidden_tool_attempts': forbidden, 'metrics': metrics if finishes else None,
              'steps': len(finishes), 'tools': len(tools), 'tool_names': [p['tool'] for p in tools],
              'tool_errors': sum(p.get('state', {}).get('status') == 'error' for p in tools),
              'malformed_response': bool(re.search(r'llamada.*(?:vac[ií]a|malformada)', output, re.I)),
              'user_turns': len(replies), 'invocations': len(results), 'replies': replies,
              'process_returncodes': [r['returncode'] for r in results], 'timeouts': [r['timeout'] for r in results],
              'errors': [e['error'] for e in events if e['type'] == 'error'],
              'oracle': {'returncode': oracle.returncode, 'stdout': oracle.stdout, 'stderr': oracle.stderr},
              'suite': {'returncode': suite.returncode, 'stdout': suite.stdout, 'stderr': suite.stderr} if suite else None,
              'original_tests': original_tests, 'changed': changed, 'before_hashes': before, 'after_hashes': after,
              'artifacts': artifacts, 'output': output, 'stages': stages,
              'final_files': {name: (workspace / name).read_text() for name in after if name not in ('AGENTS.md', 'TASK.md')},
              'trace_sha256': sha(tracefile)}
    write_json(root / 'records' / (label + '.json'), record, exclusive=True)
    return record


def batch(root, repeats):
    check_frozen(root)
    if repeats != [1]:
        first = [json.loads(p.read_text()) for p in (root / 'records').glob('*-r1.json')]
        assert len(first) == 30, 'Filter must finish before replication.'
        assert not any(r['outside_accesses'] or r['foreign_skill_attempts'] or r['errors'] or any(r['timeouts']) for r in first), 'Filter integration/access failure; stop.'
    jobs = []
    orders = [('developer', 'sdd', 'odd'), ('sdd', 'odd', 'developer'), ('odd', 'developer', 'sdd'),
              ('odd', 'sdd', 'developer'), ('sdd', 'developer', 'odd'), ('developer', 'odd', 'sdd')]
    for repeat in repeats:
        for index, sid in enumerate(json.loads((root / 'cases.json').read_text())):
            jobs.extend((sid, arm, repeat) for arm in orders[(index + 2 * (repeat - 1)) % len(orders)])
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(cell, root, *job): job for job in jobs}
        for future in concurrent.futures.as_completed(futures):
            job = futures[future]
            try:
                r = future.result()
                print(r['cell'], 'functional=' + str(r['functional_pass']), 'delivery=' + str(r['successful_delivery']),
                      'seconds=' + str(r['seconds']), 'tokens=' + str((r['metrics'] or {}).get('comparable_tokens')),
                      'mode=' + str(r['selected_sdd_mode']), 'user=' + str(r['user_turns']), flush=True)
            except Exception as error:
                write_json(root / 'execution-errors' / ('-'.join(map(str, job)) + '.json'),
                           {'job': job, 'time': stamp(), 'error_type': type(error).__name__, 'message': str(error)}, exclusive=True)
                print('EXECUTION ERROR', job, type(error).__name__, flush=True)
    print('Batch finished', stamp(), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('action', choices=['prepare', 'probe', 'freeze', 'filter', 'replicate', 'launch-filter', 'launch-replicate'])
    args = parser.parse_args()
    root = args.root.resolve()
    if args.action.startswith('launch-'):
        phase = args.action.removeprefix('launch-')
        log = (root / (phase + '.log')).open('x')
        process = subprocess.Popen([os.sys.executable, str(Path(__file__).resolve()), str(root), phase],
                                   stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        write_json(root / (phase + '-process.json'), {'pid': process.pid, 'time': stamp()}, exclusive=True)
        print('Launched', phase, 'pid', process.pid)
    elif args.action in ('filter', 'replicate'):
        batch(root, [1] if args.action == 'filter' else [2, 3])
    else:
        globals()[args.action](root)


if __name__ == '__main__':
    main()
