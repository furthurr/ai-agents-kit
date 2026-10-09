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
    templates = read(SDD / "references" / "templates.md")
    integrity = read(SDD / "references" / "integrity-gate.md")
    quality = read(SDD / "references" / "quality-bar.md")
    compact = normalized(skill).lower()

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


def test_feature_level_contract() -> None:
    skill = read(SDD / "SKILL.md")
    agent = read(SDD_AGENT)
    reference_path = SDD / "references" / "feature-level.md"
    check(not (SDD / "references" / "model-selection.md").exists(),
          "SDD ya no distribuye model-selection.md")
    check(reference_path.is_file(), "SDD incluye la referencia de calificación de feature")
    reference = read(reference_path) if reference_path.is_file() else ""
    compact = normalized(" ".join((skill, agent, reference))).lower()
    lower_reference = normalized(reference).lower()

    check("references/feature-level.md" in skill,
          "la skill carga la referencia de calificación")
    check("references/feature-level.md" in agent,
          "el agente SDD delega la rúbrica a la referencia de la skill")
    check("solo puede emitirla el agente" in normalized(skill).lower()
          and "cargar esta skill desde otro agente no autoriza" in normalized(skill).lower(),
          "la skill no autoriza a agentes consumidores a emitir la calificación")
    check("solo el agente sdd comunica" in lower_reference
          and "no concede permiso para emitirla" in lower_reference,
          "la referencia reserva la emisión al agente SDD")
    check("feature completa" in lower_reference
          and "no tareas/fases" in lower_reference,
          "la calificación mide la feature completa, no fases ni tareas")
    check("analiza primero el alcance deseado y su impacto real" in lower_reference,
          "el alcance e impacto se analizan antes de puntuar")
    check("no muestres puntuación provisional" in lower_reference
          and "no emite notas provisionales" in normalized(agent).lower(),
          "no se emiten puntuaciones provisionales")
    check("esfuerzo previsto del llm: <nota e icono>" in lower_reference,
          "la emisión usa el formato de esfuerzo definido")
    check("1–7 inclusive: 🟢" in reference and "8–9: 🟠" in reference
          and "10: 🔴" in reference,
          "la escala asigna emoji verde, naranja y rojo a los rangos correctos")
    for consumer_name, consumer in (("skill", skill), ("agente", agent)):
        check("Esfuerzo previsto del LLM:" in consumer and "Nivel de feature:" not in consumer,
              f"{consumer_name}: usa la nueva etiqueta, sin salida alternativa antigua")
    for level in range(1, 11):
        check(bool(re.search(rf"\| {level} \|", reference)),
              f"la rúbrica define ancla para el nivel {level}")
    check("no uses 0, decimales, rangos" in lower_reference,
          "la salida excluye valores fuera de escala, decimales y rangos")
    check(all(phrase in lower_reference for phrase in (
        "`direct`, antes de editar",
        "`lite`, al cerrar quick plan",
        "`standard`, con requirements/gate 1",
    )), "cada profundidad emite tras el análisis de alcance que le corresponde")
    check("no repitas el nivel al cambiar de fase" in lower_reference
          and "no emite notas provisionales ni las repite" in normalized(agent).lower(),
          "la calificación no se repite en transiciones")
    check("si cambia materialmente alcance o impacto, analiza primero" in lower_reference
          and "reanaliza cambios materiales de alcance" in normalized(agent).lower(),
          "los cambios materiales de alcance requieren reanálisis antes de actualizar")
    check("bugs, consultas y exploraciones no puntúan como features por defecto" in lower_reference,
          "bugfixes, consultas y exploraciones no se puntúan como features por defecto")
    check("no recomienda niveles de llm ni solicita cambiar o confirmar el modelo" in normalized(agent).lower()
          and "no recomiendes ni menciones modelos/proveedores llm" in normalized(skill).lower()
          and "no repite ni pausa ni pide aprobación de la nota" in normalized(skill).lower()
          and "continúa sin aviso ni espera por modelo" in normalized(agent).lower()
          and "la calificación de feature no es un gate" in normalized(skill).lower(),
          "no hay recomendación LLM ni pausa o gate adicional por modelo")
    check("recomendación de modelo" not in lower_reference
          and "nivel de llm recomendado" not in lower_reference
          and "model-selection.md" not in compact,
          "el contrato de feature no conserva avisos ni selección de modelo")
    templates = read(SDD / "references" / "templates.md")
    check("calificación de feature (solo si sdd analizó una feature)" in templates.lower()
          and "1–10 o 10+" in templates.lower()
          and all(field in templates for field in (
              "Esfuerzo previsto del LLM:", "Referente del laboratorio:",
              "Justificación:", "Supuestos relevantes:",
          ))
          and "no emitir antes de definir alcance" in templates.lower(),
          "la plantilla standard registra calificación real solo tras definir alcance")
    check("calificación de feature (añadir solo tras análisis completo)" in templates.lower()
          and "1–10 o 10+" in templates.lower(),
          "la plantilla lite reserva la calificación al cierre del análisis")
    integrity = normalized(read(SDD / "references" / "integrity-gate.md")).lower()
    check("no crea un gate nuevo" in integrity
          and "espera solo la aprobación del gate sdd real" in integrity,
          "integrity mantiene gates reales y no introduce uno por la calificación")
    check("modo sdd: standard" in templates.lower()
          and "fase: requirements" in templates.lower()
          and "gate 1: pendiente" in templates.lower()
          and "no inferirá aprobación solo por la existencia del archivo" in integrity,
          "plantillas y reanudación conservan fase y aprobación explícita")

    flow = normalized(section(skill, r"Flujo con gates")).lower()
    for gate in range(1, 5):
        check(bool(re.search(rf"\*\*gate {gate}\*\*", flow)), f"SDD: conserva Gate {gate} real")
    check("aprobación explícita" in flow and "no avances de fase" in flow,
          "SDD: no cruza gates reales sin aprobación explícita")
    check("preflight técnico" in normalized(agent).lower()
          and "no recomienda niveles de llm" in normalized(agent).lower(),
          "SDD/agente: conserva el preflight técnico, sin pausa de modelo")

    for specialist in SPECIALISTS:
        agent_id = ("documentation-orchestrator" if specialist == "architecture" else
                    "code-review" if specialist in ("code-quality", "security") else specialist)
        specialist_agent = read(ROOT / "canonical" / "agents" / f"{agent_id}.md")
        specialist_skill = read(ROOT / "canonical" / "skills" / specialist / "SKILL.md")
        specialist_text = normalized(specialist_agent + " " + specialist_skill).lower()
        check("nivel de feature:" not in specialist_text
              and "references/feature-level.md" not in specialist_text,
              f"{specialist}: no reclama emisión de calificación ni carga su rúbrica")
        check("cargar esta skill desde otro agente no autoriza" in normalized(skill).lower()
              and "no concede permiso para emitirla" in lower_reference,
              f"{specialist}: cargar sdd-spec no le concede autorización para emitir")

    manifest = json.loads((ROOT / "canonical" / "manifest.json").read_text(encoding="utf-8"))
    for platform in manifest["platforms"]:
        adapter = json.loads(
            (ROOT / "adapters" / platform / "agents" / "sdd.json").read_text(encoding="utf-8")
        )
        generated_agent = read(ROOT / "generated" / platform / "agents" / adapter["filename"])
        generated_skill = read(ROOT / "generated" / platform / "skills" / "sdd-spec" / "SKILL.md")
        generated_templates = read(ROOT / "generated" / platform / "skills" / "sdd-spec"
                                   / "references" / "templates.md")
        check(all("Esfuerzo previsto del LLM:" in consumer and "Nivel de feature:" not in consumer
                  for consumer in (generated_agent, generated_skill, generated_templates)),
              f"{platform}: agente, skill y plantillas adoptan salida de esfuerzo")
        check("references/feature-level.md" in generated_skill,
              f"{platform}: skill generada carga la rúbrica de feature")
        check("model-selection.md" not in generated_agent + generated_skill,
              f"{platform}: generated no conserva contrato de modelo retirado")
        generated_reference = (ROOT / "generated" / platform / "skills" / "sdd-spec"
                               / "references" / "feature-level.md")
        check(generated_reference.is_file(),
              f"{platform}: referencia feature-level se distribuye dentro de la skill")
        if generated_reference.is_file():
            check(generated_reference.read_bytes() == reference_path.read_bytes(),
                  f"{platform}: referencia de calificación coincide con canonical")
        check(not (ROOT / "generated" / platform / "agents" / "references"
                   / "feature-level.md").exists(),
              f"{platform}: referencia feature-level no se instala junto al agente")


