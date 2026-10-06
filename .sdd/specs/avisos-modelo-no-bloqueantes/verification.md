# Verificación — Avisos de modelo sin pausas redundantes

- Modo SDD: standard
- Fase: Verification
- Estado: verificado en fuentes y distribución; pendiente de aprobación de cierre
- Gate aprobado: Gate 1 — «procede» tras Requirements
- Gate aprobado: Gate 2 — «procede» tras Design
- Gate aprobado: Gate 3 — «procede» tras Tasks
- Gate pendiente: Gate 4
- Fecha: 2026-10-05
- Inicio de Verification: usuario «continúa» tras resumen de Implementación

## Resultado y alcance de la afirmación

**Suite automatizada y revisión estática conformes.** Las fuentes activas y los
derivados de cinco hosts expresan avisos de modelo no bloqueantes, conservando
decisiones, gates y autorizaciones reales. No hay tareas `[x]` sin artefacto o
evidencia asociada.

Este resultado valida el contrato textual, los contratos Python y el pipeline de
distribución. **No acredita conducta conversacional real del LLM**: los smokes
nuevos están definidos, pero no ejecutados en hosts. No se ha instalado el kit en
la configuración global del usuario ni se ha reiniciado su host.

## Ciclo de pruebas

- Estrategia: TDD focalizado del contrato textual modificado; regresión de las
  salvaguardas y del pipeline existentes.
- Baseline: modelo 141/141; SDD 213/213; Code Review 7 tests; Handoff 33 tests;
  validate correcto, antes de modificar fuentes/pruebas y sin render previo.
- RED: modelo 125 fallos de 456 checks; SDD 31 de 323; cuatro subtests fallidos
  de Code Review. Causas: mandatos de pausa/reanudación por modelo y deduplicación
  basada en confirmación, además del encabezado antiguo. No se atribuye el RED
  únicamente a cambios estructurales ni a paridad desactualizada.
- GREEN de implementación y retornos/comandos: `implementation-evidence.md`.
- Suite de Verification: tabla siguiente. Se ejecutó inicialmente completa y se
  repitió después de corregir dos detalles documentales detectados por la auditoría.
- PBT omitido: no hay invariante algebraico nuevo; no se añadió dependencia.

## Suite final observada

Comandos individuales desde raíz, invocados con `python3 -B`. Todos con retorno 0
en la repetición final, después de `python3 -B tools/render.py`.

| Comando | Resultado final |
| --- | --- |
| `python3 -B tools/test_integrity.py` | 391/391 comprobaciones |
| `python3 -B tools/test_links.py` | 4/4 pruebas |
| `python3 -B tools/test_model_recommendations.py` | 456/456 comprobaciones |
| `python3 -B tools/test_sdd_contract.py` | 323/323 comprobaciones |
| `python3 -B tools/test_handoff_contract.py` | 33 tests OK |
| `python3 -B tools/test_code_review_contract.py` | 8 tests OK |
| `python3 -B tools/test_validate.py` | 16/16 checks de pruebas negativas |
| `python3 -B tools/test_install.py` | 124/124 comprobaciones, HOME temporal |
| `python3 -B tools/test_mas_identity.py` | 223/223 comprobaciones |
| `python3 -B tools/validate.py` | 10 skills, 8 agentes, 5 plataformas; paridad correcta |
| `python3 -B tools/check_links.py` | 69 archivos Markdown revisados; sin enlaces rotos en su alcance |
| `git diff --check` | Sin errores de whitespace |

Las pruebas negativas de validate emiten errores deliberados de fixtures inválidos:
su resultado global 16/16 y retorno 0 acredita que los rechazan, no un fallo del kit.
Los tests de instalación usan HOME temporal y no actualizan la instalación global.
La comprobación PowerShell de esa suite es estática; no se declara ejecución Windows.

## Trazabilidad de requisitos

Los estados conformes siguientes se refieren al contrato en fuentes/distribución;
la validación conversacional en hosts permanece no ejecutada en todas las filas.

| Requisito | Tareas | Tests/checks | Evidencia | Estado |
| --- | --- | --- | --- | --- |
| R1 — Avisos no bloqueantes y cambio manual | 2.1, 3.1, 3.2, 4.1, 5.1 | `test_model_recommendations.py`: especialistas, Orchestrator, Navigator; `test_sdd_contract.py` | `canonical/agents/`, ocho skills actualizadas y sus referencias; adapters del Orchestrator; GREEN 456/456 y 323/323 | Conforme textual |
| R2 — Preflight barato, nivel sin pausa y deduplicación | 2.1, 3.2, 5.1 | Assertions por sección/fuente de continuidad, deduplicación y límites de contexto; auditoría dirigida | Cinco `references/model-selection.md` de especialistas; SDD model-selection; Orchestrator workflows; Navigator bootstrap; `docs/model-recommendations-smoke.md` | Conforme textual |
| R3 — SDD conserva gates reales | 2.1, 3.2, 4.1, 5.1 | `test_sdd_contract.py`: Gates 1–4, Quick Plan, próxima fase, planificación sola, reclasificación e integridad | `canonical/agents/sdd.md`, `canonical/skills/sdd-spec/{SKILL.md,references/model-selection.md,references/integrity-gate.md}`; `docs/sdd-smoke.md`; 323/323 | Conforme textual |
| R4 — Autorizaciones, decisiones y permisos intactos | 1.1, 2.1, 3.1, 4.1, 5.1 | Handoff 33 tests, Code Review 8 tests, assertions SDD y revisión de diff | Parser sin cambio; tests de scopes/confirmación/evidencia; Quality/Security conservan micro-pasos; adapters cambian solo description; Git/release e instaladores sin diff | Conforme estático y contratos Python |
| R5 — Consistencia de fuentes y cinco hosts | 1.1, 2.1, 3.1, 3.2, 4.1, 5.1 | Render, validate, enlaces, integridad, instalación temporal e identidad MAS | `generated/{copilot,opencode,kiro,claude,pi}/`; docs activos; todos los comandos de suite con retorno 0 | Conforme pipeline |

