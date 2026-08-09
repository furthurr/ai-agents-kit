# AI Agents Kit

Fuente versionada de **skills** y **agentes** para [GitHub Copilot](https://github.com/features/copilot),
[OpenCode](https://opencode.ai) y [Kiro](https://kiro.dev).

La lógica se mantiene **una sola vez** en `canonical/` y se renderiza por
plataforma con adaptadores declarativos. Así obtienes el mismo comportamiento
especializado en las tres herramientas, sin triplicar prompts.

## Por qué existe

Un agente genérico reexplora el repo, mezcla dominios y pierde contexto entre
sesiones. Este kit aporta:

- **Especialistas con alcance fijo** (navegación, arquitectura, calidad, datos, seguridad, UI, SDD, git/release).
- **Procedimientos canónicos** (skills) reutilizables y versionados.
- **Carpetas de contexto en tu proyecto** (`.navigator/`, `.architecture/`, `.quality/`, `.data/`, …) que la IA y el equipo comparten.

Más detalle: [docs/vision.md](docs/vision.md).

## Qué incluye

| | Cantidad | Detalle |
|---|----------|---------|
| Skills | 9 | architecture, code-quality, data-api, git-commit, project-navigator, release-management, sdd-spec, security, ui-design |
| Agentes | 8 | uno por dominio; **Git & Release Manager** orquesta commit + release; **Project Navigator** navega con `.navigator/` |
| Plataformas | 3 | copilot, opencode, kiro |

Catálogo completo (roles, carpetas, cuándo usar cada uno):
[docs/catalogo.md](docs/catalogo.md).

## Inicio rápido

Requisitos: **Python 3** y Bash o PowerShell.

```bash
# 1. Generar y validar artefactos
python3 tools/render.py
python3 tools/validate.py

# 2. Instalar la plataforma que uses
./scripts/install/copilot.sh      # → ~/.copilot/
./scripts/install/opencode.sh     # → ~/.config/opencode/
./scripts/install/kiro.sh         # → ~/.kiro/

# 3. Reinicia Copilot, OpenCode o Kiro
```

Windows (PowerShell):

```powershell
python tools/render.py
python tools/validate.py
.\scripts\install\copilot.ps1
.\scripts\install\opencode.ps1
.\scripts\install\kiro.ps1
```

Opciones: `--dry-run` / `-DryRun`, `--force` / `-Force`.
Importación segura de instalaciones locales: `scripts/backup/`.

Guía completa: [docs/instalacion.md](docs/instalacion.md) ·  
Uso diario: [docs/uso.md](docs/uso.md).

## Modelo del repositorio

```text
canonical/     ← edita aquí la lógica común (skills + agentes)
adapters/      ← solo diferencias por herramienta (frontmatter, permisos, tokens)
generated/     ← salida del render (NO editar a mano)
tools/         ← render.py, validate.py, measure_context.py, …
scripts/       ← install/ y backup/ (bash + PowerShell)
docs/          ← documentación ampliada
```

```text
canonical + adapters  →  render  →  generated  →  install  →  tu herramienta
```

## Documentación

| Documento | Contenido |
|-----------|-----------|
| [docs/README.md](docs/README.md) | Índice |
| [docs/vision.md](docs/vision.md) | Problema, principios, skill vs agente |
| [docs/catalogo.md](docs/catalogo.md) | Skills, agentes y carpetas canónicas |
| [docs/instalacion.md](docs/instalacion.md) | Install, destinos, backup/import |
| [docs/uso.md](docs/uso.md) | Cómo invocar y flujos recomendados |
| [docs/navigator-smoke.md](docs/navigator-smoke.md) | Smoke test reproducible del Project Navigator |
| [docs/desarrollo.md](docs/desarrollo.md) | Contribuir y extender el kit |
| [docs/arquitectura-del-kit.md](docs/arquitectura-del-kit.md) | Pipeline técnico |

## Contribuir (resumen)

1. Edita `canonical/` y/o `adapters/`.
2. Ejecuta `python3 tools/render.py` y `python3 tools/validate.py`.
3. Revisa `generated/` e instala en dry-run antes de probar en serio.

Nunca commits de secretos. Detalle: [docs/desarrollo.md](docs/desarrollo.md).

## Autor

Pedro G. V. [@furthurr](https://github.com/furthurr)

- GitHub: https://github.com/furthurr
- Email: pedrogvas@gmail.com

## Licencia

[Apache-2.0](LICENSE)
