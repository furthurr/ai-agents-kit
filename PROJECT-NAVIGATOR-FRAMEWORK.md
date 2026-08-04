# Project Navigator Framework

> Framework agnostico para crear una skill y un agente que permitan a una IA
> comprender y navegar cualquier proyecto con el minimo consumo de tokens.
>
> Estado: definicion MVP lista para implementar
> Ultima actualizacion: 2026-08-04
> Implementacion: pendiente — siguiente paso: crear skill/agente en el kit (§18–21)
> Documentacion del kit actual: [README.md](README.md) · [docs/](docs/README.md)
> (este archivo es roadmap; aun no forma parte del manifest instalable).

## 1. Objetivo

Crear un framework reutilizable, independiente del proyecto, lenguaje,
framework y sistema operativo, para que una IA pueda:

- Acceder a documentacion clara, estructurada y persistente.
- Entender arquitectura, modulos, relaciones y logica sin leer todo el codigo.
- Consultar codigo solo cuando las capas documentales no sean suficientes.
- Reducir el consumo de tokens en tareas de investigacion y onboarding.
- Mantener los artefactos actualizados de forma incremental.

El objetivo no es documentar un proyecto concreto. El resultado debe poder
instalarse y adaptarse a cualquier repositorio.

## 2. Problema Que Resuelve

Sin contexto persistente, un agente de IA normalmente:

- Explora miles de archivos para responder preguntas puntuales.
- Re-descubre la arquitectura en cada sesion.
- Lee archivos completos cuando solo necesita un simbolo o una funcion.
- Repite investigacion ya realizada y gasta tokens innecesariamente.
- Da respuestas inconsistentes cuando la documentacion no es una fuente unica
  y mantenida.

La propuesta aplica divulgacion progresiva: el agente consulta primero la
fuente mas compacta y solo aumenta el detalle cuando la pregunta lo exige.

## 3. Principio Rector

> La IA no debe explorar todo el repositorio para responder una pregunta.
> Debe comenzar con contexto persistente, navegar relaciones estructuradas y
> leer codigo solamente cuando sea imprescindible.

## 4. Arquitectura Conceptual

```text
Pregunta del usuario
        |
        v
Skill project-navigator
        |
        +-- Clasifica la pregunta
        |
        +-- Consulta la capa minima necesaria
                |
                +-- Capa 0: Contexto raiz
                +-- Capa 1: Mapa estructural
                +-- Capa 2: Indice de simbolos
                +-- Capa 3: Knowledge graph
                +-- Capa 4: Codigo fuente puntual
```

### Capa 0: Contexto raiz (enfoque hibrido)

`ai-context.md` no es un estandar de la industria. Existen convenciones
competidoras (`AGENTS.md`, `CLAUDE.md`, instrucciones de Copilot, secciones
"Contexto para IA" en carpetas canónicas, etc.). El framework adopta un
**enfoque hibrido**:

#### Artefacto canonico (interno del navigator)

```text
.navigator/ai-context.md
```

Es la fuente de verdad de la Capa 0 para `project-navigator`: denso, estable y
orientado a navegacion del proyecto (~500 tokens).

Contenido esperado:

- Proposito y alcance del proyecto.
- Tecnologias y build system.
- Arquitectura, modulos y patrones clave.
- Convenciones de desarrollo relevantes.
- Ubicacion de documentacion existente.
- Decisiones, riesgos y restricciones importantes.
- Indice de fuentes externas de contexto detectadas (ver abajo).

#### Fuentes externas de compatibilidad (solo lectura / merge)

Al bootstrap y al responder, la skill debe detectar y, cuando aporte valor,
incorporar o referenciar:

| Fuente | Rol tipico |
| --- | --- |
| `AGENTS.md` (raiz) | Convencion emergente multi-herramienta |
| `CLAUDE.md` | Contexto/reglas de Claude Code |
| `.cursorrules`, `.cursor/rules/` | Reglas de Cursor |
| `.github/copilot-instructions.md` | Instrucciones de GitHub Copilot |
| `README.md` con seccion "Contexto para IA" en carpetas canonicas (`.architecture/`, `.data/`, `.quality/`, `.security/`, `.design/`, etc.) | Contexto de dominio ya mantenido por otras skills |
| `README.md` raiz | Descripcion general del proyecto |

Reglas del hibrido:

1. **Canonico**: `.navigator/ai-context.md` es lo que la Capa 0 prioriza.
2. **No invadir**: no sobrescribir `AGENTS.md` / `CLAUDE.md` ajenos sin
   confirmacion del usuario.
3. **Detectar y enlazar**: el bootstrap lista fuentes halladas y las resume o
   referencia desde `ai-context.md`.
4. **Modo degradado**: si no existe `.navigator/ai-context.md` pero si
   `AGENTS.md`, `CLAUDE.md` u otro contexto externo, usarlo como Capa 0
   provisional e invitar al bootstrap.
5. **Sincronizacion opcional**: el usuario puede pedir exportar/resumir hacia
   `AGENTS.md` para interoperar con otras herramientas; es opt-in, no
   obligatorio.

Uso: preguntas como "que es este proyecto?" o "como esta organizado?".

Tamano objetivo del canonico: aproximadamente 500 tokens.

Plantilla formal y reglas de generacion: **§19.1**.
Ubicacion en monorepo: **§19.3**.

### Capa 1: Mapa estructural

Archivo propuesto:

```text
.navigator/module-map.json
```

Contenido esperado:

- Modulos, paquetes, servicios o features.
- Responsabilidad de cada unidad.
- Archivos relevantes.
- Dependencias entre unidades.
- Capas o tecnologias involucradas.

Uso: "en que modulo esta X?" o "que depende de Y?".

Schema, ejemplo minimo y reglas: **§19.2**.

### Capa 2: Indice de simbolos

Archivo propuesto:

```text
.navigator/symbols.json
```

Contenido esperado por simbolo:

- Nombre y tipo: clase, funcion, interfaz, endpoint, componente, etc.
- Archivo y linea de definicion.
- Firma publica.
- Dependencias relevantes.
- Implementaciones, consumidores o extensiones cuando aplique.
- Resumen breve.

Uso: "donde se define X?" o "que metodos tiene Y?".

La generacion debera basarse preferentemente en AST o herramientas nativas del
lenguaje, para evitar gastar tokens en datos que se pueden extraer de forma
deterministica. En el MVP es **opt-in y best-effort** (sin exigir AST
multi-lenguaje completo).

Schema, ejemplo y reglas: **§20**.

### Capa 3: Knowledge graph

Archivo propuesto:

```text
.navigator/graph/graph.json
```

El grafo debera poder relacionar:

- Nodos: modulos, clases, funciones, endpoints, documentos, decisiones y
  conceptos relevantes.
- Relaciones: importa, implementa, llama, depende, expone, documenta,
  pertenece a, consume, produce, etc.
- Comunidades: agrupaciones funcionales o arquitectonicas.

Uso: "como se relaciona X con Y?" o "que impacto tiene cambiar Z?".

Decision MVP: Capa 3 **opt-in** (`graph.provider: none` por defecto).
`graphify` es el **candidato preferido** como adapter post-MVP (sin dependencia
hard del core). La consulta nunca debe volcar el grafo completo al modelo:
solo subgrafo, path o query acotada. Ver §14.6.

### Capa 4: Codigo fuente

El codigo se consulta solo cuando las capas anteriores no proporcionan detalle
suficiente. La skill debera preferir archivo y rango de lineas precisos sobre
la lectura completa de directorios o archivos.

## 5. Componentes Decididos

### 5.1 Skill `project-navigator`

El framework tendra una skill que contendra las reglas universales de
navegacion.

Responsabilidades:

