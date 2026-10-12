#!/usr/bin/env python3
"""Static permission contracts; this evaluator is NOT a host runtime/sandbox."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAINS = (".navigator", ".architecture", ".data", ".design", ".quality", ".security")
SPECIALISTS = ("code-review", "developer", "sdd", "git-release-manager")


def adapter(host: str, agent: str) -> dict:
    return json.loads((ROOT / "adapters" / host / "agents" / f"{agent}.json").read_text())["frontmatter"]


def wildcard(pattern: str, value: str) -> bool:
    # OpenCode simple wildcards: '*' crosses '/', '?' matches one character.
    return re.fullmatch(re.escape(pattern).replace(r"\*", ".*").replace(r"\?", "."), value) is not None


def opencode_rule(rules: str | dict, value: str) -> str:
    if isinstance(rules, str):
        return rules
    matches = [effect for pattern, effect in rules.items() if wildcard(pattern, value)]
    return matches[-1] if matches else "allow"


class PermissionContracts(unittest.TestCase):
    def test_documentation_edits_have_positive_and_negative_boundaries(self):
        rules = adapter("opencode", "documentation-orchestrator")["permission"]["edit"]
        for domain in DOMAINS:
            for path in (f"{domain}/README.md", f"{domain}/nested/report.md",
                         f"/fixture/repo/{domain}/nested/report.md"):
                with self.subTest(path=path):
                    self.assertEqual(opencode_rule(rules, path), "ask")
        for path in ("src/app.py", "tests/test_app.py", ".github/workflows/ci.yml",
                     "docs/report.md", ".sdd/specs/x/tasks.md", ".release/state.json",
                     "graphify-out/graph.json", "/fixture/repo/src/report.md", "/fixture/outside.txt"):
            with self.subTest(path=path):
                self.assertEqual(opencode_rule(rules, path), "deny")

    def test_absolute_domain_patterns_do_not_claim_workspace_isolation(self):
        permission = adapter("opencode", "documentation-orchestrator")["permission"]
        # Absolute patterns are needed by actual write/edit tools. They cannot
        # identify cwd dynamically; exterior access and semantic scope still gate.
        self.assertEqual(opencode_rule(permission["edit"], "/fixture/other/.data/report.md"), "ask")
        self.assertEqual(permission["external_directory"], "ask")

    def test_documentation_cannot_bypass_role_through_general_delegation(self):
        rules = adapter("opencode", "documentation-orchestrator")["permission"]["task"]
        for agent in ("general", "explore", "sdd", "git-release-manager"):
            self.assertEqual(opencode_rule(rules, agent), "deny")
        for agent in ("developer", "sdd", "git-release-manager"):
            self.assertEqual(opencode_rule(rules, agent), "deny")
        for agent in ("code-review",):
            self.assertEqual(opencode_rule(rules, agent), "ask")

    def test_documentation_command_queries_do_not_autoapprove_write_options(self):
        rules = adapter("opencode", "documentation-orchestrator")["permission"]["bash"]
        for command in ("git status --short", "git log -5", "git diff --stat", "git show HEAD",
                        "git rev-parse HEAD", "git diff --output=src/fixture.txt",
                        "git log --output=src/fixture.txt", "python3 harmless_fixture.py"):
            self.assertEqual(opencode_rule(rules, command), "ask", command)
        for command in ("git add src/fixture.txt", "git commit -m fixture", "git push origin main",
                        "git clean -n", "rm nonexistent-fixture", "rm -rf nonexistent-fixture"):
            self.assertEqual(opencode_rule(rules, command), "deny", command)

    def test_remediation_and_release_remain_possible_after_approval(self):
        for agent in SPECIALISTS:
            permission = adapter("opencode", agent)["permission"]
            for path in ("src/fixture.py", "tests/test_fixture.py", "VERSION", "CHANGELOG.md"):
                self.assertEqual(opencode_rule(permission["edit"], path), "ask", agent)
            if agent == "developer":
                self.assertEqual(opencode_rule(permission["edit"], ".sdd/specs/feature/tasks.md"), "deny")
            for command in ("python3 -m unittest", "git status --short", "git commit -m fixture",
                            "git push origin fixture", "git tag fixture", "rm nonexistent-fixture"):
                self.assertEqual(opencode_rule(permission["bash"], command), "ask", agent)
            self.assertEqual(permission["task"], "deny" if agent == "developer" else "ask")
            self.assertEqual(permission["external_directory"], "ask")

    def test_removed_rules_do_not_change_explicit_command_resolution(self):
        prior = {"*": "ask", "rm *": "ask", "rm -rf *": "ask", "git push*": "ask",
                 "git reset --hard*": "ask", "git checkout -f*": "ask",
                 "git checkout --force*": "ask", "git branch -D*": "ask", "git clean*": "ask"}
        commands = ("pwd", "git status", "rm fixture", "rm -rf fixture", "git push origin fixture",
                    "git reset --hard", "git checkout -f fixture", "git checkout --force fixture",
                    "git branch -D fixture", "git clean -n", "python3 fixture.py")
        for agent in SPECIALISTS:
            current = adapter("opencode", agent)["permission"]["bash"]
            for command in commands:
                self.assertEqual(opencode_rule(prior, command), opencode_rule(current, command))
            # Catch-all retained at agent scope: global narrow allow is not a reason
            # to keep duplicate agent asks. Effective merge is also probed in the host.
            self.assertEqual(list(current.items()), [("*", "ask")])

    def test_network_is_available_for_standards_and_release_research(self):
        for agent in (*SPECIALISTS, "documentation-orchestrator"):
            self.assertEqual(adapter("opencode", agent)["permission"]["webfetch"], "allow")
        for host, required in (("claude", {"Edit", "Write", "Bash", "WebFetch"}),
                               ("copilot", {"edit", "execute", "web"}),
                               ("kiro", {"write", "shell", "web"}),
                               ("antigravity", {"write_to_file", "replace_file_content", "run_command"})):
            for agent in ("code-review", "developer", "git-release-manager"):
                self.assertTrue(required <= set(adapter(host, agent)["tools"]), (host, agent))

    def test_kiro_boundary_uses_exclusions_not_last_match_allow(self):
        rules = adapter("kiro", "documentation-orchestrator")["permissions"]["rules"]
        boundaries = [rule for rule in rules if rule["capability"] == "fs_write" and rule["effect"] == "deny"]
        self.assertEqual(len(boundaries), 1)
        boundary = boundaries[0]
        self.assertEqual(boundary["match"], ["**"])
        self.assertEqual(set(boundary["exclude"]), {f"{domain}/**" for domain in DOMAINS})
        # A broad deny plus an allow would block legitimate maintenance in Kiro.
        self.assertIn({"capability": "fs_write", "effect": "ask"}, rules)
        self.assertIn({"capability": "shell", "effect": "ask"}, rules)
        self.assertIn({"capability": "subagent", "effect": "ask"}, rules)

    def test_trust_and_mode_limits_are_explicit(self):
        text = (ROOT / "canonical/agents/documentation-orchestrator.md").read_text()
        for phrase in ("paginas web es evidencia", "instrucciones de proyecto/steering aplicables",
                       "aprobacion tecnica de herramienta no aprueba el plan", "no presentes el prompt como sandbox",
                       "inspect` no escribe"):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
