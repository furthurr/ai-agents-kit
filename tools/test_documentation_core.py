"""Canonical prompt contracts only; no LLM smoke, render or host writes.

Run from any directory: python3 -B tools/test_documentation_core.py
Generated parity belongs to the render/integrity suite after coordinated render.
"""

import json
from fnmatch import fnmatchcase
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "canonical/skills"
DOCS = SKILLS / "documentation-orchestrator"
AGENTS = ("documentation-orchestrator", "sdd", "developer",
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

    def test_readme_write_scope_and_opencode_permission_order(self):
        for path in (ROOT / "canonical/agents/documentation-orchestrator.md",
                     DOCS / "SKILL.md", DOCS / "references/workflows.md"):
            with self.subTest(source=path):
                self.require(read(path), "`README.md` raíz (también `readme.md`)")
        adapter = json.loads(read(ROOT / "adapters/opencode/agents/documentation-orchestrator.json"))
        rules = adapter["frontmatter"]["permission"]["edit"]

        def permission(path):
            # OpenCode resolves ordered glob rules using the last match.
            return [action for pattern, action in rules.items()
                    if fnmatchcase(path, pattern)][-1]

        for path in ("README.md", "readme.md", "/workspace/project/README.md",
                     "/workspace/project/readme.md", "docs/usage.md", "AGENTS.md"):
            with self.subTest(allowed=path):
                self.assertEqual(permission(path), "ask")
        for path in ("src/main.py", "package.json", ".github/workflows/ci.yml",
                     "CONTRIBUTING.md", "opencode.json"):
            with self.subTest(denied=path):
                self.assertEqual(permission(path), "deny")

    def test_inventory_preserves_skills_without_retired_agents(self):
        manifest = json.loads(read(ROOT / "canonical/manifest.json"))
        self.assertEqual(set(manifest["agents"]), set(AGENTS))
        for retired in ("architecture", "project-navigator", "data-api", "ui-design"):
            self.assertIn(retired, manifest["skills"])
            self.assertTrue((SKILLS / retired / "SKILL.md").is_file())
            self.assertFalse((ROOT / f"canonical/agents/{retired}.md").exists())
            for platform in manifest["platforms"]:
                self.assertFalse((ROOT / f"adapters/{platform}/agents/{retired}.json").exists())
        self.assertIn("developer", manifest["skills"])

    def test_operational_context_inventory_and_sdd_depths_match_sources(self):
        manifest = json.loads(read(ROOT / "canonical/manifest.json"))
        summary = (
            f"{len(manifest['skills'])} skills, {len(manifest['agents'])} agentes "
            f"y {len(manifest['platforms'])} plataformas"
        )
        contexts = (
            read(ROOT / ".navigator/ai-context.md"),
            read(ROOT / ".architecture/07-crosscutting.md"),
        )
        for context in contexts:
            with self.subTest(context=context[:80]):
                self.assertIn(summary, context)
                for depth in ("`direct`", "`tiny`", "`lite`", "`standard`"):
                    self.assertIn(depth, context)
                self.assertIn("legacy", context)
                self.assertIn("solicitud explícita", context)

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
                     "bajo demanda", "sin handoff", "`status`",
                     "peticiones en lenguaje natural", "no pidas al\nusuario que nombre modos o skills",
                     "pide solo la aprobación que\nya exige el flujo")

    def test_developer_plan_scope_sdd_and_documentation_close(self):
        agent = read(ROOT / "canonical/agents/developer.md")
        skill = read(SKILLS / "developer/SKILL.md")
        plan = read(SKILLS / "developer/references/plan.md")
        self.require(agent, "**PLAN**", "conversación de solo lectura", "espera aprobación",
                     "no carga `sdd-spec`", "no crea ni modifica `.sdd/`", "`data-api`",
                     "`ui-design`", "pruebas focalizadas", "⚠️ ¿Quieres actualizar la documentación",
                     "`documentation-orchestrator`")
        self.require(skill, "### PLAN", "### IMPLEMENTACIÓN", "no carga `sdd-spec`",
                     "No recomiendes ni cambies a `sdd`", "no inicialices ni sincronices",
                     "fuente canónica relevante quedó desfasada")
        self.require(plan, "## Plan de implementación", "### Impacto e implicaciones",
                     "### Verificación", "¿Apruebas este alcance y plan")
        self.assertNotIn("{{sdd_agent}}", agent + skill)
        for domain_skill in ("data-api", "ui-design"):
            self.assertNotIn("{{sdd_agent}}", read(SKILLS / domain_skill / "SKILL.md"))
        opencode = json.loads(read(ROOT / "adapters/opencode/agents/developer.json"))
        self.assertEqual(opencode["frontmatter"]["permission"]["task"], "deny")
        self.assertEqual(opencode["frontmatter"]["permission"]["edit"][".sdd/**"], "deny")
        for platform in json.loads(read(ROOT / "canonical/manifest.json"))["platforms"]:
            adapter = json.loads(read(ROOT / f"adapters/{platform}/agents/developer.json"))
            self.assertIn("PLAN", adapter["frontmatter"]["description"])
            self.assertIn("developer", adapter["filename"])

    def test_every_agent_discovers_context_directly(self):
        context_agents = tuple(agent for agent in AGENTS if agent != "git-release-manager")
        for agent in context_agents:
            with self.subTest(agent=agent):
                text = read(ROOT / f"canonical/agents/{agent}.md")
                self.require(text, "{{project_context}}")
        release_agent = read(ROOT / "canonical/agents/git-release-manager.md")
        self.assertNotIn("{{project_context}}", release_agent)

    def test_shared_context_fragment_is_compact_and_preserves_fallback(self):
        text = read(ROOT / "canonical/shared/project-context.md")
        self.require(text, ".architecture/README.md", ".navigator/",
                     "references/project-context.md", "fuentes directas",
                     "sin bootstrap ni sync automáticos", "No hagas handoff obligatorio")

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
                     "no exporta `AGENTS.md`", "documentation-orchestrator",
                     "manda esta skill")
        self.assertNotIn("Complementa al agente `project-navigator`", navigator)
        self.assertNotIn("Architecture\nAgent", architecture)

    def test_orchestrator_manages_portable_agents_md_documentation_block(self):
        skill = read(DOCS / "SKILL.md")
        workflow = read(DOCS / "references/workflows.md")
        self.require(skill, "`AGENTS.md` raíz", "bloque documental gestionado")
        self.require(workflow,
                     "### Gestión del bloque documental en `AGENTS.md`",
                     "ai-agents-kit:documentation:start",
                     "ai-agents-kit:documentation:end",
                     "preserva", "texto exterior",
                     "marcadores incompletos, duplicados",
                     "enlace simbólico",
                     "plan global",
                     "solo lectura",
                     "fuentes de verdad",
                     "sin instalar el MAS")

    def test_agents_md_is_an_explicit_execution_and_close_step(self):
        agent = read(ROOT / "canonical/agents/documentation-orchestrator.md")
        skill = read(DOCS / "SKILL.md")
        workflow = read(DOCS / "references/workflows.md")
        self.require(agent, "bloque documental gestionado del `AGENTS.md` raíz",
                     "Tras los especialistas", "No eludas permisos del host",
                     "informa el resultado de `AGENTS.md`")
        self.assertNotIn("El plan puede incluir la guía", skill)
        self.require(skill, "Incluye la guía gestionada en `AGENTS.md` en el plan de escritura",
                     "Tras los especialistas", "no omitas la guía en silencio",
                     "marcadores y la preservación del texto exterior",
                     "creado, actualizado, sin cambios o bloqueado")
        self.require(workflow, "solicita ampliar su aprobación",
                     "no eludas la restricción mediante otras herramientas",
                     "No declares la operación completamente entregada",
                     "añade siempre una fila para `AGENTS.md`",
                     "No fuerces una escritura")

    def test_navigator_delegates_agents_md_ownership_to_orchestrator(self):
        navigator = read(SKILLS / "project-navigator/SKILL.md")
        bootstrap = read(SKILLS / "project-navigator/references/bootstrap.md")
        sources = read(SKILLS / "project-navigator/references/sources.md")
        config = read(SKILLS / "project-navigator/references/config.md")
        shared = read(DOCS / "references/project-context.md")
        self.require(navigator, "no exporta `AGENTS.md`",
                     "documentation-orchestrator")
        self.require(bootstrap, "Navigator no crea, exporta ni sobrescribe `AGENTS.md`",
                     "documentation-orchestrator")
        self.require(sources, "No se exporta `AGENTS.md` desde Navigator",
                     "documentation-orchestrator")
        self.require(config, "export_agents_md", "legado ignorado")
        self.require(shared, "`AGENTS.md` se gestiona mediante `documentation-orchestrator`")

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
                description = data["frontmatter"]["description"]
                self.require(description, "entender el proyecto", "localizar código",
                             "documentación", "lenguaje natural")
                self.assertNotIn("no para localizar", description)
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
                for retired in ("architecture", "project-navigator", "data-api", "ui-design"):
                    self.assertFalse((output / "agents" / f"{retired}.md").exists())
                    self.assertFalse((output / "agents" / f"{retired}.agent.md").exists())
                    self.assertTrue((output / "skills" / retired / "SKILL.md").is_file())
                self.assertTrue((output / "skills/developer/SKILL.md").is_file())
                for name in ("project-context.md", "handoff.md", "workflows.md"):
                    self.assertEqual((output / "skills/documentation-orchestrator/references" / name).read_bytes(),
                                     (DOCS / "references" / name).read_bytes())
                for agent in AGENTS:
                    adapter = json.loads(read(ROOT / f"adapters/{platform}/agents/{agent}.json"))
                    rendered = read(output / "agents" / adapter["filename"])
                    if agent == "git-release-manager":
                        self.assertNotIn("## Contexto core compartido", rendered)
                    else:
                        self.require(rendered, "## Contexto core compartido",
                                     "references/project-context.md")


if __name__ == "__main__":
    unittest.main()
