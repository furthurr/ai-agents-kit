import json
from pathlib import Path
import unittest

import odd_standards_retry as retry

ROOT = Path('/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/odd-standards-retry-gemini-20261105').resolve()


class RetryTests(unittest.TestCase):
    def setUp(self):
        self.base, _ = retry.context(ROOT)
        self.previous, _ = retry.original.context(retry.PARTIAL)

    def test_historical_partial_still_partial_and_unchanged(self):
        self.previous.check_frozen(retry.PARTIAL)
        data = json.loads((retry.PARTIAL / 'batch-result.json').read_text())
        self.assertEqual(len(data['errors']), 1)
        trace = json.loads((retry.PARTIAL / 'invocations/TASK-2-ODD-r2-1.json').read_text())
        self.assertTrue(trace['result']['timeout'])

    def test_corpus_profiles_and_oracles_identical(self):
        for folder in ('baseline', 'oracles', 'references', 'profiles-v2'):
            self.assertEqual(self.base.hashes(ROOT / folder), self.previous.hashes(retry.PARTIAL / folder))
        for name in ('cases.json', 'dependencies.lock.txt', 'adjusted-SKILL.md', 'probe-cases.json', 'consultation_runner.py'):
            self.assertEqual(self.base.sha(ROOT / name), self.previous.sha(retry.PARTIAL / name))

    def test_same_resolved_config_except_root(self):
        for arm in retry.original.ARMS:
            left = json.dumps(self.base.configuration(ROOT, arm, ROOT / 'runs/proof'), sort_keys=True).replace(str(ROOT), 'LAB')
            right = json.dumps(self.previous.configuration(retry.PARTIAL, arm, retry.PARTIAL / 'runs/proof'), sort_keys=True).replace(str(retry.PARTIAL), 'LAB')
            self.assertEqual(left, right)

    def test_provenance_and_probes_not_recounted(self):
        plan = json.loads((ROOT / 'retry-plan.json').read_text())
        self.assertEqual(plan['prior_freeze_sha256'], self.base.sha(retry.PARTIAL / 'freeze.json'))
        self.assertEqual(plan['prior_batch_sha256'], self.base.sha(retry.PARTIAL / 'batch-result.json'))
        self.assertFalse((ROOT / 'consultation-summary.json').exists())
        self.assertEqual(self.base.sha(ROOT / 'prior-consultation-summary.json'), self.base.sha(retry.PARTIAL / 'consultation-summary.json'))
        self.assertIn('retry-plan.json', self.base.source_inputs(ROOT))

    def test_no_overwrite(self):
        with self.assertRaises(AssertionError):
            retry.prepare(ROOT)


if __name__ == '__main__':
    unittest.main()
