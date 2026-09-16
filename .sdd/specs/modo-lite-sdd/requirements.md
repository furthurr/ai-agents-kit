# Requisitos — Modo lite de SDD

Modo SDD: `standard` (esta spec modifica el contrato SDD)

## Resumen

Incorporar `lite` como cuarta profundidad SDD para cambios acotados que necesitan
más trazabilidad que `direct`, pero no justifican el flujo completo de `standard`.
Quick Plan será una característica obligatoria y exclusiva de `lite`; no podrá
combinarse con `direct`, `standard` ni `deep`.

## Historia 1: Profundidades separadas y proporcionales

Como usuario del agente SDD, quiero que la profundidad se seleccione de forma
proporcional para evitar tanto documentación innecesaria como análisis insuficiente.

### Criterios (EARS)

- REQ-001: EL SISTEMA DEBERÁ reconocer exactamente cuatro profundidades SDD:
  `direct`, `lite`, `standard` y `deep`.
- REQ-002: EL SISTEMA DEBERÁ mantener separados el tipo de trabajo, la profundidad
  SDD, la intención de planificar o implementar y la estrategia de pruebas.
- REQ-003: CUANDO una solicitud cumpla todos los límites actuales de `direct`, EL
  SISTEMA DEBERÁ seleccionar `direct` sin crear una spec innecesaria.
- REQ-004: CUANDO una solicitud no sea `direct` y cumpla todos los criterios de
  elegibilidad de `lite`, EL SISTEMA DEBERÁ seleccionar `lite` automáticamente.
- REQ-005: SI la elegibilidad de `lite` no puede demostrarse, ENTONCES EL SISTEMA
  DEBERÁ seleccionar `standard` como fallback seguro.
- REQ-006: CUANDO el usuario solicite explícitamente `standard` o `deep`, EL SISTEMA
  NO DEBERÁ rebajar automáticamente la profundidad.
- REQ-007: EL SISTEMA NO DEBERÁ activar `deep` sin una petición explícita del
  usuario, aunque podrá recomendarlo.

## Historia 2: Quick Plan exclusivo de lite

Como usuario, quiero que Quick Plan exista únicamente en `lite` para que los modos
de mayor riesgo conserven sus aprobaciones de fase.

### Criterios (EARS)

- REQ-008: EL SISTEMA DEBERÁ tratar Quick Plan como el flujo de planificación
  obligatorio y exclusivo de `lite`, no como una profundidad ni como una variante
  transversal de SDD.
- REQ-009: CUANDO EL SISTEMA seleccione `lite`, EL SISTEMA DEBERÁ activar Quick Plan
  automáticamente.
- REQ-010: CUANDO el usuario solicite Quick Plan, EL SISTEMA DEBERÁ evaluar la
  solicitud exclusivamente contra los criterios de `lite`.
- REQ-011: SI el usuario combina Quick Plan con `direct`, `standard` o `deep`,
  ENTONCES EL SISTEMA DEBERÁ rechazar la combinación y explicar que Quick Plan solo
  está disponible en `lite`.
- REQ-012: SI una solicitud explícita de Quick Plan no es apta para `lite`, ENTONCES
  EL SISTEMA DEBERÁ proponer `standard` y esperar confirmación; no deberá convertir
  el flujo silenciosamente.
- REQ-013: EL SISTEMA DEBERÁ conservar en `standard` y `deep` los Gates 1–4, sin
  permitir que Quick Plan los omita.
- REQ-014: EL SISTEMA NO DEBERÁ generar Quick Plan en `direct`, porque ese modo no
  produce una planificación SDD.

## Historia 3: Selección conservadora de lite

Como mantenedor, quiero criterios verificables de entrada y exclusión para que
`lite` no reduzca controles en cambios riesgosos o ambiguos.

### Criterios (EARS)

- REQ-015: EL SISTEMA DEBERÁ seleccionar `lite` solo cuando el resultado esperado
  esté claro, no queden decisiones funcionales relevantes abiertas, el alcance sea
  acotado y se reutilicen patrones existentes.
- REQ-016: EL SISTEMA DEBERÁ exigir para `lite` una estrategia viable de prueba o
  verificación y un cambio reversible sin migraciones complejas.
