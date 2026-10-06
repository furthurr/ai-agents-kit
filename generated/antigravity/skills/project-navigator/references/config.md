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

## Gate de disponibilidad por consulta

Ejecutar antes de elegir una capa en **cada petición**, incluso después de un
bootstrap realizado en la misma conversación. El filesystem y `config.yaml` son
la fuente de verdad; el historial conversacional no lo es.

| Configuración | Artefacto | Estado |
| --- | --- | --- |
| Capa en `true` | Existe y es legible | `disponible` |
| Capa en `true` | No existe o no es legible | `ausente` |
| Capa en `false` | Exista o no | `deshabilitada` |
| Capa no requerida por la pregunta | Cualquiera | `no_aplica` |

### Resolución determinista de instancia

Definiciones:

- `repo_root`: raíz del worktree Git; si no hay Git, raíz del workspace abierto.
- `config_path`: `.navigator/config.yaml` de la instancia seleccionada.
- `navigator_dir`: directorio que contiene `config_path`.
- `project.root`: alcance de código indexado, relativo a `repo_root`.

`project.root` **no es** la base donde buscar los índices. Todos los artefactos
de capas son relativos a `navigator_dir`. Por ejemplo, si el config elegido es
`<repo_root>/.navigator/config.yaml`, Capa 1 se comprueba exclusivamente en
`<repo_root>/.navigator/module-map.json`, aunque el entrypoint consultado esté en
`Codigo/genera/lib/main.dart`.

Selección:

1. Localizar candidatos con nombre exacto `.navigator/config.yaml` desde
   `repo_root` y subproyectos conocidos. Ignorar `.navigatorBack`, backups,
   caches y cualquier carpeta cuyo nombre no sea exactamente `.navigator`.
2. Si hay un único candidato, seleccionarlo.
3. Si hay varios, resolver el `project.root` de cada config contra `repo_root` y
   seleccionar el alcance más específico que contenga el path consultado.
4. Si existe un config raíz que cubre `.` y ningún config más específico aplica,
   seleccionar el config raíz.
5. Si cero candidatos existen, no hay Navigator. Si varios empatan, preguntar al
   usuario; nunca adivinar ni fabricar un path junto al archivo consultado.

Gate:

1. Seleccionar `config_path` con las reglas anteriores.
2. Leerlo de filesystem; no reutilizar valores recordados de otra ejecución.
3. Fijar `navigator_dir = dirname(config_path)`.
4. Para las capas candidatas, resolver y comprobar el artefacto desde
   `navigator_dir`.
5. Elegir la capa mínima entre las que estén `disponible`.
6. Reportar solo estados no disponibles que afecten a la pregunta.

Paths por capa:

| Capa | Flag | Artefacto relativo a `navigator_dir` |
| --- | --- | --- |
| 0 | `layers.context` | `ai-context.md` |
| 1 | `layers.module_map` | `module-map.json` |
| 2 | `layers.symbols` | `symbols.json` |
| 3 | `layers.graph` | Path de `graph.path` |

Una respuesta degradada declara:

- `fuentes`: paths realmente consultados
- `capas_ausentes`: capas habilitadas cuyo artefacto no existe
- `capas_deshabilitadas`: capas relevantes configuradas en `false`
- `confianza`: `alta`, `media` o `baja`, con una razón breve

No declarar una capa como ausente sin haber comprobado su path resuelto desde
`navigator_dir`. No incluir capas `no_aplica` en la respuesta.

## Alcance de escritura

| Puede escribir | No puede escribir |
| --- | --- |
| Solo `.navigator/**` en bootstrap/update | Código de negocio, UI, tests de producto, CI |
| Export opt-in a `AGENTS.md` **con confirmación** | Git remoto, configs del host sin permiso |
