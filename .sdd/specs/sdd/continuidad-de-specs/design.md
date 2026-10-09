# Diseño — Continuidad de specs y contexto selectivo

Modo SDD: standard
Fase: Design
Estado: aprobado
Gate 2: aprobado por el usuario («procede»)

## Contexto y alcance técnico

Extensión del contrato textual SDD, sin clasificador runtime ni índice persistente.
Se reutilizan renderer, pruebas y estructura de specs existentes. La spec anterior
`sdd/alcance-calificacion-y-seleccion` conserva evidencia y Gate 4 pendiente.
Este diseño no aplica anticipadamente la política nueva para omitir sus propios gates.

## Responsabilidades

- `canonical/agents/sdd.md`: recordatorio breve de comprobar relación antes de modo;
  sustituir/compactar texto existente para mantener presupuesto, no sumar un workflow.
- `canonical/skills/sdd-spec/SKILL.md`: entrada de búsqueda localizada y enlace
  condicionado a relación relevante, integrado con alcance y reanudación.
- Nueva `references/spec-continuity.md`: única política detallada de enmiendas,
  estados, evidencia y conflictos; carga solo al encontrar relación o ambigüedad
  relevante. No cargarla en consultas ajenas a una modificación/continuación.
- `references/scope-depth.md`: precedencia de spec afectada sobre recomendación
  numérica y elección previa ligada al alcance; remitir al detalle sin duplicarlo.
- `references/integrity-gate.md`: evidencia vigente vs histórica y revalidación
  proporcional; no tratar [x] histórico como cumplimiento de requisito modificado.
- Plantillas: revisar si pueden representar enmiendas con secciones breves y campos
  existentes. No imponer un nuevo archivo o metadatos de revisión a toda spec.
- `tools/test_sdd_contract.py`: regresiones textuales y presupuestos, sin simular
  autoridad funcional mediante un scorer/clasificador artificial.
- Guía/smoke SDD: ejemplos de continuidad y límites de medición. `generated/` se
  obtiene exclusivamente del renderer para las seis plataformas.

## Detección localizada

1. Usar ruta explícita o spec activa conocida; validar ruta y marcadores existentes.
2. Si no existe, localizar candidatas por módulo/rutas y términos del comportamiento,
   usando herramientas de búsqueda, no leyendo todos los documentos.
3. Leer cabecera y requisitos pertinentes de las candidatas; ampliar según vínculos
   y dependencias relevantes, sin concluir ausencia global por búsqueda limitada.
4. Si persiste conflicto de autoridad o varias candidatas plausibles, preguntar.
5. Si no hay relación relevante, continuar flujo normal sin cargar la política.

No requieren índices nuevos ni Navigator. Si existe contexto auxiliar aplicable,
conservar su preflight y validar decisiones con código/contratos reales. Si no hay
contexto fiable, continuar con fuentes directas e indicar límites pertinentes.

## Decisión de continuidad

| Relación | Tratamiento |
|---|---|
| Sin relación encontrada | Nuevo alcance normal; no afirmar auditoría exhaustiva. |
| Implementa requisito con tareas/gates existentes | Continuar spec y autorización; no sustituir flujo por direct. |
| Ajuste localizado que conserva acuerdos y no evita tarea/gate pendiente | Evaluar direct sin nueva spec; conservar referencia relevante y evidencia proporcional. |
| Cambia requisito vigente | Proponer enmienda; nota baja no cambia modo ni evita gates. |
| Código contradice spec | Identificar bug, cambio funcional o documentación obsoleta; aclarar si autoridad no es evidente. |
| Spec cerrada | Proponer revisión explícita o spec vinculada; conservar cierre y evidencia históricos. |
| Estado/modo/vigencia ambiguos | Aclarar antes de escribir acuerdos o implementar. |

No exigir pregunta si la petición y evidencia ya distinguen inequívocamente bugfix
o cambio funcional. Bugs no reciben nota de feature. Calificar modificaciones de
feature sobre trabajo pendiente e impacto conjunto, no recalificar automáticamente
todo el proyecto ni sumar notas de peticiones pequeñas.

## Enmienda, gates y trazabilidad

Antes de implementación presentar spec/ruta, ID, comportamiento actual/propuesto,
motivo y dependencias afectadas. Mantener ID si sigue siendo el mismo requisito;
añadir ID para comportamiento nuevo y marcar sustitución cuando cambia su identidad.
No borrar acuerdos/evidencia anteriores: conservar delta y vínculo a la revisión.