- Clasificar la pregunta recibida.
- Elegir la capa minima necesaria para responder.
- Priorizar documentacion, indices y grafo antes que codigo.
- Evitar exploracion amplia e innecesaria.
- Aplicar un modo degradado si faltan artefactos o dependencias.
- Indicar claramente la fuente usada y limites de la respuesta.

La skill debe poder instalarse de dos formas, a eleccion del usuario:

```text
Global:       ~/.config/opencode/skills/project-navigator/
Por proyecto: .opencode/skills/project-navigator/
```

### 5.2 Sub-agente `project-navigator`

El framework tambien tendra un sub-agente dedicado a investigacion y
navegacion del proyecto.

Responsabilidades:

- Resolver consultas de arquitectura, logica, dependencias e impacto.
- Trabajar en modo solo lectura por defecto.
- Usar el contexto, indices, grafo y codigo puntual.
- Poder invocarse explicitamente, por ejemplo con `@project-navigator`.

Permisos iniciales esperados:

- Lectura, busqueda y listado: permitidos.
- Edicion: denegada por defecto.
- Comandos de sistema: restringidos a lo necesario para consultar o actualizar
  artefactos, segun el modo de uso.

La configuracion debera poder instalarse globalmente o dentro del proyecto.

## 6. Estrategia de Modelos y Proveedores

### 6.1 Principio rector

> El framework NO selecciona, configura ni fuerza un modelo.
> Solo recomienda categorias y pide al usuario cambiar el modelo
> manualmente en la herramienta host (OpenCode, Copilot, Kiro, etc.).

### 6.2 Decision: aviso manual, no auto-seleccion

| Quien | Que hace |
| --- | --- |
| Usuario | Elige y cambia el modelo en la UI/CLI del host |
| Skill / agente | Emite avisos de recomendacion al inicio y al final del proceso |
| Framework | Nunca escribe `model:` en configs del host ni asume un modelo concreto |

Prohibido en MVP y despues:

- Hardcodear Claude Haiku u otro modelo concreto como default del sub-agente.
- Cambiar el modelo de la sesion en nombre del usuario.
- Fallar si el modelo actual no es el "recomendado".
- Bloquear el flujo por no haber cambiado de modelo.

El proceso puede continuar con el modelo actual si el usuario lo prefiere;
solo se avisa del coste/beneficio.

### 6.3 Flujo de avisos (obligatorio en skill y agente)

Aplica a: bootstrap, update pesado, indexado y sesiones de navegacion que
vayan a consumir varias capas de forma reiterada.

**Antes del proceso:**

1. Informar que va a empezar un proceso de `project-navigator`.
2. Recomendar cambiar **manualmente** a un modelo de categoria
   **pequeno / rapido / economico** (navegacion, clasificacion y sintesis de
   indices; poca creatividad).
3. Dar ejemplos **no vinculantes** segun lo que suela tener el usuario (p. ej.
   Haiku-class, Grok Build, Mini, Flash u equivalentes de su proveedor).
4. Esperar confirmacion de que ya cambio **o** de que prefiere continuar con
   el modelo actual.
5. Solo entonces continuar.

Plantilla de aviso inicial (orientativa):

```text
Antes de continuar con project-navigator, te recomiendo cambiar manualmente
el modelo de esta sesion a uno pequeno/rapido/economico (menor costo y
latencia para indexar y navegar).

No cambio el modelo por ti. Cuando lo hayas cambiado (o si prefieres seguir
con el actual), confirmalo y sigo.
```

**Despues del proceso:**

1. Informar que el proceso navigator termino y que artefactos se tocaron.
2. Avisar que ya puede cambiar **manualmente** el modelo a uno orientado a su
   **siguiente tarea** (coding, diseno, razonamiento fuerte, etc.).
3. Si el usuario indico la tarea, sugerir solo la **categoria** adecuada;
   nunca imponer un ID de modelo.

Plantilla de aviso final (orientativa):

```text
project-navigator termino.

Ya puedes cambiar manualmente el modelo a uno enfocado en tu siguiente tarea
(p. ej. coding agentic para implementar, o razonamiento fuerte para disenar).
No lo cambio por ti.
```

### 6.4 Recomendaciones por categoria (no por marca fija)

| Momento / rol | Categoria recomendada | Ejemplos no vinculantes |
| --- | --- | --- |
| Antes / durante navigator | Pequeno, rapido, barato | Haiku-class, Grok Build, Mini, Flash, etc. |
| Tras navigator → implementar codigo | Coding agentic | Grok Build, Codex-class, Sonnet, etc. |
| Tras navigator → diseno / arquitectura | Razonamiento fuerte | Grok 4.5, Opus/Sonnet, GPT flagship, etc. |
| Sin preferencia del usuario | Heredar el de la sesion; solo avisar | — |

Los ejemplos son ilustrativos y caducan. La skill no debe depender de IDs
concretos de proveedor ni fallar si un ejemplo no esta disponible.

### 6.5 Proveedores — DECIDIDO (agnostico por diseno)

No se investigara ni probara una matriz exhaustiva de proveedores (OpenAI,
MiniMax, Anthropic, xAI, OpenCode Zen, etc.). No es viable ni necesario para el
MVP. La calidad se obtiene con **comportamiento portable**, no con tuning por
vendor.

#### Que queda cerrado

| Tema | Decision |
| --- | --- |
| Matriz por cuenta / credenciales | **Cancelada** como deuda de planificacion |
| Soporte de proveedores | Todos los que el host ya exponga; el framework no elige |
| Codigo o prompts por vendor | Prohibidos (`if provider == openai`, IDs fijos, etc.) |
| Pruebas multi-proveedor | No requeridas; validar en el host/cuenta que use el equipo |
| Fallback de credenciales | Responsabilidad del host, no del navigator |

#### Como se logra buen trabajo con cualquier proveedor

1. **Capas deterministas primero** — `ai-context`, `module-map`, simbolos AST y
   grafo reducen la dependencia de la “inteligencia” del modelo.
2. **Divulgacion progresiva** — menos tokens y menos alucinacion en cualquier LLM.
3. **Instrucciones por categoria, no por marca** — pequeno/rapido vs coding vs
   razonamiento; el usuario mapea a lo que tenga en su selector.
4. **Contratos de salida estables** — plantillas y JSON con schema; el modelo
   rellena estructura, no inventa el formato.
5. **Modo degradado** — si el modelo o el host son limitados, se reduce alcance
   y se declara confianza; no se asume tool calling exotico de un vendor.
6. **Tools del host, no APIs de proveedor** — Read/Grep/Glob/Bash genericos via
   OpenCode/Copilot/Kiro; cero SDK de OpenAI/Anthropic/xAI dentro del framework.
7. **Avisos de modelo manuales** (§6.3) — el usuario optimiza costo/calidad con
   lo que su cuenta permita, sin que el framework conozca el catalogo.
8. **Adapters solo de plataforma** (OpenCode / Copilot / Kiro), nunca de
   proveedor LLM.

#### Requisitos minimos del modelo (cualquier vendor)

El usuario debe elegir un modelo del host que, en la practica, pueda:

- Seguir instrucciones y rellenar plantillas/JSON.
- Usar herramientas basicas del host (leer, buscar, listar).
- Respetar “no inventar paths” y citar fuentes de capa.

Si el modelo no cumple eso, el modo degradado avisa y limita el alcance; no se
escribe un fork por proveedor.

#### Fuera de alcance deliberado

- Documentar precios, rate limits o IDs por cuenta.
- Auto-detectar el mejor modelo disponible en la cuenta.
- Scripts de “connect” a OpenAI/MiniMax/etc.
- Garantizar paridad de calidad entre todos los LLMs del mercado.

### 6.6 Principio (cita)

> El framework no depende de un proveedor ni de un modelo especifico.
> Se optimiza para portabilidad (capas, schemas, avisos por categoria).
> El usuario elige proveedor y modelo en el host; no probamos todos.

