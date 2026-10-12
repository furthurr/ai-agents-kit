# Verificación — Condición experimental F10 sin SDD

- Modo SDD: standard
- Fase: Verification
- Estado: evidencia completada; spec cerrada
- Gate 1: aprobado
- Gate 2: aprobado
- Gate 3: aprobado
- Gate 4: aprobado por el usuario («continua») tras la solicitud conjunta de cierre y kickoff
- Alcance de verificación: runner y dry-run F10 sin invocaciones a modelos

## Resultado de implementación

Se añadió la condición experimental `no-sdd`, limitada a F10. El runner entrega una
sola tarea directa; no exige fases ni documentos SDD, lleva `canonical_sdd_sha256`
como null solo en esa condición y evalúa la primera entrega con el grader reservado
F10 en un contenedor separado. El resumen etiqueta la condición y registra hashes
de prompt, contrato, snapshot y entrega. Un validador AST rechaza cambios fuera de
los cuerpos de `Saga.submit`, `Saga.step` y `Saga.get` sin importar/ejecutar código
candidato en el host.

No se lanzó el modelo ni se autoriza un nuevo intento real por esta verificación.

## Ciclo TDD y pruebas

- RED request/prompt: los tests nuevos fallaron inicialmente por modo no admitido y
  prompt aún no directo (2 fallos observados); después pasaron.
- RED scope guard: 5 casos fallaron inicialmente porque no existía el validador AST;
  luego los casos válidos y las mutaciones fuera de alcance pasaron.
- GREEN focal: `test_pilot.py`, `test_pilot_cli.py`, `test_opencode_actor.py`,
  `test_fake_actor.py` y `test_review_gate.py` → **231 passed** en el último grupo
  dirigido anterior a la suite total.
- Suite final, desde `.agent-lab/sdd-escalation/`:

  ```sh
  PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest runner/tests snapshots --import-mode=importlib -m 'not acceptance' -q
  ```

  Resultado: **1008 passed, 2 skipped, 1 deselected** (47.63 s). Los dos skips son
  tests públicos X13 que requieren Docker en sus propios fixtures; la aceptación
  pública inicial F10 permanece excluida por su RED intencional en el scaffold.
- `python3 -m compileall -q runner/src runner/tests` → pasó.
- `git diff --check` → pasó.

## Dry-run F10 con Docker (cero modelos)

Comando:

```sh
python3 .agent-lab/sdd-escalation/lab.py pilot dry-run --mode no-sdd --feature F10
```

Evidencia final: `.agent-lab/sdd-escalation/runs/pilot-0f90cd5e-5fa4-48aa-8acc-d66d5ffe72f0/`.

| Check | Evidencia | Resultado |
|---|---|---|
| Una tarea y fase sin planificación SDD | `summary.json`: `phase_counts.no-sdd = 1`; `sdd_stages_required = false`; `canonical_sdd_sha256 = null` | ✅ |
| Evaluación reservada F10 completa | `criteria.json`: F10-01 a F10-06 | 6/6 ✅ |
| Separación de condición | `summary.json`: `condition = no-sdd`, `transitions = none_direct` | ✅ |
| Naturaleza del resultado | `source = fake_reference_fixture`, `benchmark_results = false` | Cero benchmark ✅ |
| Consumo del modelo | `model_calls = 0`, `opencode_invocations = 0`; coste/tokens N/A | Cero llamadas ✅ |
| Integridad de evidencia | `snapshot_digest`, `contract_sha256`, `condition_prompt_sha256`, digest de primera entrega presentes | ✅ |
| Contenedores | `docker ps -a --filter label=org.sdd-lab.owner` vacío al finalizar | Cleanup ✅ |

Este dry-run ejercita el harness y el evaluador con la fixture de referencia confiable;
**no es un resultado de LLM ni un benchmark de la condición no-SDD**.
La calibración previa del mismo evaluador documenta referencia 6/6, skeleton 0/6 y
fixture incorrecta 0/6, sin invocaciones a modelos:
`runs/f10-calibration-adc8772351ac4ffbad57856b9fb57007/report.json`.

