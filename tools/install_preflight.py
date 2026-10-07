#!/usr/bin/env python3
"""Preflight and post-install verification shared by every installer.

The shell and PowerShell installers delegate here so that both keep exactly the
same notion of "complete installation". The manifest is the single source of
truth: an installer must never report success after skipping required content.

Modes
-----
``--check-source``
    Verify that ``generated/<platform>/`` holds every skill and agent declared in
    ``canonical/manifest.json``. Run before touching the destination.

``--check-installed``
    Verify that the destination directories hold that same content, and report
    artifacts that the manifest does not declare. Run before reporting success.

``--validate-migration``
    Read-only argument/path validation used by wrappers before any copies.

``--migrate-retired-agents``
    Explicit retirement after checking current installed bytes. Unknown bytes
    require repeated --approve-retired-file and --approve-retired-sha256 pairs.
    --dry-run prints the plan without creating backups or changing installation.

Exit codes
----------
``0``
    Everything required is present.
``1``
    Something required is missing, unreadable, or malformed. The caller must
    abort instead of declaring the installation complete.
``2``
    The invocation itself was wrong (unknown platform, bad arguments).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import retired_agents

ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "canonical"
ADAPTERS = ROOT / "adapters"
GENERATED = ROOT / "generated"

# Entries that are never part of the kit and must not be reported as obsolete.
IGNORED_NAMES = {".DS_Store", "Thumbs.db", "Desktop.ini", ".gitkeep"}


def fail(message: str) -> int:
    print(f"preflight: {message}", file=sys.stderr)
    return 2


def load_manifest() -> dict:
    path = CANONICAL / "manifest.json"
    if not path.is_file():
        raise FileNotFoundError(f"no existe {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def agent_filenames(platform: str, agents: list[str]) -> dict[str, str]:
    """Map each agent id to the filename its adapter declares for this platform."""
    result: dict[str, str] = {}
    for agent_id in agents:
        adapter = ADAPTERS / platform / "agents" / f"{agent_id}.json"
        if not adapter.is_file():
            raise FileNotFoundError(
                f"falta el adaptador {adapter.relative_to(ROOT)}; ejecuta tools/validate.py"
            )
        data = json.loads(adapter.read_text(encoding="utf-8"))
        filename = data.get("filename")
        if not filename or not isinstance(filename, str):
            raise ValueError(f"{adapter.relative_to(ROOT)}: 'filename' ausente o no válido")
        result[agent_id] = filename
    return result


def check_source(platform: str, manifest: dict) -> list[str]:
    """Return the list of problems found in generated/<platform>/."""
    problems: list[str] = []
    skills_src = GENERATED / platform / "skills"
    agents_src = GENERATED / platform / "agents"

    if not (GENERATED / platform).is_dir():
        problems.append(
            f"no existe generated/{platform}/ — ejecuta primero: python3 tools/render.py"
        )
        return problems

    for skill_id in manifest["skills"]:
        skill = skills_src / skill_id / "SKILL.md"
        if not skill.is_file():
            problems.append(f"falta la skill '{skill_id}' (esperado {skill.relative_to(ROOT)})")

    for agent_id, filename in agent_filenames(platform, manifest["agents"]).items():
        agent = agents_src / filename
        if not agent.is_file():
            problems.append(f"falta el agente '{agent_id}' (esperado {agent.relative_to(ROOT)})")

    for entry in retired_agents.load_catalog():
        if entry["platform"] == platform and entry["id"] not in manifest["agents"]:
            retired = agents_src / entry["filename"]
            if retired.exists() or retired.is_symlink():
                problems.append(f"generated desfasado contiene agente retirado: {retired}; regenerar antes de copiar")

    return problems


def check_installed(
    platform: str, manifest: dict, skills_dest: Path, agents_dest: Path
) -> tuple[list[str], list[str]]:
    """Return (problems, notices) for the installed destination."""
    problems: list[str] = []
    notices: list[str] = []

    expected_skills = set(manifest["skills"])
    expected_agents = agent_filenames(platform, manifest["agents"])

    for skill_id in sorted(expected_skills):
        skill = skills_dest / skill_id / "SKILL.md"
        if not skill.is_file():
            problems.append(f"skill no instalada: {skill}")

    for agent_id, filename in sorted(expected_agents.items()):
        agent = agents_dest / filename
        if not agent.is_file():
            problems.append(f"agente no instalado: {agent} ({agent_id})")

    # Artifacts the manifest does not declare. They may be the user's own or
    # left over from a previous version of the kit; we cannot tell them apart,
    # so we only report them and never delete anything.
    if skills_dest.is_dir():
        for child in sorted(skills_dest.iterdir()):
            if child.name in IGNORED_NAMES:
                continue
            if child.is_dir() and child.name not in expected_skills:
                notices.append(f"skill no declarada en el manifest: {child}")

    if agents_dest.is_dir():
        declared = set(expected_agents.values())
        for child in sorted(agents_dest.iterdir()):
            if child.name in IGNORED_NAMES:
                continue
            if (child.is_file() or child.is_symlink()) and child.name not in declared:
                retired = any(e["platform"] == platform and e["filename"] == child.name for e in retired_agents.load_catalog())
                notices.append(f"agente {'retirado; migración explícita pendiente' if retired else 'no declarado en el manifest'}: {child}")

    if platform == "opencode" and agents_dest.name in {"agent", "agents"}:
        alternate = agents_dest.with_name("agents" if agents_dest.name == "agent" else "agent")
        for entry in retired_agents.load_catalog():
            if entry["platform"] == platform and entry["id"] not in manifest["agents"]:
                child = alternate / entry["filename"]
                if child.exists() or child.is_symlink():
                    notices.append(f"agente retirado; migración explícita pendiente: {child}")

    return problems, notices


def report(problems: list[str], notices: list[str], success: str) -> int:
    for notice in notices:
        print(f"  · {notice}")
    if notices:
        print(
            "  Revisa si son artefactos propios o restos de una versión anterior.\n"
            "  Instalación vigente y migración son estados distintos.\n"
            "  Usa --migrate-retired-agents para la retirada con respaldo verificado."
        )
    if problems:
        print("preflight: instalación incompleta", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print(success)
    return 0


def validate_copy_targets(platform: str, skills_dest: Path, agents_dest: Path) -> None:
    """Read-only check of every generated path wrappers may copy, before writes.

    Inspect actual source trees as some wrappers copy more than manifest entry
    points. Checking directory and file targets also covers nested references.
    """
    for section, destination in (("skills", skills_dest), ("agents", agents_dest)):
        source = GENERATED / platform / section
        retired_agents.safe_directory(source)
        if not source.is_dir():
            raise OSError(f"origen de copia ausente: {source}")
        retired_agents.safe_directory(destination)
        for item in source.rglob("*"):
            retired_agents.safe_path(item)
            target = destination / item.relative_to(source)
            if item.is_dir():
                retired_agents.safe_directory(target)
            else:
                retired_agents.read_regular(item)
                retired_agents.safe_path(target)
                if target.exists() and not target.is_file():
                    raise OSError(f"destino de archivo no regular: {target}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--platform",
        required=True,
        help="Identificador declarado en canonical/manifest.json",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check-source", action="store_true", help="Valida generated/<platform>/")
    mode.add_argument("--check-installed", action="store_true", help="Valida el destino instalado")
    mode.add_argument("--validate-migration", action="store_true", help="Valida argumentos antes de copiar; solo lectura")
    mode.add_argument("--migrate-retired-agents", action="store_true", help="Retirada explícita con respaldo obligatorio")
    parser.add_argument("--migration-requested", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--approve-retired-file", action="append", default=[])
    parser.add_argument("--approve-retired-sha256", action="append", default=[])
    parser.add_argument("--backup-root", type=Path)
    parser.add_argument("--additional-agents-dest", type=Path, action="append", default=[])
    parser.add_argument("--skills-dest", type=Path, help="Destino de skills (--check-installed)")
    parser.add_argument("--agents-dest", type=Path, help="Destino de agentes (--check-installed)")
    args = parser.parse_args(argv)

    if (args.approve_retired_file or args.approve_retired_sha256) and not (args.migrate_retired_agents or args.migration_requested):
        return fail("aprobación requiere --migrate-retired-agents")
    if args.check_installed and (args.migration_requested or args.dry_run or args.approve_retired_file or args.backup_root or args.additional_agents_dest):
        return fail("--check-installed es solo lectura; no acepta opciones de migración")
    if args.migration_requested and not args.validate_migration:
        return fail("--migration-requested solo es válido en --validate-migration")
    if args.additional_agents_dest and not (args.migrate_retired_agents or args.migration_requested):
        return fail("destinos adicionales requieren migración explícita")
    if args.check_source and (args.dry_run or args.approve_retired_file or args.backup_root):
        return fail("--check-source no acepta opciones de migración")

    try:
        manifest = load_manifest()
    except (OSError, ValueError) as error:
        return report([str(error)], [], "")

    if args.platform not in manifest.get("platforms", []):
        declared = ", ".join(manifest.get("platforms", [])) or "(ninguna)"
        return fail(f"plataforma desconocida {args.platform!r}; declaradas: {declared}")

    try:
        retired_agents.load_catalog()
    except (OSError, ValueError) as error:
        return report([str(error)], [], "")

    try:
        if args.validate_migration or args.migrate_retired_agents:
            if not args.agents_dest:
                return fail("migración requiere --agents-dest")
            destinations = [args.agents_dest, *args.additional_agents_dest]
            if args.platform == "opencode" and args.agents_dest.name in {"agent", "agents"}:
                destinations.append(args.agents_dest.with_name("agents" if args.agents_dest.name == "agent" else "agent"))
            destinations = list(dict.fromkeys(destinations))
            try:
                approvals = retired_agents.approvals_from_args(args.approve_retired_file, args.approve_retired_sha256, destinations, args.platform)
            except ValueError as error:
                return fail(str(error))
            if args.validate_migration:
                if args.migration_requested:
                    if not args.skills_dest:
                        return fail("validación de migración requiere --skills-dest")
                    validate_copy_targets(args.platform, args.skills_dest, args.agents_dest)
                    for destination in destinations:
                        retired_agents.safe_directory(destination)
                    retired_agents.validate_backup(args.backup_root or Path.home() / ".ai-agents-kit-retired-backups", destinations)
                return 0
            backup_root = args.backup_root or Path.home() / ".ai-agents-kit-retired-backups"
            if not args.dry_run:
                if not args.skills_dest:
                    return fail("migración requiere --skills-dest")
                problems, notices = check_installed(args.platform, manifest, args.skills_dest, args.agents_dest)
                # Verify bytes, not merely presence, before retiring anything.
                sources = [(GENERATED / args.platform / "agents" / name, args.agents_dest / name) for name in agent_filenames(args.platform, manifest["agents"]).values()]
                for skill in manifest["skills"]:
                    root = GENERATED / args.platform / "skills" / skill
                    canonical = CANONICAL / "skills" / skill
                    sources.extend((root / src.relative_to(canonical), args.skills_dest / skill / src.relative_to(canonical)) for src in canonical.rglob("*") if src.is_file())
                for source, target in sources:
                    try:
                        if retired_agents.read_regular(source)[0] != retired_agents.read_regular(target)[0]:
                            problems.append(f"contenido vigente no coincide: {target}")
                    except OSError as error:
                        problems.append(str(error))
                if problems:
                    return report(problems, notices, "")
            active_retired = retired_agents.IDS & set(manifest["agents"])
            if active_retired:
                return report([f"catálogo vigente todavía declara retirados: {sorted(active_retired)}"], [], "")
            return retired_agents.migrate(args.platform, destinations, backup_root, approvals=approvals, dry_run=args.dry_run)
        if args.check_source:
            problems = check_source(args.platform, manifest)
            return report(
                problems,
                [],
                f"preflight: generated/{args.platform}/ completo "
                f"({len(manifest['skills'])} skills, {len(manifest['agents'])} agentes).",
            )

        if not args.skills_dest or not args.agents_dest:
            return fail("--check-installed requiere --skills-dest y --agents-dest")
        problems, notices = check_installed(
            args.platform, manifest, args.skills_dest, args.agents_dest
        )
        return report(
            problems,
            notices,
            f"Verificado: {len(manifest['skills'])} skills y "
            f"{len(manifest['agents'])} agentes instalados.",
        )
    except (OSError, ValueError) as error:
        return report([str(error)], [], "")


if __name__ == "__main__":
    raise SystemExit(main())
