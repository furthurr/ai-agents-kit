import json
from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch
import odd_standards_gemini38_v3 as gemini38_v3

ROOT = Path('/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/odd-standards-gemini38-v3-20261108').resolve()

class Gemini38V3Tests(unittest.TestCase):
    def test_both_profiles_request_identical_model_with_temperature(self):
        base, _ = gemini38_v3.context(ROOT)
        for arm in ('odd', 'adjusted'):
            cfg = base.configuration(ROOT, arm, ROOT / 'probe')
            agent = cfg['agent'][base.agent_name(arm)]
            self.assertEqual(agent['model'], 'github-copilot/gemini-3.8-flash')
            self.assertEqual(agent['temperature'], 0.2)
            self.assertEqual(agent['steps'], 60)

    def test_invoke_enforces_timeout_1200_even_when_caller_passes_limit_600(self):
        base, _ = gemini38_v3.context(ROOT)
        child = MagicMock()
        child.communicate.return_value = (b'{"type":"text","sessionID":"s","part":{"text":"ok"}}\n', b'')
        child.returncode = 0
        with patch.object(gemini38_v3.subprocess, 'Popen', return_value=child) as call:
            # Caller passes limit=600 explicitly (simulating runner.py line 568)
            result = base.invoke(ROOT, 'odd', ROOT / 'probe', 'test', limit=600)
        argv = call.call_args.args[0]
        self.assertEqual(argv[argv.index('--model')+1], 'github-copilot/gemini-3.8-flash')
        self.assertEqual(result['model_requested'], 'github-copilot/gemini-3.8-flash')
        # child.communicate MUST receive timeout=1200
        child.communicate.assert_called_with(timeout=1200)

    def test_protocol_and_inputs_registered(self):
        base, _ = gemini38_v3.context(ROOT)
        self.assertEqual(base.PROTOCOL, 'odd-standards-gemini38-v3-20261108')
        inputs = base.source_inputs(ROOT)
        self.assertIn(str(gemini38_v3.PACKAGE / 'protocolo.md'), inputs)
        self.assertIn('model-provenance.json', inputs)

if __name__ == '__main__':
    unittest.main()
