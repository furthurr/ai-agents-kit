import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import developer_v2_domains_report as report


def fixture_result():
    cells = []
    for arm in ('developer', 'odd', 'v2', 'build'):
        for repeat in (1, 2, 3):
            cells.append({'arm': arm, 'repeat': repeat, 'trajectory_functional_pass': True,
                          'all_original_suites_pass': True, 'healthy': True,
                          'primary_loaded_by_content': None if arm == 'build' else True,
                          'metrics': {'comparable_tokens': 90 if arm == 'v2' else 100},
                          'seconds': 10, 'tools': 1, 'steps': 1, 'user_turns': 0,
                          'tool_errors': [], 'complete': True})
    arms = {arm: {'cells': 3, 'comparable_tokens': 270 if arm == 'v2' else 300, 'seconds': 30}
            for arm in ('developer', 'odd', 'v2')}
    return {'cells': cells, 'arms': arms, 'comparisons': {}, 'observed_cells': 12, 'complete': False}


class NativeReportTests(unittest.TestCase):
    def run_case(self, verified):
        with tempfile.TemporaryDirectory(dir='/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode') as folder:
            root = Path(folder)
            (root / 'native-base.json').write_text(json.dumps({'native': verified, 'prompt_present': False}))
            (root / 'preflight.json').write_text(json.dumps({'build': {'native': verified, 'prompt_present': False}}))
            with patch.object(report.previous, 'analyze', return_value=copy.deepcopy(fixture_result())):
                return report.analyze(root)

    def test_native_does_not_need_fictional_primary_skill(self):
        result = self.run_case(True)
        self.assertTrue(result['complete'])
        self.assertTrue(result['arms']['build']['healthy'])
        self.assertIsNone(result['arms']['build']['primary_skill'])
        self.assertEqual(result['arms']['build']['functional_pass'], 3)
        self.assertTrue(result['comparisons']['build']['efficiency_threshold_pass'])

    def test_native_identity_not_assumed_when_unverified(self):
        result = self.run_case(False)
        self.assertFalse(result['arms']['build']['healthy'])
        self.assertFalse(result['arms']['build']['native_identity_verified'])


if __name__ == '__main__':
    unittest.main()
