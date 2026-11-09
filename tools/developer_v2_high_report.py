#!/usr/bin/env python3
"""Report the new nine-cell cohort, never merge historical outcomes."""
import argparse
import json
from pathlib import Path
import re

import real_project_report


def analyze(root):
    source = real_project_report.collect(root)
    arms = {}
    for arm in ('developer', 'odd', 'v2'):
        cells = [cell for cell in source['cells'] if cell['arm'] == arm]
        arms[arm] = {
            'cells': len(cells), 'expected': 3,
            'functional_pass': sum(cell['trajectory_functional_pass'] for cell in cells),
            'all_original_pass': all(cell['all_original_suites_pass'] for cell in cells),
            'healthy': all(cell['healthy'] and cell['primary_loaded_by_content'] for cell in cells),
            'comparable_tokens': sum(cell['metrics']['comparable_tokens'] for cell in cells) if cells and all(cell['metrics'] for cell in cells) else None,
            'seconds': round(sum(cell['seconds'] for cell in cells), 3),
            'tools': sum(cell['tools'] for cell in cells),
            'steps': sum(cell['steps'] for cell in cells),
            'user_turns': sum(cell['user_turns'] for cell in cells),
            'tool_errors': sum(len(cell['tool_errors']) for cell in cells),
        }
    behavior = []
    for record_file in sorted((root / 'records').glob('*.json')):
        record = real_project_report.read_json(record_file)
        trace = real_project_report.read_json(root / 'traces' / (record['cell'] + '.json'))
        events = [event for result in trace['invocations'] for event in result['events']]
        first_write, first_red = None, None
        skills, reads, red_commands, green_commands, final_text = [], [], [], [], []
        for index, event in enumerate(events):
            part = event.get('part', {})
            state, tool = part.get('state', {}), part.get('tool')
            data = state.get('input', {})
            if tool == 'skill':
                skills.append(data.get('name'))
            if tool == 'read' and state.get('status') == 'completed':
                reads.append(data.get('filePath'))
            if tool in ('edit', 'write', 'apply_patch') and state.get('status') == 'completed':
                paths = [data.get('filePath', '')] + re.findall(r'^\*\*\* (?:Add|Update|Delete) File: (.+)$', data.get('patchText', ''), re.M)
                if any(Path(path).suffix in ('.py', '.html', '.css', '.js') and not ('/tests/' in path or Path(path).name.startswith('test_')) for path in paths):
                    if first_write is None:
                        first_write = index
            if tool == 'bash' and 'manage.py test' in data.get('command', ''):
                output = state.get('output', '')
                if re.search(r'FAILED|FAIL:|ERROR:', output):
                    red_commands.append(data['command'])
                    if first_red is None:
                        first_red = index
                if re.search(r'\bOK\b', output):
                    green_commands.append(data['command'])
            if tool == 'bash' and 'manage.py makemigrations' in data.get('command', '') and '--dry-run' not in data['command'] and first_write is None:
                first_write = index
            if event.get('type') == 'text':
                final_text.append(part.get('text', ''))
        behavior.append({
            'cell': record['cell'], 'arm': record['arm'], 'repeat': record['repetition'],
            'skill_calls': skills, 'read_count': len(reads),
            'project_doc_reads': [path for path in reads if path and (path.endswith('README.md') or path.endswith('lab-context.md'))],
            'markdown_changes': [path for path in record['changed_files'] if path.endswith('.md')],
            'agent_red_commands': red_commands, 'agent_green_commands': green_commands,
            'red_before_first_product_write_mechanical': first_red is not None and first_write is not None and first_red < first_write,
            'final_doc_mentions': [line for text in final_text for line in text.splitlines() if re.search(r'documentaci|orchestrator|desactualiz', line, re.I)],
            'first_product_write_index': first_write, 'first_red_index': first_red,
        })
    comparisons = {}
    if all(arms[arm]['cells'] == 3 and arms[arm]['comparable_tokens'] for arm in arms):
        for control in ('developer', 'odd'):
            tokens = (arms['v2']['comparable_tokens'] / arms[control]['comparable_tokens'] - 1) * 100
            seconds = (arms['v2']['seconds'] / arms[control]['seconds'] - 1) * 100
            wins = sum(next(cell for cell in source['cells'] if cell['arm'] == 'v2' and cell['repeat'] == repeat)['metrics']['comparable_tokens'] < next(cell for cell in source['cells'] if cell['arm'] == control and cell['repeat'] == repeat)['metrics']['comparable_tokens'] for repeat in (1, 2, 3))
            comparisons[control] = {'v2_token_delta_pct': tokens, 'v2_time_delta_pct': seconds,
                                    'v2_token_wins': wins,
                                    'efficiency_threshold_pass': tokens <= -10 + 1e-9 and seconds <= 10 + 1e-9 and wins >= 2}
    return {'expected_cells': 9, 'observed_cells': len(source['cells']),
            'complete': len(source['cells']) == 9 and all(cell['complete'] for cell in source['cells']),
            'arms': arms, 'comparisons': comparisons, 'cells': source['cells'], 'behavior': behavior,
            'execution_errors': source['execution_errors']}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    result = analyze(args.root)
    with args.destination.open('x') as file:
        json.dump(result, file, ensure_ascii=False, indent=2)
    print(json.dumps({key: result[key] for key in ('observed_cells', 'complete', 'arms', 'comparisons')}, indent=2))


if __name__ == '__main__':
    main()
