# ADR 0001: Mantener contenido canónico y adaptadores por plataforma

- Estado: Aceptada (vigencia inferida del diseño actual; registro retrospectivo).
- Fecha de registro: 2026-10-05. No consta aquí la fecha original de decisión.

## Contexto

El kit distribuye el mismo catálogo funcional a seis plataformas que usan
formatos, nombres de archivo, frontmatter y ubicaciones diferentes. La
documentación del proyecto describe una fuente común y adapters para evitar
duplicar prompts (`../README.md:13-15`; `../docs/arquitectura-del-kit.md:7-32`).

## Decisión observada

Mantener skills y agentes compartidos en `canonical/`; declarar las diferencias
por plataforma en `adapters/`; generar los árboles de salida en `generated/` con
el pipeline. Tratar `generated/` como salida regenerable y no como fuente de
edición (`../docs/desarrollo.md:6-17`; `../docs/arquitectura-del-kit.md:34-43`).

Este ADR registra la decisión que refleja el diseño vigente; no afirma
reconstruir el debate ni la autoría histórica.

## Alternativas consideradas

- **Mantener una copia completa de cada skill/agente para cada plataforma.**
  Evitada por el principio documentado de evitar prompts duplicados y conservar
  una fuente común (`../README.md:13-15`).
- **Editar las salidas generadas directamente.** Rechazada por la convención
  documentada de regenerarlas desde canonical y adapters
  (`../docs/instalacion.md:3-5`).

## Consecuencias

- **Positivas:** comportamiento compartido; diferencias localizadas; renderer
  determinista; posibilidad de comprobar inventario y reproducibilidad.
- **Negativas / trade-offs:** añadir una plataforma requiere adapters completos y
  wrappers; cambios de esquema o sustitución pueden afectar varias salidas; una
  generación fallida puede dejar salidas parciales mientras no haya publicación
  transaccional (seguimiento `ARQ-001` en
  [`../arch-tech-debt.md`](../arch-tech-debt.md)).
