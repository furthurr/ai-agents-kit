# Verificación — Pausa tras recomendaciones de modelo en el kit

Modo SDD: standard
Fase: Verification
Estado: cerrada con limitación explícita: smoke conversacional pendiente
Gate 4: aprobado (usuario: «adelante»)

## Ciclo de pruebas

- Estrategia: TDD focalizado para contrato observable en instrucciones y pruebas
  textuales. No se declara TDD de conducta real de un host.
- RED observado antes del cambio canónico:
  `python3 tools/test_sdd_contract.py` → 186/189; fallaron pausa inicial, aviso
  manual en plantilla y pausa previa a Verification.
  `python3 tools/test_model_recommendations.py` → 116/131; fallaron tres checks
  nuevos por cada uno de los cinco especialistas (agente, skill y matriz).
- GREEN tras `python3 tools/render.py`:
  `python3 tools/test_sdd_contract.py` → 189/189;
  `python3 tools/test_model_recommendations.py` → 131/131;
  `python3 tools/validate.py` → 10 skills y 9 agentes válidos en cuatro plataformas.
- Suite complementaria: `python3 tools/test_integrity.py` → 350/350;
  `python3 tools/test_handoff_contract.py` → 24/24;
  `python3 tools/test_links.py` → 4/4;
  `python3 tools/test_mas_identity.py` → 197/197;
  `python3 tools/test_validate.py` → 14/14 (casos negativos esperados);
  `python3 tools/test_install.py` → 100/100;
  `git diff --check` → sin incidencias.
- Excepción: `docs/sdd-smoke.md` describe la prueba conversacional de dos turnos,
  pero **no** se instaló ni ejecutó en los hosts reales; no se afirma eficacia
  interactiva hasta obtener esa evidencia.

## Matriz de evidencia

| Requisito | Tarea(s) | Test/check | Evidencia | Estado |
|-----------|----------|------------|-----------|--------|
| REQ-001–004 | 1.1, 2.1, 2.2, 3.1 | `test_model_selection_gate`, `test_phase_scoped_recommendations` | `canonical/agents/sdd.md`, `canonical/skills/sdd-spec/SKILL.md`, `canonical/skills/sdd-spec/references/model-selection.md`, `tools/test_sdd_contract.py` | ✅ contrato |
| REQ-005–009 | 1.1, 2.1, 2.2, 3.1 | `test_phase_scoped_recommendations` | `canonical/skills/sdd-spec/references/model-selection.md`, `canonical/skills/sdd-spec/references/integrity-gate.md`, `tools/test_sdd_contract.py` | ✅ contrato |
| REQ-010–013 | 1.1, 2.2, 2.3, 3.1 | `test_model_selection_gate`, `test_generated_references_match_canonical` | `docs/agentes/sdd.md`, `docs/sdd-smoke.md`, `generated/{copilot,opencode,kiro,claude}/skills/sdd-spec/` | ✅ contrato |
| REQ-014–015 | 1.2, 2.4, 3.1 | `test_specialist_contracts` | `canonical/agents/{architecture,code-quality,data-api,security,ui-design}.md`, `canonical/skills/*/references/model-selection.md`, `tools/test_model_recommendations.py` | ✅ contrato |
| REQ-016–019 | 1.2, 2.4, 2.5, 3.1 | `test_existing_agents_and_git_exception`, `test_handoff_contract.py` | `canonical/skills/documentation-orchestrator/references/workflows.md`, `canonical/skills/project-navigator/references/bootstrap.md`, matrices de especialistas | ✅ contrato |
| REQ-020 | 1.2, 2.6, 3.1 | `test_generated_parity`, `tools/validate.py` | `generated/{copilot,opencode,kiro,claude}/`, `docs/sdd-smoke.md` | ✅ generación; smoke pendiente |

## Self-check RNF y quality bar

| RNF | Evidencia | Estado |
|-----|-----------|--------|
| RNF-1 (elección manual) | Búsqueda puntual en `canonical/agents/`, skills de especialistas y `tools/test_model_recommendations.py`; todos conservan prohibición de cambiar host y reanudación sin declarar modelo | ✅ contrato |
| RNF-2 (paridad) | `python3 tools/render.py`, `python3 tools/validate.py`, `test_generated_parity`, `test_generated_references_match_canonical` | ✅ |
| RNF-3 (gates) | `canonical/skills/sdd-spec/SKILL.md`, `canonical/skills/sdd-spec/references/integrity-gate.md`, `test_phase_scoped_recommendations`, `test_handoff_contract.py` | ✅ contrato |
| RNF-4 (una pausa por alcance) | Cinco matrices `model-selection.md` y `canonical/skills/documentation-orchestrator/references/workflows.md`; requiere smoke para garantizar conducta de host | ⚠️ contractual, interactiva pendiente |

Capas, DI, storage, I/O de UI y errores tipados no aplican a instrucciones y
tests estáticos; no se añadieron abstracciones ni dependencias. Cada `[x]` en
`tasks.md` referencia archivos en disco o comandos con resultado registrado.

## Pendiente para cierre funcional

Ejecutar los escenarios manuales de `docs/sdd-smoke.md` en la(s) plataforma(s)
requerida(s) y registrar resultados. El usuario aprobó el cierre contractual con
esta limitación explícita; no se considera validado el comportamiento interactivo.