- REQ-017: SI la solicitud afecta un contrato público, una API, una migración de
  datos, una decisión arquitectónica, un subsistema nuevo o una integración externa
  significativa, ENTONCES EL SISTEMA DEBERÁ usar `standard`.
- REQ-018: SI la solicitud requiere coordinación relevante entre capas o módulos,
  o presenta riesgo de seguridad, privacidad, concurrencia, integridad crítica o
  compliance, ENTONCES EL SISTEMA DEBERÁ usar `standard`.
- REQ-019: SI existen reglas funcionales ambiguas, un refactor legado riesgoso o no
  hay una verificación viable, ENTONCES EL SISTEMA DEBERÁ usar `standard`.
- REQ-020: SI el bugfix es trivial y cumple los límites de `direct`, ENTONCES EL
  SISTEMA PODRÁ usar `direct`; en cualquier otro bugfix EL SISTEMA DEBERÁ usar
  `standard`.
- REQ-021: SI el usuario solicita explícitamente `direct` o `lite` pero la tarea no
  cumple sus límites, ENTONCES EL SISTEMA DEBERÁ rechazar esa profundidad y explicar
  la ruta segura propuesta.

## Historia 4: Planificación e implementación lite

Como usuario, quiero que `lite` respete si pedí solo un plan o también la
implementación, sin añadir los gates completos de `standard`.

### Criterios (EARS)

- REQ-022: CUANDO `lite` sea confirmado en el Gate 0, EL SISTEMA DEBERÁ generar
  `requirements.md`, `design.md` y `tasks.md` en una pasada, sin Gates 1–3.
- REQ-023: CUANDO el usuario solicite únicamente Quick Plan o planificación, EL
  SISTEMA DEBERÁ detenerse después de `tasks.md` y no implementar código.
- REQ-024: CUANDO la solicitud original incluya implementación, EL SISTEMA DEBERÁ
  implementar después del Quick Plan sin añadir Gates 1–3.
- REQ-025: EL SISTEMA DEBERÁ identificar de forma durable una spec `lite` mediante
  un marcador explícito `Modo SDD: lite`.
- REQ-026: CUANDO `lite` termine solo en planificación, EL SISTEMA NO DEBERÁ crear
  evidencia de implementación ni presentar tareas como completadas.
- REQ-027: CUANDO `lite` implemente cambios, EL SISTEMA DEBERÁ crear un
  `verification.md` compacto con evidencia real y cerrar sin Gate 4.
- REQ-028: EL SISTEMA DEBERÁ mantener en `tasks.md` la planificación, los estados y
  la trazabilidad, y en `verification.md` la evidencia principal de cierre.

## Historia 5: Gates y reclasificación visibles

Como usuario, quiero conocer el modo seleccionado y aprobar cualquier aumento de
control para que la automatización no cambie silenciosamente el flujo.

### Criterios (EARS)

- REQ-029: CUANDO EL SISTEMA seleccione `lite`, EL SISTEMA DEBERÁ mostrar en el
  Gate 0 el modo, los motivos verificables y que Quick Plan omite Gates 1–3 y Gate 4.
- REQ-030: EL SISTEMA DEBERÁ conservar el Gate 0 bloqueante para `lite`, separado
  conceptualmente de los gates de fase omitidos.
- REQ-031: SI durante `lite` aparece un factor de exclusión, ENTONCES EL SISTEMA
  DEBERÁ detenerse en un punto seguro, conservar honestamente el estado pendiente y
  proponer la reclasificación a `standard`.
- REQ-032: CUANDO una reclasificación cambie la política de gates, EL SISTEMA DEBERÁ
  solicitar confirmación aunque el nivel de modelo recomendado no cambie.
- REQ-033: SI la reclasificación también cambia el nivel de modelo, ENTONCES EL
  SISTEMA DEBERÁ combinar la confirmación de flujo con el nuevo Gate 0.
- REQ-034: EL SISTEMA NO DEBERÁ repetir el Gate 0 dentro de `lite` mientras no cambien
  el alcance, el riesgo ni el nivel global.

