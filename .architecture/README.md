# Arquitectura — AI Agents Kit

Documentación canónica de la arquitectura del repositorio. Léela antes de
cambiar sus fuentes, adaptadores, renderer o distribución.

## Estado de sincronización

- Tecnología detectada: Markdown, JSON, Python 3, Bash y PowerShell.
- Modo: `full`.
- Último commit documentado: **omitido**. No se declara `HEAD` como baseline:
  esta revisión se realizó con modificaciones locales presentes.
- Última actualización: 2026-10-09.
- Marca: revisión documental por fecha; no representa un snapshot Git limpio.

## Contexto para IA

- **Qué es el sistema:** repositorio fuente y pipeline para producir e instalar
  skills y agentes del MAS en GitHub Copilot, OpenCode, Kiro, Claude Code, Pi y
  Antigravity (integración inicial 2.0; runtime pendiente).
  No es una aplicación de usuario ni un servicio runtime propio.
- **Estilo arquitectónico:** contenido canónico compartido + adaptadores
  declarativos por plataforma + render determinista a artefactos consumibles.
- **Módulos y límites:** `canonical/` conserva inventario y contenido común;
  `adapters/` expresa diferencias de host; `tools/` renderiza, valida y apoya
  mantenimiento/importación; `generated/` es salida regenerable; `scripts/`
  instala o importa artefactos; `docs/` describe el uso y el pipeline. `.navigator/`
  y `.architecture/` aportan contexto documental para IA/equipo, no artefactos
  del runtime del kit.
- **Regla de dependencia:** `canonical/manifest.json` gobierna el catálogo.
  Renderer/validador consumen `canonical/` y `adapters/`; los instaladores
  consumen `generated/` y verifican el inventario con las herramientas Python.
  No editar `generated/` manualmente ni invertir dependencias hacia el contenido
  canónico desde un host.
- **Decisión clave:** separación de fuentes comunes y adaptación de plataforma;
  registrada en [ADR 0001](decisions/0001-fuente-canonica-y-adaptadores.md).
- **Fuentes de contexto:** `../README.md:5-15`,
  `../docs/arquitectura-del-kit.md:7-43` y
  `../canonical/manifest.json:1-31`.

Las carpetas raíz `copilot/` y `opencode/` son snapshots legados cuando están
presentes; no forman parte del pipeline canónico (`../docs/desarrollo.md:15-17`).

## Índice

1. [Objetivos, alcance y restricciones](01-overview.md)
2. [Contexto del sistema — C4 nivel 1](02-context.md)
3. [Contenedores — C4 nivel 2](03-containers.md)
4. [Componentes clave — C4 nivel 3](04-components.md)
5. [Flujos y secuencias](05-runtime.md)
6. [Distribución e instalación](06-deployment.md)
7. [Conceptos transversales](07-crosscutting.md)
8. [Atributos de calidad y riesgos](08-quality-risks.md)
9. [Glosario](glossary.md)
10. [Decisiones](decisions/0001-fuente-canonica-y-adaptadores.md)
11. [Deuda técnica de arquitectura](arch-tech-debt.md)

## Alcance de esta revisión

La sincronización del 2026-10-09 incorpora seis distribuciones, el contrato SDD de
alcance completo/continuidad y la evidencia CI documentada para Antigravity.
Fuentes: `../canonical/manifest.json:1-30`,
`../canonical/skills/sdd-spec/references/scope-depth.md:16-59`,
`../canonical/skills/sdd-spec/references/spec-continuity.md:22-77` y
`../.github/workflows/ci.yml:10-73`.
El working tree tiene cambios locales; esta revisión queda pendiente de baseline
Git verificable. La revisión documenta arquitectura, no certifica una
auditoría de seguridad, la compatibilidad efectiva de cada host ni la ejecución
de las pruebas del proyecto.
