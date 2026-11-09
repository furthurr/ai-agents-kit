#!/usr/bin/env python3
"""Append-only ODD original/standards experiment; no historical source mutation."""
import argparse
import concurrent.futures
import inspect
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

from developer_v2_domains_build import module_at

REPO = Path(__file__).resolve().parent.parent
PACKAGE = REPO / 'docs/experimentos/odd-estandares-gemini-2026-11-05'
ARMS = ('odd', 'adjusted')


def helpers():
    return module_at('odd_standards_previous', REPO / 'tools/developer_v2_high_benchmark.py')


def context(root):
    old = helpers()
    base = old.load_source()
    base.LAB_ROOT = root.resolve()
    base.PYTHON_BIN = str(old.SOURCE / '.venv/bin/python')
    base.PROTOCOL = 'odd-standards-v1-20261105'
    base.ARMS = ARMS
    base.namespace = lambda arm: {'odd': 'oa', 'adjusted': 'ob'}[arm]
    base.skill_name = lambda arm: base.namespace(arm) + '-odd-workflow'
    base.agent_name = lambda arm: 'odd-standards-' + arm
    source_inputs = base.source_inputs

    def inputs(folder):
        result = source_inputs(folder)
        for name in ('consultation_runner.py', 'probe-cases.json', 'adjusted-SKILL.md'):
            result[name] = base.sha(folder / name)
        for path in (Path(__file__).resolve(), REPO / 'tools/developer_v2_high_benchmark.py',
                     REPO / 'tools/developer_v2_domains_build.py', old.SOURCE / 'runner.py', old.SOURCE / 'freeze.json',
                     PACKAGE / 'ajuste.md', REPO / 'docs/experimentos/odd-vs-sdd-2026-11-04/tratamiento-b.md'):
            result[str(path)] = base.sha(path)
        return result
    base.source_inputs = inputs
    return base, old


def historical_body():
    source = REPO / 'docs/experimentos/odd-vs-sdd-2026-11-04/tratamiento-b.md'
    return source.read_text().split('<!-- experimental-instructions:start -->')[1].split('<!-- experimental-instructions:end -->')[0].strip()


def composed_body(arm):
    text = historical_body()
    if arm == 'adjusted':
        text += '\n\n' + (PACKAGE / 'ajuste.md').read_text().strip()
    prefix = {'odd': 'oa', 'adjusted': 'ob'}[arm]
    return text.replace('`data-api`', '`' + prefix + '-data-api`').replace('`ui-design`', '`' + prefix + '-ui-design`')


def consultation_source():
    previous = module_at('odd_standards_probe_definitions', REPO / 'tools/developer_v2_domains_build.py')
    function = inspect.getsource(previous.run_consultation_probes)
    function = function.replace("'v2'", "'adjusted'").replace('"v2"', '"adjusted"')
    prefix = '''import json, re, shutil, subprocess
from pathlib import Path

def domain_loaded(base, root, results, domain):
    name = base.namespace('adjusted') + '-' + domain
    expected = base.body((root / 'profiles-v2/adjusted/skills' / name / 'SKILL.md').read_text())
    return any(event.get('part', {}).get('tool') == 'skill'
               and event['part'].get('state', {}).get('input', {}).get('name') == name
               and expected in event['part'].get('state', {}).get('output', '')
               for result in results for event in result['events'])

'''
    return prefix + function, previous.probe_definitions()


