#!/usr/bin/env python3
"""Preserve a synthetic lab without environments, private transport or credentials."""
import argparse
import hashlib
import json
from pathlib import Path
import tarfile


EXCLUDED_DIRS = {'.venv', '.git', '__pycache__', 'node_modules', 'staticfiles',
                 '.ssh', '.aws', '.config', '.opencode'}
EXCLUDED_NAMES = {'auth.json', '.netrc', '.npmrc', '.pypirc', 'snapshot.tar.gz'}
EXCLUDED_SUFFIXES = {'.pem', '.key', '.p12', '.pfx', '.jks', '.keystore', '.pyc', '.sqlite3'}


def safe(path):
    return not (set(path.parts) & EXCLUDED_DIRS or path.name in EXCLUDED_NAMES
                or any(part.startswith('.env') for part in path.parts)
                or path.suffix in EXCLUDED_SUFFIXES or 'antigravity-accounts' in path.name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--dependency', type=Path, action='append', default=[])
    args = parser.parse_args()
    root, destination = args.root.resolve(), args.destination.resolve()
    if not destination.is_dir() or root == destination or root in destination.parents:
        raise SystemExit('Existing destination outside lab required')
    archive = destination / 'laboratorio.tar.gz'
    manifest_path = destination / 'preservacion.json'
    if archive.exists() or manifest_path.exists():
        raise SystemExit('Never overwrite preserved evidence')
    manifest = {}
    with tarfile.open(archive, mode='x:gz') as tar:
        for path in sorted(root.rglob('*')):
            relative = path.relative_to(root)
            if not safe(relative) or path.is_symlink() or not path.is_file():
                continue
            manifest[str(relative)] = hashlib.sha256(path.read_bytes()).hexdigest()
            tar.add(path, arcname=str(relative), recursive=False)
        for dependency in args.dependency:
            if dependency.is_symlink() or not dependency.is_file() or not safe(dependency) or dependency.suffix not in {'.py', '.json', '.md', '.txt'}:
                raise RuntimeError('Unsafe dependency path')
            name = 'dependencies/' + dependency.name
            if name in manifest:
                raise RuntimeError('Duplicate dependency name')
            manifest[name] = hashlib.sha256(dependency.read_bytes()).hexdigest()
            tar.add(dependency, arcname=name, recursive=False)
    with manifest_path.open('x') as file:
        json.dump({'root': str(root), 'files': manifest,
                   'archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
                   'exclusions': 'Environments, git, caches, static build, credentials, database files, original upstream archive.'},
                  file, ensure_ascii=False, indent=2)
    with tarfile.open(archive, mode='r:gz') as tar:
        for member in tar.getmembers():
            if not member.isfile() or not safe(Path(member.name)):
                raise RuntimeError('Unsafe archived member')
            with tar.extractfile(member) as file:
                if hashlib.sha256(file.read()).hexdigest() != manifest[member.name]:
                    raise RuntimeError('Archive hash mismatch: ' + member.name)
    evidence = destination / 'evidencia'
    evidence.mkdir(exist_ok=False)
    for name in ('protocol.md', 'cases.json', 'freeze.json', 'preflight.json',
                 'provenance.json', 'preparation-review.json', 'dependencies.lock.txt',
                 'summary-audit.json', 'batch-result.json', 'oracle-validation-v3.json',
                 'reference-proof.json', 'treatments.json', 'native-base.json',
                 'probe-cases.json', 'consultation-summary.json', 'adjusted-SKILL.md',
                 'retry-plan.json', 'prior-consultation-summary.json', 'model-provenance.json', 'budget.json',
                 'navigation-plan.json', 'summary-final.json', 'partition-manifest.json'):
        source = root / name
        if source.is_file():
            with (evidence / name).open('xb') as file:
                file.write(source.read_bytes())
    if (root / 'partition-manifest.json').is_file():
        for domain in ('data-api', 'ui-design'):
            source = root / 'profiles-v2/adjusted/skills' / ('ob-' + domain)
            for path in sorted(source.rglob('*.md')):
                relative = path.relative_to(source)
                if not safe(relative) or path.is_symlink():
                    raise RuntimeError('Unsafe domain evidence path')
                target = evidence / 'domain-profiles' / domain / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open('xb') as file:
                    file.write(path.read_bytes())
    print(f'Preserved {len(manifest)} files in {archive}')


if __name__ == '__main__':
    main()
