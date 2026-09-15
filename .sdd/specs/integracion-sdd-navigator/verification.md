# Verificación — Integración SDD con Project Navigator

## Ciclo de pruebas

- **Estrategia:** TDD focalizado sobre el contrato observable de prompts y
  artefactos generados.
- **RED observado:** `python3 tools/test_sdd_contract.py` devolvió `96/113`; los
  17 fallos correspondieron al contrato, referencia y propagación Navigator aún
  inexistentes.
- **GREEN observado:** tras implementar el contrato mínimo y renderizar,
  `python3 tools/test_sdd_contract.py` devolvió `121/121`.
- **REFACTOR:** el procedimiento detallado quedó centralizado en
  `canonical/skills/sdd-spec/references/navigator-context.md`; agente y skill solo
  contienen puntos de entrada y reglas de fase.
- **Excepciones:** ninguna. PBT fue omitido porque no existe invariante algebraico.

## Suites y validadores

| Comando | Resultado |
|---|---|
| `python3 tools/render.py` | Exit 0; salidas regeneradas |
| `python3 tools/validate.py` | 10 skills y 9 agentes válidos en 4 plataformas |
| `python3 tools/test_sdd_contract.py` | 121/121 |
| `python3 tools/test_handoff_contract.py` | 24 tests, OK |
| `python3 tools/check_links.py` | 61 archivos Markdown, correctos |
| `python3 tools/test_links.py` | 4/4 |
| `python3 tools/test_validate.py` | 14/14 pruebas negativas |
| `python3 tools/test_integrity.py` | 312/312 |
| `git diff --check` | Exit 0, sin errores |

## Matriz de trazabilidad

| Requisito | Tareas | Prueba o validación | Evidencia | Estado |
|---|---|---|---|---|
| Req 1 — Uso opcional | 1.1, 2.1, 3.1, 4.1 | `test_navigator_context_contract` | `canonical/agents/sdd.md`, `canonical/skills/sdd-spec/SKILL.md`, referencia generada en 4 plataformas | ✅ |
| Req 2 — Degradación | 1.1, 2.1, 2.2, 4.1 | checks de estados y fuentes directas | `navigator-context.md` § Capas incompletas; smoke 17–19 | ✅ |
| Req 3 — Actualización explícita | 1.1, 2.1, 2.2, 4.1 | check de ausencia de escritura | `navigator-context.md` § Bootstrap o update; smoke 20 | ✅ |
| Req 4 — Frescura | 1.1, 2.2, 4.1 | checks de `source_commit`, `generated_at` y estados | `navigator-context.md` § Frescura y confianza; smoke 19 | ✅ |
| Req 5 — Coherencia | 1.1, 3.1, 4.1 | render, validate, contratos e integridad | `generated/{copilot,opencode,kiro,claude}/`; 121/121 y 312/312 | ✅ |

## Integridad de tareas

| Tarea | Artefacto o evidencia | Estado |
|---|---|---|
| 1.1 | Test RED/GREEN; agente, skill y referencia canónicos | ✅ |
| 2.1 | `docs/agentes/sdd.md`, `docs/uso.md` | ✅ |
| 2.2 | `docs/sdd-smoke.md`, escenarios 16–20 | ✅ |
| 3.1 | Árboles `generated/` de cuatro plataformas | ✅ |
| 4.1 | Suites y validadores de la tabla anterior | ✅ |
| 4.2 | Este archivo, matriz y revisión final | ✅ |

## Self-check de RNF

| RNF | Evidencia | Estado |
|---|---|---|
| RNF-1 — Portabilidad | El contrato SDD valida agente, skill y referencia para las cuatro plataformas; `validate.py` verde | ✅ |
| RNF-2 — Resiliencia | Tests de degradación/no escritura y reglas explícitas en `navigator-context.md` | ✅ |
| RNF-3 — Eficiencia | `navigator-context.md` exige config + capa mínima y prohíbe volcar índices completos | ✅ |
| RNF-4 — Mantenibilidad | Procedimiento centralizado; ningún adapter ni `tools/render.py` fue modificado | ✅ |
| RNF-5 — Compatibilidad | Contrato SDD completo 121/121, handoff 24/24 e integridad 312/312 | ✅ |

## Spot-check de quality bar

- No se modificó código de producto, persistencia, red, UI ni dependencias.
- Los fallos de disponibilidad/frescura tienen degradación explícita; no hay fallos
  silenciosos ni información inventada.
- Se observó RED por el comportamiento nuevo y GREEN de la suite completa.
- No se añadieron abstracciones, adapters, herramientas ni dependencias PBT.
- Los cinco RNF declarados quedaron contrastados con artefactos o comandos.

## Limitaciones y seguimiento

- Los escenarios 16–20 de `docs/sdd-smoke.md` documentan la validación manual por
  plataforma instalada; no se ejecutaron en esta sesión y permanecen como smoke
  previo a una release, sin invalidar el contrato canónico automatizado.
- Esta mejora no inicializa `.navigator/` en este repositorio; solo habilita su
  consumo opcional por SDD cuando exista en un proyecto usuario.
