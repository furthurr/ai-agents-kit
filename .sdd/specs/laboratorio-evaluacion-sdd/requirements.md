# Requisitos — Laboratorio de evaluación de SDD y modelos

- Modo SDD: standard
- Tipo de trabajo: exploración orientada a definir un laboratorio
- Intención: construir el laboratorio; ninguna campaña real hasta autorización explícita de kickoff con manifiesto y límites aprobados
- Fase: 1 — Requirements
- Estado: aprobado para Design
- Gate 0: preflight presentado; continuación autorizada por el usuario («procede»)
- Gate 1: aprobado explícitamente por el usuario («procede», tras presentación de requisitos revisados)
- Próxima fase tras aprobación: Design
- Carpeta del laboratorio: .agent-lab/sdd-escalation/
- Acuerdo de alcance: variante autónoma experimental aceptada por el usuario; requisitos revisados aprobados en Gate 1
- Aclaración aprobada: MAX es el modo de pensamiento seleccionado por el usuario en la interfaz, no parte del nombre del modelo

## 1. Problema y objetivos

El usuario necesita evidencia para decidir:

1. Bajo qué condiciones el modelo objetivo y su configuración MAX resuelven features correctamente.
2. Cuándo SDD lite reduce consumo sin degradar la calidad respecto de standard.
3. Cuándo otro modelo mejora resultados que el modelo objetivo con standard no logra.

Se solicita un catálogo de diez features, desde una simple hasta otra deliberadamente
exigente para modelos de frontera, ejecutables en sesiones independientes y evaluadas
posteriormente con pruebas y otro modelo. La dificultad final de la más exigente no
puede garantizarse antes de medirla.

El usuario aclara que **MAX es el modo de pensamiento/razonamiento** y que lo
seleccionará manualmente en la interfaz. «GPT-6-LUNA» es aún una denominación del
usuario: la campaña registrará el identificador real que exponga el cliente, sin
suponer un identificador de API ni que MAX sea parte del nombre del modelo.

## 2. Alcance y límites

Incluido en el laboratorio futuro: catálogo, campañas repetidas, sesiones aisladas,
comparación de modalidades/modelos, evaluación independiente, registros, control de
presupuesto y reportes con incertidumbre y limitaciones.

La campaña principal será autónoma experimental: diez intentos iniciales con
`lite-experimental` y reintentos desde cero con `standard-autonomous` para resultados
no exitosos válidos. Estas etiquetas son condiciones de laboratorio, no nuevas
profundidades SDD. Se mantienen las cuatro profundidades canónicas sin modificaciones.
La aprobación de esta variante no elimina los gates del trabajo que construye el laboratorio.

Esta spec solo planifica. No autoriza infraestructura, consumo de APIs, ejecución de
modelos, commits, publicación de datos ni modificación de las reglas canónicas de SDD.

Fuera de alcance: demostrar ausencia de cualquier defecto, acceso a razonamiento
interno privado, garantizar que una feature derrote a todos los modelos de frontera,
o extrapolar los resultados a cualquier lenguaje o proyecto.

## 3. Historias y criterios de aceptación EARS

### H1 — Catálogo de dificultad auditable

Como investigador, quiero diez tareas especificadas antes de las ejecuciones para
comparar resultados sin cambiar la meta después de observarlos.

- R01: EL SISTEMA DEBERÁ ofrecer un catálogo versionado de exactamente diez features, identificadas de F01 a F10 y ordenadas por dificultad prevista de 1 a 10.
- R02: EL SISTEMA DEBERÁ describir para cada feature su comportamiento esperado mediante criterios de aceptación con identificadores únicos.
- R03: EL SISTEMA DEBERÁ registrar para cada feature sus factores de dificultad: reglas e interacciones, estados y límites, módulos afectados, persistencia, concurrencia e integraciones.
- R04: EL SISTEMA DEBERÁ distinguir la dificultad prevista de la dificultad observada en los resultados.
- R05: EL SISTEMA DEBERÁ registrar para cada feature una decisión de elegibilidad para lite con su justificación basada en la versión de SDD utilizada.

### H2 — Comparaciones reproducibles

Como investigador, quiero controlar las condiciones para atribuir diferencias al
modelo o al flujo y no a cambios de contexto o al entorno.

