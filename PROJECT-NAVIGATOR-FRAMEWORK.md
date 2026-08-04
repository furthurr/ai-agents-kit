# Project Navigator Framework

> Framework agnostico para crear una skill y un agente que permitan a una IA
> comprender y navegar cualquier proyecto con el minimo consumo de tokens.
>
> Estado: planificacion (definicion avanzada; MVP acotado)
> Ultima actualizacion: 2026-08-03
> Implementacion: pendiente — siguiente paso: contratos SKILL.md y agente
>
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
deterministica.

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

### Decision actual

Se recomendara inicialmente un modelo rapido y economico de la categoria de
Claude Haiku para el sub-agente, porque las tareas principales son navegacion,
clasificacion, busqueda y sintesis de informacion ya indexada.

Esta recomendacion no sera una dependencia obligatoria. El usuario podra
configurar el modelo que prefiera a nivel global o por proyecto.

### Deuda de investigacion: OpenAI, MiniMax y otros proveedores

Antes de implementar, se debe investigar y documentar:

- Como funciona la configuracion de modelos de OpenCode con una cuenta OpenAI.
- Como funciona con una cuenta MiniMax.
- Como funciona con Anthropic, OpenCode Zen y otros proveedores compatibles.
- Que modelos concretos estan disponibles para cada proveedor.
- Como configurar un modelo distinto para el sub-agente sin forzar Haiku.
- Si el sub-agente debe heredar el modelo principal cuando no exista uno
  configurado.
- Que fallback usar si el modelo configurado no esta disponible o faltan
  credenciales.
- Recomendaciones de modelo por costo, velocidad, ventana de contexto y
  calidad de razonamiento.
- Si la instalacion debe permitir seleccionar modelo de forma interactiva.

Principio:

> El framework no debe depender de un proveedor ni de un modelo especifico.
> Haiku es una recomendacion inicial, no un requisito.

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

La estructura final y que artefactos deben versionarse permanecen pendientes.

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
5. Generar el mapa de modulos.
6. Generar el indice de simbolos.
7. Construir el knowledge graph si esta habilitado.
8. Validar cobertura, consistencia y fechas de actualizacion.
9. Informar al usuario que se genero, que falta, que fuentes externas se
   detectaron y como operar el sistema.
10. Opcional (opt-in): ofrecer exportar un resumen compatible a `AGENTS.md`.

Indicadores iniciales de tecnologia que eventualmente podrian detectarse:

| Tecnologia | Indicadores posibles |
| --- | --- |
| Node.js | `package.json`, lockfiles |
| Python | `pyproject.toml`, `requirements.txt` |
| Java/Kotlin | `build.gradle`, `pom.xml` |
| Flutter/Dart | `pubspec.yaml` |
| Rust | `Cargo.toml` |
| Go | `go.mod` |
| Swift/iOS | `Package.swift`, `.xcodeproj` |
| .NET | `.csproj`, `.sln` |

Los lenguajes y frameworks incluidos en el MVP son una decision pendiente.

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

### Deuda de definicion cross-platform

- Elegir dependencia principal: Python, Node.js, binarios o Docker.
- Definir estrategia de instalacion en Windows nativo.
- Definir si WSL recibe soporte opcional o recomendado.
- Definir como se distribuyen dependencias.
- Definir si el instalador puede instalar dependencias automaticamente.
- Definir manejo de permisos, hooks y finales de linea de Git en Windows.
- Definir politica ante dependencias faltantes: degradar o fallar.

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

### 14.9 Modelos — DECISION PARCIAL

| Rol | Recomendacion | Notas |
| --- | --- | --- |
| Disenar/editar el framework | Modelo fuerte (p. ej. Grok 4.5, Claude Sonnet/Opus) | Decisiones y contratos |
| Implementar skill/agente/scripts | Modelo de coding agentic (p. ej. Grok Build 0.1) | Iteracion de codigo |
| Sub-agente `project-navigator` en runtime | Modelo rapido/economico (Haiku-class, Grok Build, o similar) | Navegacion sobre indices ya hechos |
| Sin modelo configurado | Heredar el modelo de la sesion/host | No fallar |
| Proveedor | Agnostico | Nunca hardcodear un vendor en la skill |

Pendiente documentar en `docs/providers-and-models.md` la matriz exacta por
cuenta (OpenAI, MiniMax, Anthropic, xAI, OpenCode Zen).

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

- Matriz detallada de proveedores/modelos por cuenta y fallback de credenciales.
- Contrato completo linea a linea de `SKILL.md` y del agente (prompts finales).
- Schema JSON formal de `module-map.json` y `symbols.json`.
- Adapter concreto `graphify` (mapeo `graphify-out/` → `.navigator/graph/`).
- Estrategia AST por lenguaje para Capa 2.
- Politica fina de que partes del grafo se versionan en monorepos grandes.
- Presupuesto de tokens numerico para bootstrap automatico vs asistido.
- Ejemplos por tipo de proyecto (mobile/backend/frontend).

### 15.2 Resuelto en esta ronda

- Distribucion via AI Agents Kit.
- Alcance MVP (skill + agente + bootstrap asistido + capas 0/1).
- Artefactos obligatorios/opcionales.
- Contrato minimo de `config.yaml`.
- Modo degradado.
- Grafo opt-in; graphify como candidato adapter.
- UI del agente via adapters del kit.
- Mantenimiento manual/on_request en MVP.
- Cross-platform orientado a Python del kit.
- Seguridad minima de exclusiones.

## 16. Proximos Pasos

1. Disenar contrato de `canonical/skills/project-navigator/SKILL.md`.
2. Disenar contrato de `canonical/agents/project-navigator.md`.
3. Definir schemas de `module-map.json` y plantilla de `ai-context.md`.
4. Anadir adapters (OpenCode, Copilot, Kiro) y entrada en `manifest.json`.
5. Render + validate + install de prueba.
6. Probar bootstrap asistido en un repo real sin `.navigator/`.
7. (Post-MVP) scripts deterministas y adapter graphify.

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
| Modelo runtime del sub-agente | Rapido/economico, configurable; hereda si falta |
| Modelo para construir el framework | Fuerte (diseno) + coding (implementacion) |
| Matriz proveedores/cuentas | Pendiente |
| Contratos SKILL.md / agente | Pendiente (siguiente paso) |
| Schemas JSON de capas | Pendiente |
| Automatizacion hooks/CI | Post-MVP |
