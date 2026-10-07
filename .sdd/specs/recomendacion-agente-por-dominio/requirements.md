# Requisitos — Recomendación de agente por dominio

Modo SDD: standard
Fase: Requirements
Estado: aprobada
Gate 1: aprobado

Aprobación: el usuario respondió «procede» después de la presentación de Gate 1.
Nota de continuidad: tras completar la planificación, el usuario autorizó
implementación mediante «implementa la spec». El alcance funcional aprobado no cambia.

## Resumen

Cuando una solicitud llega a `@sdd`, el sistema deberá evaluar si su alcance
pertenece enteramente a un agente especialista. La primera versión cubrirá
`ui-design` y `data-api`: explicará la recomendación y dejará al usuario decidir
si selecciona manualmente al especialista o continúa en SDD. No cambiará de agente,
invocará subagentes ni delegará implementación automáticamente.

La recomendación de agente es independiente de la profundidad SDD, de los gates y
de la estrategia de pruebas. Si la actividad es ambigua, cruza dominios o necesita
planificación SDD, SDD conserva la planificación; podrá recomendar al especialista
para una tarea acotada cuando corresponda.

## Historia 1: Detección del dominio y límites del especialista

Como usuario de `@sdd`, quiero saber si un especialista existente es el responsable
más adecuado para el alcance solicitado, para evitar que el trabajo se ejecute fuera
de su dominio.

### Criterios (EARS)

- REQ-001: CUANDO `@sdd` reciba una solicitud de trabajo, EL SISTEMA DEBERÁ evaluar
  los dominios, límites de responsabilidad, ambigüedad y riesgos del alcance antes
  de recomendar quién lo ejecuta.
- REQ-002: EL SISTEMA DEBERÁ limitar esta primera versión de la selección de agentes
  a `ui-design` y `data-api`.
- REQ-003: CUANDO la solicitud se limite a apariencia, componentes, tokens, temas,
  accesibilidad visual o UX, sin lógica de negocio, APIs, persistencia, seguridad ni
  releases, EL SISTEMA DEBERÁ considerar `ui-design` como candidato.
- REQ-004: CUANDO la solicitud se limite a APIs, persistencia, modelos, serialización,
  contratos o integraciones, sin UI, negocio ajeno a datos, seguridad transversal ni
  Git/releases, EL SISTEMA DEBERÁ considerar `data-api` como candidato.
- REQ-005: CUANDO el trabajo cruce límites de un especialista o combine dominios,
  EL SISTEMA NO DEBERÁ recomendar que ese especialista ejecute por sí solo toda la
  solicitud.
- REQ-006: CUANDO el dominio o los límites no puedan determinarse con la información
  disponible, EL SISTEMA DEBERÁ pedir la aclaración necesaria o mantener la actividad
  en SDD, sin inferir un agente por palabras clave aisladas.
- REQ-007: EL SISTEMA DEBERÁ recomendar únicamente agentes identificados y con un
  alcance verificable en las definiciones disponibles del kit.

## Historia 2: Mantener SDD cuando se necesita planificación

Como usuario, quiero conservar SDD para definir el trabajo que requiere decisiones
o cruza dominios, aunque después lo implemente un especialista.

### Criterios (EARS)

- REQ-008: CUANDO haya requisitos ambiguos, múltiples pantallas o flujos, estados o
  comportamientos nuevos, decisiones reutilizables o un cruce de dominios, EL SISTEMA
  DEBERÁ conservar SDD para aclarar y planificar el alcance antes de proponer la
  ejecución especializada de una tarea acotada.
- REQ-009: CUANDO falten requisitos o diseño para un cambio de datos/API, o este
  afecte contratos, esquemas, migraciones, compatibilidad, varias fuentes, módulos o
  capas, EL SISTEMA DEBERÁ conservar SDD para planificarlo antes de proponer la
  ejecución especializada de una tarea acotada.
- REQ-010: CUANDO una spec SDD activa incluya trabajo de un especialista, EL SISTEMA
  DEBERÁ relacionar la recomendación con requisitos o tareas existentes y conservar
  las decisiones y gates pendientes de esa spec.
- REQ-011: EL SISTEMA NO DEBERÁ tratar la selección de un especialista como
  aprobación de requisitos, diseño, tareas, cambios de alcance o gates SDD.

