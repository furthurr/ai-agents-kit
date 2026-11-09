#!/usr/bin/env python3
"""Recover explicit synthetic experiment artifacts; no inference or credentials.

capture creates a new immutable bundle; verify checks every archived byte hash.
Original ledgers/freezes are never changed. No global/isolated auth config copied.
"""
from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import hashlib
import json
from pathlib import Path
import zipfile

REPO = Path(__file__).resolve().parent.parent
EXPERIMENTS = REPO / 'docs/experimentos'
DEST = EXPERIMENTS / 'continuidad-2026-11-04'
TEMP = Path('/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode')
PLAN = Path.home() / 'Desktop/plan-crear-agente-odd-mas-2026-11-04.md'
BAD_NAMES = ('*.env*', '*.pem', '*.key', '*.p12', '*.pfx', '*.jks', '*.keystore',
             'auth.json', '*antigravity-accounts*', '.npmrc', '.netrc', '.pypirc')
BAD_KEYS = {'responseheaders', 'responsebody', 'authorization', 'set-cookie', 'cookie',
            'apikey', 'api_key', 'accesstoken', 'access_token', 'refreshtoken', 'refresh_token',
            'id_token', 'thoughtsignature', 'encrypted_content', 'providermetadata', 'provider_metadata',
            'reasoning_content', 'reasoningtext'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_json(value):
    if isinstance(value, dict):
        if value.get('type') == 'reasoning':
            return False
        for key, item in value.items():
            if str(key).lower() in BAD_KEYS:
                return False
            if str(key).lower() == 'reasoning' and not isinstance(item, (int, float, type(None))):
                return False
            if not safe_json(item):
                return False
    elif isinstance(value, list):
        return all(safe_json(item) for item in value)
    return True


def read_allowed(path, root):
    if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('symlink/escape excluded')
    if any(fnmatch.fnmatch(part.lower(), pattern) for part in path.parts for pattern in BAD_NAMES):
        raise ValueError('sensitive filename excluded before reading')
    data = path.read_bytes()
    if path.suffix == '.json':
        if not safe_json(json.loads(data)):
            raise ValueError('transport/private structured fields excluded')
    elif path.suffix == '.jsonl':
        if not all(safe_json(json.loads(line)) for line in data.splitlines() if line.strip()):
            raise ValueError('transport/private structured fields excluded')
    return data


def archive(name, root, files):
    entries, missing, excluded = [], [], []
    path = DEST / 'anexos' / (name + '.zip')
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
        for relative, expected in sorted(files.items()):
            source = root / relative
            if not source.is_file():
                missing.append(relative)
                continue
            try:
                data = read_allowed(source, root)
            except (ValueError, OSError) as error:
                excluded.append({'path': relative, 'reason': str(error)})
                continue
            actual = digest(data)
            info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            output.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
            entries.append({'path': relative, 'bytes': len(data), 'sha256': actual,
                            'expected_sha256': expected, 'provenance_matches': actual == expected if expected else None})
    return {'archive': str(path.relative_to(DEST)), 'archive_sha256': digest(path.read_bytes()),
            'archive_bytes': path.stat().st_size, 'source_root': str(root), 'entries': entries,
            'missing': missing, 'excluded': excluded}


def capture():
    if DEST.exists():
        raise SystemExit('Bundle already exists; never overwrite. Use verify.')
    DEST.mkdir()
    manifest = {'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
                'scope': 'Preservation only; no benchmark rerun, altered original result, installation or commit.',
                'archives': [], 'copies': []}
    provenance_sets = [
        ('odd-sdd-gpt-trazas', EXPERIMENTS / 'odd-vs-sdd-2026-11-04/evidencia/procedencia.json', 'external_trace_root', 'traces'),
        ('odd-sdd-suplemento-trazas', EXPERIMENTS / 'odd-vs-sdd-2026-11-04/evidencia/suplemento/procedencia.json', 'external_trace_root', 'traces'),
        ('gemini-tres-flujos-trazas', EXPERIMENTS / 'developer-sdd-odd-gemini-2026-11-04/evidencia/provenance.json', 'trace_location', 'traces'),
        ('developer-compacto-trazas', EXPERIMENTS / 'developer-compacto-gemini-2026-11-04/evidencia/provenance.json', 'traces_root', 'trace_hashes'),
    ]
    for name, provenance, root_key, hashes_key in provenance_sets:
        original = json.loads(provenance.read_text())
        item = archive(name, Path(original[root_key]), original[hashes_key])
        item['provenance_file'] = str(provenance.relative_to(REPO))
        item['provenance_file_sha256'] = digest(provenance.read_bytes())
        manifest['archives'].append(item)
    ponytail = TEMP / 'mas-ponytail-evaluacion-20261103'
    expected = {
        'resultado-final-v1.md': '5b0ea5c8f8138bdea570e236ca3b63d29b069661e9fa7b8b85de4bd55098b9ac',
        'protocolo-v1.md': 'fb864cb8e06f0cf4ac67b1c3fd8ccf768e05b812983996059a218797057d114f',
        'build_cases.py': '027f4abe0a41bc69105d892da21ca973146950e7b07a493f71344a8bf5bb09b5',
        'runner.py': '60f736cd223d1fec67ce284685ca5670f728a56c759b6cd6643553e557fc1ea8',
        'variante-b.patch': '6ae6c4bafebc6d461f9d70107af9bbe5b165fcd43dec2723b92bd8f165402378'}
    for name in ['metricas-final-v1.json', 'evaluacion-final-v1.md', 'estado-final-v1.json',
                 'preregistro-v1.json', 'ejecuciones-v1.jsonl', 'preflight.py', 'freeze.py',
                 'access-audit-v1.json', 'checks-cierre-v1.json', 'checks-estaticos-final-v1.json']:
        expected[name] = None
    for folder in ['evidencias-v1', 'casos-v1', 'oracles-v1', 'runs']:
        for file in sorted((ponytail / folder).rglob('*')):
            if file.is_file() and not any(p in {'.git', '__pycache__', 'node_modules', '.opencode', '.claude', '.agents'} for p in file.parts):
                if file.suffix in {'.json', '.jsonl', '.md', '.py', '.txt', '.diff', '.yaml', '.yml'}:
                    expected[str(file.relative_to(ponytail))] = None
    manifest['archives'].append(archive('ponytail-recuperado', ponytail, expected))
    tools = ['gemini_benchmark.py', 'odd_vs_sdd_experiment.py', 'odd_vs_sdd_audit.py', 'odd_vs_sdd_supplement.py',
             'gemini_three_way.py', 'gemini_three_way_report.py', 'test_gemini_three_way.py',
             'developer_compact_benchmark.py', 'developer_compact_report.py', 'test_developer_compact_benchmark.py',
             'preserve_experiment_context.py']
    manifest['archives'].append(archive('herramientas-actuales', REPO, {'tools/' + name: None for name in tools}))
    exploratory = TEMP / 'mas-gemini38-eval'
    selected = {'gemini_benchmark_summary.json': 'a644410118d3b23a599ec9d43ed66f9d8fd1b2de65cf71e1aae1e318c0bd3ee9'}
    for file in sorted((exploratory / 'records').glob('*.json')):
        selected[str(file.relative_to(exploratory))] = None
    manifest['archives'].append(archive('gemini-exploratorio-no-validado', exploratory, selected))
    data = read_allowed(PLAN, PLAN.parent)
    target = DEST / 'plan-odd-v1.1.md'
    with target.open('xb') as file:
        file.write(data)
    manifest['copies'].append({'path': target.name, 'source': str(PLAN), 'sha256': digest(data),
                              'bytes': len(data), 'note': 'Exact historical copy; latest discussion in README supersedes unresolved recommendations.'})
    manifest['summary'] = {
        'archives': len(manifest['archives']),
        'archived_files': sum(len(a['entries']) for a in manifest['archives']),
        'compressed_bytes': sum(a['archive_bytes'] for a in manifest['archives']),
        'missing': sum(len(a['missing']) for a in manifest['archives']),
        'excluded': sum(len(a['excluded']) for a in manifest['archives']),
        'provenance_mismatches': sum(e['provenance_matches'] is False for a in manifest['archives'] for e in a['entries'])}
    with (DEST / 'preservacion.json').open('x', encoding='utf-8') as file:
        json.dump(manifest, file, ensure_ascii=False, indent=2)
        file.write('\n')
    print(json.dumps(manifest['summary'], indent=2))
    verify()


def verify():
    manifest = json.loads((DEST / 'preservacion.json').read_text())
    checked = 0
    for item in manifest['archives']:
        archive_path = DEST / item['archive']
        assert digest(archive_path.read_bytes()) == item['archive_sha256'], item['archive']
        with zipfile.ZipFile(archive_path) as archive_file:
            assert set(archive_file.namelist()) == {e['path'] for e in item['entries']}
            for entry in item['entries']:
                assert digest(archive_file.read(entry['path'])) == entry['sha256'], entry['path']
                checked += 1
    for item in manifest['copies']:
        assert digest((DEST / item['path']).read_bytes()) == item['sha256'], item['path']
    print('Verified', len(manifest['archives']), 'archives;', checked, 'member hashes; plan copy intact.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['capture', 'verify'])
    args = parser.parse_args()
    globals()[args.action]()
