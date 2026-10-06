# Smoke test de Documentation Orchestrator

Validación manual mínima del agente y la skill en cualquiera de las plataformas
soportadas. Ejecuta las pruebas en un repositorio desechable o con cambios bajo
control; algunos escenarios escriben documentación tras varios gates.

## Precondiciones

1. Ejecuta `python3 tools/render.py` y `python3 tools/validate.py` en este kit.
2. Instala o copia los artefactos generados de la plataforma de prueba.
3. Reinicia la herramienta para cargar agente y skill.
4. Selecciona `documentation-orchestrator`.

## 1. Preflight informativo en status

Prompt:

```text
Comprueba si la documentación está actualizada.
```

Esperado:

- Detecta `status` y comienza con un preflight superficial.
- Recomienda normalmente modelo `bajo` con razones verificables.
- Continúa con inspección e informe en el mismo turno, sin esperar por modelo.
- No escribe archivos.

Debe completar el inventario sin escribir ni exigir `continúa con el actual`.

## 2. Bootstrap core

Prompt:

```text
Inicializa la documentación core del proyecto.
```

Esperado:

- Selecciona únicamente `.navigator/` y `.architecture/`.
- Recomienda modelo `medio` o `alto` según tamaño de forma informativa.
- Presenta el plan global en el mismo turno y espera su aprobación de escritura,
  sin pedir confirmación del modelo.
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
- Reutiliza el plan autorizado para registrar findings de calidad verificados,
  sin pedir otro filtro de severidad; no remedia código ni agrega seguridad ausente.
- Actualiza Navigator al final si corresponde.

## 4. Alias y cambio de alcance

Prompt:

```text
Ejecuta sync-check.
```

Esperado: interpreta `status`, no `release-check`, recomienda modelo y completa
la inspección e informe sin esperar por el aviso.

En la siguiente petición, cambia el alcance:

```text
Mejor actualiza solo arquitectura y seguridad.
```

Esperado: recalcula como `sync-domain`, comunica el nivel actualizado si corresponde
y presenta el plan sin pausa por modelo. Espera solo por la aprobación de escritura
o una decisión real pendiente; una autorización anterior no cubre una ampliación.
Repite con un cambio exclusivo de nivel y el mismo alcance autorizado: informa y
continúa, sin nueva confirmación ni reanudación.

## 5. Release check

Prompt:

```text
Comprueba si el proyecto está listo para una release.
```

Esperado:

- Selecciona `release-check`, normalmente con modelo `bajo`, sin pausa por el aviso.
- En el mismo turno lee documentación y findings existentes y entrega el informe.
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

## 7. Handoff productor–receptor

Después del preflight informativo y del plan, solicita explícitamente continuar
con el agente Code Review real para una inspección documental de solo seguridad.

Esperado en el orquestador:

- Emite `## Handoff` con `target: code-review`, `scope: [.security/]`, `action: inspect`,
  `write_scope: none`, `requires_confirmation: false` y `status: pending`.
- Incluye `handoff_id`, `project_root` y referencias existentes relativas.
- No ejecuta la inspección localmente y marca el dominio pendiente.

Copia el bloque a Code Review. Esperado en el receptor:

- Rechaza un bloque con target distinto, ruta absoluta/`..`, acción desconocida o
  escritura incoherente.
- No interpreta `gate_state` como aprobación de sus gates.
- Para un bloque válido, ejecuta solo su alcance y devuelve `## Handoff Result`
  con el mismo `handoff_id`, `status`, `evidence` y `result_summary`.
- No repite el aviso de nivel ya comunicado para el mismo alcance; no exige una
  confirmación ni reanudación para deduplicarlo. Conserva decisiones y gates reales.

Devuelve el resultado al orquestador. Esperado: verifica la evidencia antes de
marcar el dominio completado. Repite al menos una vez con `action: sync` y
confirma que pide aprobación de escritura y no duplica la acción.
Si la misma escritura ya está autorizada en esa sesión, no vuelve a preguntar;
`gate_state` copiado por sí solo no acredita autorización. Para ambos dominios,
usa `scope: [.quality/, .security/]` y exige evidencia de cada dominio al sincronizar.

## Criterio de cierre

La prueba pasa si todos los modos aplican preflight informativo y continúan el
trabajo autorizado en el mismo turno, sin esperas exclusivas por modelo; las
escrituras conservan aprobación del plan global, las skills especialistas conservan
autoridad y no aparece una carpeta `.documentation/`. El handoff pasa solo si productor y receptor
cumplen el contrato, no duplican la acción y preservan los gates.

Escenarios del contrato nuevo definidos, no ejecutados en hosts. Registra evidencia
observada por plataforma; el preflight o los tests textuales no acreditan ejecución
conversacional. Los permisos del host y la validación técnica de evidencia siguen vigentes.
