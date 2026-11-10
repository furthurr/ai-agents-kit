#!/usr/bin/env python3
"""Local checks for anonymized mobile artifacts; never prints matched values.

This bounded check does not inspect archives, Git history, credentials or images.
It is not a universal secret detector. See docs/experimentos/PRIVACIDAD-MOVIL.md.
"""
from pathlib import Path
import json
import re
import sys


REPO = Path(__file__).resolve().parent.parent
PERSONAL_HOME = re.compile(r'(?:/Users/|/home/)[^/\s"\x27`<>]+')
FINGERPRINT = re.compile(r'^(?:[a-fA-F0-9]{40}|[a-fA-F0-9]{64})$')
DETAIL_KEYS = {'stdout', 'stderr', 'prompt', 'response', 'output', 'error',
               'diff', 'patch', 'command', 'trace', 'content', 'message', 'exception'}


def json_findings(value, key=''):
    """Return categories, never the corresponding string, path key or value."""
    findings = set()
    if isinstance(value, dict):
        for name, child in value.items():
            if PERSONAL_HOME.search(name):
                findings.add('personal_path_key')
            findings.update(json_findings(child, name))
    elif isinstance(value, list):
        for child in value:
            findings.update(json_findings(child, key))
    elif isinstance(value, str):
        if PERSONAL_HOME.search(value):
            findings.add('personal_path')
        if FINGERPRINT.fullmatch(value):
            findings.add('original_fingerprint')
        if (any(part in key.lower() for part in DETAIL_KEYS) and value
                and not value.startswith('[REDACTED_')):
            findings.add('raw_execution_detail')
    return findings


def paths(root):
    patterns = (
        'docs/experimentos/real-android-*/**/*',
        'docs/experimentos/real-ios-*/**/*',
        'docs/experimentos/archive/real-android-*/**/*',
        'docs/experimentos/archive/real-ios-*/**/*',
        'docs/experimentos/proyectos-arneses-comparativa/genera/*',
    )
    for path in sorted({p for pattern in patterns for p in root.glob(pattern)}):
        if (not path.is_file() or path.is_symlink()
                or path.suffix not in {'.json', '.md', '.kt', '.swift'}
                or any(p.startswith('.env') for p in path.relative_to(root).parts)
                or root.resolve() not in path.resolve().parents):
            continue
        yield path


def check(root=REPO):
    findings = []
    checked = 0
    for path in paths(root):
        checked += 1
        text = path.read_text(encoding='utf-8')
        relative = str(path.relative_to(root))
        for number, line in enumerate(text.splitlines(), 1):
            if PERSONAL_HOME.search(line):
                findings.append((relative, number, 'personal_path'))
            if path.suffix == '.kt' and line.startswith('package '):
                package = line.removeprefix('package ').strip()
                if not package.startswith('com.example.mobilefixture.'):
                    findings.append((relative, number, 'non_fixture_namespace'))
        if path.suffix == '.json':
            try:
                categories = json_findings(json.loads(text))
            except json.JSONDecodeError:
                categories = {'invalid_json'}
            findings.extend((relative, 1, category) for category in sorted(categories))
    return checked, findings


def main():
    checked, findings = check()
    for path, line, category in findings:
        print(f'{path}:{line}: {category}')
    print(f'Mobile privacy: {checked} files checked; {len(findings)} findings. '
          'Archives, history and images remain outside this check.')
    return int(bool(findings))


if __name__ == '__main__':
    sys.exit(main())
