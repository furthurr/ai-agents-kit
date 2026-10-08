# Requisitos — Nivel de feature exclusivo de SDD

Modo SDD: standard
Fase: Requirements
Estado: cerrado
Gate 1: aprobado por el usuario («procede»)
Intención: implementación, una vez aprobados los gates de planificación

## Objetivo

Eliminar los avisos y recomendaciones de nivel de LLM del contrato operativo del
kit. SDD será el único componente que comunicará una calificación de la feature,
basada en su alcance analizado y su impacto en el proyecto, no en el modelo que
deba utilizarse ni en la siguiente tarea o fase.

## Historia 1: Calificación fundamentada de la feature

Como usuario quiero conocer el nivel de una feature después de definir su alcance
para entender su dificultad e impacto en el proyecto sin recomendaciones de LLM.

### Criterios (EARS)

- Req 1.1: CUANDO SDD haya realizado el análisis de una feature y haya definido su alcance deseado sin decisiones esenciales abiertas EL SISTEMA DEBERÁ comunicar una calificación entera de 1 a 10 fundamentada en ese alcance y su impacto en el proyecto.
- Req 1.2: MIENTRAS el análisis o el alcance de la feature estén incompletos EL SISTEMA DEBERÁ abstenerse de mostrar una calificación provisional.
- Req 1.3: CUANDO la calificación esté entre 1 y 7 inclusive EL SISTEMA DEBERÁ mostrar `Nivel de feature: <n> 🟢`.
- Req 1.4: CUANDO la calificación sea 8 o 9 EL SISTEMA DEBERÁ mostrar `Nivel de feature: <n> 🟠`.
- Req 1.5: CUANDO la calificación sea 10 EL SISTEMA DEBERÁ mostrar `Nivel de feature: 10 🔴`.
- Req 1.10: EL SISTEMA DEBERÁ sustituir `<n>` por la calificación real calculada; los ejemplos 3, 7 u 8 no serán valores fijos para sus respectivos rangos.
- Req 1.6: EL SISTEMA DEBERÁ asociar la calificación a la feature completa y no a tareas individuales, waves, fases, modelos o proveedores.
- Req 1.7: CUANDO cambie de fase sin cambiar el alcance evaluado EL SISTEMA DEBERÁ evitar repetir la calificación.
- Req 1.8: SI cambia materialmente el alcance o el impacto de una feature ENTONCES EL SISTEMA DEBERÁ volver a analizar el alcance antes de comunicar una calificación actualizada.
- Req 1.9: EL SISTEMA DEBERÁ conservar separados la calificación, la profundidad SDD y la estrategia de pruebas; una puntuación no sustituirá las reglas de elegibilidad de direct, lite y standard.

## Historia 2: Interacciones sin recomendaciones de modelo

Como usuario quiero que los agentes ejecuten el trabajo autorizado sin avisos de
modelo ni pausas artificiales para intervenir solo ante decisiones necesarias.

### Criterios (EARS)

- Req 2.1: EL SISTEMA DEBERÁ eliminar de todas las interacciones operativas, incluido SDD, los mensajes que recomiendan seleccionar o cambiar un LLM o anuncian un nivel de LLM BAJO, MEDIO o ALTO.
- Req 2.2: EL SISTEMA DEBERÁ eliminar las recomendaciones de nivel por tarea, operación o fase y los avisos de cambio de modelo previos y posteriores a procesos pesados.
- Req 2.3: MIENTRAS un componente distinto de SDD realice su actividad EL SISTEMA DEBERÁ abstenerse de emitir la calificación `Nivel de feature`.
- Req 2.4: CUANDO exista autorización suficiente y no haya una decisión esencial pendiente EL SISTEMA DEBERÁ continuar sin exigir «continúa», «listo» o confirmación por un nivel, modelo o calificación.
- Req 2.5: SI existe una decisión esencial, un gate real o una autorización pendiente ENTONCES EL SISTEMA DEBERÁ solicitar esa decisión y conservar los controles de seguridad aplicables.
- Req 2.6: EL SISTEMA DEBERÁ conservar los gates reales de SDD, las decisiones de alcance y ejecutor, las autorizaciones de remediación, exportación y escrituras sensibles y las confirmaciones de Git y acciones destructivas.
- Req 2.7: EL SISTEMA DEBERÁ abstenerse de seleccionar o cambiar el modelo del host.

## Historia 3: Contrato consistente entre fuentes y distribución

Como mantenedor quiero que fuentes, documentación, pruebas y salidas generadas
expresen el mismo contrato para no reintroducir avisos a través de otra plataforma.

### Criterios (EARS)

- Req 3.1: EL SISTEMA DEBERÁ actualizar los agentes, skills y referencias operativas afectados desde canonical y regenerar las salidas de todas las plataformas declaradas en el manifiesto sin editarlas manualmente.
- Req 3.2: EL SISTEMA DEBERÁ actualizar la documentación de uso vigente y los escenarios smoke afectados para describir la exclusividad de SDD y el momento de la calificación.
- Req 3.3: EL SISTEMA DEBERÁ disponer de pruebas de contrato que verifiquen límites 1, 7, 8, 9 y 10, ausencia de calificación antes del análisis y ausencia de avisos de modelo en los componentes operativos.
- Req 3.4: EL SISTEMA DEBERÁ verificar que las referencias retiradas no dejan enlaces operativos rotos ni recursos obsoletos en las salidas regeneradas.
- Req 3.5: EL SISTEMA DEBERÁ conservar las specs y evidencias históricas sin reescribirlas para aparentar cumplimiento del nuevo contrato.

## Alcance identificado

- Agentes SDD, Documentation Orchestrator, Code Review, Data API y UI Design.
- Skills sdd-spec, architecture, code-quality, security, data-api, ui-design,
  documentation-orchestrator y project-navigator; referencias auxiliares afectadas.
- Tests de contrato, documentación de uso y smoke, salidas generated.
- Git Release Manager y sus skills se revisan para asegurar ausencia de avisos;
  no se relajan sus confirmaciones de Git.

## Supuestos y límites

- Se reemplaza también la recomendación de LLM de SDD, no solo la de especialistas.
- El intervalo vigente es 1–10; no se introduce 0.
- La rúbrica verificable para asignar un entero y el punto exacto de publicación
  en direct, lite y standard se definirán en Design; deben respetar Req 1.1–1.9.
- No se extiende automáticamente la etiqueta «feature» a bugs, consultas o
  exploraciones que no tengan una feature con alcance definido.
- La calificación es una estimación ordinal fundamentada, no una medición exacta
  ni una estimación de tiempo o coste del LLM.
- Regenerar el repositorio no equivale a actualizar instalaciones del host.
  Reinstalación externa, commit, push y release no están incluidos por defecto.
- Hay modificaciones previas en el laboratorio SDD y documentación de seguridad;
  se preservarán sin atribuirlas a este trabajo.
- No hay AGENTS.md ni .sdd/steering en el workspace consultado.

## Evidencia de análisis inicial

- canonical/skills/sdd-spec/SKILL.md:84–119 define el contrato de recomendación
  por fase que debe reemplazarse.
- tools/test_model_recommendations.py exige hoy recomendaciones visibles para
  especialistas y avisos Navigator; su contrato debe invertirse, no solo borrarse.
- .architecture/README.md establece canonical como fuente y generated como salida
  regenerable.
- La descripción instalada de documentation-orchestrator aún exige confirmar
  antes de operar, mientras canonical declara continuidad sin pausa por modelo;
  una instalación antigua puede seguir mostrando ese comportamiento hasta actualizarse.
