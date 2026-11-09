#!/usr/bin/env python3
"""Descriptive original/adjusted ODD results, separate from previous cohorts."""
import argparse
import json
from pathlib import Path
import re

import real_project_report
import odd_standards_benchmark as adapter


def analyze(root):
    source = real_project_report.collect(root)
    base, _ = adapter.context(root)
    behavior = []
    for file in sorted((root / 'records').glob('*.json')):
        record = json.loads(file.read_text())
        arm, label = record['arm'], record['cell']
        trace = json.loads((root / 'traces' / (label + '.json')).read_text())
        events = [event for result in trace['invocations'] for event in result['events']]
        domain_indices = {}
        call_counts = {}
        for domain in ('data-api', 'ui-design'):
            name = base.namespace(arm) + '-' + domain
            expected = base.body((root / 'profiles-v2' / arm / 'skills' / name / 'SKILL.md').read_text())
            matches = [(index, event['part']['state']) for index, event in enumerate(events)
                       if event.get('part', {}).get('tool') == 'skill'
                       and event['part'].get('state', {}).get('input', {}).get('name') == name]
            call_counts[domain] = len(matches)
            domain_indices[domain] = [index for index, state in matches if expected in state.get('output', '')]
        first_write, first_red = None, None
        reads, doc_mentions = [], []
        workspace = (root / 'runs' / label).resolve()
        for index, event in enumerate(events):
            part = event.get('part', {})
            tool, state = part.get('tool'), part.get('state', {})
            data = state.get('input', {})
            if tool in ('write', 'edit', 'apply_patch') and state.get('status') == 'completed':
                paths = [data.get('filePath', '')] + re.findall(r'^\*\*\* (?:Add|Update|Delete) File: (.+)$', data.get('patchText', ''), re.M)
                if first_write is None and any(Path(path).suffix in ('.py', '.html', '.css') and '/tests/' not in path and not Path(path).name.startswith('test_') for path in paths):
                    first_write = index
            if tool == 'bash' and 'manage.py makemigrations' in data.get('command', '') and '--dry-run' not in data['command'] and first_write is None:
                first_write = index
            if tool == 'bash' and 'manage.py test' in data.get('command', '') and re.search(r'FAILED|FAIL:|ERROR:', state.get('output', '')) and first_red is None:
                first_red = index
            if tool == 'read' and state.get('status') == 'completed' and data.get('filePath'):
                path = Path(data['filePath'])
                path = path.resolve() if path.is_absolute() else (workspace / path).resolve()
                if workspace in path.parents and path.suffix == '.md':
                    reads.append(str(path.relative_to(workspace)))
            if event.get('type') == 'text':
                doc_mentions.extend(line for line in part.get('text', '').splitlines() if re.search(r'documentaci|orchestrator|desactualiz', line, re.I))
        loaded = [domain for domain, indices in domain_indices.items() if indices]
        behavior.append({'cell': label, 'arm': arm, 'repeat': record['repetition'],
                         'domains_loaded_by_content': loaded, 'domain_call_counts': call_counts,
                         'both_loaded_before_product': bool(first_write is not None and all(domain_indices[d] and min(domain_indices[d]) < first_write for d in domain_indices)),
                         'project_doc_reads': reads,
                         'markdown_changes': [name for name in record['changed_files'] if name.endswith('.md')],
                         'bootstrap_changes': [name for name in record['changed_files'] if name.startswith(('.data/', '.design/', '.architecture/', '.navigator/'))],
                         'red_before_first_product_write_mechanical': first_red is not None and first_write is not None and first_red < first_write,
                         'final_doc_mentions': doc_mentions})
    arms = {}
    for arm in adapter.ARMS:
        cells = [cell for cell in source['cells'] if cell['arm'] == arm]
        observed = [row for row in behavior if row['arm'] == arm]
        arms[arm] = {'cells': len(cells), 'expected': 3,
                     'functional_pass': sum(cell['trajectory_functional_pass'] for cell in cells),
                     'original_suites_pass': sum(cell['all_original_suites_pass'] for cell in cells),
                     'identity_and_process_ok': bool(cells) and all(cell['healthy'] and cell['primary_loaded_by_content'] for cell in cells),
                     'comparable_tokens': sum(cell['metrics']['comparable_tokens'] for cell in cells) if cells and all(cell['metrics'] for cell in cells) else None,
                     'seconds': round(sum(cell['seconds'] for cell in cells), 3),
                     'tools': sum(cell['tools'] for cell in cells), 'steps': sum(cell['steps'] for cell in cells),
                     'user_turns': sum(cell['user_turns'] for cell in cells),
                     'tool_errors': sum(len(cell['tool_errors']) for cell in cells),
                     'data_api_loaded': sum('data-api' in row['domains_loaded_by_content'] for row in observed),
                     'ui_design_loaded': sum('ui-design' in row['domains_loaded_by_content'] for row in observed),
                     'both_before_product': sum(row['both_loaded_before_product'] for row in observed),
                     'bootstrap_change_cells': sum(bool(row['bootstrap_changes']) for row in observed)}
    comparison = None
    if all(arms[arm]['cells'] == 3 and arms[arm]['comparable_tokens'] for arm in arms):
        comparison = {'adjusted_token_delta_pct': (arms['adjusted']['comparable_tokens'] / arms['odd']['comparable_tokens'] - 1) * 100,
                      'adjusted_time_delta_pct': (arms['adjusted']['seconds'] / arms['odd']['seconds'] - 1) * 100,
                      'adjusted_token_wins': sum(next(cell for cell in source['cells'] if cell['arm'] == 'adjusted' and cell['repeat'] == repeat)['metrics']['comparable_tokens'] < next(cell for cell in source['cells'] if cell['arm'] == 'odd' and cell['repeat'] == repeat)['metrics']['comparable_tokens'] for repeat in (1, 2, 3))}
    focused = json.loads((root / 'consultation-summary.json').read_text()) if (root / 'consultation-summary.json').exists() else None
    batch_errors = json.loads((root / 'batch-result.json').read_text()).get('errors', []) if (root / 'batch-result.json').exists() else []
    return {'expected_cells': 6, 'observed_cells': len(source['cells']),
            'complete': len(source['cells']) == 6 and all(cell['complete'] for cell in source['cells']),
            'arms': arms, 'comparison': comparison, 'cells': source['cells'], 'behavior': behavior,
            'focused_checks': focused, 'execution_errors': source['execution_errors'] + batch_errors}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    result = analyze(args.root)
    with args.destination.open('x') as file:
        json.dump(result, file, ensure_ascii=False, indent=2)
    print(json.dumps({key: result[key] for key in ('observed_cells', 'complete', 'arms', 'comparison')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
