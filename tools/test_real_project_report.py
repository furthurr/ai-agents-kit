import json
from pathlib import Path
import tempfile
import unittest

import real_project_report as report


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='real-lab-report-', dir='/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ('records', 'traces', 'attempts'):
            (self.root / name).mkdir()

    def write_record(self, task, metrics):
        label = task + '-DEVELOPER-r1'
        value = {'cell': label, 'task_id': task, 'arm': 'developer', 'repetition': 1,
                 'is_stage2': False, 'metrics': metrics, 'flow_violations': [],
                 'functional_pass': True, 'original_suite_pass': True, 'healthy': True,
                 'primary_loaded_by_content': True, 'outside_accesses': [],
                 'foreign_skill_attempts': [], 'forbidden_tool_attempts': [],
                 'seconds': 1, 'tools_count': 0, 'steps': 1, 'user_turns': 0,
                 'selected_sdd_mode': None}
        value['evaluation'] = {'oracle_suite': {'count': 1, 'stderr': 'Ran 1 tests\nOK\n'}}
        (self.root / 'records' / (label + '.json')).write_text(json.dumps(value))
        (self.root / 'traces' / (label + '.json')).write_text('{"invocations":[]}')

    def test_empty_does_not_certify_complete(self):
        result = report.collect(self.root)
        self.assertFalse(result['complete_batch'])
        self.assertIsNone(result['arms']['developer']['comparable_tokens'])

    def test_missing_metrics_not_zero(self):
        self.write_record('TASK-1', None)
        result = report.collect(self.root)
        self.assertIsNone(result['cells'][0]['metrics'])
        self.assertIsNone(result['arms']['developer']['comparable_tokens'])

    def test_stage1_alone_not_successful_trajectory(self):
        self.write_record('TASK-3', {'input': 1, 'output': 2, 'cache_read': 3,
                                     'cache_write': 0, 'reasoning': 0, 'comparable_tokens': 6})
        result = report.collect(self.root)
        self.assertFalse(result['cells'][0]['complete'])
        self.assertFalse(result['cells'][0]['trajectory_functional_pass'])
        self.assertFalse(result['cells'][0]['final_functional_pass'])


if __name__ == '__main__':
    unittest.main()
