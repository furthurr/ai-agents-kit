#!/usr/bin/env python3
"""Contract tests for adaptive testing in the canonical SDD prompts."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SDD = ROOT / "canonical" / "skills" / "sdd-spec"

PASSED = 0
FAILED = 0


def check(condition: bool, message: str) -> None:
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print(f"  PASS {message}")
    else:
        FAILED += 1
        print(f"  FAIL {message}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_modes_remain_proportional() -> None:
    skill = read(SDD / "SKILL.md")
    check("| `direct` | Cambio trivial verificable" in skill, "direct conserva criterio verificable")
    check("| `standard` | **Default**" in skill, "standard sigue siendo el modo default")
    check("`deep` no activa TDD estricto" in skill, "deep y TDD estricto permanecen independientes")
    check("sin contrato público" in skill and "cruce de capas" in skill, "direct declara límites de riesgo")


def test_adaptive_testing_selection() -> None:
    testing = read(SDD / "references" / "testing.md")
    for strategy in (
        "Sin test nuevo",
        "Caracterización / regresión",
        "TDD focalizado",
        "TDD estricto",
    ):
        check(strategy in testing, f"testing declara estrategia: {strategy}")
    check("Default para comportamiento nuevo o modificado" in testing, "feature normal selecciona TDD focalizado")
    check("Solo si el usuario lo solicita" in testing, "TDD estricto permanece opt-in")
    check("no evidencia TDD" in testing, "un test retroactivo no se presenta como TDD")


def test_variants_and_evidence() -> None:
    skill = read(SDD / "SKILL.md")
    templates = read(SDD / "references" / "templates.md")
    integrity = read(SDD / "references" / "integrity-gate.md")

    bugfix = skill.split("## Variante Bugfix", maxsplit=1)[1].split("## Variante Quick Plan", maxsplit=1)[0]
    quick_plan = skill.split("## Variante Quick Plan", maxsplit=1)[1].split("## Reglas de calidad", maxsplit=1)[0]

    check("regresión que falle" in bugfix, "bugfix exige regresión antes del fix")
    check("sin gates" in quick_plan and "Omite Fase 4" in quick_plan, "Quick Plan conserva su contrato ligero")
    check("RED del comportamiento → GREEN mínimo → REFACTOR" in templates, "tasks enseña orden test-first")
    check("RED o baseline" in templates and "GREEN / suite" in templates, "verification registra el ciclo")
    check("evidencia del RED esperado y del GREEN" in integrity, "integrity gate exige evidencia TDD")


def test_generated_references_match_canonical() -> None:
    references = (SDD / "references").glob("*.md")
    for canonical in sorted(references):
        expected = canonical.read_bytes()
        for platform in ("copilot", "opencode", "kiro"):
            generated = ROOT / "generated" / platform / "skills" / "sdd-spec" / "references" / canonical.name
            check(generated.is_file(), f"{platform} genera {canonical.name}")
            if generated.is_file():
                check(generated.read_bytes() == expected, f"{platform}/{canonical.name} coincide con canonical")


def main() -> int:
    print("Contrato SDD — testing adaptativo")
    test_modes_remain_proportional()
    test_adaptive_testing_selection()
    test_variants_and_evidence()
    test_generated_references_match_canonical()
    total = PASSED + FAILED
    print(f"{PASSED}/{total} comprobaciones correctas")
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
