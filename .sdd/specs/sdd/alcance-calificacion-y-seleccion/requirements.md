# Requisitos — Alcance, calificación y selección de profundidad SDD

Modo SDD: standard
Fase: Requirements
Estado: aprobado
Gate 1: aprobado por el usuario («procede»)
Intención: implementación tras aprobar los gates correspondientes

## Objetivo

Definir el alcance antes de elegir profundidad SDD, publicar una estimación de
esfuerzo y una recomendación concisa, permitir selección manual y priorizar
entregas incrementales cuando el alcance completo sea complejo.

Este cambio del contrato se desarrolla con el flujo vigente. Las reglas propuestas
no se aplican retroactivamente para omitir las aprobaciones de esta spec.

## Calificación de este cambio

- Esfuerzo previsto del LLM: 4 🟢
- Referente del laboratorio: F04, comparación ordinal de normalización y conflictos.
- Justificación: coordina reglas de clasificación y precedencia; resuelve conflictos
  entre nota, atención y elegibilidad; reutiliza render y validadores existentes;
  exige regresiones del contrato y coherencia entre distribuciones.
- Supuestos relevantes: no cambia el runtime, los adaptadores ni el instalador;
  las pruebas automáticas comprueban contratos textuales, no garantizan conducta LLM.
- Alcance evaluado: agente, skill, referencias, documentación, pruebas y render.

## Historia 1 — Alcance común antes de profundidad

Como usuario quiero acordar el resultado antes de seleccionar el proceso SDD.

- Req 1.1: CUANDO se reciba una solicitud nueva, EL SISTEMA DEBERÁ definir objetivo,
  resultados, límites y criterios verificables antes de elegir profundidad.
- Req 1.2: SI faltan decisiones esenciales, ENTONCES EL SISTEMA DEBERÁ preguntar
  únicamente lo necesario para resolverlas antes de calificar.
- Req 1.3: CUANDO la solicitud ya esté suficientemente definida, EL SISTEMA DEBERÁ
  reutilizar esa información sin preguntas ni introducciones ceremoniales.
- Req 1.4: CUANDO se formalice una spec, EL SISTEMA DEBERÁ reutilizar el alcance
  acordado manteniendo criterios EARS, errores, casos límite y supuestos pertinentes.
- Req 1.5: CUANDO se evalúe el esfuerzo, EL SISTEMA DEBERÁ consultar el contexto
  técnico mínimo necesario para distinguir infraestructura existente de trabajo pendiente.

## Historia 2 — Calificación y atención

- Req 2.1: CUANDO quede definido el alcance de una feature y su impacto, EL SISTEMA
  DEBERÁ publicar una única nota 1–10 o 10+ antes de recomendar profundidad.
- Req 2.2: CUANDO presente la calificación, EL SISTEMA DEBERÁ omitir del mensaje
  rutinario el referente de laboratorio y la explicación de rangos y exclusiones.
- Req 2.3: CUANDO registre una feature en una spec, EL SISTEMA DEBERÁ conservar
  referente, justificación y supuestos para trazabilidad sin repetir la nota al usuario.
- Req 2.4: SI una feature menor de 10 presenta complicaciones concretas controlables,
  ENTONCES EL SISTEMA DEBERÁ mostrar atención naranja y una advertencia específica
  sin modificar artificialmente su nota de esfuerzo.
- Req 2.5: CUANDO publique 10 o 10+, EL SISTEMA DEBERÁ usar indicador rojo.
- Req 2.6: SI cambia materialmente el alcance, ENTONCES EL SISTEMA DEBERÁ reevaluarlo
  antes de actualizar la calificación y la recomendación.
- Req 2.7: CUANDO el trabajo sea bugfix, consulta o exploración, EL SISTEMA DEBERÁ
  conservar su tratamiento específico sin inventar una calificación de feature.

## Historia 3 — Recomendación y elección

- Req 3.1: CUANDO una feature obtenga 1–3 y sea trivial, localizada, reversible y
  verificable, EL SISTEMA DEBERÁ recomendar direct.
- Req 3.2: CUANDO una feature obtenga 4–9 y tenga alcance claro, acotado y garantías
  verificables, EL SISTEMA DEBERÁ priorizar lite.
