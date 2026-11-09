#!/usr/bin/env python3
"""Four-arm report with honest native identity and content-verified domain calls."""
import argparse
import json
from pathlib import Path

import developer_v2_high_report as previous
import developer_v2_domains_build as adapter


def analyze(root):
    result = previous.analyze(root)
    native = json.loads((root / 'native-base.json').read_text())
    preflight = json.loads((root / 'preflight.json').read_text())
    native_verified = native.get('native') is True and not native.get('prompt_present') and preflight['build']['native'] is True and not preflight['build']['prompt_present']
    cells = [cell for cell in result['cells'] if cell['arm'] == 'build']
    result['arms']['build'] = {
        'cells': len(cells), 'expected': 3,
        'functional_pass': sum(cell['trajectory_functional_pass'] for cell in cells),
        'all_original_pass': all(cell['all_original_suites_pass'] for cell in cells),
        'healthy': bool(native_verified and all(cell['healthy'] for cell in cells)),
        'comparable_tokens': sum(cell['metrics']['comparable_tokens'] for cell in cells) if cells and all(cell['metrics'] for cell in cells) else None,
        'seconds': round(sum(cell['seconds'] for cell in cells), 3),
        'tools': sum(cell['tools'] for cell in cells), 'steps': sum(cell['steps'] for cell in cells),
        'user_turns': sum(cell['user_turns'] for cell in cells),
        'tool_errors': sum(len(cell['tool_errors']) for cell in cells),
        'native_identity_verified': native_verified, 'primary_skill': None}
    base, _ = adapter.context(root)
    consultations = []
    for file in sorted((root / 'records').glob('*.json')):
        record = json.loads(file.read_text())
        arm, label = record['arm'], record['cell']
        trace = json.loads((root / 'traces' / (label + '.json')).read_text())
        verified, counts = [], {}
        for domain in ('data-api', 'ui-design'):
            skill = base.namespace(arm) + '-' + domain
            expected = base.body((root / 'profiles-v2' / arm / 'skills' / skill / 'SKILL.md').read_text())
            calls = [event.get('part', {}).get('state', {}) for invocation in trace['invocations'] for event in invocation['events']
                     if event.get('part', {}).get('tool') == 'skill' and event['part'].get('state', {}).get('input', {}).get('name') == skill]
            counts[domain] = len(calls)
            if any(expected in state.get('output', '') for state in calls):
                verified.append(domain)
        canonical_prefixes = ('.data/', '.design/', '.architecture/', '.navigator/', '.sdd/')
        workspace = root / 'runs' / label
        doc_reads = []
        for invocation in trace['invocations']:
            for event in invocation['events']:
                part = event.get('part', {})
                state = part.get('state', {})
                path = state.get('input', {}).get('filePath', '')
                if part.get('tool') == 'read' and state.get('status') == 'completed' and path:
                    absolute = Path(path) if Path(path).is_absolute() else workspace / path
                    if workspace.resolve() in absolute.resolve().parents and absolute.suffix == '.md':
                        doc_reads.append(str(absolute.relative_to(workspace)) if workspace in absolute.parents else str(absolute))
        consultations.append({'cell': label, 'arm': arm, 'repeat': record['repetition'],
                              'loaded_domains_by_content': verified, 'domain_call_counts': counts,
                              'both_loaded': len(verified) == 2,
                              'canonical_changes': [name for name in record['changed_files'] if name.startswith(canonical_prefixes)],
                              'markdown_changes': [name for name in record['changed_files'] if name.endswith('.md')],
                              'project_document_reads': doc_reads,
                              'identity_verified': bool(native_verified if arm == 'build' else record['primary_loaded_by_content'])})
    result['domain_consultations'] = consultations
    for arm in adapter.ARMS:
        subset = [item for item in consultations if item['arm'] == arm]
        result['arms'][arm]['data_api_loaded'] = sum('data-api' in item['loaded_domains_by_content'] for item in subset)
        result['arms'][arm]['ui_design_loaded'] = sum('ui-design' in item['loaded_domains_by_content'] for item in subset)
        result['arms'][arm]['both_domains_loaded'] = sum(item['both_loaded'] for item in subset)
        result['arms'][arm]['canonical_change_cells'] = sum(bool(item['canonical_changes']) for item in subset)
    all_complete = all(result['arms'][arm]['cells'] == 3 and result['arms'][arm]['comparable_tokens'] for arm in adapter.ARMS)
    if all_complete:
        control = 'build'
        candidate = result['arms']['v2']
        other = result['arms'][control]
        tokens = (candidate['comparable_tokens'] / other['comparable_tokens'] - 1) * 100
        seconds = (candidate['seconds'] / other['seconds'] - 1) * 100
        wins = sum(next(cell for cell in result['cells'] if cell['arm'] == 'v2' and cell['repeat'] == repeat)['metrics']['comparable_tokens'] < next(cell for cell in result['cells'] if cell['arm'] == control and cell['repeat'] == repeat)['metrics']['comparable_tokens'] for repeat in (1, 2, 3))
        result['comparisons'][control] = {'v2_token_delta_pct': tokens, 'v2_time_delta_pct': seconds,
                                           'v2_token_wins': wins,
                                           'efficiency_threshold_pass': tokens <= -10 + 1e-9 and seconds <= 10 + 1e-9 and wins >= 2}
    result['expected_cells'] = 12
    result['complete'] = len(result['cells']) == 12 and all(cell['complete'] for cell in result['cells'])
    result['consultation_probes'] = json.loads((root / 'consultation-summary.json').read_text()) if (root / 'consultation-summary.json').exists() else None
    result['probe_note'] = 'Supplemental single-pass checks, not included in main task tokens/time; textual closure requires semantic review'
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    result = analyze(args.root)
    with args.destination.open('x') as file:
        json.dump(result, file, ensure_ascii=False, indent=2)
    print(json.dumps({key: result[key] for key in ('observed_cells', 'complete', 'arms', 'comparisons')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
