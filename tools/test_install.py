"""Tests for the installers, run against a throwaway HOME.

Every test copies the kit into a temporary directory, points ``HOME`` at another
temporary directory and runs the real installer. Nothing touches the developer's
actual installation.

Covered contracts (docs/mejoras.md P0.4):

* A complete install leaves every skill and agent of the manifest in place.
* Missing or partial ``generated/`` content aborts with a non-zero exit code and
  never prints a success line.
* ``--dry-run`` creates and modifies nothing.
* Re-running the installer is idempotent.
* The backup taken before overwriting can restore the previous state.

PowerShell installers are not exercised here: ``pwsh`` is not available on every
development machine. Their parity is covered by review and by CI on Windows.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Per platform: installer name, skills destination, agents destination, backup root.
PLATFORMS = {
    "copilot": (".copilot/skills", ".copilot/agents", ".copilot-backup"),
    "opencode": (".config/opencode/skills", ".config/opencode/agent", ".opencode-kit-backup"),
    "kiro": (".kiro/skills", ".kiro/agents", ".kiro-kit-backup"),
}

# Directories the kit needs in order to render, validate and install.
COPIED = ("canonical", "adapters", "tools", "scripts", "generated")

SUCCESS_MARKERS = ("Instalación completada", "Restauración completada")

PASSED = 0
FAILED = 0


def ok(msg: str) -> None:
    global PASSED
    PASSED += 1
    print(f"  \033[32m\u2713\033[0m {msg}")


def fail(msg: str, detail: str = "") -> None:
    global FAILED
    FAILED += 1
    print(f"  \033[31m\u2717\033[0m {msg}")
    if detail:
        for line in detail.strip().splitlines():
            print(f"      {line}")


def check(condition: bool, msg: str, detail: str = "") -> None:
    ok(msg) if condition else fail(msg, detail)


def manifest() -> dict:
    return json.loads((ROOT / "canonical" / "manifest.json").read_text(encoding="utf-8"))


def agent_filenames(platform: str, agents: list[str]) -> list[str]:
    names = []
    for agent_id in agents:
        adapter = ROOT / "adapters" / platform / "agents" / f"{agent_id}.json"
        names.append(json.loads(adapter.read_text(encoding="utf-8"))["filename"])
    return names


def build_repo(base: Path) -> Path:
    """Copy the parts of the kit an installer needs into an isolated repo."""
    repo = base / "kit"
    repo.mkdir()
    for name in COPIED:
        source = ROOT / name
        if source.is_dir():
            shutil.copytree(source, repo / name, ignore=shutil.ignore_patterns("__pycache__"))
    return repo


def run_installer(repo: Path, home: Path, platform: str, *args: str):
    """Run an installer with an isolated HOME and a deterministic XDG path."""
    env = dict(os.environ)
    env["HOME"] = str(home)
    # opencode falls back to $HOME/.config only when XDG_CONFIG_HOME is unset.
    env.pop("XDG_CONFIG_HOME", None)
    return subprocess.run(
        ["bash", str(repo / "scripts" / "install" / f"{platform}.sh"), *args],
        capture_output=True,
        text=True,
        env=env,
    )


def installed_paths(home: Path, platform: str) -> tuple[Path, Path]:
    skills_rel, agents_rel, _ = PLATFORMS[platform]
    return home / skills_rel, home / agents_rel


def missing_artifacts(home: Path, platform: str) -> list[str]:
    data = manifest()
    skills_dest, agents_dest = installed_paths(home, platform)
    missing = [
        skill for skill in data["skills"] if not (skills_dest / skill / "SKILL.md").is_file()
    ]
    missing += [
        name
        for name in agent_filenames(platform, data["agents"])
        if not (agents_dest / name).is_file()
    ]
    return missing


def claims_success(result) -> bool:
    return any(marker in result.stdout for marker in SUCCESS_MARKERS)


def entries_under(path: Path) -> list[Path]:
    return [child for child in path.rglob("*")] if path.is_dir() else []


# ---------------------------------------------------------------------------
# 1. A complete installation installs everything the manifest declares
# ---------------------------------------------------------------------------
def test_install_completo() -> None:
    print("\n\033[1m[1] Instalación completa\033[0m")
    data = manifest()
    for platform in PLATFORMS:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            repo = build_repo(base)
            home = base / "home"
            home.mkdir()
            result = run_installer(repo, home, platform)
            check(result.returncode == 0, f"{platform}: exit 0", result.stderr)
            missing = missing_artifacts(home, platform)
            check(
                not missing,
                f"{platform}: instala {len(data['skills'])} skills y "
                f"{len(data['agents'])} agentes",
                "faltan: " + ", ".join(missing) if missing else "",
            )


# ---------------------------------------------------------------------------
# 2. Missing generated/ must abort, not report success
# ---------------------------------------------------------------------------
def test_falla_si_falta_generated() -> None:
    print("\n\033[1m[2] Falla temprano si falta generated/\033[0m")
    for platform in PLATFORMS:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            repo = build_repo(base)
            shutil.rmtree(repo / "generated" / platform)
            home = base / "home"
            home.mkdir()
            result = run_installer(repo, home, platform)
            check(result.returncode != 0, f"{platform}: exit distinto de cero", result.stdout)
            check(
                not claims_success(result),
                f"{platform}: no declara la instalación completada",
                result.stdout,
            )


# ---------------------------------------------------------------------------
# 3. Partial content must abort too
# ---------------------------------------------------------------------------
def test_falla_si_falta_una_skill() -> None:
    print("\n\033[1m[3] Falla si el contenido está incompleto\033[0m")
    victim = manifest()["skills"][0]
    for platform in PLATFORMS:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            repo = build_repo(base)
            shutil.rmtree(repo / "generated" / platform / "skills" / victim)
            home = base / "home"
            home.mkdir()
            result = run_installer(repo, home, platform)
            check(
                result.returncode != 0,
                f"{platform}: rechaza una instalación sin '{victim}'",
                result.stdout,
            )
            check(
                not claims_success(result),
                f"{platform}: no declara éxito con contenido incompleto",
                result.stdout,
            )


# ---------------------------------------------------------------------------
# 4. --dry-run must not create or modify anything
# ---------------------------------------------------------------------------
def test_dry_run_sin_efectos() -> None:
    print("\n\033[1m[4] --dry-run no escribe nada\033[0m")
    for platform in PLATFORMS:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            repo = build_repo(base)
            home = base / "home"
            home.mkdir()
            result = run_installer(repo, home, platform, "--dry-run")
            check(result.returncode == 0, f"{platform}: exit 0 en dry-run", result.stderr)
            created = entries_under(home)
            check(
                not created,
                f"{platform}: no crea rutas bajo HOME",
                "creado: " + ", ".join(str(p.relative_to(home)) for p in created),
            )


# ---------------------------------------------------------------------------
# 5. Installing twice is idempotent
# ---------------------------------------------------------------------------
def test_actualizacion_idempotente() -> None:
    print("\n\033[1m[5] Actualización idempotente\033[0m")
    for platform in PLATFORMS:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            repo = build_repo(base)
            home = base / "home"
            home.mkdir()
            run_installer(repo, home, platform)
            result = run_installer(repo, home, platform)
            check(result.returncode == 0, f"{platform}: segunda ejecución exit 0", result.stderr)
            missing = missing_artifacts(home, platform)
            check(
                not missing,
                f"{platform}: el destino sigue completo",
                "faltan: " + ", ".join(missing) if missing else "",
            )


# ---------------------------------------------------------------------------
# 6. The backup restores the previous state
# ---------------------------------------------------------------------------
def test_rollback_desde_backup() -> None:
    print("\n\033[1m[6] Rollback desde el backup\033[0m")
    for platform in PLATFORMS:
        skills_rel, _, backup_rel = PLATFORMS[platform]
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            repo = build_repo(base)
            home = base / "home"
            home.mkdir()

            # Seed a previous installation with a recognisable marker.
            victim = manifest()["skills"][0]
            previous = home / skills_rel / victim
            previous.mkdir(parents=True)
            (previous / "SKILL.md").write_text("VERSION ANTERIOR\n", encoding="utf-8")

            result = run_installer(repo, home, platform)
            check(result.returncode == 0, f"{platform}: instala sobre lo previo", result.stderr)

            overwritten = (previous / "SKILL.md").read_text(encoding="utf-8")
            check(
                "VERSION ANTERIOR" not in overwritten,
                f"{platform}: sobrescribe la versión anterior",
            )

            backup_root = home / backup_rel
            copies = list(backup_root.rglob(f"{victim}/SKILL.md")) if backup_root.is_dir() else []
            preserved = [
                path for path in copies if "VERSION ANTERIOR" in path.read_text(encoding="utf-8")
            ]
            check(
                bool(preserved),
                f"{platform}: el backup conserva la versión anterior",
                f"buscado en {backup_root}",
            )

            if preserved:
                shutil.copy(preserved[0], previous / "SKILL.md")
                restored = (previous / "SKILL.md").read_text(encoding="utf-8")
                check(
                    "VERSION ANTERIOR" in restored,
                    f"{platform}: la restauración recupera el estado previo",
                )


# ---------------------------------------------------------------------------
# 7. bash and PowerShell installers stay in parity (static check)
# ---------------------------------------------------------------------------
def test_paridad_bash_powershell() -> None:
    """The PowerShell installers cannot be executed on every machine.

    Their contract is therefore enforced statically, so a fix applied to the bash
    side cannot silently skip its PowerShell counterpart.
    """
    print("\n\033[1m[7] Paridad bash / PowerShell (estático)\033[0m")
    for platform in PLATFORMS:
        for ext in ("sh", "ps1"):
            path = ROOT / "scripts" / "install" / f"{platform}.{ext}"
            rel = path.relative_to(ROOT)
            if not path.is_file():
                fail(f"{rel}: no existe")
                continue
            content = path.read_text(encoding="utf-8")
            check("install_preflight" in content, f"{rel}: delega en install_preflight.py")
            check(
                f"--platform {platform}" in content,
                f"{rel}: pasa --platform {platform}",
            )
            check("--check-source" in content, f"{rel}: valida el origen antes de escribir")
            check(
                "--check-installed" in content,
                f"{rel}: verifica el destino antes de declarar éxito",
            )
            # -printf is a GNU extension missing from the find shipped with macOS.
            check("-printf" not in content, f"{rel}: sin extensiones GNU de find")


def main() -> int:
    print("\033[1mTests de instalación (HOME temporal)\033[0m")
    test_paridad_bash_powershell()
    if sys.platform == "win32":
        print("\nLos instaladores bash no se ejecutan en Windows; se omiten [1]-[6].")
    else:
        test_install_completo()
        test_falla_si_falta_generated()
        test_falla_si_falta_una_skill()
        test_dry_run_sin_efectos()
        test_actualizacion_idempotente()
        test_rollback_desde_backup()
    total = PASSED + FAILED
    print(f"\n{PASSED}/{total} pruebas correctas")
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
