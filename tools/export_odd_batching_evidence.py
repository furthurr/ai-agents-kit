#!/usr/bin/env python3
"""Export supplemental JSON from an already preserved, completed batching lab."""
import argparse
import hashlib
import json
from pathlib import Path

NAMES = ('offline-preflight.json', 'preparation-verifications.json', 'diagnostico-http.json',
         'diagnostico-http-corregido.json', 'batch-start.json', 'repetition-1.json', 'repetition-2.json')


def export(root, destination):
    assert (root / 'batch-result.json').is_file()
    preserved = json.loads((destination / 'preservacion.json').read_text())
    assert hashlib.sha256((destination / 'laboratorio.tar.gz').read_bytes()).hexdigest() == preserved['archive_sha256']
    target = destination / 'evidencia'
    assert target.is_dir() and not (destination / 'exportacion.json').exists()
    exported = {}
    for name in NAMES:
        source = root / name
        if not source.exists():
            continue
        assert source.is_file() and not source.is_symlink()
        data = source.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        assert preserved['files'][name] == digest
        with (target / name).open('xb') as output:
            output.write(data)
        exported['evidencia/' + name] = digest
    with (destination / 'exportacion.json').open('x') as output:
        json.dump({'files': exported, 'verified_against_archive_manifest': True}, output, indent=2)
    print('Exported', len(exported), 'supplemental JSON; archive hashes verified')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    export(args.root.resolve(), args.destination.resolve())


if __name__ == '__main__':
    main()