def table_rows(text: str, heading: str) -> dict[str, list[str]]:
    """Inspect a normative Markdown table; this is not a feature scorer."""
    rows: dict[str, list[str]] = {}
    for line in section(text, re.escape(heading)).splitlines():
        if line.startswith("| "):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if cells[0] in rows:
                raise ValueError(f"Fila duplicada en {heading}: {cells[0]}")
            rows[cells[0]] = cells[1:]
    return rows


def effort_contract_errors(text: str) -> list[str]:
    """Validate the operational rubric only; never infer a feature score."""
    errors: list[str] = []
    profiles = table_rows(text, "Perfiles comparables")
    for level in range(1, 11):
        profile = profiles.get(str(level), [])
        if len(profile) != 2 or not all(profile):
            errors.append(f"perfil {level}")
    for level, anchor in (("1", "F01"), ("8", "F10"), ("10", "X13")):
        if profiles.get(level, [None])[0] != anchor:
            errors.append(f"referente {level}")
    output = normalized(section(text, "Formato de salida")).lower()
    for rule in (
        "1–7 inclusive: 🟢", "8–9: 🟠", "10: 🔴", "superior a x13: exactamente 10+ 🔴",
    ):
        if rule not in output:
            errors.append(f"presentación {rule}")
    if re.search(r"esfuerzo previsto del llm:\s*(?:1[1-9]|[2-9]\d|\d{3,})\b", text, re.I):
        errors.append("nota superior a 10")
    contrasts = table_rows(text, "Contrastes mínimos")
    expected_contrasts = {
        "F10-scaffold": ("8 🟠", "F10", ("tres métodos", "participantes", "locks")),
        "F10-sin-scaffold": ("9 🟠", "Entre F10 y X13", ("mismo alcance", "construir")),
        "X13-plus-saga": ("10+ 🔴", "Superior a X13", ("saga", "compensación", "interacciones")),
    }
    for case_id, (note, reference, factors) in expected_contrasts.items():
        row = contrasts.get(case_id, [])
        if len(row) != 3:
            errors.append(f"contraste {case_id}")
            continue
        if row[:2] != [note, reference]:
            errors.append(f"ancla {case_id}")
        if not all(factor in row[2].lower() for factor in factors):
            errors.append(f"factores {case_id}")
    if "verde no habilita lite" not in text.lower():
        errors.append("independencia de lite")
    return errors


