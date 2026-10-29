# Changelog

Historial de cambios de MAS (Multi-Agent System). Las versiones siguen SemVer y
los tags usan el formato `vX.Y.Z`.

## [3.4.1] - 2026-10-28

### Correcciones

- Permitir que Documentation Orchestrator cree o actualice el `README.md` raíz,
  también si se llama `readme.md`, dentro del alcance documental aprobado.
- Incluir ambas variantes en los permisos de edición de OpenCode con nivel `ask`,
  igual que las guías bajo `docs/`, sin habilitar edición general de producto.
- Reconocer «documenta el README.md» como mantenimiento documental de escritura,
  conservando el preflight, el plan y la gestión del bloque documental de `AGENTS.md`.

### Documentación

- Aclarar el contexto del proyecto en Project Navigator.
- Actualizar la guía de Documentation Orchestrator y regenerar sus instrucciones
  compartidas para las seis plataformas.

### Pruebas

- Añadir una prueba de regresión del alcance README y del orden de los permisos
  de edición de OpenCode. Es una comprobación de contrato, no un smoke del host.

## [3.4.0] - 2026-10-22

### Funcionalidades

- Añadir `tools/configure_autonomy.py` como utilidad experimental y optativa para
  preparar perfiles locales de autonomía sin lanzar un prompt en el host.
- Incorporar adaptaciones para OpenCode, Claude Code, Copilot CLI, Kiro,
  Antigravity CLI/App/IDE y Pi, con cobertura parcial según la superficie.
- Usar vista previa por defecto; aplicar cambios solo con `--apply`, creando
  respaldos previos y ofreciendo `--restore` con comprobación del contenido
  posterior para no sobrescribir ediciones más recientes.
- Añadir 19 pruebas aisladas del configurador y su ejecución en CI.

### Documentación

- Sustituir el prompt YOLO por seis prompts independientes de autonomía,
  optimizados por host, y retirar `docs/extra-tools/modo-yolo.md`.
- Incorporar en el `AGENTS.md` raíz únicamente la guía documental gestionada;
  este archivo no activa el perfil autónomo ni concede permisos técnicos.

### Activación voluntaria

- Publicar o instalar el kit no ejecuta el configurador. No se modifican las
  fuentes `canonical/`, los adaptadores, `generated/` ni los instaladores normales
  por esta funcionalidad.
- Consultar la ayuda con `python3 -B tools/configure_autonomy.py --help`.
  Para OpenCode, `python3 -B tools/configure_autonomy.py --host opencode` muestra
  la vista previa; añadir `--apply` autoriza la escritura del perfil seleccionado.
- No existe una opción `--dry-run` en el configurador: la vista previa es el
  comportamiento predeterminado. Los cambios aplicados pueden ser globales
  para el host y afectar sesiones futuras; no se limitan a la carpeta de ejecución.

### Verificación

- 204 pruebas unitarias correctas, incluidas las 19 del configurador.
- 334 comprobaciones de instalación y 416 de integridad correctas.
- 22 pruebas de integración del instalador/exportador Antigravity correctas en
  macOS; no acreditan la ejecución del configurador dentro de ese host.
- Render, validación, enlaces, contratos y comprobación de diferencias correctos;
  el render no introduce cambios en `generated/`.
- Escaneo acotado de firmas de secretos y revisión contextual antes de publicar;
  no equivale a una auditoría universal de credenciales.

### Límites y pendientes

- Las pruebas del configurador usan perfiles temporales. No se certifica su
  aceptación runtime en todas las versiones, variantes o sistemas operativos.
  Permitir shell no crea un sandbox ni protege todo secreto frente a subprocesos.
- El configurador procesa JSON estricto y formas concretas de YAML/frontmatter;
  no resuelve todos los archivos, esquemas, hooks ni políticas efectivas del host.
- En OpenCode, `--project` también modifica configuración global. En un perfil
  nuevo debe prepararse primero el global sin `--project` para crear el archivo
  de instrucciones referenciado. La selección `bash`/`shell` no migra por sí sola
  todo el frontmatter de los agentes entre versiones.
