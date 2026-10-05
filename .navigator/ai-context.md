# AI Agents Kit

## Propósito
- Qué es: repositorio fuente de skills y agentes del MAS para GitHub Copilot, OpenCode, Kiro, Claude Code y Pi.
- Alcance: define contenido compartido en `canonical/`, diferencias en `adapters/`, artefactos en `generated/` y herramientas/scripts de render e instalación.
- Fuera de alcance: no es una aplicación runtime; `generated/` es salida del pipeline, no se edita a mano.

## Stack
- Lenguajes y formatos: Python 3, Bash, PowerShell, Markdown y JSON.
- Build: no se detectó manifiesto de build/gestor de paquetes; el flujo documentado usa `python3 tools/render.py` y `python3 tools/validate.py`.
- Entrypoints: `tools/render.py`, `tools/validate.py`, `scripts/install/`.

## Mapa rápido
- `canonical/` → fuente de verdad de skills, agentes y manifiesto.
- `adapters/` → configuración por plataforma (copilot, opencode, kiro, claude, pi).
- `tools/` → render, validación, métricas e importación; ver `module-map.json`.
- `generated/` → salidas renderizadas por plataforma.
- `scripts/` → instalación y backup/importación.
- `docs/` → guías de uso, desarrollo y arquitectura del pipeline.

## Convenciones
- Flujo principal: `canonical/` + `adapters/` → `tools/render.py` → `generated/` → `scripts/install/`.
- Consultar `docs/arquitectura-del-kit.md` antes de navegar el pipeline; detalle y dependencias en `module-map.json`.

## Docs y contexto externo
- `README.md`, `docs/README.md` y `docs/arquitectura-del-kit.md` — presentes.
- `.architecture/` — presente; índice en `README.md` (C4, flujos, despliegue,
  ADRs y deuda); overview en `01-overview.md`.
- `.quality/` — presente; índice en `README.md`; tablero `quality-tech-debt.md`,
  métricas, `findings/` y estándares en caché.
- `.security/` — presente; índice en `README.md`; tablero `security-tech-debt.md`,
  `findings/`, `pii-secrets.md`, `dependencies.md` y estándares en caché.
- `.data/` y `.design/` — no presentes; `.sdd/steering/` no presente (`.sdd/`
  contiene `specs/`).
- `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.cursor/rules/` — no detectados.

## Riesgos y restricciones
- No indexar secretos ni archivos de credenciales; patrones excluidos en `config.yaml`.
- El working tree sigue modificado; se omite `source_commit` y no se declara `HEAD` como baseline.

## Meta
- Actualizado: 2026-10-05
- Navigator root: `.`
- Generado por: project-navigator sync (solo Context)
- Presupuesto aproximado: ~650 tokens.
