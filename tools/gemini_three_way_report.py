#!/usr/bin/env python3
"""Offline analysis/export of all attempts; never changes cells or frozen input."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import statistics


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write('\n')


def aggregate(rows):
    tokens = [r['metrics']['comparable_tokens'] for r in rows if r['metrics'] is not None]
    seconds = [r['seconds'] for r in rows]
    return {'cells': len(rows), 'functional_pass': sum(r['functional_pass'] for r in rows),
            'conforming_delivery': sum(r['successful_delivery'] for r in rows),
            'healthy': sum(r['healthy'] for r in rows),
            'primary_loaded_by_content': sum(r['primary_loaded_by_content'] for r in rows),
            'seconds_sum': round(sum(seconds), 3),
            'seconds_median': round(statistics.median(seconds), 3) if seconds else None,
            'tokens_observed_sum': sum(tokens), 'tokens_median': statistics.median(tokens) if tokens else None,
            'missing_metrics': len(rows) - len(tokens),
            'metrics_observed': {k: sum(r['metrics'][k] for r in rows if r['metrics'] is not None)
                                  for k in ('input', 'output', 'cache_read', 'cache_write', 'reasoning', 'reported_cost')},
            'tools': sum(r['tools'] for r in rows), 'tool_errors': sum(r['tool_errors'] for r in rows),
            'steps': sum(r['steps'] for r in rows), 'invocations': sum(r['invocations'] for r in rows),
            'user_turns': sum(r['user_turns'] for r in rows),
            'timeouts': sum(any(r['timeouts']) for r in rows),
            'malformed_responses': sum(r['malformed_response'] for r in rows),
            'artifact_documents': sum(len(r['artifacts']) for r in rows),
            'sdd_modes': dict(Counter(r['selected_sdd_mode'] or 'none' for r in rows if r['arm'] == 'sdd'))}


def analyze(root, destination=None):
    repo = Path(__file__).resolve().parent.parent
    frozen = json.loads((root / 'freeze.json').read_text())
    cases = json.loads((root / 'cases.json').read_text())
    input_changes = []
    for name, value in frozen['inputs'].items():
        path = root / name if name.startswith(('profiles/', 'fixtures/', 'references/')) else repo / name
        if not path.exists() or sha(path) != value:
            input_changes.append(name)
    if sha(root / 'cases.json') != frozen['cases_sha256']:
        input_changes.append('cases.json')
    records = [json.loads(p.read_text()) for p in sorted((root / 'records').glob('*.json'))]
    preflight = json.loads((root / 'preflight.json').read_text())
    counts = Counter(r['cell'] for r in records)
    arms = ('developer', 'sdd', 'odd')
    summary = {'protocol': frozen['protocol'], 'model': frozen['model'], 'host': frozen['host'],
               'cells': len(records), 'expected': 90, 'frozen_inputs': len(frozen['inputs']),
               'input_changes': input_changes, 'duplicates': [name for name, count in counts.items() if count > 1],
               'arms': {arm: aggregate([r for r in records if r['arm'] == arm]) for arm in arms},
               'scenarios': {sid: {arm: aggregate([r for r in records if r['scenario'] == sid and r['arm'] == arm]) for arm in arms} for sid in cases},
               'repetitions': {str(repeat): {arm: aggregate([r for r in records if r['repetition'] == repeat and r['arm'] == arm]) for arm in arms} for repeat in (1, 2, 3)}}
    audits, stage_totals = [], {}
    token_check = {'steps_with_host_total': 0, 'host_total_sum': 0, 'mismatch_steps': 0}
    for r in records:
        tracefile = root / 'traces' / (r['cell'] + '.json')
        trace = json.loads(tracefile.read_text())
        for index, invocation in enumerate(trace['invocations']):
            reason = r['stages'][index]['reason']
            if r['arm'] == 'sdd' and index == 0 and r['scenario'] not in ('S08', 'S10'):
                reason = 'natural-depth-proposal'
            key = r['arm'] + ':' + reason
            totals = stage_totals.setdefault(key, {'invocations': 0, 'seconds': 0, 'tokens_observed': 0})
            totals['invocations'] += 1
            totals['seconds'] += invocation['seconds']
            for event in invocation['events']:
                if event['type'] == 'step_finish':
                    tokens = event.get('part', {}).get('tokens', {})
                    counted = sum(tokens.get(k, 0) for k in ('input', 'output')) + sum(tokens.get('cache', {}).get(k, 0) for k in ('read', 'write'))
                    totals['tokens_observed'] += counted
                    if 'total' in tokens:
                        token_check['steps_with_host_total'] += 1
                        token_check['host_total_sum'] += tokens['total']
                        token_check['mismatch_steps'] += tokens['total'] != counted
        tools = [e['part'] for inv in trace['invocations'] for e in inv['events'] if e.get('part', {}).get('type') == 'tool']
        first_source_write, first_red, last_green = None, None, None
        commands, failed_tools = [], []
        for i, tool in enumerate(tools):
            name, state = tool.get('tool'), tool.get('state', {})
            data = state.get('input', {})
            if state.get('status') == 'error':
                failed_tools.append({'tool': name, 'input': data, 'category': state.get('error_category')})
            if name in ('edit', 'write', 'apply_patch') and state.get('status') == 'completed':
                paths = [data.get('filePath', '')] + re.findall(r'^\*\*\* (?:Add|Update|Delete) File: (.+)$', data.get('patchText', ''), re.M)
                if first_source_write is None and any(p.endswith('.py') and not Path(p).name.startswith('test_') for p in paths):
                    first_source_write = i
            if name == 'bash':
                command, output = data.get('command', ''), state.get('output', '')
                is_test = 'python3 -m unittest' in command
                if is_test and first_red is None and re.search(r'FAILED \(|ERROR:', output):
                    first_red = i
                if is_test and re.search(r'\bOK\b', output):
                    last_green = i
                commands.append({'tool_index': i, 'command': command, 'status': state.get('status'), 'output': output})
        assertions_original = all(v['returncode'] == 0 for v in r['original_tests'].values())
        audit = {'cell': r['cell'], 'trace_hash_matches': sha(tracefile) == r['trace_sha256'],
                 'original_suite_count': len(r['original_tests']), 'original_tests_pass': assertions_original,
                 'read_search_calls': sum(p['tool'] in ('read', 'glob', 'grep', 'list') for p in tools),
                 'red_before_source_write': first_red is not None and first_source_write is not None and first_red < first_source_write,
                 'green_observed': last_green is not None,
                 'commands': commands, 'failed_tools': failed_tools,
                 'initial_read_only_stage_mutated': r['arm'] == 'sdd' and r['scenario'] not in ('S08', 'S10')
                    and r['stages'][0]['hashes'] != r['before_hashes'],
                 'qualification_notes': []}
        if r['arm'] == 'sdd' and r['selected_sdd_mode'] == 'direct' and r['scenario'] in ('S05', 'S07'):
            audit['qualification_notes'].append('Review Direct eligibility: public/shared CLI or persistence risk; source guards apply.')
        if r['arm'] == 'sdd' and r['scenario'] in ('S04', 'S07', 'S10') and re.search(r'Esfuerzo previsto del LLM\s*:\s*\d', r['output'].replace('*', '').replace('`', ''), re.I):
            audit['qualification_notes'].append('Feature effort score emitted for a bug/consultation; inspect source-contract compliance.')
        if r['arm'] == 'odd' and r['scenario'] in ('S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08') and not audit['red_before_source_write']:
            audit['qualification_notes'].append('No observed RED before product write; check meaningful exception to applicable test-first.')
        if r['arm'] == 'odd' and r['scenario'] == 'S08' and any(re.search(r'\[ \].*T2', value) for value in r['artifacts'].values()):
            audit['qualification_notes'].append('Seeded T2 remains unchecked in the final ODD record despite code delivery.')
        if r['arm'] == 'odd' and r['scenario'] in ('S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08') and not re.search(r'Risk\s*:', r['output'], re.I):
            audit['qualification_notes'].append('Final response lacks the prescribed Risk line; inspect local artifact for risk evidence.')
        if r['arm'] == 'developer' and r['scenario'] == 'S09' and any('py_compile' in c['command'] for c in commands):
            audit['qualification_notes'].append('PLAN invoked py_compile (bytecode side effect), though product source remained unchanged.')
        audits.append(audit)
    summary['invocation_stages'] = {key: {**value, 'seconds': round(value['seconds'], 3)} for key, value in stage_totals.items()}
    summary['token_total_crosscheck'] = token_check
    summary['audit'] = {'all_trace_hashes_match': all(a['trace_hash_matches'] for a in audits),
                        'read_search_calls': sum(a['read_search_calls'] for a in audits),
                        'original_suites_executed': sum(a['original_suite_count'] for a in audits),
                        'original_suites_failed_cells': [a['cell'] for a in audits if not a['original_tests_pass']],
                        'qualification_notes': {a['cell']: a['qualification_notes'] for a in audits if a['qualification_notes']},
                        'red_before_write_cells': {arm: sum(a['red_before_source_write'] for a in audits if ('-' + arm + '-') in a['cell']) for arm in arms},
                        'tool_error_cells': {a['cell']: a['failed_tools'] for a in audits if a['failed_tools']}}
    summary['audit']['inherited_custom_tools_exposed'] = {arm: [name for name, enabled in preflight[arm]['tools'].items()
        if enabled and name in ('google_search', 'antigravity_quota')] for arm in arms}
    summary['audit']['inherited_custom_tool_calls'] = {r['cell']: [name for name in r['tool_names']
        if name in ('google_search', 'antigravity_quota')] for r in records
        if any(name in ('google_search', 'antigravity_quota') for name in r['tool_names'])}
    summary['incomplete_or_nonconforming'] = {r['cell']: {
        'functional_pass': r['functional_pass'], 'healthy': r['healthy'], 'primary_loaded': r['primary_loaded_by_content'],
        'violations': r['flow_violations'], 'outside_accesses': r['outside_accesses'],
        'foreign_skills': r['foreign_skill_attempts'], 'errors': r['errors'], 'timeouts': r['timeouts']}
        for r in records if not r['successful_delivery']}
    summary['within_scenario_descriptive'] = {}
    for sid, groups in summary['scenarios'].items():
        eligible = {arm: group for arm, group in groups.items()
                    if group['cells'] == 3 and group['conforming_delivery'] == 3 and not group['missing_metrics']}
        summary['within_scenario_descriptive'][sid] = {
            'eligible_3_of_3': list(eligible),
            'lowest_median_tokens': min(eligible, key=lambda arm: eligible[arm]['tokens_median']) if eligible else None,
            'lowest_median_seconds': min(eligible, key=lambda arm: eligible[arm]['seconds_median']) if eligible else None,
            'interpretation': 'Descriptive n=3 only; inspect trade-offs and differences below 10%, not a universal winner.'}
    baseline = summary['arms']['developer']
    summary['observed_change_vs_developer_percent'] = {
        arm: {'tokens': round(100 * (value['tokens_observed_sum'] / baseline['tokens_observed_sum'] - 1), 3) if baseline['tokens_observed_sum'] else None,
              'seconds': round(100 * (value['seconds_sum'] / baseline['seconds_sum'] - 1), 3) if baseline['seconds_sum'] else None}
        for arm, value in summary['arms'].items()}
    if destination:
        assert not input_changes and not summary['duplicates']
        save(destination / 'freeze.json', frozen)
        save(destination / 'cases.json', cases)
        save(destination / 'records.json', records)
        save(destination / 'summary.json', summary)
        save(destination / 'audit.json', audits)
        portable_preflight = (root / 'preflight.json').read_text().replace(str(root), '<EXPERIMENT_ROOT>').replace(str(Path.home()), '<HOST_HOME>')
        save(destination / 'preflight.json', json.loads(portable_preflight))
        save(destination / 'oracles.json', json.loads((root / 'oracle-validation.json').read_text()))
        source_profiles = {str(p.relative_to(root)): p.read_text() for p in sorted((root / 'profiles').rglob('*.md'))}
        save(destination / 'profiles.json', source_profiles)
        save(destination / 'provenance.json', {
            'trace_location': str(root / 'traces'), 'traces': {p.name: sha(p) for p in sorted((root / 'traces').glob('*.json'))},
            'probe_traces': {p.name: sha(p) for p in sorted(root.glob('probe-*.json'))},
            'reporter_sha256': sha(Path(__file__).resolve()),
            'stage': 'Post-run analysis; acceptance and source fixtures were fixed before cells.',
            'preflight_export': 'Root and host-home paths normalized; raw resolved preflight retained externally.',
            'limitations': 'Complete tool traces external; profiles, final snapshots and command evidence retained. Provider config and cache not hermetic.'})
    compact_scenarios = {sid: {arm: {key: value[key] for key in ('cells', 'functional_pass', 'conforming_delivery', 'tokens_median', 'seconds_median', 'sdd_modes')}
                              for arm, value in groups.items()} for sid, groups in summary['scenarios'].items()}
    print(json.dumps({'cells': summary['cells'], 'input_changes': input_changes, 'arms': summary['arms'],
                      'change_vs_developer_percent': summary['observed_change_vs_developer_percent'],
                      'token_total_crosscheck': summary['token_total_crosscheck'],
                      'invocation_stages': summary['invocation_stages'], 'scenarios': compact_scenarios,
                      'audit': summary['audit'], 'incomplete_or_nonconforming': summary['incomplete_or_nonconforming']},
                     ensure_ascii=False, indent=2))
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('--export', type=Path)
    arguments = parser.parse_args()
    analyze(arguments.root.resolve(), arguments.export.resolve() if arguments.export else None)
