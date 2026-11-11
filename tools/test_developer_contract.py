#!/usr/bin/env python3
"""Offline prompt/distribution contracts and controlled fixtures, NOT LLM behavior.

No benchmark runner is imported. Behavioral acceptance (especially cross-session
continuity) remains pending until explicitly budgeted model runs are authorized.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import render
import retired_agents
import developer_migration as migration

ROOT = Path(__file__).resolve().parent.parent
FROZEN = ROOT / "docs/experimentos/continuidad-developer-v2-refuerzos-2026-11-06/fuentes"
ARCHIVE = ROOT / "tools/fixtures/developer_previous.json"
DELTA_A = (
    "Vincula los criterios afectados con pruebas o checks observables, sin casos de relleno. "
    "Cuando modifiques código compartido, contrasta con el baseline disponible el comportamiento "
    "existente que no se pidió cambiar y añade regresión para protegerlo."
)
DELTA_B = (
    "Al reanudar, contrasta el registro con el código y las verificaciones disponibles antes de "
    "continuar; los estados guardados no sustituyen evidencia vigente. Si cambia un requisito, "
    "actualiza su literal y reabre solo el trabajo afectado."
)
AGENT = """# Developer

{{project_context}}

{{mas_identity}}

Eres Developer, agente de desarrollo integral del MAS. Carga y sigue `developer`,
autoridad única de tu procedimiento. No cambies de agente automáticamente.
"""


def expected_skill() -> str:
    text = (FROZEN / "SKILL-candidato2.md").read_text(encoding="utf-8")
    lines = text.splitlines()
    for heading, delta in (("Comprobar", DELTA_A), ("Continuidad bajo demanda", DELTA_B)):
        matches = [i for i, line in enumerate(lines) if line.startswith(f"- **{heading}.**")]
        if len(matches) != 1:
            raise ValueError(f"Base congelada ambigua: {heading}")
        lines[matches[0]] += " " + delta
    text = "\n".join(lines) + "\n"
    for old, new in (("__SKILL__", "developer"), ("__DATA_API__", "data-api"),
                     ("__UI_DESIGN__", "ui-design"), ("# Developer v2 — candidato 2", "# Developer")):
        text = text.replace(old, new)
    return text


def contract_errors(agent: str, skill: str) -> list[str]:
    # Full equivalence, not a keyword proxy: extra/old authorities also fail.
    errors = []
    if agent.replace("\r\n", "\n") != AGENT:
        errors.append("agent")
    if skill.replace("\r\n", "\n") != expected_skill():
        errors.append("skill")
    return errors


class DeveloperContract(unittest.TestCase):
    def test_frozen_sources_and_originals_are_unchanged(self):
        originals = ROOT / "docs/experimentos/archive/developer-v2-dominios-build-gemini-2026-11-05/candidato"
        for filename, original, sha in (
            ("agent-candidato2.md", "agent.md", "67d8173d21000004496be59c5990b6d843ae5a956a4cfa06ff317562dc0de1d9"),
            ("SKILL-candidato2.md", "SKILL.md", "2b06d8950e791cf911d5aea455b4e9bf9d404452da48239cc290872efc744d78"),
        ):
            with self.subTest(source=filename):
                data = (FROZEN / filename).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), sha)
                self.assertEqual(data, (originals / original).read_bytes())

    def test_deltas_match_historical_code_without_importing_runners(self):
        for filename in ("mobile_benchmark_common.py", "real_android_harness_benchmark.py"):
            tree = ast.parse((ROOT / "tools" / filename).read_text(encoding="utf-8"))
            values = {node.targets[0].id: ast.literal_eval(node.value) for node in tree.body
                      if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
                      and node.targets[0].id in ("DELTA_A", "DELTA_B")}
            self.assertEqual(values, {"DELTA_A": DELTA_A, "DELTA_B": DELTA_B})

    def test_full_composition_and_delta_placement(self):
        agent = (ROOT / "canonical/agents/developer.md").read_text(encoding="utf-8")
        skill = (ROOT / "canonical/skills/developer/SKILL.md").read_text(encoding="utf-8")
        self.assertEqual(contract_errors(agent, skill), [])
        for heading, delta in (("Comprobar", DELTA_A), ("Continuidad bajo demanda", DELTA_B)):
            self.assertEqual(skill.count(delta), 1)
            self.assertTrue(next(line for line in skill.splitlines()
                                 if line.startswith(f"- **{heading}.**")).endswith(delta))

    def test_negative_compositions(self):
        skill = expected_skill()
        archived = json.loads(ARCHIVE.read_text(encoding="utf-8"))["files"]
        mutations = {
            "omit A": skill.replace(" " + DELTA_A, ""),
            "omit B": skill.replace(" " + DELTA_B, ""),
            "duplicate A": skill.replace(DELTA_A, DELTA_A + " " + DELTA_A),
            "duplicate B": skill.replace(DELTA_B, DELTA_B + " " + DELTA_B),
            "wrong points": skill.replace(DELTA_A, "SWAP").replace(DELTA_B, DELTA_A).replace("SWAP", DELTA_B),
            "truncate base": skill.replace("Conserva contratos, datos y trabajo local; ", ""),
            "old second authority": skill + archived["canonical/skills/developer/SKILL.md"]["text"],
            "wrong namespace": skill.replace("`data-api`", "`hv2-data-api`"),
        }
        self.assertEqual(contract_errors(AGENT, skill.replace("\n", "\r\n")), [])
        for label, mutated in mutations.items():
            with self.subTest(mutation=label):
                self.assertNotEqual(mutated, skill)
                self.assertIn("skill", contract_errors(AGENT, mutated))
        self.assertIn("agent", contract_errors(AGENT + archived["canonical/agents/developer.md"]["text"], skill))

    def test_archive_is_complete_non_invocable_and_hash_verified(self):
        self.assertEqual(hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
                         "cd65f99ba94af3a55d272e3745f345ce16057997adbe8dcc29d557dd8b4d6fff")
        archive = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        self.assertEqual(archive["baseline_commit"], "b5a7dc439212b68c3488998a071ab9772839af86")
        self.assertEqual(len(archive["files"]), 14)
        for relative, entry in archive["files"].items():
            with self.subTest(archived=relative):
                self.assertEqual(hashlib.sha256(entry["text"].encode()).hexdigest(), entry["sha256"])
        self.assertNotIn("canonical", ARCHIVE.relative_to(ROOT).parts)
        self.assertNotIn("generated", ARCHIVE.relative_to(ROOT).parts)
        self.assertEqual(ARCHIVE.suffix, ".json")

    def test_distribution_and_metadata_preserve_public_ids_and_host_limits(self):
        manifest = json.loads((ROOT / "canonical/manifest.json").read_text())
        archived = json.loads(ARCHIVE.read_text(encoding="utf-8"))["files"]
        self.assertEqual(manifest, json.loads(archived["canonical/manifest.json"]["text"]))
        for platform in manifest["platforms"]:
            with self.subTest(platform=platform):
                relative = f"adapters/{platform}/agents/developer.json"
                adapter = json.loads((ROOT / relative).read_text())
                old = json.loads(archived[relative]["text"])
                # Only human-facing naming/description may change, never permissions/tools/model.
                current_meta, old_meta = dict(adapter["frontmatter"]), dict(old["frontmatter"])
                for field in ("description", "name"):
                    current_meta.pop(field, None)
                    old_meta.pop(field, None)
                if platform == "kiro":
                    # Additive resource discovery for Kiro V3; permissions/tools
                    # remain byte-for-byte identical and are checked separately.
                    current_meta.pop("resources", None)
                self.assertEqual(current_meta, old_meta)
                # The version label in the Antigravity host note is documentation,
                # not a capability change; normalize it before comparing.
                current_suffix = adapter.get("body_suffix", "").replace("Antigravity 2.x", "Antigravity 2.0")
                self.assertEqual(current_suffix, old.get("body_suffix", ""))
                self.assertEqual(adapter["filename"], old["filename"])
                if platform == "copilot":
                    self.assertEqual(adapter["frontmatter"]["name"], "Developer")
                output = ROOT / "generated" / platform
                skill = output / "skills/developer"
                self.assertEqual(sorted(p.name for p in skill.rglob("*") if p.is_file()), ["SKILL.md"])
                self.assertEqual((skill / "SKILL.md").read_text(encoding="utf-8"), expected_skill())
                body = render.substitute(AGENT, render.shared_substitutions(), platform)
                self.assertEqual((output / "agents" / adapter["filename"]).read_text(encoding="utf-8"),
                                 render.frontmatter(adapter["frontmatter"]) + body + adapter.get("body_suffix", ""))
                self.assertEqual(len(list((output / "agents").glob("developer*"))), 1)
                self.assertEqual(len(list((output / "skills").glob("developer*"))), 1)
        self.assertFalse((ROOT / "canonical/skills/developer/references/plan.md").exists())
        self.assertNotIn('"developer"', (ROOT / "tools/retired_agents.json").read_text())


class DeveloperInstallation(unittest.TestCase):
    """Execute the real Bash installers on clean and prior-version fixtures."""

    @unittest.skipIf(os.name == "nt", "Bash fixtures; native Windows remains pending")
    def test_clean_upgrade_backups_extras_and_rollback_all_platforms(self):
        from test_install import PLATFORMS, agent_filenames, installed_paths, run_installer
        archived = json.loads(ARCHIVE.read_text(encoding="utf-8"))["files"]
        for platform in PLATFORMS:
            with self.subTest(platform=platform), tempfile.TemporaryDirectory(prefix="developer-install-") as temp:
                home = Path(temp).resolve()
                before = list(home.rglob("*"))
                result = run_installer(ROOT, home, platform, "--dry-run")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(list(home.rglob("*")), before)
                result = run_installer(ROOT, home, platform)
                self.assertEqual(result.returncode, 0, result.stderr)
                skills, agents = installed_paths(home, platform)
                agent_name = agent_filenames(platform, ["developer"])[0]
                self.assertEqual((skills / "developer/SKILL.md").read_text(), expected_skill())
                adapter = json.loads(archived[f"adapters/{platform}/agents/developer.json"]["text"])
                substitutions = {token: archived[f"canonical/shared/{filename}"]["text"].rstrip("\n")
                                 for token, filename in render.SHARED_TOKENS.items()}
                old_agent = render.frontmatter(adapter["frontmatter"]) + render.substitute(
                    archived["canonical/agents/developer.md"]["text"], substitutions, platform
                ) + adapter.get("body_suffix", "")
                old_skill = render.substitute(archived["canonical/skills/developer/SKILL.md"]["text"],
                                              substitutions, platform)
                previous = {agents / agent_name: old_agent, skills / "developer/SKILL.md": old_skill}
                for path, text in previous.items():
                    path.write_text(text, encoding="utf-8")
                reference = skills / "developer/references/plan.md"
                reference.parent.mkdir(parents=True, exist_ok=True)
                reference.write_text(archived["canonical/skills/developer/references/plan.md"]["text"])
                extra = skills / "developer/custom.txt"
                extra.write_text("personalizado\n")
                result = run_installer(ROOT, home, platform)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual((skills / "developer/SKILL.md").read_text(), expected_skill())
                self.assertEqual((agents / agent_name).read_bytes(),
                                 (ROOT / "generated" / platform / "agents" / agent_name).read_bytes())
                self.assertEqual(extra.read_text(), "personalizado\n")
                # Merge is intentionally NOT misreported as removal of old resources.
                self.assertTrue(reference.is_file())
                backup_root = home / PLATFORMS[platform][2]
                for path, text in previous.items():
                    backups = [p for p in backup_root.rglob(path.name)
                               if p.is_file() and p.read_text(encoding="utf-8") == text]
                    self.assertTrue(backups, path.name)
                    self.assertFalse(any(parent in (agents, skills) for parent in backups[0].parents))
                    # Restore only the two selected artifacts in this temporary fixture.
                    path.write_bytes(backups[0].read_bytes())
                    self.assertEqual(path.read_text(encoding="utf-8"), text)


class DeveloperCleanup(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="developer-cleanup-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.profile = self.base / "config/opencode"
        self.backups = self.base / "backups"
        self.archive = json.loads(ARCHIVE.read_text(encoding="utf-8"))["files"]
        for installed, source in migration.CURRENT.items():
            path = self.profile / installed
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((ROOT / source).read_bytes())
        for relative, archived in (
            ("agents/developer.md", "generated/opencode/agents/developer.md"),
            ("skills/developer/references/plan.md", "canonical/skills/developer/references/plan.md"),
        ):
            path = self.profile / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(self.archive[archived]["text"], encoding="utf-8")

    def snapshot(self):
        return {str(p.relative_to(self.base)): p.read_bytes() if p.is_file() else None
                for p in self.base.rglob("*")}

    def test_known_cleanup_dry_run_idempotence_and_per_file_rollback(self):
        extras = [self.profile / "agents/custom.md", self.profile / "skills/developer/custom.txt",
                  self.base / "unselected-project/.opencode/agents/developer.md"]
        for path in extras:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("personalizado\n")
        before = self.snapshot()
        self.assertEqual(len(migration.clean(self.profile, self.backups)), 2)
        self.assertEqual(self.snapshot(), before)
        results = migration.clean(self.profile, self.backups, apply=True)
        self.assertEqual(len(results), 2)
        migration.verify_current(self.profile)
        self.assertEqual(migration.clean(self.profile, self.backups, apply=True), [])
        for result in results:
            path, backup = Path(result["path"]), Path(result["backup"])
            self.assertFalse(path.exists())
            self.assertNotIn(self.profile, backup.parents)
            self.assertEqual(retired_agents.digest(backup.read_bytes()), result["sha256"])
            retired_agents.restore(backup, path, result["sha256"])
            self.assertEqual(path.read_bytes(), before[str(path.relative_to(self.base))])
            with self.assertRaises(FileExistsError):
                retired_agents.restore(backup, path, result["sha256"])
        for path in extras:
            self.assertEqual(path.read_text(), "personalizado\n")

    def test_customized_candidates_block_without_writing(self):
        for relative in migration.KNOWN:
            with self.subTest(candidate=relative):
                path = self.profile / relative
                old = path.read_bytes()
                path.write_bytes(old + b"\nCUSTOM\n")
                before = self.snapshot()
                with self.assertRaisesRegex(OSError, "personalizados"):
                    migration.clean(self.profile, self.backups, apply=True)
                self.assertEqual(before, self.snapshot())
                path.write_bytes(old)

    def test_current_customization_blocks_without_overwriting(self):
        path = self.profile / "agent/developer.md"
        path.write_bytes(path.read_bytes() + b"\nCUSTOM\n")
        before = self.snapshot()
        with self.assertRaisesRegex(OSError, "vigente no verificado"):
            migration.clean(self.profile, self.backups, apply=True)
        self.assertEqual(before, self.snapshot())

    def test_symlinks_and_active_backup_roots_block(self):
        for backup in (self.profile / "backups", self.profile / "agents/backups"):
            with self.subTest(backup=backup), self.assertRaises(OSError):
                migration.clean(self.profile, backup, apply=True)
        path = self.profile / "agents/developer.md"
        path.unlink()
        path.symlink_to(self.base / "absent.md")
        with self.assertRaises(OSError):
            migration.clean(self.profile, self.backups, apply=True)
        self.assertTrue(path.is_symlink())
        self.assertFalse(self.backups.exists())

    def test_backup_failure_preserves_candidates(self):
        before = self.snapshot()
        with patch.object(migration, "write_backup", side_effect=OSError("fixture backup failure")):
            with self.assertRaisesRegex(OSError, "backup failure"):
                migration.clean(self.profile, self.backups, apply=True)
        self.assertEqual(before, self.snapshot())

    def test_changed_candidate_after_backup_is_not_removed(self):
        original = migration.write_backup
        path = self.profile / "agents/developer.md"

        def changing_backup(*args):
            backup = original(*args)
            path.write_text("changed during backup\n")
            return backup

        with patch.object(migration, "write_backup", side_effect=changing_backup):
            with self.assertRaisesRegex(OSError, "candidato/backup cambió"):
                migration.clean(self.profile, self.backups, apply=True)
        self.assertEqual(path.read_text(), "changed during backup\n")
        self.assertTrue((self.profile / "skills/developer/references/plan.md").is_file())


    def test_cli_defaults_to_read_only_and_apply_is_explicit(self):
        command = [sys.executable, "-B", str(ROOT / "tools/developer_migration.py"),
                   "--opencode-home", str(self.profile), "--backup-root", str(self.backups)]
        before = self.snapshot()
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["mode"], "dry-run")
        self.assertEqual(before, self.snapshot())
        result = subprocess.run(command + ["--apply"], capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        migration.verify_current(self.profile)
        self.assertTrue(all(not (self.profile / relative).exists() for relative in migration.KNOWN))


class DeveloperAcceptanceFixtures(unittest.TestCase):
    """Validate fixture/oracle sensitivity only. No model actions are observed."""

    def setUp(self):
        self.definition = json.loads((ROOT / "tools/fixtures/developer_acceptance.json").read_text())
        self.temp = tempfile.TemporaryDirectory(prefix="developer-acceptance-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()

    def materialize(self, case_id):
        case = self.definition["cases"][case_id]
        directory = self.base / case_id
        directory.mkdir()
        files = dict(self.definition["common_files"]) if case["shared"] else {}
        files.update(case["files"])
        if "initial_source" in case:
            files["shared.py"] = self.definition["oracle_sources"][case["initial_source"]]
        for name, content in files.items():
            (directory / name).write_text(content, encoding="utf-8")
        return directory

    def check_fixture(self, directory, test, expected_exit):
        result = subprocess.run([sys.executable, "-B", "-m", "unittest", test], cwd=directory,
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, expected_exit, result.stdout + result.stderr)
        self.assertFalse(list(directory.rglob("__pycache__")))
        return result

    def source(self, directory, name):
        (directory / "shared.py").write_text(self.definition["oracle_sources"][name])

    def test_a1_baseline_new_criterion_and_regression_sensitive_mutation(self):
        directory = self.materialize("A1")
        self.assertEqual((directory / "baseline.txt").read_bytes(), (directory / "shared.py").read_bytes())
        self.check_fixture(directory, "test_legacy", 0)
        self.check_fixture(directory, "test_prefix", 1)
        self.source(directory, "prefix")
        self.check_fixture(directory, "test_legacy", 0)
        self.check_fixture(directory, "test_prefix", 0)
        self.source(directory, "broken_legacy")
        self.check_fixture(directory, "test_prefix", 0)
        self.check_fixture(directory, "test_legacy", 1)

    def test_a2_has_no_baseline_but_observable_current_checks(self):
        directory = self.materialize("A2")
        self.assertFalse((directory / "baseline.txt").exists())
        self.assertFalse((directory / ".git").exists())
        self.check_fixture(directory, "test_legacy", 0)
        self.source(directory, "prefix")
        self.check_fixture(directory, "test_legacy", 0)
        self.check_fixture(directory, "test_prefix", 0)

    def test_a3_and_b3_small_checks_without_tracking_fixtures(self):
        for case_id in ("A3", "B3"):
            with self.subTest(case=case_id):
                directory = self.materialize(case_id)
                self.assertEqual({p.name for p in directory.iterdir()}, {"greet.py", "test_greet.py"})
                self.check_fixture(directory, "test_greet", 1)
                (directory / "greet.py").write_text(self.definition["cases"][case_id]["solution"])
                self.check_fixture(directory, "test_greet", 0)

    def test_b1_saved_done_state_is_contradicted_by_failing_check(self):
        directory = self.materialize("B1")
        self.assertIn("[x] R2 implementado", (directory / "tarea.md").read_text())
        self.check_fixture(directory, "test_legacy", 0)
        self.check_fixture(directory, "test_prefix", 1)
        self.source(directory, "prefix")
        self.check_fixture(directory, "test_legacy", 0)
        self.check_fixture(directory, "test_prefix", 0)

    def test_b2_requirement_change_affects_only_prefix_behavior(self):
        directory = self.materialize("B2")
        case = self.definition["cases"]["B2"]
        self.assertIn(case["previous_literal"], (directory / "tarea.md").read_text())
        self.assertIn(case["new_literal"], case["prompt"])
        self.check_fixture(directory, "test_legacy", 0)
        self.check_fixture(directory, "test_prefix", 0)
        self.check_fixture(directory, "test_suffix", 1)
        self.source(directory, "suffix")
        self.check_fixture(directory, "test_legacy", 0)
        self.check_fixture(directory, "test_suffix", 0)

    def test_all_behavior_remains_explicitly_pending(self):
        self.assertEqual(self.definition["runtime_status"], "PENDIENTE")
        self.assertEqual(set(self.definition["cases"]), {"A1", "A2", "A3", "B1", "B2", "B3"})
        self.assertIn("NO se entregan al agente", self.definition["execution_boundary"])
        self.assertIn("sesiones nuevas sin contexto previo", self.definition["execution_boundary"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
