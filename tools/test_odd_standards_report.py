from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import odd_standards_report as report


def cell(arm, repeat, tokens=100):
    return {'arm': arm, 'repeat': repeat, 'trajectory_functional_pass': True,
            'all_original_suites_pass': True, 'healthy': True, 'primary_loaded_by_content': True,
            'metrics': {'comparable_tokens': tokens}, 'seconds': 10,
            'tools': 1, 'steps': 1, 'user_turns': 0, 'tool_errors': [], 'complete': True}


class OddReportTests(unittest.TestCase):
    def run_case(self, cells):
        with tempfile.TemporaryDirectory(dir='/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode') as folder:
            with patch.object(report.real_project_report, 'collect', return_value={'cells': cells, 'execution_errors': []}):
                return report.analyze(Path(folder))

    def test_partial_does_not_claim_complete_or_compare(self):
        result = self.run_case([cell('adjusted', 1)])
        self.assertFalse(result['complete'])
        self.assertIsNone(result['comparison'])
        self.assertIsNone(result['arms']['odd']['comparable_tokens'])

    def test_overhead_reported_not_hidden(self):
        cells = [cell(arm, repeat, 120 if arm == 'adjusted' else 100)
                 for arm in ('odd', 'adjusted') for repeat in (1, 2, 3)]
        result = self.run_case(cells)
        self.assertTrue(result['complete'])
        self.assertAlmostEqual(result['comparison']['adjusted_token_delta_pct'], 20)
        self.assertEqual(result['comparison']['adjusted_token_wins'], 0)
        self.assertEqual(result['arms']['adjusted']['functional_pass'], 3)


if __name__ == '__main__':
    unittest.main()
