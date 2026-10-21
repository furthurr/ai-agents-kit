# SDD-Tiny — spec breve de documento único

SDD-Tiny es una profundidad canónica del MAS. Nombre visible: **SDD-Tiny**;
identificador de modo: `tiny`. No usa como ID canónico `sdd-tiny-experimental`, que
pertenece exclusivamente al piloto F10.

## Cuándo usarlo

Es la recomendación base para features con nota 4–8, si el alcance definido cabe en
una entrega cohesiva y puede verificarse con pruebas proporcionales al riesgo. La
nota orienta, pero no certifica elegibilidad ni selecciona el modo. Respeta una
elección explícita previa compatible; si Tiny no es seguro/elegible, explica el
conflicto y aplica `scope-depth.md`.

Tipo de trabajo, nota, profundidad, intención y testing siguen siendo ejes
independientes. No califiques bugs, consultas ni exploraciones. Un bugfix usa Tiny
solo por elección explícita del usuario y conserva regresión/causa raíz. Solo
planificación no implementa.

## Documento único y ruta

- Usa un único archivo `.sdd/specs/<ruta-spec>/spec.md`, respetando las reglas de
  rutas planas o agrupadas de `SKILL.md`.
- Crea `spec.md` con estado inicial `Planificado` **antes de modificar código de
  producto**. Después, actualiza ese mismo archivo como documento vivo; no crees una
  copia inicial/final en la ruta de entrega ni archivos `requirements.md`,
  `design.md`, `tasks.md` o `verification.md` para esta misma spec.
- Conserva cuatro secciones concisas: `Alcance y aceptación`, `Enfoque técnico y
  estrategia de pruebas`, `Checklist` y `Verificación y cierre`.
- Alcance y aceptación incluye objetivo, resultados, comportamientos, condiciones,
  criterios observables, errores/casos límite, invariantes, exclusiones y supuestos.
- El enfoque técnico se limita a decisiones necesarias, patrones/mecanismos
  existentes, riesgos relevantes y estrategia de prueba. No exige una fase de Design,
  Quick Plan, gramática EARS, arquitectura extensa ni matriz completa de
  trazabilidad. No exige Quick Plan.
- La checklist es corta y verificable; enlaza requisitos y pruebas cuando aporte
  claridad, sin requerir el formato completo de Tasks/Waves de Standard.
- Verificación y cierre registra estrategia, comandos exactos y resultados
  realmente observados, estado de checklist, excepciones, limitaciones y estado final.
  Registra también los fallos locales previos/iniciales y su reparación: no reemplaces
  la historia por el resultado verde final.
- No exijas hashes, checkpoints de sandbox o instrumentación de laboratorio que el
  host no proporcione. El control canónico es crear el documento inicial antes del
  código y actualizar ese mismo documento; no afirmes evidencia técnica que no tengas.

La tabla de modos usa el marcador `Modo SDD: tiny`. Al reanudar, verifica el marcador,
estado, autorización y gates; la mera presencia de `spec.md` no aprueba nada. Si hay
varias specs plausibles, pide la ruta sin elegir solo por nombre final.

## Gates, selección e intención

- La etapa de alcance común presenta el alcance funcional completo y resuelve su
  validación explícita y la elección del usuario antes de escribir el spec. No es
  Gate 1 y no aprueba el spec ni una fase.
- Si la intención incluye implementación, presenta el `spec.md` inicial y espera el
  **Gate 3 existente** (aprobación del plan y autorización para iniciar la
  implementación) antes de cambiar código. El score y la recomendación no lo aprueban.
- Tras implementar, ejecutar pruebas/checks, completar el mismo documento y presentar
  sus resultados reales, espera el **Gate 4 existente** para cerrar o cubrir huecos.
- En solo planificación, deja `Estado: Planificado`, no implementa ni inventa
  verificación; Gate 3 y Gate 4 quedan como no aplicables a esa intención.
