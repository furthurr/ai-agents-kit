from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import developer_v2_high_report as report


def cell(arm, repeat, tokens):
    return {'arm': arm, 'repeat': repeat, 'trajectory_functional_pass': True,
            'all_original_suites_pass': True, 'healthy': True, 'primary_loaded_by_content': True,
            'metrics': {'comparable_tokens': tokens}, 'seconds': 10,
            'tools': 1, 'steps': 1, 'user_turns': 0, 'tool_errors': [], 'complete': True}


class HighReportTests(unittest.TestCase):
    def run_report(self, cells):
        with tempfile.TemporaryDirectory(dir='/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode') as folder:
            with patch.object(report.real_project_report, 'collect', return_value={'cells': cells, 'execution_errors': []}):
                return report.analyze(Path(folder))

    def test_partial_does_not_compare_or_claim_complete(self):
        result = self.run_report([cell('v2', repeat, 1) for repeat in (1, 2, 3)] + [cell('odd', 1, 2)])
        self.assertFalse(result['complete'])
        self.assertEqual(result['comparisons'], {})
        self.assertIsNone(result['arms']['developer']['comparable_tokens'])

    def test_exact_ten_percent_threshold_and_repeated_wins(self):
        cells = [cell(arm, repeat, 90 if arm == 'v2' else 100)
                 for arm in ('developer', 'odd', 'v2') for repeat in (1, 2, 3)]
        result = self.run_report(cells)
        self.assertTrue(result['complete'])
        self.assertEqual(result['arms']['v2']['functional_pass'], 3)
        for comparison in result['comparisons'].values():
            self.assertTrue(comparison['efficiency_threshold_pass'])
            self.assertEqual(comparison['v2_token_wins'], 3)


if __name__ == '__main__':
    unittest.main()
