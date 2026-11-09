#!/usr/bin/env python3
"""One TASK-2 pair: standards ODD vs standards ODD with selective context routing."""
import argparse
import concurrent.futures
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

import odd_standards_luna_1800 as previous

REPO = previous.REPO
PACKAGE = REPO / 'docs/experimentos/odd-navigator-architecture-luna-max'
PRIOR = Path('/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/odd-standards-luna-max-1800-20261105').resolve()


def context(root):
    base, old = previous.context(root)
    base.PROTOCOL = 'odd-context-routing-luna-max-v1'
    original_inputs = base.source_inputs

    def inputs(folder):
        result = original_inputs(folder)
        for path in (Path(__file__).resolve(), PACKAGE / 'ruta-contexto.md', PACKAGE / 'protocolo.md',
                     REPO / 'tools/test_odd_context_routing.py', PRIOR / 'freeze.json'):
            result[str(path)] = base.sha(path)
        for file in (PACKAGE / 'fixtures').rglob('*.md'):
            result[str(file)] = base.sha(file)
        result['navigation-plan.json'] = base.sha(folder / 'navigation-plan.json')
        result['treatments.json'] = base.sha(folder / 'treatments.json')
        return result
    base.source_inputs = inputs
    return base, old


def prepare(root):
    prior, _ = previous.context(PRIOR)
    prior.check_frozen(PRIOR)
    previous.prepare(root)
    source = (PRIOR / 'profiles-v2/adjusted/skills/ob-odd-workflow/SKILL.md').read_text()
    control = source.replace('name: ob-odd-workflow\n', 'name: oa-odd-workflow\n').replace('`ob-data-api`', '`oa-data-api`').replace('`ob-ui-design`', '`oa-ui-design`')
    routed = source.rstrip() + '\n\n' + (PACKAGE / 'ruta-contexto.md').read_text().strip() + '\n'
    (root / 'profiles-v2/odd/skills/oa-odd-workflow/SKILL.md').write_text(control)
    (root / 'profiles-v2/adjusted/skills/ob-odd-workflow/SKILL.md').write_text(routed)
    (root / 'adjusted-SKILL.md').write_text(routed)
    for file in (PACKAGE / 'fixtures').rglob('*.md'):
        relative = file.relative_to(PACKAGE / 'fixtures')
        for target in (root / 'baseline' / relative, root / 'references/TASK-2' / relative):
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('x') as output:
                output.write(file.read_text())
    shutil.copyfile(PACKAGE / 'protocolo.md', root / 'protocol.md')
    shutil.copyfile(Path(__file__).resolve(), root / 'runner.py')
    shutil.copyfile(REPO / 'tools/test_odd_context_routing.py', root / 'test_runner.py')
    base, _ = context(root)
    base.write_json(root / 'budget.json', {'timeout_per_invocation_seconds': 1800, 'model': 'openai/gpt-6-luna',
                                         'variant': 'max', 'cohort': base.PROTOCOL})
    base.write_json(root / 'navigation-plan.json', {
        'control': 'ODD standards-adjusted previously tested; not original unadjusted ODD',
        'treatment': 'Same standards-adjusted body + ruta-contexto.md',
        'model': 'openai/gpt-6-luna', 'variant': 'max', 'cells': 2, 'repetitions_per_arm': 1,
        'same_maps_for_both': True, 'project_maps_are_fixture_not_kit_canonical': True,
        'prior_freeze_sha256': base.sha(PRIOR / 'freeze.json')}, exclusive=True)
    base.write_json(root / 'treatments.json', {
        'labels': {'odd': 'ODD ajustado con estándares (control)', 'adjusted': 'ODD ajustado + ruta selectiva de contexto'},
        'delta': 'ruta-contexto.md only; same standard skills and mapped project input',
        'sizes': {arm: {'agent_bytes': (root / 'profiles-v2' / arm / 'agent.md').stat().st_size,
                       'primary_skill_bytes': (root / 'profiles-v2' / arm / 'skills' / base.skill_name(arm) / 'SKILL.md').stat().st_size}
                  for arm in ('odd', 'adjusted')}})
    print('Prepared same mapped baseline for both standards ODD variants')


def run(base, root):
    base.check_frozen(root)
    base.write_json(root / 'batch-start.json', {'started': base.stamp(), 'cells': 2}, exclusive=True)
    start = time.monotonic()
    completed, errors = [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        jobs = {pool.submit(base.run_cell_full, root, 'TASK-2', arm, 1): arm for arm in ('odd', 'adjusted')}
        for future in concurrent.futures.as_completed(jobs):
            try:
                record = future.result()['phase1']
                completed.append(record['cell'])
            except Exception as error:
                errors.append({'arm': jobs[future], 'type': type(error).__name__, 'message': str(error)})
    base.write_json(root / 'batch-result.json', {'wall_seconds': round(time.monotonic()-start, 3), 'completed': completed, 'errors': errors}, exclusive=True)
    if errors:
        raise SystemExit('Partial pair; no selective retries')


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
        previous.preflight(base, root)
    elif args.command == 'freeze':
        assert json.loads((root / 'reference-proof.json').read_text())['functional_pass']
        base.freeze(root)
    elif args.command == 'check':
        base.check_frozen(root)
        print('Navigation cohort inputs intact')
    else:
        run(base, root)


if __name__ == '__main__':
    main()
