#!/usr/bin/env python3
"""Bounded four-invocation experiment; complete domain skills, one scheduling delta."""
import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import queue
import shutil
import signal
import subprocess
import sys
import threading
import time

import odd_standards_luna_1800 as prior_adapter
import preserve_real_project_lab as preservation

REPO = Path(__file__).resolve().parent.parent
PACKAGE = REPO / 'docs/experimentos/odd-batching-luna-max'
PRIOR = Path('/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/odd-standards-luna-max-1800-20261105').resolve()
SOURCE = Path('/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/real-project-gemini-20261104').resolve()
MODEL, VARIANT, PROTOCOL = 'openai/gpt-6-luna', 'max', 'odd-batching-luna-max-v1'
TOKEN_LIMIT, STEP_LIMIT, TIMEOUT, CALL_LIMIT = 5_000_000, 60, 1800, 4


def metric(part):
    tokens = part.get('tokens', {})
    cache = tokens.get('cache', {})
    keys = ('input', 'output', 'reasoning')
    if not all(isinstance(tokens.get(k), (int, float)) for k in keys):
        return None
    if not all(isinstance(cache.get(k), (int, float)) for k in ('read', 'write')):
        return None
    values = {k: tokens[k] for k in keys}
    values.update(cache_read=cache['read'], cache_write=cache['write'])
    if any(v < 0 for v in values.values()):
        return None
    values['comparable_tokens'] = sum(values[k] for k in ('input', 'output', 'cache_read', 'cache_write'))
    return values


def totals(events):
    steps = [e['part'] for e in events if e.get('type') == 'step_finish']
    values = [metric(part) for part in steps]
    complete = bool(values) and all(value is not None for value in values)
    observed = {key: sum(value[key] for value in values if value is not None)
                for key in ('input', 'output', 'reasoning', 'cache_read', 'cache_write', 'comparable_tokens')}
    return {'complete': complete, 'steps': len(steps), 'measured_steps': sum(v is not None for v in values),
            'observed': observed if any(v is not None for v in values) else None}


class Budget:
    def __init__(self):
        self.lock = threading.Lock()
        self.stop = threading.Event()
        self.calls = 0
        self.reasons = []

    def halt(self, reason):
        with self.lock:
            if reason not in self.reasons:
                self.reasons.append(reason)
            self.stop.set()

    def reserve(self, session):
        with self.lock:
            if session or self.stop.is_set() or self.calls >= CALL_LIMIT:
                raise RuntimeError('No additional invocation authorized')
            self.calls += 1


def stripped_kernel(text):
    start = text.index("    if arm != 'sdd' and kit_bench.healthy(result) and initial_product == product_hashes(workspace):")
    end = text.index("    if arm == 'sdd' and selected_mode == 'tiny':", start)
    removed = text[start:end]
    assert "'approve-plan'" in removed
    return text[:start] + '    # No additional inference or simulated approval in this bounded cohort.\n\n' + text[end:]


def context(root, budget=None):
    spec = importlib.util.spec_from_file_location('odd_batching_private_kernel', root / 'kernel.py')
    base = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base)
    base.LAB_ROOT, base.PROTOCOL, base.MODEL = root, PROTOCOL, MODEL
    base.PYTHON_BIN = str(SOURCE / '.venv/bin/python')
    base.ARMS = ('odd', 'adjusted')
    base.namespace = lambda arm: {'odd': 'oa', 'adjusted': 'ob'}[arm]
    base.skill_name = lambda arm: base.namespace(arm) + '-odd-workflow'
    base.agent_name = lambda arm: 'odd-standards-' + arm
    original_config, original_inputs, original_eval = base.configuration, base.source_inputs, base.evaluate_cell

    def configuration(folder, arm, workspace, intent='implement'):
        cfg = original_config(folder, arm, workspace, intent)
        agent = cfg['agent'][base.agent_name(arm)]
        agent['model'], agent['steps'] = MODEL, STEP_LIMIT
        agent.pop('temperature', None)
        return cfg

    def inputs(folder):
        result = original_inputs(folder)
        for name in ('kernel.py', 'budget.json', 'treatments.json', 'offline-preflight.json'):
            result[name] = base.sha(folder / name)
        for path in (Path(__file__).resolve(), REPO / 'tools/test_odd_batching.py', REPO / 'tools/odd_batching_report.py',
                     PACKAGE / 'agrupacion.md', PACKAGE / 'protocolo.md', PRIOR / 'freeze.json'):
            result[str(path)] = base.sha(path)
        return result

    def evaluate(folder, label, workspace, task_id, is_stage2=False):
        start = time.monotonic()
        result = original_eval(folder, label, workspace, task_id, is_stage2)
        stage = folder / 'evaluation' / (label + '-stage')
        env = dict(os.environ, PYTHONPATH=str(folder) + os.pathsep + str(stage),
                   PYTHONDONTWRITEBYTECODE='1', EVAL_TEST_DB_FILE=str(folder / 'evaluation' / (label + '-original43.sqlite3')))
        env.pop('DATABASE_URL', None)
        proc = base.run_cmd([base.PYTHON_BIN, 'manage.py', 'test', '--settings=oracles.eval_settings',
                             'catalog.tests.test_models', 'catalog.tests.test_forms', 'catalog.tests.test_views'],
                            stage, execution_env=env)
        import re
        match = re.search(r'Ran (\d+) tests', proc.stderr)
        count = int(match.group(1)) if match else None
        result['original43_separate'] = {'returncode': proc.returncode, 'count': count,
                                         'passed': proc.returncode == 0 and count == 43,
                                         'stdout': proc.stdout, 'stderr': proc.stderr}
        result['external_evaluation_seconds'] = round(time.monotonic() - start, 3)
        return result

    base.configuration, base.source_inputs, base.evaluate_cell = configuration, inputs, evaluate
    if budget is not None:
        base.invoke = lambda folder, arm, workspace, prompt, session=None, limit=600: invoke(
            base, budget, folder, arm, workspace, prompt, session)
    return base


