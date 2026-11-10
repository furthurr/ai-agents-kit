#!/usr/bin/env python3
"""Post-run contract diagnostic only; does not change frozen grades or solutions."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time

CODE = '''import json, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oracles.eval_settings')
import django
django.setup()
from django.conf import settings
# Outside Django's test runner, testserver is not automatically allowed.
settings.ALLOWED_HOSTS = ['testserver']
from django.test import Client
url = '/catalog/api/bookinstance/00000000-0000-0000-0000-000000000000/reserve/'
results = {}
for enforce in (False, True):
    response = Client(enforce_csrf_checks=enforce).post(url, HTTP_IDEMPOTENCY_KEY='diagnostic-placeholder')
    results[str(enforce)] = {'status': response.status_code, 'content_type': response.get('Content-Type')}
    if response.get('Content-Type', '').startswith('application/json'):
        results[str(enforce)]['json'] = response.json()
print(json.dumps(results))
'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    assert (root / 'batch-result.json').exists(), 'Only after inference batch ends'
    python = root.parent / 'real-project-gemini-20261104/.venv/bin/python'
    started, results = time.monotonic(), []
    for path in sorted((root / 'records').glob('*.json')):
        cell = path.stem
        stage = root / 'evaluation' / (cell + '-stage')
        env = dict(os.environ, PYTHONPATH=str(root) + os.pathsep + str(stage), PYTHONDONTWRITEBYTECODE='1',
                   EVAL_TEST_DB_FILE=str(root / 'evaluation' / (cell + '-diagnostic-unused.sqlite3')))
        env.pop('DATABASE_URL', None)
        proc = subprocess.run([str(python), '-B', '-c', CODE], cwd=stage, env=env,
                              capture_output=True, text=True, timeout=60)
        result = {'cell': cell, 'returncode': proc.returncode}
        if proc.returncode == 0:
            result['anonymous_post'] = json.loads(proc.stdout)
        else:
            result['status'] = 'diagnostic_failed_unknown'
        results.append(result)
    report = {'kind': 'post_run_supplemental_contract_diagnostic', 'model_calls': 0,
              'frozen_suite_grades_changed': False, 'feedback_to_agents': False,
              'seconds': round(time.monotonic() - started, 3), 'results': results,
              'interpretation': 'Application HTTP status, not provider API status. Explicit CSRF enforcement probes coverage beyond the nine frozen oracles.'}
    with args.destination.open('x') as output:
        json.dump(report, output, ensure_ascii=False, indent=2)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
