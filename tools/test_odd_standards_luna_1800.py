from pathlib import Path
import unittest
from unittest.mock import patch
import odd_standards_luna_1800 as experiment

ROOT = Path('/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/odd-standards-luna-max-1800-20261105').resolve()

class BudgetTests(unittest.TestCase):
    def test_both_models_and_budget(self):
        base, _ = experiment.context(ROOT)
        for arm in ('odd', 'adjusted'):
            cfg = base.configuration(ROOT, arm, ROOT / 'probe')
            agent = cfg['agent'][base.agent_name(arm)]
            self.assertEqual(agent['model'], 'openai/gpt-6-luna')
            self.assertNotIn('temperature', agent)
        self.assertEqual(experiment.TIMEOUT, 1800)

    def test_override_passes_1800_to_underlying_invoke(self):
        with patch.object(experiment.luna, 'context') as make:
            original = unittest.mock.MagicMock()
            invoke = original.invoke
            original.source_inputs.return_value = {}
            make.return_value = (original, None)
            base, _ = experiment.context(ROOT)
            base.invoke(ROOT, 'odd', ROOT / 'probe', 'p', limit=600)
            self.assertEqual(invoke.call_args.kwargs['limit'], 1800)

    def test_prior_and_profiles_unchanged(self):
        current, _ = experiment.context(ROOT)
        prior, _ = experiment.luna.context(experiment.PRIOR)
        prior.check_frozen(experiment.PRIOR)
        for folder in ('baseline', 'oracles', 'references', 'profiles-v2'):
            self.assertEqual(current.hashes(ROOT / folder), prior.hashes(experiment.PRIOR / folder))
        self.assertEqual(current.sha(ROOT / 'cases.json'), prior.sha(experiment.PRIOR / 'cases.json'))

if __name__ == '__main__':
    unittest.main()
