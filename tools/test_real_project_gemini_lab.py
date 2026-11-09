import importlib.util
from pathlib import Path
import unittest
import preserve_real_project_lab as preserve


spec = importlib.util.spec_from_file_location('lab', Path(__file__).with_name('real_project_gemini_lab.py'))
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


class TransportTests(unittest.TestCase):
    def test_preservation_filters_sensitive_and_ephemeral_files(self):
        for name in ('baseline/.env.example', 'x/client.pem', '.venv/lib/module.py',
                     'runs/a/db.sqlite3', 'snapshot.tar.gz', 'x/auth.json',
                     'baseline/staticfiles/manifest.json'):
            self.assertFalse(preserve.safe(Path(name)), name)
        for name in ('baseline/README.md', 'oracles/test_migration.py', 'traces/cell.json'):
            self.assertTrue(preserve.safe(Path(name)), name)

    def test_model_is_previous_cohort(self):
        self.assertEqual(lab.previous.MODEL, 'google/antigravity-gemini-3.8-flash')

    def test_reasoning_not_preserved(self):
        self.assertEqual(lab.previous.clean_events('{"type":"reasoning","part":{"text":"private"}}'), [])

    def test_error_transport_fields_excluded(self):
        result = lab.previous.clean_events('{"type":"error","error":{"name":"APIError",'
            '"data":{"statusCode":429,"message":"quota","headers":{"sensitive":"placeholder"}}}}')
        self.assertEqual(result[0]['error'], {'name': 'APIError', 'statusCode': 429, 'category': 'quota'})
        self.assertNotIn('headers', str(result))


if __name__ == '__main__':
    unittest.main()
