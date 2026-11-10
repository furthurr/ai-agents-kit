# Incidente de la regla comodín en `permission`

**Fecha:** 2026-11-09
**Brazo afectado:** gentle-ai (primer intento)
**Estado:** corregido; el resultado final es el PASS de `resultados.json`.

## Síntoma

El primer intento de gentle-ai terminó con **0 archivos**, 3 pasos y el oráculo
en FAIL. El orquestador delegó a `gentle-ai-worker`, que devolvió `blocked`:
«this runtime provides no file-read, file-write, or shell tools». Un mensaje
equivalente apareció al probar directamente los agentes `build` y `gentleman` de
su perfil: el modelo decía que `apply_patch` no estaba disponible.

## Diagnóstico A/B

Se reprodujo con perfiles aislados y trazas en `_probe/`:

1. El mismo sandbox y el mismo modelo funcionan en `v2_reforzado`: su agente
   `build` crea un archivo con `apply_patch`.
2. En un perfil de gentle-ai con `permission: {}` la herramienta vuelve a
   aparecer y el archivo se crea (`_probe/gentle-noperm.jsonl`).
3. En el perfil de `v2_reforzado`, mover `"*": "deny"` al **final** del objeto
   `permission` hace desaparecer `apply_patch` (`_probe/v2-starlast.jsonl`).
   Devolverlo al **principio** lo restaura.

Conclusión: OpenCode evalúa la regla comodín con semántica de última
coincidencia. Si `"*": "deny"` queda al final, anula las reglas explícitas de
`read`/`edit`/`write` y las herramientas de archivo no se ofrecen a la sesión.
Era un defecto del **runner**, no del arnés.

## Corrección

`merge_sandbox` ahora reconstruye el objeto `permission` con `"*"` como primera
clave, antes de `read`, `edit`, `write` y `bash`. Se reinstaló el perfil de
gentle-ai y se repitió solo ese brazo.

Resultado final de gentle-ai:

- PASS de oráculo y suite original.
- 3 archivos esperados, 0 fuera de alcance.
- 90,7 s, 274.726 tokens, 10 pasos.

## Evidencia

- `_probe/gentle-noperm.jsonl` y `_probe/gentle-onlybuild/`: el sandbox sin
  `permission` permite escribir.
- `_probe/v2-starlast.jsonl`: el mismo perfil con la comodín al final falla.
- `_probe/gentle-config.json` y `_probe/v2-config.json`: configuración resuelta
  comparada.
- `task_1/evidence/gentle-ai-{install,preflight,run,eval}.json` y
  `gentle-ai-events.jsonl`: ejecución final corregida.

La traza del primer intento fue reemplazada por la repetición; el síntoma queda
documentado aquí y en las trazas de diagnóstico.
