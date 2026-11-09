import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import export_odd_batching_evidence as exporter


class ExportTests(unittest.TestCase):
    def fixture(self, parent):
        root, target = parent / 'lab', parent / 'export'
        root.mkdir(); target.mkdir(); (target / 'evidencia').mkdir()
        (root / 'batch-result.json').write_text('{}')
        value = b'{"kind":"offline_only"}'
        (root / 'offline-preflight.json').write_bytes(value)
        archive = b'archive-placeholder-for-hash-check'
        (target / 'laboratorio.tar.gz').write_bytes(archive)
        manifest = {'archive_sha256': hashlib.sha256(archive).hexdigest(),
                    'files': {'offline-preflight.json': hashlib.sha256(value).hexdigest()}}
        (target / 'preservacion.json').write_text(json.dumps(manifest))
        return root, target

    def test_exports_exact_verified_json(self):
        with tempfile.TemporaryDirectory() as directory:
            root, target = self.fixture(Path(directory))
            exporter.export(root, target)
            self.assertEqual((root / 'offline-preflight.json').read_bytes(),
                             (target / 'evidencia/offline-preflight.json').read_bytes())
            self.assertTrue(json.loads((target / 'exportacion.json').read_text())['verified_against_archive_manifest'])

    def test_never_overwrites_export(self):
        with tempfile.TemporaryDirectory() as directory:
            root, target = self.fixture(Path(directory))
            exporter.export(root, target)
            with self.assertRaises(AssertionError): exporter.export(root, target)

    def test_changed_source_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root, target = self.fixture(Path(directory))
            (root / 'offline-preflight.json').write_text('{"changed":true}')
            with self.assertRaises(AssertionError): exporter.export(root, target)
            self.assertFalse((target / 'exportacion.json').exists())


if __name__ == '__main__': unittest.main()