- No se crean gates nuevos para la nota, la recomendación, la creación del archivo ni
  la confirmación del modo. Si el usuario había elegido explícitamente `standard`,
  conserva `standard` y sus Gates 1–4; no conviertas la petición a Tiny. `standard`
  solo se activa por petición explícita.
- Si una elección Tiny previa ya es compatible, no vuelvas a pedir que elija modo;
  resuelve únicamente validación o gate que siga pendiente. Permisos del host,
  autorización y límites de alcance permanecen vigentes.

## Pruebas y evidencia

Tiny reduce documentos, no controles de comportamiento:

- Comportamiento observable nuevo o modificado: verificación focalizada conforme a
  `testing.md`, salvo excepción justificada; cubre los criterios y riesgos relevantes
  con tests o checks adecuados.
- Bugfix: regresión del caso afectado y verificación del arreglo. Legado/refactor:
  caracterización del comportamiento que debe preservarse.
- Sin cambio observable: no agregues tests por ceremonia; registra check existente o
  razón y ejecuta la verificación pertinente.
- Concurrencia, persistencia, idempotencia, recuperación o integridad requieren
  invariantes comprobables, mecanismo real/seam representativo y pruebas suficientes
  de fallos/reintentos/estados pertinentes. Un mock que oculte el mecanismo crítico
  no prueba la garantía.
- Antes de cerrar, cada casilla completada debe tener artefacto o evidencia de un
  comando ejecutado. Marca como pendiente/no ejecutado lo que no corriste. Si un
  comando falla, conserva el resultado, describe la reparación y registra la nueva
  ejecución sin borrar el fallo inicial.

Aplica `integrity-gate.md`, `quality-bar.md` proporcionalmente y permisos efectivos.
La prueba no autoriza ampliar la implementación; el alcance y la intención aceptados
siguen delimitándola.

## Antecedente experimental F10 — alcance de la evidencia

El piloto experimental documentado en `.agent-lab/sdd-escalation/` inspiró el
formato de documento único, no la política completa de este modo canónico. La
condición se llamó históricamente `lite2-experimental` en el run
`pilot-94ac27b7-36cd-4af2-81be-ffa4963fc38f`; ese nombre y los artefactos históricos
no se renombran ni representan otra condición. El nombre visible actual es SDD-Tiny;
el identificador de esa condición experimental fue `sdd-tiny-experimental`, distinto
del ID canónico `tiny`.

Fuentes de procedencia: `.agent-lab/sdd-escalation/SDD-TINY.md` conserva el contrato
experimental activo; `.agent-lab/sdd-escalation/results/f10-lite2-first-real-pilot.md`
describe la única ejecución real y sus métricas;
`.agent-lab/sdd-escalation/results/f10-sdd-tiny-technical-review-2026-10-12.md` y el
`post-run-audit.json` del run preservan revisión y telemetría. Se leen como evidencia
histórica, no se editan ni reclasifican al cambiar el flujo canónico.

En esa única ejecución real F10, el candidato implementó solo los cuerpos de
`Saga.submit`, `Saga.step` y `Saga.get` sobre un scaffold que ya proporcionaba
esquema, participantes, validadores, inicialización y locks. Un `spec.md` inicial
fue observado antes del cambio de código, el documento único se actualizó y el hash
final coincidió con el spec entregado. Pasaron los seis criterios externos. La
ejecución registró 15 pasos, una invocación CLI, 278 037 tokens reportados por el
cliente y 763.267 segundos totales, incluido el evaluador externo.

La telemetría local registró un primer fallo de crash injection (`InjectedCrash` no
observado), seguido por 11 verificaciones locales verdes en tres ejecuciones
(7 + 2 + 2). El post-run audit conserva el fallo inicial aunque el spec final no lo
menciona; esta omisión limita la trazabilidad y no debe repetirse en el flujo
canónico. Los seis criterios externos, el scaffold específico y estas métricas
describen solo F10 y una ejecución: no demuestran superioridad universal en rapidez,
fiabilidad o corrección, ni justifican quitar gates, pruebas o salvaguardas del MAS.