## Historia 3: Recomendación y decisión manual

Como usuario, quiero comprender por qué se recomienda un agente y elegir quién
continúa, sin que SDD cambie de agente por su cuenta.

### Criterios (EARS)

- REQ-012: CUANDO un agente especialista sea claramente adecuado para todo el
  alcance ejecutable actual, EL SISTEMA DEBERÁ indicar su identificador, justificar
  la coincidencia con el alcance y resumir los límites relevantes de su
  responsabilidad.
- REQ-013: CUANDO presente una recomendación, EL SISTEMA DEBERÁ ofrecer al usuario
  la elección explícita entre seleccionar manualmente al especialista y continuar
  con SDD.
- REQ-014: EL SISTEMA NO DEBERÁ cambiar el agente activo, invocar subagentes ni
  delegar ejecución automáticamente como resultado de una recomendación.
- REQ-015: CUANDO el usuario elija continuar con SDD, EL SISTEMA DEBERÁ seguir el
  flujo SDD autorizado sin repetir la misma recomendación mientras no cambie el
  alcance, el riesgo o la decisión del usuario.
- REQ-016: CUANDO el usuario elija manualmente al especialista, EL SISTEMA DEBERÁ
  proporcionar un resumen transferible con el objetivo, alcance y límites, contexto
  y decisiones aprobadas relevantes, requisitos o tareas vinculados y preguntas
  pendientes; EL SISTEMA NO DEBERÁ presentarlo como una invocación o handoff
  automático.
- REQ-017: CUANDO el usuario ya haya especificado explícitamente un agente, EL
  SISTEMA DEBERÁ respetar esa selección si el alcance cabe en sus límites; si no
  cabe, EL SISTEMA DEBERÁ explicar el conflicto y pedir cómo continuar.

## Historia 4: Coherencia y portabilidad

Como mantenedor del kit, quiero que la política de recomendación sea comprobable y
coherente en sus agentes y plataformas compatibles.

### Criterios (EARS)

- REQ-018: EL SISTEMA DEBERÁ mantener separadas la recomendación de agente, la
  profundidad SDD, los gates y la estrategia de pruebas.
- REQ-019: EL SISTEMA DEBERÁ aplicar la misma política de límites y selección en las
  definiciones canónicas y los artefactos de agente generados para las plataformas
  compatibles.
- REQ-020: EL SISTEMA DEBERÁ permitir verificar mediante pruebas los casos de
  solicitud solo-UI, solo-datos/API, alcance mixto o ambiguo, selección explícita y
  ausencia de cambio o invocación automática de agente.

## Casos límite

- Cambio visual acotado que no modifica comportamiento ni toca datos.
- Cambio de API o persistencia que no modifica UI ni negocio ajeno a datos.
- Solicitud visual que también requiere una API o lógica de negocio.
- Rediseño ambiguo con varias pantallas, flujos, estados o comportamientos nuevos.
- Cambio de datos/API con contrato, esquema, migración o compatibilidad afectados.
- Usuario que nombra explícitamente un especialista cuyo alcance no cubre toda la solicitud.
- Spec SDD activa con una tarea especializada y un gate pendiente.
- El usuario rechaza la recomendación o elige seguir con SDD.

## Supuestos

- La primera versión cubre solo `ui-design` y `data-api`; ampliar la selección a
  otros especialistas requiere una decisión posterior.
- La selección del especialista la hace el usuario en el host; SDD no asume que el
  host permita llamadas automáticas a subagentes.
- El resumen transferible es contexto textual para selección manual, no el contrato
  formal de handoff del `documentation-orchestrator`.
- Las reglas propias del especialista y los gates SDD aplicables siguen vigentes.
- Esta solicitud es solo de planificación: esta fase define requisitos y no
  implementa cambios en agentes, skills, adaptadores ni artefactos generados.

## Fuera de alcance

- Invocación automática de agentes, ejecución de subagentes o delegación de código.
- Extender la selección inicial a `architecture`, `security`, `code-review` u otros
  especialistas.
- Cambiar el alcance, los gates o las reglas de ejecución de `ui-design` y
  `data-api`.
- Cambiar el contrato de handoff de `documentation-orchestrator`.