Para spec activa, preparar cambios como propuesta/en revisión con historia breve;
no presentar la nueva versión como aprobada hasta decisión pertinente.
En standard, Gate 1 cubre requisito modificado; Gate 2/3 se revisan solo si cambia
la decisión de diseño o el plan. Registrar cuáles aprobaciones siguen válidas y por
qué. No reutilizar una aprobación que autoriza comportamiento diferente.
Gate 4 se presenta tras nueva evidencia; aprobación anterior no cierra la revisión.
Lite actualiza Quick Plan afectado con autorización clara, sin inventar Gates 1–4.
Si enmienda vuelve inelegible lite, pedir reclasificación antes de continuar.

Para spec cerrada, el usuario decide revisión o spec vinculada según alcance.
Registrar el cierre anterior como histórico y la nueva revisión como pendiente,
sin borrar la evidencia ni declarar que el nuevo requisito siempre existió.
Si se elige spec vinculada, señalar explícitamente qué acuerdo vigente sustituirá
tras aprobación; un enlace por sí solo no vuelve obsoleto el requisito anterior.
No migrar automáticamente specs legacy ni asumir caducidad por antigüedad.

## Evidencia y tareas

Revisar enlaces requisito → diseño → tarea → test/check → evidencia. Identificar
solo lo afectado y marcar pendiente de revalidación; conservar resultado anterior
como histórico. No desmarcar indiscriminadamente tareas ajenas al cambio.
Un artefacto existente no demuestra criterio nuevo: verificar su comportamiento.
Mantener pruebas de integración de requisitos transversales y gates pendientes.

## Contexto, elecciones y costo

- Reutilizar contexto de sesión si alcance/archivos relevantes siguen iguales;
  si cambiaron o no se puede verificar vigencia, revalidar únicamente lo necesario.
- Selección de modo y ejecutor aplica al alcance aceptado, no a toda la sesión.
  Cambio material obliga a evaluar compatibilidad/autorización; no repetir elección
  por retoques sin impacto. Routing manual y límites especialistas se conservan.
- Mantener límites existentes: agente <1066 palabras/<7580 caracteres; skill
  <2357/<16378; plantillas ≤863/≤5722. Compactar entradas si hace falta.
- Referencia nueva: <1200 palabras/<9000 caracteres; límite separado, sin aumentar
  presupuestos previos. No cargar plantillas/rúbrica si la operación no las requiere.
- Medir cuatro rutas estáticas: cambio aislado, spec conocida, enmienda y candidatas
  múltiples. Separar prompt/referencias de contenido de proyecto variable.
- Reportar palabras/caracteres y documentos necesarios, no tokens exactos ni porcentajes
  de ahorro. Costo de búsqueda/lecturas reales se evalúa en smoke, no en tests textuales.

## Pruebas y errores

TDD focalizado: añadir regresiones de política ausente, observar RED; implementar
instrucciones mínimas, observar GREEN y mantener suites previas. Verificar ejemplos
de requisito modificado con nota 2, continuación con Gate 3 pendiente, cambio que
conserva requisito, spec cerrada, evidencia obsoleta, conflicto código/spec, varias
candidatas, solicitudes pequeñas relacionadas y elección ligada a alcance.
Pruebas negativas del contrato deben detectar eliminación de precedencias o
revalidación, sin convertir checks textuales en supuesta simulación de decisiones LLM.
Ejecutar render, suite SDD, modelo/handoff, validate, enlaces y diff --check;
ampliar checks según diff. No introducir librerías de testing ni PBT ceremonial.

Errores: ruta inválida se rechaza; autoridad ambigua se aclara; contexto ausente se
degrada; evidencia desfasada se registra; requisito sin dependencias verificadas no
se da por terminado. No eliminar cambios ajenos ni instalar globalmente.

## RNF e invariantes

- RNF-1: presupuestos existentes intactos y referencia nueva acotada bajo demanda.
- RNF-2: relación/enmienda no evade modo, autorización ni gates de spec existente.
- RNF-3: resultado histórico no acredita requisito vigente modificado.
- RNF-4: seis distribuciones reproducibles y política idéntica desde canonical.
- RNF-5: alcance aceptado limita elecciones y lecturas se amplían según impacto.

Barra de calidad: política separada de agente y renderer; sin lógica por adaptador,
sin infraestructura/caché ni abstracciones nuevas. DI, UI y almacenamiento de negocio
no aplican a este cambio. Los escenarios runtime se documentan como pendientes si
no se ejecutan, sin usar tests textuales como evidencia de conducta real.
