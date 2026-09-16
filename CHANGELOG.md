# Changelog

Historial de cambios de MAS (Multi-Agent System). Las versiones siguen SemVer y
los tags usan el formato `vX.Y.Z`.

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