- En Kiro, `--network` se añade al insertar inicialmente el bloque de reglas;
  volver a ejecutarlo sobre un bloque existente no agrega ni revoca esa regla.
- Copilot CLI solo persiste escritura y comandos suministrados. Antigravity
  App/IDE requieren ajustes de permisos en la interfaz; Pi recibe instrucciones,
  no un sistema de permisos por acción. Los modos de revisión y las políticas
  del host pueden conservar confirmaciones.
- Queda pendiente documentar el uso del script y actualizar la matriz en
  `docs/extra-tools/modo-autonomo.md` y `docs/permisos-hosts.md`; esta release no
  presenta esas guías como actualizadas para el configurador.

## [3.3.5] - 2026-10-21

### Correcciones

- Permitir al orquestador mantener Markdown bajo `docs/` con aprobación,
  preservando los permisos de `AGENTS.md` y las restricciones del rol.
- Alinear agentes, skills y workflows en las seis plataformas.
- Añadir regresiones de escritura, edición, rechazo y límites de permisos.

### Documentación

- Incorporar el prompt YOLO y trasladarlo a `docs/extra-tools/`.
- Documentar la actualización de perfiles y los límites de verificación.

### Verificación

- 185 pruebas unitarias, 334 comprobaciones de instalación y 416 de integridad.
- Validación y enlaces correctos.
- Runtime comprobado en OpenCode y Pi; las demás plataformas mantienen
  los pendientes indicados en la documentación.

## [3.3.4] - 2026-10-21

### Correcciones

- Eliminar la obligación de TDD/test-first en todos los modos SDD y adoptar
  verificación focalizada según criterios y riesgos; conservar regresión para bugs,
  caracterización para legado y PBT condicional.
- Actualizar instrucciones, plantillas, guía de uso y smoke tests; regenerar agentes
  y skills para las seis plataformas. Se preservan las specs históricas.

### Verificación

- Validación y enlaces correctos; contrato SDD 762/762, integridad 416/416,
  instalación 334/334, descubrimiento unittest 183 pruebas y contrato nativo
  Antigravity en macOS 22/22.

## [3.3.3] - 2026-10-19

### Correcciones

- Corregir los permisos distribuidos del orquestador documental para editar
  AGENTS.md tras aprobación: Kiro lo excluye del deny general y conserva ask;
  OpenCode solicita aprobación para AGENTS.md y */AGENTS.md.
- Añadir regresiones de límites de escritura, actualización de agentes, skills y
  referencias mediante instaladores, y autorización/rechazo en el probe de OpenCode.

### Actualización y verificación

- Reinstalar agentes y skills mediante el instalador de la plataforma y reiniciar
  el host. Los perfiles locales antiguos pueden prevalecer sobre la instalación
  global y requieren revisión y actualización autorizada por separado.
- Validar instalación (334/334), integridad (416/416), descubrimiento unittest
  (183), permisos (10), contratos documentales (18) y Antigravity en macOS (22).
- Registrar evidencia previa de OpenCode real con proveedor simulado: escritura
  autorizada y rechazada de AGENTS.md y denegación de CLAUDE.md. No certifica
  conducta LLM; Kiro runtime y PowerShell/Windows no se certificaron en esta sesión.

## [3.3.2] - 2026-10-19

### Correcciones

- Integrar explícitamente el mantenimiento del bloque documental de AGENTS.md
  en la planificación, ejecución y cierre del orquestador documental.
- Exigir informar su resultado y conservar la aprobación, el texto exterior
  y las restricciones del host.
- Añadir cobertura de regresión y regenerar las seis distribuciones.

## [3.3.1] - 2026-10-14

### Correcciones

- Aceptar rutas cortas válidas de Windows al importar artefactos, manteniendo el
  rechazo de symlinks, junctions y reparse points.
- Añadir cobertura de regresión para la normalización de rutas de Windows.

## [3.3.0] - 2026-10-14

### Funcionalidades

- Separar los flujos de consulta, implementación y documentación persistente en
  UI/Data.
