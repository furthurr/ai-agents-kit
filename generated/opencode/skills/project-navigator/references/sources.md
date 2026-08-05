# Fuentes externas de contexto (híbrido Capa 0)

El artefacto canónico de Capa 0 es **siempre** `.navigator/ai-context.md`.
Las fuentes externas se detectan y referencian; **no se sobrescriben**.

## Fuentes a detectar

| Fuente | Rol típico |
| --- | --- |
| `AGENTS.md` (raíz) | Convención emergente multi-herramienta |
| `CLAUDE.md` | Contexto/reglas de Claude Code |
| `.cursorrules`, `.cursor/rules/` | Reglas de Cursor |
| `README.md` (raíz) | Propósito y onboarding humano |
| `.architecture/` — sección "Contexto para IA" | Arquitectura del kit |
| `.data/` — "Contexto para IA" | Datos y APIs |
| `.quality/` — "Contexto para IA" | Calidad de código |
| `.security/` — "Contexto para IA" | Seguridad |
| `.design/` — "Contexto para IA" | UI / design system |
| `.sdd/steering/` | Steering SDD si existe |
| Manifests de build | `package.json`, `settings.gradle`, `pubspec.yaml`, `Cargo.toml`, `go.mod`, `pyproject.toml`, etc. |

## Reglas de uso

1. En bootstrap y al responder: detectar best-effort si `sources.detect_external: true`
2. Incorporar o referenciar cuando aporte valor; **no pegar** contenidos largos en `ai-context.md`
3. En `ai-context.md` § Docs: listar path + nota breve (`presente` / `ausente` / una frase)
4. Preferir secciones "Contexto para IA" de carpetas canónicas sobre copiar READMEs enteros
5. Si solo existen fuentes externas y no hay `.navigator/`: modo degradado Capa 0 provisional e invitar a bootstrap
6. Export a `AGENTS.md`: solo opt-in con confirmación del usuario; no es la fuente de verdad del navigator

## Relación con otras skills del kit

- `project-navigator` **no sustituye** a architecture, security, quality, data-api ni ui-design
- Solo navega e indexa para reducir tokens
- Puede **señalar** que otra skill/agente es más adecuada para documentar o remediar
- En bootstrap Capa 0: leer best-effort "Contexto para IA" de carpetas canónicas si existen

## Stack — detección agnóstica

El MVP no limita lenguajes. Indicadores orientativos:

| Tecnología | Indicadores posibles |
| --- | --- |
| Node.js / JS/TS | `package.json`, lockfiles, workspaces |
| Python | `pyproject.toml`, `requirements.txt` |
| Java/Kotlin | `build.gradle`, `settings.gradle`, `pom.xml` |
| Flutter/Dart | `pubspec.yaml` |
| Rust | `Cargo.toml` |
| Go | `go.mod` |
| Swift/iOS | `Package.swift`, `.xcodeproj`, `.xcworkspace` |

La calidad del mapa depende de la estructura del repo, no de una lista blanca.