Una ejecución preliminar `pilot-e36b9ccd-3c5a-43e7-a006-fb6cf53ca10b` fue interrumpida
por el timeout externo de la herramienta durante evaluación. Conserva estado `running`
sin `process.json`; no se cuenta como verificación ni benchmark. Su contenedor de
evaluación se identificó por etiqueta de ownership y se eliminó; el dry-run final
independiente anterior completó correctamente.

## Matriz Req → Task → Test → Evidencia

| Req | Task(s) | Test/check | Evidencia | Estado |
|---|---|---|---|---|
| R1.1, R3.1 | 1.1 | `test_no_sdd_request_is_f10_only`; `test_no_sdd_rejects_other_feature_before_side_effects` | `runner/tests/test_pilot.py`; suite final | ✅ |
| R1.2, R2.2–R2.3 | 1.2, 1.3 | `test_no_sdd_prompt_is_one_integral_task_without_sdd_artifacts`; `test_no_sdd_actor_accepts_null_hash_without_sdd_policy` | `pilot-0f90.../summary.json`, `runner/tests/test_opencode_actor.py` | ✅ |
| R1.3, R3.2, R3.4 | 2.2 | `test_f10_scope_guard_accepts_only_changes_inside_target_method_bodies`; `test_f10_scope_guard_rejects_changes_outside_target_bodies`; `test_no_sdd_rejects_out_of_scope_ast_without_evaluation` | `runner/tests/test_pilot.py` | ✅ |
| R1.4–R1.5, R3.3 | 2.1 | `test_no_sdd_runs_one_direct_phase_and_evaluates_f10_without_sdd_docs`; tests de límite/entrega parcial | suite final y run final | ✅ |
| R2.1, R2.4 | 2.3, 3.2 | grader externo y separación de contenedores | `pilot-0f90.../criteria.json`, `observations.json`, `report.json` | ✅ |
| R2.2–R2.3, R3.4–R3.5 | 3.1 | `test_no_sdd_cli_is_f10_only_and_has_no_sdd_hash` | `pilot-0f90.../summary.json` | ✅ |
| R3.1–R3.2 | 1.3, 3.3–3.4 | tests de autorización/actor y `test_f10_review_binds_direct_mode_runner_and_stale_review_blocks` | `runner/tests/test_review_gate.py`; suite final | ✅ |

## Self-check RNF

| RNF | Evidencia | Estado |
|---|---|---|
| RNF-1: cero llamadas a modelos en implementación/dry-run | `summary.json` con ambos contadores en cero y fixture explícita | ✅ |
| RNF-2: candidato no se importa/ejecuta en host | comparación AST de texto; generación y evaluación en contenedores separados; suite RPC/entrega | ✅ |
| RNF-3: evidencia identificada por run y hashes | `report.json`, `snapshot.json`, `delivery` y `criteria.json` del dry-run | ✅ |
| RNF-4: secretos/excepciones no se exponen | tests existentes de sanitización del actor/CLI dentro de la suite total | ✅ |
| RNF-5: límites/fallos no se convierten en falso éxito | tests de entrega en límite, timeout, scope inválido y evaluación incompleta | ✅ |

## Limitaciones y condiciones para lanzamiento real

- La revisión F10 previa queda obsoleta porque sus fingerprints cubren módulos del
  runner que cambiaron. El test confirma que el review gate bloquea un fingerprint
  stale. Antes de un launch real debe instalarse una revisión vigente para
  `pilot-F10`; no se creó ni se afirma una revisión nueva aquí.
- El dry-run usa la implementación de referencia confiable: no mide el desempeño
  del modelo. Un run real requiere modelo/variante exactos, presupuesto/límites,
  autenticación opt-in y autorización explícita de kickoff propia.
