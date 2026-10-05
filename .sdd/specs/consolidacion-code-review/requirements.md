# Requisitos — Consolidación de agentes en Code Review

Modo SDD: standard
Fase: Requirements
Estado: aprobado
Gate 0: reanudado por el usuario
Gate 1: aprobado por el usuario («procede»)
Tipo de trabajo: feature
Intención: implementación
Estrategia de pruebas propuesta: TDD focalizado para contratos nuevos; regresión para comportamiento existente

## Objetivo y motivo

Ofrecer una sola entrada `code-review` para revisar calidad y seguridad sin exigir
al usuario cambiar de agente entre ambos dominios. Conservar la especialización
de las skills y la trazabilidad existente, y evitar confirmaciones documentales
repetidas dentro de una revisión autorizada.

## Contexto observado

- `canonical/manifest.json` declara nueve agentes y diez skills en cinco
  plataformas: Copilot, OpenCode, Kiro, Claude y Pi.
- Los agentes actuales `code-quality` y `security` tienen flujos simétricos, pero
  prohíben trabajar en el dominio del otro y reciben targets diferentes.
- Las skills mantienen criterios Sonar y OWASP/CWE, severidades y registros
  separados en `.quality/` y `.security/`.
- El contrato de handoff y `tools/handoff_contract.py` asignan actualmente una
  carpeta a cada target; no contemplan un receptor con dos dominios seleccionables.
- No se encontró steering, Navigator ni README canónico de arquitectura. Se usa
  evidencia directa del repositorio; el contexto arquitectónico imprescindible
  se recogerá en Design. Se recomienda Architecture para documentar el kit en una
  operación independiente, no como prerrequisito de esta feature.

## Historia 1: Una entrada para revisión

Como usuario quiero invocar `code-review` para revisar calidad y seguridad sin
elegir entre dos agentes ni transferir manualmente hallazgos entre ellos.

### Criterios (EARS)

- Req 1.1: CUANDO se genere el catálogo de agentes EL SISTEMA DEBERÁ ofrecer
  `code-review` como sustituto de `code-quality` y `security`, sin publicar esos
  dos agentes anteriores como entradas adicionales.
- Req 1.2: CUANDO se solicite explícitamente una revisión solo de calidad o solo
  de seguridad EL SISTEMA DEBERÁ aplicar únicamente el dominio solicitado dentro
  del alcance de archivos o módulos indicado.
- Req 1.3: CUANDO se solicite una revisión completa EL SISTEMA DEBERÁ cubrir
  calidad y seguridad en una misma interacción y presentar un resumen conjunto
  que identifique los dominios revisados y sus limitaciones.
- Req 1.4: SI la solicitud no permite determinar un alcance material de revisión
  ENTONCES EL SISTEMA DEBERÁ aclararlo antes de ampliar el análisis.

## Historia 2: Especialización y registros conservados

Como mantenedor quiero conservar las dos skills para mantener sus estándares y
continuar trabajando con hallazgos existentes sin migrar sus registros.

### Criterios (EARS)

- Req 2.1: EL SISTEMA DEBERÁ conservar las skills `code-quality` y `security` y
  aplicar los criterios Sonar a calidad y OWASP/CWE a seguridad.
- Req 2.2: CUANDO se registren o actualicen hallazgos EL SISTEMA DEBERÁ mantener
  los hallazgos de calidad en `.quality/` con IDs `QLT` y los de seguridad en
  `.security/` con IDs `SEC`, conservando IDs y estados de registros existentes.
- Req 2.3: CUANDO un análisis de calidad encuentre un riesgo de seguridad dentro
  de una revisión de ambos dominios EL SISTEMA DEBERÁ tratarlo con los criterios
  de la skill `security` sin exigir cambiar de agente ni duplicar el hallazgo.
- Req 2.4: CUANDO se presente el resumen conjunto EL SISTEMA DEBERÁ conservar la
  severidad y referencia originales de cada dominio sin asumir equivalencias
  entre las escalas Sonar y OWASP.

## Historia 3: Documentar sin preguntas redundantes

Como usuario quiero que una auditoría documental autorizada deje sus resultados
persistidos sin tener que volver a elegir qué severidades guardar.

### Criterios (EARS)

- Req 3.1: CUANDO se solicite auditar y documentar, inicializar o sincronizar un
  dominio de revisión EL SISTEMA DEBERÁ registrar todos los hallazgos verificados
  y distintos dentro del alcance autorizado, sin pedir un filtro por severidad.
- Req 3.2: CUANDO existan ocurrencias repetidas de una misma causa EL SISTEMA
  DEBERÁ agruparlas con sus ubicaciones, sin crear un finding por ocurrencia.
- Req 3.3: CUANDO la petición sea una consulta exploratoria o una inspección de
  solo lectura EL SISTEMA DEBERÁ responder sin crear ni actualizar registros,
  cachés de estándares o marcas de sincronización.
- Req 3.4: SI existe ambigüedad de proyecto, volumen excepcional que requiera
  cambiar el alcance, sobrescritura de trabajo manual o escritura fuera del
  alcance autorizado ENTONCES EL SISTEMA DEBERÁ solicitar la decisión pendiente
  antes de ejecutar esa escritura.
