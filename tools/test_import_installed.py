#!/usr/bin/env python3
"""Exercise the importer in temporary profiles; never read installed host profiles."""
from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import import_installed


class ImportInstalledTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.repo = self.base / "repo"
        (self.repo / "canonical").mkdir(parents=True)
        (self.repo / "canonical/manifest.json").write_text(json.dumps({
            "platforms": ["opencode"], "skills": ["sample"], "agents": ["review"],
        }))
        adapters = self.repo / "adapters/opencode/agents"
        adapters.mkdir(parents=True)
        (adapters / "review.json").write_text(json.dumps({"filename": "review.md"}))
        self.skills = self.base / "skills"
        self.agents = self.base / "agents"
        (self.skills / "sample").mkdir(parents=True)
        self.agents.mkdir()
        (self.skills / "sample/SKILL.md").write_text("legitimate skill")
        (self.agents / "review.md").write_text("legitimate agent")
        self.external = self.base / "external"
        self.external.mkdir()
        (self.external / "sentinel.txt").write_text("external sentinel")

    def run_import(self, *extra):
        args = ["import_installed.py", "opencode", "--skills-dir", str(self.skills),
                "--agents-dir", str(self.agents), *extra]
        with patch.object(import_installed, "ROOT", self.repo), patch("sys.argv", args):
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                return import_installed.main()

    def assert_rejected_without_snapshot(self):
        self.assertNotEqual(self.run_import(), 0)
        self.assertFalse((self.repo / "imports").exists())

    def test_regular_artifacts_and_unknown_entries(self):
        (self.skills / "unknown").symlink_to(self.external, target_is_directory=True)
        (self.skills / "sample/.DS_Store").write_text("ignored")
        self.assertEqual(self.run_import(), 0)
        imported = list((self.repo / "imports/opencode").iterdir())
        self.assertEqual(len(imported), 1)
        self.assertEqual((imported[0] / "skills/sample/SKILL.md").read_text(), "legitimate skill")
        self.assertEqual((imported[0] / "agents/review.md").read_text(), "legitimate agent")
        self.assertFalse((imported[0] / "skills/sample/.DS_Store").exists())
        self.assertFalse((imported[0] / "skills/unknown").exists())

    def test_dry_run_validates_without_writing(self):
        self.assertEqual(self.run_import("--dry-run"), 0)
        self.assertFalse((self.repo / "imports").exists())

    def test_declared_agent_symlink_to_external_file(self):
        (self.agents / "review.md").unlink()
        (self.agents / "review.md").symlink_to(self.external / "sentinel.txt")
        self.assert_rejected_without_snapshot()

    def test_declared_skill_symlink_to_external_directory(self):
        (self.skills / "sample/SKILL.md").unlink()
        (self.skills / "sample").rmdir()
        (self.skills / "sample").symlink_to(self.external, target_is_directory=True)
        self.assert_rejected_without_snapshot()

    def test_nested_internal_and_external_links_are_rejected(self):
        for target in (self.skills / "sample/SKILL.md", self.external / "sentinel.txt",
                       self.external, self.base / "missing"):
            with self.subTest(target=target):
                link = self.skills / "sample/link"
                link.symlink_to(target, target_is_directory=target.is_dir())
                try:
                    self.assert_rejected_without_snapshot()
                finally:
                    link.unlink()

    def test_linked_source_root_and_parent_are_rejected(self):
        for suffix in ("", "/sample", "/sample/.."):
            with self.subTest(suffix=suffix):
                alias = self.base / "alias"
                alias.symlink_to(self.skills, target_is_directory=True)
                original = self.skills
                self.skills = Path(str(alias) + suffix)
                try:
                    self.assert_rejected_without_snapshot()
                finally:
                    self.skills = original
                    alias.unlink()

    def test_dry_run_rejects_links_too(self):
        (self.skills / "sample/link").symlink_to(self.external)
        self.assertNotEqual(self.run_import("--dry-run"), 0)
        self.assertFalse((self.repo / "imports").exists())

    @unittest.skipUnless(hasattr(os, "mkfifo"), "POSIX FIFO required")
    def test_special_file_is_rejected_without_blocking(self):
        os.mkfifo(self.skills / "sample/pipe")
        self.assert_rejected_without_snapshot()

    def test_missing_sources_are_skipped(self):
        self.skills = self.base / "absent-skills"
        self.agents = self.base / "absent-agents"
        self.assertEqual(self.run_import(), 0)
        self.assertFalse((self.repo / "imports").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
