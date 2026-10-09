# Changelog

Historial de cambios de MAS (Multi-Agent System). Las versiones siguen SemVer y
los tags usan el formato `vX.Y.Z`.

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