- Aceptar peticiones en lenguaje natural para el orquestador documental.
- Definir límites de confianza y capacidades por operación para SDD y Code Review.

### Seguridad y correcciones

- Rechazar enlaces y archivos especiales al importar artefactos instalados.
- Fijar las acciones de CI a SHA completos y habilitar revisiones mensuales con
  Dependabot.
- Eliminar expresiones redundantes de las pruebas de integridad.

### Documentación y verificación

- Actualizar documentación, seguimiento de auditorías y distribuciones para seis
  plataformas.
- Añadir pruebas del importador seguro y registrar límites de validación por host.
- Validar localmente render, contratos, integridad, importación, permisos e
  instaladores; la verificación dinámica de LLM y hosts adicionales queda pendiente.

## [3.2.0] - 2026-10-12

### Funcionalidades

- Acotar el preflight de Developer para cambios multicapa y responsive, revisando
  código y pruebas relevantes en una pasada y resolviendo decisiones de aceptación
  antes de editar.
- Enrutar las actualizaciones de documentación canónica mediante un resumen portable
  hacia Documentation Orchestrator, con selección manual del usuario.

### Correcciones

- Evitar la doble inyección del contexto compartido en el agente Developer generado.

### Verificación y distribución

- Añadir pruebas de inyección única y contratos de preflight/documentación en las seis
  plataformas generadas.
- Añadir D11 al smoke manual con registro de baseline/post y costo total reportado;
  la ejecución conversacional en hosts reales permanece pendiente.

## [3.1.0] - 2026-10-12

### Funcionalidades

- Añadir SDD-Tiny con un único `spec.md` y recomendar profundidad según la nota de
  feature: `direct` (1–3), SDD-Tiny (4–8) y SDD-Lite (9–10/10+).
- Mantener Quick Plan en SDD-Lite y conservar las guardas de Direct, las elecciones
  explícitas y los gates SDD existentes.

### Verificación y distribución

- Añadir pruebas de fronteras de score, incluida la codificación 10 +
  `exceeds_x13=true`, y regenerar los artefactos para seis plataformas.
- Documentar el antecedente F10 como evidencia acotada, sin modificar sus artefactos
  históricos ni inferir superioridad universal de Tiny.

## [3.0.0] - 2026-10-12

### Cambios incompatibles

- Convertir `standard` de SDD en modo legacy opt-in; `direct` y `lite` quedan como
  modos operativos predeterminados y `standard` requiere solicitud explícita.

### Documentación y verificación

- Añadir al README un prompt copiable para instalar o actualizar MAS y aclarar que
  se reinicia la herramienta de IA donde se ejecutó el prompt.
- Actualizar contratos y evidencias SDD, incluida la verificación experimental F10
  con fixture; alinear el test con la política vigente para modos retirados.

## [2.0.0] - 2026-10-12

### Cambios incompatibles

- Retirar los agentes `data-api` y `ui-design` como puntos de entrada independientes;
  usar `developer` para implementación y `documentation-orchestrator` para documentación.
- Retirar Scalar y su lanzador del flujo de documentación de APIs; OpenAPI, JSON Schema
  y el catálogo de endpoints permanecen como contratos.

### Funcionalidades y correcciones

- Incorporar el agente `developer` para planificar e implementar cambios de producto
  en UI, datos/APIs y lógica de negocio.
- Permitir evidencia de código del proyecto en consultas `inspect`, manteniendo las
  escrituras restringidas al alcance autorizado.
- Validar archivos anidados y sus hashes en el preflight de origen y en la verificación
  posterior a la instalación.
- Actualizar guías, pruebas y distribuciones generadas para seis plataformas.

### Verificación y límites

- Pasar localmente las suites de contratos, integridad, handoff, instalación y migración;
  validar 11 skills y 5 agentes en 6 plataformas.
- No se ejecutaron smokes conversacionales de hosts ni CI remota en esta preparación.

## [1.3.0] - 2026-10-11

### Funcionalidades

- Gestionar desde Documentation Orchestrator un bloque documental delimitado
  en `AGENTS.md`, preservando el contenido externo y retirando la exportación
  competidora de Project Navigator.
