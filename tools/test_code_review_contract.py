#!/usr/bin/env python3
"""Static prompt/distribution contracts, not runtime proof of LLM behavior."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


class CodeReviewContractTest(unittest.TestCase):
    maxDiff = 1000
    def text(self, relative: str) -> str:
        path = ROOT / relative
        self.assertTrue(path.is_file(), f"Falta artefacto: {relative}")
        return path.read_text(encoding="utf-8")

    def manifest(self) -> dict:
        return json.loads(self.text("canonical/manifest.json"))

    def test_single_agent_and_separate_skills(self) -> None:
        manifest = self.manifest()
        # El manifest y las fuentes canónicas deben declarar el mismo inventario,
        # sin congelar un total que cambia al retirar agentes consolidados.
        self.assertEqual(
            set(manifest["agents"]),
            {path.stem for path in (ROOT / "canonical" / "agents").glob("*.md")},
        )
        self.assertEqual(len(manifest["skills"]), 10)
        self.assertIn("code-review", manifest["agents"])
        for old in ("code-quality", "security"):
            self.assertNotIn(old, manifest["agents"])
            self.assertIn(old, manifest["skills"])
            self.assertFalse((ROOT / "canonical" / "agents" / f"{old}.md").exists())

    def test_routing_and_evidence_contract(self) -> None:
        agent = self.text("canonical/agents/code-review.md")
        for rule in ("solo calidad", "solo seguridad", "revisión completa", "QLT", "SEC",
                     "Sonar", "OWASP", "severidad original", "misma causa",
                     "no amplía", "target: code-review", "Handoff Result"):
            self.assertTrue(rule in agent, f"Falta regla del agente: {rule}")
        self.assertIn("carga únicamente", agent)
        self.assertIn("sin escrituras", agent)
        self.assertIn("antes del primer", agent)
        self.assertIn("{{sdd_agent}}", agent)

    def test_skill_documentation_and_read_only_contract(self) -> None:
        for skill, folder, prefix in (("code-quality", ".quality/", "QLT"),
                                      ("security", ".security/", "SEC")):
            text = self.text(f"canonical/skills/{skill}/SKILL.md")
            for rule in ("Code Review", folder, prefix, "todas las severidades",
                         "ocurrencias de la", "sin escrituras", "cachés", "marcas",
                         "antes del primer", "sesión"):
                with self.subTest(skill=skill, rule=rule):
                    self.assertTrue(rule in text, f"Falta regla de {skill}: {rule}")
            self.assertNotIn("Confirma el **alcance** (todo, solo", text)
            self.assertNotIn("deriva al Security Agent", text)

    def test_remediation_authorization_is_not_model_confirmation(self) -> None:
        for skill in ("code-quality", "security"):
            text = self.text(f"canonical/skills/{skill}/SKILL.md")
            compact = " ".join(text.split()).lower()
            with self.subTest(skill=skill):
                self.assertRegex(compact, r"(?:no|ni) transfieras[^.]*autorizaci[oó]n[^.]*remediaci[oó]n")
                self.assertIn("solicita aprobación antes del primer micro-paso y de cada siguiente", compact)
                self.assertIn("un solo micro-paso", compact)
                self.assertRegex(compact, r"detente y espera ok")
                self.assertIn("nunca encadenes varios cambios sin confirmación", compact)

    def test_orchestrator_domain_mapping(self) -> None:
        text = self.text("canonical/skills/documentation-orchestrator/SKILL.md")
        for rule in ("code-review", "misma accion", "mismo proyecto", "scope",
                     "no pide un filtro", "no entres en remediacion"):
            self.assertIn(rule, text)
        contract = self.text("canonical/skills/documentation-orchestrator/references/handoff.md")
        self.assertIn("[.quality/, .security/]", contract)
        self.assertIn("cada dominio", contract)
        self.assertIn("gate_state", contract)

    def test_adapter_identity_and_permissions(self) -> None:
        for platform in self.manifest()["platforms"]:
            adapter = json.loads(self.text(f"adapters/{platform}/agents/code-review.json"))
            self.assertIn("code-review", adapter["filename"])
            front = adapter["frontmatter"]
            for old in ("security", "code-quality"):
                self.assertFalse((ROOT / "adapters" / platform / "agents" / f"{old}.json").exists())
            if platform == "opencode":
                self.assertEqual(front["permission"]["edit"], "ask")
                self.assertEqual(front["permission"]["bash"]["*"], "ask")
            elif platform == "kiro":
                self.assertTrue(all(rule["effect"] == "deny" for rule in front["permissions"]["rules"]))
            elif platform == "claude":
                self.assertFalse(front["user-invocable"])
                self.assertIn("Skill", front["tools"])
                self.assertNotIn("skills", front, "Evitar precargar ambos dominios")
            elif platform == "pi":
                self.assertIn("$ARGUMENTS", adapter["body_suffix"])

    def test_generated_catalog(self) -> None:
        canonical = self.text("canonical/agents/code-review.md")
        manifest = self.manifest()
        for platform in self.manifest()["platforms"]:
            adapter = json.loads(self.text(f"adapters/{platform}/agents/code-review.json"))
            generated = ROOT / "generated" / platform
            self.assertEqual(
                len(list((generated / "agents").glob("*.md"))),
                len(manifest["agents"]),
            )
            body = self.text(f"generated/{platform}/agents/{adapter['filename']}")
            self.assertIn("# Code Review Agent", body)
            self.assertIn("sin escrituras", body)
            self.assertIn("severidad original", body)
            self.assertNotIn("{{", body)
            self.assertIn("## Recepción de handoff", canonical)
            for skill in ("code-quality", "security"):
                self.assertTrue((generated / "skills" / skill / "SKILL.md").is_file())
                self.assertFalse(any((generated / "agents").glob(f"{skill}*.md")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
