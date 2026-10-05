# Glosario

| Término | Definición en este repositorio |
|---|---|
| MAS | *Multi-Agent System*: el sistema multiagente formado por skills, agentes, coordinación y artefactos del kit; no un modelo/proveedor ni una referencia a estándares OWASP de seguridad. |
| Skill | Procedimiento canónico reutilizable, normalmente con `SKILL.md` y referencias. |
| Agente | Rol/prompt canónico que una plataforma convierte a su formato y punto de invocación. |
| Canonical | Fuentes compartidas de skills, agentes y manifiesto bajo `canonical/`. |
| Adapter | Configuración JSON que representa diferencias de formato, filename, frontmatter y sustituciones de una plataforma. |
| Manifest | `canonical/manifest.json`, inventario de IDs de skills, agentes y plataformas. |
| Renderer | `tools/render.py`, transforma contenido canónico y adapters en árboles bajo `generated/`. |
| Generated | Artefactos de salida por plataforma; derivables y no editables a mano. |
| Preflight | Comprobación compartida que verifica completitud del origen o instalación contra el manifest. |
| Host / plataforma | Cliente externo que consume skills/agentes instalados: Copilot, OpenCode, Kiro, Claude Code o Pi. |
| Backup | Copia timestamped del contenido de destino antes de instalar, salvo cuando se usa `--force`. |
| Import | Copia filtrada de contenido instalado a `imports/<plataforma>/<fecha>/` para revisión y promoción manual. |
| Working tree | Estado local del repositorio, que durante esta revisión tenía cambios no atribuidos a un baseline `HEAD`. |

Fuentes del vocabulario: `../README.md:5-15`,
`../docs/arquitectura-del-kit.md:7-43` y
`../docs/instalacion.md:112-189`.
