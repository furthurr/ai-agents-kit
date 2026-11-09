#!/usr/bin/env python3
"""One-pair routing analysis; no pooled historical comparisons."""
import argparse
import json
from pathlib import Path
import re

import odd_standards_report


def analyze(root):
    source = odd_standards_report.analyze(root)
    labels = {'odd': 'ODD ajustado (control)', 'adjusted': 'ODD ajustado + navegación selectiva'}
    records = {json.loads(path.read_text())['arm']: json.loads(path.read_text())
               for path in (root / 'records').glob('*.json')}
    details = []
    for arm, record in records.items():
        trace = json.loads((root / 'traces' / (record['cell'] + '.json')).read_text())
        parts = [event.get('part', {}) for invocation in trace['invocations'] for event in invocation['events']]
        rows = [row for row in source['behavior'] if row['arm'] == arm]
        read_bytes, search_bytes, skill_bytes = 0, 0, 0
        read_calls, search_calls = 0, 0
        for part in parts:
            state, tool = part.get('state', {}), part.get('tool')
            output = state.get('output', '')
            size = len(output.encode()) if isinstance(output, str) else 0
            if tool == 'read' and state.get('status') == 'completed':
                read_calls += 1
                read_bytes += size
            if tool in ('grep', 'glob', 'list') and state.get('status') == 'completed':
                search_calls += 1
                search_bytes += size
            if tool == 'skill' and state.get('status') == 'completed':
                skill_bytes += size
        reads = rows[0]['project_doc_reads'] if rows else []
        final_text = '\n'.join(event.get('part', {}).get('text', '')
                               for invocation in trace['invocations'] for event in invocation['events']
                               if event.get('type') == 'text')
        doc_lines = [line for line in final_text.splitlines()
                     if re.search(r'documentaci|documental|orchestrator|desactualiz|README', line, re.I)]
        details.append({'arm': arm, 'label': labels[arm], 'cell': record['cell'],
                        'functional_pass': record['functional_pass'],
                        'oracle_suite_pass': record['oracle_suite_pass'],
                        'combined_catalog_suite_pass': record['original_suite_pass'],
                        'healthy': record['healthy'], 'identity_verified': record['primary_loaded_by_content'],
                        'seconds': record['seconds'], 'metrics': record['metrics'],
                        'tools': record['tools_count'], 'steps': record['steps'],
                        'read_calls': read_calls, 'read_output_bytes': read_bytes,
                        'search_calls': search_calls, 'search_output_bytes': search_bytes,
                        'skill_output_bytes': skill_bytes,
                        'navigator_reads': [name for name in reads if name.startswith('.navigator/')],
                        'architecture_reads': [name for name in reads if name.startswith('.architecture/')],
                        'changed_map_files': [name for name in record['changed_files'] if name.startswith(('.navigator/', '.architecture/'))],
                        'changed_markdown': [name for name in record['changed_files'] if name.endswith('.md')],
                        'doc_close_mentions': doc_lines,
                        'explicit_documentation_orchestrator': 'documentation-orchestrator' in final_text,
                        'domains_loaded': rows[0]['domains_loaded_by_content'] if rows else [],
                        'both_domains_before_product': rows[0]['both_loaded_before_product'] if rows else False})
    comparison = None
    if len(details) == 2 and all(row['metrics'] for row in details):
        control = next(row for row in details if row['arm'] == 'odd')
        routed = next(row for row in details if row['arm'] == 'adjusted')
        tokens = (routed['metrics']['comparable_tokens'] / control['metrics']['comparable_tokens'] - 1) * 100
        duration = (routed['seconds'] / control['seconds'] - 1) * 100
        comparison = {'routed_token_delta_pct': tokens, 'routed_time_delta_pct': duration,
                      'both_functional': all(row['functional_pass'] for row in details),
                      'favorable_exploratory_signal': bool(all(row['functional_pass'] and row['healthy'] for row in details)
                          and routed['navigator_reads'] and routed['both_domains_before_product']
                          and not routed['changed_map_files'] and tokens <= -10 + 1e-9 and duration <= 10 + 1e-9)}
    return {'expected_cells': 2, 'observed_cells': len(details),
            'conversations_complete': len(details) == 2 and all(row['healthy'] for row in details),
            'scenario': 'TASK-2 Alta; one repetition per arm, exploratory',
            'arms': details, 'comparison': comparison, 'underlying': source,
            'bytes_note': 'Observed tool output bytes, not estimated tokens; SDK token counters kept separately'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    result = analyze(args.root)
    with args.destination.open('x') as file:
        json.dump(result, file, ensure_ascii=False, indent=2)
    print(json.dumps({key: result[key] for key in ('observed_cells', 'conversations_complete', 'arms', 'comparison')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
