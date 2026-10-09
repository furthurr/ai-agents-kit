# 1. Visión general

## 1.1 Propósito y objetivos

AI Agents Kit mantiene skills y agentes de un sistema multiagente en una fuente
versionada común y los adapta a seis herramientas de asistencia de código. El
objetivo arquitectónico es compartir comportamiento entre plataformas evitando
duplicar prompts, a la vez que se representa cada formato host mediante
adaptadores (`../README.md:5-15`; `../canonical/manifest.json:1-31`).

Objetivos observables:

- Mantener inventario explícito de skills, agentes y plataformas.
- Renderizar artefactos por plataforma desde fuentes comunes y configuración
  declarativa.
- Detectar incoherencias de manifest/adapters y deriva entre fuentes y salidas.
- Instalar o importar artefactos sin sobrescribir silenciosamente contenido
  desconocido del usuario.

La arquitectura de las fuentes y el pipeline se describe también en
`../docs/arquitectura-del-kit.md:7-43`.

## 1.2 Alcance

**Dentro del sistema:** catálogo canónico, prompts y referencias, adapters por
plataforma, renderer, validador, artefactos generados, utilidades de soporte y
scripts de instalación/backup. El recorrido oficial es
`canonical/` → `adapters/` → `generated/` → `scripts/install/`
(`../docs/desarrollo.md:6-17`).

**Fuera del sistema:** los clientes Copilot, OpenCode, Kiro, Claude Code, Pi y Antigravity,
sus runtimes, permisos de sesión y configuración local del usuario. El kit
produce y copia archivos para esos hosts; no ejecuta sus funciones como un
servicio propio (`../docs/instalacion.md:3-12`).

## 1.3 Stakeholders

| Stakeholder | Interés arquitectónico |
|---|---|
| Mantenedor/contribuidor | Editar fuentes, adapters y herramientas; regenerar y validar el resultado. |
| Usuario del kit | Instalar una o varias plataformas, conservar personalizaciones y poder revisar/restaurar backups. |
| Herramientas host | Consumir los formatos, ubicaciones y convenciones que cada adapter declara. |

## 1.4 Restricciones y convenciones

- Python 3 para render, validación e importación; Bash o PowerShell para los
  wrappers de instalación/backup (`../docs/instalacion.md:7-12`).
- `canonical/manifest.json` es la fuente de inventario; una nueva skill/agente o
  plataforma debe declararse y satisfacer los adapters requeridos
  (`../docs/desarrollo.md:39-56, 58-87`).
- `generated/` se regenera; no se edita a mano (`../docs/instalacion.md:3-5`).
- La documentación del kit establece español por defecto para prompts y
documentos (`../docs/desarrollo.md:129-136`).
- Las rutas de instalación son globales al usuario y los instaladores ofrecen
  dry-run y backup (véase [distribución](06-deployment.md)).

## 1.5 Supuestos y aspectos no demostrados

- El manifiesto enumera seis plataformas, pero esta documentación no implica
  que todos los clientes host estén instalados o disponibles en cada entorno.
- La validación local no equivale a una prueba de compatibilidad ejecutada dentro
  de cada cliente host.
- No se identifica una aplicación de negocio, base de datos ni servicio remoto
  propio en el flujo documentado; el producto aquí es el repositorio/pipeline.
- La fecha de revisión describe las fuentes observadas con cambios locales y no
  establece un baseline Git limpio.
