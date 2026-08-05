---
name: project-navigator
description: >-
  Navega cualquier proyecto con minimo de tokens mediante capas en `.navigator/`
  (contexto, mapa de modulos, simbolos, grafo y codigo puntual). Hace bootstrap
  y update de indices bajo peticion. No modifica codigo de negocio. Avisa al
  usuario para cambiar el modelo manualmente antes/despues de procesos pesados;
  nunca selecciona el modelo por el usuario.
---

# Skill: Project Navigator

Referencia canónica de **cómo navegar e indexar** un repositorio con mínimo de
tokens. Complementa al agente `project-navigator`. Si agente y skill divergen,
**manda esta skill**.

Objetivo: responder con la capa más barata suficiente y citar fuentes.

> **Alcance inviolable:** por defecto **solo lectura** del repo y de
> `.navigator/`. Escritura **solo** en `.navigator/` (bootstrap/update). Export
> opt-in a `AGENTS.md` **con confirmación**. NO modifica código de negocio, UI,
> tests de producto, CI ni Git remoto. NO selecciona ni fuerza el modelo del host.
> Si piden implementar features o refactors: **declarar límite**, aportar
> ubicación/mapa si ayuda, y detenerse.

## Cuándo usar

- Onboarding: qué es el proyecto, cómo está organizado
- Localizar módulos, símbolos, dependencias e impacto
- Antes de una feature/refactor cuando haga falta mapa sin reexplorar el repo
- Primera vez sin `.navigator/` → bootstrap
- Actualizar índices cuando el usuario lo pida o haya desfase claro

## Flujo obligatorio al recibir una petición

1. **Clasificar** (consulta vs bootstrap/update vs fuera de alcance).
2. Si es bootstrap, update pesado o navegación reiterada de varias capas:
   **aviso de modelo** antes (`references/bootstrap.md`); esperar confirmación
   o "sigo con el actual".
3. Comprobar `.navigator/` y capas habilitadas en `config.yaml`.
4. Si no hay navigator y la consulta lo necesita → **ofrecer bootstrap**; si el
   usuario no quiere → modo degradado (`references/config.md`).
5. Elegir la **capa mínima** (tabla abajo); subir de capa solo si no basta.
6. Responder de forma concisa citando **fuente** (path de capa o `archivo:linea`).
7. Si hubo degradado: declarar `capas_ausentes` y límite de confianza.
8. Si el proceso fue pesado: **aviso de modelo** final.

### Clasificador pregunta → capa

| Tipo de pregunta | Capa inicial | Subir a si no basta |
| --- | --- | --- |
| Qué es / propósito / organización | 0 `ai-context.md` | 1 |
| En qué módulo / dependencias entre módulos | 1 `module-map.json` | 2 o 4 |
| Dónde se define un símbolo / firma | 2 `symbols.json` (si existe) | 4 |
| Relación X–Y / impacto de cambiar Z | 3 grafo (si existe y on) | 1 + 4 |
| Detalle de implementación | 4 código puntual (rango) | — |
| Bootstrap / indexar / actualizar | Escritura en `.navigator/` | — |

Detalle de capas, schemas y presupuestos: `references/layers.md`.

### Reglas de consulta

- Preferir archivo + rango de líneas sobre leer directorios enteros
- No volcar grafo ni `symbols.json` / `module-map.json` completos al contexto
- No inventar entradas de índices; si faltan, degradar o proponer update
- Máx. 2–3 capas distintas y 1–3 archivos de código por pregunta
- Nunca “leer el repo entero” para compensar

## Bootstrap y update

Contrato de pasos, monorepo, avisos de modelo y export `AGENTS.md`:
`references/bootstrap.md`.

Resumen bootstrap:

1. Aviso de modelo → detectar stack y fuentes externas
2. Ubicación `.navigator/` (preguntar si ambiguo)
3. `config.yaml` + `ai-context.md` (~500 tokens) + `module-map.json`
4. No bloquear si faltan symbols/grafo
5. Respetar exclude/secretos → informar artefactos, gaps, cómo consultar
6. Aviso final de modelo

Plantillas: `references/templates/`.

Update: solo on_request; capas afectadas; no regenerar todo por defecto;
preguntar si `ai-context.md` tiene edición manual evidente.

## Artefactos en `.navigator/`

| Artefacto | Tras bootstrap | Notas |
| --- | --- | --- |
| `config.yaml` | Obligatorio | Contrato en `references/config.md` |
| `ai-context.md` | Obligatorio | Capa 0; ~500 tokens |
| `module-map.json` | Obligatorio | Capa 1 |
| `symbols.json` | Opt-in | Capa 2 best-effort |
| `graph/` | Opt-in | Capa 3; provider default `none` |
| `cache/` | No versionar | gitignore |

## Fuentes externas (híbrido Capa 0)

Detectar best-effort: `AGENTS.md`, `CLAUDE.md`, README, "Contexto para IA" en
`.architecture/`, `.data/`, `.quality/`, `.security/`, `.design/`, etc.
Referenciar; no sobrescribir. Detalle: `references/sources.md`.

## Formato de respuesta

- Conciso, orientado a la pregunta
- Indicar **fuentes** (p. ej. `.navigator/ai-context.md`, `src/foo.ts:42`)
- En degradado: `capas_ausentes` + confianza limitada
- No rellenar con especulación presentada como hecho indexado

## Presupuesto de tokens (MVP, tope blando)

| Artefacto / acción | Objetivo | Si se pasa |
| --- | --- | --- |
| `ai-context.md` | ~500 (tope ~700) | Recortar convenciones y riesgos |
| `module-map.json` | ~1–2k (tope ~4k) | Menos módulos o responsibilities más cortas |
| Respuesta típica | ~200–600 (tope ~1k) | Solo lo pedido + fuentes |
| Hits symbols | top 5–15 (máx. 25) | Filtrar; no dump |
| Capa 4 código | ~80–150 líneas (tope ~250) | Pedir rango más preciso |
| Bootstrap sesión | < ~30–50k in+out | Acotar `project.root` |

~4 chars ≈ 1 token. Detalle: `references/layers.md`.

## Relación con otras skills

No sustituye a architecture, security, quality, data-api ni ui-design: solo
navega e indexa. Puede señalar el especialista adecuado para documentar o remediar.

## Fuera de alcance

Si piden implementar features, refactors de producto o cambios de CI/Git remoto:
declarar límite, aportar mapa/ubicación si ayuda, y detenerse (no implementar).
