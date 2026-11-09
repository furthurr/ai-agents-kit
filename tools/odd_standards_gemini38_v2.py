#!/usr/bin/env python3
"""Clean Gemini 3.8 Flash cohort v2 for ODD standards with 1200s timeout and context guard."""
import argparse
import hashlib
import inspect
import json
import os
from pathlib import Path
import signal
import shutil
import subprocess
import sys
import time

import odd_standards_retry as retry

REPO = retry.REPO
PACKAGE = REPO / 'docs/experimentos/odd-estandares-gemini-38-v2-2026-11-08'
MODEL = 'github-copilot/gemini-3.8-flash'
PROTOCOL = 'odd-standards-gemini38-v2-20261108'
TIMEOUT = 1200
ARMS = ('odd', 'adjusted')


def context(root):
    base, old = retry.context(root)
    base.MODEL = MODEL
    base.PROTOCOL = PROTOCOL
    original_config, old_inputs = base.configuration, base.source_inputs

    def config(folder, arm, workspace, intent='implement'):
        result = original_config(folder, arm, workspace, intent)
        agent = result['agent'][base.agent_name(arm)]
        agent['model'] = MODEL
        agent['temperature'] = 0.2
        return result
    base.configuration = config

    def inputs(folder):
        values = old_inputs(folder)
        values['model-provenance.json'] = base.sha(folder / 'model-provenance.json')
        for path in (Path(__file__).resolve(), PACKAGE / 'protocolo.md', REPO / 'tools/test_odd_standards_gemini38_v2.py'):
            values[str(path)] = base.sha(path)
        return values
    base.source_inputs = inputs

    def invoke(folder, arm, workspace, prompt, session=None, limit=TIMEOUT):
        cfg = base.configuration(folder, arm, workspace)
        args = [base.CLI, 'run', '--format', 'json', '--model', MODEL,
                '--agent', base.agent_name(arm), '--dir', str(workspace)]
        if session:
            args += ['--session', session]
        args.append(prompt)
        start = time.monotonic()
        started = base.stamp()
        child = subprocess.Popen(args, cwd=workspace, env=base.make_exec_env(cfg), stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, start_new_session=True)
        timeout = False
        try:
            out, err = child.communicate(timeout=limit)
        except subprocess.TimeoutExpired:
            timeout = True
            os.killpg(child.pid, signal.SIGTERM)
            try:
                out, err = child.communicate(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL)
                out, err = child.communicate()
        events = base.kit_bench.clean_events(out.decode('utf-8', 'replace'))
        return {'started': started, 'seconds': round(time.monotonic()-start, 3), 'returncode': child.returncode,
                'timeout': timeout, 'events': events, 'stderr_bytes': len(err),
                'stderr_sha256': hashlib.sha256(err).hexdigest(),
                'session': next((e.get('sessionID') for e in events if e.get('sessionID')), None),
                'model_requested': MODEL,
                'config_sha256': base.text_sha(json.dumps(cfg, sort_keys=True))}
    base.invoke = invoke
    return base, old


def prepare(root):
    retry.prepare(root)
    cases_path = root / 'cases.json'
    cases = json.loads(cases_path.read_text(encoding='utf-8'))
    rule6 = "\n6. Continuidad y alcance: Para esta entrega el diff y los oráculos vigentes son suficientes para reanudar; no crees registros persistentes de seguimiento en odd/tasks/ ni uses todowrite para micro-pasos repetitivos. Implementa y verifica directamente."
    for task in cases['tasks']:
        if task['id'] == 'TASK-2' and rule6 not in task['task']:
            task['task'] += rule6
    cases_path.write_text(json.dumps(cases, ensure_ascii=False, indent=2), encoding='utf-8')
    shutil.copyfile(PACKAGE / 'protocolo.md', root / 'protocol.md')
    shutil.copyfile(Path(__file__).resolve(), root / 'runner.py')
    shutil.copyfile(REPO / 'tools/test_odd_standards_gemini38_v2.py', root / 'test_runner.py')
    base, _ = context(root)
    base.write_json(root / 'model-provenance.json', {
        'model': MODEL,
        'selection': 'Gemini 3.8 Flash via active OpenCode Copilot provider',
        'timeout_seconds': TIMEOUT,
        'temperature': 0.2,
        'protocol': PROTOCOL,
        'clean_cohort': True,
        'prior_cohorts_preserved': True
    }, exclusive=True)


def run(base, root):
    base.check_frozen(root)
    base.write_json(root / 'batch-start.json', {'started': base.stamp(), 'cells': 6}, exclusive=True)
    start = time.monotonic()
    completed, failures = [], []
    for repeat in (1, 2, 3):
        order = ARMS if repeat % 2 else tuple(reversed(ARMS))
        for arm in order:
            try:
                record = base.run_cell_full(root, 'TASK-2', arm, repeat)['phase1']
                completed.append(record['cell'])
                print(f"Cell finished: {record['cell']}, functional_pass: {record['functional_pass']}, seconds: {record['seconds']}", flush=True)
            except Exception as error:
                failures.append({'arm': arm, 'repeat': repeat, 'type': type(error).__name__, 'message': str(error)})
                print(f"Cell failed: {arm}-r{repeat}, error: {error}", flush=True)
                break
        base.write_json(root / f'repetition-{repeat}.json', {'completed': completed.copy(), 'errors': failures.copy()}, exclusive=True)
        if failures:
            break
    base.write_json(root / 'batch-result.json', {'wall_seconds': round(time.monotonic()-start, 3), 'completed': completed, 'errors': failures}, exclusive=True)
    if failures:
        raise SystemExit('Stopped at integration failure; no selective retries')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('command', choices=['prepare', 'reference', 'preflight', 'freeze', 'run', 'check'])
    parser.add_argument('--background', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    if args.background:
        assert args.command == 'run'
        child = subprocess.Popen([sys.executable, '-B', str(Path(__file__).resolve()), str(root), 'run'],
                                 cwd=REPO, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL, start_new_session=True)
        print(json.dumps({'pid': child.pid}))
        return
    if args.command == 'prepare':
        prepare(root)
        return
    base, old = context(root)
    if args.command == 'reference':
        old.validate_reference(base, root)
    elif args.command == 'preflight':
        source = inspect.getsource(base.preflight)
        before = "tools.get('read') and tools.get('edit') and tools.get('bash')"
        after = "tools.get('read') and (tools.get('edit') or tools.get('apply_patch')) and tools.get('bash')"
        if before in source:
            source = source.replace(before, after)
        probe = "'Sin red ni delegación. Responde PREFLIGHT_OK al terminar.')"
        replacement = "'Ejecuta el comando con workdir exactamente igual a ' + str(workspace) + '. Sin red ni delegación. Responde PREFLIGHT_OK al terminar.')"
        if probe in source:
            source = source.replace(probe, replacement)
        exec(source, base.__dict__)
        base.preflight(root)
    elif args.command == 'freeze':
        assert json.loads((root / 'reference-proof.json').read_text())['functional_pass']
        base.freeze(root)
    elif args.command == 'check':
        base.check_frozen(root)
        print('Gemini 3.8 v2 cohort inputs intact')
    else:
        run(base, root)


if __name__ == '__main__':
    main()
