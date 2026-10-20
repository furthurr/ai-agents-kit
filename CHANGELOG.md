# Changelog

Historial de cambios de MAS (Multi-Agent System). Las versiones siguen SemVer y
los tags usan el formato `vX.Y.Z`.

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
