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
            if child.is_file() and child.name not in declared:
                notices.append(f"agente no declarado en el manifest: {child}")

    return problems, notices


def report(problems: list[str], notices: list[str], success: str) -> int:
    for notice in notices:
        print(f"  · {notice}")
    if notices:
        print(
            "  Revisa si son artefactos propios o restos de una versión anterior.\n"
            "  El instalador nunca los borra; retíralos a mano si ya no aplican."
        )
    if problems:
        print("preflight: instalación incompleta", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print(success)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", required=True, help="copilot | opencode | kiro")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check-source", action="store_true", help="Valida generated/<platform>/")
    mode.add_argument("--check-installed", action="store_true", help="Valida el destino instalado")
    parser.add_argument("--skills-dest", type=Path, help="Destino de skills (--check-installed)")
    parser.add_argument("--agents-dest", type=Path, help="Destino de agentes (--check-installed)")
    args = parser.parse_args(argv)

    try:
        manifest = load_manifest()
    except (OSError, ValueError) as error:
        return fail(str(error))

    if args.platform not in manifest.get("platforms", []):
        declared = ", ".join(manifest.get("platforms", [])) or "(ninguna)"
        return fail(f"plataforma desconocida {args.platform!r}; declaradas: {declared}")

    try:
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
        return fail(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
