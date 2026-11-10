# Incidentes previos a la cohorte GPT Luna max

1. Raíz temporal `odd-standards-luna-max-20261105`: el preflight exigía la
   herramienta `edit`; GPT Luna expuso `apply_patch`, además de bash/read.
   Falló la verificación estática antes de invocar celdas. Sin inferencia comparativa.
2. Raíz temporal `odd-standards-luna-max-20261105-v2`: el preflight de ODD cargó
   su skill y cambió READY a DONE, pero ejecutó unittest usando como workdir la raíz
   histórica y el host denegó la llamada. No se afirmó preflight verde. Se preserva
   `probe-odd.json` como evidencia, con errores saneados y sin secretos.
3. Raíz temporal `odd-standards-luna-max-20261105-v3`: preflight reconoce
   apply_patch e indica explícitamente el directorio del fixture; ambos perfiles
   pasan. Se congelan entradas y se ejecuta R1; la cohorte se detiene tras dos timeouts.

Las reglas de los agentes, tarea, permisos y oráculos no se retocaron entre perfiles.
La indicación adicional de workdir corresponde al preflight trivial, no al prompt
de las celdas. La evidencia histórica de preparación no se usa como repetición.
