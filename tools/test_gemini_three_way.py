#!/usr/bin/env python3
"""Focused offline tests; no provider calls, credentials or global config."""
import json
from pathlib import Path
import tempfile
import unittest

import gemini_three_way as bench


class HarnessTests(unittest.TestCase):
    def test_mode_uses_response_field_not_score_or_tool_text(self):
        for text, mode in [
            ('Recomendación: Direct', 'direct'),
            ('**Recomendación:** **SDD-Tiny**', 'tiny'),
            ('Recomendación: `SDD-Lite`', 'lite'),
            ('Profundidad recomendada: SDD-Tiny', 'tiny'),
            ('Existen Direct, Tiny y Lite; ¿qué eliges?', None),
            ('Esfuerzo 2; todavía no recomiendo un modo.', None),
        ]:
            with self.subTest(text=text):
                self.assertEqual(bench.recommended_mode(text), mode)

    def test_sanitizer_never_retains_transport_or_private_reasoning(self):
        raw = '\n'.join(json.dumps(event) for event in [
            {'type': 'reasoning', 'part': {'type': 'reasoning', 'text': 'PRIVATE_TEST_PAYLOAD'}},
            {'type': 'error', 'error': {'name': 'APIError', 'data': {
                'statusCode': 429, 'message': 'The usage limit has been reached',
                'responseHeaders': {'test-header': 'TRANSPORT_TEST_PAYLOAD'},
                'responseBody': 'BODY_TEST_PAYLOAD'}}},
            {'type': 'step_finish', 'part': {'tokens': {'input': 4}, 'cost': 0,
                                           'metadata': {'opaque': 'OPAQUE_TEST_PAYLOAD'}}},
        ])
        clean = bench.clean_events(raw)
        value = json.dumps(clean)
        for marker in ['PRIVATE_TEST_PAYLOAD', 'TRANSPORT_TEST_PAYLOAD', 'BODY_TEST_PAYLOAD', 'OPAQUE_TEST_PAYLOAD']:
            self.assertNotIn(marker, value)
        self.assertEqual(clean[0]['error']['category'], 'quota')
        self.assertEqual(clean[1]['part']['tokens']['input'], 4)

    def test_successful_process_with_error_event_is_not_healthy(self):
        self.assertFalse(bench.healthy({'returncode': 0, 'timeout': False, 'events': [{'type': 'error'}]}))

    def test_gates_are_not_approved_in_task_files(self):
        cases = bench.load_cases()
        prompt = bench.task_prompt(cases['S03'], 'sdd')
        self.assertIn('no hay modo SDD elegido', prompt)
        self.assertIn('no equivale a aprobar gates', prompt)
        self.assertNotIn('Selecciono explícitamente modo tiny', prompt)

    def test_secret_denies_and_outside_boundary_remain(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for arm in bench.ARMS:
                p = bench.policy(root, arm, root / 'fixture')
                self.assertEqual(p['external_directory']['*'], 'deny')
                self.assertEqual(p['read']['*.env*'], 'deny')
                self.assertEqual(p['bash']['*.env*'], 'deny')
                self.assertEqual(p['task'], 'deny')
                self.assertEqual(p['skill']['*'], 'deny')
                self.assertEqual(p['skill'][bench.skill_name(arm)], 'allow')
                self.assertEqual(bench.policy(root, arm, root / 'fixture', 'read')['edit']['*'], 'deny')

    def test_negative_close_marker_does_not_approve_gate(self):
        self.assertFalse(bench.premature_close({'spec.md': 'Estado: pendiente de Gate 4; no cerrado\nGate 4: pendiente'}))
        self.assertTrue(bench.premature_close({'spec.md': 'Estado: Cerrado\n'}))

    def test_artifact_write_is_exclusive(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'record.json'
            bench.write_json(p, {'attempt': 1}, exclusive=True)
            with self.assertRaises(FileExistsError):
                bench.write_json(p, {'attempt': 2}, exclusive=True)
            self.assertEqual(json.loads(p.read_text())['attempt'], 1)


if __name__ == '__main__':
    unittest.main()