## Integridad de tareas

| `[x]` | Artefacto/comando que acredita la tarea |
| --- | --- |
| 1.1 | Baseline con comandos y retornos en `implementation-evidence.md`; inventario de estado inicial |
| 2.1 | Cuatro tests modificados, fuentes canónicas y ciclo RED/GREEN documentado; suite final verde |
| 3.1 | Diff solo `description` en los cuatro adapters de Documentation Orchestrator |
| 3.2 | README, fichas y documentos/smokes activos del inventario, incluido deslinde histórico Navigator |
| 4.1 | Árboles generated presentes; comparación por hashes contra render temporal en validate verde |
| 5.1 | Esta matriz, suite final, auditoría RNF y propuesta de Gate 4 |

Revisión independiente de solo lectura contrastó los cinco primeros `[x]` con
disco/evidencia. Baseline y RED son registros compactos de ejecución: no se infiere
su orden temporal exclusivamente del checkout final. No se marcan smokes nuevos
como aprobados a partir de tests textuales o evidencias antiguas.

## Self-check RNF de Design

| RNF | Evidencia | Resultado |
| --- | --- | --- |
| Coherencia | Búsqueda dirigida en canonical/docs/adapters/README de hard stop, fin de turno, espera, reanudación, confirmación y Gate 0; revisión por secciones y assertions positivas/negativas | Conforme: sin mandatos activos de pausa exclusivamente por modelo |
| Seguridad | Diff adapters solo descripciones; `git diff --name-only` vacío para parser de handoff, scripts, Git/release y adapters Kiro; Handoff 33 tests y Code Review 8 | Conforme: no ampliación de permisos ni transferencia de autorización a remediación |
| Reproducibilidad | `tools/validate.py` compara cada árbol generated con render temporal por hashes; cinco hosts correctos tras regeneración final | Conforme |
| Contexto proporcional | Presupuestos de matrices y carga selectiva conservados; assertions de tests verdes y auditoría de referencias | Conforme: no referencias globales obligatorias ni infraestructura nueva |

Conteos de palabras observados por auditoría: Architecture 176, Data 178, UI 178,
Quality 180 y Security 186 (máximo 230 por referencia); SDD 413 (máximo 450).
Son palabras, no estimaciones de tokens. La carga bajo demanda se mantiene.

### Quality bar

- Separación canonical/adapters/generated conservada; no edición manual de derivados.
- Sin lógica nueva de UI, DI, persistencia, red, singletons ni errores runtime:
  no aplica añadir esas capas para resolver una pausa de prompt.
- Cambio mínimo de contenido/tests; parser y permisos no se modifican como atajo.
- Estrategia de pruebas y excepciones identificadas; evidencia no tautológica.
- Cuatro RNF del propio diseño revisados; no se inventan RNF de producto ajenos.

## Hallazgos menores resueltos durante Verification

1. **Ejemplo de handoff:** se retiró `Gate0 aprobado` de `gate_state` en
   `canonical/skills/documentation-orchestrator/references/handoff.md`, dejando
   `plan global aprobado`. No se cambiaron campos, tabla de confirmación, parser ni
   permisos. Se regeneraron las cinco copias y se repitió la suite completa.
2. **Smoke Navigator:** se añadió una advertencia explícita de que sus resultados
   de agosto son evidencia histórica MVP y no validan el contrato nuevo. Se cambió
   únicamente la etiqueta final a «Resultado histórico del MVP», sin reescribir
   los resultados anteriores.

## Límites y preservación

- Smokes nuevos en Copilot, OpenCode, Kiro, Claude y Pi: **no ejecutados**. Queda
  pendiente comprobar continuidad efectiva del LLM, incluido el caso UI de la
  captura, al cargar el kit actualizado en un host real.
- No se declara sandbox universal del host ni equivalencia entre permiso lógico
  de handoff y enforcement técnico.
- No se editan specs históricas, CHANGELOG, configuración global ni cambios de
  laboratorio ajenos. Se observó evolución externa del diff del archivo de tareas
  del laboratorio durante la auditoría; se dejó fuera del ajuste. No se afirma
  identidad byte a byte de cambios concurrentes ni se atribuyen a esta feature.
- Sin commit, push, tag, release ni instalación global. La sesión actual sigue
  usando su prompt inicial, no el contenido nuevo por auto-reemplazo.

## Gate 4

Propuesta: cerrar la spec para el **alcance de fuentes, contratos y distribución
verificado**, dejando explícito que no se ha validado la conversación en hosts ni
actualizado la instalación del usuario. No hay fallos automatizados pendientes.
Esperar aprobación de cierre; no inferirla por este archivo ni por la suite verde.