def prepare(base, old, root):
    assert root != REPO and REPO not in root.parents
    assert not root.exists(), 'Fresh root required'
    old.load_source().check_frozen(old.SOURCE)
    root.mkdir(parents=True)
    for folder in ('baseline', 'oracles'):
        shutil.copytree(old.SOURCE / folder, root / folder)
    shutil.copytree(old.SOURCE / 'references/TASK-2', root / 'references/TASK-2')
    for name in ('provenance.json', 'dependencies.lock.txt', 'oracle-validation-v3.json'):
        shutil.copyfile(old.SOURCE / name, root / name)
    for source, destination in ((PACKAGE / 'protocolo.md', 'protocol.md'),
                                (Path(__file__).resolve(), 'runner.py'),
                                (REPO / 'tools/test_odd_standards_benchmark.py', 'test_runner.py')):
        shutil.copyfile(source, root / destination)
    cases = json.loads((old.SOURCE / 'cases.json').read_text())
    cases['tasks'] = [case for case in cases['tasks'] if case['id'] == 'TASK-2']
    base.write_json(root / 'cases.json', cases, exclusive=True)
    manifest = json.loads((REPO / 'canonical/manifest.json').read_text())
    for arm in ARMS:
        profile = root / 'profiles-v2' / arm
        for sid in ('data-api', 'ui-design'):
            target = profile / 'skills' / (base.namespace(arm) + '-' + sid)
            shutil.copytree(REPO / 'generated/opencode/skills' / sid, target)
            for file in target.rglob('*.md'):
                file.write_text(old.substitute(file.read_text(), base.namespace(arm), manifest))
        primary = profile / 'skills' / base.skill_name(arm)
        primary.mkdir()
        text = '---\nname: ' + base.skill_name(arm) + '\ndescription: ODD experimental inline con continuidad proporcional.\n---\n\n' + composed_body(arm) + '\n'
        (primary / 'SKILL.md').write_text(text)
        agent = 'Ejecutas ODD experimental adaptado al MAS, no SDD ni Developer. Carga y sigue `' + base.skill_name(arm) + '` antes de actuar. No cambies de agente automáticamente.'
        agent += '\n\nIdentidad técnica de laboratorio: ' + base.agent_name(arm) + '. La skill primaria es `' + base.skill_name(arm) + '`. Conserva su metodología y los permisos del host.\n'
        (profile / 'agent.md').write_text(agent)
        if arm == 'adjusted':
            (root / 'adjusted-SKILL.md').write_text(text)
    probe_source, probe_cases = consultation_source()
    (root / 'consultation_runner.py').write_text(probe_source)
    base.write_json(root / 'probe-cases.json', probe_cases, exclusive=True)
    base.write_json(root / 'treatments.json', {
        'arms': ARMS, 'delta': 'Historical body unchanged + ajuste.md; namespaces only',
        'sizes': {arm: {'agent_bytes': (root / 'profiles-v2' / arm / 'agent.md').stat().st_size,
                       'primary_skill_bytes': (root / 'profiles-v2' / arm / 'skills' / base.skill_name(arm) / 'SKILL.md').stat().st_size} for arm in ARMS},
        'probe_adaptation': 'Previous five generic fixtures; only actor v2→adjusted and domain loader namespace changed'}, exclusive=True)
    print('Prepared two ODD profiles and five focused cases')


def run(base, root):
    base.check_frozen(root)
    base.write_json(root / 'batch-start.json', {'started': base.stamp(), 'cells': 6}, exclusive=True)
    start = time.monotonic()
    completed, failures = [], []
    for repeat in (1, 2, 3):
        order = ARMS if repeat % 2 else tuple(reversed(ARMS))
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            jobs = {pool.submit(base.run_cell_full, root, 'TASK-2', arm, repeat): arm for arm in order}
            for future in concurrent.futures.as_completed(jobs):
                try:
                    record = future.result()['phase1']
                    completed.append(record['cell'])
                except Exception as error:
                    failures.append({'arm': jobs[future], 'repeat': repeat, 'type': type(error).__name__, 'message': str(error)})
        base.write_json(root / f'repetition-{repeat}.json', {'completed': completed.copy(), 'errors': failures.copy()}, exclusive=True)
        if failures:
            break
    base.write_json(root / 'batch-result.json', {'wall_seconds': round(time.monotonic()-start, 3), 'completed': completed, 'errors': failures}, exclusive=True)
    if failures:
        raise SystemExit('Stopped at integration failure; no selective retries')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('command', choices=['prepare', 'reference', 'preflight', 'freeze', 'probes', 'run', 'check'])
    parser.add_argument('--background', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    if args.background:
        assert args.command in ('probes', 'run')
        child = subprocess.Popen([sys.executable, '-B', str(Path(__file__).resolve()), str(root), args.command],
                                 cwd=REPO, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL, start_new_session=True)
        print(json.dumps({'pid': child.pid}))
        return
    base, old = context(root)
    if args.command == 'prepare':
        prepare(base, old, root)
    elif args.command == 'reference':
        old.validate_reference(base, root)
    elif args.command == 'preflight':
        base.preflight(root)
    elif args.command == 'freeze':
        assert json.loads((root / 'reference-proof.json').read_text())['functional_pass']
        base.freeze(root)
    elif args.command == 'check':
        base.check_frozen(root)
        print('Frozen inputs intact')
    elif args.command == 'probes':
        module_at('odd_standards_focused_runtime', root / 'consultation_runner.py').run_consultation_probes(base, root)
    else:
        run(base, root)


if __name__ == '__main__':
    main()
