#!/usr/bin/env python3
"""Privacy regressions use synthetic data only."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import importlib
import subprocess

import check_mobile_privacy as privacy
import real_android_gemini_benchmark as android
import real_ios_antigravity_benchmark as ios


class MobilePrivacyTests(unittest.TestCase):
    def test_removed_continuity_note_is_not_reintroduced(self):
        note = 'docs/experimentos/CONTINUAR-AQUI.md'
        self.assertFalse((privacy.REPO / note).exists())
        ignored = subprocess.run(
            ['git', '-C', str(privacy.REPO), 'check-ignore', '--no-index', '--', note],
            capture_output=True, text=True,
        )
        self.assertEqual(ignored.returncode, 0)

    def test_repository_mobile_artifacts_pass_bounded_check(self):
        checked, findings = privacy.check()
        self.assertGreater(checked, 0)
        self.assertEqual(findings, [])

    def test_ci_runs_mobile_privacy_gate(self):
        workflow = (privacy.REPO / '.github/workflows/ci.yml').read_text()
        self.assertIn('python tools/check_mobile_privacy.py', workflow)
        self.assertIn('python tools/test_mobile_privacy.py', workflow)
        self.assertIn('apt-get install -y --no-install-recommends ripgrep', workflow)

    def test_aggregates_and_redacted_details_are_accepted(self):
        record = {'passed': 8, 'rate': 0.5, 'done': True, 'unknown': None,
                  'stdout': '[REDACTED_MOBILE_EVIDENCE]'}
        self.assertEqual(privacy.json_findings(record), set())

    def test_raw_details_and_fingerprints_are_reported_without_values(self):
        findings = privacy.json_findings({'command': 'synthetic command',
                                         'sha256': 'a' * 64})
        self.assertEqual(findings, {'raw_execution_detail', 'original_fingerprint'})

    def test_personal_path_is_reported_without_value(self):
        synthetic = '/' + 'Users' + '/synthetic-person/fixture'
        self.assertEqual(privacy.json_findings({'workspace': synthetic}),
                         {'personal_path'})

    def test_only_fixture_packages_are_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'docs/experimentos/real-android-synthetic/oraculos/Test.kt'
            source.parent.mkdir(parents=True)
            source.write_text('package com.example.mobilefixture.tests\n')
            self.assertEqual(privacy.check(root), (1, []))
            source.write_text('package org.synthetic.privatefixture.tests\n')
            self.assertEqual(privacy.check(root)[1][0][2], 'non_fixture_namespace')

    def test_archives_and_images_are_not_read(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            parent = root / 'docs/experimentos/real-ios-synthetic'
            parent.mkdir(parents=True)
            (parent / 'image.png').write_bytes(b'not an image')
            (parent / 'fixture.zip').write_bytes(b'not an archive')
            self.assertEqual(privacy.check(root), (0, []))

    def test_adapters_accept_explicit_fixture_archives(self):
        try:
            with patch.dict('os.environ', {
                'MOBILE_BENCHMARK_ANDROID_ARCHIVE': '/synthetic/android.zip',
                'MOBILE_BENCHMARK_IOS_ARCHIVE': '/synthetic/ios.zip',
            }):
                self.assertEqual(importlib.reload(android).BASE_ZIP,
                                 Path('/synthetic/android.zip'))
                self.assertEqual(importlib.reload(ios).BASE_ZIP,
                                 Path('/synthetic/ios.zip'))
        finally:
            importlib.reload(android)
            importlib.reload(ios)


if __name__ == '__main__':
    unittest.main()
