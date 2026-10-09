# Continuidad y cambios de specs

Política bajo demanda para modificaciones relacionadas con specs existentes.
No es un clasificador runtime ni exige nuevos índices o archivos para todo cambio.

## Búsqueda localizada

Antes de recomendar profundidad, comprobar relación con acuerdos existentes:

1. Empezar por ruta explícita o spec activa conocida; validar ruta y marcadores.
2. Sin referencia conocida, buscar candidatas por módulo/rutas/comportamiento;
   no auditar toda `.sdd` rutinariamente ni leer todos sus documentos.
3. Leer modo, estado, gates y requisitos pertinentes; ampliar según dependencias.
4. Si hay varias candidatas o autoridad incompatible, preguntar antes de modificar.
5. Sin relación encontrada, continuar normalmente; no afirmar ausencia global con
   una búsqueda limitada. No crear una spec contradictoria por omitir la conocida.

Distinguir: implementar requisito, ajuste que conserva acuerdo, cambiar requisito,
bugfix o discrepancia documental. Código, steering y contratos reales sustentan
decisiones; no asumir que el código o la spec siempre tienen razón.

## Enmiendas y gates

Presentar ruta/ID, comportamiento actual/propuesto, motivo y dependencias afectadas.
Conservar ID si sigue siendo el mismo requisito; asignar ID nuevo a una adición e
identificar sustituciones con vínculo al acuerdo previo. Registrar delta breve,
sin duplicar documentos completos ni imponer un archivo de revisión universal.

Una nota baja no evade el modo/gates de una spec afectada. Implementar una tarea
existente conserva su flujo; direct no sustituye una tarea con aprobación pendiente.
Un ajuste trivial que conserva acuerdos y no evita una tarea/gate pendiente puede
evaluarse como direct sin nueva spec, con vínculo y evidencia proporcional.

Si se cambia un requisito vigente, preparar propuesta/en revisión. No implementar
el alcance nuevo hasta autorización y gates pertinentes; petición inequívoca puede
autorizar la enmienda lite, pero no aprobar por inferencia un gate standard.

- Standard: Gate 1 cubre requisito cambiado; revisar Gate 2/3 si afecta diseño/plan.
  Identificar aprobaciones afectadas y cuáles siguen válidas con motivo; no repetir
  todas ni reutilizar una aprobación que cubre comportamiento distinto.
- Lite: actualizar Quick Plan afectado con autorización, sin inventar Gates 1–4.
  Si deja de ser elegible, pedir reclasificación antes de continuar.
- Cierre de revisión standard: Gate 4 tras evidencia nueva, no por cierre anterior.

## Estado y evidencia

Revisar requisito → diseño → tarea → test/check → evidencia. Lo afectado queda
pendiente de revalidación; evidencia anterior es histórica, no prueba del criterio
nuevo. No borrar resultados previos ni desmarcar todo: no desmarcar tareas ajenas.
Un artefacto existente requiere comprobar comportamiento, no solo su presencia.

Spec cerrada: proponer revisión explícita o spec vinculada según alcance. Conservar
historia del cierre, acuerdo y evidencia anteriores. Registrar revisión pendiente
sin sobrescribir silenciosamente el cierre. Si se elige spec vinculada, señalar qué
requisito vigente sustituirá y cuándo se aprueba; un enlace no lo invalida solo.

Distinguir vigente/sustituido/histórico por evidencia y decisiones, no edad: un
requisito no caduca por antigüedad. Estado, modo o autoridad ambiguos se aclaran;
no migrar legacy ni inferir aprobación por archivos. Mantener integración transversal.

## Impacto y continuidad

Si código y spec difieren, determinar bugfix, documentación desfasada o cambio
funcional. Preguntar solo si la petición/evidencia no resuelven qué corregir; no
calificar un bug como feature ni actualizar requisitos para ocultar un defecto.

Evaluar cambios pequeños relacionados por su impacto conjunto; no sumar notas
matemáticamente ni dividir garantías para forzar direct. Calificar trabajo pendiente
e impacto relevante, no automáticamente toda la feature histórica o el proyecto.

Elección de modo/ejecutor aplica al alcance aceptado. Ante cambio material,
reevaluar compatibilidad y autorización; no repetir elecciones por retoques sin
impacto. Respetar routing manual, límites especialistas y gates pendientes.

## Contexto proporcional

Cargar esta referencia bajo demanda solo ante relación o ambigüedad relevante;
sin relación, evitarla. Leer cabecera/requisitos primero; diseño, tareas y pruebas
solo según impacto. Reutilizar contexto conocido mientras fuentes y alcance sigan
iguales; revalidar si cambian o no puede comprobarse vigencia. Sin índice ni caché
persistente nuevos, sin bootstrap/sync automático ni preguntas repetidas.

Mantener presupuestos del agente/skill/plantillas; medir la referencia separadamente.
Reportar palabras/caracteres de instrucciones fijas, no tokens reales ni ahorro
porcentual no observado. Contenido de proyecto, número de candidatas y costo de
búsqueda/lecturas dependen del caso y requieren observación runtime. Sin cargar
plantillas o rúbrica si la operación no las necesita.

## Casos de continuidad

Ejemplos normativos ilustrativos; no son resultados runtime ni decisiones simuladas.

| Caso | Resultado esperado |
|---|---|
| nota-2-enmienda | Conservar modo existente y revisar requisito/gates afectados; no forzar direct. |
| gate-3-pendiente | Continuar tarea en spec; no implementar sin aprobación requerida. |
| conserva-requisito | Direct evaluable si trivial y sin evasión de tarea/gate; vínculo y evidencia breve. |
| cerrada | Proponer revisión/spec vinculada conservando historia y cierre previo. |
| evidencia-obsoleta | Registrar revalidación pendiente; anterior permanece histórica. |
| código-spec | Aclarar autoridad si no es evidente antes de corregir código o acuerdo. |
| varias-candidatas | Preguntar si no se distingue la spec/autoridad aplicable. |
| cambios-relacionados | Evaluar conjunto y dependencias sin sumar notas. |
