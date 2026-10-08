# Verificación — Nivel de feature exclusivo de SDD

Modo SDD: standard
Fase: Verification
Estado: cerrada
Gate 4: aprobado por el usuario («cierra»)

## Ciclo de pruebas

- Estrategia: TDD focalizado para contratos de instrucciones y distribución; validación/regresión para contratos preexistentes.
- RED: observado antes del render final; faltaba `feature-level.md` generado, existían matrices antiguas y fallaba el silencio del adapter Antigravity.
- GREEN: tras actualizar fuentes/adapters y renderizar, los contratos relevantes pasan.
- Suite final focalizada: SDD 427/427; silencio y exclusividad 5/5; Code Review 7/7; Documentation Core 12/12; Retired Agents 26/26; Handoff 34/34.
- Distribución: `validate.py` correcto para 10 skills, 6 agentes y 6 plataformas; suites de instalación 196/196 y Antigravity 22/22.
- Checks finales: `test_validate.py` 38/38; `test_links.py` 4/4; `check_links.py` 66 archivos; `git diff --check` limpio.
- Excepción: los smokes conversacionales en hosts reales no se ejecutaron. Los checks de prompts/render no prueban obediencia runtime; ver `implementation-evidence.md`.

## Matriz de requisitos y evidencia

| Requisito | Tarea(s) | Test/check | Evidencia (path o comando) | Estado |
|---|---|---|---|---|
| Req 1.1–1.2 | 1.1, 2.1 | `test_feature_level_contract` comprueba análisis previo y ausencia de provisional | `tools/test_sdd_contract.py`; `canonical/skills/sdd-spec/references/feature-level.md`; `generated/*/skills/sdd-spec/references/feature-level.md` | ✅ |
| Req 1.3–1.5, 1.10 | 1.1, 2.1 | Rubrica todos los niveles, rangos emoji y ejemplos con el entero real; límites 1/7/8/9/10 | `python3 -B tools/test_sdd_contract.py` → 427/427; `feature-level.md` | ✅ |
| Req 1.6–1.9 | 1.1, 2.1 | Exclusividad SDD, feature completa, emisión por modo, no repetición y reanálisis si cambia alcance | `tools/test_sdd_contract.py`; `tools/test_model_recommendations.py`; `canonical/agents/sdd.md`; `canonical/skills/sdd-spec/SKILL.md` | ✅ |
| Req 2.1–2.4, 2.7 | 1.1, 2.2–2.5, 3.2, 4.1 | Contrato negativo revisa canonical/adapters/generated; no quedan matrices operativas ni recomendaciones activas | `python3 -B tools/test_model_recommendations.py` → 5/5; `canonical/`; `adapters/`; `generated/` | ✅ |
| Req 2.5–2.6 | 1.2, 2.2–2.4 | Contratos preservan gates SDD, autorización Code Review/remediación, handoff y migración segura | `test_sdd_contract.py`; `test_code_review_contract.py` → 7/7; `test_handoff_contract.py` → 34/34; `test_retired_agents.py` → 26/26 | ✅ |
| Req 3.1 | 2.1–2.5, 4.1 | Render y validación de todas las plataformas; referencia SDD coincide byte a byte | `python3 -B tools/render.py`; `python3 -B tools/validate.py`; `tools/test_sdd_contract.py` | ✅ |
| Req 3.2 | 3.1 | Revisión de guías y escenarios smoke vigentes; evidencia histórica diferenciada | `docs/agentes/`; `docs/uso.md`; `docs/sdd-smoke.md`; `docs/model-recommendations-smoke.md`; `docs/*-smoke.md` | ✅ |
| Req 3.3 | 1.1, 1.2, 5.1 | Pruebas de límites/calificación, ausencia de avisos y gates/autorizaciones | `tools/test_sdd_contract.py`; `tools/test_model_recommendations.py`; `tools/test_code_review_contract.py`; `tools/test_handoff_contract.py` | ✅ |
| Req 3.4 | 1.2, 3.2, 4.1, 5.1 | Recursos obsoletos se retiran del render y enlaces validan | `python3 -B tools/validate.py`; `python3 -B tools/check_links.py`; contratos generated de SDD/silencio | ✅ |
| Req 3.5 | 3.1 | Evidencia anterior se identifica como histórica; historial de specs ajenas no migrado | `docs/model-recommendations-smoke.md`; `git status --short` y diff revisado | ✅ |

## Self-check RNF

| RNF | Evidencia | Estado |
|---|---|---|
| RNF-1: paridad de todas las plataformas y ausencia de matrices retiradas | `python3 -B tools/render.py`; `python3 -B tools/validate.py`; `test_sdd_contract.py` verifica la referencia en 6 plataformas; `test_model_recommendations.py` busca matrices stale | ✅ |
| RNF-2: prompts no exigen recomendación LLM ni pausa | `test_model_recommendations.py` inspecciona canonical, adapters y generated; `test_sdd_contract.py` comprueba preflight técnico y calificación sin gate | ✅ |
| RNF-3: gates/autorizaciones siguen protegidos | `test_sdd_contract.py`; `test_code_review_contract.py`; `test_handoff_contract.py`; `test_retired_agents.py`; `test_install.py` | ✅ |
| RNF-4: no quedan enlaces operativos rotos | `python3 -B tools/check_links.py` → 66 archivos; `python3 -B tools/test_links.py` → 4/4 | ✅ |
| RNF-5: cambios locales ajenos y perfiles instalados se preservan | Revisión de `git status --short`: modificaciones preexistentes en laboratorio SDD/`.security/` permanecen ajenas; no se ejecutó instalador sobre el host | ✅ |

## Quality bar y límites de evidencia

- Capas: canonical/adapters → render → generated; `validate.py` pasa. No hay cambios en runtime de producto ni dependencias.
- DI, persistencia de aplicación, UI, I/O e hilos: no aplican a este cambio de instrucciones/configuración.
- Errores: validadores fallan con exit no-cero ante fixtures inválidos; casos cubiertos por `test_validate.py` (38/38).
- TDD no se atribuye a verificaciones del host; solo al ciclo de contrato textual RED/GREEN observado.
- El smoke multi-plataforma de conversación queda no ejecutado. No marcar como probado el comportamiento runtime de los LLM.
- `.sdd/specs/nivel-feature-sdd/tasks.md` conserva `[omitido: razón]` para ese escenario no ejecutado.