- Añadir fragmentos compartidos para identidad y contexto, propagados a las seis
  plataformas desde las fuentes canónicas.
- Incorporar medición de bytes, caracteres, líneas y palabras para archivos
  explícitamente cargados; no estima tokens reales.

### Flujo de trabajo y documentación

- Ajustar las instrucciones de agentes y skills para reducir duplicación y cargar
  referencias bajo demanda.
- Aplicar aprobación única a correcciones atómicas de bajo riesgo y conservar
  micro-pasos para cambios estructurales o de mayor riesgo.
- Permitir continuar dominios independientes ya autorizados cuando otro dominio
  quede bloqueado; acotar la investigación de releases a fuentes oficiales.

### Auditoría y validación

- Actualizar evidencias de cierre y seguimiento de REC-01/REC-02, con sus límites
  de cobertura documentados.
- Ampliar pruebas y CI para fragmentos compartidos, eficiencia de contexto,
  contratos de agentes y validación de distribuciones.

### Verificación y límites

- Pasar localmente las suites de CI: validación de seis plataformas, secretos,
  contratos, integridad, permisos, enlaces e instalación; `git diff --check` limpio.
- No se ejecutó smoke runtime de LLM; las pruebas estáticas no acreditan obediencia
  universal de los hosts.

## [1.2.0] - 2026-10-11

### Funcionalidades

- Incorporar un control distribuido de secretos de solo lectura para candidatos,
  archivos tracked e índice Git, con exclusión de secretos confirmados y revisión
  contextual de configuración pública y placeholders.
- Integrar el control de secretos y sus pruebas negativas en CI.

### Seguridad y permisos

- Reforzar los permisos de agentes en OpenCode y Kiro, limitar las escrituras y
  delegaciones del orquestador documental y distinguir evidencia de autorización.
- Añadir pruebas de contrato de permisos y herramientas de comprobación en hosts
  para permisos y política de secretos.

### Documentación y mantenimiento

- Añadir auditorías de MAS, consolidación de hallazgos y seguimiento REC-01/REC-02.
- Documentar permisos por host, el procedimiento de revisión de secretos y las
  limitaciones de los controles automatizados.
- Incorporar specs de política de secretos y del caso F10 del laboratorio SDD,
  junto con una presentación HTML de MAS.
- Sincronizar agentes, skills y el control distribuido para las seis plataformas.

### Validación y límites

- Aprobar las 14 suites automatizadas locales, la validación de 10 skills y
  6 agentes en 6 plataformas, los enlaces en 80 archivos Markdown y la sintaxis
  de los scripts Bash de instalación y respaldo.
- El control de firmas no acredita ausencia universal de secretos; las pruebas
  locales no sustituyen la evidencia conversacional en hosts ni los pendientes
  registrados en las fichas de seguimiento.

## [1.0.0] - 2026-10-09

### Funcionalidades

- Definir y presentar el alcance funcional completo antes de calificar features;
  validar explícitamente el alcance y resolver la elección de profundidad antes
  de generar artefactos o implementar.
- Preservar acuerdos, aprobaciones y evidencia al reanudar o modificar specs;
  presentar el conjunto actualizado ante ajustes y distinguir aceptación del
  alcance, modo, ejecutor, autorización de implementación y gates de fase.

### Documentación y mantenimiento

- Publicar la versión 1.0.0 de MAS y sincronizar el contrato SDD en seis plataformas.
- Actualizar guías, ejemplos, arquitectura, navegación y backlog con el catálogo
  vigente y los límites de la evidencia disponible.
- Añadir la spec de validación del alcance completo y pruebas de contrato con
  casos negativos de aprobación, orden de presentación y continuidad.

### Validación y límites

- Aprobar las 13 suites automatizadas locales, incluidas 613 comprobaciones SDD;
  validar 10 skills y 6 agentes en 6 plataformas, enlaces en 69 archivos Markdown,
  render reproducible y sintaxis de 12 scripts Bash.
