---
name: architecture
description: >-
  Documenta y mantiene la ARQUITECTURA de cualquier proyecto (agnóstica a la
  tecnología) en una carpeta canónica `.architecture/`, para dar contexto rápido
  y confiable a la IA y al equipo. Combina, en modo ligero, la estructura arc42,
  diagramas C4 en Mermaid y ADRs (registro de decisiones). Detecta el tamaño del
  proyecto (modo lite/full), sincroniza con el historial de git de forma
  incremental y lleva "deuda técnica de arquitectura" priorizada por severidad.
  Úsala al documentar, auditar o entender la arquitectura: módulos, capas,
  dependencias, patrones, decisiones, diagramas, contexto del sistema.
---

# Skill: Architecture (documentación de arquitectura para IA y equipo)

Esta skill es la **referencia canónica** para documentar y mantener la
arquitectura de un proyecto, sin importar la tecnología. Su objetivo es que
**cualquier agente o persona** encuentre en `.architecture/` un contexto
predecible del sistema y trabaje más rápido. Complementa al agente `Architecture
Agent`. Si el agente y esta skill divergen, **manda esta skill**.

> **Regla de alcance (inviolable):** esta skill **documenta, audita y recomienda**
> arquitectura. NO modifica código de negocio ni ejecuta refactors. Solo escribe
> dentro de `.architecture/`. Si piden cambios de código, decláralo y detente.

## Cuándo usar esta skill

- Documentar la arquitectura: módulos, capas, límites, dependencias, patrones,
  contenedores/servicios y decisiones.
- Dar contexto del proyecto a la IA antes de una feature, refactor o auditoría.
- Registrar y consultar **decisiones** (ADRs) y su justificación.
- Auditar la arquitectura y registrar **deuda técnica** priorizada.
- Sincronizar la documentación tras cambios estructurales en el repositorio.

## Estándares que aplica (modo ligero)

- **arc42** → estructura del documento (solo secciones con contenido real).
- **C4 model** en **Mermaid** → diagramas por capas: Contexto (C1), Contenedores
  (C2) y Componentes (C3). Se omite C4/Code salvo casos puntuales.
- **ADR** (Architecture Decision Records) → un archivo por decisión importante.

## Carpeta canónica: `.architecture/`

Toda la documentación de arquitectura vive en una carpeta `.architecture/`
(oculta, estilo `.github/`) que **se versiona** con el repo. La skill SIEMPRE
trabaja aquí; si no existe, **créala**.

### Ubicación: uno o varios proyectos

**Detección (primera vez, antes de crear la carpeta):** escanea las subcarpetas
de primer nivel —y contenedores típicos de monorepo como `apps/`, `packages/`,
`services/`— buscando marcadores de proyecto: `settings.gradle(.kts)` /
`build.gradle` (Android/JVM), `*.xcodeproj` / `*.xcworkspace` / `Podfile` (iOS),
`pubspec.yaml` (Flutter), `package.json` (JS/TS).

- **Un solo proyecto** — hay un **agregador en la raíz** (p. ej. `settings.gradle`
  que incluye los módulos, `package.json` con workspaces, o un `pubspec.yaml`
  raíz), o todo el repo es un mismo producto multi-módulo → **una**
  `.architecture/` en la **raíz del repositorio**.
- **Varios proyectos/apps independientes** — los marcadores aparecen en
  **subcarpetas hermanas sin agregador en la raíz** (p. ej. `backend/` y
  `mobile/`, o `android/` e `ios/` como apps nativas separadas) → una
  `.architecture/` **dentro de cada proyecto** (`<proyecto>/.architecture/`),
  sincronizada solo con su subárbol. **Nunca mezcles** proyectos distintos.
- ⚠️ **Excepción Flutter / React Native / KMP:** si en la **raíz** hay
  `pubspec.yaml` (Flutter) o `package.json` con `react-native`, `android/` e
  `ios/` son **plataformas de un mismo proyecto** → una sola `.architecture/`
  en la raíz.
- Si el escaneo es **ambiguo**, **pregunta** antes de escribir (recomendado: una
  por proyecto para apps nativas separadas).

## Dos modos según el tamaño del proyecto

La skill detecta el tamaño (nº de módulos, servicios, archivos, dependencias) y
**propone** el modo; el usuario confirma.

### Modo `lite` (proyectos pequeños)
Un solo módulo / equipo reducido. Estructura mínima:
```
.architecture/
├── README.md          # Estado de sincronización + Contexto para IA + arc42 mínimo + C4 Contexto
└── decisions/         # ADRs puntuales (opcional, solo decisiones que duelen olvidar)
    └── 0001-*.md
```
En lite no hay `arch-tech-debt.md`: la **deuda técnica** va en una sección
`## Deuda técnica` dentro del `README.md` (créala solo si hay hallazgos). Si la
deuda crece, promueve el proyecto a modo `full`.

