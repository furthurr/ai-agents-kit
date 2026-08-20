# Smoke test de Documentation Orchestrator

Validación manual mínima del agente y la skill en cualquiera de las plataformas
soportadas. Ejecuta las pruebas en un repositorio desechable o con cambios bajo
control; algunos escenarios escriben documentación tras varios gates.

## Precondiciones

1. Ejecuta `python3 tools/render.py` y `python3 tools/validate.py` en este kit.
2. Instala o copia los artefactos generados de la plataforma de prueba.
3. Reinicia la herramienta para cargar agente y skill.
4. Selecciona `documentation-orchestrator`.

## 1. Gate 0 en status

Prompt:

```text
Comprueba si la documentación está actualizada.
```

Esperado:

- Detecta `status` y realiza solo preflight superficial.
- Recomienda normalmente modelo `bajo` con razones verificables.
- Se detiene antes de completar el status.
- No escribe archivos.

Responde `continúa con el actual`. Debe completar el inventario sin escribir.

## 2. Bootstrap core

Prompt:

```text
Inicializa la documentación core del proyecto.
```

Esperado:

- Selecciona únicamente `.navigator/` y `.architecture/`.
- Recomienda modelo `medio` o `alto` según tamaño y espera.
- Tras confirmar modelo, presenta un plan global y espera aprobación de escritura.
- Conserva los gates de Project Navigator y Architecture.
- No crea `.data/`, `.design/`, `.quality/` ni `.security/`.

## 3. Sync existing con Quality

Prepara un repo que tenga `.navigator/`, `.architecture/` y `.quality/`, pero no
`.data/` ni `.design/`. Prompt:

```text
Actualiza las carpetas documentales que ya tenemos.
```

Esperado:

- Detecta `sync-existing`.
- Selecciona solo las tres carpetas existentes.
- Recomienda las ausentes aplicables sin crearlas.
- Mantiene el gate de alcance de Quality y no remedia código.
- Actualiza Navigator al final si corresponde.

## 4. Alias y cambio de alcance

Prompt:

```text
Ejecuta sync-check.
```

Esperado: interpreta `status`, no `release-check`, recomienda modelo y espera.

Antes de confirmar, responde:

```text
Mejor actualiza solo arquitectura y seguridad.
```

Esperado: recalcula como `sync-domain`, vuelve a recomendar nivel y espera otra
confirmación.

## 5. Release check

Prompt:

```text
Comprueba si el proyecto está listo para una release.
```

Esperado:

- Selecciona `release-check`, normalmente con modelo `bajo`, y espera.
- Después solo lee documentación y findings existentes.
- No reescanea código, no genera changelog, no versiona y no crea tags.
- Devuelve `APTO`, `APTO CON ADVERTENCIAS` o `NO APTO` con evidencia.
- Un finding `Crítica` de Security o `Blocker` de Quality produce `NO APTO`.
- Cualquier core distinto de `Vigente` o cambio local relevante produce `NO APTO`.
- Un Navigator legado sin `source_commit` queda `No verificable` hasta ejecutar
  un update que establezca un baseline Git limpio.

## 6. Límites

Solicita una feature, un bugfix, una release y Graphify. El agente debe redirigir
respectivamente a SDD, Git & Release Manager o Graphify sin modificar `.sdd/`,
`.release/`, `graphify-out/` ni código de producto.

## Criterio de cierre

La prueba pasa si todos los modos aplican Gate 0, ninguna operación comienza sin
confirmación explícita, las skills especialistas conservan autoridad y no aparece
una carpeta `.documentation/`.
