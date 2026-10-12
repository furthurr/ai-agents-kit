# Verificación — F10 Developer Agent Experimental

- Modo SDD: lite
- Resultado de implementación: completado
- Puertas SDD: no aplican en Lite; no se añadieron Gates 1–4

## Evidencia compacta

| Requisito | Evidencia | Resultado |
|---|---|---|
| R1 — F10 exclusivo, snapshot nuevo, perfil renderizado y cuatro herramientas | `test_pilot.py`, `test_pilot_cli.py`, `test_developer_profile.py`, `test_opencode_actor.py`; perfil/política en el run de fixture | PASS |
| R2 — método propio Developer, aprobación humana no simulada, texto final, `plan_only`/`no_delivery` sin evaluación | `test_developer_profile.py`, `test_opencode_actor.py`, `test_fake_actor.py` | PASS |
| R3 — guard AST, primera entrega, exportación solo `feature.py`, evaluador aislado y recibos | `test_pilot.py`, `test_delivery.py`, `test_fake_actor.py`; `criteria.json` del fixture Docker | PASS |
| Dry-run integral | `runs/pilot-781ced4a-9d16-44f6-b437-b34fe7674f5c/` | PASS como fixture; no es resultado LLM |

## Comandos y resultados

- Suite pertinente completa: `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest runner/tests snapshots --import-mode=importlib -m 'not acceptance' -q` — **1060 passed, 2 skipped, 1 deselected**.
- Pruebas focalizadas de perfil/runner/CLI/actor/fixture/entrega — **286 passed**.
- `python3 -m compileall -q runner/src runner/tests evaluation` — PASS.
- `git diff --check` — PASS.
- `python3 lab.py pilot dry-run --mode developer-agent-experimental --feature F10` — PASS; Docker, actor falso, `model_calls=0`, `opencode_invocations=0`, `benchmark_results=false`, `fixture=true`, evaluación externa F10 **6/6**. Tiempo total: 488.621 s. No se usó OpenCode para invocar un modelo.

La RED/GREEN observada en el dry-run es la del test público F10 contra el snapshot
inicial y la referencia confiable de fixture. No se presenta como TDD del candidato
LLM ni del harness. No se atribuye un resultado experimental al modelo.

## Límites y excepciones

- No se ejecutó el agente Developer real, no se preparó autenticación, no hubo llamada
  a modelo, gasto ni launch.
- Por ser fixture, modelo/variante efectivos son `null`; `dryrun/fixture` y
  `dryrun-fixture` son los valores de prueba, no una selección de modelo.
- El primer intento de fixture (`pilot-241a4c08-0d6f-453f-958c-cfbb76234e8f`) fue
  interrumpido por el timeout externo de 300 s mientras evaluaba. Se preservó como
  incompleto, sin criterios ni veredicto funcional; el contenedor propio se retiró
  tras confirmar su etiqueta de propiedad. El segundo run completo usa un ID nuevo.
- Una ejecución LLM futura necesita autorización separada, selección/telemetría
  efectivas y revisión F10 vigente; este dry-run no los certifica.