def test_lab_effort_rubric() -> None:
    reference = read(SDD / "references" / "feature-level.md")
    examples_path = ROOT / "docs" / "sdd-effort-examples.md"
    examples = read(examples_path) if examples_path.is_file() else ""
    errors = effort_contract_errors(reference)
    check(not errors, f"ReserveLab: anclas, presentación y contrastes coherentes ({errors})")
    protocol = normalized(section(reference, "Comparación del esfuerzo")).lower()
    for concept in (
        "regresión", "casos límite", "estados", "capas", "persistencia", "integraciones",
        "concurrencia", "idempotencia", "compensación", "recuperación", "migraciones",
        "legado", "aislamiento", "autorización", "pruebas significativas",
    ):
        check(concept in protocol, f"ReserveLab: contempla {concept}")
    check("infraestructura correcta reutilizada" in protocol
          and "pendientes" in protocol and "no es una fórmula" in protocol,
          "ReserveLab: distingue trabajo pendiente de infraestructura reutilizada, sin fórmula")
    evidence = normalized(section(reference, "Evidencia de X13")).lower()
    check(all(fact in evidence for fact in (
        "10/11", "c12 válido", "admin_create", "no superó x13",
    )), "ReserveLab: conserva resultado parcial y límites de X13")
    emission = normalized(section(reference, "Formato de salida"))
    check(all(field in emission for field in (
        "Esfuerzo previsto del LLM: <nota e icono>", "Referente del laboratorio:",
        "Justificación:", "Supuestos relevantes:", "2–4",
    )), "ReserveLab: conserva los cuatro campos de la salida")
    check("verde no habilita lite" in reference.lower(),
          "ReserveLab: verde no elimina exclusiones de lite")
    check("indicador separado `exceeds_x13`" in reference
          and "10+ es valor 10 e" in reference
          and "como nota 11" in reference,
          "ReserveLab: conserva valor numérico e indicador 10+ separado")
    consumers = " ".join((read(SDD / "SKILL.md"), read(SDD_AGENT),
                          read(SDD / "references" / "templates.md")))
    check(examples_path.is_file() and "solo respaldo opcional" in examples.lower(),
          "ReserveLab: ejemplos extensos disponibles fuera del camino operativo")
    check("sdd-effort-examples.md" not in consumers,
          "agente/skill/plantillas no exigen cargar ejemplos de respaldo")
    mutations = (
        ("ancla F01", "| 1 | F01 |", "| 1 | F01 alterado |", "referente 1"),
        ("ancla X13", "| 10 | X13 |", "| 10 | X13 alterado |", "referente 10"),
        ("ancla F10", "| 8 | F10 |", "| 8 | F10 alterado |", "referente 8"),
        ("emoji/rango", "1–7 inclusive: 🟢", "1–7 inclusive: 🟠", "presentación 1–7 inclusive: 🟢"),
        ("10+ como nota", "exactamente 10+ 🔴", "exactamente 11 🔴", "presentación superior a x13: exactamente 10+ 🔴"),
        ("reutilización", "participantes y locks ya proporcionados", "infraestructura no especificada", "factores F10-scaffold"),
        ("exceso sin dimensiones", "Saga y compensación externa", "Cambio muy grande", "factores X13-plus-saga"),
        ("verde habilita lite", "Verde no habilita lite", "Verde habilita lite", "independencia de lite"),
    )
    for name, old, new, expected_error in mutations:
        check(old in reference, f"negativo/{name}: mutación alcanza el contrato real")
        mutated = reference.replace(old, new)
        check(expected_error in effort_contract_errors(mutated),
              f"negativo/{name}: detecta el defecto pertinente")

    backup_cases = table_rows(examples, "Casos detallados")
    check({"F01", "F10-scaffold", "F10-sin-scaffold", "X13", "X13-ampliado", "F07"}
          <= set(backup_cases), "respaldo conserva contrastes detallados sin cargar en scoring")
    backup_outputs = table_rows(examples, "Salidas por nota")
    check({str(level) for level in range(1, 11)} | {"10+"} <= set(backup_outputs),
          "respaldo enumera presentaciones sin repetirlas en la referencia operativa")
    check(all(fact in examples.lower() for fact in (
        "contracts.md", "contracts-f05-f07.md", "contracts-f08-f09.md", "contracts-f10.md",
        "contracts-x13.md", "10/11", "c12 válido", "admin_create", "post-hoc",
    )), "respaldo conserva procedencia y matiz histórico de X13")