### Modo `full` (proyectos medianos/grandes)
Multi-módulo, varios servicios o equipo. Estructura completa:
```
.architecture/
├── README.md                 # Índice + Estado de sincronización + Contexto para IA
├── 01-overview.md            # Objetivos, alcance, restricciones (arc42 §1–2)
├── 02-context.md             # C4 Contexto (C1): sistema y actores externos
├── 03-containers.md          # C4 Contenedores (C2): apps, servicios, datos
├── 04-components.md          # C4 Componentes (C3) de los contenedores clave
├── 05-runtime.md             # Flujos/secuencias importantes (Mermaid sequence)
├── 06-deployment.md          # Despliegue e infraestructura (si aplica)
├── 07-crosscutting.md        # Conceptos transversales: seguridad, errores, i18n, logging
├── 08-quality-risks.md       # Atributos de calidad y riesgos
├── glossary.md               # Glosario
├── decisions/                # ADRs
│   └── 0001-*.md
└── arch-tech-debt.md         # Deuda técnica de arquitectura priorizada
```

## Detección de tecnología (dónde vive la arquitectura)

| Tecnología | Dónde inferir la arquitectura |
|------------|-------------------------------|
| Android (multi-módulo/Gradle) | `settings.gradle(.kts)`, módulos `:app`/`:core`/`:feature`, capas domain/data/ui, Hilt/DI |
| iOS | targets/frameworks, Swift Packages, capas y coordinadores |
| Flutter | `pubspec.yaml`, capas (data/domain/presentation), gestión de estado |
| Backend (JVM/Node/Go/…) | módulos/paquetes, capas (controller/service/repo), puntos de entrada, config de despliegue |
| Web/Front | estructura de features, routing, state management, build |
| Monorepo | `package.json` workspaces, Nx/Turbo/Gradle includes, límites entre paquetes |

Fuentes de verdad transversales: archivos de build/deps, DI/inyección, capas de
carpetas, puntos de entrada (`main`, `Application`, `index`), configuración de
red/datos y CI. Cita siempre `archivo:línea`. No inventes.

## Flujo de trabajo

### 0. Estudio y propuesta (antes de escribir en masa)
Al invocarse por primera vez (o cuando no exista `.architecture/`), NO generes
todo de golpe. Primero:
1. Escanea la estructura, detecta tecnología y **tamaño** (propón modo lite/full).
2. Entrega un **resumen** de la arquitectura observada (módulos, capas,
   dependencias, patrones, decisiones implícitas) y **recomendaciones
   priorizadas** de qué documentar primero.
3. Pregunta qué generar (todo o por bloques) y **espera confirmación**.

### 1. Localizar / crear `.architecture/`
Créala en la ubicación resultante de *"Ubicación: uno o varios proyectos"* (raíz
o una por proyecto) y según el modo confirmado. `.architecture/` se versiona; no
metas binarios.

### 2. Leer el estado de sincronización
En `.architecture/README.md` hay una sección **"Estado de sincronización"** con
el último commit documentado (hash + fecha), tecnología y modo. Léela.

### 3. Revisar el historial de git (incremental)
- Con marca: `git log <hash>..HEAD --name-only` y filtra rutas estructurales
  (build/deps, módulos, capas, config de red/datos, DI, CI, puntos de entrada).
  Usa `git diff <hash>..HEAD -- <rutas>` para ver cambios concretos.
- **Multi-proyecto:** acota el escaneo al subárbol del proyecto, p. ej.
  `git log <hash>..HEAD -- <proyecto>/`; cada `.architecture/` sincroniza solo
  su propia carpeta.
- Sin marca (primera vez): barrido completo de la estructura.
- Sin git (no es repo o sin commits): barrido completo y marca por **fecha**.
- Solo git de **lectura** (`git log`, `git diff`, `git show`).

### 4. Extraer y actualizar la documentación
Actualiza los `.md` afectados y los diagramas C4. Documenta lo real Y lo
mejorable (esto último como deuda). Detecta **decisiones implícitas** en el
código y propón redactar el ADR faltante.

### 5. Registrar deuda técnica de arquitectura
Actualiza `arch-tech-debt.md` (o la sección `## Deuda técnica` del `README.md` en
modo lite) con hallazgos priorizados por severidad.

### 6. Actualizar la marca de sincronización
Escribe el hash de `HEAD` (o la fecha) y la tecnología/modo en `README.md`.

## Índice de contexto para otros agentes

`.architecture/README.md` incluye una sección **"Contexto para IA"**: un resumen
denso (qué es el sistema, capas, módulos, límites, patrones, dónde vive cada
cosa, enlaces a ADRs clave). Es el **punto de entrada** que otros agentes leen al
iniciar en el proyecto para orientarse rápido antes de tocar nada.

## Referencias bajo demanda

Las plantillas completas y criterios de clasificación están en
[`references/templates.md`](references/templates.md). Ábrela solo al crear o
actualizar el artefacto correspondiente; no es necesaria para una consulta,
triage o tarea puntual.

## Reglas

- Comunícate en español por defecto; si el usuario escribe en otro idioma o lo
  pide, adáptate. Sé claro y conciso.
- Solo arquitectura/documentación: nunca modifiques código de negocio ni ejecutes
  refactors; recomienda y registra en deuda.
- No expongas secretos, tokens ni credenciales.
- Cita `archivo:línea` como fuente de verdad; no inventes.
- Mantén los diagramas C4 al día; si un cambio los desactualiza, corrígelos.
- git solo de lectura.
