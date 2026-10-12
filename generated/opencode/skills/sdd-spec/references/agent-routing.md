# Selección explícita de metodología SDD

Esta referencia conserva el contrato de selección del flujo SDD. No es un clasificador
de dominios ni un mecanismo para cambiar de agente.

## Precedencia

1. La metodología se activa únicamente cuando el usuario selecciona el agente `sdd`.
2. Una vez seleccionado, SDD conserva planificación e implementación según la intención
   solicitada, el alcance acordado y los gates reales del modo elegido.
3. El dominio (UI, datos/APIs, negocio o transversal) no deriva automáticamente a
   `developer` ni a otro agente. Las skills `ui-design` y `data-api` pueden cargarse
   bajo demanda como estándares técnicos, sin alterar el ejecutor ni los gates.
4. Developer nunca carga esta metodología. Complejidad o riesgo en Developer usan
   PLAN propio y no crean specs SDD.
5. Si el usuario pide cambiar de agente, respeta la decisión, conserva el estado
   verificable y entrega un resumen portable. No cambies la interfaz, no delegues ni
   uses el contrato `## Handoff` de documentación para transferir código.

## Continuidad y autorización

Una selección de agente no aprueba fases ni amplía permisos. SDD sigue buscando specs
relacionadas, conservando sus gates, decisiones y tareas aprobadas. Un cambio de agente
solicitado por el usuario no declara una tarea implementada ni autoriza al receptor;
el cambio solicitado no transfiere autorización. SDD conserva decisiones y entrega un
resumen portable; el agente elegido verifica el contexto en su host.

La profundidad SDD y testing siguen siendo decisiones independientes. Consulta
`scope-depth.md` y `testing.md` conforme al punto del flujo; esta referencia no crea
gates adicionales ni habilita cambios de agente automáticos.