## 7. Instalacion Global o por Proyecto

El usuario elegira el alcance de instalacion.

### Instalacion global

Ventajas:

- Disponible para todos los proyectos del usuario.
- Una sola instalacion y actualizacion.
- Adecuada para uso personal o configuracion centralizada de equipo.

Los datos particulares de cada repositorio deben mantenerse dentro de ese
repositorio, por ejemplo:

```text
mi-proyecto/.navigator/
```

### Instalacion por proyecto

Ventajas:

- Puede versionarse con Git junto al proyecto.
- Permite reglas y configuracion especificas.
- Se comparte automaticamente con el equipo al clonar el repositorio.
- No afecta otros proyectos del usuario.

### Principio de separacion

La skill y el agente son reutilizables. El contexto, indices, grafo y
configuracion son propios de cada proyecto.

## 8. Estructura Propuesta del Framework

### 8.1 Distribucion decidida: dentro de AI Agents Kit

El framework **no** sera un repositorio independiente en el MVP. Vivira en este
kit, con el mismo flujo que el resto de skills/agentes:

```text
canonical/
  skills/project-navigator/
    SKILL.md
    references/
      layers.md
      bootstrap.md
      config.md
      sources.md
      templates/
        ai-context.template.md
        module-map.template.json
        symbols.template.json
        config.template.yaml
  agents/project-navigator.md

adapters/
  opencode/ ...
  copilot/ ...
  kiro/ ...

generated/          # render.py -> artefactos instalables
scripts/install/    # instalacion por plataforma
```

Post-MVP (opcional): scripts deterministas de bootstrap/update/verify podran
vivir en `canonical/skills/project-navigator/scripts/` o en `tools/navigator/`,
siempre invocables de forma portable (Python + pathlib).

### 8.2 Estructura en un proyecto consumidor

Estructura propuesta dentro de un proyecto que use el framework:

```text
mi-proyecto/
├── AGENTS.md                      # opcional; compatibilidad externa (no canonico)
├── CLAUDE.md                      # opcional; detectado si existe
├── .opencode/
│   ├── skills/
│   │   └── project-navigator/
│   └── agents/
│       └── project-navigator.md
├── .architecture/                 # opcional; "Contexto para IA" si existe
└── .navigator/
    ├── config.yaml
    ├── ai-context.md              # Capa 0 canonica (hibrido)
    ├── module-map.json
    ├── symbols.json
    └── graph/
        └── graph.json
```

Estructura de consumidor y versionado: **§19.3** (monorepo) y **§19.4**
(gitignore / que versionar). Artefactos opcionales: symbols y graph (§14.3).

## 9. Bootstrap Generico de un Proyecto

El framework debera poder inicializarse sobre cualquier repositorio.

Flujo conceptual:

1. Detectar lenguajes, build systems y frameworks.
2. Detectar documentacion existente y fuentes externas de contexto
   (`AGENTS.md`, `CLAUDE.md`, reglas de editor, "Contexto para IA" en carpetas
   canonicas, `README.md` raiz).
3. Excluir dependencias, codigo generado, binarios y secretos.
4. Generar o proponer el contexto raiz canonico (`.navigator/ai-context.md`)
   fusionando/resumiendo fuentes externas sin sobrescribirlas.
5. Generar el mapa de modulos (`module-map.json`).
6. (Opt-in) Generar indice de simbolos si `layers.symbols: true`.
7. (Opt-in) Construir knowledge graph si `layers.graph: true` y hay provider.
8. Validar cobertura minima (capas 0–1), consistencia y fechas.
9. Informar al usuario que se genero, que falta, que fuentes externas se
   detectaron y como operar el sistema.
10. Opcional (opt-in): ofrecer exportar un resumen compatible a `AGENTS.md`.

#### Stack del MVP — DECIDIDO (agnostico)

El MVP **no** limita lenguajes. Detecta por indicadores y genera capas 0–1
con la misma plantilla para cualquier stack. La calidad del mapa depende de la
estructura del repo, no de una lista blanca de frameworks.

Indicadores de deteccion (no exhaustivos; extensibles):

| Tecnologia | Indicadores posibles |
| --- | --- |
| Node.js / JS/TS | `package.json`, lockfiles, workspaces |
| Python | `pyproject.toml`, `requirements.txt` |
| Java/Kotlin | `build.gradle`, `settings.gradle`, `pom.xml` |
| Flutter/Dart | `pubspec.yaml` |
| Rust | `Cargo.toml` |
| Go | `go.mod` |
| Swift/iOS | `Package.swift`, `.xcodeproj`, `.xcworkspace` |
| .NET | `.csproj`, `.sln` |

Capa 2 (symbols) y AST por lenguaje: best-effort / post-MVP (§20.7).

## 10. Compatibilidad Cross-Platform

El framework debe ser funcional en:

- macOS.
- Windows.
- Linux.

### Principios propuestos

- Preferir Python para la logica de scripts frente a Bash como dependencia
  central.
- Usar `pathlib` para rutas portables.
- Usar `subprocess` y evitar comandos exclusivos de Unix.
- Detectar herramientas con `shutil.which`.
- Usar UTF-8 de forma explicita.
- Informar comandos de instalacion apropiados por sistema operativo.
- Ofrecer modo degradado si faltan dependencias.

### Modos de operacion propuestos

| Modo | Requisitos | Capacidades |
| --- | --- | --- |
| Full | Runtime, Git, indexador y herramienta de grafo | Todas las capas |
| Degraded | OpenCode y documentacion existente | Navegacion documental e indice basico |
| Minimal | Solo OpenCode | Consulta de contexto existente y guia de setup |

### Decisiones cross-platform (resueltas; detalle §14.11)

| Tema | Decision |
| --- | --- |
| Runtime de scripts | Python 3 + pathlib (como `tools/` del kit) |
| Install por OS | Scripts del kit (`.sh` / `.ps1`); Windows nativo soportado |
| WSL | Como Linux; no requisito en Windows nativo |
| Dependencias extra (grafo, AST) | Opt-in; si faltan → modo degradado, no instalar sin permiso |
| Politica ante faltantes | **Degradar, no fallar** (§14.5) |
| Encoding / EOL | UTF-8; respetar Git del usuario en Windows |

## 11. Mantenimiento Incremental

El sistema debe actualizar solo lo afectado por cambios, no regenerar todo.

| Evento | Accion esperada |
| --- | --- |
| Cambio de codigo | Actualizar simbolos y relaciones afectadas |
| Cambio de documentacion | Actualizar contexto y referencias |
| Nuevo modulo | Actualizar mapa estructural |
| Archivo eliminado | Eliminar nodos y referencias obsoletas |
| Commit o push | Actualizacion incremental opcional |
| Pull request o merge request | Validacion opcional en CI/CD |

Estrategias posibles:

- Actualizacion manual.
- Hook de Git.
- File watcher.
- CI/CD.
- Combinacion configurable por proyecto.

Decision MVP: estrategia `manual` u `on_request`. Hooks, watcher y CI quedan
como post-MVP configurables en `update.strategy`. Ver §14.10.

## 12. Seguridad y Privacidad

El framework debera considerar desde el inicio:

- Exclusion de secretos, claves, tokens y archivos `.env`.
- Deteccion y manejo de PII o informacion confidencial.
- Politica para artefactos generados que puedan contener nombres de endpoints,
  modelos o estructura interna.
- Definicion de que archivos pueden versionarse o deben ignorarse.
- Separacion entre informacion local, compartible y sensible.

Politica minima MVP definida en §14.12 (exclusiones, no indexar secretos,
cache fuera de git). Detalle fino de PII y monorepos grandes sigue abierto.

## 13. Criterios de Exito

