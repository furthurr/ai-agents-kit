import json
from pathlib import Path
import unittest

import odd_standards_benchmark as adapter

ROOT = Path('/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/odd-standards-gemini-20261105').resolve()


class OddStandardsTests(unittest.TestCase):
    def setUp(self):
        self.base, self.old = adapter.context(ROOT)

    def test_original_body_exact_and_adjustment_additive(self):
        control = adapter.composed_body('odd').replace('`oa-data-api`', '`data-api`').replace('`oa-ui-design`', '`ui-design`')
        adjusted = adapter.composed_body('adjusted').replace('`ob-data-api`', '`data-api`').replace('`ob-ui-design`', '`ui-design`')
        self.assertEqual(control, adapter.historical_body())
        self.assertEqual(adjusted, control + '\n\n' + (adapter.PACKAGE / 'ajuste.md').read_text().strip())
        for arm in adapter.ARMS:
            actual = ROOT / 'profiles-v2' / arm / 'skills' / self.base.skill_name(arm) / 'SKILL.md'
            self.assertEqual(self.base.body(actual.read_text()), adapter.composed_body(arm))

    def test_equal_agent_after_namespaces(self):
        normalized = []
        for arm in adapter.ARMS:
            text = (ROOT / 'profiles-v2' / arm / 'agent.md').read_text()
            normalized.append(text.replace(self.base.agent_name(arm), 'AGENT').replace(self.base.skill_name(arm), 'PRIMARY'))
        self.assertEqual(*normalized)

    def test_same_domain_tree_and_permissions(self):
        manifest = json.loads((adapter.REPO / 'canonical/manifest.json').read_text())
        configs = []
        for arm in adapter.ARMS:
            for sid in ('data-api', 'ui-design'):
                source = adapter.REPO / 'generated/opencode/skills' / sid
                target = ROOT / 'profiles-v2' / arm / 'skills' / (self.base.namespace(arm) + '-' + sid)
                for file in source.rglob('*.md'):
                    self.assertEqual((target / file.relative_to(source)).read_text(), self.old.substitute(file.read_text(), self.base.namespace(arm), manifest))
            agent = self.base.configuration(ROOT, arm, ROOT / 'runs' / arm)['agent'][self.base.agent_name(arm)]
            permission = agent['permission']
            configs.append((agent['model'], agent['temperature'], agent['steps'], permission['bash'], permission['task'], permission['google_search']))
            self.assertEqual(permission['edit']['*.key'], 'deny')
            self.assertEqual(permission['skill']['*'], 'deny')
        self.assertEqual(*configs)

    def test_task_same_and_no_reservation_hints_in_adjustment(self):
        original = json.loads((self.old.SOURCE / 'cases.json').read_text())
        current = json.loads((ROOT / 'cases.json').read_text())
        self.assertEqual(current['tasks'], [case for case in original['tasks'] if case['id'] == 'TASK-2'])
        text = (adapter.PACKAGE / 'ajuste.md').read_text()
        for word in ('Reservation', 'SQLite', 'Idempotency-Key', 'TASK-2'):
            self.assertNotIn(word, text)

    def test_probe_derivative_and_expectations(self):
        expected_source, cases = adapter.consultation_source()
        self.assertEqual((ROOT / 'consultation_runner.py').read_text(), expected_source)
        self.assertNotIn('"v2"', expected_source)
        self.assertNotIn("'v2'", expected_source)
        self.assertEqual(json.loads((ROOT / 'probe-cases.json').read_text()), cases)
        self.assertEqual([case['expected'] for case in cases], [['data-api'], ['ui-design'], [], [], []])

    def test_freeze_sources_and_no_overwrite(self):
        inputs = self.base.source_inputs(ROOT)
        for key in ('consultation_runner.py', 'probe-cases.json', 'adjusted-SKILL.md'):
            self.assertIn(key, inputs)
        self.assertIn(str(adapter.PACKAGE / 'ajuste.md'), inputs)
        with self.assertRaises(AssertionError):
            adapter.prepare(self.base, self.old, ROOT)

    def test_historical_baseline_unchanged(self):
        self.old.load_source().check_frozen(self.old.SOURCE)


if __name__ == '__main__':
    unittest.main()