- Req 3.5: CUANDO la misma operación documental ya esté autorizada en la sesión
  EL SISTEMA DEBERÁ reutilizar esa autorización para su mismo alcance, sin
  trasladarla a remediación, otros proyectos ni ampliaciones de escritura.

## Historia 4: Orquestación y handoffs acotados

Como usuario del orquestador quiero derivar una o ambas revisiones a `code-review`
sin perder los límites de lectura y escritura del dominio solicitado.

### Criterios (EARS)

- Req 4.1: CUANDO el orquestador derive calidad, seguridad o ambas EL SISTEMA
  DEBERÁ dirigir el trabajo a `code-review` con los dominios y alcances explícitos,
  sin ejecutar localmente la misma acción que haya derivado.
- Req 4.2: CUANDO se reciba un handoff de `code-review` EL SISTEMA DEBERÁ validar
  que el alcance se limita a `.quality/`, `.security/` o ambas según lo solicitado,
  y que la evidencia devuelta pertenece a ese alcance original.
- Req 4.3: SI un handoff contiene rutas fuera del proyecto, carpetas no
  autorizadas, target desconocido, acción no admitida o permisos incoherentes
  ENTONCES EL SISTEMA DEBERÁ rechazarlo antes de ejecutar la operación.
- Req 4.4: CUANDO el handoff tenga acción `inspect` EL SISTEMA DEBERÁ exigir
  ausencia de escritura y conservar la inspección en solo lectura.
- Req 4.5: CUANDO se procese un handoff válido EL SISTEMA DEBERÁ conservar los
  límites técnicos del host, la correlación de emisión y respuesta y los
  contratos de los otros especialistas sin ampliarlos.

## Historia 5: Remediación segura y alcance de seguridad

Como usuario quiero que el nuevo agente mantenga las salvaguardas de corrección
y no reduzca una auditoría de seguridad a lectura de código fuente.

### Criterios (EARS)

- Req 5.1: CUANDO una revisión de seguridad lo requiera EL SISTEMA DEBERÁ incluir
  configuración, autenticación, red, permisos, almacenamiento y dependencias
  dentro del alcance solicitado, además del código fuente.
- Req 5.2: EL SISTEMA DEBERÁ documentar la existencia y ubicación de datos
  sensibles con placeholders, sin exponer secretos, credenciales ni valores de PII.
- Req 5.3: CUANDO se proponga remediar un hallazgo EL SISTEMA DEBERÁ solicitar
  autorización antes del primer micro-paso y de cada micro-paso posterior;
  autorizar una auditoría o su documentación no autoriza modificar producto.
- Req 5.4: SI la corrección requiere requisitos, diseño o coordinación fuera de
  una corrección segura localizada ENTONCES EL SISTEMA DEBERÁ recomendar SDD y
  detenerse antes de modificar código.
- Req 5.5: CUANDO se pretenda marcar un hallazgo resuelto EL SISTEMA DEBERÁ
  verificar la evidencia de su corrección antes de cambiar su estado.

## Historia 6: Distribución y verificación

Como mantenedor quiero distribuir el agente consolidado en todas las plataformas
del kit y verificar su funcionamiento y sus contratos.

### Criterios (EARS)

- Req 6.1: CUANDO se renderice el kit EL SISTEMA DEBERÁ generar `code-review` en
  Copilot, OpenCode, Kiro, Claude y Pi con permisos acordes al rol, conservar ambas
  skills y producir un catálogo de ocho agentes y diez skills.
- Req 6.2: CUANDO se publiquen las guías y ejemplos vigentes EL SISTEMA DEBERÁ
  distinguir los agentes de las skills, sustituir las invocaciones a los agentes
  retirados por `code-review` y explicar la actualización de instalaciones previas.
- Req 6.3: CUANDO se validen los cambios EL SISTEMA DEBERÁ contar con pruebas
  contractuales para revisiones de un dominio y de ambos, handoffs válidos e
  inválidos, restricciones de escritura y paridad de las plataformas.
- Req 6.4: CUANDO se cierre la feature EL SISTEMA DEBERÁ registrar comandos,
  resultados y límites de evidencia, diferenciando tests de contratos de prompts
  de pruebas manuales de comportamiento en un host real.

## Límites y supuestos para aprobación

- El nombre elegido es `code-review`, no `cede-review`.
- Se sustituyen los agentes antiguos sin aliases; sus skills y registros siguen
  disponibles. Este es el alcance anunciado antes de las solicitudes de proceder.
- La reducción de preguntas documentales se aplica a las dos skills de revisión
  y su coordinación; no extiende esta feature a Architecture, Data & API o UI.
- No se elimina la pausa de recomendación de modelo para tareas puntuales en esta
  feature; la inconsistencia de esa política se tratará por separado. Dentro de
  una misma revisión se evita duplicar un preflight ya satisfecho.
- No se ejecutan instalaciones sobre la configuración del usuario, commits,
  pushes, tags ni cambios de versión como parte de esta implementación.
- No se modifica ni reorganiza documentación histórica de specs cerradas para
  borrar referencias que eran correctas en su momento.

## Gate actual

Gate 1 aprobado. Estado posterior y evidencias en `tasks.md` y `verification.md`.