| Metrica | Objetivo inicial |
| --- | --- |
| Reduccion de tokens por investigacion | 90 por ciento o mas |
| Tiempo de bootstrap de un proyecto base | 30 minutos o menos |
| Sistemas operativos | macOS, Windows y Linux |
| Alcance de instalacion | Global o por proyecto |
| Degradacion | Util sin todas las dependencias |
| Reutilizacion | Aplicable a proyectos de distintos stacks |
| Mantenimiento | Actualizacion incremental y verificable |

## 14. Decisiones de Definicion (ronda 2026-08-03)

### 14.1 Distribucion — DECIDIDO

| Aspecto | Decision |
| --- | --- |
| Donde vive | Dentro de **AI Agents Kit** (`canonical/` + `adapters/` + `generated/`) |
| Repo independiente | No en el MVP |
| Plataformas | OpenCode, Copilot y Kiro (mismo pipeline de render/install) |
| Versionado | El del kit (git + releases del kit) |
| Compartir con equipos | Via kit instalado + artefactos `.navigator/` versionados en cada repo |
| Scripts de indexado | Opcionales post-MVP; el MVP puede generar capas con la IA siguiendo plantillas |

### 14.2 Alcance del MVP — DECIDIDO

El MVP entrega **skill + agente + plantillas + flujo de bootstrap asistido por IA**.
No exige scripts deterministas completos ni grafo obligatorio.

| Pieza | MVP | Post-MVP |
| --- | --- | --- |
| Skill `project-navigator` | Si | Mejoras |
| Agente `project-navigator` | Si | Mejoras |
| Adaptadores OpenCode / Copilot / Kiro | Si | - |
| `.navigator/ai-context.md` (Capa 0) | Si, obligatorio tras bootstrap | - |
| `.navigator/module-map.json` (Capa 1) | Si, obligatorio tras bootstrap | - |
| `.navigator/config.yaml` | Si, minimo | Opciones avanzadas |
| Deteccion hibrida de contexto externo | Si | - |
| Bootstrap asistido (IA + plantillas) | Si | Bootstrap determinista (Python) |
| `.navigator/symbols.json` (Capa 2) | Opcional / best-effort | Generacion AST multi-lenguaje |
| Knowledge graph (Capa 3) | Opcional | Adapter `graphify` u otro |
| Update incremental automatico | Manual o pedida por el usuario | Hooks / CI / watcher |
| Cobertura de dominios | Codigo + docs + carpetas canonicas existentes | Infra, diseno, seguridad como nodos de grafo |

**MVP de bootstrap (asistido):**

1. Detectar stack y fuentes de contexto externas.
2. Crear `.navigator/` si no existe.
3. Escribir `config.yaml` minimo.
4. Generar `ai-context.md` (~500 tokens) y `module-map.json`.
5. Informar fuentes detectadas, gaps y como consultar.
6. No bloquear si faltan simbolos o grafo.

### 14.3 Artefactos: obligatorios vs opcionales — DECIDIDO

| Artefacto | Obligatorio tras bootstrap | Versionar en git | Notas |
| --- | --- | --- | --- |
| `.navigator/config.yaml` | Si | Si | Config del proyecto |
| `.navigator/ai-context.md` | Si | Si | Capa 0 canonica |
| `.navigator/module-map.json` | Si | Si | Capa 1 |
| `.navigator/symbols.json` | No | Si si existe | Capa 2 |
| `.navigator/graph/` | No | Configurable; por defecto si si es estable y sin secretos | Capa 3 |
| `.navigator/cache/` | No | No | Cache local; gitignore |
| `AGENTS.md` (raiz) | No | Segun equipo | Export opt-in |

### 14.4 Configuracion `.navigator/config.yaml` — DECIDIDO (contrato minimo)

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

### 14.5 Politica de modo degradado — DECIDIDO

Principio: **degradar, no fallar**.

| Situacion | Comportamiento |
| --- | --- |
| No existe `.navigator/` | Ofrecer bootstrap; si el usuario no quiere, modo minimal con fuentes externas + codigo puntual y aviso de coste |
| Existe config pero faltan capas | Usar las capas presentes; no inventar indices |
| Solo hay `AGENTS.md` / `CLAUDE.md` | Capa 0 provisional; invitar a materializar `ai-context.md` |
| Grafo pedido pero `graph: false` o ausente | Responder con Capa 1/2/4; indicar que Capa 3 no esta habilitada |
| Script/herramienta externa ausente | Continuar en modo skill-only; no instalar dependencias sin permiso |
| Secreto o path excluido | Nunca indexar ni citar contenido sensible |

Toda respuesta en modo degradado debe declarar: **fuente usada**, **capas
ausentes** y **limite de confianza**.

### 14.6 Knowledge graph — DECIDIDO (MVP)

| Aspecto | Decision |
| --- | --- |
| Obligatorio | No; Capa 3 opt-in |
| Provider por defecto | `none` |
| Candidato preferido post-MVP | `graphify` (adapter, no hard dependency del core) |
| Consulta | Nunca volcar el grafo completo al modelo; subgrafo / query / path |
| Ubicacion canonica | `.navigator/graph/graph.json` (aunque graphify escriba en `graphify-out/`, el adapter puede copiar o enlazar) |

### 14.7 Postura de diseno — DECIDIDO

- **Neutral en stack**: no impone arquitectura de negocio.
- **Opinionado en navegacion**: siempre divulgacion progresiva y capas.
- **Alineado al kit**: misma carpeta canónica por concern (`.navigator/` como
  los demas `.architecture/`, `.data/`, etc.).
- **Solo lectura por defecto** en el agente de navegacion.
- **Escritura limitada** a `.navigator/` (y export opt-in a `AGENTS.md`) solo en
  modos bootstrap/update explicitos.

### 14.8 Agente en interfaz grafica — DECIDIDO (requisito)

El sub-agente debe poder:

1. Registrarse en el selector de agentes del host cuando la plataforma lo
   soporte (OpenCode, Copilot, Kiro via adapters del kit).
2. Invocarse por texto (`@project-navigator` o equivalente del host).
3. Tener descripcion corta orientada a UI: investigacion/navegacion de
   proyecto en solo lectura.

Una skill sola no garantiza UI universal: cada adapter del kit aporta el
frontmatter/permisos/nombre visibles en esa herramienta.

### 14.9 Modelos — DECIDIDO

| Aspecto | Decision |
| --- | --- |
| Quien elige el modelo | Siempre el usuario, en el host |
| Auto-seleccion por skill/agente | Prohibida |
| Antes de bootstrap/update/navegacion pesada | Aviso: cambiar manualmente a categoria pequeno/rapido/economico; esperar confirmacion o "sigo con el actual" |
| Al finalizar el proceso | Aviso: ya puede cambiar manualmente a un modelo de su siguiente tarea |
| Default hardcodeado (Haiku u otro) | No |
| Si no cambia de modelo | Continuar igual; no fallar |
| Proveedor | Agnostico por diseno; sin matriz ni pruebas multi-vendor (§6.5) |
| Matriz OpenAI/MiniMax/etc. | **Cancelada** — no viable ni necesaria |
| Calidad multi-proveedor | Capas deterministas + schemas + degradado + tools del host |
| Ejemplos de modelos en docs/avisos | Solo ilustrativos por categoria; no vinculantes |

Detalle operativo y plantillas de aviso: §6.

### 14.10 Mantenimiento — DECIDIDO (MVP)

MVP: **manual / on_request** (el usuario pide actualizar, o la skill detecta
desfase y pregunta).

Post-MVP: hooks git, CI, watcher — configurables en `update.strategy`.

### 14.11 Cross-platform — DECIDIDO (direccion)

| Aspecto | Decision |
| --- | --- |
| Runtime de scripts | Python 3 + pathlib (alineado al kit: `tools/*.py`) |
| Shell de install | Ya resuelto por el kit (`.sh` / `.ps1`) |
| Dependencias extra | Opt-in; si faltan, modo degradado |
| WSL | Soporte como Linux; no requisito en Windows nativo |
| Encoding | UTF-8 explicito |

