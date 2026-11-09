import json
from pathlib import Path
import unittest
import odd_context_routing as experiment

ROOT = Path('/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/odd-context-routing-luna-max-v1').resolve()


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.base, _ = experiment.context(ROOT)

    def test_control_is_prior_adjusted_and_treatment_only_adds_routing(self):
        prior = self.base.body((experiment.PRIOR / 'profiles-v2/adjusted/skills/ob-odd-workflow/SKILL.md').read_text())
        control = self.base.body((ROOT / 'profiles-v2/odd/skills/oa-odd-workflow/SKILL.md').read_text())
        control = control.replace('`oa-data-api`', '`ob-data-api`').replace('`oa-ui-design`', '`ob-ui-design`')
        routed = self.base.body((ROOT / 'profiles-v2/adjusted/skills/ob-odd-workflow/SKILL.md').read_text())
        self.assertEqual(control, prior)
        self.assertEqual(routed, prior + '\n\n' + (experiment.PACKAGE / 'ruta-contexto.md').read_text().strip())

    def test_code_unchanged_and_maps_shared(self):
        prior, _ = experiment.previous.context(experiment.PRIOR)
        prior.check_frozen(experiment.PRIOR)
        current = self.base.hashes(ROOT / 'baseline')
        for name, value in prior.hashes(experiment.PRIOR / 'baseline').items():
            self.assertEqual(current[name], value)
        extra = set(current) - set(prior.hashes(experiment.PRIOR / 'baseline'))
        self.assertEqual(extra, {'.navigator/ai-context.md', '.architecture/README.md', '.architecture/flows.md'})
        for name in extra:
            self.assertEqual(self.base.sha(ROOT / 'baseline' / name), self.base.sha(ROOT / 'references/TASK-2' / name))
        for arm in ('odd', 'adjusted'):
            cfg = self.base.configuration(ROOT, arm, ROOT / 'proof')['agent'][self.base.agent_name(arm)]
            self.assertEqual(cfg['model'], 'openai/gpt-6-luna')
            self.assertEqual(cfg['steps'], 60)

    def test_no_new_task_or_oracle_and_no_solution_in_maps(self):
        self.assertEqual(self.base.sha(ROOT / 'cases.json'), self.base.sha(experiment.PRIOR / 'cases.json'))
        self.assertEqual(self.base.hashes(ROOT / 'oracles'), self.base.hashes(experiment.PRIOR / 'oracles'))
        for file in (experiment.PACKAGE / 'fixtures').rglob('*.md'):
            text = file.read_text()
            for term in ('Reservation', 'Idempotency-Key', 'test_oracle_task2', '/reserve/'):
                self.assertNotIn(term, text)
        self.assertIn('navigation-plan.json', self.base.source_inputs(ROOT))

    def test_sources_referenced_by_map_exist(self):
        for path in ('catalog/models.py', 'catalog/views.py', 'catalog/urls.py', 'locallibrary/urls.py',
                     'catalog/forms.py', 'catalog/templates/base_generic.html',
                     'catalog/templates/catalog/book_detail.html', 'catalog/static/css/styles.css',
                     'catalog/tests/test_models.py', 'catalog/tests/test_forms.py', 'catalog/tests/test_views.py',
                     'catalog/templates/catalog/book_renew_librarian.html', 'docs/lab-context.md'):
            self.assertTrue((ROOT / 'baseline' / path).is_file(), path)


if __name__ == '__main__':
    unittest.main()
