# AI Agents Kit

## Propósito
- Qué es: kit con 11 skills, 5 agentes y 6 plataformas MAS para Copilot, OpenCode, Kiro, Claude Code, Pi y Antigravity 2.0 (runtime pendiente).
- Alcance: define contenido compartido en `canonical/`, diferencias en `adapters/`, artefactos en `generated/` y herramientas/scripts de render e instalación.
- Fuera de alcance: no es una aplicación runtime; `generated/` es salida del pipeline, no se edita a mano.

## Stack
- Lenguajes y formatos: Python 3, Bash, PowerShell, Markdown y JSON.
- Build: no se detectó manifiesto de build/gestor de paquetes; el flujo documentado usa `python3 tools/render.py` y `python3 tools/validate.py`.
- Entrypoints: `tools/render.py`, `tools/validate.py`, `scripts/install/`.

## Mapa rápido
- `canonical/` → fuente de verdad de skills, agentes y manifiesto.
- `adapters/` → configuración por plataforma; inventario en `canonical/manifest.json`.
- `tools/` → render, validación, métricas e importación; ver `module-map.json`.
- `generated/` → salidas renderizadas por plataforma.
- `scripts/` → instalación y backup/importación.
- `docs/` → guías de uso, desarrollo y arquitectura del pipeline.

## Convenciones
- Flujo principal: `canonical/` + `adapters/` → `tools/render.py` → `generated/` → `scripts/install/`.
- Consultar `docs/arquitectura-del-kit.md` antes de navegar el pipeline; detalle y dependencias en `module-map.json`.
- SDD: alcance completo validado antes de artefactos/código; `direct` sin spec, `tiny` con `spec.md` único y Gates 3/4, `lite` con Quick Plan sin Gates 1–4 y `standard` legacy solo por solicitud explícita con Gates 1–4. Continuidad en `canonical/skills/sdd-spec/references/spec-continuity.md`.

## Docs y contexto externo
- `README.md`, `docs/README.md` y `docs/arquitectura-del-kit.md` — presentes.
- `.architecture/` — presente; índice en `README.md` (C4, flujos, despliegue,
  ADRs y deuda); overview en `01-overview.md`.
- `.quality/` — auditoría tools/scripts del 2026-10-05; índice y tablero `quality-tech-debt.md`.
- `.security/` — revisión puntual F07 del laboratorio del 2026-10-07; no certifica el kit completo.
- `.data/` y `.design/` — no presentes; `.sdd/steering/` no presente (`.sdd/`
  contiene `specs/`).
- `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.cursor/rules/` — no detectados.

## Riesgos y restricciones
- No indexar secretos ni archivos de credenciales; patrones excluidos en `config.yaml`.
- Contexto de inventario y SDD contrastado con las fuentes de `HEAD` `10373b3e9510cc71049eb37c5393b4e18415e40d`; los cambios locales actuales son de seguimiento documental.
- `.agent-lab/` es experimental y local; no pertenece al render ni a la distribución.

## Meta
- Actualizado: 2026-10-13
- Source commit: `10373b3e9510cc71049eb37c5393b4e18415e40d`
- Navigator root: `.`
- Generado por: revisión focalizada de frescura FUT-14 (Capa 0; el mapa de módulos no requirió cambios)
