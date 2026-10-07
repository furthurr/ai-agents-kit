#!/usr/bin/env python3
"""Contract tests for model-level recommendations across canonical agents."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SPECIALISTS = ("architecture", "code-quality", "data-api", "security", "ui-design")

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


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().split()).lower()


def section(text: str, heading: str) -> str:
    """Select a heading and its body without borrowing rules from another section."""
    match = re.search(rf"^## (?:{heading})[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S | re.I)
    return match.group(0) if match else ""


def check_continuity(text: str, label: str, *, positive: bool = True) -> None:
    compact = normalized(text)
    if positive:
        check(bool(re.search(r"mismo turno|continua\w*[^.]*sin (?:esperar|pausa)|sin (?:espera|pausa)[^.]*continua", compact)),
              f"{label}: continúa trabajo autorizado tras el aviso")
    # Scoped to model sections: approval of a real gate may still end a turn.
    obsolete = (
        r"hard stop", r"(?<!sin )(?<!no )\btermina(?:n|r)? el turno", r"(?<!no )\btermina el .*? turno",
        r"(?:responde|indica|espera) [^.]{0,100}(?:continua|listo)",
        r"reanuda cuando el usuario", r"prohibido inspeccionar el proyecto",
        r"(?:nivel ya confirmado|salvo (?:esa )?confirmacion previa|usuario (?:lo confirmo|reanudo))",
        r"detente de nuevo solo si cambia el nivel", r"puntual[^.]*pausa",
        r"continua solo si el usuario responde", r"reanudar con [^.]*continua",
        r"tras la reanudacion", r"confirmacion del gate 0 satisface",
    )
    for pattern in obsolete:
        check(not re.search(pattern, compact), f"{label}: sin mandato antiguo /{pattern}/")


def test_specialist_contracts() -> None:
    for specialist in SPECIALISTS:
        agent_id = ("documentation-orchestrator" if specialist == "architecture" else
                    "code-review" if specialist in ("code-quality", "security") else specialist)
        agent = read(ROOT / "canonical" / "agents" / f"{agent_id}.md")
        skill_dir = ROOT / "canonical" / "skills" / specialist
        skill = read(skill_dir / "SKILL.md")
        reference_path = skill_dir / "references" / "model-selection.md"
        check(reference_path.is_file(), f"{specialist}: incluye matriz bajo demanda")
        reference = read(reference_path) if reference_path.is_file() else ""
        compact = normalized(reference)

        for kind, text in (("agente", agent), ("skill", skill)):
            preflight = section(text, r"Preflight informativo")
            check(bool(preflight), f"{specialist}/{kind}: preflight informativo explícito")
            # Fall back only to diagnose the old section during RED, not to accept it.
            check_continuity(preflight or section(text, r"Gate obligatorio de modelo|Aviso de modelo"),
                             f"{specialist}/{kind}/preflight")
            check("nivel recomendado" in normalized(text), f"{specialist}/{kind}: recomendación visible")
        execution = section(agent, r"Ejecución mínima")
        if execution:
            check(not re.search(r"puntual[^.]*pausa|termina el turno", normalized(execution)),
                  f"{specialist}/agente/ejecución: sin pausa puntual contradictoria")
        check("model-selection.md" in skill, f"{specialist}: skill enlaza la matriz")
        check(
            "nunca nombres modelos/proveedores ni cambies el modelo del host" in normalized(skill),
            f"{specialist}: la regla puntual permanece genérica y manual",
        )
        check(
            all(level in reference for level in ("`BAJO`", "`MEDIO`", "`ALTO`")),
            f"{specialist}: usa los tres niveles genéricos",
        )
        check_continuity(reference, f"{specialist}/referencia")
        check("| si |" not in compact, f"{specialist}: matriz no exige pausa por nivel")
        check(
            "no menciones nombres de modelos, proveedores" in compact,
            f"{specialist}: permanece agnóstico de proveedor",
        )
        check(
            "documentation orchestrator" in compact and "no repitas el aviso" in compact
            and bool(re.search(r"(?:comunico|comunicado|mostro|recomendo)", compact)),
            f"{specialist}: deduplica por comunicación orquestada",
        )
        check(
            "nunca selecciones ni cambies el modelo del host" in compact,
            f"{specialist}: no cambia el modelo del host",
        )
        check(len(reference.split()) <= 230, f"{specialist}: referencia respeta presupuesto")


def test_existing_agents_and_git_exception() -> None:
    markers = {
        "documentation-orchestrator": "Preflight informativo",
        "sdd": "Gate 0 de `sdd-spec`",
    }
    for agent_id, marker in markers.items():
        agent = read(ROOT / "canonical" / "agents" / f"{agent_id}.md")
        check(normalized(marker) in normalized(agent) or
              (agent_id == "sdd" and "preflight" in normalized(agent)),
              f"{agent_id}: conserva recomendación existente")
        if agent_id != "sdd":
            check_continuity(section(agent, r"Ejecuci[oó]n m[ií]nima"),
                             f"{agent_id}/agente/modelo")
            check_continuity(section(agent, r"Alcance inviolable"),
                             f"{agent_id}/agente/alcance", positive=False)

    workflows = read(ROOT / "canonical" / "skills" / "documentation-orchestrator" / "references" / "workflows.md")
    check_continuity(section(workflows, r"Nivel de modelo"), "orquestador/workflows/modelo")
    orch_skill = read(ROOT / "canonical" / "skills" / "documentation-orchestrator" / "SKILL.md")
    check_continuity(section(orch_skill, r"Preflight informativo|Gate 0[^\n]*"), "orquestador/skill/preflight")
    navigator = read(ROOT / "canonical" / "skills" / "project-navigator" / "references" / "bootstrap.md")
    check_continuity(section(navigator, r"Avisos de modelo[^\n]*"), "Navigator/bootstrap/modelo")
    navigator_after = normalized(navigator).split("**despues:**", maxsplit=1)
    check(len(navigator_after) == 2 and "ya puedes cambiar manualmente" in navigator_after[1]
          and "termina el turno" not in navigator_after[1].split("## bootstrap asistido", maxsplit=1)[0],
          "Navigator conserva aviso final no bloqueante")
    navigator_skill = read(ROOT / "canonical" / "skills" / "project-navigator" / "SKILL.md")
    check_continuity(section(navigator_skill, r"Flujo obligatorio al recibir una petición"), "Navigator/skill/flujo")
    check_continuity(section(navigator_skill, r"Bootstrap y update"), "Navigator/skill/bootstrap", positive=False)

    git_agent = read(ROOT / "canonical" / "agents" / "git-release-manager.md")
    check(
        "model-selection.md" not in git_agent and "gate 0 de modelo" not in normalized(git_agent),
        "git-release-manager: no añade un gate de modelo innecesario",
    )


def test_generated_parity() -> None:
    manifest = json.loads((ROOT / "canonical" / "manifest.json").read_text(encoding="utf-8"))
    for platform in manifest["platforms"]:
        for specialist in SPECIALISTS:
            canonical_reference = (
                ROOT / "canonical" / "skills" / specialist / "references" / "model-selection.md"
            )
            generated_reference = (
                ROOT / "generated" / platform / "skills" / specialist / "references" / "model-selection.md"
            )
            check(generated_reference.is_file(), f"{platform}/{specialist}: genera la matriz")
            if generated_reference.is_file():
                check(
                    generated_reference.read_bytes() == canonical_reference.read_bytes(),
                    f"{platform}/{specialist}: matriz coincide con canonical",
                )


def main() -> int:
    print("Contrato de recomendación de modelo — cobertura, coste y paridad")
    test_specialist_contracts()
    test_existing_agents_and_git_exception()
    test_generated_parity()
    total = PASSED + FAILED
    print(f"{PASSED}/{total} comprobaciones correctas")
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
