#!/usr/bin/env python3
"""Contract tests for SDD and its integration with specialist agents."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SDD = ROOT / "canonical" / "skills" / "sdd-spec"
SDD_AGENT = ROOT / "canonical" / "agents" / "sdd.md"
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
    return " ".join(text.split())


def section(text: str, heading: str) -> str:
    match = re.search(rf"^## (?:{heading})[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S | re.I)
    return match.group(0) if match else ""


def check_nonblocking(text: str, label: str) -> None:
    compact = normalized(text).lower()
    check(bool(re.search(r"mismo turno|contin[uú]a\w*[^.]*sin (?:esperar|pausa)|sin (?:espera|pausa)[^.]*contin[uú]a", compact)),
          f"{label}: continuidad explícita del trabajo autorizado")
    for pattern in (
        r"termina(?:n)? el turno (?:tras el preflight|antes de|para permitir)",
        r"verification y termina el turno", r"termina el turno\. cuando el usuario",
        r"(?:responde|indica) [^.]{0,100}contin[uú]a",
        r"reanuda cuando el usuario", r"pausa si no hay gate",
        r"gate 0 inicial pausa", r"suite cuando el usuario indique continuar",
        r"termina el turno tras el aviso", r"si cambia la recomendación[^.]*termina el",
        r"ejecuta verification solo cuando el usuario reanude",
    ):
        check(not re.search(r"(?<!no )(?<!sin )\b" + pattern, compact),
              f"{label}: sin pausa de modelo /{pattern}/")


def test_modes_remain_proportional() -> None:
    skill = read(SDD / "SKILL.md")
    agent = read(SDD_AGENT)
    compact = normalized(skill + " " + agent).lower()
    check("| `direct` | Cambio trivial verificable" in skill, "direct conserva criterio verificable")
    check("| `lite` |" in skill, "lite existe como profundidad intermedia")
    check("| `standard` | **Default**" in skill, "standard sigue siendo el modo default")
    check("`deep` y tdd estricto" in compact and "opciones retiradas" in compact,
          "deep y TDD estricto están retirados")
    check("sin contrato público" in skill and "cruce de capas" in skill, "direct declara límites de riesgo")
    check(
        "exactamente tres profundidades" in compact
        and all(mode in skill for mode in ("`direct`", "`lite`", "`standard`")),
        "SDD declara exactamente tres profundidades",
    )
    check(
        "tipo de trabajo" in compact
        and "intención" in compact
        and "estrategia de pruebas" in compact,
        "tipo, profundidad, intención y testing permanecen separados",
    )
    check(
        "si la elegibilidad de `lite` no puede demostrarse" in compact
        and "`standard`" in compact,
        "la incertidumbre sobre lite cae en standard",
    )
    check(
        "solicitud explícita de `standard`" in compact and "no se rebaja" in compact,
        "standard explícito no se rebaja automáticamente",
    )
    check(
        "espera aceptación" in compact and "no convierte la solicitud silenciosamente" in compact,
        "las opciones retiradas requieren aceptación explícita",
    )


def test_lite_quick_plan_contract() -> None:
    skill = read(SDD / "SKILL.md")
    agent = read(SDD_AGENT)
    model = read(SDD / "references" / "model-selection.md")
    templates = read(SDD / "references" / "templates.md")
    integrity = read(SDD / "references" / "integrity-gate.md")
    quality = read(SDD / "references" / "quality-bar.md")
    compact = normalized(" ".join((skill, agent, model))).lower()

    check(
        "quick plan" in compact and "obligatorio y exclusivo" in compact,
        "Quick Plan es obligatorio y exclusivo de lite",
    )
    check(
        all(combo in compact for combo in ("`direct` + quick plan", "`standard` + quick plan")),
        "Quick Plan rechaza combinaciones con otros modos",
    )
    check(
        "solo planificación" in compact and "no implementar" in compact,
        "lite distingue planificar de implementar",
    )
    check(
        "sin gates 1–3" in compact and "sin gate 4" in compact,
        "lite omite únicamente sus gates de fase definidos",
    )
    check(
        "aunque el nivel de modelo" in compact and "no cambie" in compact,
        "reclasificar lite a standard requiere confirmación de flujo",
    )
    check(
        "Modo SDD: lite" in templates and "verification.md (lite)" in templates,
        "las plantillas distinguen y verifican specs lite",
    )
    check(
        "cierre `lite`" in integrity.lower() and "verification.md" in integrity,
        "integrity gate exige evidencia durable para lite",
    )
    check(
        "Lite" in quality and "RNF declarados" in quality,
        "quality bar mantiene el cierre lite proporcional",
    )

    manifest = json.loads((ROOT / "canonical" / "manifest.json").read_text(encoding="utf-8"))
    for platform in manifest["platforms"]:
        adapter = json.loads(
            (ROOT / "adapters" / platform / "agents" / "sdd.json").read_text(encoding="utf-8")
        )
        description = adapter["frontmatter"]["description"].lower()
        check(
            all(term in description for term in ("direct", "lite", "standard", "quick plan"))
            and "deep" not in description
            and "estricto" not in description,
            f"{platform}: descripción expone modos vigentes y Quick Plan",
        )


def test_model_selection_gate() -> None:
    skill = read(SDD / "SKILL.md")
    agent = read(SDD_AGENT)
    reference_path = SDD / "references" / "model-selection.md"
    check(reference_path.is_file(), "SDD incluye selección de modelo bajo demanda")
    reference = read(reference_path) if reference_path.is_file() else ""
    normalized_reference = normalized(reference)
    lower_reference = normalized_reference.lower()

    check("model-selection.md" in skill, "la skill carga el contrato de modelo")
    check("model-selection.md" in agent, "el agente delega la selección a la skill")
    check(
        "si la solicitud cumple claramente `direct`" in normalized(skill).lower()
        and "no cargues la referencia" in normalized(skill).lower(),
        "direct evita cargar la referencia detallada",
    )
    check(
        all(level in reference for level in ("`BAJO`", "`MEDIO`", "`ALTO`")),
        "el contrato declara los tres niveles genéricos",
    )
    check(len(reference.split()) <= 450, "la referencia de modelo respeta el presupuesto de contexto")
    check(
        "no menciones modelos ni proveedores" in lower_reference,
        "la recomendación permanece agnóstica de modelos y proveedores",
    )
    check(
        "preflight debe ser barato" in lower_reference
        and "no puede escribir, ejecutar tests, cargar referencias pesadas" in lower_reference,
        "el preflight no consume trabajo costoso antes del Gate 0",
    )
    check(
        "`direct`: informa" in lower_reference
        and "nivel de llm recomendado" in lower_reference
        and "sin esperar" in lower_reference,
        "direct recibe un aviso no bloqueante",
    )
    check(
        all(mode in lower_reference for mode in ("`lite`", "`standard`", "bugfix"))
        and any("`lite`" in bullet and "`standard`" in bullet
                and bool(re.search(r"sin (?:esperar|pausa)|mismo turno", bullet))
                for bullet in re.split(r"(?m)^- ", reference.lower())),
        "lite, standard y bugfix inician sin espera por modelo",
    )
    check(
        "modo sdd: <direct|lite|standard>" in lower_reference
        and "modo sdd: <direct|lite|standard|deep>" not in lower_reference,
        "la salida de preflight solo admite las tres profundidades",
    )
    check(
        "una sola recomendación visible por fase" in lower_reference
        and "no repitas la misma recomendación" in lower_reference,
        "la recomendación se limita a la próxima fase",
    )
    check(
        "recalcula" in lower_reference
        and "`lite` a `standard`" in lower_reference,
        "el alcance recalcula modelo y los cambios de flujo se confirman",
    )
    check(
        "nivel de llm recomendado para" in lower_reference
        and "no preguntes si el usuario seleccionó o cambiará el llm" in lower_reference,
        "la recomendación identifica el nivel de LLM y es informativa",
    )
    check(
        "ni cambies el modelo del host" in normalized(reference).lower(),
        "SDD/referencia nunca cambia el modelo del host",
    )
    check(
        "sin gates 1–3" in normalized(skill).lower()
        and "preflight informativo" in normalized(skill).lower()
        and bool(re.search(r"sin (?:esperar|pausa)|mismo turno", normalized(skill).lower())),
        "lite conserva el preflight informativo y omite sus gates de fase",
    )
    for label, text in (("agente", agent), ("skill/preflight", section(skill, r"Gate 0[^\n]*|Preflight[^\n]*")),
                        ("referencia/transiciones", section(reference, r"Recomendación informativa y transiciones")),
                        ("referencia/salida", section(reference, r"Salida")),
                        ("skill/flujo", section(skill, r"Flujo con gates")),
                        ("skill/Quick Plan", section(skill, r"Modo lite y Quick Plan")),
                        ("integrity/transición", section(read(SDD / "references" / "integrity-gate.md"), r"Estado de fase y transición"))):
        check_nonblocking(text, f"SDD/{label}")

    flow = normalized(section(skill, r"Flujo con gates")).lower()
    for gate in range(1, 5):
        check(bool(re.search(rf"\*\*gate {gate}\*\*", flow)), f"SDD: conserva Gate {gate} real")
    check("aprobación explícita" in flow and "no avances de fase" in flow,
          "SDD: no cruza gates reales sin aprobación explícita")
    check("preflight" in normalized(agent).lower() and
          bool(re.search(r"(?:no (?:es|crea|representa)|sin)[^.]*gate (?:humano|adicional)|no humano|no bloqueante", normalized(agent).lower())),
          "SDD/agente: Gate 0 identifica preflight no humano")

    manifest = json.loads((ROOT / "canonical" / "manifest.json").read_text(encoding="utf-8"))
    for platform in manifest["platforms"]:
        adapter = json.loads(
            (ROOT / "adapters" / platform / "agents" / "sdd.json").read_text(encoding="utf-8")
        )
        generated_agent = read(ROOT / "generated" / platform / "agents" / adapter["filename"])
        generated_skill = read(ROOT / "generated" / platform / "skills" / "sdd-spec" / "SKILL.md")
        check("model-selection.md" in generated_agent, f"{platform}: agente propaga Gate 0 de modelo")
        check("model-selection.md" in generated_skill, f"{platform}: skill propaga Gate 0 de modelo")


def test_phase_scoped_recommendations() -> None:
    skill = read(SDD / "SKILL.md")
    agent = read(SDD_AGENT)
    model = read(SDD / "references" / "model-selection.md")
    templates = read(SDD / "references" / "templates.md")
    integrity = read(SDD / "references" / "integrity-gate.md")
    compact = normalized(" ".join((skill, agent, model, templates, integrity))).lower()
    templates_lower = templates.lower()
    output_parts = model.split("## Salida", maxsplit=1)
    output = output_parts[1] if len(output_parts) == 2 else ""
    template_parts = output.split("```text", maxsplit=1)
    output_template = template_parts[1].split("```", maxsplit=1)[0] if len(template_parts) == 2 else ""

    check(
        "próximo proceso" in compact
        and "nivel de llm recomendado para" in compact,
        "el preflight recomienda el nivel de la próxima fase",
    )
    check(
        "fases pendientes" not in output.lower()
        and "perfil" not in output.lower(),
        "la salida inicial no muestra el perfil global de fases",
    )
    check(
        "nivel de llm recomendado para" in output_template.lower()
        and "cambiar manualmente" in output_template.lower()
        and "responde" not in output_template.lower()
        and "modelo recomendado" not in output_template.lower(),
        "la plantilla permite cambio manual sin pedir confirmación de modelo",
    )
    check(
        "resumen verificable" in compact
        and "gate actual" in compact
        and "recomendación de la próxima fase" in compact,
        "la transición combina resumen, gate y próxima recomendación",
    )
    check(
        "condicionada a la aprobación actual" in compact
        and "aprobación del gate real de la fase actual" in compact,
        "la próxima recomendación queda condicionada al gate actual",
    )
    check(
        "espera únicamente la aprobación del gate real de la fase actual" in compact
        and "no preguntes si el usuario seleccionó o cambiará el llm" in compact
        and "apruebo y usaré el nivel recomendado" not in compact
        and "apruebo y continúo con el nivel actual" not in compact,
        "la transición espera aprobación de fase, no confirmación del nivel de LLM",
    )
    for label, text in (("agente", agent), ("skill", skill), ("modelo", model), ("integridad", integrity)):
        own = normalized(text).lower()
        check(bool(re.search(r"espera (?:únicamente |solo )?(?:la )?aprobación[^.]*gate|espera[^.]*solo la aprobación[^.]*gate", own)),
              f"SDD/{label}: espera gate real de forma independiente")
        check(not re.search(r"apruebo y usaré el nivel recomendado|apruebo y continúo con el nivel actual", own),
              f"SDD/{label}: aprobación no condicionada al modelo")
    verification = section(skill, r"Flujo con gates").split("### Fase 4", maxsplit=1)
    check_nonblocking(verification[1] if len(verification) == 2 else "", "SDD/skill/Verification")
    check(
        "después de implementación" in normalized(model).lower()
        and "verification" in normalized(model).lower()
        and bool(re.search(r"contin[uú]a[^.]*verification|verification[^.]*sin (?:esperar|pausa)|mismo turno", normalized(model).lower())),
        "Verification continúa sin gate ni espera informativa intermedios",
    )
    check(
        "`direct` recibe un aviso breve y no bloqueante" in normalized(skill).lower()
        and "quick plan" in normalized(skill).lower()
        and bool(re.search(r"mismo turno|contin[uú]a[^.]*sin (?:esperar|pausa)", normalized(section(skill, r"Modo lite y Quick Plan")).lower())),
        "direct y Quick Plan continúan tras el aviso no bloqueante",
    )
    check(
        all(phase in compact for phase in ("requirements", "design", "tasks", "implementación", "verification")),
        "el contrato cubre las cinco fases recomendables",
    )
    check(
        "después de verification" in compact
        and "únicamente gate 4" in compact,
        "el cierre no muestra una recomendación inexistente",
    )
    check(
        "modo sdd: standard" in templates_lower
        and "fase: requirements" in templates_lower
        and "gate 1: pendiente" in templates_lower,
        "las plantillas persisten el estado de fase y gate",
    )
    check(
        "no inferirá aprobación solo por la existencia del archivo" in compact,
        "la reanudación no confunde archivo existente con aprobación",
    )

    manifest = json.loads((ROOT / "canonical" / "manifest.json").read_text(encoding="utf-8"))
    for platform in manifest["platforms"]:
        adapter = json.loads(
            (ROOT / "adapters" / platform / "agents" / "sdd.json").read_text(encoding="utf-8")
        )
        generated_agent = read(ROOT / "generated" / platform / "agents" / adapter["filename"])
        generated_skill = read(ROOT / "generated" / platform / "skills" / "sdd-spec" / "SKILL.md")
        check(
            "próximo proceso" in normalized(generated_agent + generated_skill).lower(),
            f"{platform}: propaga preflight por próxima fase",
        )


def test_spec_paths_support_grouping() -> None:
    skill = read(SDD / "SKILL.md")
    normalized_skill = normalized(skill)

    check("Destino: `.sdd/specs/<ruta-spec>/`" in skill, "la spec usa una ruta relativa extensible")
    check("`<nombre-feature>/`" in skill, "las rutas planas siguen siendo válidas")
    check("`modo-invitado/android-contactos/`" in skill, "el contrato ejemplifica agrupación por módulo")
    check("ruta relativa completa identifica la spec" in normalized_skill,
          "la identidad no depende solo del nombre final")
    check("requirements.md` o `bugfix.md`" in normalized_skill,
          "los marcadores distinguen una spec de un agrupador")
    check("Al crear sin ruta explícita" in skill and "No muevas specs existentes" in normalized_skill,
          "la creación reutiliza módulos sin migrar specs previas")
    check("evita repetir su prefijo" in normalized_skill,
          "las specs agrupadas no duplican el nombre del módulo")
    check("busca recursivamente" in normalized_skill, "la reanudación descubre specs anidadas")
    check("varias candidatas plausibles" in normalized_skill and "pregunta" in normalized_skill,
          "la reanudación ambigua requiere elección del usuario")
    check("no contiene `..`" in normalized_skill and "permanece bajo `.sdd/specs/`" in normalized_skill,
          "las rutas no pueden escapar de .sdd/specs")

    manifest = json.loads((ROOT / "canonical" / "manifest.json").read_text(encoding="utf-8"))
    for platform in manifest["platforms"]:
        generated = read(ROOT / "generated" / platform / "skills" / "sdd-spec" / "SKILL.md")
        check("Destino: `.sdd/specs/<ruta-spec>/`" in generated,
              f"{platform}: propaga soporte de rutas agrupadas")
        check("`modo-invitado/android-contactos/`" in generated,
              f"{platform}: propaga el ejemplo agrupado")


def test_adaptive_testing_selection() -> None:
    testing = read(SDD / "references" / "testing.md")
    check(
        "(`direct`, `lite`, `standard`)" in testing,
        "testing reconoce las tres profundidades SDD",
    )
    for strategy in (
        "Sin test nuevo",
        "Caracterización / regresión",
        "TDD focalizado",
    ):
        check(strategy in testing, f"testing declara estrategia: {strategy}")
    check("Default para comportamiento nuevo o modificado" in testing, "feature normal selecciona TDD focalizado")
    check("Si el usuario pide TDD estricto" in testing and "se retiró" in testing,
          "TDD estricto se rechaza como opción retirada")
    check("no evidencia TDD" in testing, "un test retroactivo no se presenta como TDD")


def test_variants_and_evidence() -> None:
    skill = read(SDD / "SKILL.md")
    templates = read(SDD / "references" / "templates.md")
    integrity = read(SDD / "references" / "integrity-gate.md")

    bugfix_parts = skill.split("## Variante Bugfix", maxsplit=1)
    lite_parts = skill.split("## Modo lite y Quick Plan", maxsplit=1)
    check(len(bugfix_parts) == 2, "la skill conserva la variante Bugfix")
    check(len(lite_parts) == 2, "la skill declara el flujo lite y Quick Plan")
    bugfix = bugfix_parts[1].split("## Modo lite y Quick Plan", maxsplit=1)[0] if len(bugfix_parts) == 2 else ""
    quick_plan = lite_parts[1].split("## Reglas de calidad", maxsplit=1)[0] if len(lite_parts) == 2 else ""

    check("regresión que falle" in bugfix, "bugfix exige regresión antes del fix")
    check(
        "obligatorio y exclusivo" in normalized(quick_plan)
        and "sin Gates 1–3" in normalized(quick_plan),
        "Quick Plan pertenece exclusivamente a lite",
    )
    check(
        "verification.md" in quick_plan and "sin Gate 4" in quick_plan,
        "lite implementado conserva evidencia sin fase de cierre completa",
    )
    check("RED del comportamiento → GREEN mínimo → REFACTOR" in templates, "tasks enseña orden test-first")
    check("RED o baseline" in templates and "GREEN / suite" in templates, "verification registra el ciclo")
    check("evidencia del RED esperado y del GREEN" in integrity, "integrity gate exige evidencia TDD")
    check("TDD estricto" in integrity and "opción retirada" in integrity,
          "integrity gate no acredita TDD estricto")


def test_navigator_context_contract() -> None:
    skill = read(SDD / "SKILL.md")
    agent = read(SDD_AGENT)
    reference_path = SDD / "references" / "navigator-context.md"
    check(reference_path.is_file(), "SDD incluye el contrato de contexto Navigator")
    reference = read(reference_path) if reference_path.is_file() else ""
    normalized_reference = normalized(reference)

    check("navigator-context.md" in skill, "la skill carga el contrato Navigator bajo demanda")
    check("navigator-context.md" in agent, "el agente delega el procedimiento Navigator a la skill")
    check(
        all(state in reference for state in ("`vigente`", "`desfasado`", "`no_verificable`", "`ambiguo`", "`ausente`")),
        "Navigator distingue todos los estados de confianza",
    )
    check(
        "steering" in normalized_reference
        and "Navigator" in normalized_reference
        and "contexto de dominio" in normalized_reference
        and "código puntual" in normalized_reference,
        "el contrato ordena steering, Navigator, dominio y código",
    )
    check(
        "no bloquea SDD" in normalized_reference and "fuentes directas" in normalized_reference,
        "la ausencia o el desfase degradan hacia fuentes directas",
    )
    check(
        "no crea ni actualiza `.navigator/`" in normalized_reference and "aprobación explícita" in normalized_reference,
        "SDD no escribe Navigator sin aprobación explícita",
    )
    check(
        "`source_commit`" in reference and "`generated_at`" in reference,
        "la frescura usa baseline y no depende de la fecha",
    )
    check(
        "fuentes de verdad" in normalized_reference and "pistas de ubicación" in normalized_reference,
        "un índice no confiable solo aporta pistas verificables",
    )

    manifest = json.loads((ROOT / "canonical" / "manifest.json").read_text(encoding="utf-8"))
    for platform in manifest["platforms"]:
        adapter = json.loads(
            (ROOT / "adapters" / platform / "agents" / "sdd.json").read_text(encoding="utf-8")
        )
        generated_agent = read(ROOT / "generated" / platform / "agents" / adapter["filename"])
        generated_skill = read(ROOT / "generated" / platform / "skills" / "sdd-spec" / "SKILL.md")
        check("navigator-context.md" in generated_agent, f"{platform}: agente propaga integración Navigator")
        check("navigator-context.md" in generated_skill, f"{platform}: skill propaga integración Navigator")


def test_specialists_recommend_sdd_without_switching() -> None:
    for specialist in SPECIALISTS:
        agent_id = "code-review" if specialist in ("code-quality", "security") else specialist
        agent = read(ROOT / "canonical" / "agents" / f"{agent_id}.md")
        skill = read(ROOT / "canonical" / "skills" / specialist / "SKILL.md")
        normalized_agent = normalized(agent)
        normalized_skill = normalized(skill)
        check("{{sdd_agent}}" in agent, f"{specialist}: agente puede recomendar SDD")
        check("{{sdd_agent}}" in skill, f"{specialist}: skill define criterio SDD")
        check("cambies de agente" in normalized_agent and "automáticamente" in normalized_agent,
              f"{specialist}: agente no cambia automáticamente")
        check("cambies de agente" in normalized_skill and "automáticamente" in normalized_skill,
              f"{specialist}: skill conserva decisión del usuario")

    quality = read(ROOT / "canonical" / "skills" / "code-quality" / "SKILL.md")
    security = read(ROOT / "canonical" / "skills" / "security" / "SKILL.md")
    check("QLT-NNNN" in quality and "Detente antes de modificar código" in quality,
          "quality entrega referencia y se detiene antes del código")
    check("SEC-NNNN" in security and "Detente antes de modificar código" in security,
          "security entrega referencia y se detiene antes del código")


def test_generated_references_match_canonical() -> None:
    references = (SDD / "references").glob("*.md")
    manifest = json.loads((ROOT / "canonical" / "manifest.json").read_text(encoding="utf-8"))
    for canonical in sorted(references):
        expected = canonical.read_bytes()
        for platform in manifest["platforms"]:
            generated = ROOT / "generated" / platform / "skills" / "sdd-spec" / "references" / canonical.name
            check(generated.is_file(), f"{platform} genera {canonical.name}")
            if generated.is_file():
                check(generated.read_bytes() == expected, f"{platform}/{canonical.name} coincide con canonical")


def main() -> int:
    print("Contrato SDD — modelo, rutas, testing adaptativo, Navigator e integración")
    test_modes_remain_proportional()
    test_lite_quick_plan_contract()
    test_model_selection_gate()
    test_phase_scoped_recommendations()
    test_spec_paths_support_grouping()
    test_adaptive_testing_selection()
    test_variants_and_evidence()
    test_navigator_context_contract()
    test_specialists_recommend_sdd_without_switching()
    test_generated_references_match_canonical()
    total = PASSED + FAILED
    print(f"{PASSED}/{total} comprobaciones correctas")
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
