"""Canonical prompt contracts only; no LLM smoke, render or host writes.

Run from any directory: python3 -B tools/test_documentation_core.py
Generated parity belongs to the render/integrity suite after coordinated render.
"""

import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "canonical/skills"
DOCS = SKILLS / "documentation-orchestrator"
AGENTS = ("documentation-orchestrator", "sdd", "data-api", "ui-design",
          "code-review", "git-release-manager")


def read(path):
    return path.read_text(encoding="utf-8")


def missing(text, clauses):
    """Report required explicit clauses, without claiming semantic obedience."""
    normalized = " ".join(text.split())
    return [clause for clause in clauses if " ".join(clause.split()) not in normalized]


class DocumentationCoreContract(unittest.TestCase):
    def require(self, text, *clauses):
        self.assertEqual(missing(text, clauses), [])

    def test_inventory_preserves_skills_without_retired_agents(self):
        manifest = json.loads(read(ROOT / "canonical/manifest.json"))
        self.assertEqual(set(manifest["agents"]), set(AGENTS))
        for retired in ("architecture", "project-navigator"):
            self.assertIn(retired, manifest["skills"])
            self.assertTrue((SKILLS / retired / "SKILL.md").is_file())
            self.assertFalse((ROOT / f"canonical/agents/{retired}.md").exists())
            for platform in manifest["platforms"]:
                self.assertFalse((ROOT / f"adapters/{platform}/agents/{retired}.json").exists())

    def test_inspect_distinct_from_default_status(self):
        skill = read(DOCS / "SKILL.md")
        workflow = read(DOCS / "references/workflows.md")
        self.require(skill, "| `inspect` |", "sin modo → `status`",
                     "bajo demanda", "core se ejecuta localmente")
        self.require(workflow, "### `inspect`", "cero persistencia",
                     "sin handoff", "no acredita sincronizacion",
                     "peticion mixta", "fuentes", "confianza")

    def test_documentation_agent_local_core(self):
        text = read(ROOT / "canonical/agents/documentation-orchestrator.md")
        self.require(text, "`inspect`", "core se ejecuta localmente",
                     "bajo demanda", "sin handoff", "`status`")

    def test_every_agent_discovers_context_directly(self):
        for agent in AGENTS:
            with self.subTest(agent=agent):
                text = read(ROOT / f"canonical/agents/{agent}.md")
                self.require(text, "## Contexto core compartido", ".architecture/README.md",
                             ".navigator/", "references/project-context.md",
                             "sin handoff obligatorio", "fuentes directas",
                             "sin bootstrap ni sync automaticos")

    def test_shared_reference_portable_and_selective(self):
        path = DOCS / "references/project-context.md"
        self.assertTrue(path.is_file(), "shared reference missing")
        text = read(path)
        self.require(text, "steering", ".architecture/README.md", "Contexto para IA",
                     "config.yaml", "project.root", "ai-context.md", "module-map.json",
                     "source_commit", "HEAD", "working tree", "generated_at",
                     "bajo demanda", "fuentes directas", "no bloquea",
                     "no crea ni actualiza", "formatos", "contratos canónicos")
        self.assertNotRegex(text, r"\{\{|/Users/|~/|\$\{|\{env:")

    def test_fallback_scenarios_are_explicit_contracts(self):
        path = DOCS / "references/project-context.md"
        self.assertTrue(path.is_file(), "shared reference missing")
        text = read(path)
        for state in ("Ausente", "Desfasado", "Ambiguo", "Ilegible", "No verificable", "Vigente"):
            with self.subTest(state=state):
                self.assertRegex(text, rf"(?m)^\| `{state}` \|.+\|$")

    def test_relative_skill_links_resolve(self):
        consumers = (
            DOCS / "references/project-context.md",
            SKILLS / "architecture/SKILL.md",
            SKILLS / "project-navigator/SKILL.md",
            SKILLS / "sdd-spec/references/navigator-context.md",
        )
        for path in consumers:
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertTrue(path.is_file())
                text = read(path)
                links = re.findall(r"\]\(([^)]+)\)", text)
                self.assertTrue(links)
                for link in links:
                    if not re.match(r"https?://", link):
                        self.assertTrue((path.parent / link.split('#')[0]).is_file(), link)
                if path.name != "project-context.md":
                    self.assertTrue(any(link.endswith("project-context.md") for link in links))

    def test_read_only_specialists_keep_write_gates(self):
        architecture = read(SKILLS / "architecture/SKILL.md")
        navigator = read(SKILLS / "project-navigator/SKILL.md")
        self.require(architecture, "## Consultas de solo lectura", "no activa",
                     "espera confirmación", "NO modifica código de negocio")
        self.require(navigator, "sin bloquear la consulta", "solo on_request",
                     "Export", "con confirmación", "manda esta skill")
        self.assertNotIn("Complementa al agente `project-navigator`", navigator)
        self.assertNotIn("Architecture\nAgent", architecture)

    def test_sdd_specific_freshness_preserved(self):
        text = read(SKILLS / "sdd-spec/references/navigator-context.md")
        self.require(text, "source_commit", "working tree", "generated_at",
                     "no bloquea SDD", "No se invoca ni se cambia automáticamente",
                     "documentation-orchestrator", "project-context.md")

    def test_adapter_descriptions_discover_queries_without_preload(self):
        paths = sorted((ROOT / "adapters").glob("*/agents/documentation-orchestrator.json"))
        self.assertEqual(len(paths), 6)
        for path in paths:
            with self.subTest(platform=path.parent.parent.name):
                data = json.loads(read(path))
                self.require(data["frontmatter"]["description"], "arquitectura", "navegación")
                self.assertNotIn("architecture", data["frontmatter"].get("skills", []))
                self.assertNotIn("project-navigator", data["frontmatter"].get("skills", []))

    def test_clause_checker_rejects_missing_instruction_fixture(self):
        # Mutation fixture exercises the checker, not agent behavior.
        fixture = "solo lectura; sin handoff; cero persistencia"
        clauses = ("solo lectura", "sin handoff", "cero persistencia")
        self.assertEqual(missing(fixture, clauses), [])
        for clause in clauses:
            with self.subTest(removed=clause):
                self.assertEqual(missing(fixture.replace(clause, ""), clauses), [clause])

    def test_generated_core_inventory_and_reference_parity(self):
        manifest = json.loads(read(ROOT / "canonical/manifest.json"))
        for platform in manifest["platforms"]:
            with self.subTest(platform=platform):
                output = ROOT / "generated" / platform
                self.assertEqual(len(list((output / "agents").glob("*.md"))), len(AGENTS))
                for retired in ("architecture", "project-navigator"):
                    self.assertFalse((output / "agents" / f"{retired}.md").exists())
                    self.assertFalse((output / "agents" / f"{retired}.agent.md").exists())
                    self.assertTrue((output / "skills" / retired / "SKILL.md").is_file())
                for name in ("project-context.md", "handoff.md", "workflows.md"):
                    self.assertEqual((output / "skills/documentation-orchestrator/references" / name).read_bytes(),
                                     (DOCS / "references" / name).read_bytes())
                for agent in AGENTS:
                    adapter = json.loads(read(ROOT / f"adapters/{platform}/agents/{agent}.json"))
                    self.require(read(output / "agents" / adapter["filename"]),
                                 "## Contexto core compartido", "references/project-context.md")


if __name__ == "__main__":
    unittest.main()
