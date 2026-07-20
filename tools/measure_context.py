#!/usr/bin/env python3
"""Report the prompt context loaded by default versus on-demand references."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def words(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").split())


def main() -> None:
    agents = list((ROOT / "canonical" / "agents").glob("*.md"))
    skills = list((ROOT / "canonical" / "skills").glob("*/SKILL.md"))
    references = list((ROOT / "canonical" / "skills").glob("*/references/*.md"))
    print(f"Agentes cargados: {sum(words(path) for path in agents):,} palabras ({len(agents)} archivos)")
    print(f"Skills cargadas: {sum(words(path) for path in skills):,} palabras ({len(skills)} archivos)")
    print(f"Referencias bajo demanda: {sum(words(path) for path in references):,} palabras ({len(references)} archivos)")


if __name__ == "__main__":
    main()
