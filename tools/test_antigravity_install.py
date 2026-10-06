#!/usr/bin/env python3
"""Isolated stdlib integration tests; execute the native required shell, never real profiles."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
WINDOWS = os.name == "nt"
SHELL = shutil.which("pwsh") or shutil.which("powershell") if WINDOWS else shutil.which("bash")


def snapshot(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
             if p.is_file() else "directory" for p in root.rglob("*")}


def prepare_shell_profile(home: Path, env: dict[str, str], windows: bool) -> None:
    """Prepare only shell infrastructure; do not exclude it from snapshots."""
    if windows:
        # ConsoleHost creates this directory unconditionally. CoreCLR can disable
        # profile gathering, so a new fixture has no StartupProfileData writes.
        # https://github.com/PowerShell/PowerShell/blob/v7.6.6/src/Microsoft.PowerShell.ConsoleHost/host/msh/ConsoleHost.cs
        # https://github.com/dotnet/runtime/blob/v10.0.0/src/coreclr/inc/clrconfigvalues.h
        env["DOTNET_MultiCoreJitNoProfileGather"] = "1"
        (home / "AppData/Local/Microsoft/PowerShell").mkdir(parents=True)


class ShellProfileIsolation(unittest.TestCase):
    def test_windows_fixture_disables_profile_gathering(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            env = {"HOME": str(home), "DOTNET_MultiCoreJitNoProfileGather": "0"}
            prepare_shell_profile(home, env, windows=True)
            self.assertEqual(env["DOTNET_MultiCoreJitNoProfileGather"], "1")
            self.assertTrue((home / "AppData/Local/Microsoft/PowerShell").is_dir())
            self.assertFalse(any(path.is_file() for path in home.rglob("*")))

    def test_non_windows_fixture_unchanged(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            env = {"HOME": str(home)}
            prepare_shell_profile(home, env, windows=False)
            self.assertEqual(env, {"HOME": str(home)})
            self.assertEqual(snapshot(home), {})

    def test_snapshot_still_detects_unexpected_cache_writes(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            prepare_shell_profile(home, {}, windows=True)
            before = snapshot(home)
            unexpected = home / "AppData/Local/Microsoft/PowerShell/StartupProfileData-NonInteractive"
            unexpected.write_text("unexpected shell write", encoding="utf-8")
            self.assertNotEqual(snapshot(home), before)


class AntigravityInstall(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not SHELL:
            raise RuntimeError("Required native shell unavailable: PowerShell" if WINDOWS else "Required bash unavailable")
        manifest = json.loads((ROOT / "canonical/manifest.json").read_text(encoding="utf-8"))
        if "antigravity" not in manifest["platforms"]:
            raise RuntimeError("Real repository manifest does not declare antigravity")
        adapter = ROOT / "adapters/antigravity"
        required = [adapter / "platform.json"] + [
            adapter / "agents" / (aid + ".json") for aid in manifest["agents"]
        ]
        for path in required:
            if not path.is_file():
                raise RuntimeError(f"Required real adapter absent: {path.relative_to(ROOT)}")
        if not (ROOT / "generated/antigravity").is_dir():
            raise RuntimeError("Delivered generated/antigravity absent; run tools/render.py first")

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="antigravity tests ")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / "repo with spaces"
        self.repo.mkdir()
        for directory in ("canonical", "adapters", "tools", "scripts", "generated"):
            source = ROOT / directory
            shutil.copytree(source, self.repo / directory,
                            ignore=shutil.ignore_patterns("__pycache__"))
        self.home = self.base / "profile with spaces"
        self.home.mkdir()
        self.env = {**os.environ, "HOME": str(self.home), "USERPROFILE": str(self.home),
                    "PYTHONDONTWRITEBYTECODE": "1"}
        prepare_shell_profile(self.home, self.env, WINDOWS)
        self.initial_home = snapshot(self.home)
        self.manifest = json.loads((self.repo / "canonical/manifest.json").read_text())
        adapter = self.repo / "adapters/antigravity"
        self.assertIn("antigravity", self.manifest["platforms"], "Copied manifest must declare antigravity")
        self.assertTrue((adapter / "platform.json").is_file(), "Required Antigravity platform adapter absent")
        for aid in self.manifest["agents"]:
            self.assertTrue((adapter / "agents" / (aid + ".json")).is_file(),
                            f"Required Antigravity agent adapter absent: {aid}")
        self.src = self.repo / "generated/antigravity"
        self.assertTrue(self.src.is_dir(), "Delivered generated distribution must exist")
        self.skills = self.home / ".gemini/config/skills"
        self.agents = self.home / ".gemini/config/agents"
        self.sid = self.manifest["skills"][0]
        self.names = [json.loads((adapter / "agents" / (a + ".json")).read_text())["filename"]
                      for a in self.manifest["agents"]]
        self.aid = self.names[0]

    def run_script(self, kind="install", *args):
        script = self.repo / "scripts" / kind / ("antigravity.ps1" if WINDOWS else "antigravity.sh")
        self.assertTrue(script.is_file(), f"Expected script absent: scripts/{kind}/{script.name}")
        flags = [{"--dry-run": "-DryRun", "--force": "-Force"}.get(a, a) for a in args] if WINDOWS else list(args)
        cmd = [SHELL, "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", str(script)] if WINDOWS else [SHELL, str(script)]
        return subprocess.run(cmd + flags, env=self.env, capture_output=True, text=True, timeout=120)

    def success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def failure(self, result):
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("Instalacion completada", result.stdout)
        self.assertNotIn("Instalación completada", result.stdout)

    def installed_equal(self):
        for sid in self.manifest["skills"]:
            canonical = self.repo / "canonical/skills" / sid
            for resource in canonical.rglob("*"):
                if resource.is_file():
                    rel = resource.relative_to(canonical)
                    generated = self.src / "skills" / sid / rel
                    self.assertTrue(generated.is_file(), f"Required generated resource absent: {sid}/{rel}")
                    expected = generated if rel == Path("SKILL.md") else resource
                    self.assertEqual(hashlib.sha256((self.skills / sid / rel).read_bytes()).hexdigest(),
                                     hashlib.sha256(expected.read_bytes()).hexdigest())
        for name in self.names:
            self.assertEqual((self.agents / name).read_bytes(), (self.src / "agents" / name).read_bytes())

    def populate(self):
        (self.skills / self.sid).mkdir(parents=True)
        (self.skills / self.sid / "SKILL.md").write_text("old skill")
        (self.skills / self.sid / "custom.txt").write_text("personal reference")
        self.agents.mkdir(parents=True)
        (self.agents / self.aid).write_text("old agent")

    def test_install_hashes_and_references_spaces(self):
        self.success(self.run_script())
        self.installed_equal()
        self.assertFalse((self.home / ".antigravity-kit-backup").exists())

    def test_missing_skill(self):
        (self.src / "skills" / self.sid / "SKILL.md").unlink()
        self.failure(self.run_script())
        self.assertEqual(snapshot(self.home), self.initial_home)

    def test_missing_agent(self):
        (self.src / "agents" / self.aid).unlink()
        self.failure(self.run_script())
        self.assertEqual(snapshot(self.home), self.initial_home)

    def canonical_reference(self):
        for sid in self.manifest["skills"]:
            canonical = self.repo / "canonical/skills" / sid
            for resource in sorted((canonical / "references").rglob("*")):
                if resource.is_file():
                    return sid, resource.relative_to(canonical)
        self.fail("Real canonical skills must provide a reference for this regression")

    def test_missing_source_reference_aborts_before_writes(self):
        sid, rel = self.canonical_reference()
        (self.src / "skills" / sid / rel).unlink()
        self.populate()
        before = snapshot(self.home)
        self.failure(self.run_script())
        self.assertEqual(snapshot(self.home), before)

    def inject_installed_reference_change(self, corrupt=False):
        sid, rel = self.canonical_reference()
        p = self.repo / "tools/install_preflight.py"
        target = self.skills / sid / rel
        operation = f"Path({str(target)!r}).write_bytes(b'corrupted reference')" if corrupt else f"Path({str(target)!r}).unlink()"
        # Only mutate at postflight: source validation and the real copy still run.
        marker = "    args = parser.parse_args(argv)\n"
        self.assertIn(marker, p.read_text())
        p.write_text(p.read_text().replace(marker, marker +
                     f"    if args.check_installed:\n        {operation}\n"))
        return target

    def test_missing_installed_reference_no_success(self):
        target = self.inject_installed_reference_change()
        self.failure(self.run_script())
        self.assertFalse(target.exists())

    def test_corrupted_installed_reference_no_success(self):
        target = self.inject_installed_reference_change(corrupt=True)
        self.failure(self.run_script())
        self.assertEqual(target.read_bytes(), b"corrupted reference")

    def test_dryrun_empty(self):
        before = snapshot(self.base)
        self.success(self.run_script("install", "--dry-run"))
        self.assertEqual(snapshot(self.base), before)

    def test_dryrun_populated(self):
        self.populate()
        before = snapshot(self.base)
        self.success(self.run_script("install", "--dry-run"))
        self.assertEqual(snapshot(self.base), before)

    def test_force(self):
        self.populate()
        self.success(self.run_script("install", "--force"))
        self.installed_equal()
        self.assertFalse((self.home / ".antigravity-kit-backup").exists())
        self.assertEqual((self.skills / self.sid / "custom.txt").read_text(), "personal reference")

    def test_backup_and_manual_restore(self):
        self.populate()
        old = snapshot(self.skills / self.sid)
        self.success(self.run_script())
        backup, = (self.home / ".antigravity-kit-backup").iterdir()
        self.assertEqual(snapshot(backup / "skills" / self.sid), old)
        self.assertEqual((backup / "agents" / self.aid).read_text(), "old agent")
        shutil.copytree(backup / "skills" / self.sid, self.skills / self.sid, dirs_exist_ok=True)
        shutil.copy2(backup / "agents" / self.aid, self.agents / self.aid)
        self.assertEqual((self.skills / self.sid / "SKILL.md").read_text(), "old skill")
        self.assertEqual((self.agents / self.aid).read_text(), "old agent")

    def test_extras_ignored_and_personal_preserved(self):
        self.populate()
        files = [self.skills / "personal/SKILL.md", self.agents / "personal.md",
                 self.home / ".gemini/config/settings.json", self.home / ".gemini/config/rules.md",
                 self.home / ".gemini/credentials.json"]
        for p in files:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("fictional personal data")
        (self.src / "skills/rogue").mkdir()
        (self.src / "skills/rogue/SKILL.md").write_text("rogue")
        (self.src / "agents/rogue.md").write_text("rogue")
        self.success(self.run_script())
        for p in files:
            self.assertEqual(p.read_text(), "fictional personal data")
        self.assertFalse((self.skills / "rogue").exists())
        self.assertFalse((self.agents / "rogue.md").exists())
        self.assertEqual((self.skills / self.sid / "custom.txt").read_text(), "personal reference")

    def test_second_install_and_timestamp_collision(self):
        # Freeze shell clock in the copied script, including PowerShell on Windows.
        p = self.repo / "scripts/install" / ("antigravity.ps1" if WINDOWS else "antigravity.sh")
        self.assertTrue(p.is_file(), "Expected installer absent")
        text = p.read_text().replace('Get-Date -Format "yyyyMMdd-HHmmss"', '"20000101-000000"').replace('date +%Y%m%d-%H%M%S', "printf 20000101-000000")
        p.write_text(text)
        self.populate()
        self.success(self.run_script())
        root = self.home / ".antigravity-kit-backup"
        before = snapshot(root)
        self.success(self.run_script())
        self.assertEqual(len(list(root.iterdir())), 2)
        for path, digest in before.items():
            self.assertEqual(snapshot(root)[path], digest)
        self.installed_equal()

    def test_preflight_stdout_failure(self):
        (self.repo / "tools/install_preflight.py").write_text("print('fake stdout')\nraise SystemExit(1)\n")
        self.failure(self.run_script())
        self.assertEqual(snapshot(self.home), self.initial_home)

    def test_postflight_failure(self):
        p = self.repo / "tools/install_preflight.py"
        p.write_text("import sys\nprint('fake stdout')\nraise SystemExit(1 if '--check-installed' in sys.argv else 0)\n")
        self.failure(self.run_script())
        self.assertTrue((self.skills / self.sid / "SKILL.md").exists())

    def test_copy_failure_preserves_backup(self):
        self.populate()
        # A nonempty directory cannot be overwritten by a regular resource file.
        (self.skills / self.sid / "SKILL.md").unlink()
        (self.skills / self.sid / "SKILL.md").mkdir()
        (self.skills / self.sid / "SKILL.md/blocker.txt").write_text("preserve")
        self.failure(self.run_script())
        backup, = (self.home / ".antigravity-kit-backup").iterdir()
        self.assertTrue((backup / "skills" / self.sid / "SKILL.md").is_dir())

    def test_export_filtered_content(self):
        self.success(self.run_script())
        (self.agents / "personal.md").write_text("fictional")
        (self.skills / "personal").mkdir()
        (self.skills / "personal/SKILL.md").write_text("fictional")
        before = {d: snapshot(self.repo / d) for d in ("canonical", "adapters")}
        self.success(self.run_script("backup"))
        exported, = (self.repo / "imports/antigravity").iterdir()
        self.assertEqual(snapshot(exported / "skills"), snapshot(self.src / "skills"))
        self.assertEqual(snapshot(exported / "agents"), snapshot(self.src / "agents"))
        for d in before:
            self.assertEqual(snapshot(self.repo / d), before[d])

    def test_export_dryrun_zero_writes(self):
        self.success(self.run_script())
        before = snapshot(self.base)
        self.success(self.run_script("backup", "--dry-run"))
        self.assertEqual(snapshot(self.base), before)

    def test_export_partial_warning(self):
        self.populate()
        result = self.run_script("backup")
        self.success(result)
        self.assertIn("No instalado:", result.stdout)
        exported, = (self.repo / "imports/antigravity").iterdir()
        self.assertEqual((exported / "agents" / self.aid).read_text(), "old agent")
        self.assertNotIn("Instalacion completada", result.stdout)

    def test_export_failure_exit_code(self):
        (self.repo / "tools/import_installed.py").write_text("print('import failure')\nraise SystemExit(7)\n")
        result = self.run_script("backup")
        self.assertEqual(result.returncode, 7, result.stdout + result.stderr)


if __name__ == "__main__":
    print("Native integration shell:", SHELL, flush=True)
    print("Testing real Antigravity distribution in isolated repository/profile copies.", flush=True)
    unittest.main(verbosity=2)