- Mantener pendientes los smoke tests conversacionales en hosts reales y la
  evidencia nativa Windows de migración/recuperación de agentes retirados.
  La versión 1.0.0 no amplía la certificación runtime documentada.

## [0.7.0] - 2026-10-08

### Funcionalidades

- Refinar la rúbrica de esfuerzo SDD con referentes ReserveLab y escala 10+;
  añadir el comando de preparación del piloto del laboratorio.

### Documentación y mantenimiento

- Compactar y distribuir la guía SDD en seis plataformas; añadir ejemplos, specs
  y evidencias F07/X13 y revisiones de seguridad.
- Reforzar las pruebas de contrato y registrar la reducción de contexto operativo.

### Validación y límites

- Registrar la validación local: 483 comprobaciones SDD, 5 tests de recomendaciones,
  415 de integridad y enlaces en 67 archivos.

## [0.6.0] - 2026-10-07

### Funcionalidades

- Añadir a SDD una calificación de dificultad de feature de 1 a 10, con emoji
  según el rango, tras analizar y definir el alcance.

### Cambios incompatibles

- Retirar las recomendaciones de nivel o selección de LLM de agentes y skills;
  conservar únicamente las decisiones, autorizaciones y gates reales.

### Documentación y mantenimiento

- Actualizar contratos, guías, smoke tests y artefactos generados para seis plataformas.
- Añadir rúbrica y pruebas de exclusividad, formato y distribución de la calificación.

### Validación y límites

- Registrar que las suites automatizadas pasan.
- Dejar explícito que el smoke conversacional en hosts reales sigue pendiente.

## [0.5.0] - 2026-10-07

### Funcionalidades

- Consolidar arquitectura y navegación en `documentation-orchestrator`: modo
  `inspect` de solo lectura, ejecución core local con las skills `architecture`
  y `project-navigator`, y contrato compartido de consumo de `.architecture/`
  y `.navigator/` para el resto de agentes.
- Añadir la recomendación de agente por dominio en SDD con selección manual
  (`references/agent-routing.md`) sin alterar gates ni permisos.
- Incorporar la migración segura de agentes retirados en los instaladores de las
  seis plataformas: opt-in explícito, catálogo de hashes históricos, respaldo
  verificado fuera de árboles escaneados y aprobación por ruta exacta + SHA-256.

### Cambios incompatibles

- Retirar los agentes `architecture` y `project-navigator`; sus skills y carpetas
  se conservan. Las instalaciones previas migran con `--migrate-retired-agents`.

### Correcciones

- Validar destinos de skills y estructura del respaldo antes de copiar durante la
  migración, y generar instrucciones de aprobación con quoting portable.

### Documentación y mantenimiento

- Actualizar catálogo, guías de agentes, instalación y la guía de migración.
- Añadir suites de contratos core y migración a CI, con historial completo para
  la evidencia de artefactos históricos.

### Validación y límites

- Suite completa en verde (integridad 416/416, instalación 196/196, migración
  26/26, SDD 465/465). Pendiente ejecución nativa PowerShell/Windows y smoke
  conversacional LLM; ningún perfil de usuario fue modificado.

## [0.4.0] - 2026-10-06

### Funcionalidades

- Añadir la distribución inicial para Antigravity 2.0 con ocho agentes,
  diez skills y sus recursos.
- Incorporar instalación y exportación en Bash y PowerShell, con dry-run,
  respaldo previo y preservación de archivos propios del usuario.

### Correcciones

- Hacer informativas las recomendaciones de nivel de modelo y continuar
  el trabajo autorizado sin pausas adicionales, conservando los gates
  reales y las confirmaciones operativas.
- Aislar la caché de inicio de PowerShell en los fixtures de pruebas,
  conservando los snapshots completos y la detección de escrituras inesperadas.

### Documentación y mantenimiento

- Sincronizar los artefactos de las cinco plataformas existentes.
- Actualizar guías, contratos, pruebas y documentación del laboratorio SDD.
- Añadir el procedimiento smoke de Antigravity y cobertura CI nativa
  para Linux, macOS y Windows.

### Validación y límites

