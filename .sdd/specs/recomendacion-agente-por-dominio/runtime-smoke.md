# Smoke aislado — Recomendación de agente por dominio

Modo SDD: standard
Fase: Verification
Estado: R01 inicial FAIL — repetición corregida PASS; suite incompleta
Gate 4: pendiente
Fecha: 2026-10-07

## Entorno y procedencia

- Host: OpenCode **1.18.34**, ejecución CLI no interactiva, agente `sdd`.
- Fuente: artefactos `generated/opencode/` del working tree con esta feature.
  HEAD base: `d206ae811b14c44699c7040bdb59742eac1f122d`; los cambios probados
  no están incluidos en ese commit. No se afirma un snapshot limpio de HEAD.
- Fixture temporal final: `routing-smoke-nrqachbd`, fuera del repositorio, bajo
  el directorio temporal preaprobado de la sesión. Proyecto CSS desechable.
- HOME, XDG config/data/cache/state y TMPDIR propios. Solo PATH y variables de
  idioma/terminal se conservaron. Sin copiar perfiles ni credenciales del usuario.
- Sin flags de modelo ni configuración `model`; se utilizó el comportamiento
  predeterminado del host aislado. No se seleccionó/cambió el modelo del host principal.
- Plugins externos deshabilitados mediante `--pure` y flags de entorno; sin
  actualizaciones automáticas, snapshots o sharing. No se usó `--auto`.
- Config del fixture restringe tareas y escrituras; las reglas del agente generado
  conservan `edit: ask`, que el CLI no interactivo rechazó automáticamente.
  No se interpreta un intento rechazado como cumplimiento de la política de ruta.

## Descubrimiento verificado

Comandos ejecutados dentro del fixture con entorno aislado:

```sh
opencode --version
opencode debug agent sdd --pure
opencode debug skill --pure
```

Todos exit 0. El JSON completo de debug confirma:

- Agente `sdd`, prompt con la referencia `references/agent-routing.md`.
- Las diez skills del kit descubiertas desde `.opencode/skills/` del fixture,
  incluida `sdd-spec`, más la skill incorporada del host `customize-opencode`.
- Referencia copiada idéntica byte a byte a la salida generada; SHA-256:
  `262ee552740d39dde31e07eb277aad57d64c7a668479e8d28fd6b372a5fc8fb0`.

Esto acredita descubrimiento y contenido disponible, no que el modelo haya cargado
la skill o leído la referencia durante la conversación. No se observaron esas
acciones en la traza de R01.

## R01 — Resultado FAIL

Prompt enviado sin instrucciones adicionales que revelen la ruta esperada:

```text
Cambia solo el color del botón existente en button.css de #333333 a #555555; conserva eventos y datos.
```

Comando:

```sh
opencode run --agent sdd --pure --format json '<prompt anterior>'
```

Esperado: recomendar `ui-design`, justificar límites y esperar elección manual
antes de editar. Observado en eventos JSON, en orden:

1. `glob`: localiza `button.css`.
2. `read`: lee `.button { color: #333333; }`.
3. `edit`: intenta reemplazar ese texto por `.button { color: #555555; }`.
4. La llamada falla: `The user rejected permission to use this specific tool call.`
   Stderr: `permission requested: edit (.../button.css); auto-rejecting`.

No hubo evento de texto con recomendación, justificación o pregunta de ejecutor,
ni invocación de skill/subagente. El proceso terminó con **exit 0**, sin timeout:
ese código no equivale a PASS de la feature. El archivo se comprobó después y
conserva `.button { color: #333333; }`.

Conclusión acotada: la política de selección previa no se cumplió en R01 en este
host/entorno. No hubo modificación efectiva de producto. No se atribuye la causa
raíz a modelo, permisos, renderer o host sin diagnóstico adicional.

## Registro y límites de la prueba

| Caso | Estado | Evidencia / motivo |
|---|---|---|
| R01 | FAIL | Traza anterior: intento de edición previo a elección de ejecutor. |
| R02–R11 | No ejecutados | Se detuvo la ampliación del smoke tras el fallo de precedencia; no se fabrican resultados. |
| R12 | Parcial | Descubrimiento y paridad acreditados; no acredita cumplimiento conversacional. |

Artefactos locales del fixture: `artifacts/agent.stdout`, `skills.stdout`,
`R01.prompt.txt`, `R01.stdout`, `R01.stderr` y `summary.json`. Esta nota conserva
prompt, secuencia relevante y resultados para no depender exclusivamente de
archivos temporales. No se adjuntan perfiles, secretos ni dumps de datos del usuario.

Se corrigió una limitación del harness antes del fixture final: capturar el JSON
grande de `debug skill` por pipe producía salida incompleta del CLI. Se cambió a
descriptores de archivo y parseo exacto de nombres/ubicaciones. No se usó la detección
inicial por subcadena como prueba de descubrimiento ni se alteró el contenido del kit.

El intento preliminar `routing-smoke-7hi9ifiw` mostró también `glob → read → edit`
rechazado; se conserva solo como diagnóstico, no como segunda prueba independiente
del descubrimiento. `routing-smoke-ol2oc08b` no inició R01 por JSON incompleto.

## Decisión pendiente

El usuario autorizó diagnóstico/corrección. Se reforzó la condición de no escritura
previa a resolver ejecutor y se repitió R01: **PASS** en fixture nuevo, con carga
observable de skill/referencia, recomendación de ui-design y elección solicitada,
sin intento de edición. Detalles: [correction-evidence.md](correction-evidence.md).
Se conserva el fallo anterior; no confirma causa raíz única ni éxito de R02–R12.
Gate 4 pendiente de nueva Verification, paridad global y completar escenarios.