- R06: CUANDO se prepare una campaña EL SISTEMA DEBERÁ fijar su matriz de features, modalidades, modelos y repeticiones antes de iniciar las ejecuciones.
- R07: CUANDO comience una ejecución EL SISTEMA DEBERÁ iniciar una sesión sin conversación ni artefactos de otras ejecuciones.
- R08: CUANDO se comparen dos condiciones de una feature EL SISTEMA DEBERÁ utilizar el mismo estado inicial, contrato de aceptación y evaluación externa.
- R09: EL SISTEMA DEBERÁ registrar por ejecución el identificador real del modelo, proveedor, configuración de razonamiento disponible, límites de contexto y parámetros expuestos por el cliente.
- R10: EL SISTEMA DEBERÁ registrar las versiones del proyecto inicial, instrucciones SDD, prompts, herramientas y entorno utilizadas en cada ejecución.
- R11: CUANDO se prepare una campaña EL SISTEMA DEBERÁ registrar el orden de ejecución y el procedimiento utilizado para reducir sesgos por orden.
- R12: SI cambia una condición fijada durante una campaña ENTONCES EL SISTEMA DEBERÁ identificar los resultados afectados como no directamente comparables con la condición anterior.

### H3 — Fidelidad al proceso SDD

Como responsable del MAS, quiero medir el cumplimiento del proceso por separado del
resultado funcional para no premiar soluciones que ignoran sus restricciones.

- R13: CUANDO una ejecución use standard canónico EL SISTEMA DEBERÁ detener el avance en los gates que requieren aprobación hasta recibir la aprobación explícita correspondiente.
- R14: CUANDO una ejecución use lite canónico EL SISTEMA DEBERÁ evaluar el cumplimiento de Quick Plan y de las reglas de verificación de esa modalidad.
- R15: SI una ejecución lite canónica detecta una exclusión de elegibilidad ENTONCES EL SISTEMA DEBERÁ registrar la detención y la solicitud de reclasificación como resultado del proceso, separado de la finalización funcional.
- R16: SI se autoriza reclasificar una ejecución ENTONCES EL SISTEMA DEBERÁ reportar su trayectoria como lite→standard, separada de las ejecuciones exclusivamente lite o standard.
- R17: EL SISTEMA DEBERÁ excluir las features no elegibles para lite de la comparación principal de ahorro lite frente a standard.
- R18: SI una campaña emplea una variante con gates automáticos o lite forzado ENTONCES EL SISTEMA DEBERÁ identificarla como condición experimental distinta del SDD canónico.
- R19: EL SISTEMA DEBERÁ registrar por ejecución las aprobaciones, correcciones, pistas e intervenciones humanas que puedan afectar el resultado.

### H4 — Evaluación independiente y verificable

Como evaluador, quiero comprobar el comportamiento contra un contrato independiente
del candidato para que sus propios tests no sean la única evidencia.

- R20: EL SISTEMA DEBERÁ fijar y versionar los criterios y pruebas externos de aceptación antes de ejecutar al candidato.
- R21: EL SISTEMA DEBERÁ mantener el contenido reservado de evaluación fuera del contexto y permisos de lectura del candidato.
- R22: CUANDO se evalúe una entrega EL SISTEMA DEBERÁ producir un resultado y evidencia asociados a cada criterio de aceptación.
- R23: EL SISTEMA DEBERÁ evaluar regresiones del comportamiento inicial que deba permanecer inalterado.
- R24: CUANDO intervenga un modelo auditor EL SISTEMA DEBERÁ ocultarle la identidad del modelo candidato y la etiqueta de condición experimental en la medida compatible con la auditoría.
- R25: EL SISTEMA DEBERÁ registrar la rúbrica, configuración, entrada y respuesta del modelo auditor como evidencia de su evaluación.
- R26: SI una opinión del auditor discrepa de una prueba externa ENTONCES EL SISTEMA DEBERÁ registrar la discrepancia sin sustituir automáticamente el resultado de la prueba.
- R27: EL SISTEMA DEBERÁ distinguir evaluación funcional, cumplimiento de SDD y revisión cualitativa del auditor.
- R28: EL SISTEMA DEBERÁ definir éxito funcional completo como cumplimiento de todos los criterios obligatorios y regresiones exigidas para la feature.

### H5 — Métricas para decisiones de costo y capacidad

Como usuario, quiero decidir a partir de tasas de éxito y costos observados, no de
una puntuación subjetiva única.

- R29: EL SISTEMA DEBERÁ distinguir éxito en la primera entrega evaluada de éxito obtenido después de ciclos de reparación.
- R30: EL SISTEMA DEBERÁ registrar las cantidades disponibles de tokens, costo, tiempo transcurrido, tiempo de espera de aprobaciones, intentos e intervenciones por ejecución.
- R31: SI una métrica no está expuesta por el proveedor o cliente ENTONCES EL SISTEMA DEBERÁ marcarla como no disponible y no sustituirla por cero.
- R32: CUANDO se agreguen resultados EL SISTEMA DEBERÁ mostrar el número de ejecuciones de cada condición y los resultados individuales que sustentan el agregado.
- R33: CUANDO se estime una tasa de éxito EL SISTEMA DEBERÁ presentar su incertidumbre y el tratamiento de ejecuciones inválidas o incompletas.
- R34: CUANDO se compare lite con standard EL SISTEMA DEBERÁ reportar tanto la diferencia de calidad como el consumo y costo por entrega exitosa bajo presupuestos explícitos.
- R35: CUANDO se recomiende escalar de modelo EL SISTEMA DEBERÁ respaldar la recomendación con ejecuciones comparables de ambos modelos bajo standard.
- R36: EL SISTEMA DEBERÁ limitar las recomendaciones a los perfiles de tarea, configuraciones y condiciones efectivamente evaluados.