- Registrar 14 comandos de aceptación locales aprobados en macOS.
- Acreditar instalación/exportación con fixtures en Linux, macOS y Windows:
  22/22 pruebas nativas por OS con Python 3.10, en el
  [run 37510771502](https://github.com/furthurr/ai-agents-kit/actions/runs/37510771502).
- Mantener pendiente la verificación runtime de Antigravity:
  descubrimiento, selección, carga de recursos
  e invocación como subagente.
- Conservar abierto el Gate 4; esta versión no certifica soporte completo
  de Antigravity.
- El bridge `GEMINI.md` → `AGENTS.md` no está implementado.

## [0.3.0] - 2026-10-05

### Funcionalidades

- Consolidar calidad y seguridad bajo el agente `code-review`.
- Simplificar los modos SDD y el testing adaptativo.
- Documentar el laboratorio de evaluación SDD y añadir una simulación sintética
  offline sin llamadas a modelos.

### Correcciones

- Aislar el contrato SDD de dependencias locales y conservar su compatibilidad
  con el agente unificado.

### Otros

- Unificar la autoría y la licencia MIT.

## [0.2.1] - 2026-09-30

### Funcionalidades

- Añadir soporte de Pi con 10 skills nativas y 9 agentes invocables como prompt templates.

### Compatibilidad

- Añadir generación, validación, instalación y backup de los artefactos Pi en Bash y PowerShell.

## [0.2.0] - 2026-09-24

### Funcionalidades

- Pausar tras recomendar un nivel de modelo en SDD y en las tareas puntuales de los agentes especialistas, para permitir un cambio manual opcional.
- Reanudar sin declarar el modelo elegido, conservando los gates de cada agente y evitando avisos duplicados tras un handoff.

### Compatibilidad

- Propagar las instrucciones a Copilot, OpenCode, Kiro y Claude Code.

### Validación

- Ampliar las pruebas contractuales de SDD y de recomendaciones multiagente.
- Documentar el smoke conversacional, pendiente de ejecución en los hosts.

## [0.1.2] - 2026-09-23

### Correcciones

- Crear el lanzador Scalar aunque falte el contrato OpenAPI.

### Documentación

- Añadir una imagen de presentación de MAS al README.
- Hacer informativas las recomendaciones de nivel de LLM en SDD: solo los gates
  reales bloquean las transiciones entre fases.
- Propagar el contrato SDD actualizado a las guías y las cuatro plataformas
  generadas.

### Validación

- Actualizar las pruebas de contrato y smoke tests SDD para cubrir transiciones sin
  confirmación del nivel de LLM.

## [0.1.1] - 2026-09-15

### Funcionalidades

- Incorporar la profundidad SDD `lite` con Quick Plan exclusivo, selección
  conservadora y verificación proporcional.
- Añadir recomendaciones de capacidad para la próxima fase SDD, manteniendo los
  gates y las confirmaciones explícitas entre fases.
- Permitir especificaciones SDD agrupadas por módulo y reanudarlas con rutas
  seguras.

### Compatibilidad

- Propagar los contratos SDD actualizados a Copilot, OpenCode, Kiro y Claude
  Code mediante los artefactos generados.

### Validación

- Ampliar los contratos, smoke tests y specs de SDD para cubrir los nuevos modos,
  recomendaciones, trazabilidad y evidencia.

## [0.1.0] - 2026-09-15

### Funcionalidades

- Consolidar la coordinación SDD, Navigator, handoffs y testing adaptativo.
- Añadir recomendaciones de nivel de modelo con gates proporcionales y sin
  dependencia de proveedores.
- Extender el catálogo Data & API con documentación interactiva opcional.
- Mantener artefactos instalables para Copilot, OpenCode, Kiro y Claude Code.

### Documentación

- Definir la identidad transversal `MAS` y la convención de mensajes del sistema.
- Actualizar las guías de uso, instalación, arquitectura y agentes.
- Registrar smoke tests, criterios de release y evidencia de validación.

### Validación

- Reforzar los contratos de integridad, SDD, handoff, render e instalación.
- Validar paridad de fuentes canónicas y artefactos generados en cuatro plataformas.
