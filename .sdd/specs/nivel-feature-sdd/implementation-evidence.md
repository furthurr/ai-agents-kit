# Evidencia de implementación — Nivel de feature exclusivo de SDD

Modo SDD: standard
Fase: Implementación
Estado: cerrada; ver `verification.md`
Gate 3: aprobado por el usuario («procede»)

## Cambios observables

- La nueva rúbrica vive en `canonical/skills/sdd-spec/references/feature-level.md`;
  la skill y agente SDD ya no recomiendan modelos. Solo el agente SDD puede mostrar
  la puntuación, una vez definido el alcance de una feature.
- Retiradas las seis referencias operativas `model-selection.md` (cinco especialistas
  y SDD), avisos en Documentation Orchestrator y Project Navigator y matrices de
  comunicación por agente.
- Actualizados tests de contrato, documentación, adapters y `.github/workflows/ci.yml`.
- Render actualizado para Copilot, OpenCode, Kiro, Claude, Pi y Antigravity.
- Las instalaciones del host no se modificaron/reinstalaron.

## RED → GREEN focalizado

- RED observado al ejecutar las comprobaciones del contrato antes del render final:
  faltaba la rúbrica en `generated/`, persistían matrices distribuidas antiguas y la
  descripción de Antigravity aún recomendaba nivel LLM. Se corrigió la fuente y el
  render; los checks completos pasan después.
- No hubo refactor amplio ni abstracciones nuevas.

## Verificación ejecutada durante Implementación

| Comando | Resultado observado |
|---|---|
| `python3 -B tools/render.py` | Exit 0; seis plataformas regeneradas. |
| `python3 -B tools/validate.py` | Exit 0; 10 skills y 6 agentes en 6 plataformas. |
| `python3 -B tools/test_sdd_contract.py` | 427/427 comprobaciones. |
| `python3 -B tools/test_model_recommendations.py` | 5/5 tests. |
| `python3 -B tools/test_code_review_contract.py` | 7/7 tests. |
| `python3 -B tools/test_documentation_core.py` | 12/12 tests. |
| `python3 -B tools/test_retired_agents.py` | 26/26 tests. |
| `python3 -B tools/test_handoff_contract.py` | 34/34 tests. |
| `python3 -B tools/test_antigravity_contract.py` | 5/5 tests. |
| `python3 -B tools/test_validate.py` | 38/38 pruebas negativas. |
| `python3 -B tools/test_links.py` | 4/4 tests. |
| `python3 -B tools/check_links.py` | 66 archivos revisados; enlaces correctos. |
| `python3 -B tools/test_integrity.py` | 415/415 checks. |
| `python3 -B tools/test_install.py` | 196/196 pruebas en perfiles temporales para seis plataformas. |
| `python3 -B tools/test_antigravity_install.py` | 22/22 tests. |
| `python3 -B tools/measure_context.py` | 3,419 palabras agentes; 17,419 skills; 14,171 referencias bajo demanda. |
| `git diff --check` | Exit 0. |

## Pendientes explícitos

- Smoke conversacional en hosts reales: no ejecutado; los tests de texto prueban
  instrucciones y paridad, no obediencia runtime.
- Verification formal está en `verification.md`; solo resta obtener Gate 4.
- No afirmar que el perfil personal instalado se haya actualizado.
