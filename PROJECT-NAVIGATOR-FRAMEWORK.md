# Project Navigator Framework

> **Documento retirado como especificación operativa.** Esta redirección se
> mantiene temporalmente para no romper enlaces existentes.

Project Navigator está implementado como MVP dentro de AI Agents Kit. Su antiguo
documento de diseño mezclaba contratos runtime, plantillas, decisiones históricas
y trabajo futuro. Ese contenido se distribuyó entre las fuentes responsables para
evitar dos autoridades divergentes.

## Fuentes vigentes

| Necesidad | Fuente |
| --- | --- |
| Comportamiento runtime | [`canonical/skills/project-navigator/SKILL.md`](canonical/skills/project-navigator/SKILL.md) |
| Capas y presupuestos | [`references/layers.md`](canonical/skills/project-navigator/references/layers.md) |
| Schemas normativos | [`references/schemas.md`](canonical/skills/project-navigator/references/schemas.md) |
| Bootstrap y update | [`references/bootstrap.md`](canonical/skills/project-navigator/references/bootstrap.md) |
| Configuración y seguridad | [`references/config.md`](canonical/skills/project-navigator/references/config.md) |
| Uso diario | [`docs/uso.md`](docs/uso.md) |
| Catálogo | [`docs/catalogo.md`](docs/catalogo.md) |
| Arquitectura y decisiones | [`docs/arquitectura-del-kit.md`](docs/arquitectura-del-kit.md) |
| Validación manual | [`docs/navigator-smoke.md`](docs/navigator-smoke.md) |
| Roadmap y deuda | [`docs/mejoras.md`](docs/mejoras.md) |

## Autoridad

La skill canónica y sus referencias son la única fuente de verdad del
comportamiento de Project Navigator. Las plantillas son ejemplos y los artefactos
bajo `generated/` son salidas del renderer; ninguno reemplaza la fuente canónica.

## Historial

El diseño monolítico anterior permanece disponible en el historial de Git. Esta
redirección puede eliminarse después de una release de transición, cuando no
queden enlaces internos ni consumidores conocidos de sus secciones históricas.
