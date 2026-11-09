import json
from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch
import odd_standards_luna as luna

ROOT = Path('/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/odd-standards-luna-max-20261105').resolve()

class LunaTests(unittest.TestCase):
    def test_both_profiles_request_identical_model_no_temperature(self):
        base, _ = luna.context(ROOT)
        for arm in ('odd', 'adjusted'):
            cfg = base.configuration(ROOT, arm, ROOT / 'probe')
            agent = cfg['agent'][base.agent_name(arm)]
            self.assertEqual(agent['model'], 'openai/gpt-6-luna')
            self.assertNotIn('temperature', agent)
            self.assertEqual(agent['steps'], 60)

    def test_invocation_explicit_variant_max(self):
        base, _ = luna.context(ROOT)
        child = MagicMock()
        child.communicate.return_value = (b'{"type":"text","sessionID":"s","part":{"text":"ok"}}\n', b'')
        child.returncode = 0
        with patch.object(luna.subprocess, 'Popen', return_value=child) as call:
            result = base.invoke(ROOT, 'odd', ROOT / 'probe', 'test')
        argv = call.call_args.args[0]
        self.assertEqual(argv[argv.index('--model')+1], 'openai/gpt-6-luna')
        self.assertEqual(argv[argv.index('--variant')+1], 'max')
        self.assertEqual(result['variant_requested'], 'max')

    def test_previous_inputs_and_profiles_unchanged(self):
        base, _ = luna.context(ROOT)
        prior, _ = luna.retry.original.context(luna.retry.PARTIAL)
        prior.check_frozen(luna.retry.PARTIAL)
        for folder in ('baseline', 'oracles', 'references', 'profiles-v2'):
            self.assertEqual(base.hashes(ROOT / folder), prior.hashes(luna.retry.PARTIAL / folder))
        self.assertEqual(base.sha(ROOT / 'cases.json'), prior.sha(luna.retry.PARTIAL / 'cases.json'))
        self.assertIn(str(luna.PACKAGE / 'protocolo.md'), base.source_inputs(ROOT))

if __name__ == '__main__':
    unittest.main()
