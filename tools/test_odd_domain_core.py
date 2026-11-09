import hashlib
import json
from pathlib import Path
import unittest
import odd_domain_core as experiment

ROOT = Path('/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/odd-domain-core-luna-max-v1').resolve()


class DomainCoreTests(unittest.TestCase):
    def setUp(self):
        self.base, _ = experiment.context(ROOT)

    def test_primary_odd_same_after_namespaces(self):
        control = self.base.body((ROOT / 'profiles-v2/odd/skills/oa-odd-workflow/SKILL.md').read_text())
        treatment = self.base.body((ROOT / 'profiles-v2/adjusted/skills/ob-odd-workflow/SKILL.md').read_text())
        self.assertEqual(control.replace('`oa-data-api`', '`ob-data-api`').replace('`oa-ui-design`', '`ob-ui-design`'), treatment)
        expected = self.base.body((experiment.PRIOR / 'profiles-v2/adjusted/skills/ob-odd-workflow/SKILL.md').read_text())
        self.assertEqual(treatment, expected)
        self.assertNotIn('Ruta selectiva de contexto', treatment)

    def test_full_original_and_templates_preserved(self):
        for domain in ('data-api', 'ui-design'):
            control = ROOT / 'profiles-v2/odd/skills' / ('oa-' + domain)
            treatment = ROOT / 'profiles-v2/adjusted/skills' / ('ob-' + domain)
            original = (control / 'SKILL.md').read_text().replace('oa-', 'ob-')
            self.assertEqual((treatment / 'original-contract.md').read_text(), original)
            for file in (control / 'references').rglob('*.md'):
                self.assertEqual((treatment / 'references' / file.relative_to(control / 'references')).read_text(), file.read_text().replace('oa-', 'ob-'))

    def test_lossless_partition_and_hash_ledger(self):
        manifest = json.loads((ROOT / 'partition-manifest.json').read_text())
        for domain in ('data-api', 'ui-design'):
            directory = ROOT / 'profiles-v2/adjusted/skills' / ('ob-' + domain)
            original = (directory / 'original-contract.md').read_text()
            header, parts = experiment.sections(original)
            self.assertEqual(header + ''.join(part['text'] for part in parts), original)
            core, impl, doc, ledger = experiment.partition(original, domain)
            self.assertEqual((directory / 'SKILL.md').read_text(), core)
            self.assertEqual((directory / 'implementation.md').read_text(), impl)
            self.assertEqual((directory / 'documentation.md').read_text(), doc)
            self.assertEqual(manifest[domain]['sections_in_original_order'], ledger)
            self.assertEqual(manifest[domain]['source_sha256'], hashlib.sha256(original.encode()).hexdigest())
            self.assertLess(len(core.encode()) + len(impl.encode()), len(original.encode()))

    def test_same_project_no_navigation_maps(self):
        previous, _ = experiment.previous.context(experiment.PRIOR)
        previous.check_frozen(experiment.PRIOR)
        for folder in ('baseline', 'oracles', 'references'):
            self.assertEqual(self.base.hashes(ROOT / folder), previous.hashes(experiment.PRIOR / folder))
        self.assertFalse((ROOT / 'baseline/.navigator').exists())
        self.assertFalse((ROOT / 'baseline/.architecture').exists())
        self.assertEqual(self.base.sha(ROOT / 'cases.json'), previous.sha(experiment.PRIOR / 'cases.json'))

    def test_equal_model_and_permission_budget(self):
        configs = []
        for arm in ('odd', 'adjusted'):
            cfg = self.base.configuration(ROOT, arm, ROOT / 'proof')['agent'][self.base.agent_name(arm)]
            permission = cfg['permission']
            configs.append((cfg['model'], cfg['steps'], permission['bash'], permission['task'], permission['google_search']))
            self.assertNotIn('temperature', cfg)
        self.assertEqual(*configs)

    def test_core_has_no_task_clues_and_requires_reference(self):
        core = (experiment.PACKAGE / 'nucleo.md').read_text()
        self.assertIn('lee `implementation.md`', core)
        self.assertIn('original-contract.md', core)
        for term in ('Reservation', 'SQLite', 'Idempotency-Key', 'TASK-2'):
            self.assertNotIn(term, core)
        self.assertIn('partition-manifest.json', self.base.source_inputs(ROOT))


if __name__ == '__main__':
    unittest.main()
