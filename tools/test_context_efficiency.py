#!/usr/bin/env python3
"""Static contracts for prompt-load and interaction-efficiency changes."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class ContextEfficiencyTests(unittest.TestCase):
    def test_common_prompt_fragments_have_single_sources(self):
        identity = read("canonical/shared/mas-identity.md")
        context = read("canonical/shared/project-context.md")
        self.assertIn("MAS:", identity)
        self.assertIn("@<agente>", identity)
        self.assertIn("references/project-context.md", context)
        manifest = json.loads(read("canonical/manifest.json"))
        for agent in manifest["agents"]:
            body = read(f"canonical/agents/{agent}.md")
            self.assertIn("{{mas_identity}}", body, agent)
            if agent == "git-release-manager":
                self.assertNotIn("{{project_context}}", body)
            else:
                self.assertIn("{{project_context}}", body, agent)
        for skill in manifest["skills"]:
            self.assertIn("{{mas_identity}}", read(f"canonical/skills/{skill}/SKILL.md"), skill)

    def test_skills_have_specific_triggers(self):
        descriptions = {
            "architecture": read("canonical/skills/architecture/SKILL.md").split("---", 2)[1],
            "navigator": read("canonical/skills/project-navigator/SKILL.md").split("---", 2)[1],
            "data": read("canonical/skills/data-api/SKILL.md").split("---", 2)[1],
            "ui": read("canonical/skills/ui-design/SKILL.md").split("---", 2)[1],
        }
        for name, description in descriptions.items():
            with self.subTest(skill=name):
                self.assertNotIn("cualquier proyecto", description.casefold())
                self.assertNotIn("todo lo relacionado", description.casefold())
        self.assertIn("localiza archivos", descriptions["navigator"].casefold())
        self.assertIn("endpoints", descriptions["data"].casefold())
        self.assertIn("tokens", descriptions["ui"].casefold())

    def test_claude_git_agent_loads_skills_on_demand(self):
        adapter = json.loads(read("adapters/claude/agents/git-release-manager.json"))
        tools = adapter["frontmatter"]["tools"]
        self.assertIn("Skill", tools)
        self.assertNotIn("skills", adapter["frontmatter"])

    def test_atomic_remediation_uses_one_approval_structural_uses_steps(self):
        for skill in ("code-quality", "security"):
            text = " ".join(read(f"canonical/skills/{skill}/SKILL.md").casefold().split())
            with self.subTest(skill=skill):
                self.assertIn("atómica y bajo riesgo", text)
                self.assertIn("una sola aprobación", text)
                self.assertIn("estructural o de riesgo elevado", text)
                self.assertIn("pide aprobación antes de cada paso", text)
                self.assertNotIn("antes del primer micro-paso y de cada siguiente", text)

    def test_sdd_loads_only_needed_references_once(self):
        text = " ".join(read("canonical/skills/sdd-spec/SKILL.md").casefold().split())
        self.assertIn("carga únicamente la referencia necesaria", text)
        self.assertIn("reutilízalo durante la tarea", text)
        self.assertIn("no cargues todas las referencias por defecto", text)

    def test_retired_modes_and_git_basics_are_not_repeated(self):
        agent = read("canonical/agents/sdd.md").casefold()
        sdd = read("canonical/skills/sdd-spec/SKILL.md").casefold()
        git = read("canonical/skills/git-commit/SKILL.md")
        self.assertIn("opciones retiradas siguen la política compacta de `sdd-spec`", agent)
        self.assertIn("`deep` no está disponible", sdd)
        self.assertIn("ante una solicitud nueva", sdd)
        self.assertNotIn("## Tipos de Commit", git)
        self.assertNotIn("## Comandos de referencia", git)
        self.assertNotIn("## Solución de problemas", git)

    def test_navigator_uses_qualitative_limits_not_token_heuristics(self):
        for relative in (
            "canonical/skills/project-navigator/SKILL.md",
            "canonical/skills/project-navigator/references/layers.md",
            "canonical/skills/project-navigator/references/bootstrap.md",
        ):
            text = read(relative).casefold()
            with self.subTest(path=relative):
                self.assertNotIn("chars ≈ 1 token", text)
                self.assertNotIn("caracteres / 4", text)
                self.assertNotIn("tope blando: ~700", text)

    def test_independent_documentation_work_can_continue(self):
        skill = " ".join(read("canonical/skills/documentation-orchestrator/SKILL.md").casefold().split())
        workflow = " ".join(read("canonical/skills/documentation-orchestrator/references/workflows.md").casefold().split())
        self.assertIn("dominios independientes ya autorizados", skill)
        self.assertIn("continúa las ramas independientes ya autorizadas", workflow)
        self.assertIn("pregunta solo si cambian", workflow)

    def test_release_research_is_bounded(self):
        text = " ".join(read("canonical/skills/release-management/SKILL.md").casefold().split())
        self.assertIn("dos fuentes oficiales", text)
        self.assertIn("no abras investigación general", text)


if __name__ == "__main__":
    unittest.main()
