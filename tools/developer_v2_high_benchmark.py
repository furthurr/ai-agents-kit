#!/usr/bin/env python3
"""Isolated new-cohort adapter for the verified LocalLibrary TASK-2 runner.

Overrides affect a private imported module instance, never historical files/config.
"""
import argparse
import concurrent.futures
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

REPO = Path('/Users/pedrogomezvasquez/Documents/Repositorios/GITHUBREPOS/ai-agents-kit')
SOURCE = Path('/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/real-project-gemini-20261104').resolve()
PACKAGE = REPO / 'docs/experimentos/developer-v2-alta-gemini-2026-11-05'
ARMS = ('developer', 'odd', 'v2')


def load_source():
    spec = importlib.util.spec_from_file_location('v2_private_source', SOURCE / 'runner.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def context(root):
    base = load_source()
    base.LAB_ROOT = root.resolve()
    base.PYTHON_BIN = str(SOURCE / '.venv/bin/python')
    base.PROTOCOL = 'v2-high-v1-20261105'
    base.ARMS = ARMS
    base.namespace = lambda arm: {'developer': 'hdev', 'odd': 'hodd', 'v2': 'hv2'}[arm]
    base.skill_name = lambda arm: base.namespace(arm) + '-' + {
        'developer': 'developer', 'odd': 'odd-workflow', 'v2': 'developer-v2'}[arm]
    base.agent_name = lambda arm: 'high-' + arm
    source_inputs = base.source_inputs

    def inputs(folder):
        result = source_inputs(folder)
        result.update({'adapter-source': base.sha(Path(__file__).resolve()),
                       'historical-runner-source': base.sha(SOURCE / 'runner.py'),
                       'historical-freeze': base.sha(SOURCE / 'freeze.json')})
        result.update({'candidate/' + str(path.relative_to(PACKAGE / 'candidato')): base.sha(path)
                       for path in (PACKAGE / 'candidato').rglob('*.md')})
        return result
    base.source_inputs = inputs
    return base


def substitute(text, namespace, manifest):
    for sid in manifest['skills']:
        text = text.replace('name: ' + sid + '\n', 'name: ' + namespace + '-' + sid + '\n')
        text = text.replace('name: "' + sid + '"\n', 'name: "' + namespace + '-' + sid + '"\n')
        text = text.replace('`' + sid + '`', '`' + namespace + '-' + sid + '`')
    return text.replace('`sdd`', '`high-sdd`').replace('`developer`', '`high-developer`')


def prepare(base, root):
    assert root != REPO and REPO not in root.parents
    assert not root.exists(), 'Use a new laboratory, never overwrite'
    source = load_source()
    source.check_frozen(SOURCE)
    root.mkdir(parents=True)
    for folder in ('baseline', 'oracles'):
        shutil.copytree(SOURCE / folder, root / folder)
    shutil.copytree(SOURCE / 'references/TASK-2', root / 'references/TASK-2')
    for name in ('provenance.json', 'dependencies.lock.txt', 'oracle-validation-v3.json'):
        shutil.copyfile(SOURCE / name, root / name)
    shutil.copyfile(PACKAGE / 'protocolo.md', root / 'protocol.md')
    shutil.copyfile(Path(__file__).resolve(), root / 'runner.py')
    shutil.copyfile(REPO / 'tools/test_developer_v2_high_benchmark.py', root / 'test_runner.py')
    cases = json.loads((SOURCE / 'cases.json').read_text())
    cases['tasks'] = [case for case in cases['tasks'] if case['id'] == 'TASK-2']
    base.write_json(root / 'cases.json', cases, exclusive=True)
    manifest = json.loads((REPO / 'canonical/manifest.json').read_text())
    for arm in ARMS:
        profile = root / 'profiles-v2' / arm
        skills = profile / 'skills'
        for sid in manifest['skills']:
            target = skills / (base.namespace(arm) + '-' + sid)
            shutil.copytree(REPO / 'generated/opencode/skills' / sid, target)
            for file in target.rglob('*.md'):
                file.write_text(substitute(file.read_text(), base.namespace(arm), manifest))
        if arm == 'developer':
            agent = substitute(base.body((REPO / 'generated/opencode/agents/developer.md').read_text()), base.namespace(arm), manifest)
        elif arm == 'odd':
            treatment = (REPO / 'docs/experimentos/odd-vs-sdd-2026-11-04/tratamiento-b.md').read_text()
            skill = treatment.split('<!-- experimental-instructions:start -->')[1].split('<!-- experimental-instructions:end -->')[0].strip()
            skill = skill.replace('`data-api`', '`hodd-data-api`').replace('`ui-design`', '`hodd-ui-design`')
            target = skills / base.skill_name(arm)
            target.mkdir()
            (target / 'SKILL.md').write_text('---\nname: ' + base.skill_name(arm) + '\ndescription: ODD experimental inline con continuidad proporcional.\n---\n\n' + skill + '\n')
            agent = 'Ejecutas ODD experimental adaptado al MAS, no SDD ni Developer. Carga y sigue `' + base.skill_name(arm) + '` antes de actuar. No cambies de agente automáticamente.'
        else:
            replacements = {'__SKILL__': base.skill_name(arm), '__DATA_API__': 'hv2-data-api', '__UI_DESIGN__': 'hv2-ui-design'}
            agent = (PACKAGE / 'candidato/agent.md').read_text().strip()
            skill = (PACKAGE / 'candidato/SKILL.md').read_text()
            for before, after in replacements.items():
                agent, skill = agent.replace(before, after), skill.replace(before, after)
            target = skills / base.skill_name(arm)
            target.mkdir()
            (target / 'SKILL.md').write_text(skill)
        agent += '\n\nIdentidad técnica de laboratorio: ' + base.agent_name(arm) + '. La skill primaria es `' + base.skill_name(arm) + '`. Conserva su metodología y los permisos del host.\n'
        (profile / 'agent.md').write_text(agent)
    sizes = {arm: {'agent_bytes': (root / 'profiles-v2' / arm / 'agent.md').stat().st_size,
                   'primary_skill_bytes': (root / 'profiles-v2' / arm / 'skills' / base.skill_name(arm) / 'SKILL.md').stat().st_size} for arm in ARMS}
    base.write_json(root / 'treatments.json', {'arms': ARMS, 'source_lab': str(SOURCE), 'sizes': sizes}, exclusive=True)
    print(json.dumps(sizes, indent=2))


def validate_reference(base, root):
    proof = base.evaluate_cell(root, 'reference-proof', root / 'references/TASK-2', 'TASK-2')
    base.write_json(root / 'reference-proof.json', proof, exclusive=True)
    assert proof['functional_pass'], proof
    print('Reference passed: original43 + external9')


def run(base, root):
    base.check_frozen(root)
    base.write_json(root / 'batch-start.json', {'started': base.stamp(), 'cells': 9}, exclusive=True)
    started = time.monotonic()
    completed = []
    for repeat in (1, 2, 3):
        order = ARMS[repeat - 1:] + ARMS[:repeat - 1]
        failures = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            jobs = {pool.submit(base.run_cell_full, root, 'TASK-2', arm, repeat): arm for arm in order}
            for future in concurrent.futures.as_completed(jobs):
                arm = jobs[future]
                try:
                    record = future.result()['phase1']
                    completed.append(record['cell'])
                    print(record['cell'], record['functional_pass'], record['seconds'], flush=True)
                except Exception as error:
                    failures.append({'arm': arm, 'repeat': repeat, 'type': type(error).__name__, 'message': str(error)})
        base.write_json(root / f'repetition-{repeat}.json', {'completed': completed.copy(), 'errors': failures}, exclusive=True)
        if failures:
            break
    base.write_json(root / 'batch-result.json', {'wall_seconds': round(time.monotonic() - started, 3), 'completed': completed, 'errors': failures}, exclusive=True)
    if failures:
        raise SystemExit('Stopped after integration failure. No selective retries.')


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
    base = context(root)
    if args.command == 'prepare':
        prepare(base, root)
    elif args.command == 'reference':
        validate_reference(base, root)
    elif args.command == 'preflight':
        base.preflight(root)
    elif args.command == 'freeze':
        assert json.loads((root / 'reference-proof.json').read_text())['functional_pass']
        base.freeze(root)
    elif args.command == 'check':
        base.check_frozen(root)
        print('Frozen inputs intact')
    else:
        run(base, root)


if __name__ == '__main__':
    main()
