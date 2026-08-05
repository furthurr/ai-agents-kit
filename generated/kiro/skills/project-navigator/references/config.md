# Configuración y seguridad de `.navigator/`

## `config.yaml` (contrato mínimo)

Plantilla: `templates/config.template.yaml`.

```yaml
version: 1
project:
  name: ""                      # opcional; si vacio se infiere del repo
  root: .                       # relativo al repo; monorepo puede apuntar a subcarpeta
layers:
  context: true                 # Capa 0
  module_map: true              # Capa 1
  symbols: false                # Capa 2 (opt-in MVP)
  graph: false                  # Capa 3 (opt-in MVP)
sources:
  detect_external: true         # AGENTS.md, CLAUDE.md, Contexto para IA, etc.
  export_agents_md: false       # opt-in
graph:
  provider: none                # none | graphify | custom
  path: graph/graph.json
exclude:
  - node_modules/**
  - .git/**
  - dist/**
  - build/**
  - "**/.env"
  - "**/.env.*"
  - "**/secrets/**"
update:
  strategy: manual              # manual | on_request | hook | ci  (MVP: manual/on_request)
```

### Campos clave

| Campo | Notas |
| --- | --- |
| `project.root` | Subárbol indexado; alineado a `module-map.root` y `symbols.root` |
| `layers.*` | Capas 0–1 on tras bootstrap; 2–3 opt-in |
| `graph.provider` | Default `none`; no instalar deps sin permiso |
| `exclude` | Siempre respetar al leer e indexar |
| `update.strategy` | MVP: `manual` / `on_request` |

## Artefactos

| Artefacto | Obligatorio tras bootstrap | Versionar |
| --- | --- | --- |
| `.navigator/config.yaml` | Sí | Sí |
| `.navigator/ai-context.md` | Sí | Sí |
| `.navigator/module-map.json` | Sí | Sí |
| `.navigator/symbols.json` | No | Sí si existe y es estable |
| `.navigator/graph/` | No | Configurable; solo si estable y sin secretos |
| `.navigator/cache/` | No | **No** |

## `.gitignore` recomendado

```gitignore
# project-navigator
.navigator/cache/
```

Opcional si el grafo es enorme o local-only:

```gitignore
.navigator/graph/
```

## Seguridad (política mínima MVP)

- Excluir por defecto: `.env`, `.env.*`, claves, credenciales, `secrets/`
- No copiar secretos a `ai-context`, mapas, símbolos ni grafo
- Preferir paths y nombres públicos; no pegar valores sensibles
- `.navigator/cache/` fuera de git
- Si un hallazgo parece PII/secreto al bootstrap: **omitir y avisar**
- Nada bajo `.navigator/` debe contener secretos, `.env` ni PII

Patrones sensibles orientativos (además de `exclude`):

| Patrón | Ejemplos |
| --- | --- |
| Variables de entorno | `.env`, `.env.*`, `local.properties` |
| Llaves y certificados | `*.key`, `*.pem`, `*.p12`, `*.jks`, `*.keystore` |
| Credenciales | `credentials*`, `secrets*`, `*.secret`, `service-account*.json` |
| Tokens en nombre | `token`, `apikey`, `api_key`, `password` en el path |

## Modo degradado

Principio: **degradar, no fallar**.

| Situación | Comportamiento |
| --- | --- |
| No existe `.navigator/` | Ofrecer bootstrap; si no quiere → modo minimal con fuentes externas + código puntual y aviso de coste |
| Existe config pero faltan capas | Usar las capas presentes; no inventar índices |
| Solo hay `AGENTS.md` / `CLAUDE.md` | Capa 0 provisional; invitar a materializar `ai-context.md` |
| Grafo pedido pero `graph: false` o ausente | Responder con Capa 1/2/4; indicar que Capa 3 no está habilitada |
| Symbols off o ausente | Búsqueda en código (Capa 4) y declarar que Capa 2 no está disponible |
| Tool externa ausente | Continuar skill-only; no instalar deps sin permiso |
| Secreto o path excluido | Nunca indexar ni citar contenido sensible |

Toda respuesta en modo degradado declara: **fuente usada**, **capas_ausentes** y **límite de confianza**.

## Alcance de escritura

| Puede escribir | No puede escribir |
| --- | --- |
| Solo `.navigator/**` en bootstrap/update | Código de negocio, UI, tests de producto, CI |
| Export opt-in a `AGENTS.md` **con confirmación** | Git remoto, configs del host sin permiso |
