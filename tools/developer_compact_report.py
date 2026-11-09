#!/usr/bin/env python3
"""Offline, immutable export for the Developer prompt-only experiment."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

import developer_compact_benchmark as bench
from gemini_three_way_report import aggregate


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as file:
        json.dump(value, file, ensure_ascii=False, indent=2)
        file.write('\n')


def analyze(root, destination=None):
    bench.base.check_frozen(root)
    equivalence = bench.profile_equivalence(root)
    freeze = json.loads((root / 'freeze.json').read_text())
    cases = json.loads((root / 'cases.json').read_text())
    rows = [json.loads(p.read_text()) for p in sorted((root / 'records').glob('*.json'))]
    assert len({r['cell'] for r in rows}) == len(rows)
    groups = {arm: aggregate([r for r in rows if r['arm'] == arm]) for arm in bench.ARMS}
    scenarios = {sid: {arm: aggregate([r for r in rows if r['arm'] == arm and r['scenario'] == sid]) for arm in bench.ARMS} for sid in cases}
    repetitions = {str(repeat): {arm: aggregate([r for r in rows if r['arm'] == arm and r['repetition'] == repeat]) for arm in bench.ARMS} for repeat in (1, 2, 3)}
    audits = []
    token_check = {'steps': 0, 'host_total': 0, 'comparable': 0, 'reasoning': 0,
                   'host_differences_explained_by_reasoning': 0, 'unexplained_host_differences': 0}
    for row in rows:
        tracefile = root / 'traces' / (row['cell'] + '.json')
        trace = json.loads(tracefile.read_text())
        parts = [e['part'] for inv in trace['invocations'] for e in inv['events'] if e.get('part', {}).get('type') == 'tool']
        tools, commands, notes = [], [], []
        red, green, first_write = None, None, None
        for index, part in enumerate(parts):
            state, data = part.get('state', {}), part.get('state', {}).get('input', {})
            if state.get('status') == 'error':
                tools.append({'tool': part['tool'], 'input': data, 'category': state.get('error_category')})
            if part['tool'] in ('edit', 'write', 'apply_patch') and state.get('status') == 'completed':
                paths = [data.get('filePath', '')] + re.findall(r'^\*\*\* (?:Update|Add|Delete) File: (.+)$', data.get('patchText', ''), re.M)
                if first_write is None and any(name.endswith('.py') and not Path(name).name.startswith('test_') for name in paths):
                    first_write = index
            if part['tool'] == 'bash':
                command, output = data.get('command', ''), state.get('output', '')
                commands.append({'command': command, 'status': state.get('status'), 'output': output})
                if 'python3 -m unittest' in command:
                    if red is None and re.search(r'FAILED \(|ERROR:', output):
                        red = index
                    if re.search(r'\bOK\b', output):
                        green = index
        if row['arm'] in ('A', 'B') and row['scenario'] == 'S09' and any('py_compile' in c['command'] for c in commands):
            notes.append('PLAN invoked py_compile: bytecode side effect, although source did not change.')
        protected = [name for name in row['changed'] if name.startswith(('.architecture/', '.navigator/', '.data/', '.design/', '.quality/', '.security/'))
                     or name in ('AGENTS.md', 'TASK.md')]
        if protected:
            notes.append('Protected/context artifacts changed outside the fixture task: ' + ', '.join(protected))
        if row['arm'] == 'C' and cases[row['scenario']]['intent'] == 'implement' and row['scenario'] != 'S01':
            if not (red is not None and first_write is not None and red < first_write):
                notes.append('No RED before product write; inspect meaningful exception.')
            if not re.search(r'Risk\s*:', row['output'], re.I):
                notes.append('Final answer omits the prescribed Risk line; inspect artifacts for risk evidence.')
        if row['arm'] == 'C' and row['scenario'] == 'S08' and any(re.search(r'\[ \].*T2', text) for text in row['artifacts'].values()):
            notes.append('T2 still pending in ODD record despite code delivery.')
        for invocation in trace['invocations']:
            for event in invocation['events']:
                if event['type'] != 'step_finish':
                    continue
                tokens = event.get('part', {}).get('tokens', {})
                comparable = sum(tokens.get(k, 0) for k in ('input', 'output')) + sum(tokens.get('cache', {}).get(k, 0) for k in ('read', 'write'))
                reasoning = tokens.get('reasoning', 0)
                token_check['comparable'] += comparable
                token_check['reasoning'] += reasoning
                if 'total' in tokens:
                    token_check['steps'] += 1
                    token_check['host_total'] += tokens['total']
                    if tokens['total'] != comparable:
                        if tokens['total'] == comparable + reasoning:
                            token_check['host_differences_explained_by_reasoning'] += 1
                        else:
                            token_check['unexplained_host_differences'] += 1
        custom_calls = [part['tool'] for part in parts if part['tool'] in ('google_search', 'antigravity_quota')]
        audits.append({'cell': row['cell'], 'trace_hash_matches': sha(tracefile) == row['trace_sha256'],
                       'primary_loaded': row['primary_loaded_by_content'], 'outside_accesses': row['outside_accesses'],
                       'foreign_skills': row['foreign_skill_attempts'], 'custom_tool_calls': custom_calls,
                       'original_suite_count': len(row['original_tests']),
                       'original_suites_pass': all(v['returncode'] == 0 for v in row['original_tests'].values()),
                       'read_search_calls': sum(p['tool'] in ('read', 'glob', 'grep', 'list') for p in parts),
                       'red_before_write': red is not None and first_write is not None and red < first_write,
                       'green_observed': green is not None, 'commands': commands, 'tool_errors': tools, 'notes': notes,
                       'skill_loads': [{'tool_index': index, 'name': part.get('state', {}).get('input', {}).get('name')}
                                       for index, part in enumerate(parts) if part['tool'] == 'skill'],
                       'todo_calls': sum(part['tool'] == 'todowrite' for part in parts)})
    def delta(value, reference):
        return round(100 * (value / reference - 1), 3) if reference else None
    comparison = {arm: {'tokens_percent': delta(data['tokens_observed_sum'], groups['A']['tokens_observed_sum']),
                         'seconds_percent': delta(data['seconds_sum'], groups['A']['seconds_sum'])} for arm, data in groups.items()}
    favorable_scenarios = [sid for sid, data in scenarios.items() if data['B']['tokens_observed_sum'] < data['A']['tokens_observed_sum']]
    favorable_repetitions = [repeat for repeat, data in repetitions.items() if data['B']['tokens_observed_sum'] < data['A']['tokens_observed_sum']]
    controls = [r for r in rows if r['arm'] in ('A', 'B')]
    structural_quality = len(rows) == 90 and len(controls) == 60 and all(r['successful_delivery'] for r in controls)
    pattern_A = [a['cell'] for a in audits if '-A-' in a['cell'] and any('PLAN invoked' in note for note in a['notes'])]
    pattern_B = [a['cell'] for a in audits if '-B-' in a['cell'] and any('PLAN invoked' in note for note in a['notes'])]
    numerical_gate = (structural_quality and comparison['B']['tokens_percent'] <= -10 and comparison['B']['seconds_percent'] <= 10
                      and len(favorable_scenarios) >= 6 and len(favorable_repetitions) >= 2)
    summary = {'protocol': freeze['protocol'], 'model': freeze['model'], 'host': freeze['host'],
               'cells': len(rows), 'expected': 90, 'roles': bench.ROLES, 'frozen_inputs': len(freeze['inputs']),
               'equivalence': equivalence, 'arms': groups, 'scenarios': scenarios, 'repetitions': repetitions,
               'change_vs_A': comparison, 'token_crosscheck': token_check,
               'candidate_favorable_token_scenarios': favorable_scenarios,
               'candidate_favorable_token_repetitions': favorable_repetitions,
               'numerical_gate_passed': bool(numerical_gate),
               'interpretation': 'Numerical gate does not replace semantic review or authorize installation.',
               'plan_side_effect_alerts_A': pattern_A, 'plan_side_effect_alerts_B': pattern_B,
               'audit': {'trace_hashes_match': all(a['trace_hash_matches'] for a in audits),
                         'original_suites': sum(a['original_suite_count'] for a in audits),
                         'all_original_suites_pass': all(a['original_suites_pass'] for a in audits),
                         'read_search_calls': sum(a['read_search_calls'] for a in audits),
                         'red_before_write': {arm: sum(a['red_before_write'] for a in audits if ('-' + arm + '-') in a['cell']) for arm in bench.ARMS},
                         'todo_calls': {arm: sum(a['todo_calls'] for a in audits if ('-' + arm + '-') in a['cell']) for arm in bench.ARMS},
                         'notes': {a['cell']: a['notes'] for a in audits if a['notes']},
                         'tool_error_cells': {a['cell']: a['tool_errors'] for a in audits if a['tool_errors']},
                         'custom_tool_calls': {a['cell']: a['custom_tool_calls'] for a in audits if a['custom_tool_calls']}},
               'nonconforming_or_partial': {r['cell']: {'functional': r['functional_pass'], 'healthy': r['healthy'],
                    'violations': r['flow_violations'], 'errors': r['errors']} for r in rows if not r['successful_delivery']}}
    if destination:
        assert not destination.exists(), 'Export into a new directory; never overwrite evidence.'
        assert summary['audit']['trace_hashes_match']
        for name, value in [('freeze.json', freeze), ('cases.json', cases), ('records.json', rows),
                            ('summary.json', summary), ('audit.json', audits), ('equivalence.json', equivalence)]:
            save(destination / name, value)
        preflight = (root / 'preflight.json').read_text().replace(str(root), '<EXPERIMENT_ROOT>').replace(str(Path.home()), '<HOST_HOME>')
        save(destination / 'preflight.json', json.loads(preflight))
        save(destination / 'profiles.json', {str(p.relative_to(root)): p.read_text() for p in sorted((root / 'profiles').rglob('*.md'))})
        save(destination / 'oracles.json', json.loads((root / 'oracle-validation.json').read_text()))
        save(destination / 'provenance.json', {'traces_root': str(root / 'traces'),
            'trace_hashes': {p.name: sha(p) for p in sorted((root / 'traces').glob('*.json'))},
            'reporter_sha256': sha(Path(__file__).resolve()),
            'limitation': 'Offline, non-blinded audit. Raw traces external; profiles/final files/commands retained. Host-home/root paths normalized in exported preflight.'})
    compact_table = {sid: {arm: {key: value[key] for key in ('cells', 'functional_pass', 'tokens_median', 'seconds_median')}
                          for arm, value in data.items()} for sid, data in scenarios.items()}
    print(json.dumps({'cells': summary['cells'], 'arms': groups, 'change_vs_A': comparison,
                      'numerical_gate_passed': summary['numerical_gate_passed'],
                      'favorable_scenarios': favorable_scenarios, 'favorable_repetitions': favorable_repetitions,
                      'plan_alerts_A': pattern_A, 'plan_alerts_B': pattern_B,
                      'token_crosscheck': token_check, 'audit': summary['audit'],
                      'nonconforming_or_partial': summary['nonconforming_or_partial'], 'scenarios': compact_table}, ensure_ascii=False, indent=2))
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('--export', type=Path)
    args = parser.parse_args()
    analyze(args.root.resolve(), args.export.resolve() if args.export else None)
