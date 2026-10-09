#!/usr/bin/env python3
"""Negative contract: model guidance is silent outside SDD."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = json.loads((ROOT / "canonical/manifest.json").read_text(encoding="utf-8"))

MODEL_GUIDANCE = re.compile(
    r"model-selection\.md"
    r"|nivel\s+de\s+llm\s+recomendad"
    r"|recomendaci[oó]n\s+(?:de|del)\s+nivel\s+de\s+llm"
    r"|recomienda\s+(?:el\s+)?nivel\s+de\s+llm"
    r"|no\s+recomiend\w*[^.\n]{0,100}\b(?:nivel|modelo|modelos|llm)\b"
    r"|(?<!no )recomiend\w*[^.\n]{0,100}\b(?:el\s+)?(?:nivel|modelo|modelos|llm)\b",
    re.IGNORECASE,
)
FEATURE_SCORING = re.compile(
    r"references/feature-level\.md"
    r"|nivel de feature"
    r"|esfuerzo previsto del llm"
    r"|calificaci[oó]n[^.\n]{0,60}feature"
    r"|puntuaci[oó]n[^.\n]{0,60}feature"
    r"|scoring[^.\n]{0,60}feature",
    re.IGNORECASE,
)
ACTIVE_MODEL_RECOMMENDATION = re.compile(
    r"model-selection\.md"
    r"|nivel\s+de\s+llm\s+recomendad"
    r"|nivel\s+recomendado\s*:\s*(?:bajo|medio|alto)"
    r"|recomienda\s+(?:solo\s+)?(?:el\s+)?nivel\s+de\s+llm"
    r"|modelo\s+recomendado\s*:",
    re.IGNORECASE,
)


def markdown_files(directory: Path) -> list[Path]:
    return sorted(directory.rglob("*.md")) if directory.is_dir() else []


class ModelRecommendationsContractTest(unittest.TestCase):
    def assert_silent(self, path: Path, content: str) -> None:
        self.assertIsNone(
            MODEL_GUIDANCE.search(content),
            f"{path.relative_to(ROOT)} contiene una recomendación/matriz de modelo fuera de SDD",
        )
        self.assertIsNone(
            FEATURE_SCORING.search(content),
            f"{path.relative_to(ROOT)} puntúa features fuera de SDD",
        )

    def test_canonical_non_sdd_sources_are_silent(self) -> None:
        for agent_id in MANIFEST["agents"]:
            if agent_id == "sdd":
                continue
            path = ROOT / "canonical/agents" / f"{agent_id}.md"
            self.assert_silent(path, path.read_text(encoding="utf-8"))

        for skill_id in MANIFEST["skills"]:
            if skill_id == "sdd-spec":
                continue
            matrix = (
                ROOT / "canonical" / "skills" / skill_id
                / "references" / "model-selection.md"
            )
            self.assertFalse(
                matrix.exists(),
                f"Matriz canónica no-SDD todavía presente: {matrix.relative_to(ROOT)}",
            )
            for path in markdown_files(ROOT / "canonical/skills" / skill_id):
                self.assert_silent(path, path.read_text(encoding="utf-8"))

    def test_adapters_are_silent_outside_sdd(self) -> None:
        for platform in MANIFEST["platforms"]:
            for agent_id in MANIFEST["agents"]:
                if agent_id == "sdd":
                    continue
                path = ROOT / "adapters" / platform / "agents" / f"{agent_id}.json"
                self.assertTrue(path.is_file(), f"Falta adaptador: {path.relative_to(ROOT)}")
                self.assert_silent(path, path.read_text(encoding="utf-8"))

    def test_generated_artifacts_have_no_retired_non_sdd_matrices(self) -> None:
        non_sdd_skills = set(MANIFEST["skills"]) - {"sdd-spec"}
        for platform in MANIFEST["platforms"]:
            stale_matrices = [ROOT / "generated" / platform / "skills" / skill_id
                              / "references" / "model-selection.md"
                              for skill_id in MANIFEST["skills"]]
            self.assertFalse(
                any(matrix.exists() for matrix in stale_matrices),
                f"{platform}: generated aún conserva matriz LLM retirada",
            )
            for agent_id in MANIFEST["agents"]:
                adapter_path = ROOT / "adapters" / platform / "agents" / f"{agent_id}.json"
                adapter = json.loads(adapter_path.read_text(encoding="utf-8"))
                agent_path = ROOT / "generated" / platform / "agents" / adapter["filename"]
                if agent_path.is_file():
                    content = agent_path.read_text(encoding="utf-8")
                    self.assertIsNone(ACTIVE_MODEL_RECOMMENDATION.search(content),
                                      f"{platform}/{agent_id} emite guía LLM")
                    if agent_id != "sdd":
                        self.assertIsNone(FEATURE_SCORING.search(content),
                                          f"{platform}/{agent_id} puntúa features")
            for skill_id in non_sdd_skills:
                for path in markdown_files(ROOT / "generated" / platform / "skills" / skill_id):
                    self.assert_silent(path, path.read_text(encoding="utf-8"))
            generated_sdd_skill = ROOT / "generated" / platform / "skills/sdd-spec/SKILL.md"
            self.assertTrue(generated_sdd_skill.is_file())
            self.assertIsNone(ACTIVE_MODEL_RECOMMENDATION.search(
                generated_sdd_skill.read_text(encoding="utf-8")
            ))
            feature_reference = ROOT / "generated" / platform / "skills/sdd-spec/references/feature-level.md"
            self.assertTrue(feature_reference.is_file(), f"{platform}: falta feature-level.md")

    def test_sdd_alone_owns_feature_scoring_not_model_selection_gates(self) -> None:
        agent = (ROOT / "canonical/agents/sdd.md").read_text(encoding="utf-8")
        skill = (ROOT / "canonical/skills/sdd-spec/SKILL.md").read_text(encoding="utf-8")
        feature_reference = ROOT / "canonical/skills/sdd-spec/references/feature-level.md"

        self.assertTrue(feature_reference.is_file())
        for label, content in (("agente SDD", agent), ("skill SDD", skill)):
            with self.subTest(source=label):
                self.assertRegex(content, FEATURE_SCORING)
        self.assertIn("Esfuerzo previsto del LLM:", agent)
        self.assertIn("Esfuerzo previsto del LLM:", skill)
        self.assertNotIn("Nivel de feature:", agent + skill)
        self.assertNotIn("sdd-effort-examples.md", agent + skill)
        self.assertIn("no recomienda modelos", skill)
        self.assertIn("no\n  recomienda niveles de LLM", agent)
        self.assertNotIn("model-selection.md", feature_reference.read_text(encoding="utf-8"))
        self.assertFalse((ROOT / "canonical/skills/sdd-spec/references/model-selection.md").exists())

    def test_real_roles_gates_and_confirmations_remain(self) -> None:
        sdd_skill = (ROOT / "canonical/skills/sdd-spec/SKILL.md").read_text(encoding="utf-8")
        for gate in ("GATE 1", "GATE 2", "GATE 3", "GATE 4"):
            self.assertIn(gate, sdd_skill)
        self.assertIn("espera solo la aprobación del gate SDD real", sdd_skill)

        for skill_id in ("architecture", "data-api"):
            skill = (ROOT / "canonical/skills" / skill_id / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=skill_id):
                self.assertIn("confirma", skill.lower())
                self.assertTrue("confirmación" in skill.lower() or "confirma" in skill.lower())

        review = (ROOT / "canonical/agents/code-review.md").read_text(encoding="utf-8")
        self.assertIn("autorización", review.lower())
        self.assertIn("Handoff Result", review)


if __name__ == "__main__":
    unittest.main(verbosity=2)