### 14.12 Seguridad (politica minima MVP) — DECIDIDO

- Excluir por defecto: `.env`, `.env.*`, claves, credenciales, `secrets/`.
- No copiar secretos a `ai-context`, mapas, simbolos ni grafo.
- Preferir paths y nombres publicos; no pegar valores sensibles.
- `.navigator/cache/` fuera de git.
- Si un hallazgo parece PII/secreto al bootstrap: omitir y avisar.

## 15. Deuda de Planificacion Restante

### 15.1 Aun pendiente

- Adapter concreto `graphify` (mapeo `graphify-out/` → `.navigator/graph/`).
- Estrategia AST por lenguaje para Capa 2 (generacion determinista post-MVP).
- Politica fina de que partes del grafo se versionan en monorepos grandes.
- Ejemplos por tipo de proyecto (mobile/backend/frontend) — doc opcional.
- Implementacion en el kit (`canonical/`, adapters, `manifest.json`).

### 15.2 Resuelto en esta ronda

- Distribucion via AI Agents Kit.
- Alcance MVP (skill + agente + bootstrap asistido + capas 0/1).
- Artefactos obligatorios/opcionales.
- Contrato minimo de `config.yaml`.
- Modo degradado.
- Grafo opt-in; graphify como candidato adapter.
- UI del agente via adapters del kit.
- Mantenimiento manual/on_request en MVP.
- Cross-platform orientado a Python del kit (§10 alineado a §14.11).
- Seguridad minima de exclusiones.
- Modelos: aviso manual, sin auto-seleccion (§6, §14.9).
- Proveedores: agnostico por diseno; matriz multi-vendor **cancelada** (§6.5).
- Contratos de comportamiento skill + agente **definidos en documento** (§18).
- Plantilla `ai-context.md`, schema `module-map.json`, monorepo y gitignore (§19).
- Schema `symbols.json` (Capa 2 opt-in, best-effort) (§20).
- Stack MVP agnostico; versionado de artefactos (§8–9 limpios).
- Presupuesto de tokens numerico (§21).

## 16. Proximos Pasos

1. Implementar en el kit: `canonical/skills/project-navigator/` y
   `canonical/agents/project-navigator.md` segun §18–21.
2. Anadir adapters (OpenCode, Copilot, Kiro) y entrada en `manifest.json`.
3. Render + validate + install de prueba.
4. Probar bootstrap asistido en un repo real sin `.navigator/`.
5. (Opcional doc) ejemplos mobile/backend/frontend.
6. (Post-MVP) AST multi-lenguaje, scripts deterministas y adapter graphify.

## 17. Estado Actual de Decisiones

| Tema | Estado |
| --- | --- |
| Enfoque agnostico al proyecto | Decidido |
| Skill `project-navigator` | Decidido |
| Sub-agente `project-navigator` | Decidido |
| Instalacion global o por proyecto | Configurable por usuario (via kit) |
| Distribucion | **Decidido: dentro de AI Agents Kit** |
| Alcance MVP | **Decidido: skill + agente + bootstrap asistido + capas 0/1** |
| Capa 0 hibrida | Decidido |
| Artefactos obligatorios/opcionales | Decidido |
| `config.yaml` minimo | Decidido |
| Modo degradado | Decidido (degradar, no fallar) |
| Knowledge graph | **Opt-in; graphify candidato adapter** |
| Agente en UI del host | Decidido (via adapters) |
| Mantenimiento MVP | Manual / on_request |
| Cross-platform | Python 3 + scripts del kit |
| Seguridad minima | Exclusiones y no indexar secretos |
| Modelo runtime del sub-agente | **Aviso manual a modelo pequeno; no auto-seleccion** (§6, §14.9) |
| Tras el proceso navigator | **Aviso manual a modelo de la tarea siguiente** |
| Modelo para construir el framework | Fuerte (diseno) + coding (implementacion); eleccion del usuario |
| Proveedores LLM | **Decidido: agnostico por diseno; sin matriz ni pruebas multi-vendor** (§6.5) |
| Contratos SKILL.md / agente | **Definidos en §18; implementacion en kit pendiente** |
| Plantilla `ai-context.md` (Capa 0) | **Definida en §19.1** |
| Schema `module-map.json` (Capa 1) | **Definido en §19.2** |
| Monorepo / ubicacion `.navigator/` | **Definido en §19.3** |
| `.gitignore` de `.navigator/` | **Definido en §19.4** |
| Schema `symbols.json` (Capa 2) | **Definido en §20** (opt-in, best-effort MVP) |
| Stack / lenguajes MVP | **Agnostico por deteccion** (§9); sin lista blanca |
| Versionado artefactos `.navigator/` | **§19.4** |
| Cross-platform | **Resuelto** (§10 + §14.11); degradar si faltan deps |
| Presupuesto de tokens | **Definido en §21** |
| Generacion AST multi-lenguaje | Post-MVP |
| Automatizacion hooks/CI | Post-MVP |

## 18. Contratos de Comportamiento (especificacion MVP)

> Especificacion en documento. Aun **no** existen archivos en `canonical/`.
> Cuando se implementen, este apartado es la fuente de verdad del comportamiento.
> Si el agente y la skill divergen, **manda la skill**.

### 18.1 Skill `project-navigator`

#### Metadatos previstos (frontmatter futuro)

```yaml
name: project-navigator
description: >-
  Navega cualquier proyecto con minimo de tokens mediante capas en `.navigator/`
  (contexto, mapa de modulos, simbolos, grafo y codigo puntual). Hace bootstrap
  y update de indices bajo peticion. No modifica codigo de negocio. Avisa al
  usuario para cambiar el modelo manualmente antes/despues de procesos pesados;
  nunca selecciona el modelo por el usuario.
```

#### Rol

- Referencia canonica de **como navegar e indexar** un repositorio.
- Complementa al agente `project-navigator`.
- Objetivo: responder con la capa mas barata suficiente y citar fuentes.

#### Alcance inviolable

| Puede | No puede |
| --- | --- |
| Leer el repo respetando `exclude` y secretos | Modificar codigo de negocio, UI, tests de producto, CI o Git remoto |
| Escribir **solo** en `.navigator/` | Instalar dependencias o cambiar configs del host sin permiso |
| Export opt-in a `AGENTS.md` **con confirmacion** | Seleccionar o forzar el modelo de la sesion |
| Ofrecer y ejecutar bootstrap/update de indices | Inventar paths, simbolos o arquitectura no respaldados |
| Usar tools genericos del host (read/search/list) | Depender de APIs o IDs de un proveedor LLM |

Si piden implementar features o refactors de producto: **declarar limite**,
aportar ubicacion/mapa si ayuda, y detenerse (no implementar).

#### Cuando usar

- Onboarding: que es el proyecto, como esta organizado.
- Localizar modulos, simbolos, dependencias e impacto.
- Antes de una feature/refactor cuando haga falta mapa sin reexplorar el repo.
- Primera vez sin `.navigator/` → bootstrap.
- Actualizar indices cuando el usuario lo pida o haya desfase claro.

#### Flujo obligatorio al recibir una peticion

1. **Clasificar** la peticion (consulta vs bootstrap/update vs fuera de alcance).
2. Si es bootstrap, update pesado o navegacion reiterada de varias capas:
   **aviso de modelo** antes (§6.3); esperar confirmacion o "sigo con el actual".
3. Comprobar `.navigator/` y capas habilitadas en `config.yaml`.
4. Si no hay navigator y la consulta lo necesita → **ofrecer bootstrap**; si el
   usuario no quiere → modo degradado (§14.5).