def test_sdd_effort_context_budgets() -> None:
    paths = {
        "agente": (ROOT / "canonical/agents/sdd.md", 1066, 7580),
        "skill": (SDD / "SKILL.md", 2357, 16378),
        "rúbrica": (SDD / "references/feature-level.md", 1774, 12303),
        "plantillas": (SDD / "references/templates.md", 863, 5722),
    }
    measured: dict[str, tuple[int, int]] = {}
    for label, (path, max_words, max_chars) in paths.items():
        text = read(path)
        words, chars = len(text.split()), len(text)
        measured[label] = words, chars
        word_ok = words <= max_words if label == "plantillas" else words < max_words
        char_ok = chars <= max_chars if label == "plantillas" else chars < max_chars
        check(word_ok and char_ok,
              f"eficiencia {label}: {words} palabras/{chars} caracteres bajo baseline")
    for scenario, labels, max_words, max_chars in (
        ("inicio", ("agente", "skill"), 3423, 23958),
        ("scoring", ("agente", "skill", "rúbrica"), 5197, 36261),
        ("planificación con plantillas", ("agente", "skill", "rúbrica", "plantillas"), 6060, 41983),
    ):
        words = sum(measured[label][0] for label in labels)
        chars = sum(measured[label][1] for label in labels)
        check(words < max_words and chars < max_chars,
              f"eficiencia escenario {scenario}: {words} palabras/{chars} caracteres")


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
        agent_id = ("documentation-orchestrator" if specialist == "architecture" else
                    "code-review" if specialist in ("code-quality", "security") else specialist)
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


