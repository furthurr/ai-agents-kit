import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import odd_context_routing_report as report


class RoutingReportTests(unittest.TestCase):
    def analyze_fixture(self, passed=True, map_read=True, empty=False, closing=''):
        with tempfile.TemporaryDirectory(dir='/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode') as folder:
            root = Path(folder)
            (root / 'records').mkdir()
            (root / 'traces').mkdir()
            source = {'behavior': []}
            if not empty:
                for arm in ('odd', 'adjusted'):
                    label = arm + '-r1'
                    record = {'arm': arm, 'cell': label, 'functional_pass': passed if arm == 'adjusted' else True,
                              'oracle_suite_pass': True, 'original_suite_pass': True, 'healthy': True,
                              'primary_loaded_by_content': True, 'seconds': 10,
                              'metrics': {'comparable_tokens': 80 if arm == 'adjusted' else 100},
                              'tools_count': 1, 'steps': 1, 'changed_files': []}
                    (root / 'records' / (label + '.json')).write_text(json.dumps(record))
                    (root / 'traces' / (label + '.json')).write_text(json.dumps({'invocations': [{'events': [{'type': 'text', 'part': {'text': closing}}]}]}))
                    source['behavior'].append({'arm': arm, 'project_doc_reads': ['.navigator/ai-context.md'] if arm == 'adjusted' and map_read else [],
                                              'final_doc_mentions': [], 'domains_loaded_by_content': ['data-api', 'ui-design'],
                                              'both_loaded_before_product': True})
            with patch.object(report.odd_standards_report, 'analyze', return_value=source):
                return report.analyze(root)

    def test_empty_is_not_complete(self):
        result = self.analyze_fixture(empty=True)
        self.assertFalse(result['conversations_complete'])
        self.assertIsNone(result['comparison'])

    def test_cheaper_correct_and_map_used_is_only_exploratory_signal(self):
        result = self.analyze_fixture()
        self.assertTrue(result['conversations_complete'])
        self.assertAlmostEqual(result['comparison']['routed_token_delta_pct'], -20)
        self.assertTrue(result['comparison']['favorable_exploratory_signal'])

    def test_incorrect_or_no_map_not_preferred(self):
        self.assertFalse(self.analyze_fixture(passed=False)['comparison']['favorable_exploratory_signal'])
        self.assertFalse(self.analyze_fixture(map_read=False)['comparison']['favorable_exploratory_signal'])

    def test_documental_word_not_missed_and_role_not_invented(self):
        result = self.analyze_fixture(closing='README.md requiere una actualización documental manual.')
        for row in result['arms']:
            self.assertTrue(row['doc_close_mentions'])
            self.assertFalse(row['explicit_documentation_orchestrator'])


if __name__ == '__main__':
    unittest.main()