5. Elegir la **capa minima** (tabla 18.1.1); subir de capa solo si no basta.
6. Responder de forma concisa citando **fuente** (path de capa o `archivo:linea`).
7. Si hubo degradado: declarar capas ausentes y limite de confianza.
8. Si el proceso fue pesado: **aviso de modelo** final (§6.3).

#### 18.1.1 Clasificador pregunta → capa

| Tipo de pregunta | Capa inicial | Subir a si no basta |
| --- | --- | --- |
| Que es / proposito / como esta organizado | 0 `ai-context.md` | 1 |
| En que modulo esta / dependencias entre modulos | 1 `module-map.json` | 2 o 4 |
| Donde se define un simbolo / firma / metodos | 2 `symbols.json` (si existe) | 4 |
| Como se relaciona X con Y / impacto de cambiar Z | 3 grafo (si existe y `graph` on) | 1 + 4 |
| Detalle de implementacion | 4 codigo puntual (rango de lineas) | — |
| Bootstrap / indexar / actualizar navigator | Modo escritura en `.navigator/` | — |

Reglas:

- Preferir archivo + rango de lineas sobre leer directorios enteros.
- No volcar grafo ni `symbols.json` completos al contexto.
- No inventar entradas de indices; si faltan, degradar o proponer update.

#### Bootstrap asistido (contrato de pasos)

1. Aviso de modelo pequeno (§6.3).
2. Detectar lenguajes, build system y fuentes externas de contexto (hibrido Capa 0).
3. Crear `.navigator/` si no existe.
4. Escribir `config.yaml` minimo (§14.4).
5. Generar `ai-context.md` (~500 tokens) y `module-map.json`.
6. No bloquear si faltan `symbols` o grafo.
7. Respetar excludes y no indexar secretos (§14.12).
8. Informar: artefactos creados, fuentes externas detectadas, gaps, como consultar.
9. Aviso final de modelo (§6.3).

#### Update on_request (contrato)

- Solo cuando el usuario lo pida o acepte tras detectar desfase.
- Actualizar capas afectadas; no regenerar todo por defecto.
- Si `ai-context.md` tiene edicion manual evidente: preguntar antes de sobrescribir
  o fusionar conservando notas del usuario.
- Mantener `exclude` y politica de secretos.
- Avisos de modelo antes/despues si el update es pesado.

#### Formato de respuesta

- Conciso, orientado a la pregunta.
- Indicar **fuentes** (p. ej. `.navigator/ai-context.md`, `.navigator/module-map.json`,
  `src/foo.ts:42`).
- En degradado: `capas_ausentes` + confianza limitada.
- No rellenar con especulacion presentada como hecho indexado.

#### Relacion con otras skills del kit

- En bootstrap y Capa 0: leer best-effort secciones "Contexto para IA" de
  `.architecture/`, `.data/`, `.quality/`, `.security/`, `.design/` si existen.
- No sustituir a architecture, security, quality, data-api ni ui-design:
  solo navega e indexa para reducir tokens.
- Puede **senalar** que otra skill/agente es mas adecuada para documentar o remediar.

#### References previstos (al implementar en el kit)

```text
canonical/skills/project-navigator/
  SKILL.md
  references/
    layers.md
    bootstrap.md
    config.md
    sources.md
    templates/
      ai-context.template.md
      module-map.template.json
      config.template.yaml
```

### 18.2 Agente `project-navigator`

#### Rol

- Especialista de **investigacion y navegacion** del proyecto.
- Carga y sigue la skill `project-navigator`.
- Idioma: el del usuario (por defecto espanol en este kit).

#### Texto canonico previsto del agente (cuerpo futuro)

```markdown
# Project Navigator Agent

Navegas e investigas proyectos con minimo de tokens. Carga y sigue la skill
`project-navigator`: capas en `.navigator/`, bootstrap/update y modo degradado.

## Alcance inviolable

- Por defecto solo lectura del repositorio y de `.navigator/`.
- Escritura solo en `.navigator/` (y export opt-in a `AGENTS.md` con confirmacion)
  en bootstrap o update explicitos.
- No implementes features, no refactorices codigo de negocio, no toques CI ni Git remoto.
- No selecciones ni cambies el modelo del host; solo avisos segun la skill (§6).
- Si piden implementacion o trabajo fuera de navegacion/indexado: responde con
  ubicacion/mapa si ayuda, declara el limite y redirige al flujo o agente adecuado.
- Si agente y skill divergen, manda la skill.

## Ejecucion minima

1. Clasifica la peticion (consulta, bootstrap/update, fuera de alcance).
2. Aviso de modelo si el proceso es pesado; espera confirmacion o "sigo con el actual".
3. Aplica divulgacion progresiva (capas 0 → 4) y cita fuentes.
4. Bootstrap solo si no hay `.navigator/` y hace falta, o si el usuario lo pide.
5. Al cerrar un proceso pesado, aviso final de modelo.
```

#### UI e invocacion

| Aspecto | Valor |
| --- | --- |
| Id | `project-navigator` |
| Nombre visible | Project Navigator |
| Invocacion | `@project-navigator` o selector de agentes del host |
| Descripcion corta (UI) | Navegacion e investigacion del proyecto con minimo de tokens (`.navigator/`). Solo lectura por defecto; bootstrap/update de indices bajo peticion. |

#### Permisos previstos por plataforma (adapters futuros)

Principios comunes:

- Lectura/busqueda/listado: permitidos.
- Edicion: pedir confirmacion (`ask`) salvo que el host permita acotar a `.navigator/`.
- Bash: `ask` por defecto; patrones destructivos siempre con confirmacion (como el resto del kit).
- **No** incluir clave `model` en el frontmatter del agente.
- Webfetch: opcional; no requerido para el MVP de navegacion local.

OpenCode (orientativo, espejo del kit):

```json
{
  "description": "Navegacion e investigacion del proyecto con minimo de tokens (.navigator/). Solo lectura por defecto; bootstrap/update de indices bajo peticion. PROHIBIDO modificar codigo de negocio ni seleccionar el modelo del host.",
  "mode": "all",
  "temperature": 0.2,
  "permission": {
    "edit": "ask",
    "webfetch": "allow",
    "bash": {
      "*": "ask",
      "rm *": "ask",
      "rm -rf *": "ask",
      "git push*": "ask",
      "git reset --hard*": "ask",
      "git checkout -f*": "ask",
      "git clean*": "ask"
    }
  }
}
```

Copilot y Kiro: misma semantica de alcance; frontmatter/tools segun adapters
existentes del kit (sin fijar modelo).

### 18.3 Separacion skill vs agente

| Aspecto | Skill | Agente |
| --- | --- | --- |
| Procedimiento, capas, plantillas | Si (manda) | Sigue la skill |
| Visible en selector UI | No (o indirecto) | Si |
| Invocacion tipica | Al cargar el procedimiento | `@project-navigator` / selector |
| Modelo | Solo avisos §6 | Solo avisos §6 |
| Escritura | Solo `.navigator/` (+ export opt-in) | Igual, en bootstrap/update |

### 18.4 Criterios de aceptacion del contrato (cuando se implemente)

- [ ] Sin `.navigator/`, ofrece bootstrap y no explora el repo entero en silencio.
- [ ] Con capas 0–1, responde "que es" / "donde esta el modulo" sin leer todo el codigo.
- [ ] Cita fuentes de capa o `archivo:linea`.
- [ ] No escribe fuera de `.navigator/` (salvo export `AGENTS.md` confirmado).
- [ ] Emite avisos de modelo antes/despues en procesos pesados; nunca cambia el modelo.
- [ ] Fuera de alcance (implementar feature): rechaza implementar y aporta mapa si aplica.
- [ ] Modo degradado declara limites cuando faltan capas.

## 19. Plantillas, Schemas y Monorepo (MVP)

> Fuente de verdad de la forma de las capas 0 y 1. Al implementar, copiar a
> `canonical/skills/project-navigator/references/templates/`.

