#!/usr/bin/env python3
"""Descriptive report for frozen LocalLibrary trajectories; no model calls."""
import argparse
import json
from pathlib import Path
import re


def read_json(path):
    return json.loads(path.read_text())


def collect(root):
    records = [read_json(path) for path in sorted((root / 'records').glob('*.json'))]
    trajectories = {}
    for record in records:
        key = (record['task_id'], record['arm'], record['repetition'])
        trajectories.setdefault(key, []).append(record)
    cells = []
    for (task, arm, repeat), phases in sorted(trajectories.items()):
        phases.sort(key=lambda value: value['is_stage2'])
        expected_phases = 2 if task == 'TASK-3' else 1
        complete = len(phases) == expected_phases
        metrics_present = all(phase['metrics'] is not None for phase in phases)
        metrics = {key: sum(phase['metrics'].get(key, 0) for phase in phases)
                   for key in ('input', 'output', 'cache_read', 'cache_write', 'reasoning', 'comparable_tokens')} if metrics_present else None
        alerts = [alert for phase in phases for alert in phase['flow_violations']]
        docs, tests, skill_calls, tool_failures = [], [], [], []
        sessions = []
        for phase in phases:
            trace = read_json(root / 'traces' / (phase['cell'] + '.json'))
            for invocation in trace['invocations']:
                sessions.append(invocation['session'])
                for event in invocation['events']:
                    part = event.get('part', {})
                    state = part.get('state', {})
                    tool, data = part.get('tool'), state.get('input', {})
                    if tool == 'read':
                        path = data.get('filePath', '')
                        if path.endswith('.md'):
                            docs.append({'path': path, 'status': state.get('status')})
                    if tool == 'skill':
                        skill_calls.append({'name': data.get('name'), 'status': state.get('status')})
                    if tool == 'bash' and ('manage.py test' in data.get('command', '') or '-m unittest' in data.get('command', '')):
                        output = state.get('output', '')
                        tests.append({'command': data['command'], 'status': state.get('status'),
                                      'green_text': bool(re.search(r'\bOK\b', output)),
                                      'red_text': bool(re.search(r'FAILED|FAIL:|ERROR:', output))})
                    if tool and state.get('status') == 'error':
                        tool_failures.append({'tool': tool, 'category': state.get('error_category')})
        cells.append({'task': task, 'arm': arm, 'repeat': repeat,
                      'phases': [phase['cell'] for phase in phases], 'complete': complete,
                      'trajectory_functional_pass': complete and all(phase['functional_pass'] for phase in phases),
                      'final_functional_pass': complete and phases[-1]['functional_pass'],
                      'all_original_suites_pass': all(phase['original_suite_pass'] for phase in phases),
                      'healthy': all(phase['healthy'] for phase in phases),
                      'primary_loaded_by_content': all(phase['primary_loaded_by_content'] for phase in phases),
                      'flow_alerts_mechanical': alerts,
                      'outside_attempts': [attempt for phase in phases for attempt in phase['outside_accesses']],
                      'foreign_skill_attempts': [attempt for phase in phases for attempt in phase['foreign_skill_attempts']],
                      'forbidden_tool_attempts': [attempt for phase in phases for attempt in phase['forbidden_tool_attempts']],
                      'seconds': round(sum(phase['seconds'] for phase in phases), 3),
                      'metrics': metrics, 'tools': sum(phase['tools_count'] for phase in phases),
                      'steps': sum(phase['steps'] for phase in phases),
                      'user_turns': sum(phase['user_turns'] for phase in phases),
                      'selected_modes': [phase['selected_sdd_mode'] for phase in phases],
                      'phase_diagnostics': [{
                          'phase': phase['cell'], 'functional_pass': phase['functional_pass'],
                          'original_pass': phase['original_suite_pass'],
                          'oracle_count': phase['evaluation']['oracle_suite']['count'],
                          'failed_external_tests': re.findall(r'^(?:FAIL|ERROR): ([^\n]+)', phase['evaluation']['oracle_suite']['stderr'], re.M),
                          'external_summary': re.findall(r'^(?:Ran \d+ tests.*|FAILED.*|OK.*)$', phase['evaluation']['oracle_suite']['stderr'], re.M),
                      } for phase in phases],
                      'sessions': sessions, 'documentation_reads': docs,
                      'skill_calls': skill_calls, 'agent_test_commands': tests, 'tool_errors': tool_failures})
    arms = {}
    for arm in ('developer', 'sdd', 'odd'):
        selected = [cell for cell in cells if cell['arm'] == arm]
        arms[arm] = {'observed_cells': len(selected), 'expected_cells': 9,
                     'trajectory_pass': sum(cell['trajectory_functional_pass'] for cell in selected),
                     'final_pass': sum(cell['final_functional_pass'] for cell in selected),
                     'seconds_sum': round(sum(cell['seconds'] for cell in selected), 3),
                     'tools': sum(cell['tools'] for cell in selected),
                     'user_turns': sum(cell['user_turns'] for cell in selected),
                     'comparable_tokens': sum(cell['metrics']['comparable_tokens'] for cell in selected) if all(cell['metrics'] is not None for cell in selected) and selected else None}
    return {'expected_cells': 27, 'observed_cells': len(cells), 'phase_records': len(records),
            'complete_batch': len(cells) == 27 and all(cell['complete'] for cell in cells),
            'arms': arms, 'cells': cells,
            'attempts_started': len(list((root / 'attempts').glob('*.json'))),
            'execution_errors': [read_json(path) for path in sorted((root / 'execution-errors').glob('*.json'))]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    result = collect(args.root)
    with args.destination.open('x') as file:
        json.dump(result, file, ensure_ascii=False, indent=2)
    print(json.dumps({key: result[key] for key in ('observed_cells', 'phase_records', 'complete_batch', 'arms')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
