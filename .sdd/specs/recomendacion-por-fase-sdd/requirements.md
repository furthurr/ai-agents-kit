# Requisitos — Recomendación de modelo por próxima fase

Modo SDD: standard
Fase: Requirements
Estado: aprobada
Gate 1: aprobado

## Resumen

Modificar el Gate 0 y la interacción de SDD para que no muestre al inicio un
modelo global junto con recomendaciones para todas las fases pendientes. En su
lugar, el sistema deberá recomendar únicamente el nivel genérico (`BAJO`, `MEDIO`
o `ALTO`) de la próxima fase. En los límites entre fases, el resumen de la fase
completada, su gate de aprobación y la recomendación de la fase siguiente deberán
aparecer en el mismo mensaje.

La aprobación de la fase anterior y la confirmación del nivel de la siguiente
fase serán necesarias antes de iniciar dicha fase. Esta recomendación de capacidad
no sustituye ni crea gates SDD adicionales.

## Historia 1: Recomendación inicial acotada

Como usuario del agente SDD, quiero conocer la capacidad recomendada para el
proceso que va a comenzar sin recibir un perfil de todo el flujo futuro.

### Criterios (EARS)

- REQ-001: CUANDO una solicitud SDD vaya a iniciar un proceso, EL SISTEMA DEBERÁ
  identificar la próxima fase u operación ejecutable.
- REQ-002: CUANDO se muestre el preflight inicial, EL SISTEMA DEBERÁ recomendar
  únicamente el nivel genérico aplicable a la próxima fase u operación.
- REQ-003: EL SISTEMA NO DEBERÁ mostrar en el preflight inicial una lista de
  recomendaciones para todas las fases pendientes.
- REQ-004: EL SISTEMA DEBERÁ mostrar el tipo de trabajo, el modo SDD, el alcance,
  la complejidad, la próxima fase, el nivel recomendado y los motivos verificables.
- REQ-005: EL SISTEMA NO DEBERÁ mencionar nombres de modelos, proveedores ni
  afirmar conocer el modelo activo del host.
- REQ-006: CUANDO no exista una spec previa, EL SISTEMA DEBERÁ considerar
  Requirements como la próxima fase de `standard` o `deep`.
- REQ-007: CUANDO exista una spec aprobada con fases pendientes, EL SISTEMA DEBERÁ
  considerar como próxima fase la primera fase pendiente real.

## Historia 2: Recomendación en transición de fases

Como usuario, quiero recibir la recomendación de la siguiente fase junto con el
resumen y la aprobación de la fase actual para poder decidir antes de continuar.

### Criterios (EARS)

- REQ-008: CUANDO finalice una fase con un gate de aprobación pendiente, EL SISTEMA
  DEBERÁ presentar primero un resumen verificable de esa fase.
- REQ-009: CUANDO exista una fase siguiente, EL SISTEMA DEBERÁ mostrar en el mismo
  mensaje el gate de la fase actual y la recomendación de nivel para la siguiente.
- REQ-010: EL SISTEMA DEBERÁ indicar que la recomendación de la fase siguiente
  queda condicionada a la aprobación de la fase actual.
- REQ-011: CUANDO el usuario apruebe la fase actual y confirme el nivel recomendado
  o el nivel actual, EL SISTEMA DEBERÁ iniciar la fase siguiente.
- REQ-012: SI el usuario aprueba la fase actual pero no deja claro el nivel que
  usará en la siguiente, ENTONCES EL SISTEMA DEBERÁ pedir esa confirmación antes de
  iniciar la siguiente fase.
- REQ-013: SI el usuario rechaza o solicita iterar la fase actual, ENTONCES EL
  SISTEMA NO DEBERÁ iniciar la fase siguiente ni aplicar su recomendación pendiente.
- REQ-014: SI no existe una fase siguiente porque la verificación terminó, ENTONCES
  EL SISTEMA DEBERÁ mostrar únicamente el gate de cierre aplicable, sin nueva
  recomendación de modelo.

## Historia 3: Separación entre fases y gates

Como mantenedor, quiero que la recomendación de modelo se refiera a procesos y no
a gates para no multiplicar artificialmente el flujo SDD.

### Criterios (EARS)

- REQ-015: EL SISTEMA DEBERÁ conservar los Gates 1–4 de `standard` y `deep` sin
  cambiar su propósito ni crear gates adicionales.
- REQ-016: EL SISTEMA DEBERÁ nombrar la salida como recomendación para la próxima
  fase o proceso, no como recomendación para un gate.
- REQ-017: EL SISTEMA DEBERÁ mantener una sola recomendación visible por cada fase
  que vaya a iniciar.
- REQ-018: EL SISTEMA NO DEBERÁ repetir la misma recomendación dentro de una fase
  mientras no cambien el alcance, el riesgo ni el nivel requerido.
- REQ-019: EL SISTEMA DEBERÁ permitir que una respuesta confirme simultáneamente la
  aprobación de la fase actual y el nivel de la fase siguiente.
- REQ-020: EL SISTEMA DEBERÁ aceptar como confirmación del nivel una selección
  explícita del nivel recomendado o la decisión de continuar con el nivel actual.

## Historia 4: Modos proporcionalmente compatibles

Como usuario, quiero que la recomendación por fase respete la diferencia entre los
modos SDD y no elimine las garantías de `lite`, `standard` o `deep`.

### Criterios (EARS)

- REQ-021: CUANDO el modo sea `direct`, EL SISTEMA DEBERÁ conservar un aviso breve
  no bloqueante y no deberá crear un preflight por fases.
