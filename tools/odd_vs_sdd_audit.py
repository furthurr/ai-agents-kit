#!/usr/bin/env python3
"""Post-run evidence audit/export; no inference and no modification of treatments."""
from __future__ import annotations

import ast
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def assertions(source):
    """Keep original assertion calls, ignoring formatting and enclosing class names."""
    return Counter(ast.dump(n, include_attributes=False) for n in ast.walk(ast.parse(source))
                   if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                   and n.func.attr.startswith('assert'))


def audit(root, destination):
    frozen = json.loads((root / 'freeze.json').read_text())
    repo = Path(__file__).resolve().parent.parent
    input_differences = {}
    for name, expected in frozen['inputs'].items():
        path = root / name if name.startswith(('profiles/', 'fixtures/')) else repo / name
        actual = sha(path) if path.exists() else None
        if actual != expected:
            input_differences[name] = {'expected': expected, 'actual': actual}
    for arm in ['A', 'B']:
        for p in (root / 'profiles' / arm).rglob('*'):
            if p.is_file() and 'node_modules' not in p.parts and (p.suffix == '.md' or p.name == 'opencode.json') and str(p.relative_to(root)) not in frozen['inputs']:
                input_differences[str(p.relative_to(root))] = {'new': True}
    records = [json.loads(p.read_text()) for p in sorted((root / 'records').glob('*.json'))]
    profile_maps = {arm: {name.removeprefix(f'profiles/{arm}/'): value for name, value in frozen['inputs'].items()
                          if name.startswith(f'profiles/{arm}/')} for arm in ['A', 'B']}
    differences = sorted(name for name in profile_maps['A'].keys() | profile_maps['B'].keys()
                         if profile_maps['A'].get(name) != profile_maps['B'].get(name))
    unexpected_differences = []
    for name in differences:
        if name == 'opencode/opencode.json':
            texts = [(root / 'profiles' / arm / name).read_text().replace(str(root / 'profiles' / arm), '<ARM>') for arm in ['A', 'B']]
            if texts[0] != texts[1]: unexpected_differences.append(name)
        elif name != 'opencode/agents/sdd.md' and not name.startswith('opencode/skills/sdd-spec/'):
            unexpected_differences.append(name)
    cells = []
    for r in records:
        workspace = root / 'runs' / r['cell']
        tracefile = root / 'traces' / (r['cell'] + '.json')
        trace = json.loads(tracefile.read_text())
        premature_gate4 = []
        if r['arm'] == 'A' and frozen['cases'][r['scenario']]['mode'] == 'tiny' and frozen['cases'][r['scenario']]['intent'] == 'implement':
            for index, invocation in enumerate(trace['invocations']):
                if any('Gate 4' in reply for reply in r['user_replies'][:index]):
                    continue
                for event in invocation['events']:
                    part = event.get('part', {})
                    if part.get('tool') not in {'apply_patch', 'edit', 'write'}:
                        continue
                    data = part.get('state', {}).get('input', {})
                    value = data.get('patchText') or data.get('newString') or data.get('content') or ''
                    additions = '\n'.join(line[1:] for line in value.splitlines() if line.startswith('+')) if data.get('patchText') else value
                    if re.search(r'(?:Estado[^\n]*(?<!no )(?<!No )[Cc]errad|Gate 4[^\n]*(?<!no )aprobado)', additions):
                        premature_gate4.append({'invocation': index + 1, 'tool_input': value})
        tools = [e['part'] for invocation in trace['invocations'] for e in invocation['events']
                 if e.get('part', {}).get('type') == 'tool']
        treatment_text = '\n'.join(p.get('state', {}).get('output', '') for p in tools
                                    if p.get('tool') == 'skill' and p.get('state', {}).get('input', {}).get('name') == 'sdd-spec')
        correct_treatment = ('ODD adaptado al MAS' in treatment_text) if r['arm'] == 'B' else ('Flujo SDD proporcional' in treatment_text)
        accesses, suspicious = [], []
        commands, product_writes = [], []
        for index, p in enumerate(tools):
            state = p.get('state', {})
            data = state.get('input', {})
            tool = p.get('tool')
            if tool in {'apply_patch', 'edit', 'write'}:
                patch = data.get('patchText') or data.get('patch') or ''
                paths = re.findall(r'^\*\*\* (?:Update|Add|Delete) File: (.+)$', patch, re.M)
                if not paths:
                    paths = [data.get('filePath', '')]
                if any(name.endswith('.py') and not Path(name).name.startswith('test_') for name in paths):
                    product_writes.append(index)
            if tool in {'read', 'glob', 'grep', 'list'}:
                value = data.get('filePath') or data.get('path')
                if value:
                    accesses.append({'tool': tool, 'path': value})
                    path = Path(value)
                    allowed = [workspace, root / 'profiles' / r['arm'] / 'opencode']
                    if path.is_absolute() and not any(path.resolve() == a.resolve() or a.resolve() in path.resolve().parents for a in allowed):
                        suspicious.append({'tool': tool, 'path': value})
            if tool == 'bash':
                output = state.get('output', '')
                is_test = 'python3 -m unittest' in (data.get('command') or '')
                commands.append({'tool_index': index, 'command': data.get('command'), 'status': state.get('status'),
                                 'red_observed': is_test and bool(re.search(r'FAILED \(|FAILED$|ERROR:', output)),
                                 'green_observed': is_test and bool(re.search(r'\bOK\b', output)),
                                 'output': output})
        preserved, original_runs = {}, {}
        for name, source in frozen['cases'][r['scenario']]['files'].items():
            if name.startswith('test_') and name.endswith('.py'):
                target = workspace / name
                try:
                    old, new = assertions(source), assertions(target.read_text()) if target.exists() else Counter()
                    preserved[name] = not bool(old - new)
                except SyntaxError:
                    preserved[name] = False
                proof = subprocess.run([sys.executable, '-c', source + '\nif __name__ == "__main__": unittest.main()\n'],
                                       cwd=workspace, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'},
                                       text=True, capture_output=True, timeout=30)
                original_runs[name] = {'returncode': proof.returncode, 'stdout': proof.stdout, 'stderr': proof.stderr}
        artifacts = r['artifacts']
        checks = {'trace_hash_matches': sha(tracefile) == r['trace_sha256'],
                  'no_visible_out_of_scope_access': not suspicious,
                  'original_tests_pass_unchanged': all(v['returncode'] == 0 for v in original_runs.values()),
                  'skill_loaded': r['skill_loaded'], 'functional_pass': r['functional_pass'],
                  'correct_treatment_loaded': correct_treatment,
                  'no_gate3_violation': not r['flow_violations'],
                  'no_premature_gate4_marker': not premature_gate4,
                  'no_forbidden_tools': not r['forbidden_tools'],
                  'no_timeout': not any(r['timeouts'])}
        if r['arm'] == 'A' and frozen['cases'][r['scenario']]['mode'] == 'tiny':
            checks['tiny_single_document'] = len(artifacts) == 1 and next(iter(artifacts)).endswith('/spec.md')
        if r['arm'] == 'A' and frozen['cases'][r['scenario']]['mode'] == 'lite':
            names = {Path(p).name for p in artifacts}
            checks['lite_four_documents'] = names in [
                {'requirements.md', 'design.md', 'tasks.md', 'verification.md'},
                {'bugfix.md', 'design.md', 'tasks.md', 'verification.md'}]
        cells.append({'cell': r['cell'], 'checks': checks, 'original_assertions': preserved,
                      'suspicious_accesses': suspicious, 'read_search_calls': len(accesses),
                      'commands': commands, 'artifact_paths': list(artifacts),
                      'original_test_runs': original_runs,
                      'red_before_product_write': bool(product_writes) and any(c['red_observed'] and c['tool_index'] < min(product_writes) for c in commands),
                      'product_write_tool_indices': product_writes,
                      'flow_violations': r['flow_violations']})
        cells[-1]['premature_gate4_markers'] = premature_gate4
    summary = {'cells': len(records), 'input_differences': input_differences,
               'profile_treatment_differences': differences,
               'unexpected_profile_differences': unexpected_differences,
               'trace_hashes_match': all(c['checks']['trace_hash_matches'] for c in cells),
               'suspicious_accesses': sum(len(c['suspicious_accesses']) for c in cells),
               'original_assertions_syntactic_match_cells': sum(all(c['original_assertions'].values()) for c in cells),
               'original_tests_pass_unchanged_cells': sum(c['checks']['original_tests_pass_unchanged'] for c in cells),
               'original_suites_executed': sum(len(c['original_test_runs']) for c in cells),
               'read_search_calls': sum(c['read_search_calls'] for c in cells),
               'check_failures': {c['cell']: [k for k, v in c['checks'].items() if not v] for c in cells if not all(c['checks'].values())},
               'red_green_cells': {arm: {'red_before_product': sum(c['red_before_product_write'] for c in cells if f'-{arm}-' in c['cell']),
                                         'red': sum(any(x['red_observed'] for x in c['commands']) for c in cells if f'-{arm}-' in c['cell']),
                                         'green': sum(any(x['green_observed'] for x in c['commands']) for c in cells if f'-{arm}-' in c['cell'])}
                                  for arm in ['A', 'B']}}
    summary['artifact_documents'] = {arm: sum(len(r['artifacts']) for r in records if r['arm'] == arm) for arm in ['A', 'B']}
    summary['nonzero_process_codes'] = {r['cell']: r['returncodes'] for r in records if any(code != 0 for code in r['returncodes'])}
    summary['duplicate_cells'] = [cell for cell, count in Counter(r['cell'] for r in records).items() if count > 1]
    complete_repetitions = []
    for repetition in [1, 2, 3]:
        rows = [r for r in records if r['repetition'] == repetition]
        if len(rows) == 20 and all(all(code == 0 for code in r['returncodes']) and r['metrics'] is not None and r['functional_pass'] for r in rows):
            complete_repetitions.append(repetition)
    clean_rows = [r for r in records if r['repetition'] in complete_repetitions]
    summary['complete_repetitions_only'] = {
        'repetitions': complete_repetitions, 'decision_use': 'descriptive only; full protocol incomplete',
        'arms': {arm: {'cells': sum(r['arm'] == arm for r in clean_rows),
                       'tokens': sum(r['metrics']['comparable_tokens'] for r in clean_rows if r['arm'] == arm),
                       'seconds': round(sum(r['seconds'] for r in clean_rows if r['arm'] == arm), 3),
                       'tools': sum(r['tool_count'] for r in clean_rows if r['arm'] == arm),
                       'steps': sum(r['steps'] for r in clean_rows if r['arm'] == arm),
                       'simulated_user_replies': sum(r['simulated_user_replies'] for r in clean_rows if r['arm'] == arm)} for arm in ['A', 'B']}}
    clean = summary['complete_repetitions_only']['arms']
    if clean['A']['tokens'] and clean['B']['tokens']:
        summary['complete_repetitions_only']['delta_B_vs_A_percent'] = {k: round(100 * (clean['B'][k] / clean['A'][k] - 1), 3) for k in ['tokens', 'seconds']}
    summary['error_sanitation'] = json.loads((root / 'error-sanitation.json').read_text()) if (root / 'error-sanitation.json').exists() else []
    summary['metrics_missing_cells'] = [r['cell'] for r in records if r['metrics'] is None]
    summary['by_selected_A_mode'] = {}
    for mode in ['direct', 'tiny', 'lite', 'read']:
        group = [r for r in records if ('read' if frozen['cases'][r['scenario']]['intent'] == 'read' else frozen['cases'][r['scenario']]['mode']) == mode]
        summary['by_selected_A_mode'][mode] = {arm: {
            'cells': sum(r['arm'] == arm for r in group),
            'tokens': sum((r['metrics'] or {}).get('comparable_tokens', 0) for r in group if r['arm'] == arm),
            'seconds': round(sum(r['seconds'] for r in group if r['arm'] == arm), 3)} for arm in ['A', 'B']}
    aggregates = {}
    for arm in ['A', 'B']:
        rows = [r for r in records if r['arm'] == arm]
        aggregates[arm] = {'tokens': sum((r['metrics'] or {}).get('comparable_tokens', 0) for r in rows),
                           'seconds': sum(r['seconds'] for r in rows)}
    if all(aggregates[arm]['tokens'] for arm in ['A', 'B']):
        key = 'delta_observed_all_attempts_not_comparable' if summary['metrics_missing_cells'] or summary['nonzero_process_codes'] else 'delta_B_vs_A_percent'
        summary[key] = {field: round(100 * (aggregates['B'][field] / aggregates['A'][field] - 1), 3) for field in ['tokens', 'seconds']}
    summary['favorable_scenarios_B'] = {}
    summary['favorable_repetitions_B'] = {}
    for key in ['tokens', 'seconds']:
        value = (lambda r: (r['metrics'] or {}).get('comparable_tokens', 0)) if key == 'tokens' else (lambda r: r['seconds'])
        for field, groups, target in [('scenario', sorted({r['scenario'] for r in records}), 'favorable_scenarios_B'),
                                      ('repetition', sorted({r['repetition'] for r in records}), 'favorable_repetitions_B')]:
            favorable = []
            for group in groups:
                total = {arm: sum(value(r) for r in records if r['arm'] == arm and r[field] == group) for arm in ['A', 'B']}
                if total['B'] < total['A']:
                    favorable.append(group)
            summary[target][key] = favorable
    save(root / 'audit.json', {'summary': summary, 'cells': cells})
    if destination:
        destination.mkdir(parents=True, exist_ok=True)
        save(destination / 'congelacion.json', frozen)
        metrics = json.loads((root / 'summary.json').read_text())
        metrics['coverage'] = {'metrics_missing_cells': summary['metrics_missing_cells'],
                               'execution_error_cells': list(summary['nonzero_process_codes']),
                               'aggregation': 'Observed counters only; null cell metrics are unknown, not zero. Do not use all-attempt totals for a complete-workload efficiency claim.',
                               'decision': 'Full protocol incomplete; descriptive complete repetitions in auditoria.json.'}
        save(destination / 'metricas.json', metrics)
        save(destination / 'celdas.json', records)
        save(destination / 'auditoria.json', {'summary': summary, 'cells': cells})
        save(destination / 'oraculos.json', json.loads((root / 'oracle-validation.json').read_text()))
        save(destination / 'errores-proveedor.json', summary['error_sanitation'])
        # Portable manifest/resolved configuration: remove temporary absolute prefixes.
        preflight = (root / 'preflight.json').read_text().replace(str(root), '<EXPERIMENT_ROOT>')
        save(destination / 'preflight.json', json.loads(preflight))
        save(destination / 'procedencia.json', {
            'audit_script_sha256': sha(Path(__file__).resolve()),
            'audit_stage': 'post-run; external functional oracles were frozen before execution',
            'external_trace_root': str(root / 'traces'),
            'traces': {p.name: sha(p) for p in sorted((root / 'traces').glob('*.json'))},
            'raw_probe_hashes': {p.name: sha(p) for p in sorted(root.glob('probe-*.json'))},
            'frozen_input_snapshot': frozen['inputs'],
            'limitations': 'Raw full traces external; tool command evidence and final changed files retained in celdas/auditoria.'})
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def incident(root, destination):
    records = [json.loads(p.read_text()) for p in sorted((root / 'records').glob('*.json'))]
    save(destination, {'status': 'abandoned infrastructure pilot, excluded from v2',
                       'freeze': json.loads((root / 'freeze.json').read_text()),
                       'records': records,
                       'not_started': {p.stem: json.loads(p.read_text()) for p in sorted((root / 'errors').glob('*.json'))},
                       'log': (root / 'filter.log').read_text()})
    print('Preserved incident:', len(records), 'completed cells, 16 pre-launch failures.')


