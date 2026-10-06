#!/usr/bin/env python3
"""Distribution contracts; these checks do not certify an Antigravity runtime."""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import render
import validate
from test_install import PLATFORMS

ROOT = Path(__file__).resolve().parent.parent
LOCAL_TOOLS = {
    "view_file", "list_dir", "find_by_name", "grep_search", "write_to_file",
    "replace_file_content", "run_command", "ask_question",
}
WEB_TOOLS = {"read_url_content", "search_web"}


class AntigravityContract(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / "canonical/manifest.json").read_text(encoding="utf-8"))
        self.adapters = ROOT / "adapters/antigravity"

    def test_manifest(self):
        self.assertIn("antigravity", self.manifest["platforms"])
        self.assertTrue({"copilot", "opencode", "kiro", "claude", "pi"}.issubset(self.manifest["platforms"]))

    def test_installer_inventory(self):
        self.assertIn("antigravity", PLATFORMS, "Native installers must be in the existing test inventory")
        self.assertEqual(PLATFORMS["antigravity"],
                         (".gemini/config/skills", ".gemini/config/agents", ".antigravity-kit-backup"))

    def test_substitutions(self):
        path = self.adapters / "platform.json"
        self.assertTrue(path.is_file(), "Antigravity platform adapter missing")
        self.assertEqual(json.loads(path.read_text(encoding="utf-8")), {"substitutions": {
            "{{sdd_agent}}": "sdd", "{{gate_instruction}}": "",
            "{{steering_paths}}": "`GEMINI.md`, `AGENTS.md`, `.agents/rules/*.md`",
        }})

    def test_agents(self):
        self.assertTrue(self.adapters.is_dir(), "Antigravity adapters missing")
        self.assertEqual({p.stem for p in (self.adapters / "agents").glob("*.json")}, set(self.manifest["agents"]))
        for aid in self.manifest["agents"]:
            with self.subTest(agent=aid):
                data = json.loads((self.adapters / "agents" / f"{aid}.json").read_text(encoding="utf-8"))
                errors: list[str] = []
                validate.validate_antigravity_adapter(data, aid, f"{aid}.json", errors)
                self.assertEqual(errors, [])
                fm = data["frontmatter"]
                self.assertEqual(fm["model"], "inherit")
                self.assertIs(fm["mainAgent"], True)
                self.assertIs(fm["subagent"], True)
                self.assertEqual(set(fm["tools"]), LOCAL_TOOLS | (set() if aid == "project-navigator" else WEB_TOOLS))
                self.assertIn("@<agente>", data["body_suffix"])
                self.assertIn("no", data["body_suffix"].lower())
                if aid == "sdd":
                    description = fm["description"].lower()
                    for term in ("direct", "lite", "standard", "quick plan"):
                        self.assertIn(term, description)
                    for term in ("deep", "estricto"):
                        self.assertNotIn(term, description)

    def test_render_and_resources(self):
        self.assertIn("antigravity", self.manifest["platforms"], "Cannot characterize an undeclared platform")
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            render.render(target)
            output = target / "antigravity"
            self.assertEqual({p.stem for p in (output / "agents").glob("*.md")}, set(self.manifest["agents"]))
            self.assertEqual({p.name for p in (output / "skills").iterdir()}, set(self.manifest["skills"]))
            for sid in self.manifest["skills"]:
                canonical = ROOT / "canonical/skills" / sid
                generated = output / "skills" / sid
                for source in canonical.rglob("*"):
                    if not source.is_file():
                        continue
                    dest = generated / source.relative_to(canonical)
                    self.assertTrue(dest.is_file())
                    if source.name != "SKILL.md":
                        self.assertEqual(dest.read_bytes(), source.read_bytes())
                    else:
                        content = dest.read_text(encoding="utf-8")
                        self.assertNotIn("{{", content)
                        self.assertIn("name:", content)
                        self.assertIn("description:", content)
            for platform in self.manifest["platforms"]:
                if platform != "antigravity":
                    self.assertEqual(validate.digest_tree(target / platform),
                                     validate.digest_tree(ROOT / "generated" / platform), platform)


if __name__ == "__main__":
    unittest.main()
