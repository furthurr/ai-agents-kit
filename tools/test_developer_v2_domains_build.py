import json
from pathlib import Path
import unittest

import developer_v2_domains_build as adapter

ROOT = Path('/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/developer-v2-domains-build-gemini-20261105').resolve()


class DomainsBuildTests(unittest.TestCase):
    def setUp(self):
        self.base, self.old = adapter.context(ROOT)
        self.manifest = json.loads((adapter.REPO / 'canonical/manifest.json').read_text())

    def test_previous_cohorts_unchanged(self):
        source = self.old.SOURCE
        original = adapter.module_at('unchanged_original', source / 'runner.py')
        original.check_frozen(source)
        prior = adapter.module_at('unchanged_prior_adapter', adapter.REPO / 'tools/developer_v2_high_benchmark.py')
        prior.context(source.parent / 'developer-v2-high-gemini-20261105').check_frozen(source.parent / 'developer-v2-high-gemini-20261105')

    def test_native_build_no_methodology_prompt_or_primary(self):
        cfg = self.base.configuration(ROOT, 'build', ROOT / 'runs/build-test')
        self.assertEqual(self.base.agent_name('build'), 'build')
        self.assertNotIn('prompt', cfg['agent']['build'])
        self.assertNotIn('description', cfg['agent']['build'])
        self.assertIsNone(self.base.primary_loaded(ROOT, 'build', []))
        self.assertFalse((ROOT / 'profiles-v2/build/agent.md').exists())
        allowed = cfg['agent']['build']['permission']['skill']
        self.assertEqual(allowed, {'*': 'deny', 'bld-data-api': 'allow', 'bld-ui-design': 'allow'})
        native = json.loads((ROOT / 'native-base.json').read_text())
        self.assertTrue(native['native'])
        self.assertFalse(native['prompt_present'])

    def test_shared_prompt_patch_only_one_exception(self):
        original = (self.old.SOURCE / 'runner.py').read_text()
        metadata = json.loads((ROOT / 'treatments.json').read_text())['shared_runner_patch']
        self.assertEqual(original.count(metadata['before']), 1)
        self.assertEqual((ROOT / 'shared_runner.py').read_text(), original.replace(metadata['before'], metadata['after']))

    def test_specialized_controls_and_domain_content(self):
        expected = self.old.substitute(self.base.body((adapter.REPO / 'generated/opencode/agents/developer.md').read_text()), 'hdev', self.manifest)
        actual = (ROOT / 'profiles-v2/developer/agent.md').read_text().split('\n\nIdentidad técnica de laboratorio:')[0]
        self.assertEqual(actual, expected)
        odd = (adapter.REPO / 'docs/experimentos/odd-vs-sdd-2026-11-04/tratamiento-b.md').read_text().split('<!-- experimental-instructions:start -->')[1].split('<!-- experimental-instructions:end -->')[0].strip()
        odd = odd.replace('`data-api`', '`hodd-data-api`').replace('`ui-design`', '`hodd-ui-design`')
        self.assertEqual(self.base.body((ROOT / 'profiles-v2/odd/skills/hodd-odd-workflow/SKILL.md').read_text()), odd)
        for arm in adapter.ARMS:
            for sid in ('data-api', 'ui-design'):
                original = adapter.REPO / 'generated/opencode/skills' / sid
                target = ROOT / 'profiles-v2' / arm / 'skills' / (self.base.namespace(arm) + '-' + sid)
                for file in original.rglob('*.md'):
                    self.assertEqual((target / file.relative_to(original)).read_text(), self.old.substitute(file.read_text(), self.base.namespace(arm), self.manifest))

    def test_limits_and_permissions_match(self):
        normalized = []
        for arm in adapter.ARMS:
            cfg = self.base.configuration(ROOT, arm, ROOT / 'runs' / arm)['agent'][self.base.agent_name(arm)]
            permission = cfg['permission']
            normalized.append((cfg['model'], cfg['steps'], cfg['temperature'], permission['bash'], permission['task'], permission['google_search']))
            self.assertEqual(permission['skill']['*'], 'deny')
            self.assertEqual(permission['edit']['*.key'], 'deny')
        self.assertTrue(all(value == normalized[0] for value in normalized))

    def test_same_high_task_and_generic_candidate(self):
        source = json.loads((self.old.SOURCE / 'cases.json').read_text())
        actual = json.loads((ROOT / 'cases.json').read_text())
        self.assertEqual(actual['tasks'], [case for case in source['tasks'] if case['id'] == 'TASK-2'])
        candidate = (adapter.PACKAGE / 'candidato/SKILL.md').read_text()
        for term in ('Reservation', 'SQLite', 'TASK-2', 'Idempotency-Key'):
            self.assertNotIn(term, candidate)
        self.assertIn('Si abarca ambos, carga ambas', candidate)
        self.assertIn('Si no toca ninguno, no las cargues', candidate)
        self.assertIn('aunque no hayas cargado skills', candidate)

    def test_five_probe_contracts_and_frozen_inputs(self):
        cases = json.loads((ROOT / 'probe-cases.json').read_text())
        self.assertEqual(len(cases), 5)
        self.assertEqual([case['expected'] for case in cases], [['data-api'], ['ui-design'], [], [], []])
        inputs = self.base.source_inputs(ROOT)
        for key in ('shared_runner.py', 'probe-cases.json', 'native-base.json', 'domains-adapter', 'candidate/SKILL.md'):
            self.assertIn(key, inputs)


if __name__ == '__main__':
    unittest.main()