def sanitize_errors(root):
    """Discard provider transport headers/bodies; retain only the typed failure.

    This is post-run output sanitation, never a treatment or metrics change.
    Original hashes survive as provenance, not copies of transport metadata.
    """
    if (root / 'error-sanitation.json').exists():
        raise SystemExit('Sanitation already recorded; preserve the original receipt.')
    receipts = []
    for tracefile in sorted((root / 'traces').glob('*.json')):
        original = sha(tracefile)
        trace = json.loads(tracefile.read_text())
        errors = []
        for invocation in trace['invocations']:
            for event in invocation['events']:
                if event.get('type') != 'error':
                    continue
                error = event.get('error', {})
                data = error.get('data', {})
                safe = {'name': error.get('name'), 'data': {k: data[k] for k in ['message', 'statusCode', 'isRetryable'] if k in data}}
                event['error'] = safe
                errors.append(safe)
        if not errors:
            continue
        save(tracefile, trace)
        recordfile = root / 'records' / tracefile.name
        record = json.loads(recordfile.read_text())
        record.setdefault('raw_trace_sha256_before_sanitation', original)
        record['trace_sha256'] = sha(tracefile)
        record['provider_errors'] = errors
        save(recordfile, record)
        receipts.append({'cell': tracefile.stem, 'before_sha256': original, 'after_sha256': sha(tracefile),
                         'provider_errors': errors, 'policy': 'Only name, message, statusCode, isRetryable retained.'})
    save(root / 'error-sanitation.json', receipts)
    print(json.dumps(receipts, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[2] == '--sanitize-errors':
        sanitize_errors(Path(sys.argv[1]).resolve())
    elif len(sys.argv) > 3 and sys.argv[3] == '--incident':
        incident(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
    else:
        audit(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None)
