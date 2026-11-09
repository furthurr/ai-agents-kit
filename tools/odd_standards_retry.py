#!/usr/bin/env python3
"""Independent full retry; keep the partial ODD cohort and its timeout immutable."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

import odd_standards_benchmark as original

REPO = original.REPO
PACKAGE = REPO / 'docs/experimentos/odd-estandares-reintento-gemini-2026-11-05'
PARTIAL = Path('/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/odd-standards-gemini-20261105').resolve()


def context(root):
    base, old = original.context(root)
    base.PROTOCOL = 'odd-standards-retry-v1-20261105'
    original_inputs = base.source_inputs

    def inputs(folder):
        result = original_inputs(folder)
        for name in ('retry-plan.json', 'prior-consultation-summary.json'):
            result[name] = base.sha(folder / name)
        for path in (Path(__file__).resolve(), PARTIAL / 'freeze.json', PACKAGE / 'protocolo.md'):
            result[str(path)] = base.sha(path)
        return result
    base.source_inputs = inputs
    return base, old


def prepare(root):
    assert not root.exists(), 'Never overwrite a retry or historical cohort'
    assert root != REPO and REPO not in root.parents
    previous, _ = original.context(PARTIAL)
    previous.check_frozen(PARTIAL)
    root.mkdir(parents=True)
    for folder in ('baseline', 'oracles', 'references', 'profiles-v2'):
        shutil.copytree(PARTIAL / folder, root / folder)
    for name in ('provenance.json', 'dependencies.lock.txt', 'oracle-validation-v3.json',
                 'cases.json', 'treatments.json', 'consultation_runner.py', 'probe-cases.json', 'adjusted-SKILL.md'):
        shutil.copyfile(PARTIAL / name, root / name)
    shutil.copyfile(PARTIAL / 'consultation-summary.json', root / 'prior-consultation-summary.json')
    shutil.copyfile(PACKAGE / 'protocolo.md', root / 'protocol.md')
    shutil.copyfile(Path(__file__).resolve(), root / 'runner.py')
    shutil.copyfile(REPO / 'tools/test_odd_standards_retry.py', root / 'test_runner.py')
    base, _ = context(root)
    base.write_json(root / 'retry-plan.json', {
        'protocol': base.PROTOCOL, 'prior_root': str(PARTIAL),
        'prior_freeze_sha256': base.sha(PARTIAL / 'freeze.json'),
        'prior_batch_sha256': base.sha(PARTIAL / 'batch-result.json'),
        'prior_status': 'partial; ODD original R2 timed out, snapshot functional',
        'strategy': 'six NEW cells, no substitution or pooling with partial cohort',
        'focused_checks': 'previous evidence only; not repeated',
        'same_timeouts_and_treatment': True}, exclusive=True)
    print('Fresh retry prepared; original partial inputs verified and preserved')


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
        base.preflight(root)
    elif args.command == 'freeze':
        assert json.loads((root / 'reference-proof.json').read_text())['functional_pass']
        base.freeze(root)
    elif args.command == 'check':
        base.check_frozen(root)
        original.context(PARTIAL)[0].check_frozen(PARTIAL)
        print('Retry and prior inputs intact')
    else:
        original.run(base, root)


if __name__ == '__main__':
    main()
