#!/usr/bin/env python3
"""New GPT-6 Luna max cohort; preserve and reuse the historical ODD fixtures."""
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
PACKAGE = REPO / 'docs/experimentos/odd-estandares-gpt6-luna-max'
MODEL = 'openai/gpt-6-luna'
VARIANT = 'max'


def context(root):
    base, old = retry.context(root)
    base.MODEL = MODEL
    base.PROTOCOL = 'odd-standards-luna-max-v1'
    original_config, old_inputs = base.configuration, base.source_inputs

    def config(folder, arm, workspace, intent='implement'):
        result = original_config(folder, arm, workspace, intent)
        agent = result['agent'][base.agent_name(arm)]
        agent['model'] = MODEL
        agent.pop('temperature', None)
        return result
    base.configuration = config

    def inputs(folder):
        values = old_inputs(folder)
        values['model-provenance.json'] = base.sha(folder / 'model-provenance.json')
        for path in (Path(__file__).resolve(), PACKAGE / 'protocolo.md', REPO / 'tools/test_odd_standards_luna.py'):
            values[str(path)] = base.sha(path)
        return values
    base.source_inputs = inputs

    def invoke(folder, arm, workspace, prompt, session=None, limit=600):
        cfg = base.configuration(folder, arm, workspace)
        args = [base.CLI, 'run', '--format', 'json', '--model', MODEL, '--variant', VARIANT,
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
                'model_requested': MODEL, 'variant_requested': VARIANT,
                'config_sha256': base.text_sha(json.dumps(cfg, sort_keys=True))}
    base.invoke = invoke
    return base, old


def prepare(root):
    retry.prepare(root)
    shutil.copyfile(PACKAGE / 'protocolo.md', root / 'protocol.md')
    shutil.copyfile(Path(__file__).resolve(), root / 'runner.py')
    shutil.copyfile(REPO / 'tools/test_odd_standards_luna.py', root / 'test_runner.py')
    base, _ = context(root)
    base.write_json(root / 'model-provenance.json', {'model': MODEL, 'variant': VARIANT,
        'selection': 'explicit CLI --model and --variant on every invoke',
        'temperature': 'omitted: model capability false', 'not_pooled_with_gemini': True}, exclusive=True)


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
        assert source.count(before) == 1
        source = source.replace(before, after)
        probe = "'Sin red ni delegación. Responde PREFLIGHT_OK al terminar.')"
        replacement = "'Ejecuta el comando con workdir exactamente igual a ' + str(workspace) + '. Sin red ni delegación. Responde PREFLIGHT_OK al terminar.')"
        assert source.count(probe) == 1
        exec(source.replace(probe, replacement), base.__dict__)
        base.preflight(root)
    elif args.command == 'freeze':
        assert json.loads((root / 'reference-proof.json').read_text())['functional_pass']
        base.freeze(root)
    elif args.command == 'check':
        base.check_frozen(root)
        print('GPT Luna cohort inputs intact')
    else:
        retry.original.run(base, root)


if __name__ == '__main__':
    main()
