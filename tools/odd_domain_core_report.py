#!/usr/bin/env python3
"""Audit loaded criteria, not just short-core calls; report a single fresh pair."""
import argparse
import json
from pathlib import Path
import re

import odd_context_routing_report as basic
import odd_domain_core as experiment


def read_numbered_lines(output):
    content = output.split('<content>', 1)[-1].split('</content>', 1)[0]
    found = {}
    for line in content.splitlines():
        match = re.match(r'^[ \t]*(\d+)[:|] ?(.*)$', line)
        if match:
            found[int(match.group(1))] = match.group(2).rstrip()
    return found


def content_complete(expected, numbered, outputs):
    needed = {index: line.rstrip() for index, line in enumerate(expected.splitlines(), 1) if line.strip()}
    if needed and all(numbered.get(index) == line for index, line in needed.items()):
        return True
    if not numbered:
        normalized = re.sub(r'\s+', ' ', expected).strip()
        return any(normalized in re.sub(r'\s+', ' ', output) for output in outputs)
    return False


def inspect_reference(events, target, expected, workspace):
    target = target.resolve()
    numbered, outputs, verified_at, attempts = {}, [], None, 0
    for index, event in enumerate(events):
        part = event.get('part', {})
        state = part.get('state', {})
        value = state.get('input', {}).get('filePath')
        if part.get('tool') != 'read' or not value:
            continue
        path = Path(value) if Path(value).is_absolute() else workspace / value
        if path.resolve() != target:
            continue
        attempts += 1
        if state.get('status') != 'completed':
            continue
        output = state.get('output', '')
        outputs.append(output)
        numbered.update(read_numbered_lines(output))
        if verified_at is None and content_complete(expected, numbered, outputs):
            verified_at = index
    return {'attempts': attempts, 'completed_reads': len(outputs), 'full_content_verified': verified_at is not None,
            'verified_event_index': verified_at, 'observed_output_bytes': sum(len(output.encode()) for output in outputs)}


def first_product_write(events):
    for index, event in enumerate(events):
        part = event.get('part', {})
        state, tool = part.get('state', {}), part.get('tool')
        data = state.get('input', {})
        if tool in ('write', 'edit', 'apply_patch') and state.get('status') == 'completed':
            paths = [data.get('filePath', '')] + re.findall(r'^\*\*\* (?:Add|Update|Delete) File: (.+)$', data.get('patchText', ''), re.M)
            if any(Path(path).suffix in ('.py', '.html', '.css', '.js') and '/tests/' not in path and not Path(path).name.startswith('test_') for path in paths):
                return index
        if tool == 'bash' and 'manage.py makemigrations' in data.get('command', '') and '--dry-run' not in data['command']:
            return index
    return None


def analyze(root):
    result = basic.analyze(root)
    result['scenario'] = 'TASK-2 Alta; one fresh pair; primary standards ODD identical'
    result['experiment'] = 'Short domain core + lossless technical/documentary references'
    base, _ = experiment.context(root)
    for row in result['arms']:
        arm = row['arm']
        row['label'] = 'ODD ajustado + skills completas' if arm == 'odd' else 'Mismo ODD + núcleo/referencias de dominio'
        trace = json.loads((root / 'traces' / (row['cell'] + '.json')).read_text())
        events = [event for invocation in trace['invocations'] for event in invocation['events']]
        workspace = root / 'runs' / row['cell']
        first = first_product_write(events)
        domains = {}
        for domain in ('data-api', 'ui-design'):
            name = base.namespace(arm) + '-' + domain
            directory = root / 'profiles-v2' / arm / 'skills' / name
            expected_core = base.body((directory / 'SKILL.md').read_text())
            loaded = [index for index, event in enumerate(events)
                      if event.get('part', {}).get('tool') == 'skill'
                      and event['part'].get('state', {}).get('input', {}).get('name') == name
                      and expected_core in event['part'].get('state', {}).get('output', '')]
            data = {'skill_loaded_by_content': bool(loaded), 'skill_loaded_event_indices': loaded}
            if arm == 'odd':
                data['technical_criteria_verified'] = bool(loaded)
                data['criteria_before_product'] = bool(loaded and first is not None and min(loaded) < first)
                data['delivery'] = 'full skill body'
            else:
                for filename in ('implementation.md', 'documentation.md', 'original-contract.md'):
                    data[filename] = inspect_reference(events, directory / filename, (directory / filename).read_text(), workspace)
                candidates = [data[filename]['verified_event_index'] for filename in ('implementation.md', 'original-contract.md')
                              if data[filename]['full_content_verified']]
                data['technical_criteria_verified'] = bool(candidates)
                data['criteria_before_product'] = bool(candidates and first is not None and min(candidates) < first)
                data['delivery'] = 'core + technical reference or original fallback'
            domains[domain] = data
        row['domain_criteria_audit'] = domains
        row['criteria_preserved_in_context_before_product'] = all(data['skill_loaded_by_content'] and data['criteria_before_product'] for data in domains.values())
        record = json.loads((root / 'records' / (row['cell'] + '.json')).read_text())
        row['bootstrap_changes'] = [name for name in record['changed_files'] if name.startswith(('.data/', '.design/', '.architecture/', '.navigator/', '.sdd/'))]
        row['first_product_write_index'] = first
    comparison = result['comparison']
    if comparison is not None:
        treatment = next(row for row in result['arms'] if row['arm'] == 'adjusted')
        comparison.pop('favorable_exploratory_signal', None)
        comparison['core_token_delta_pct'] = comparison.pop('routed_token_delta_pct')
        comparison['core_time_delta_pct'] = comparison.pop('routed_time_delta_pct')
        comparison['criteria_references_verified_before_product'] = treatment['criteria_preserved_in_context_before_product']
        comparison['favorable_exploratory_signal'] = bool(
            all(row['functional_pass'] and row['healthy'] for row in result['arms'])
            and treatment['criteria_preserved_in_context_before_product'] and not treatment['bootstrap_changes']
            and comparison['core_token_delta_pct'] <= -10 + 1e-9 and comparison['core_time_delta_pct'] <= 10 + 1e-9)
    return result


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