def invoke(base, budget, root, arm, workspace, prompt, session=None):
    budget.reserve(session)
    cfg = base.configuration(root, arm, workspace)
    args = [base.CLI, 'run', '--format', 'json', '--model', MODEL, '--variant', VARIANT,
            '--agent', base.agent_name(arm), '--dir', str(workspace), prompt]
    started, start = base.stamp(), time.monotonic()
    child = subprocess.Popen(args, cwd=workspace, env=base.make_exec_env(cfg), stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, start_new_session=True)
    events, inbox = [], queue.Queue()
    invalid_stdout_lines = []
    stderr_hash, stderr_bytes = hashlib.sha256(), [0]

    def stdout_reader():
        for line in child.stdout:
            inbox.put(line)
        inbox.put(None)

    def stderr_reader():
        while True:
            chunk = child.stderr.read(65536)
            if not chunk:
                break
            stderr_hash.update(chunk)
            stderr_bytes[0] += len(chunk)

    readers = [threading.Thread(target=stdout_reader, daemon=True), threading.Thread(target=stderr_reader, daemon=True)]
    for thread in readers:
        thread.start()
    reason, sent_at, eof, live = None, None, False, workspace.name
    livepath = root / 'live' / (live + '.json')

    def consume(line):
        nonlocal reason
        try:
            decoded = json.loads(line)
            if not isinstance(decoded, dict):
                raise ValueError('Expected event object')
        except (ValueError, UnicodeDecodeError):
            if line.strip():
                invalid_stdout_lines.append({'bytes': len(line), 'sha256': hashlib.sha256(line).hexdigest()})
                reason = reason or 'invalid_event_stream'
                budget.halt(reason)
            return
        clean = base.kit_bench.clean_events(line.decode('utf-8', 'replace'))
        events.extend(clean)
        for event in clean:
            if event.get('type') == 'error':
                reason = reason or 'api_or_process_error'
                budget.halt(reason)
            if event.get('type') == 'step_finish':
                measurement = totals(events)
                if metric(event['part']) is None:
                    reason = reason or 'incomplete_metrics'
                elif measurement['observed']['comparable_tokens'] >= TOKEN_LIMIT:
                    reason = reason or 'token_budget'
                elif measurement['steps'] >= STEP_LIMIT and event['part'].get('reason') not in ('stop', 'end_turn'):
                    reason = reason or 'step_budget'
                if reason:
                    budget.halt(reason)
                base.write_json(livepath, {'cell': live, 'elapsed_seconds': round(time.monotonic()-start, 3),
                                          'measurement': measurement, 'stop_reason': reason})
                # Only sanitized observable events, never raw transport/private reasoning.
                base.write_json(root / 'live' / (live + '-events.json'), {'events': events})

    while not eof or child.poll() is None:
        try:
            line = inbox.get(timeout=0.2)
            if line is None:
                eof = True
            else:
                consume(line)
        except queue.Empty:
            pass
        if time.monotonic()-start >= TIMEOUT and reason is None:
            reason = 'timeout'
            budget.halt(reason)
        if budget.stop.is_set() and reason is None and child.poll() is None:
            reason = 'cohort_cancelled'
        if reason and child.poll() is None:
            if sent_at is None:
                try:
                    os.killpg(child.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                sent_at = time.monotonic()
            elif time.monotonic()-sent_at >= 10:
                try:
                    os.killpg(child.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
        if eof and child.poll() is not None:
            break
    child.wait()
    for thread in readers:
        thread.join(timeout=10)
    measurement = totals(events)
    if not measurement['complete']:
        reason = reason or 'incomplete_metrics'
        budget.halt(reason)
    if child.returncode != 0:
        reason = reason or 'process_error'
        budget.halt(reason)
    result = {'started': started, 'seconds': round(time.monotonic()-start, 3), 'returncode': child.returncode,
              'timeout': reason == 'timeout', 'events': events, 'stderr_bytes': stderr_bytes[0],
              'stderr_sha256': stderr_hash.hexdigest(),
              'session': next((e.get('sessionID') for e in events if e.get('sessionID')), None),
              'model_requested': MODEL, 'variant_requested': VARIANT,
              'config_sha256': base.text_sha(json.dumps(cfg, sort_keys=True)),
              'stop_reason': reason, 'measurement': measurement, 'invalid_stdout_lines': invalid_stdout_lines}
    # Persist even if downstream evaluation fails.
    base.write_json(root / 'transport' / (live + '.json'), result, exclusive=True)
    return result


def safe_copy(source, target):
    def ignore(directory, names):
        return [name for name in names if name != 'staticfiles' and not preservation.safe(Path(name))]
    shutil.copytree(source, target, ignore=ignore)


def prepare(root):
    assert not root.exists() and root != REPO and REPO not in root.parents
    prior, _ = prior_adapter.context(PRIOR)
    prior.check_frozen(PRIOR)
    root.mkdir()
    for name in ('baseline', 'oracles', 'references', 'profiles-v2'):
        safe_copy(PRIOR / name, root / name)
    for name in ('cases.json', 'provenance.json', 'dependencies.lock.txt', 'oracle-validation-v3.json'):
        shutil.copyfile(PRIOR / name, root / name)
    source = (PRIOR / 'profiles-v2/adjusted/skills/ob-odd-workflow/SKILL.md').read_text()
    control = source.replace('name: ob-odd-workflow\n', 'name: oa-odd-workflow\n').replace('`ob-data-api`', '`oa-data-api`').replace('`ob-ui-design`', '`oa-ui-design`')
    treatment = source.rstrip() + '\n\n' + (PACKAGE / 'agrupacion.md').read_text().strip() + '\n'
    (root / 'profiles-v2/odd/skills/oa-odd-workflow/SKILL.md').write_text(control)
    (root / 'profiles-v2/adjusted/skills/ob-odd-workflow/SKILL.md').write_text(treatment)
    (root / 'adjusted-SKILL.md').write_text(treatment)
    (root / 'kernel.py').write_text(stripped_kernel((SOURCE / 'runner.py').read_text()))
    shutil.copyfile(Path(__file__), root / 'runner.py')
    shutil.copyfile(REPO / 'tools/test_odd_batching.py', root / 'test_runner.py')
    shutil.copyfile(PACKAGE / 'protocolo.md', root / 'protocol.md')
    base = context(root)
    base.write_json(root / 'budget.json', {'model': MODEL, 'variant': VARIANT, 'timeout_seconds': TIMEOUT,
                    'steps': STEP_LIMIT, 'tokens_per_conversation': TOKEN_LIMIT, 'max_invocations': CALL_LIMIT,
                    'nominal_total_tokens': TOKEN_LIMIT*CALL_LIMIT, 'boundary_overshoot_possible': True}, exclusive=True)
    base.write_json(root / 'treatments.json', {'control': 'standards ODD + complete domain skills',
                    'treatment_delta': 'agrupacion.md only', 'prior_freeze_sha256': base.sha(PRIOR / 'freeze.json'),
                    'pairs': 2, 'order': [['odd', 'adjusted'], ['adjusted', 'odd']], 'concurrency': 2}, exclusive=True)
    print('Prepared isolated batching experiment; no inference performed')


def offline_preflight(root):
    base = context(root)
    checks = {}
    source = (PRIOR / 'profiles-v2/adjusted/skills/ob-odd-workflow/SKILL.md').read_text()
    control = (root / 'profiles-v2/odd/skills/oa-odd-workflow/SKILL.md').read_text()
    normalized = control.replace('oa-', 'ob-')
    checks['control_normalized_equal'] = normalized == source
    treatment = (root / 'profiles-v2/adjusted/skills/ob-odd-workflow/SKILL.md').read_text()
    checks['only_scheduling_delta'] = treatment == source.rstrip()+'\n\n'+(PACKAGE/'agrupacion.md').read_text().strip()+'\n'
    for domain in ('data-api', 'ui-design'):
        a = root / 'profiles-v2/odd/skills' / ('oa-'+domain)
        b = root / 'profiles-v2/adjusted/skills' / ('ob-'+domain)
        checks[domain+'_all_references_equal'] = {
            str(p.relative_to(a)): p.read_text().replace('oa-', 'ob-') for p in a.rglob('*.md')
        } == {str(p.relative_to(b)): p.read_text() for p in b.rglob('*.md')}
    for arm in base.ARMS:
        cfg = base.configuration(root, arm, root/'runs'/'offline')
        agent = cfg['agent'][base.agent_name(arm)]
        checks[arm+'_config'] = agent['model']==MODEL and agent['steps']==60 and 'temperature' not in agent
    checks['single_call_kernel'] = "'approve-plan'" not in (root/'kernel.py').read_text()
    checks['no_maps_added'] = not (root/'baseline/.navigator').exists() and not (root/'baseline/.architecture').exists()
    checks['python_exists'] = Path(base.PYTHON_BIN).exists()
    checks['cli_exists'] = bool(base.CLI)
    base.write_json(root/'offline-preflight.json', {'kind': 'offline_only_no_model_calls', 'checks': checks,
                    'passed': all(checks.values())}, exclusive=True)
    assert all(checks.values()), checks
    print('Offline preflight passed; zero model calls')


def freeze(root):
    base = context(root)
    assert json.loads((root/'offline-preflight.json').read_text())['passed']
    assert json.loads((root/'reference-proof.json').read_text())['functional_pass']
    base.write_json(root/'freeze.json', {'protocol': PROTOCOL, 'created': base.stamp(), 'model': MODEL,
                    'inputs': base.source_inputs(root), 'cases_sha256': base.sha(root/'cases.json'),
                    'preflight_kind': 'offline_only'}, exclusive=True)
    print('Frozen before inference')


def run(root):
    budget = Budget()
    base = context(root, budget)
    base.check_frozen(root)
    base.write_json(root/'batch-start.json', {'started': base.stamp(), 'max_cells': 4,
                    'pid': os.getpid()}, exclusive=True)
    start, completed, errors = time.monotonic(), [], []
    try:
        for repeat, order in enumerate((('odd','adjusted'), ('adjusted','odd')), 1):
            if budget.stop.is_set():
                break
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
                jobs = {pool.submit(base.run_cell_full, root, 'TASK-2', arm, repeat): arm for arm in order}
                for future in concurrent.futures.as_completed(jobs):
                    try:
                        record = future.result()['phase1']
                        completed.append(record['cell'])
                        print(record['cell'], record['functional_pass'], record['seconds'], flush=True)
                    except Exception as error:
                        errors.append({'arm': jobs[future], 'repeat': repeat, 'type': type(error).__name__,
                                       'message': 'Cell failed; inspect preserved sanitized records/transport'})
                        budget.halt('integration_failure')
            base.write_json(root/f'repetition-{repeat}.json', {'completed': completed.copy(), 'errors': errors.copy()}, exclusive=True)
    finally:
        base.write_json(root/'batch-result.json', {'wall_seconds': round(time.monotonic()-start,3),
                        'completed': completed, 'errors': errors, 'invocations_attempted': budget.calls,
                        'stop_reasons': budget.reasons, 'no_selective_retries': True}, exclusive=True)
    base.check_frozen(root)
    print('Batch stopped' if budget.stop.is_set() else 'Batch complete', budget.calls, flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('command', choices=['prepare','offline-preflight','reference','freeze','run','check'])
    parser.add_argument('--background', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    if args.background:
        assert args.command=='run' and (root/'freeze.json').exists() and not (root/'batch-start.json').exists()
        with (root/'coordinator.log').open('xb') as log:
            child = subprocess.Popen([sys.executable,'-B',str(Path(__file__).resolve()),str(root),'run'],
                                     cwd=REPO, stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True)
        print(json.dumps({'pid':child.pid,'root':str(root)}))
    elif args.command=='prepare': prepare(root)
    elif args.command=='offline-preflight': offline_preflight(root)
    elif args.command=='freeze': freeze(root)
    elif args.command=='run': run(root)
    elif args.command=='reference':
        base=context(root)
        result=base.evaluate_cell(root,'reference-proof',root/'references/TASK-2','TASK-2')
        base.write_json(root/'reference-proof.json',result,exclusive=True)
        assert result['functional_pass'] and result['original43_separate']['passed']
        print('Reference original43 + external9 + separate43 passed')
    else:
        context(root).check_frozen(root)
        print('Frozen inputs intact')


if __name__=='__main__':
    main()
