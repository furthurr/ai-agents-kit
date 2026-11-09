from pathlib import Path
import unittest

import odd_domain_core_report as report


class CriteriaCoverageTests(unittest.TestCase):
    def test_numbered_read_preserves_indentation_and_no_loss(self):
        source = '# Rules\n\n- A\n  B\n'
        output = '<content>\n1: # Rules\n2: \n3: - A\n4:   B\n</content>'
        numbered = report.read_numbered_lines(output)
        self.assertTrue(report.content_complete(source, numbered, [output]))
        numbered.pop(4)
        self.assertFalse(report.content_complete(source, numbered, [output]))

    def test_partial_reads_combine_and_track_first_complete_index(self):
        target = Path('/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/criteria.md')
        def event(output):
            return {'part': {'tool': 'read', 'state': {'input': {'filePath': str(target)}, 'status': 'completed', 'output': output}}}
        events = [event('<content>\n1: Rule A\n</content>'), event('<content>\n2: Rule B\n</content>')]
        coverage = report.inspect_reference(events, target, 'Rule A\nRule B\n', target.parent)
        self.assertTrue(coverage['full_content_verified'])
        self.assertEqual(coverage['verified_event_index'], 1)
        self.assertEqual(coverage['completed_reads'], 2)

    def test_failed_read_not_counted_as_standards_consulted(self):
        target = Path('/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/criteria.md')
        events = [{'part': {'tool': 'read', 'state': {'input': {'filePath': str(target)}, 'status': 'error', 'output': 'Rule A'}}}]
        self.assertFalse(report.inspect_reference(events, target, 'Rule A', target.parent)['full_content_verified'])

    def test_test_write_not_product_but_generated_migration_is(self):
        events = [{'part': {'tool': 'write', 'state': {'status': 'completed', 'input': {'filePath': '/app/catalog/tests/test_api.py'}}}},
                  {'part': {'tool': 'bash', 'state': {'input': {'command': 'python manage.py makemigrations catalog'}}}}]
        self.assertEqual(report.first_product_write(events), 1)


if __name__ == '__main__':
    unittest.main()
