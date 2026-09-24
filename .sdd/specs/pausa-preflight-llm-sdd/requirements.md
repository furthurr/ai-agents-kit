# Requisitos — Pausa tras recomendaciones de modelo en los agentes del kit

Modo SDD: standard
Fase: Requirements
Estado: aprobada (ampliación multiagente)
Gate 1: aprobado (usuario: «continua»)

## Objetivo

Dar al usuario una oportunidad real de cambiar manualmente el modelo tras el
preflight y antes de ejecutar el proceso recomendado. La pausa no confirma qué
modelo se usa ni sustituye los gates de aprobación de las fases SDD.

## Historia 1: Pausa inicial

Como usuario, quiero recibir la recomendación antes de que empiece el trabajo
para poder cambiar manualmente de modelo si lo deseo.

- REQ-001: CUANDO se muestre el preflight inicial de una operación SDD no trivial,
  EL SISTEMA DEBERÁ terminar el turno antes de iniciar la operación recomendada.
- REQ-002: EL SISTEMA DEBERÁ indicar que el usuario puede cambiar manualmente de
  modelo o continuar con el actual, sin afirmar conocer cuál está activo.
- REQ-003: CUANDO el usuario indique que desea continuar tras la pausa inicial,
  EL SISTEMA DEBERÁ iniciar la operación pendiente sin exigir que declare qué
  modelo ha seleccionado.
- REQ-004: EL SISTEMA NO DEBERÁ seleccionar ni cambiar el modelo del host.

## Historia 2: Transiciones y gates

Como usuario, quiero que el aviso de la próxima fase llegue antes de iniciarla,
sin tener que aprobar un gate adicional de modelo.

- REQ-005: CUANDO una fase `standard` o `deep` concluya con un gate pendiente,
  EL SISTEMA DEBERÁ mostrar juntos el resumen verificable, el gate actual y la
  recomendación para la próxima fase, y detenerse hasta la aprobación del gate.
- REQ-006: CUANDO el usuario apruebe el gate de la fase actual, EL SISTEMA DEBERÁ
  iniciar la próxima fase sin pedir confirmación sobre el modelo elegido.
- REQ-007: CUANDO termine Implementación y corresponda Verification sin gate
  intermedio, EL SISTEMA DEBERÁ presentar la recomendación y terminar el turno
  antes de iniciar Verification.
- REQ-008: CUANDO el usuario reanude tras la pausa previa a Verification, EL
  SISTEMA DEBERÁ iniciar Verification sin pedir confirmación del nivel de LLM.
- REQ-009: SI el usuario solicita cambios en la fase actual, ENTONCES EL SISTEMA
  NO DEBERÁ iniciar la fase siguiente y DEBERÁ descartar su recomendación pendiente.

## Historia 3: Compatibilidad y validación

Como mantenedor, quiero que el contrato sea coherente en los artefactos canónicos
y en las plataformas generadas.

- REQ-010: CUANDO el modo sea `lite`, EL SISTEMA DEBERÁ pausar tras el único
  preflight de Quick Plan, antes de generarlo, sin introducir Gates 1–4.
- REQ-011: CUANDO el modo sea `direct`, EL SISTEMA DEBERÁ conservar su aviso breve
  y no bloqueante.
- REQ-012: EL SISTEMA DEBERÁ conservar la recomendación por próxima fase, sin
  mostrar un perfil global ni crear gates adicionales de modelo.
- REQ-013: EL SISTEMA DEBERÁ verificar mediante pruebas contractuales la pausa
  inicial, la reanudación sin confirmar modelo, la transición por gates y la pausa
  anterior a Verification en los artefactos canónicos y generados.

## Historia 4: Coherencia de los otros agentes

Como usuario del kit, quiero una oportunidad real de cambiar manualmente el
modelo en todos los agentes que recomienden un nivel antes de trabajar, sin
eliminar sus confirmaciones o garantías existentes.

- REQ-014: CUANDO Architecture, Code Quality, Data & API, Security o UI Design
  recomienden un nivel inicial, incluso para una consulta o tarea puntual, EL
  SISTEMA DEBERÁ terminar el turno antes de inspeccionar, escribir o ejecutar la
  operación y permitir reanudar con «continúa» sin declarar el modelo elegido.
- REQ-015: CUANDO el proceso sea pesado en esos cinco especialistas, EL SISTEMA
  DEBERÁ conservar el hard stop previo a herramientas, incluida la carga de la
  skill, sin añadir un segundo aviso tras reanudar para el mismo alcance.
- REQ-016: CUANDO Documentation Orchestrator o Project Navigator muestren su aviso
  previo a una operación, EL SISTEMA DEBERÁ conservar su pausa existente y
  permitir reanudar sin confirmar qué modelo se eligió, sin omitir sus otros gates.
- REQ-017: CUANDO un orquestador haya mostrado y pausado la recomendación para el
  mismo alcance y el usuario reanude, EL SISTEMA DEBERÁ evitar que el agente
  especialista repita la pausa por el mismo aviso; deberá conservar los gates de
  alcance, escritura o remediación que correspondan.
- REQ-018: EL SISTEMA DEBERÁ mantener los avisos finales que ya recomiendan un
  cambio manual de modelo sin convertirlos en pausas previas a una tarea inexistente.
- REQ-019: EL SISTEMA DEBERÁ conservar las reglas de seguridad, evidencias y
  confirmación de cada agente con independencia de esta pausa de modelo.
- REQ-020: EL SISTEMA DEBERÁ comprobar el contrato de pausa y reanudación de los
  agentes aplicables en sus fuentes canónicas y artefactos generados para Copilot,
  OpenCode, Kiro y Claude.

## Supuestos y casos límite

- La pausa se realiza terminando el turno: el usuario puede cambiar el modelo
  fuera del agente y responder simplemente «continúa».
- La aprobación del gate de una fase sirve también como oportunidad para cambiar
  modelo antes de la siguiente; no se añade una segunda pausa tras aprobarla.
- Si el usuario continúa sin cambiar el modelo, el flujo sigue igualmente.
- El Gate 4 de cierre no necesita una recomendación para una fase inexistente.
- Git Release Manager no tiene un preflight de recomendación de nivel propio:
  conserva sus confirmaciones de Git/release sin agregar un aviso ficticio.
- Los cinco especialistas hoy pausaban solo los procesos pesados: este cambio
  amplía la pausa también a los avisos de tareas puntuales.
- Documentation Orchestrator y Project Navigator ya pausaban antes de procesos
  sujetos a recomendación: se verifica su coherencia y se ajusta solo si hace falta.
- Se conserva la spec histórica `recomendacion-por-fase-sdd` como evidencia de la
  decisión anterior; esta spec propone modificar su comportamiento vigente.