### 19.1 Plantilla `.navigator/ai-context.md`

Tamano objetivo: **~500 tokens**. Tope blando: **~700 tokens**. Preferir viñetas
densas; no copiar README enteros ni pegar secretos.

```markdown
# <Nombre del proyecto>

## Proposito
- Que es: <1-3 frases>
- Alcance: <que incluye>
- Fuera de alcance: <que no es / no cubre>

## Stack
- Lenguajes y frameworks: <...>
- Build / monorepo tool: <gradle, npm workspaces, melos, ...>
- Entrypoints: <paths clave, p. ej. app/main.ts, :app>

## Mapa rapido
- `<path o modulo>` → <responsabilidad en una frase>
- `<path o modulo>` → <...>
- (Detalle y dependencias: ver `module-map.json`; no duplicar el JSON aqui)

## Convenciones
- <solo las que afectan a navegar o editar: capas, naming, tests, paquetes>

## Docs y contexto externo
- `README.md` — <nota breve o "presente">
- `AGENTS.md` / `CLAUDE.md` / otras — <presente|ausente; no pegar contenido>
- Carpetas canonicas (`.architecture/`, `.data/`, ...) — <paths si existen>

## Riesgos y restricciones
- <areas delicadas, PII, no tocar sin cuidado>
- Secretos: nunca indexar `.env` ni claves (ver exclude)

## Meta
- Actualizado: <YYYY-MM-DD>
- Navigator root: <`.` o subpath del monorepo>
- Generado por: project-navigator bootstrap|update|manual
```

#### Reglas de generacion

1. Idioma del repo o del usuario.
2. No incluir valores de secretos, tokens, connection strings ni PII.
3. Referenciar paths de docs largas; no incrustarlas.
4. El mapa rapido es un resumen; la fuente de dependencias es `module-map.json`.
5. Listar fuentes externas detectadas (hibrido §4 Capa 0); no sobrescribirlas.
6. Si el contenido supera ~700 tokens, recortar convenciones y riesgos primero.

### 19.2 Schema `.navigator/module-map.json`

#### Contrato de campos

| Campo | Tipo | Obligatorio | Descripcion |
| --- | --- | --- | --- |
| `version` | number | Si | Schema version; MVP = `1` |
| `generated_at` | string (ISO-8601) | Si | Fecha/hora de generacion o update |
| `root` | string | Si | Root indexado relativo al repo (alineado a `config.project.root`) |
| `modules` | array | Si | Lista de unidades navegables |
| `modules[].id` | string | Si | Id estable unico (snake_case o path normalizado) |
| `modules[].name` | string | Si | Nombre legible |
| `modules[].path` | string | Si | Path relativo al `root` |
| `modules[].responsibility` | string | Si | Una frase |
| `modules[].kind` | string | Si | `app` \| `package` \| `service` \| `feature` \| `lib` \| `other` |
| `modules[].tech` | string[] | No | Tecnologias del modulo |
| `modules[].entrypoints` | string[] | No | Archivos o targets de entrada |
| `modules[].depends_on` | string[] | No | Ids de otros modulos (deben existir) |
| `modules[].tags` | string[] | No | Etiquetas libres |
| `modules[].notes` | string | No | Nota corta opcional |

#### Ejemplo minimo

```json
{
  "version": 1,
  "generated_at": "2026-08-04T12:00:00Z",
  "root": ".",
  "modules": [
    {
      "id": "app",
      "name": "App",
      "path": "app",
      "responsibility": "Aplicacion principal y composition root",
      "kind": "app",
      "tech": ["kotlin", "gradle"],
      "entrypoints": ["app/src/main"],
      "depends_on": ["core"],
      "tags": ["mobile"]
    },
    {
      "id": "core",
      "name": "Core",
      "path": "core",
      "responsibility": "Dominio compartido y utilidades",
      "kind": "lib",
      "tech": ["kotlin"],
      "entrypoints": [],
      "depends_on": []
    }
  ]
}
```

#### Reglas de generacion

1. `id` unico y estable entre updates (no renombrar sin necesidad).
2. Todo `depends_on` debe apuntar a un `id` existente en el mismo archivo.
3. MVP: unidades de primer nivel / features detectables; no explotar a miles de
   nodos archivo-a-archivo.
4. No listar `node_modules`, build outputs ni paths excluidos.
5. Si no hay dependencias claras, `depends_on: []` (no inventar).
6. `root` debe coincidir con el subarbol de esta instancia `.navigator/`.

`symbols.json` (Capa 2) queda **fuera** de este schema; se definira aparte.

### 19.3 Monorepo y ubicacion de `.navigator/`

Misma logica de deteccion que la skill `architecture` del kit.

#### Deteccion (antes de crear la carpeta)

Escanear raiz y subcarpetas de primer nivel (y contenedores tipicos `apps/`,
`packages/`, `services/`) buscando marcadores: `settings.gradle(.kts)`,
`build.gradle`, `package.json`, `pubspec.yaml`, `Cargo.toml`, `go.mod`,
`*.xcodeproj` / `*.xcworkspace`, `Podfile`, `pyproject.toml`, etc.

| Situacion | Donde crear `.navigator/` |
| --- | --- |
| Un solo producto o **agregador en la raiz** (workspaces, `settings.gradle` que incluye modulos, `pubspec` raiz, etc.) | **Una** en la **raiz del repo** |
| Varios productos/apps **independientes** sin agregador (p. ej. `backend/` + `mobile/`) | **Una por subproyecto** (`backend/.navigator/`, `mobile/.navigator/`) |
| Flutter / React Native / KMP con marcador en raiz | **Una en la raiz** (`android/` e `ios/` son plataformas del mismo producto) |
| Escaneo **ambiguo** | **Preguntar** al usuario antes de escribir |

#### Reglas

1. **Nunca mezclar** productos independientes en el mismo `module-map.json`.
2. Cada `.navigator/` indexa solo su subarbol (`config.project.root`).
3. En multi-navigator, cada uno tiene su `ai-context.md` y `module-map.json`.
4. Consultas: usar el `.navigator/` del subproyecto en contexto; si hay varios y
   no esta claro, preguntar.
5. `config.yaml` minimo por instancia:

```yaml
project:
  name: ""      # opcional
  root: .       # o "apps/mobile", etc., relativo al repo
```

### 19.4 Versionado y `.gitignore`

#### Versionar en git (recomendado)

- `.navigator/config.yaml`
- `.navigator/ai-context.md`
- `.navigator/module-map.json`
- `.navigator/symbols.json` — si existe y es estable
- `.navigator/graph/` — solo si es estable, util al equipo y **sin secretos**

#### No versionar

```gitignore
# project-navigator
.navigator/cache/
```

Opcional si el grafo es enorme o local-only:

```gitignore
.navigator/graph/
```

#### Regla

Nada bajo `.navigator/` debe contener secretos, `.env` ni PII. Si aparece,
omitir del artefacto y avisar (§14.12).

## 20. Schema `.navigator/symbols.json` (Capa 2)

> Capa **opt-in** (`layers.symbols: false` por defecto en `config.yaml`).
> MVP: generacion **best-effort** (asistida o con tools del lenguaje si hay).
> No se exige AST multi-lenguaje completo en el MVP (eso es post-MVP).

### 20.1 Rol

- Responder "donde se define X", firmas y tipos sin abrir el repo entero.
- Enlazar a `module-map` via `module_id` cuando se conozca.
- El detalle de implementacion sigue en Capa 4 (`file:line`).
- Relaciones call/import ricas → Capa 3 (grafo), no este archivo.

### 20.2 Contrato de campos

#### Raiz

| Campo | Tipo | Obligatorio | Descripcion |
| --- | --- | --- | --- |
| `version` | number | Si | Schema version; MVP = `1` |
| `generated_at` | string (ISO-8601) | Si | Fecha/hora de generacion o update |
| `root` | string | Si | Root indexado (alineado a config / module-map) |
| `symbols` | array | Si | Lista de simbolos |