## Historia 6: Testing y evidencia proporcionales

Como mantenedor, quiero que `lite` reduzca ceremonia documental sin reducir la
honestidad de las pruebas ni la trazabilidad.

### Criterios (EARS)

- REQ-035: EL SISTEMA DEBERÁ mantener la estrategia de pruebas independiente de la
  profundidad SDD e incluir `lite` en ese contrato.
- REQ-036: CUANDO `lite` añada o modifique comportamiento observable, EL SISTEMA
  DEBERÁ aplicar TDD focalizado salvo una excepción explícita y verificable.
- REQ-037: CUANDO no cambie comportamiento observable, EL SISTEMA PODRÁ omitir un
  test nuevo si registra el check existente o una razón concreta.
- REQ-038: SI no se observó un RED que fallara por la razón esperada, ENTONCES EL
  SISTEMA NO DEBERÁ presentar la evidencia como TDD.
- REQ-039: CUANDO exista implementación `lite`, `verification.md` DEBERÁ registrar
  estrategia, RED o baseline, GREEN, suite final, excepciones y una matriz compacta
  de requisito, tarea, test o check, evidencia y estado.
- REQ-040: EL SISTEMA NO DEBERÁ inventar requisitos no funcionales, evidencia,
  resultados de comandos ni cumplimiento para completar el cierre `lite`.

## Historia 7: Compatibilidad y propagación multiplataforma

Como mantenedor del kit, quiero que el nuevo contrato sea coherente y compatible en
todas las plataformas soportadas.

### Criterios (EARS)

- REQ-041: EL SISTEMA DEBERÁ conservar sin cambios conductuales el flujo interno de
  `standard`, incluido Requirements, Design, Tasks, Implementación, Verification y
  sus Gates 1–4.
- REQ-042: EL SISTEMA DEBERÁ conservar los límites actuales de `direct` y el carácter
  explícito de `deep`.
- REQ-043: CUANDO se rendericen los artefactos, EL SISTEMA DEBERÁ propagar el mismo
  contrato de `lite` y Quick Plan a Copilot, OpenCode, Kiro y Claude.
- REQ-044: EL SISTEMA DEBERÁ actualizar pruebas contractuales y documentación de
  usuario para reflejar la exclusividad de Quick Plan y las reglas de selección.
- REQ-045: EL SISTEMA NO DEBERÁ modificar manualmente los artefactos bajo
  `generated/`; deberán producirse desde fuentes canónicas y adaptadores.
- REQ-046: EL SISTEMA DEBERÁ mantener utilizables las specs y Quick Plans existentes
  sin exigir una migración automática.
- REQ-047: SI una spec legacy de tres archivos no declara el modo y su estado resulta
  ambiguo, ENTONCES EL SISTEMA DEBERÁ pedir aclaración antes de reanudarla.

## Casos límite

- El usuario solicita `standard con Quick Plan` o `deep con Quick Plan`.
- El usuario solicita Quick Plan para una migración, API pública o cambio de auth.
- Una tarea parece `lite` en el preflight, pero el código revela un cruce de capas.
- El modo cambia de `lite` a `standard` y ambos recomiendan modelo `MEDIO`.
- El usuario pide solo Quick Plan y después, en otro turno, solicita implementar.
- Existe una spec antigua con requirements, design y tasks, pero sin marcador de modo.
- Un test nuevo pasa antes de escribir producción y no constituye un RED válido.
- No existe un harness de pruebas viable para un cambio de comportamiento.
- El nombre `lite` coincide con modos de otros agentes; la salida debe identificarlo
  como `Modo SDD: lite`.

## Supuestos

- Quick Plan deja de ser una variante transversal y pasa a formar parte exclusiva
  del contrato de `lite`.
- El Gate 0 confirmado autoriza el flujo `lite` mostrado; no se añade un gate de
  implementación si la petición original ya incluía implementar.
- La verificación compacta de `lite` es un cierre durable, pero no constituye la
  Fase 4 completa ni añade Gate 4.
- Los cambios a esta propia capacidad se implementarán mediante esta spec
  `standard`, no mediante el nuevo modo todavía inexistente.
