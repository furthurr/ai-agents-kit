#!/usr/bin/env python3
"""Offline equivalence checks, no model calls or credential access."""
import json
from pathlib import Path
import tempfile
import unittest

import developer_compact_benchmark as bench

TEST_TMP = Path(tempfile.gettempdir()) / 'opencode'


class CompactTests(unittest.TestCase):
    def test_treatment_labels_do_not_change_agent_or_skill_id(self):
        self.assertEqual(bench.agent_name('A'), bench.agent_name('B'))
        self.assertEqual(bench.skill_name('A'), bench.skill_name('B'))
        self.assertNotEqual(bench.skill_name('A'), bench.skill_name('C'))

    def test_shared_context_and_identity_once(self):
        text = bench.candidate_body()
        for source in ['project-context.md', 'mas-identity.md']:
            fragment = (bench.REPO / 'canonical/shared' / source).read_text().strip()
            self.assertEqual(text.count(fragment), 1)
        self.assertNotIn('{{', text)

    def test_unique_guards_are_preserved(self):
        text = bench.candidate_body()
        for fragment in ['dc-developer', '.sdd/', 'No delegues', 'selección manual',
                         'carga, error', 'persistencia', 'AGENTS.md', 'documentación canónica']:
            self.assertIn(fragment, text)
        self.assertIn('autoridad', text)
        self.assertNotIn('test-first', text)

    def test_task_prompts_identical_between_A_B(self):
        for sid, case in bench.base.load_cases().items():
            seed = 'WORK.md' if sid == 'S08' else None
            self.assertEqual(bench.base.task_prompt(case, 'A', seed), bench.base.task_prompt(case, 'B', seed))

    def test_seed_same_between_A_B(self):
        with tempfile.TemporaryDirectory(dir=TEST_TMP if TEST_TMP.is_dir() else None) as tmp:
            root = Path(tmp)
            for arm in ('A', 'B', 'C'):
                (root / arm).mkdir()
                bench.seed_resume(root / arm, arm)
            self.assertEqual((root / 'A/WORK.md').read_bytes(), (root / 'B/WORK.md').read_bytes())
            self.assertTrue((root / 'C/odd/tasks/slug.md').exists())
            self.assertFalse((root / 'A/.sdd').exists())

    def test_profiles_are_identical_except_agent(self):
        with tempfile.TemporaryDirectory(dir=TEST_TMP if TEST_TMP.is_dir() else None) as tmp:
            root = Path(tmp)
            bench.prepare(root)
            result = bench.profile_equivalence(root)
            self.assertTrue(result['skills_and_references_identical'])
            self.assertLess(result['agent_bytes_B'], result['agent_bytes_A'])
            self.assertEqual(result['primary_skill_sha256_A'], result['primary_skill_sha256_B'])

    def test_source_namespace_does_not_rename_collaborating_agents(self):
        manifest = json.loads((bench.REPO / 'canonical/manifest.json').read_text())
        text = bench.namespace_text('`developer` `data-api` `documentation-orchestrator` `sdd`', 'A', manifest)
        self.assertEqual(text, '`dc-developer` `dc-data-api` `documentation-orchestrator` `sdd`')


if __name__ == '__main__':
    unittest.main()
