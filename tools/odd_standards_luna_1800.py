#!/usr/bin/env python3
"""Six fresh Luna max cells; extend symmetric timeout without touching prior cohort."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

import odd_standards_luna as luna

REPO = luna.REPO
PACKAGE = REPO / 'docs/experimentos/odd-estandares-gpt6-luna-max-1800'
PRIOR = Path('/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/odd-standards-luna-max-20261105-v3').resolve()
TIMEOUT = 1800


def context(root):
    base, old = luna.context(root)
    base.PROTOCOL = 'odd-standards-luna-max-1800-v1'
    original_invoke, original_inputs = base.invoke, base.source_inputs

    def invoke(folder, arm, workspace, prompt, session=None, limit=600):
        return original_invoke(folder, arm, workspace, prompt, session=session, limit=TIMEOUT)
    base.invoke = invoke

    def inputs(folder):
        result = original_inputs(folder)
        for path in (Path(__file__).resolve(), PACKAGE / 'protocolo.md', REPO / 'tools/test_odd_standards_luna_1800.py', PRIOR / 'freeze.json'):
            result[str(path)] = base.sha(path)
        result['budget.json'] = base.sha(folder / 'budget.json')
        return result
    base.source_inputs = inputs
    return base, old


def prepare(root):
    prior, _ = luna.context(PRIOR)
    prior.check_frozen(PRIOR)
    luna.prepare(root)
    shutil.copyfile(PACKAGE / 'protocolo.md', root / 'protocol.md')
    shutil.copyfile(Path(__file__).resolve(), root / 'runner.py')
    shutil.copyfile(REPO / 'tools/test_odd_standards_luna_1800.py', root / 'test_runner.py')
    base, _ = context(root)
    base.write_json(root / 'budget.json', {'timeout_per_invocation_seconds': TIMEOUT,
        'prior_timeout_seconds': 600, 'model': luna.MODEL, 'variant': luna.VARIANT,
        'prior_freeze_sha256': base.sha(PRIOR / 'freeze.json'), 'cohort': base.PROTOCOL}, exclusive=True)


def preflight(base, root):
    import inspect
    source = inspect.getsource(base.preflight)
    before = "tools.get('read') and tools.get('edit') and tools.get('bash')"
    after = "tools.get('read') and (tools.get('edit') or tools.get('apply_patch')) and tools.get('bash')"
    assert source.count(before) == 1
    source = source.replace(before, after)
    before = "'Sin red ni delegación. Responde PREFLIGHT_OK al terminar.')"
    after = "'Ejecuta el comando con workdir exactamente igual a ' + str(workspace) + '. Sin red ni delegación. Responde PREFLIGHT_OK al terminar.')"
    assert source.count(before) == 1
    exec(source.replace(before, after), base.__dict__)
    base.preflight(root)


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
        preflight(base, root)
    elif args.command == 'freeze':
        assert json.loads((root / 'reference-proof.json').read_text())['functional_pass']
        base.freeze(root)
    elif args.command == 'check':
        base.check_frozen(root)
        print('Inputs intact')
    else:
        luna.retry.original.run(base, root)


if __name__ == '__main__':
    main()
