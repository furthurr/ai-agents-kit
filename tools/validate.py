#!/usr/bin/env python3
"""Validate canonical definitions, adapters, and reproducible generated artifacts.

This validation is **non-destructive**: it renders into a temporary directory and
compares hashes against ``generated/`` without renaming or deleting it. An
interruption never alters ``generated/``.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

import render as render_module

ROOT = Path(__file__).resolve().parent.parent
PLATFORM_MARKERS = ("GitHub Copilot", "opencode", ".github/copilot-instructions.md", "VS Code")


def digest_tree(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    return {
        str(file.relative_to(path)): hashlib.sha256(file.read_bytes()).hexdigest()
        for file in sorted(path.rglob("*"))
        if file.is_file()
    }


def _safe_filename(filename: object) -> bool:
    if not filename or not isinstance(filename, str):
        return False
    candidate = Path(filename)
    if candidate.is_absolute() or ".." in candidate.parts:
        return False
    if filename.startswith(("/", "\\")):
        return False
    return True


def validate_manifest(manifest: dict, errors: list[str]) -> None:
    for key in ("skills", "agents", "platforms"):
        value = manifest.get(key)
        if not isinstance(value, list) or not value:
            errors.append(f"manifest.json: '{key}' debe ser una lista no vacía")
            continue
        if not all(isinstance(item, str) and item for item in value):
            errors.append(f"manifest.json: '{key}' contiene entradas no válidas")
        if len(set(value)) != len(value):
            duplicates = sorted({item for item in value if value.count(item) > 1})
            errors.append(f"manifest.json: '{key}' tiene IDs duplicados: {', '.join(duplicates)}")


def validate_adapters(manifest: dict, errors: list[str]) -> dict[str, set[str]]:
    platform_substitutions: dict[str, set[str]] = {}
    for platform in manifest.get("platforms", []):
        platform_dir = ROOT / "adapters" / platform
        platform_json = platform_dir / "platform.json"
        if not platform_json.is_file():
            errors.append(f"Falta el adaptador de plataforma: {platform}")
            continue
        try:
            config = json.loads(platform_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"platform.json inválido para {platform}: {exc}")
            continue
        substitutions = config.get("substitutions", {})
        if not isinstance(substitutions, dict):
            errors.append(f"platform.json de {platform}: 'substitutions' debe ser un objeto")
            substitutions = {}
        platform_substitutions[platform] = set(substitutions)

        for skill_id in manifest.get("skills", []):
            if not (ROOT / "canonical" / "skills" / skill_id / "SKILL.md").is_file():
                errors.append(f"Falta la skill canónica: {skill_id}")

        seen_filenames: dict[str, str] = {}
        for agent_id in manifest.get("agents", []):
            if not (ROOT / "canonical" / "agents" / f"{agent_id}.md").is_file():
                errors.append(f"Falta el agente canónico: {agent_id}")
            adapter = platform_dir / "agents" / f"{agent_id}.json"
            if not adapter.is_file():
                errors.append(f"Falta el adaptador {platform} del agente {agent_id}")
                continue
            try:
                data = json.loads(adapter.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"Adaptador inválido {adapter.relative_to(ROOT)}: {exc}")
                continue
            filename = data.get("filename")
            frontmatter = data.get("frontmatter")
            if not filename or not frontmatter:
                errors.append(f"Adaptador incompleto: {adapter.relative_to(ROOT)}")
                continue
            if not isinstance(frontmatter, dict):
                errors.append(f"Adaptador {adapter.relative_to(ROOT)}: 'frontmatter' debe ser un objeto")
            if not _safe_filename(filename):
                errors.append(f"Adaptador {adapter.relative_to(ROOT)}: filename inseguro {filename!r}")
                continue
            if filename in seen_filenames:
                errors.append(
                    f"Colisión de filename en {platform}: {filename!r} usado por "
                    f"{seen_filenames[filename]} y {agent_id}"
                )
            else:
                seen_filenames[filename] = agent_id
    return platform_substitutions


def validate_orphans(manifest: dict, errors: list[str]) -> None:
    """Detect canonical or generated entries not declared in the manifest."""
    declared_skills = set(manifest.get("skills", []))
    declared_agents = set(manifest.get("agents", []))
    declared_platforms = set(manifest.get("platforms", []))

    skills_dir = ROOT / "canonical" / "skills"
    if skills_dir.is_dir():
        for child in sorted(skills_dir.iterdir()):
            if child.is_dir() and child.name not in declared_skills:
                errors.append(f"Skill canónica huérfana (no en manifest): {child.name}")

    agents_dir = ROOT / "canonical" / "agents"
    if agents_dir.is_dir():
        for child in sorted(agents_dir.glob("*.md")):
            if child.stem not in declared_agents:
                errors.append(f"Agente canónico huérfano (no en manifest): {child.stem}")

    generated_dir = ROOT / "generated"
    if generated_dir.is_dir():
        for child in sorted(generated_dir.iterdir()):
            if child.is_dir() and child.name not in declared_platforms:
                errors.append(f"Plataforma generada huérfana (no en manifest): {child.name}")


def validate_markers(manifest: dict, platform_substitutions: dict[str, set[str]], errors: list[str]) -> None:
    canonical_files = (
        list((ROOT / "canonical" / "agents").glob("*.md"))
        + list((ROOT / "canonical" / "skills").glob("*/SKILL.md"))
    )
    used_tokens: set[str] = set()
    for path in canonical_files:
        content = path.read_text(encoding="utf-8")
        for marker in PLATFORM_MARKERS:
            if marker.lower() in content.lower():
                errors.append(f"Referencia específica de plataforma en {path.relative_to(ROOT)}: {marker}")
        tokens = set(re.findall(r"\{\{[^{}]+\}\}", content))
        used_tokens |= tokens
        for platform, substitutions in platform_substitutions.items():
            missing = tokens - substitutions
            if missing:
                errors.append(
                    f"Tokens sin adaptador para {platform} en {path.relative_to(ROOT)}: "
                    f"{', '.join(sorted(missing))}"
                )

    # Substitutions declared but never used anywhere in canonical. Without this
    # check dead configuration passes CI and drifts from the prompts it claims to
    # adapt.
    for platform, substitutions in platform_substitutions.items():
        unused = substitutions - used_tokens
        if unused:
            errors.append(
                f"Sustituciones declaradas y no usadas en adapters/{platform}/platform.json: "
                f"{', '.join(sorted(unused))}"
            )

    # render.py only substitutes SKILL.md, so a token inside references/ would be
    # copied verbatim and reach the model unresolved.
    for path in sorted((ROOT / "canonical" / "skills").rglob("*")):
        if not path.is_file() or path.name == "SKILL.md":
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        stray = set(re.findall(r"\{\{[^{}]+\}\}", content))
        if stray:
            errors.append(
                f"Token sin sustituir fuera de SKILL.md en {path.relative_to(ROOT)}: "
                f"{', '.join(sorted(stray))} (render.py no sustituye en references/)"
            )


def validate_reproducibility(manifest: dict, errors: list[str]) -> None:
    """Render into a temporary directory and compare hashes without touching generated/."""
    before = {
        platform: digest_tree(ROOT / "generated" / platform)
        for platform in manifest["platforms"]
    }
    with tempfile.TemporaryDirectory() as temporary:
        temp_root = Path(temporary)
        render_module.render(temp_root)
        after = {
            platform: digest_tree(temp_root / platform)
            for platform in manifest["platforms"]
        }
    if before != after:
        errors.append(
            "Los artefactos generados no coinciden con la fuente canónica. Ejecuta tools/render.py."
        )


def main() -> int:
    manifest = json.loads((ROOT / "canonical" / "manifest.json").read_text(encoding="utf-8"))
    errors: list[str] = []

    validate_manifest(manifest, errors)
    platform_substitutions = validate_adapters(manifest, errors)
    validate_orphans(manifest, errors)
    validate_markers(manifest, platform_substitutions, errors)

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    try:
        validate_reproducibility(manifest, errors)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"Fallo al renderizar para validación: {exc}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(
        f"Validación correcta: {len(manifest['skills'])} skills y "
        f"{len(manifest['agents'])} agentes en {len(manifest['platforms'])} plataformas."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
