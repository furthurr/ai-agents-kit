# Recomendación de agente por dominio

Política de `@sdd` para recomendar un ejecutor, no un clasificador runtime ni un
contrato de delegación. Primera versión: solo `ui-design` y `data-api`.
`@` es notación del kit: no es un comando universal ni acredita instalación.

## Candidatos y límites

La lista cerrada de candidatos v1 es `ui-design` y `data-api`; no enumeres ni
recomiendes otros agentes al aclarar, ni presentes sus dominios como alternativas
de routing. Si surge un dominio distinto, mixto o fuera de catálogo, mantén SDD y
explica solo que queda fuera de los dos candidatos de esta versión.

- `ui-design`: apariencia, componentes, tokens, temas, accesibilidad visual y UX.
  Excluye lógica de negocio, APIs, persistencia, seguridad y releases.
- `data-api`: APIs, persistencia, modelos, serialización, contratos e integraciones.
  Excluye UI, negocio ajeno a datos, seguridad transversal y Git/releases.
- Comprueba los IDs en el catálogo y el alcance en las definiciones disponibles.
  Candidato ausente o no verificable: mantener SDD, explicar la limitación y no
  inventar disponibilidad en el host. No recomendar otros agentes mediante esta
  política ni extender los límites de los especialistas.

## Precedencias

Seleccionar el agente `sdd` no equivale a rechazar una recomendación de especialista.
Solo una preferencia explícita de ejecutor para ese alcance (por ejemplo «hazlo
aquí en SDD») evita esa elección; no infieras tal preferencia del agente activo.

1. Respeta la elección explícita del usuario de agente o continuidad con SDD.
   Ante conflicto con límites, explica y pide aclarar cómo continuar antes de actuar.
2. Evalúa responsabilidades, alcance, ambigüedad y riesgo desde la solicitud y
   contexto mínimo verificable; no clasifiques por palabras clave aisladas.
3. Si falta alcance, pregunta lo esencial o mantén planificación SDD; no edites
   un alcance ambiguo. Si el alcance es mixto, ningún especialista ejecuta el total.
4. Conserva planificación SDD si hay requisitos ambiguos, múltiples pantallas o
   flujos, nuevos estados/comportamientos, decisiones reutilizables o cruce de dominios.
5. Para datos, conserva planificación SDD si faltan requisitos/diseño o se afectan
   contratos, esquemas, migraciones, compatibilidad, varias fuentes, módulos o capas.
6. Cuando el alcance ejecutable esté claro, autorizado y íntegramente dentro de un
   especialista, recomienda ese agente. Después de planificación aprobada puede
   evaluarse una tarea acotada existente, conservando su vínculo a la spec; no
   inventes tareas para justificar una recomendación.

## Decisión manual

Presenta actividad, ID recomendado, motivo verificable y límites. Pregunta:
«¿Quieres seleccionar manualmente este agente o continuar con SDD?».
Indica el gate pendiente si lo hay. Espera la elección de ejecutor antes de ejecutar
la actividad candidata; una preferencia ya explícita compatible no exige otra pregunta.
No uses herramientas de escritura ni comandos que modifiquen archivos mientras falte
esa elección esencial. La carga de la skill y la evaluación de la política deben
preceder al primer intento de edición, no solo a una edición exitosa.

Esta recomendación no cambia el agente activo, no invoca subagentes y no delega
ejecución automáticamente. El usuario selecciona el agente en la interfaz del host.

- Si el usuario continúa con SDD, sigue solo el trabajo autorizado y no repetir la
  misma recomendación sin cambio de alcance, riesgo o decisión. Usa el historial de
  sesión, sin persistencia nueva; no asumas una elección si falta ese contexto.
- Si elige al especialista, prepara el contexto siguiente y deja de ejecutar esa
  actividad en SDD. No afirmes que la interfaz haya cambiado de agente.
- Si la respuesta no permite distinguir ejecutor, aclara esa elección.

## Contexto para selección manual

Entrega un mensaje copiable con este título; no usar `## Handoff` ni activar el
contrato documental de `documentation-orchestrator`.

Si el usuario elige explícitamente al especialista para la actividad actual,
detente en SDD después de preparar el contexto copiable. No continúes la
implementación aquí, aunque la petición original incluyera «implementa» o
«actualiza»: la elección de especialista significa que esa actividad no se ejecuta en SDD.
Solo reanuda si el usuario vuelve a elegir explícitamente continuar la ejecución
en SDD.

- Objetivo, alcance autorizado, límites y exclusiones.
- ID recomendado y motivo de selección.
- Rutas relativas verificadas y contexto mínimo relevante.
- Ruta completa de spec, requisitos y tareas vinculados, si existen.
- Decisiones aprobadas, fase y gate pendiente; no inferir aprobación por archivos.
- Preguntas abiertas y criterios de aceptación/verificación.

No incluir secretos, PII innecesaria ni volcar documentación completa. No inventar
rutas, líneas, requisitos o tareas. El resumen no acredita entrega, ejecución ni
cierre; el receptor comprueba contexto, sus reglas y gates. No requiere un archivo
nuevo ni otorga permisos al agente receptor.

## Integración con SDD

El preflight técnico inicial puede orientar la evaluación; no justifica cargar
contexto pesado antes de resolver decisiones esenciales. Consulta esta referencia cuando haga falta
evaluar un especialista y comprueba contexto mínimo antes de editar o ejecutar la
actividad candidata. Reevaluar solo si cambia el alcance, riesgo o decisión.

La elección no aprueba gates, no cambia permisos y no amplía autorización.
Ejecutor, profundidad SDD y estrategia de pruebas son ejes independientes.
Conserva decisiones y gates pendientes de una spec activa. «Sigue aquí» no aprueba
por sí solo un gate: una respuesta puede elegir ejecutor y aprobar el gate únicamente
si ambas decisiones son explícitas. Mantén SDD para planificación/coordinación si
el alcance no pertenece enteramente a un especialista.

Esta política no crea un gate SDD nuevo: la elección manual se aclara solo cuando
es una decisión esencial pendiente.