### H6 — Ejecución controlada y conservación de evidencia

Como operador, quiero dejar el trabajo automatizable corriendo sin perder registros,
ignorar gates ni incurrir en consumo ilimitado.

- R37: CUANDO se configure una campaña EL SISTEMA DEBERÁ exigir límites explícitos de tiempo, consumo y ciclos de reparación antes de ejecutarla.
- R38: SI una ejecución alcanza un límite ENTONCES EL SISTEMA DEBERÁ detenerla y registrar el límite alcanzado junto con la evidencia obtenida.
- R39: CUANDO una ejecución espere una aprobación EL SISTEMA DEBERÁ identificarla como pendiente de intervención y no como fallo funcional.
- R40: SI una ejecución falla por infraestructura ENTONCES EL SISTEMA DEBERÁ clasificarla separadamente de un fallo atribuible a la solución candidata.
- R41: CUANDO se interrumpa una campaña EL SISTEMA DEBERÁ permitir reanudarla sin sobrescribir ejecuciones ya registradas ni omitir su estado anterior.
- R42: EL SISTEMA DEBERÁ conservar por ejecución los mensajes disponibles, llamadas a herramientas, artefactos SDD, cambios de código, salidas de evaluación y estado final vinculados a un identificador único.
- R43: EL SISTEMA DEBERÁ excluir credenciales y secretos de los registros conservados y reportes exportados.
- R44: EL SISTEMA DEBERÁ impedir que una ejecución modifique los artefactos o resultados de otra ejecución y el material reservado de evaluación.
- R45: EL SISTEMA DEBERÁ generar un reporte consultable y una exportación de resultados procesable automáticamente con referencias a su evidencia.

### H7 — Campaña autónoma de escalamiento experimental

Como investigador, quiero iniciar una campaña que intente las diez metas y escale
los resultados no exitosos sin aprobaciones humanas durante sus ejecuciones.

- R46: CUANDO se inicie una campaña autónoma autorizada EL SISTEMA DEBERÁ programar un intento inicial de cada una de las diez features con la condición lite-experimental, sujeto a los límites globales fijados.
- R47: CUANDO una feature no sea elegible para lite canónico EL SISTEMA DEBERÁ etiquetar su intento ligero como forzado experimental y excluirlo de conclusiones sobre lite canónico.
- R48: CUANDO una ejecución standard-autonomous alcance una transición de fase EL SISTEMA DEBERÁ registrar la decisión automática y su evidencia conforme a una política fijada antes de la campaña, sin atribuirle aprobación humana.
- R49: CUANDO una campaña autónoma esté en ejecución EL SISTEMA DEBERÁ avanzar conforme a su política predefinida sin solicitar intervención humana para sus transiciones experimentales.
- R50: CUANDO termine la ronda ligera EL SISTEMA DEBERÁ evaluar y clasificar sus diez resultados antes de programar la ronda de escalamiento.
- R51: CUANDO una ejecución ligera válida termine sin éxito completo EL SISTEMA DEBERÁ programar un intento standard-autonomous independiente para esa feature, sujeto a los límites globales fijados.
- R52: CUANDO se inicie un intento de escalamiento EL SISTEMA DEBERÁ restaurar el estado inicial de la feature sin transmitir código, conversación, diagnóstico ni feedback reservado del intento anterior.
- R53: SI una ejecución resulta inválida por infraestructura o evaluación ENTONCES EL SISTEMA DEBERÁ aplicar una política predefinida de repetición o exclusión sin usarla como evidencia de inferioridad del modelo o modalidad.
- R54: CUANDO se reporte la campaña escalonada EL SISTEMA DEBERÁ incluir el costo de los intentos ligeros fallidos en el costo total de la política de escalamiento.
- R55: CUANDO standard-autonomous se evalúe solo en features no exitosas de la ronda ligera EL SISTEMA DEBERÁ advertir que esa selección no estima su ventaja general sobre el flujo ligero.
- R56: CUANDO se prepare una ronda de control EL SISTEMA DEBERÁ fijar antes de ejecutarla el procedimiento para seleccionar features exitosas del flujo ligero que también se evaluarán con standard-autonomous.
- R57: SI se agota el presupuesto global ENTONCES EL SISTEMA DEBERÁ marcar los intentos pendientes como no ejecutados y no como fallos funcionales.
- R58: CUANDO se autorice una tercera ronda con otro modelo EL SISTEMA DEBERÁ usar el mismo protocolo standard-autonomous y punto inicial para comparar los casos escalados.
- R59: CUANDO el usuario haya seleccionado MAX en la interfaz EL SISTEMA DEBERÁ conservar su selección de modelo y variante en las sesiones de la campaña mediante herencia comprobada o propagación explícita del mismo valor, sin sustituirlos por otros.
- R60: SI no puede identificarse y verificarse la configuración seleccionada para una nueva ejecución ENTONCES EL SISTEMA DEBERÁ bloquear su invocación al modelo y registrar la limitación.