- Req 3.3: SI un alcance 1–3 no es trivial pero cumple condiciones de lite,
  ENTONCES EL SISTEMA DEBERÁ recomendar lite en lugar de forzar direct.
- Req 3.4: SI existen complicaciones acotadas de concurrencia o integridad con
  mecanismos adecuados y pruebas viables, ENTONCES EL SISTEMA DEBERÁ permitir
  evaluar lite con atención especial, sin exclusión automática por esas palabras.
- Req 3.5: SI faltan garantías verificables o persiste incertidumbre esencial,
  ENTONCES EL SISTEMA DEBERÁ aclarar el alcance o recomendar standard sin ocultar
  esa limitación cuando sea necesaria para decidir.
- Req 3.6: CUANDO recomiende profundidad, EL SISTEMA DEBERÁ permitir aceptar la
  recomendada o seleccionar otra elegible antes de ejecutar su flujo.
- Req 3.7: SI el usuario ya eligió explícitamente una profundidad compatible,
  ENTONCES EL SISTEMA DEBERÁ respetarla sin repetir la elección ni rebajar standard.
- Req 3.8: CUANDO se seleccione una profundidad, EL SISTEMA DEBERÁ mantener
  independientes permisos, intención, ejecutor, testing y aprobaciones de fase.

## Historia 4 — Entregas incrementales

- Req 4.1: CUANDO el alcance completo obtenga 10 o 10+, EL SISTEMA DEBERÁ recomendar
  standard para el conjunto y ofrecer dividirlo en entregas incrementales.
- Req 4.2: CUANDO proponga entregas, EL SISTEMA DEBERÁ definir resultados verificables,
  límites y dependencias sin separar garantías que deban cumplirse juntas.
- Req 4.3: CUANDO una entrega tenga alcance definido, EL SISTEMA DEBERÁ evaluarla
  individualmente sin asumir que su nota será menor que la del conjunto.
- Req 4.4: SI una entrega sigue siendo 10 o 10+, ENTONCES EL SISTEMA DEBERÁ evaluar
  otra división útil o mantener standard cuando no exista una separación segura.
- Req 4.5: CUANDO divida el alcance, EL SISTEMA DEBERÁ conservar los requisitos
  transversales y prever verificación de integración entre entregas.

## Historia 5 — Ejecución y routing conservados

- Req 5.1: CUANDO se elija direct, EL SISTEMA DEBERÁ ejecutar y verificar el alcance
  autorizado sin Quick Plan ni archivos formales de spec, y presentar evidencia breve.
- Req 5.2: CUANDO se elija lite, EL SISTEMA DEBERÁ generar Quick Plan y, si implementa,
  verificación compacta sin Gates 1–3 ni Gate 4.
- Req 5.3: CUANDO se elija standard, EL SISTEMA DEBERÁ conservar los Gates 1–4 sin
  inferir aprobación de requisitos por la conversación de alcance o selección de modo.
- Req 5.4: CUANDO el alcance ejecutable sea exclusivamente visual o de datos,
  EL SISTEMA DEBERÁ conservar la recomendación manual de ui-design o data-api.
- Req 5.5: CUANDO el usuario elija un especialista, EL SISTEMA DEBERÁ entregar
  contexto copiable y detener esa actividad en SDD sin invocarlo automáticamente.
- Req 5.6: CUANDO el alcance sea ambiguo o mixto, EL SISTEMA DEBERÁ mantener la
  definición y planificación en SDD.
- Req 5.7: CUANDO solo se solicite planificación, EL SISTEMA DEBERÁ abstenerse de implementar.

## Alcance y límites de esta actualización

- Actualizar fuentes canónicas, referencias afectadas, documentación y pruebas;
  regenerar distribuciones con las herramientas existentes, sin editarlas a mano.
- Mantener exactamente tres profundidades y las opciones deep/TDD estricto retiradas.
- No sustituir la rúbrica de esfuerzo por una puntuación de riesgo ni inventar pruebas.
- Las pruebas lite descritas por el usuario motivan la política, pero no certifican
  todos los casos posibles de nivel 1–9.
- No instalar cambios globales, hacer commit, push o release como parte de esta spec.
- Conservar specs históricas y gates pendientes; no migrarlas automáticamente.

## Punto que concretará Design

Definir criterios verificables de complicación controlable y límites que siguen
requiriendo standard; no interpretar naranja como autorización para ignorar riesgos.
