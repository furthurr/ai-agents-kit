# Verificación — Modo lite de SDD

Modo de esta spec: `standard`
Estado: `cerrada`
Gate 4: aprobado por el usuario el 2026-09-15

## Ciclo de pruebas

- **Estrategia:** TDD focalizado sobre el contrato observable de prompts,
  referencias, adaptadores y artefactos generados.
- **RED observado:** `python3 tools/test_sdd_contract.py` devolvió `149/168`; los
  19 fallos correspondieron a `lite`, exclusividad de Quick Plan, gates,
  plantillas, evidencia y testing todavía no implementados.
- **GREEN observado:** tras actualizar el contrato canónico y renderizar,
  `python3 tools/test_sdd_contract.py` devolvió `172/172`.
- **REFACTOR:** la semántica común quedó en la skill y el agente canónicos; modelo,
  testing, plantillas, integridad y quality bar permanecen en referencias bajo
  demanda. No se añadió tooling ni una referencia nueva.
- **Excepciones:** ninguna. PBT fue omitido porque el contrato textual no contiene
  un invariante algebraico útil.

## Suites y validadores

| Comando | Resultado |
|---|---|
| `python3 tools/render.py` | Exit 0; cuatro plataformas regeneradas |
| `python3 tools/validate.py` | 10 skills y 9 agentes válidos en 4 plataformas |
| `python3 tools/test_sdd_contract.py` | 172/172 |
| `python3 tools/test_model_recommendations.py` | 114/114 |
| `python3 tools/test_validate.py` | 14/14 pruebas negativas |
| `python3 tools/test_integrity.py` | 345/345 |
| `python3 tools/test_links.py` | 4/4 |
| `python3 tools/check_links.py` | 70 archivos Markdown, correctos |
| `python3 tools/measure_context.py` | Agentes 3.291; skills 16.810; referencias 13.113 palabras |
| `git diff --check` | Exit 0 |

## Matriz de trazabilidad

| Requisitos | Tareas | Prueba o validación | Evidencia | Estado |
|---|---|---|---|---|
| REQ-001–REQ-007 | 1.1, 4.2 | `test_modes_remain_proportional` | `SKILL.md`, `agents/sdd.md`, contrato 172/172 | ✅ |
| REQ-008–REQ-014 | 1.2, 3.3, 3.4, 4.4 | `test_lite_quick_plan_contract`; smoke 5 y 8 | Contrato canónico, docs y adaptadores | ✅ |
| REQ-015–REQ-021 | 1.1, 4.2 | selección y fallback en contrato; smoke 3, 4 y 9 | `SKILL.md` § Modos de profundidad | ✅ |
| REQ-022–REQ-028 | 2.2, 3.3 | checks de intención, marcador y verificación; smoke 6 y 7 | `templates.md`, `integrity-gate.md` | ✅ |
| REQ-029–REQ-034 | 2.1, 3.3, 3.4 | checks de Gate 0 y reclasificación; smoke 10 | `model-selection.md`, `agents/sdd.md` | ✅ |
| REQ-035–REQ-040 | 2.3, 3.4, 4.3 | testing adaptativo e integrity gate | `testing.md`, `quality-bar.md`, suites verdes | ✅ |
| REQ-041–REQ-047 | 3.1–3.4, 4.1–4.4 | paridad generated, validate y smoke 11, 15, 17 | cuatro árboles `generated/`; validate exit 0 | ✅ |

## Integridad de tareas

| Tarea | Artefacto o evidencia | Estado |
|---|---|---|
| 1.1 | Tests de cuatro modos y selección; skill/agente canónicos | ✅ |
| 1.2 | Tests y contrato de Quick Plan exclusivo | ✅ |
| 2.1 | `model-selection.md`; checks de gates y reclasificación | ✅ |
| 2.2 | `templates.md`; marcador y verificación compacta | ✅ |
| 2.3 | `testing.md`, `integrity-gate.md`, `quality-bar.md` | ✅ |
| 3.1 | Contrato 172/172 y compatibilidad legacy documentada | ✅ |
| 3.2 | Cuatro adaptadores JSON válidos | ✅ |
| 3.3 | Documentación de agente, uso y catálogo | ✅ |
| 3.4 | `docs/sdd-smoke.md` con 29 escenarios; backlog actualizado | ✅ |
| 4.1 | `generated/{copilot,opencode,kiro,claude}` renderizado | ✅ |
| 4.2 | Contrato SDD y validate verdes | ✅ |
| 4.3 | Suites, enlaces, contexto y diff check verdes | ✅ |
| 4.4 | Diff revisado; cambio concurrente de `README.md` excluido | ✅ |
| 5.1 | Este archivo, ciclo y matrices | ✅ |
| 5.2 | Integrity gate final aplicado; cierre presentado en Gate 4 | ✅ |

## Self-check de RNF

| RNF | Evidencia | Estado |
|---|---|---|
| RNF-1 Portabilidad | Contrato y referencias coinciden en las cuatro plataformas; validate verde | ✅ |
| RNF-2 Compatibilidad | `standard` conserva Gates 1–4; legacy se aclara sin migración automática | ✅ |
| RNF-3 Auditabilidad | Plantilla y gate exigen `verification.md` compacto para lite implementado | ✅ |
| RNF-4 Proporcionalidad | Lite usa Gate 0 y Quick Plan sin Gates 1–3 ni Gate 4 | ✅ |
| RNF-5 Mantenibilidad | Semántica común en `canonical/`; `generated/` procede del render | ✅ |

## Alcance y observaciones

- No se modificaron `canonical/manifest.json`, `tools/render.py` ni
  `tools/validate.py` porque el pipeline existente soporta el cambio.
- Las specs cerradas anteriores no fueron reescritas.
- El cambio concurrente de título en `README.md` no pertenece a esta spec y se
  conserva sin modificación.
