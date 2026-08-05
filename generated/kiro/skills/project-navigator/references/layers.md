# Capas de navegación

Divulgación progresiva: empezar por la capa más barata y subir solo si no basta.
Nunca volcar índices completos al contexto del modelo.

## Clasificador pregunta → capa

| Tipo de pregunta | Capa inicial | Subir a si no basta |
| --- | --- | --- |
| Qué es / propósito / cómo está organizado | 0 `ai-context.md` | 1 |
| En qué módulo está / dependencias entre módulos | 1 `module-map.json` | 2 o 4 |
| Dónde se define un símbolo / firma / métodos | 2 `symbols.json` (si existe) | 4 |
| Cómo se relaciona X con Y / impacto de cambiar Z | 3 grafo (si existe y `graph` on) | 1 + 4 |
| Detalle de implementación | 4 código puntual (rango de líneas) | — |
| Bootstrap / indexar / actualizar navigator | Modo escritura en `.navigator/` | — |

## Capa 0 — Contexto raíz

- Path: `.navigator/ai-context.md`
- Objetivo: ~500 tokens; tope blando ~700
- Plantilla: `templates/ai-context.template.md`
- Enfoque híbrido: artefacto canónico interno + fuentes externas solo lectura/merge (ver `sources.md`)

## Capa 1 — Mapa estructural

- Path: `.navigator/module-map.json`
- Schema version MVP = `1`
- Campos obligatorios raíz: `version`, `generated_at`, `root`, `modules`
- Por módulo: `id`, `name`, `path`, `responsibility`, `kind`
- `kind`: `app` | `package` | `service` | `feature` | `lib` | `other`
- Opcionales: `tech`, `entrypoints`, `depends_on`, `tags`, `notes`
- Todo `depends_on` debe apuntar a un `id` existente
- MVP: unidades de primer nivel / features detectables; no explotar archivo-a-archivo
- Objetivo serializado: ~1–2k tokens; tope blando ~4k
- Plantilla: `templates/module-map.template.json`

## Capa 2 — Símbolos (opt-in)

- Path: `.navigator/symbols.json`
- Solo si `layers.symbols: true` o el usuario pide indexar símbolos
- Schema version MVP = `1`
- Por símbolo: `id`, `name`, `kind`, `file`, `line` (obligatorios)
- `kind`: `class` | `function` | `method` | `interface` | `type` | `enum` | `component` | `endpoint` | `other`
- Preferir públicos / entrypoints; omitir si no hay confianza en `file`+`line`
- **Nunca** volcar el JSON entero; filtrar y devolver top 5–15 hits (máx. 25)
- Tras localizar → Capa 4 en `file:line` si hace falta detalle
- Si deshabilitada o ausente → degradar a búsqueda en código y declarar límite
- Plantilla: `templates/symbols.template.json`

## Capa 3 — Knowledge graph (opt-in)

- Path por defecto: `.navigator/graph/graph.json` (`config.graph.path`)
- Solo si `layers.graph: true` y `graph.provider` ≠ `none`
- MVP: no bloquear bootstrap si falta; provider default `none`
- Consulta: solo subgrafo / path / query acotada (~500–1.5k tokens; tope ~2.5k)
- Nunca volcar el grafo completo

## Capa 4 — Código puntual

- Leer rangos acotados (`archivo:línea`), no directorios enteros
- Objetivo: ~80–150 líneas; tope blando ~250 líneas o ~2k tokens
- Máx. 1–3 archivos de código por pregunta
- Preferir archivo + rango sobre explorar el repo

## Reglas transversales

1. Preferir archivo + rango de líneas sobre leer directorios enteros
2. No inventar entradas de índices; si faltan, degradar o proponer update
3. Máx. 2–3 capas distintas por pregunta (salvo que el usuario pida profundidad)
4. Dump de `module-map` / `symbols` / grafo completo: **prohibido**
5. Tokens de artefactos: ~4 chars ≈ 1 token (aproximado; no hace falta contador exacto)

## Relación entre capas

| Necesidad | Capa |
| --- | --- |
| Qué es el proyecto | 0 `ai-context` |
| En qué módulo vive | 1 `module-map` (`module_id`) |
| Dónde se define el símbolo | 2 `symbols` |
| Quién llama / impacto amplio | 3 grafo (si existe) |
| Cómo está implementado | 4 código en `file:line` |