- El timeout preliminar está preservado como ejecución interrumpida, no se reanudó ni
  se sobrescribió.

**Gate 4 — pendiente:** ¿Cierro esta spec o quieres cubrir algún hueco?

Esta pregunta histórica queda resuelta por la aprobación registrada al final.

## Reanudación y revisión vigente — 2026-10-09

- Se revisaron las fuentes actuales completas de `pilot.py`, `pilot_cli.py`,
  `opencode_actor.py` y `review_gate.py`, los cuatro módulos cuyos fingerprints
  difieren del registro F10 anterior. Los otros 20 fingerprints coinciden,
  incluido contrato/scaffold/evaluador/configuración calibrada.
- Informe técnico nuevo y local:
  `.agent-lab/sdd-escalation/results/f10-no-sdd-technical-review-2026-10-09.md`.
  Registro vigente: `runtime/pilot-review-f10.json`; registro anterior preservado
  íntegro en `runtime/pilot-review-f10-2026-10-07.json`. No se ejecutó el script
  histórico `f10_review_record.py` ni se usó un waiver.
- Se reejecutó la suite exacta de esta verificación: **1008 passed, 2 skipped,
  1 deselected in 45.99s**. Compileall y `git diff --check` pasaron.
- `load_image` validó configuración/fuentes y Docker confirmó que la imagen
  evaluadora calibrada está disponible; no había contenedores con label de
  ownership del laboratorio. No se repitió el dry-run ni la calibración.
- Se consultó `pilot prepare --help` y `pilot launch --help`; no se ejecutó
  preparación del actor ni inferencia. Cero llamadas reales en esta reanudación.
- La selección histórica de standard para construir esta extensión no quedó
  suficientemente justificada frente a evaluar lite. Se conserva la decisión
  histórica y sus aprobaciones; no se reabre planificación ni se traslada SDD al
  candidato experimental.
- Gate 4 continúa pendiente de aprobación explícita, que se solicita conjuntamente
  con configuración y autorización del único intento real. Evidencia lista para
  cierre; la revisión técnica no autoriza gasto ni modelos.

## Cierre y autorización posterior — 2026-10-10

El usuario respondió «continua» a la solicitud conjunta de cierre de Gate 4 y
autorización del único intento real con la configuración expuesta. Gate 4 aprobado;
esta spec de extensión del laboratorio queda cerrada. No se imponen gates al candidato.

Kickoff autorizado: F10 / `no-sdd`, `openai/gpt-6-luna` / `max`, 1200 segundos
totales incluyendo evaluación, 32 pasos, USD 1 reportado blando con aceptación de
que no garantiza facturación, tokens sin tope y auth existente OpenCode mediante
opt-in. Un intento independiente, primera entrega, sin feedback reservado ni
reparación. Preparar y atestar selección exacta antes de launch; si no está
disponible, detenerse sin sustitución. Los resultados se registrarán separadamente
bajo un run nuevo del laboratorio; no se modifica evidencia histórica.

## Resultado de la operación posterior autorizada

El único intento real autorizado terminó el 2026-10-10: run
`pilot-98910efc-094a-4b0b-91d8-72ebd476a9a2`, `no-sdd`, Luna/max,
**success 6/6 externos**, 700.986671 s totales, 10 pasos, una invocación,
145364 tokens y USD 0 reportados (no facturación). Preparación exacta
`prepare-78080a10-acff-4343-909e-cd381e5e195b`, sin inferencia.

Informe separado:
`.agent-lab/sdd-escalation/results/f10-first-real-no-sdd-pilot.md`.
Entrega, recibo, observaciones, auditoría de integridad y respuesta final disponible
se conservaron bajo ese run. No hubo reparación ni otro intento real. La spec de
extensión continúa cerrada; este resultado no cierra la spec principal/campaña ni
permite inferir confiabilidad o atribuir diferencias exclusivamente a SDD.
