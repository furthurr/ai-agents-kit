# Changelog

Historial de cambios de MAS (Multi-Agent System). Las versiones siguen SemVer y
los tags usan el formato `vX.Y.Z`.

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
