# Evidencia de implementación — Avisos de modelo no bloqueantes

- Modo SDD: standard
- Fase: Implementación
- Estado: implementado; pendiente de Verification
- Gate aprobado: Gate 3 — usuario: «procede» tras Tasks
- Fecha: 2026-10-05

Esta es evidencia compacta de comandos observados y artefactos de implementación,
no un informe de suite completa ni validación conversacional en hosts.

## Baseline antes de modificar fuentes/pruebas (tarea 1.1)

Desde la raíz del repositorio, invocación secuencial con `&&`:

| Comando | Resultado observado | Retorno |
| --- | --- | --- |
| `python3 -B tools/test_model_recommendations.py` | 141/141 comprobaciones | 0 |
| `python3 -B tools/test_sdd_contract.py` | 213/213 comprobaciones | 0 |
| `python3 -B tools/test_code_review_contract.py` | 7 tests OK | 0 |
| `python3 -B tools/test_handoff_contract.py` | 33 tests OK | 0 |
| `python3 -B tools/validate.py` | 10 skills, 8 agentes, 5 plataformas correctos | 0 |

No se regeneró antes del baseline. `git status --short`/`git diff --stat`
identificaron los tres cambios ajenos de `inventory.md`, conservados durante el
ajuste. El baseline de los dos archivos ajenos rastreados fue 11 inserciones y
10 eliminaciones agregadas; esa misma estadística permaneció después.

## RED observado antes de cambiar fuentes (tarea 2.1)

Se modificaron primero los tests contractuales. Ejecución por agente delegado con
fuentes canónicas, adapters y generated todavía sin cambios:

| Comando | Resultado observado | Retorno |
| --- | --- | --- |
| `python3 -B tools/test_model_recommendations.py` | 331/456 PASS, 125 FAIL | 1 |
| `python3 -B tools/test_sdd_contract.py` | 292/323 PASS, 31 FAIL | 1 |
| `python3 -B tools/test_code_review_contract.py` | 8 tests; 4 subtests fallidos del contrato de modelo | 1 |
| `python3 -B tools/test_handoff_contract.py` | 33 tests OK | 0 |
| `python3 -B tools/validate.py` | Paridad vigente correcta | 0 |

Causas relevantes: fuentes con `Hard stop`, `termina el turno`, espera de
«continúa»/«listo», deduplicación condicionada a confirmación/reanudación e inicio
de Quick Plan/Verification bloqueado por avisos. También se detectó ausencia del
encabezado informativo nuevo; no se usa ese fallo estructural como único RED.
El selector de handoff acepta el encabezado anterior/nuevo, preservando semántica.

## GREEN e integración observados (tareas 2.1 y 4.1)

Después de modificar fuentes, adapters y documentación, el coordinador ejecutó
esta secuencia desde raíz, todos los comandos con retorno 0:

```bash
python3 -B tools/render.py && python3 -B tools/test_model_recommendations.py && python3 -B tools/test_sdd_contract.py && python3 -B tools/test_code_review_contract.py && python3 -B tools/test_handoff_contract.py && python3 -B tools/validate.py && git diff --check
```

| Check | Resultado observado |
| --- | --- |
| Recomendaciones de modelo | 456/456 comprobaciones correctas |
| Contrato SDD | 323/323 comprobaciones correctas |
| Code Review | 8 tests OK, incluidos controles de micro-remediación |
| Handoff | 33 tests OK, parser y permisos sin modificación |
| Validate | 10 skills y 8 agentes en 5 plataformas; render reproducible |
| Diff check | Sin errores de whitespace |

El renderer propagó 24 fuentes canónicas modificadas a 120 archivos derivados
en Copilot, OpenCode, Kiro, Claude y Pi. Las cuatro descripciones de adapter se
propagaron a sus agentes correspondientes. No se editaron derivados a mano.
No se añadió infraestructura ni dependencia; refactor limitado a selección de
secciones/assertions en los tests.

## Artefactos por tarea

| Tarea | Evidencia en disco / check |
| --- | --- |
| 1.1 | Baseline de esta sección y comandos arriba; estado ajeno documentado en `inventory.md` |
| 2.1 | `tools/test_model_recommendations.py`, `test_sdd_contract.py`, `test_code_review_contract.py`, `test_handoff_contract.py`; siete agentes, ocho skills y nueve referencias canónicas del inventario; RED/GREEN arriba |
| 3.1 | `adapters/{opencode,copilot,claude,pi}/agents/documentation-orchestrator.json`: diff exclusivamente de `description` |
| 3.2 | `README.md`, fichas `docs/agentes/` y docs/smokes activos del inventario; estados explícitos de smokes no ejecutados |
| 4.1 | `generated/{copilot,opencode,kiro,claude,pi}/`; render + tests focalizados + validate + diff check arriba |

Revisión de integración solo lectura por agente independiente: sin hallazgos
concretos en el diff de fuentes, adapters, documentación y tests. Revisión estática
de alcance medio, no evidencia de conducta LLM ni sustituto de Verification.

Inspección dirigida de fuentes/docs no encontró mandatos restantes de pausa
exclusivamente por modelo. Las coincidencias de confirmación corresponden a reglas
no bloqueantes o controles reales. Conservaron sin modificación el parser de
handoff, instaladores, Git/release, permisos técnicos y specs históricas.

## Pendiente y limitaciones

- Tarea 5.1: suite completa, check de enlaces, auditoría RNF, matriz de
  `verification.md` y Gate 4; aún no ejecutados como Verification.
- Smokes conversacionales del contrato nuevo: definidos, no ejecutados en hosts.
  Los checks textuales no acreditan continuidad real del LLM.
- Sin instalación global, commit, push ni release. Los hosts instalados no se
  actualizan solo por modificar el checkout; deben cargar el kit actualizado.
- La sesión actual conserva sus instrucciones iniciales, incluida la pausa antes
  de Verification. No se sustituye retroactivamente el prompt del host al editar
  `canonical/` o `generated/`.