- REQ-022: CUANDO el modo sea `lite`, EL SISTEMA DEBERÁ recomendar el nivel solo
  para la operación Quick Plan, sin recomendar por separado sus pasos internos.
- REQ-023: CUANDO el modo sea `standard` o `deep`, EL SISTEMA DEBERÁ recomendar el
  nivel de Requirements, Design, Tasks, Implementación y Verification únicamente al
  iniciar cada una.
- REQ-024: EL SISTEMA DEBERÁ conservar Quick Plan como capacidad exclusiva de
  `lite`; este cambio no deberá habilitarlo en `standard` ni `deep`.
- REQ-025: CUANDO una tarea cambie de `lite` a `standard`, EL SISTEMA DEBERÁ mostrar
  la nueva próxima fase, su recomendación y solicitar confirmación del cambio de
  flujo aunque el nivel genérico coincida.
- REQ-026: EL SISTEMA DEBERÁ conservar la distinción entre estrategia de testing y
  profundidad SDD.

## Historia 5: Recalculo y cambios de alcance

Como usuario, quiero que la recomendación se actualice si cambia el riesgo o el
alcance antes de iniciar la próxima fase.

### Criterios (EARS)

- REQ-027: SI cambia el alcance o el riesgo antes de iniciar la próxima fase,
  ENTONCES EL SISTEMA DEBERÁ recalcular la recomendación de esa fase.
- REQ-028: SI el cambio de alcance obliga a otro modo SDD, ENTONCES EL SISTEMA DEBERÁ
  detenerse y solicitar confirmación de la reclasificación.
- REQ-029: SI cambia únicamente el nivel recomendado pero no el modo ni la política
  de gates, ENTONCES EL SISTEMA DEBERÁ mostrar el nuevo nivel antes de iniciar la
  fase y esperar la decisión del usuario.
- REQ-030: EL SISTEMA NO DEBERÁ iniciar una fase con una recomendación antigua
  cuando el preflight revele un cambio relevante de riesgo.
- REQ-031: CUANDO el usuario pida cambiar manualmente de nivel, EL SISTEMA DEBERÁ
  conservar la recomendación como referencia y no cambiar el modelo del host.

## Historia 6: Reanudación y compatibilidad documental

Como mantenedor, quiero que las specs nuevas y existentes puedan reanudarse sin
perder qué fase está pendiente ni confundir una recomendación con un gate.

### Criterios (EARS)

- REQ-032: EL SISTEMA DEBERÁ determinar la próxima fase a partir del estado de la
  spec y no a partir de una lista estática de recomendaciones iniciales.
- REQ-033: EL SISTEMA DEBERÁ conservar las specs cerradas existentes sin reescribir
  su evidencia histórica.
- REQ-034: SI una spec no tiene estado suficiente para determinar la próxima fase,
  ENTONCES EL SISTEMA DEBERÁ pedir aclaración antes de recomendar un nivel.
- REQ-035: EL SISTEMA DEBERÁ mantener la compatibilidad de rutas planas y agrupadas
  de `.sdd/specs/`.

## Historia 7: Documentación, pruebas y propagación

Como mantenedor del kit, quiero que el contrato de recomendación sea coherente,
testeable y portable a todas las plataformas.

### Criterios (EARS)

- REQ-036: EL SISTEMA DEBERÁ actualizar la skill y el agente canónicos para
  describir el preflight inicial y los preflights de fase.
- REQ-037: EL SISTEMA DEBERÁ actualizar el contrato de selección de modelo para
  eliminar el perfil global visible y definir la salida de próxima fase.
- REQ-038: EL SISTEMA DEBERÁ actualizar la documentación y el smoke test con la
  secuencia resumen → aprobación → recomendación de próxima fase.
- REQ-039: EL SISTEMA DEBERÁ comprobar mediante tests contractuales que no se
  recomiendan modelos para gates ni se muestran todas las fases al inicio.
- REQ-040: CUANDO se rendericen los artefactos, EL SISTEMA DEBERÁ propagar el mismo
  contrato a Copilot, OpenCode, Kiro y Claude.
- REQ-041: EL SISTEMA DEBERÁ mantener la recomendación agnóstica de modelos,
  proveedores y plataforma.

## Casos límite

- Solicitud nueva de feature `standard` sin spec previa.
- Continuación con Requirements aprobados y Design pendiente.
- Usuario aprueba una fase con una respuesta ambigua como `adelante`.
- Usuario aprueba una fase pero solicita mantener el nivel actual.
- Usuario aprueba una fase y selecciona el nivel recomendado para la siguiente.
- Usuario itera la fase actual después de ver la recomendación siguiente.
- Verification termina y solo queda Gate 4.
- `lite` con Quick Plan y sin fases internas expuestas.
- Reclasificación `lite → standard` con el mismo nivel genérico.
- Cambio de `MEDIO` a `ALTO` antes de Design.
- Spec legacy sin estado de fase suficiente.
- Modo Quick Plan combinado con `standard` o `deep`.

## Supuestos

- El nivel recomendado seguirá siendo genérico: `BAJO`, `MEDIO` o `ALTO`.
- El agente nunca seleccionará ni cambiará el modelo del host.
- Una recomendación de fase no constituye un gate SDD adicional.
- La aprobación y la confirmación del nivel siguiente pueden resolverse en una
  sola respuesta del usuario.
- `lite` mantendrá un único preflight para Quick Plan y no expondrá sus pasos
  internos como fases independientes.
- La modificación de este contrato se implementará mediante `standard`, no mediante
  `lite` ni Quick Plan.