#### Por simbolo

| Campo | Tipo | Obligatorio | Descripcion |
| --- | --- | --- | --- |
| `id` | string | Si | Id estable unico (p. ej. `path#Name` o `path:line:name`) |
| `name` | string | Si | Nombre del simbolo |
| `kind` | string | Si | `class` \| `function` \| `method` \| `interface` \| `type` \| `enum` \| `component` \| `endpoint` \| `other` |
| `file` | string | Si | Path relativo a `root` |
| `line` | number | Si | Linea de definicion (1-based) |
| `end_line` | number | No | Fin del simbolo si se conoce |
| `signature` | string | No | Firma publica corta |
| `module_id` | string | No | Id de `module-map.json` si se conoce |
| `summary` | string | No | Una frase |
| `exported` | boolean | No | Si es API publica / exportada |
| `tags` | string[] | No | Etiquetas libres |

**Fuera de este schema (MVP):** cuerpos de funcion, AST completo, lista exhaustiva
de callers/callees (usar grafo o codigo puntual).

### 20.3 Ejemplo minimo

```json
{
  "version": 1,
  "generated_at": "2026-08-04T12:00:00Z",
  "root": ".",
  "symbols": [
    {
      "id": "app/src/main/AuthService.kt#AuthService",
      "name": "AuthService",
      "kind": "class",
      "file": "app/src/main/AuthService.kt",
      "line": 12,
      "signature": "class AuthService(private val client: ApiClient)",
      "module_id": "app",
      "summary": "Autenticacion y sesion de usuario",
      "exported": true,
      "tags": ["auth"]
    },
    {
      "id": "app/src/main/AuthService.kt#login",
      "name": "login",
      "kind": "method",
      "file": "app/src/main/AuthService.kt",
      "line": 28,
      "signature": "suspend fun login(user: String, pass: String): Result<Session>",
      "module_id": "app",
      "summary": "Login contra API",
      "exported": true
    },
    {
      "id": "core/src/Session.kt#Session",
      "name": "Session",
      "kind": "class",
      "file": "core/src/Session.kt",
      "line": 4,
      "signature": "data class Session(val token: String, val userId: String)",
      "module_id": "core",
      "summary": "Sesion autenticada",
      "exported": true
    }
  ]
}
```

### 20.4 Reglas de generacion

1. Opt-in: solo si `layers.symbols: true` o el usuario pide indexar simbolos.
2. Preferir simbolos **publicos / entrypoints** sobre privados masivos.
3. Priorizar por modulos del `module-map`; no indexar deps, build ni excludes.
4. `id` estable entre updates; no renombrar sin necesidad.
5. Si no hay confianza en `file`+`line`, **omitir** el simbolo (no inventar).
6. No copiar secretos, literals sensibles ni cuerpos completos a `summary`/`signature`.
7. Bootstrap asistido puede generar un subconjunto util; cobertura total no es meta del MVP.
8. Update on_request: regenerar afectados o el archivo completo si el usuario lo pide.

### 20.5 Reglas de consulta

1. **Nunca** volcar `symbols.json` entero al contexto del modelo.
2. Filtrar por `name`, prefijo, `module_id` o path; devolver solo hits relevantes.
3. Tras localizar el simbolo, si hace falta detalle → Capa 4 en `file:line` (rango acotado).
4. Si la capa esta deshabilitada o el archivo no existe → degradar a busqueda en
   codigo (Capa 4) y declarar que Capa 2 no esta disponible.

### 20.6 Relacion con otras capas

| Necesidad | Capa |
| --- | --- |
| Que es el proyecto | 0 `ai-context` |
| En que modulo vive | 1 `module-map` (`module_id`) |
| Donde se define el simbolo | 2 `symbols` |
| Quien llama / impacto amplio | 3 grafo (si existe) |
| Como esta implementado | 4 codigo en `file:line` |

### 20.7 Post-MVP (no bloquea)

- Extraccion determinista por AST / SCIP / LSIF / tools nativas por lenguaje.
- Cobertura y verificacion automatica de ids huerfanos.
- Enriquecer con `implements` / `overrides` solo si es barato y fiable.

## 21. Presupuesto de Tokens (MVP)

> Objetivos blandos para no reventar costo/contexto. No son hard-fail del host:
> si se superan, **recortar**, subir de capa con rango acotado o declarar
> degradado. Nunca “leer el repo entero” para compensar.

### 21.1 Artefactos persistentes (tamano objetivo)

| Artefacto | Objetivo | Tope blando | Accion si se pasa |
| --- | --- | --- | --- |
| `ai-context.md` | ~500 tokens | ~700 | Recortar convenciones y riesgos (§19.1) |
| `module-map.json` (serializado) | ~1–2k tokens | ~4k | Menos modulos o responsibilities mas cortas |
| Respuesta de consulta tipica | ~200–600 tokens | ~1k | Solo lo pedido + fuentes |
| Hits de `symbols` por consulta | top 5–15 simbolos | 25 | Filtrar mas; no dump del JSON |
| Subgrafo / path (si Capa 3) | ~500–1.5k tokens | ~2.5k | Acotar profundidad/nodos |
| Lectura Capa 4 (codigo) | ~80–150 lineas | ~250 lineas o ~2k tokens | Pedir rango mas preciso |

Los tokens de artefactos se miden de forma aproximada (~4 chars ≈ 1 token) al
generar; no hace falta un contador exacto en el MVP.

### 21.2 Bootstrap asistido (sesion)

| Fase | Presupuesto orientativo | Notas |
| --- | --- | --- |
| Deteccion de stack y fuentes externas | Bajo (listados + headers) | No leer arboles completos |
| Lectura para Capa 0 | Preferir README + Contexto para IA + manifests | Max ~3–5 docs cortos de entrada |
| Generacion `ai-context` + `module-map` | Salida acotada a topes §21.1 | Una pasada; no re-explorar |
| Symbols (si opt-in) | Subconjunto util, no cobertura total | Priorizar entrypoints / public API |
| Graph (si opt-in) | Fuera del presupuesto MVP core | Provider externo; no bloquear bootstrap |
| **Total sesion bootstrap tipica** | **Objetivo: menos de ~30–50k tokens** in+out | Repos enormes: acotar `project.root` o modo lite |

Si el repo es muy grande: indexar solo el `project.root` acordado, o pedir al
usuario que elija subproyecto (§19.3).

### 21.3 Consulta / navegacion (por pregunta)

Orden de gasto (de barato a caro):

1. Capa 0 (~500) → 2. Capa 1 (fragmento del map) → 3. Capa 2 (hits) →
4. Capa 3 (subgrafo) → 5. Capa 4 (rango de codigo).

| Regla | Valor |
| --- | --- |
| Empezar siempre por la capa minima (§18.1.1) | Obligatorio |
| Max capas distintas por pregunta (salvo que el usuario pida profundidad) | 2–3 |
| Max archivos de codigo abiertos por pregunta | 1–3 |
| Dump de `module-map` / `symbols` / grafo completo | Prohibido |
| Objetivo de reduccion vs explorar el repo sin navigator | ≥ 90% en onboarding tipico (§13) |

### 21.4 Update on_request

- Preferir regenerar **solo capas/modulos afectados**.
- Evitar re-leer el repo completo si el desfase es local.
- Si el update seria mas caro que un bootstrap acotado, proponer bootstrap
  parcial del `root` y pedir confirmacion.

### 21.5 Principio

> El presupuesto se cumple con **divulgacion progresiva y artefactos densos**,
> no con un modelo mas grande. Si no cabe en el tope, se reduce alcance y se
> declara; no se silencia el sobrecoste explorando mas codigo.
