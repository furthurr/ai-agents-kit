#!/usr/bin/env python3
"""Controlled prompt-only Developer ablation; leaves prior runners untouched."""
from __future__ import annotations

import argparse
import concurrent.futures
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess

REPO = Path(__file__).resolve().parent.parent
PACKAGE = REPO / 'docs/experimentos/developer-compacto-gemini-2026-11-04'
PROTOCOL = 'developer-compact-v1-20261104'
ARMS = ('A', 'B', 'C')
ROLES = {'A': 'Developer actual', 'B': 'Developer compacto', 'C': 'ODD referencia'}

spec = importlib.util.spec_from_file_location('compact_common', REPO / 'tools/gemini_three_way.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
original_configuration = base.configuration
original_inputs = base.source_inputs
original_seed = base.seed_resume


def namespace(arm):
    return 'dc' if arm in ('A', 'B') else 'do'


def skill_name(arm):
    return namespace(arm) + ('-developer' if arm in ('A', 'B') else '-odd-workflow')


def agent_name(arm):
    return 'dc-developer' if arm in ('A', 'B') else 'dc-odd'


def configuration(root, arm, workspace, intent='implement'):
    config = original_configuration(root, arm, workspace, intent)
    config['agent'][agent_name(arm)]['description'] = 'Perfil experimental controlado'
    return config


def source_inputs(root):
    values = original_inputs(root)
    for path in [Path(__file__).resolve(), REPO / 'tools/test_developer_compact_benchmark.py',
                 PACKAGE / 'candidato.md', REPO / 'canonical/shared/project-context.md',
                 REPO / 'canonical/shared/mas-identity.md']:
        values[str(path.relative_to(REPO))] = base.sha(path)
    return values


def seed_resume(workspace, arm):
    return original_seed(workspace, 'odd' if arm == 'C' else 'developer')


# Runtime adaptation only: never write to the imported source or installed MAS.
base.ARMS = ARMS
base.PROTOCOL = PROTOCOL
base.PACKAGE = PACKAGE
base.namespace = namespace
base.skill_name = skill_name
base.agent_name = agent_name
base.configuration = configuration
base.source_inputs = source_inputs
base.seed_resume = seed_resume


def namespace_text(text, arm, manifest):
    prefix = namespace(arm)
    for name in manifest['skills']:
        text = text.replace('name: ' + name + '\n', 'name: ' + prefix + '-' + name + '\n')
    # These identifiers are invoked skills; collaborators remain real agent names.
    for name in ('developer', 'data-api', 'ui-design', 'sdd-spec'):
        text = text.replace('`' + name + '`', '`' + prefix + '-' + name + '`')
    return text


def candidate_body():
    text = (PACKAGE / 'candidato.md').read_text().split('<!-- candidate:start -->')[1].split('<!-- candidate:end -->')[0].strip()
    replacements = {
        '{{project_context}}': (REPO / 'canonical/shared/project-context.md').read_text().strip(),
        '{{mas_identity}}': (REPO / 'canonical/shared/mas-identity.md').read_text().strip(),
        '{{developer_skill}}': 'dc-developer', '{{sdd_skill}}': 'dc-sdd-spec',
        '{{data_skill}}': 'dc-data-api', '{{ui_skill}}': 'dc-ui-design'}
    for token, value in replacements.items():
        text = text.replace(token, value)
    assert '{{' not in text
    return text


def profile_equivalence(root):
    a, b = root / 'profiles/A', root / 'profiles/B'
    assert base.hashes(a / 'skills') == base.hashes(b / 'skills'), 'A/B skills or references differ'
    aa, bb = (a / 'agent.md').read_text(), (b / 'agent.md').read_text()
    assert len(bb.encode()) < len(aa.encode()), 'Candidate is not shorter'
    ca = configuration(root, 'A', root / 'probe-fixture')
    cb = configuration(root, 'B', root / 'probe-fixture')
    ca['agent'][agent_name('A')].pop('prompt')
    cb['agent'][agent_name('B')].pop('prompt')
    xa = json.dumps(ca, sort_keys=True).replace(str(a), '<PROFILE>')
    xb = json.dumps(cb, sort_keys=True).replace(str(b), '<PROFILE>')
    assert xa == xb, 'A/B non-prompt configuration differs'
    return {'skills_and_references_identical': True, 'non_prompt_config_equivalent': True,
            'same_public_agent_and_skill_ids': agent_name('A') == agent_name('B') and skill_name('A') == skill_name('B'),
            'agent_bytes_A': len(aa.encode()), 'agent_bytes_B': len(bb.encode()),
            'agent_words_A': len(aa.split()), 'agent_words_B': len(bb.split()),
            'primary_skill_sha256_A': base.sha(a / 'skills' / skill_name('A') / 'SKILL.md'),
            'primary_skill_sha256_B': base.sha(b / 'skills' / skill_name('B') / 'SKILL.md')}


def prepare(root):
    if REPO == root or REPO in root.parents:
        raise SystemExit('Use a dedicated external root')
    root.mkdir(parents=True, exist_ok=True)
    if (root / 'profiles').exists():
        raise SystemExit('Never overwrite an existing experiment')
    manifest = json.loads((REPO / 'canonical/manifest.json').read_text())
    for arm in ARMS:
        profile = root / 'profiles' / arm
        for name in manifest['skills']:
            folder = profile / 'skills' / (namespace(arm) + '-' + name)
            shutil.copytree(REPO / 'generated/opencode/skills' / name, folder)
            for path in folder.rglob('*.md'):
                path.write_text(namespace_text(path.read_text(), arm, manifest))
        if arm == 'A':
            agent = namespace_text(base.body((REPO / 'generated/opencode/agents/developer.md').read_text()), arm, manifest)
        elif arm == 'B':
            agent = candidate_body()
        else:
            treatment = (REPO / 'docs/experimentos/odd-vs-sdd-2026-11-04/tratamiento-b.md').read_text()
            instructions = treatment.split('<!-- experimental-instructions:start -->')[1].split('<!-- experimental-instructions:end -->')[0].strip()
            instructions = namespace_text(instructions, arm, manifest)
            folder = profile / 'skills' / skill_name(arm)
            folder.mkdir()
            (folder / 'SKILL.md').write_text('---\nname: ' + skill_name(arm) + '\ndescription: ODD experimental inline con continuidad proporcional.\n---\n\n' + instructions + '\n')
            agent = ('Ejecutas ODD experimental adaptado al MAS, no SDD ni Developer. Carga y sigue `'
                     + skill_name(arm) + '` antes de actuar. No cambies de agente automáticamente.')
        agent += ('\n\nIdentidad técnica de laboratorio: ' + agent_name(arm) + '. La skill primaria es `'
                  + skill_name(arm) + '`. Conserva su metodología y los permisos del host.\n')
        (profile / 'agent.md').write_text(agent)
    cases, checks = base.load_cases(), {}
    for sid, case in cases.items():
        fixture = root / 'fixtures' / sid
        fixture.mkdir(parents=True)
        for name, value in case['files'].items():
            (fixture / name).write_text(value)
        env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
        baseline = base.run(['python3', '-c', case['oracle']], fixture, env=env)
        reference = root / 'references' / sid
        shutil.copytree(fixture, reference)
        for name, value in case['solution'].items():
            (reference / name).write_text(value)
        solved = base.run(['python3', '-c', case['oracle']], reference, env=env)
        assert solved.returncode == 0, (sid, solved.stderr)
        assert (baseline.returncode != 0) == bool(case['solution']), sid
        checks[sid] = {'baseline': baseline.returncode, 'reference': solved.returncode}
    base.write_json(root / 'cases.json', cases, exclusive=True)
    base.write_json(root / 'oracle-validation.json', checks, exclusive=True)
    equivalence = profile_equivalence(root)
    base.write_json(root / 'equivalence.json', equivalence, exclusive=True)
    print(json.dumps(equivalence, indent=2), flush=True)


def batch(root, repeats):
    base.check_frozen(root)
    profile_equivalence(root)
    if repeats != [1]:
        rows = [json.loads(p.read_text()) for p in (root / 'records').glob('*-r1.json')]
        assert len(rows) == 30
        assert not any(r['outside_accesses'] or r['foreign_skill_attempts'] or r['errors'] or any(r['timeouts']) for r in rows), 'Filter integration/access failure'
    orders = [('A', 'B', 'C'), ('B', 'C', 'A'), ('C', 'A', 'B'),
              ('C', 'B', 'A'), ('B', 'A', 'C'), ('A', 'C', 'B')]
    jobs = [(sid, arm, repeat) for repeat in repeats
            for index, sid in enumerate(json.loads((root / 'cases.json').read_text()))
            for arm in orders[(index + 2 * (repeat - 1)) % len(orders)]]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(base.cell, root, *job): job for job in jobs}
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                print(result['cell'], 'pass=' + str(result['functional_pass']),
                      'delivery=' + str(result['successful_delivery']), 'seconds=' + str(result['seconds']),
                      'tokens=' + str((result['metrics'] or {}).get('comparable_tokens')), flush=True)
            except Exception as error:
                job = futures[future]
                base.write_json(root / 'execution-errors' / ('-'.join(map(str, job)) + '.json'),
                                {'job': job, 'time': base.stamp(), 'error_type': type(error).__name__, 'message': str(error)}, exclusive=True)
                print('EXECUTION ERROR', job, type(error).__name__, flush=True)
    print('Batch finished', base.stamp(), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('action', choices=['prepare', 'probe', 'freeze', 'filter', 'replicate', 'launch-filter', 'launch-replicate'])
    args = parser.parse_args()
    root = args.root.resolve()
    if args.action == 'prepare':
        prepare(root)
    elif args.action in ('probe', 'freeze'):
        profile_equivalence(root)
        getattr(base, args.action)(root)
    elif args.action in ('filter', 'replicate'):
        batch(root, [1] if args.action == 'filter' else [2, 3])
    else:
        phase = args.action.removeprefix('launch-')
        log = (root / (phase + '.log')).open('x')
        process = subprocess.Popen([os.sys.executable, str(Path(__file__).resolve()), str(root), phase],
                                   stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        base.write_json(root / (phase + '-process.json'), {'pid': process.pid, 'time': base.stamp()}, exclusive=True)
        print('Launched', phase, 'pid', process.pid)


if __name__ == '__main__':
    main()
