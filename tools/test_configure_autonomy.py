#!/usr/bin/env python3
"""Isolated profile tests for tools/configure_autonomy.py; never touch real homes."""
from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import configure_autonomy as autonomy  # noqa: E402


class ConfigureAutonomyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="ai-agents-autonomy-test-")
        self.home = Path(self.temp.name) / "home"
        self.home.mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_json(self, path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def apply(self, plan: autonomy.Plan) -> Path | None:
        return autonomy.apply_plan(plan, home=self.home)

    def test_opencode_converts_asks_in_global_and_agent_configs_but_preserves_deny(self) -> None:
        config_dir = self.home / ".config"
        opencode = config_dir / "opencode"
        settings = opencode / "opencode.json"
        self.write_json(settings, {
            "$schema": "https://opencode.ai/config.json",
            "permission": {
                "read": {"*": "allow", "*.env": "deny"},
                "edit": {"*": "ask", ".sdd/**": "deny"},
                "bash": {"*": "ask", "git push *": "deny"},
                "external_directory": {"*": "ask"},
            },
            "agent": {
                "developer": {"permission": {"bash": {"*": "ask"}, "edit": {".sdd/**": "deny"}}}
            },
            "instructions": ["OPENCODE.md"],
        })
        agent = opencode / "agent" / "developer.md"
        agent.parent.mkdir(parents=True)
        agent.write_text(
            "---\npermission:\n  edit:\n    '*': ask\n    '.sdd/**': deny\n  bash:\n    '*': ask\n---\nThe literal ask in body remains.\n",
            encoding="utf-8",
        )
        with patch.dict(os.environ, {"XDG_CONFIG_HOME": str(config_dir), "OPENCODE_CONFIG": ""}):
            plan = autonomy.build_opencode_plan(self.home, None, None)
        backup = self.apply(plan)
        self.assertIsNotNone(backup)
        result = json.loads(settings.read_text(encoding="utf-8"))
        self.assertEqual(result["permission"]["bash"]["*"], "allow")
        self.assertEqual(result["permission"]["bash"]["git push *"], "deny")
        self.assertEqual(result["permission"]["read"]["*.env"], "deny")
        self.assertEqual(result["permission"]["read"]["*.pem"], "deny")
        self.assertEqual(result["permission"]["read"]["*.env.example"], "allow")
        self.assertEqual(result["permission"]["edit"]["*.key"], "deny")
        self.assertEqual(result["permission"]["edit"][".sdd/**"], "deny")
        self.assertEqual(result["permission"]["external_directory"]["*"], "allow")
        self.assertIn(str(opencode / "ai-agents-kit-autonomy.md"), result["instructions"])
        self.assertEqual(result["agent"]["developer"]["permission"]["bash"]["*"], "allow")
        agent_text = agent.read_text(encoding="utf-8")
        self.assertIn(".sdd/**': deny", agent_text)
        self.assertIn("The literal ask in body remains.", agent_text)
        self.assertNotIn("'*': ask", agent_text)
        self.assertTrue((opencode / "ai-agents-kit-autonomy.md").is_file())

    def test_opencode_jsonc_is_refused_without_mutation(self) -> None:
        config_dir = self.home / ".config"
        path = config_dir / "opencode" / "opencode.jsonc"
        path.parent.mkdir(parents=True)
        path.write_text('{\n  // keep this comment\n  "permission": {"bash": {"*": "ask"}},\n}\n', encoding="utf-8")
        with patch.dict(os.environ, {"XDG_CONFIG_HOME": str(config_dir), "OPENCODE_CONFIG": str(path)}):
            with self.assertRaises(autonomy.ConfigError):
                autonomy.build_opencode_plan(self.home, None, None)
        self.assertIn("keep this comment", path.read_text(encoding="utf-8"))

    def test_opencode_v2_wildcard_preserves_loop_guard_and_command_deny(self) -> None:
        config_dir = self.home / ".config"
        settings = config_dir / "opencode" / "opencode.json"
        self.write_json(settings, {
            "permission": {
                "*": "ask",
                "doom_loop": "ask",
                "shell": {"git push *": "deny"},
            }
        })
        with patch.dict(os.environ, {"XDG_CONFIG_HOME": str(config_dir), "OPENCODE_CONFIG": ""}):
            plan = autonomy.build_opencode_plan(self.home, None, "shell")
        self.apply(plan)
        result = json.loads(settings.read_text(encoding="utf-8"))
        self.assertEqual(result["permission"]["*"], "allow")
        self.assertEqual(result["permission"]["doom_loop"], "ask")
        self.assertEqual(result["permission"]["shell"]["git push *"], "deny")

    def test_claude_moves_local_asks_to_allows_and_preserves_denies(self) -> None:
        settings = self.home / ".claude" / "settings.json"
        self.write_json(settings, {
            "permissions": {
                "allow": ["Read"],
                "ask": ["Bash(npm test *)"],
                "deny": ["Read(./.env)", "Bash(git push *)"],
                "defaultMode": "default",
            }
        })
        plan = autonomy.build_claude_plan(self.home)
        self.apply(plan)
        result = json.loads(settings.read_text(encoding="utf-8"))
        permission = result["permissions"]
        self.assertEqual(permission["defaultMode"], "auto")
        self.assertIn("Bash(npm test *)", permission["allow"])
        self.assertIn("Bash", permission["allow"])
        self.assertEqual(permission["ask"], [])
        self.assertIn("Read(./.env)", permission["deny"])
        self.assertIn("Bash(git push *)", permission["deny"])
        self.assertIn("Read(.env)", permission["deny"])
        self.assertIn("Read(!.env.example)", permission["deny"])
        self.assertTrue((self.home / ".claude" / "CLAUDE.md").is_file())

    def test_copilot_cli_is_partial_and_only_saves_supplied_commands(self) -> None:
        project = self.home / "repo"
        project.mkdir()
        (project / ".git").mkdir()
        project_root = self.home / ".copilot"
        permissions = project_root / "permissions-config.json"
        project_key = str(project.resolve())
        self.write_json(permissions, {"locations": {project_key: {
            "tool_approvals": [{"kind": "commands", "commandIdentifiers": ["git status"]}]
        }}})
        self.write_json(project_root / "settings.json", {"askUser": False, "theme": "dark"})
        with patch.dict(os.environ, {"COPILOT_HOME": str(project_root)}):
            plan = autonomy.build_copilot_plan(self.home, project, ["python3 -m unittest:*", "git status"])
        self.assertEqual(plan.completeness, "parcial: shell persistente limitado a --command")
        permission_change = next(item for item in plan.changes if item.path == permissions)
        self.assertIn(b'"kind": "write"', permission_change.content)
        self.apply(plan)
        self.assertEqual(permissions.read_bytes(), permission_change.content)
        result = json.loads(permissions.read_text(encoding="utf-8"))
        approvals = result["locations"][project_key]["tool_approvals"]
        self.assertIn({"kind": "write"}, approvals)
        self.assertIn({"kind": "commands", "commandIdentifiers": ["git status"]}, approvals)
        self.assertIn({"kind": "commands", "commandIdentifiers": ["python3 -m unittest:*", "git status"]}, approvals)
        settings_result = json.loads((project_root / "settings.json").read_text(encoding="utf-8"))
        self.assertTrue(settings_result["askUser"])
        self.assertEqual(settings_result["theme"], "dark")
        self.assertTrue(json.loads((project_root / "settings.json").read_text(encoding="utf-8"))["askUser"])
        instructions = project_root / "instructions" / "ai-agents-kit-autonomy.instructions.md"
        self.assertTrue(instructions.is_file())

    def test_copilot_rejects_undocumented_wildcards(self) -> None:
        project = self.home / "repo"
        project.mkdir()
        with self.assertRaises(autonomy.ConfigError):
            autonomy.build_copilot_plan(self.home, project, ["*"])

    def test_copilot_worktree_permission_scope_resolves_to_main_repository(self) -> None:
        main = self.home / "repo"
        worktree = self.home / "repo-worktree"
        main_git = main / ".git"
        git_dir = main_git / "worktrees" / "feature"
        git_dir.mkdir(parents=True)
        worktree.mkdir()
        (git_dir / "commondir").write_text("../..\n", encoding="utf-8")
        (worktree / ".git").write_text(f"gitdir: {git_dir}\n", encoding="utf-8")
        self.assertEqual(autonomy._git_root(worktree), main.resolve())

    def test_kiro_changes_ask_rules_preserves_denies_and_network_is_opt_in(self) -> None:
        kiro_home = self.home / ".kiro"
        permission_path = kiro_home / "settings" / "permissions.yaml"
        permission_path.parent.mkdir(parents=True)
        permission_path.write_text(
            "rules:\n"
            "  - capability: shell\n"
            "    match: [\"git *\"]\n"
            "    effect: ask\n"
            "  - capability: fs_read\n"
            "    match: [\"**/.env\"]\n"
            "    effect: deny\n",
            encoding="utf-8",
        )
        agent = kiro_home / "agents" / "developer.md"
        agent.parent.mkdir()
        agent.write_text(
            "---\npermissions:\n  rules:\n    - capability: shell\n      effect: ask\n    - capability: shell\n      match: [\"rm *\"]\n      effect: deny\n---\nBody.\n",
            encoding="utf-8",
        )
        with patch.dict(os.environ, {"KIRO_HOME": str(kiro_home)}):
            plan = autonomy.build_kiro_plan(self.home, allow_network=False, surface="cli")
        self.apply(plan)
        config_text = permission_path.read_text(encoding="utf-8")
        self.assertIn("effect: allow", config_text)
        self.assertIn('match: ["**/.env"]\n    effect: deny', config_text)
        self.assertIn("capability: all", config_text)
        self.assertIn("capability: fs_read", config_text)
        self.assertIn('"**/.env.example"', config_text)
        self.assertNotIn("capability: sandbox_network", config_text)
        agent_text = agent.read_text(encoding="utf-8")
        self.assertIn('match: ["rm *"]\n      effect: deny', agent_text)
        self.assertIn(autonomy.START_MARKER, agent_text)
        self.assertIn("sandbox_network queda sin regla allow", " ".join(plan.notes))

    def test_kiro_network_flag_adds_explicit_sandbox_network_rule(self) -> None:
        with patch.dict(os.environ, {"KIRO_HOME": str(self.home / ".kiro")}):
            plan = autonomy.build_kiro_plan(self.home, allow_network=True, surface="cli")
        change = next(item for item in plan.changes if item.path.name == "permissions.yaml")
        self.assertIn('match: ["*"]', change.content.decode())
        self.assertIn("capability: sandbox_network", change.content.decode())

    def test_antigravity_converts_asks_keeps_denies_and_does_not_unsandbox_by_default(self) -> None:
        settings = self.home / ".gemini" / "antigravity-cli" / "settings.json"
        self.write_json(settings, {
            "permissions": {
                "allow": ["read_file(src/)"],
                "ask": ["command(npm test)", "read_url(example.com)"],
                "deny": ["command(rm -rf)", "read_file(**/.env)"],
            },
            "toolPermission": "request-review",
            "artifactReviewPolicy": "asks-for-review",
        })
        plan = autonomy.build_antigravity_plan(self.home, allow_network=False)
        self.apply(plan)
        result = json.loads(settings.read_text(encoding="utf-8"))
        permissions = result["permissions"]
        self.assertIn("command(*)", permissions["allow"])
        self.assertIn("command(npm test)", permissions["allow"])
        self.assertEqual(permissions["ask"], [])
        self.assertIn("command(rm -rf)", permissions["deny"])
        self.assertIn("read_file(**/.env)", permissions["deny"])
        self.assertIn(f"read_file({(self.home / '.ssh').resolve()})", permissions["deny"])
        self.assertEqual(result["toolPermission"], "always-proceed")
        self.assertEqual(result["artifactReviewPolicy"], "always-proceed")
        self.assertNotIn("unsandboxed(*)", permissions["allow"])
        self.assertNotIn("read_url(*)", permissions["allow"])
        self.assertTrue((self.home / ".gemini" / "AGENTS.md").is_file())

    def test_antigravity_network_flag_allows_web_but_does_not_add_unsandboxed_wildcard(self) -> None:
        plan = autonomy.build_antigravity_plan(self.home, allow_network=True)
        settings_change = next(item for item in plan.changes if item.path.name == "settings.json")
        settings = json.loads(settings_change.content)
        self.assertIn("read_url(*)", settings["permissions"]["allow"])
        self.assertIn("execute_url(*)", settings["permissions"]["allow"])
        self.assertNotIn("unsandboxed(*)", settings["permissions"]["allow"])

    def test_antigravity_app_script_reports_permission_preset_as_manual(self) -> None:
        plan = autonomy.build_plan("antigravity-app", home=self.home)
        self.assertEqual(len(plan.changes), 1)
        self.assertEqual(plan.changes[0].path, (self.home / ".gemini" / "AGENTS.md").resolve())
        self.assertIn("preset Turbo", " ".join(plan.notes))
        self.assertTrue(plan.completeness.startswith("parcial"))

    def test_pi_only_installs_managed_instructions_and_keeps_project_trust(self) -> None:
        agent = self.home / ".pi" / "agent"
        system = agent / "APPEND_SYSTEM.md"
        system.parent.mkdir(parents=True)
        system.write_text("Personal instruction.\n", encoding="utf-8")
        with patch.dict(os.environ, {"PI_CODING_AGENT_DIR": str(agent)}):
            plan = autonomy.build_pi_plan(self.home)
        self.apply(plan)
        self.assertIn("Personal instruction.", system.read_text(encoding="utf-8"))
        self.assertIn(autonomy.START_MARKER, system.read_text(encoding="utf-8"))
        self.assertIn("defaultProjectTrust", " ".join(plan.notes))
        self.assertEqual(plan.completeness, "solo conductual; la seguridad depende de permisos del proceso, extensiones y sandbox externo")

    def test_dry_run_is_read_only_apply_is_reversible_and_restore_refuses_later_edits(self) -> None:
        target = self.home / ".config" / "fixture.json"
        target.parent.mkdir(parents=True)
        target.write_text('{"before": true}\n', encoding="utf-8")
        original = target.read_bytes()
        plan = autonomy.Plan([autonomy.Change(target, b'{"after": true}\n', "fixture")], [])
        # Planning alone does not write; apply_plan is called only below.
        self.assertEqual(target.read_bytes(), original)
        backup = autonomy.apply_plan(plan, home=self.home)
        self.assertIsNotNone(backup)
        self.assertEqual(json.loads(target.read_text())["after"], True)
        autonomy.restore_backup(backup, home=self.home)
        self.assertEqual(target.read_bytes(), original)

        backup = autonomy.apply_plan(plan, home=self.home)
        target.write_text('{"later": true}\n', encoding="utf-8")
        with self.assertRaises(autonomy.ConfigError):
            autonomy.restore_backup(backup, home=self.home)
        self.assertEqual(json.loads(target.read_text())["later"], True)

    def test_apply_is_idempotent(self) -> None:
        target = self.home / "config.md"
        plan = autonomy.Plan([autonomy.Change(target, (autonomy.AUTONOMY_BLOCK + "\n").encode(), "fixture")], [])
        first = autonomy.apply_plan(plan, home=self.home)
        self.assertIsNotNone(first)
        self.assertIsNone(autonomy.apply_plan(plan, home=self.home))

    def test_managed_instruction_update_preserves_user_text_and_trailing_spacing(self) -> None:
        original = "Personal rule.\n\n"
        updated = autonomy._managed_block(original)
        self.assertTrue(updated.startswith(original))
        self.assertEqual(autonomy._managed_block(updated), updated)

    def test_cli_defaults_to_dry_run_and_does_not_create_user_config(self) -> None:
        agent_dir = self.home / ".pi" / "agent"
        stdout = io.StringIO()
        with patch.dict(os.environ, {
            "HOME": str(self.home),
            "USERPROFILE": str(self.home),
            "PI_CODING_AGENT_DIR": str(agent_dir),
        }, clear=False), redirect_stdout(stdout):
            status = autonomy.main(["--host", "pi"])
        self.assertEqual(status, 0)
        self.assertIn("DRY-RUN", stdout.getvalue())
        self.assertFalse((agent_dir / "APPEND_SYSTEM.md").exists())

    def test_restore_rejects_backup_outside_owned_backup_root(self) -> None:
        outside = self.home / "foreign-backup"
        outside.mkdir()
        (outside / "manifest.json").write_text('{"format":1,"files":[]}\n', encoding="utf-8")
        with self.assertRaises(autonomy.ConfigError):
            autonomy.restore_backup(outside, home=self.home)

    def test_symlink_destination_is_rejected(self) -> None:
        real = self.home / "real.txt"
        real.write_text("untouched", encoding="utf-8")
        link = self.home / "link.txt"
        link.symlink_to(real)
        plan = autonomy.Plan([autonomy.Change(link, b"replacement", "fixture")], [])
        with self.assertRaises(autonomy.ConfigError):
            autonomy.apply_plan(plan, home=self.home)
        self.assertEqual(real.read_text(encoding="utf-8"), "untouched")


if __name__ == "__main__":
    unittest.main(verbosity=2)
