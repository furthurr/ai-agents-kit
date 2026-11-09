import json
from pathlib import Path
import re
import unittest

import developer_v2_high_benchmark as adapter

ROOT = Path('/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/developer-v2-high-gemini-20261105').resolve()


class HighBenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.base = adapter.context(ROOT)
        self.manifest = json.loads((adapter.REPO / 'canonical/manifest.json').read_text())

    def test_historical_inputs_unchanged(self):
        original = adapter.load_source()
        original.check_frozen(adapter.SOURCE)
        self.assertEqual(original.ARMS, ('developer', 'sdd', 'odd'))
        self.assertEqual(self.base.ARMS, ('developer', 'odd', 'v2'))

    def test_unique_valid_names(self):
        names = [self.base.skill_name(arm) for arm in adapter.ARMS]
        self.assertEqual(len(set(names)), 3)
        for name in names:
            self.assertRegex(name, r'^[a-z0-9-]+$')

    def test_current_agent_preserved_in_full(self):
        source = self.base.body((adapter.REPO / 'generated/opencode/agents/developer.md').read_text())
        expected = adapter.substitute(source, 'hdev', self.manifest)
        actual = (ROOT / 'profiles-v2/developer/agent.md').read_text().split('\n\nIdentidad técnica de laboratorio:')[0]
        self.assertEqual(actual, expected)
        source_skill = adapter.REPO / 'generated/opencode/skills/developer/SKILL.md'
        self.assertEqual((ROOT / 'profiles-v2/developer/skills/hdev-developer/SKILL.md').read_text(),
                         adapter.substitute(source_skill.read_text(), 'hdev', self.manifest))

    def test_odd_exact_historical_body(self):
        text = (adapter.REPO / 'docs/experimentos/odd-vs-sdd-2026-11-04/tratamiento-b.md').read_text()
        expected = text.split('<!-- experimental-instructions:start -->')[1].split('<!-- experimental-instructions:end -->')[0].strip()
        expected = expected.replace('`data-api`', '`hodd-data-api`').replace('`ui-design`', '`hodd-ui-design`')
        actual = self.base.body((ROOT / 'profiles-v2/odd/skills/hodd-odd-workflow/SKILL.md').read_text())
        self.assertEqual(actual, expected)

    def test_same_domain_skills_for_all_arms(self):
        for arm in adapter.ARMS:
            for sid in ('data-api', 'ui-design'):
                source = adapter.REPO / 'generated/opencode/skills' / sid
                target = ROOT / 'profiles-v2' / arm / 'skills' / (self.base.namespace(arm) + '-' + sid)
                for file in source.rglob('*.md'):
                    self.assertEqual((target / file.relative_to(source)).read_text(),
                                     adapter.substitute(file.read_text(), self.base.namespace(arm), self.manifest))

    def test_identical_task_no_targeted_candidate_clues(self):
        original = json.loads((adapter.SOURCE / 'cases.json').read_text())
        cases = json.loads((ROOT / 'cases.json').read_text())
        self.assertEqual(cases['tasks'], [case for case in original['tasks'] if case['id'] == 'TASK-2'])
        candidate = (adapter.PACKAGE / 'candidato/SKILL.md').read_text()
        self.assertFalse(re.search(r'SQLite|Reservation|Idempotency|reserve/|TASK-2', candidate))
        self.assertNotIn('Risk: none', candidate)
        self.assertNotIn('## Specs', candidate)

    def test_configuration_limits_and_tools_equivalent(self):
        limits = []
        for arm in adapter.ARMS:
            cfg = self.base.configuration(ROOT, arm, ROOT / 'runs' / arm)
            agent = cfg['agent'][self.base.agent_name(arm)]
            permission = agent['permission']
            limits.append((agent['model'], agent['steps'], agent['temperature'], permission['bash'],
                           {key: permission[key] for key in ('task', 'question', 'webfetch', 'google_search', 'antigravity_quota')}))
            self.assertEqual(permission['edit']['*.key'], 'deny')
            self.assertEqual(permission['skill']['*'], 'deny')
            self.assertEqual(permission['skill'][self.base.skill_name(arm)], 'allow')
        self.assertEqual(limits[0], limits[1])
        self.assertEqual(limits[0], limits[2])

    def test_inputs_cover_candidate_and_adapter(self):
        inputs = self.base.source_inputs(ROOT)
        self.assertIn('candidate/SKILL.md', inputs)
        self.assertIn('adapter-source', inputs)
        self.assertIn('historical-runner-source', inputs)
        self.assertIn('historical-freeze', inputs)
        self.assertTrue(any(name.startswith('oracles/') for name in inputs))


if __name__ == '__main__':
    unittest.main()
