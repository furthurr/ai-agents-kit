# Verificación — Recomendación de modelo por próxima fase

Modo SDD: standard
Fase: Verification
Estado: cerrada
Gate 4: aprobado
Fecha de cierre: 2026-09-15

## Ciclo de pruebas

- Estrategia: TDD focalizado sobre el contrato observable de mensajes, estado y
  artefactos generados.
- RED: `python3 tools/test_sdd_contract.py` → `172/186`; fallaron los checks nuevos
  de preflight por próxima fase, transición, estado y paridad antes de actualizar el
  contrato canónico.
- GREEN: `python3 tools/test_sdd_contract.py` → `186/186`.
- Excepción PBT: omitido; los mensajes y estados textuales no contienen un invariante
  algebraico útil.
- Smoke interactivo: no ejecutado en las cuatro plataformas; se validó la paridad
  estática de Copilot, OpenCode, Kiro y Claude.

## Suite final

| Comando | Resultado |
|---|---|
| `python3 tools/test_sdd_contract.py` | 186/186 |
| `python3 tools/test_model_recommendations.py` | 114/114 |
| `python3 tools/test_integrity.py` | 345/345 |
| `python3 tools/test_install.py` | 100/100 |
| `python3 tools/test_handoff_contract.py` | 24 tests OK |
| `python3 tools/test_mas_identity.py` | 197/197 |
| `python3 tools/test_links.py` | 4/4 |
| `python3 tools/check_links.py` | 70 archivos revisados |
| `python3 tools/measure_context.py` | agentes 3,350; skills 17,098; referencias 13,312 palabras |
| `python3 tools/render.py` | generado sin errores |
| `git diff --check` | sin errores |

## Matriz de requisitos

| Requisitos | Tarea(s) | Test/check | Evidencia | Estado |
|---|---|---|---|---|
| REQ-001–REQ-007 | 1.1, 1.2, 2.1, 2.2 | `test_phase_scoped_recommendations` | `canonical/skills/sdd-spec/references/model-selection.md`, `SKILL.md` | ✅ |
| REQ-008–REQ-014 | 3.1–3.4, 4.4 | `test_phase_scoped_recommendations` | `docs/sdd-smoke.md`, `canonical/skills/sdd-spec/SKILL.md` | ✅ |
| REQ-015–REQ-020 | 3.1, 3.4, 4.2, 5.4 | `test_sdd_contract.py` | `canonical/agents/sdd.md`, `canonical/skills/sdd-spec/SKILL.md` | ✅ |
| REQ-021–REQ-026 | 4.1, 4.2 | `test_modes_remain_proportional`, `test_lite_quick_plan_contract` | `canonical/skills/sdd-spec/SKILL.md`, `model-selection.md` | ✅ |
| REQ-027–REQ-031 | 3.3, 5.4 | `test_model_selection_gate`, `test_phase_scoped_recommendations` | `model-selection.md`, `integrity-gate.md` | ✅ |
| REQ-032–REQ-035 | 2.1, 2.2, 3.3, 6.2 | `test_phase_scoped_recommendations` | `templates.md`, `integrity-gate.md` | ✅ |
| REQ-036–REQ-041 | 1.1, 1.2, 3.1, 4.3, 4.4, 5.1–5.4, 6.1 | `test_sdd_contract.py`, `test_model_recommendations.py` | `generated/{copilot,opencode,kiro,claude}/` | ✅ |

## Self-check RNF

| RNF | Evidencia | Estado |
|---|---|---|
| RNF-1 Claridad | `model-selection.md`: preflight y gate se describen como conceptos separados | ✅ |
| RNF-2 Control | `SKILL.md` e `integrity-gate.md`: exige aprobación actual y nivel confirmado | ✅ |
| RNF-3 Proporcionalidad | `test_modes_remain_proportional`, `test_lite_quick_plan_contract` | ✅ |
| RNF-4 Reanudación | `templates.md` e `integrity-gate.md`: marcadores de modo, fase, estado y gate | ✅ |
| RNF-5 Portabilidad | `test_generated_references_match_canonical`, 4 plataformas renderizadas | ✅ |

## Integridad

- Las tareas 1.1–6.2 están marcadas `[x]` y tienen evidencia de archivo o comando.
- PBT queda declarado como omitido con razón explícita.
- No se crean gates adicionales; `standard` y `deep` conservan Gates 1–4.
- El cambio concurrente de `README.md` se conserva y no forma parte de esta spec.
- Gate 4 aprobado por el usuario; la spec queda cerrada.