## 4. Requisitos no funcionales transversales

- Reproducibilidad: R07–R12 y R20 permiten identificar condiciones; no se promete salida determinista de un LLM.
- Integridad: R21, R42 y R44 separan candidato, evaluación y registros de otras ejecuciones.
- Auditabilidad: R19, R22, R25, R32 y R42 vinculan conclusiones con evidencia verificable.
- Control operativo: R37–R41 limitan consumo y hacen explícitas pausas y errores.
- Confidencialidad: R43 excluye secretos; se propone utilizar datos sintéticos, pendiente de aprobación.

## 5. Supuestos y propuestas pendientes de aprobación

1. Usar un proyecto sintético común, con puntos iniciales independientes por feature; no una cadena en la que los defectos de F01 contaminen F02.
2. Seleccionar features elegibles y no elegibles para lite. Las diez se intentarán con el flujo ligero experimental; los casos forzados no medirán cumplimiento ni viabilidad de lite canónico.
3. Empezar con un piloto y usar al menos tres repeticiones por condición como punto de partida operativo, no como garantía de suficiencia estadística.
4. Mantener la evaluación reservada accesible solo al evaluador y registrar por separado los tests que escriba el candidato.
5. No proporcionar feedback del evaluador reservado durante la medición al primer intento; cualquier reparación posterior debe seguir una política de feedback predefinida.
6. Los gates canónicos de standard tienen aprobación humana. La campaña utiliza decisiones automáticas explícitamente experimentales; este acuerdo no autoriza omitir los gates de planificación y construcción del laboratorio.
7. Versionar cada campaña; las correcciones de evaluación que alteren el veredicto requieren identificar o repetir las ejecuciones afectadas.
8. La política principal mide ligero→completo; no compara imparcialmente ambas modalidades sobre todo el catálogo. Se recomienda una ronda de control y repeticiones antes de inferir fronteras de capacidad.
9. Un flujo autónomo puede detenerse por límites o errores sin conseguir las diez entregas; no se garantiza finalización exitosa por el hecho de automatizarlo.

## 6. Decisiones abiertas

Estas decisiones no se consideran resueltas por la creación de este archivo:

- D01 — Dominio y stack: proyecto web/backend, CLI u otro; lenguaje y experiencia que se desea representar.
- D02 — Integración acordada: OpenCode. MAX es el modo que el usuario seleccionará en la interfaz. Pendiente identificar modelo/variante reales y verificar propagación de esa selección; no se asume que la etiqueta interna de variante sea `max`.
- D03 — Comparador y auditor: modelos disponibles y posibilidad de separar ambas funciones.
- D04 — Presupuesto: techo económico, tiempo disponible y política de reparación.
- D05 — Operación: política verificable de decisiones automáticas, autorización inicial y límites de permisos de la campaña. Durante las ejecuciones experimentales no habrá aprobaciones humanas.
- D06 — Política de decisión: confiabilidad mínima aceptable, tolerancia de degradación lite/standard y precisión estadística buscada.
- D07 — Exigencia del catálogo: amplitud de perfiles frente a progresión dentro de un único dominio; concretar las diez features en el diseño.

No se fijará un umbral de escalamiento universal ni se calificará una solución como
«perfecta» fuera de los criterios evaluados. Un piloto informa el diseño de campañas
posteriores, pero no demuestra por sí solo una frontera estable de capacidad.

## 7. Contexto consultado y siguiente gate

Fuente metodológica: skill sdd-spec y referencias de selección de nivel de LLM y EARS.
No se encontraron AGENTS.md, .sdd/steering ni .quality/README.md en la búsqueda inicial.
Se recomienda revisión del especialista de calidad para el protocolo de evaluación;
esta fase no crea documentación de dominio ni implementa el laboratorio.

Gate 1 aprobado: requisitos revisados autorizados para elaborar design.md.
Design concretará el catálogo, evaluación, métricas, aislamiento y estrategia de
pruebas; Tasks y cualquier implementación siguen sujetos a sus gates correspondientes.