def test_agent_routing_policy() -> None:
    """Validate instructions, not a simulated runtime LLM classifier."""
    path = SDD / "references" / "agent-routing.md"
    check(path.is_file(), "routing: referencia canónica existe")
    if not path.is_file():
        return
    text = read(path)
    compact = normalized(text).lower()
    for heading, terms in (
        ("Candidatos y límites", ("`ui-design`", "`data-api`", "lógica de negocio",
                                  "seguridad transversal", "no verificable",
                                  "no enumeres ni recomiendes otros agentes")),
        ("Precedencias", ("elección explícita", "palabras clave", "mixto",
                          "contratos", "migraciones", "múltiples pantallas")),
        ("Decisión manual", ("seleccionar manualmente", "continuar con sdd",
                            "no cambia el agente activo", "no invoca subagentes",
                            "no delega ejecución automáticamente", "no repetir")),
        ("Contexto para selección manual", ("objetivo", "exclusiones", "rutas relativas",
                                           "requisitos", "tareas", "gate pendiente",
                                           "preguntas", "secretos", "no acredita entrega")),
        ("Integración con SDD", ("preflight", "antes de editar", "gate",
                                "profundidad", "estrategia de pruebas", "autorización")),
    ):
        body = normalized(section(text, heading)).lower()
        check(bool(body), f"routing: sección {heading}")
        for term in terms:
            check(term in body, f"routing/{heading}: regla {term}")
    manifest = json.loads(read(ROOT / "canonical" / "manifest.json"))
    check(all(candidate in manifest["agents"] for candidate in ("ui-design", "data-api")),
          "routing: candidatos pertenecen al catálogo real")
    check("no es un comando universal" in compact, "routing: notación portable, no invocación nativa")
    check("no usar `## handoff`" in compact, "routing: contexto manual separado de handoff documental")
    check("no aprueba gates" in compact, "routing: elección no aprueba gates")
    check("no cambia permisos" in compact, "routing: elección no cambia permisos")
    check("no enumeres ni recomiendes otros agentes" in compact,
          "routing: lista blanca v1 no se amplía al proponer aclaraciones")
    check("la elección de especialista significa que esa actividad no se ejecuta en sdd" in compact,
          "routing: selección especializada detiene ejecución local incluso si se pidió implementar")


def test_agent_routing_integration() -> None:
    agent = read(SDD_AGENT)
    skill = read(SDD / "SKILL.md")
    for label, text in (("agente", agent), ("skill", skill)):
        body = normalized(section(text, "Recomendación de agente por dominio")).lower()
        check(bool(body), f"routing/{label}: entrada explícita")
        check("references/agent-routing.md" in body, f"routing/{label}: referencia bajo demanda")
        check("selección manual" in body and "no" in body and "automáticamente" in body,
              f"routing/{label}: selección manual, sin cambio automático")
    implementation = normalized(section(skill.replace("### Implementación", "## Implementación"),
                                        "Implementación")).lower()
    check("agent-routing.md" in implementation and "gates pendientes" in implementation,
          "routing: tareas acotadas preservan gates pendientes")
    requirements = normalized(skill[skill.index("### Fase 1 — Requirements"):]).lower()
    check("la ausencia de contexto no obliga a cambiar de agente" in requirements,
          "routing: ausencia de README no impone cambio ni duplica elección")


def test_agent_routing_write_barrier() -> None:
    """Regression for R01: instructions must make routing a prerequisite to writing."""
    agent = read(SDD_AGENT)
    guard = section(agent, "Control previo a cualquier escritura")
    compact = normalized(guard).lower()
    check(bool(guard), "routing/R01: control de escritura explícito en agente")
    check(bool(guard) and agent.index(guard) < agent.index("## Reglas inviolables"),
          "routing/R01: control visible antes de las reglas generales")
    for term in ("solo visual", "`ui-design`", "solo datos", "`data-api`",
                 "carga `sdd-spec`", "references/agent-routing.md", "no uses `edit`",
                 "selección explícita", "no equivale", "preflight"):
        check(term in compact, f"routing/R01: antecedente {term}")
    skill = normalized(section(read(SDD / "SKILL.md"), "Recomendación de agente por dominio")).lower()
    check("no uses herramientas de escritura" in skill and "decisión de ejecutor" in skill,
          "routing/R01: skill prohíbe escribir sin resolver ejecutor")
    check("la lista v1 es cerrada" in skill and "no enumeres ni recomiendes otros agentes" in skill,
          "routing: skill refuerza lista cerrada")
    reference = normalized(read(SDD / "references" / "agent-routing.md")).lower()
    check("seleccionar el agente `sdd` no equivale" in reference,
          "routing/R01: abrir SDD no suprime recomendación del especialista")
    check("no uses herramientas de escritura" in reference,
          "routing/R01: referencia conserva barrera explícita")
    check("la petición original incluyera «implementa»" in reference
          and "detente en sdd" in reference,
          "routing/R10: selección manual detiene implementación local")


