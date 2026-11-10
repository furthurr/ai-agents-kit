#!/usr/bin/env python3
"""Pruebas unitarias para el arnés real_android_gemini_benchmark.py."""
from pathlib import Path
import tempfile
import unittest

import real_android_gemini_benchmark as bench


class GeneraAndroidBenchmarkTests(unittest.TestCase):

    def test_arms_and_tasks_configuration(self):
        self.assertEqual(len(bench.ARMS), 5)
        self.assertIn('v2_reforzado', bench.ARMS)
        self.assertIn('v2', bench.ARMS)
        self.assertIn('developer_actual', bench.ARMS)
        self.assertIn('build_sin_mas', bench.ARMS)
        self.assertIn('build_mas', bench.ARMS)

        self.assertEqual(len(bench.TASKS), 3)
        self.assertEqual(bench.TASKS['1']['complexity'], 'media-baja')
        self.assertEqual(bench.TASKS['2']['complexity'], 'media-alta')
        self.assertEqual(bench.TASKS['3']['complexity'], 'alta')

    def test_task_files_exist(self):
        for tid, meta in bench.TASKS.items():
            self.assertTrue(meta['file'].exists(), f"El archivo de la tarea {tid} debe existir: {meta['file']}")
            self.assertTrue(meta['oracle_source'].exists(), f"El archivo de oráculo de la tarea {tid} debe existir: {meta['oracle_source']}")

    def test_reinforce_adds_deltas(self):
        raw_skill = "- **Comprobar.**\n- **Continuidad bajo demanda.**\n"
        reinf = bench.reinforce(raw_skill)
        self.assertIn(bench.DELTA_A, reinf)
        self.assertIn(bench.DELTA_B, reinf)

    def test_prepare_local_properties_regenerates_only_sdk_dir(self):
        with tempfile.TemporaryDirectory() as temp:
            ws = Path(temp)
            (ws / 'local.properties').write_text("sdk.dir=/old/path\nsecret=xyz\n")
            bench.prepare_local_properties(ws)
            content = (ws / 'local.properties').read_text()
            self.assertIn(f"sdk.dir={bench.ANDROID_HOME}", content)
            self.assertNotIn("/old/path", content)
            self.assertNotIn("secret=xyz", content)

    def test_sandbox_permissions(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            task_id = '1'
            task_dir = root / f'task_{task_id}'
            for arm in bench.ARMS:
                (task_dir / 'runs' / arm).mkdir(parents=True, exist_ok=True)
                (task_dir / 'profiles' / arm / 'skills').mkdir(parents=True, exist_ok=True)
                (task_dir / 'profiles' / arm / 'agent.md').write_text("Agent prompt")

                cfg = bench.configuration(root, task_id, arm)
                agent_k = bench.agent_name(arm)
                perm = cfg['agent'][agent_k]['permission']

                # Comandos permitidos
                self.assertEqual(perm['bash']['./gradlew :core:domain:test*'], 'allow')
                self.assertEqual(perm['bash']['git status*'], 'allow')
                self.assertEqual(perm['bash']['git diff*'], 'allow')
                self.assertEqual(perm['bash']['*'], 'deny')

                # Permisos de escritura y edición
                self.assertIn('write', perm)
                self.assertIn('edit', perm)
                self.assertEqual(perm['write']['*'], 'deny')
                self.assertEqual(perm['edit']['*'], 'deny')

                # Denegaciones estrictas
                for sec in bench.SECRETS:
                    self.assertEqual(perm['bash'][sec], 'deny')
                    self.assertEqual(perm['read'][sec], 'deny')
                    self.assertEqual(perm['write'][sec], 'deny')

                # MAS context rules
                if arm == 'build_sin_mas':
                    self.assertEqual(cfg['instructions'], [])
                    self.assertNotIn('data-api', perm['skill'])
                else:
                    self.assertIn('data-api', perm['skill'])
                    self.assertIn('ui-design', perm['skill'])
                    self.assertIn(str(task_dir / 'runs' / arm / 'AGENTS.md'), cfg['instructions'])


if __name__ == '__main__':
    unittest.main()