def test_agent_routing_scope_and_manual_handoff() -> None:
    """Keep v1 candidates closed and make specialist choice a stop-and-package branch."""
    reference = normalized(read(SDD / "references" / "agent-routing.md")).lower()
    check("solo `ui-design` y `data-api`" in reference,
          "routing/R04: lista blanca v1 explícita")
    check("no enumeres ni recomiendes otros agentes" in reference,
          "routing/R04: no filtrar otros candidatos al aclarar")
    check("mantén sdd" in reference,
          "routing/R04: agente fuera de la lista mantiene SDD")
    specialist = normalized(section(read(SDD / "references" / "agent-routing.md"),
                                   "Contexto para selección manual")).lower()
    for term in ("si el usuario elige explícitamente al especialista", "detente en sdd",
                 "no continúes la implementación aquí", "la petición original incluyera «implementa»",
                 "contexto copiable"):
        check(term in specialist, f"routing/R10: selección especialista → stop/package ({term})")


def test_agent_routing_conflict_clarification() -> None:
    """Clarification must never broaden the v1 candidate set."""
    skill = normalized(read(SDD / "references" / "agent-routing.md")).lower()
    check("no enumeres ni recomiendes otros agentes" in skill,
          "routing/R04: no propone candidatos fuera de v1 al aclarar")
    check("explica solo que queda fuera de los dos candidatos" in skill,
          "routing/R04: dominio externo a lista queda en SDD")
    check("security" not in skill and "code-quality" not in skill and "architecture" not in skill,
          "routing/R04: referencia no lista terceros como candidatos")


def test_agent_routing_generated() -> None:
    manifest = json.loads(read(ROOT / "canonical" / "manifest.json"))
    for platform in manifest["platforms"]:
        adapter = json.loads(read(ROOT / "adapters" / platform / "agents" / "sdd.json"))
        agent = read(ROOT / "generated" / platform / "agents" / adapter["filename"])
        skill = read(ROOT / "generated" / platform / "skills" / "sdd-spec" / "SKILL.md")
        barrier = normalized(section(agent, "Control previo a cualquier escritura")).lower()
        check("no uses `edit`" in barrier and "carga `sdd-spec`" in barrier,
              f"routing/{platform}: barrera R01 propagada")
        for label, text in (("agente", agent), ("skill", skill)):
            body = normalized(section(text, "Recomendación de agente por dominio")).lower()
            check("references/agent-routing.md" in body, f"routing/{platform}/{label}: referencia integrada")
            check("selección manual" in body and "no cambies de agente automáticamente" in body,
                  f"routing/{platform}/{label}: manual, sin cambio automático")
            compact = normalized(text).lower()
            check("no enumeres ni recomiendes otros agentes" in compact,
                  f"routing/{platform}/{label}: whitelist sin ampliación")
            check("la elección de especialista significa que esa actividad no se ejecuta en sdd" in compact,
                  f"routing/{platform}/{label}: stop al elegir especialista")
        reference = ROOT / "generated" / platform / "skills" / "sdd-spec" / "references" / "agent-routing.md"
        check(reference.is_file(), f"routing/{platform}: referencia distribuida")
        if reference.is_file():
            check(reference.read_bytes() == (SDD / "references" / "agent-routing.md").read_bytes(),
                  f"routing/{platform}: referencia idéntica a canonical")


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
    print("Contrato SDD — calificación de feature, rutas, testing adaptativo, Navigator e integración")
    test_modes_remain_proportional()
    test_lite_quick_plan_contract()
    test_feature_level_contract()
    test_lab_effort_rubric()
    test_sdd_effort_context_budgets()
    test_spec_paths_support_grouping()
    test_adaptive_testing_selection()
    test_variants_and_evidence()
    test_navigator_context_contract()
    test_specialists_recommend_sdd_without_switching()
    test_agent_routing_policy()
    test_agent_routing_integration()
    test_agent_routing_write_barrier()
    test_agent_routing_scope_and_manual_handoff()
    test_agent_routing_conflict_clarification()
    test_agent_routing_generated()
    test_generated_references_match_canonical()
    total = PASSED + FAILED
    print(f"{PASSED}/{total} comprobaciones correctas")
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
