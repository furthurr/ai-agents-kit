---
name: data-api
description: >-
  Documenta, audita y ayuda a desarrollar TODO lo relacionado con DATOS y APIs de
  cualquier proyecto (agnóstica a la tecnología) en una carpeta canónica `.data/`.
  Cubre catálogo de endpoints, modelos/DTOs y su mapeo, contratos (OpenAPI, JSON
  Schema, y condicionalmente GraphQL, AsyncAPI, gRPC), esquema de datos con
  diagramas ER en Mermaid, campos sensibles/PII y convenciones (auth, errores,
  paginación, timeouts, reintentos, entornos). Detecta el tamaño y la persistencia
  (modo lite/full; omite ER si no hay BD interna), sincroniza con el historial de
  git de forma incremental y lleva "deuda técnica de datos/APIs" priorizada por
  severidad. Úsala al trabajar datos, APIs, endpoints, DTOs, contratos, modelos,
  repositorios, clientes de red, serialización o integración de servicios.

---

# Skill: Data & API (datos, APIs y contratos)

Esta skill es la **referencia canónica** para documentar, auditar y ayudar a
desarrollar la **capa de datos y APIs** de un proyecto, sin importar la
tecnología. Su objetivo es que cualquier agente o persona encuentre en `.data/`
un contrato claro de qué datos entran/salen y cómo. Complementa al agente `Data &
API Agent`. Si el agente y esta skill divergen, **manda esta skill**.

> **Regla de alcance (inviolable):** esta skill trabaja SOLO la **capa de datos y
> APIs** (DTOs, modelos, contratos, clientes de red, repositorios, mappers,
> serialización, esquema de datos). NO toca UI ni lógica de presentación, y no se
> mete con negocio ajeno a datos. Si aparece algo fuera de este alcance,
> decláralo y detente.

## Cuándo usar esta skill

- Documentar endpoints consumidos/expuestos, modelos/DTOs y sus mapeos.
- Definir o auditar contratos de API y esquemas de datos.
- Ayudar a desarrollar la capa de datos: DTOs, clientes de red, repositorios,
  mappers, serialización, caché.
- Registrar campos sensibles/PII y convenciones (auth, errores, paginación…).
- Auditar y registrar **deuda técnica** de datos/APIs.
- Sincronizar la documentación tras cambios en la capa de datos.

## Estándares que reconoce

**Núcleo (siempre que aplique):**
- **OpenAPI (REST)** → contrato de endpoints. Si el backend ya tiene uno, se
  **referencia**; no lo reescribas. Si no hay, mantén un **catálogo de endpoints**
  equivalente desde el lado del cliente.
- **JSON Schema** → forma y validación de modelos/DTOs.
- **Diagramas ER en Mermaid** (`erDiagram`) → solo si hay **persistencia interna**
  (Room/SQLite/Core Data/Realm/…). Si no hay BD interna, **se omite**.

**Soporte condicional (solo si se detecta en el proyecto):**
- **GraphQL SDL** (si hay GraphQL) · **AsyncAPI** (si hay eventos/colas/streaming)
  · **gRPC/Protobuf** (si hay `.proto`).

## Carpeta canónica: `.data/`

Toda la documentación de datos/APIs vive en una carpeta `.data/` (oculta, estilo
`.github/`) que **se versiona** con el repo. La skill SIEMPRE trabaja aquí; si no
existe, **créala**. **Nunca** incluyas secretos, tokens, credenciales ni dominios
productivos reales: usa **placeholders**.

### Ubicación: uno o varios proyectos

**Detección (primera vez, antes de crear la carpeta):** escanea las subcarpetas
de primer nivel —y contenedores típicos de monorepo como `apps/`, `packages/`,
`services/`— buscando marcadores de proyecto: `settings.gradle(.kts)` /
`build.gradle` (Android/JVM), `*.xcodeproj` / `*.xcworkspace` / `Podfile` (iOS),
`pubspec.yaml` (Flutter), `package.json` (JS/TS).

- **Un solo proyecto** — hay un **agregador en la raíz** (p. ej. `settings.gradle`
  que incluye los módulos, `package.json` con workspaces, o un `pubspec.yaml`
  raíz), o todo el repo es un mismo producto multi-módulo → **una** `.data/` en la
  **raíz del repositorio**.
- **Varios proyectos/apps independientes** — los marcadores aparecen en
  **subcarpetas hermanas sin agregador en la raíz** (p. ej. `backend/` y
  `mobile/`, o `android/` e `ios/` como apps nativas separadas) → una `.data/`
  **dentro de cada proyecto** (`<proyecto>/.data/`), sincronizada solo con su
  subárbol. **Nunca mezcles** proyectos distintos.
- ⚠️ **Excepción Flutter / React Native / KMP:** si en la **raíz** hay
  `pubspec.yaml` (Flutter) o `package.json` con `react-native`, las carpetas
  `android/` e `ios/` son **plataformas de un mismo proyecto** → una sola `.data/`
  en la raíz.
- Si el escaneo es **ambiguo**, **pregunta** antes de escribir (recomendado: una
  por proyecto para apps nativas separadas).

## Dos modos según tamaño y persistencia

La skill detecta tamaño (nº de endpoints, fuentes de datos) y si hay **BD
interna**, y **propone** el modo; el usuario confirma.

### Modo `lite` (proyectos pequeños / cliente móvil sin BD interna)
```
.data/
└── README.md     # Contexto para IA + catálogo de endpoints + modelos/DTOs
                  # + mapeo a dominio + campos sensibles/PII + deuda técnica
```
Si NO hay persistencia interna, **omite la sección de ER/esquema**. En lite no hay
`data-tech-debt.md`: la **deuda técnica** va en una sección `## Deuda técnica`
dentro del `README.md` (créala solo si hay hallazgos). Si la deuda crece, promueve
el proyecto a modo `full`.

### Modo `full` (medianos/grandes o con persistencia/múltiples fuentes)
```
.data/
├── README.md                 # Índice + Estado de sincronización + Contexto para IA
├── 01-endpoints.md           # Catálogo de endpoints (o referencia al OpenAPI)
├── 02-models.md              # Modelos/DTOs, tipos, validaciones (JSON Schema)
├── 03-mapping.md             # Mapeo DTO ↔ dominio (transformaciones)
├── 04-schema.md              # Esquema de datos + ER en Mermaid (solo si hay BD)
├── 05-conventions.md         # Auth, errores/estados, paginación, timeouts, reintentos, versionado
├── 06-sensitive-data.md      # Campos sensibles/PII, cifrado, almacenamiento (sin valores)
├── 07-environments.md        # Entornos y endpoints con placeholders
├── contracts/                # OpenAPI/GraphQL/AsyncAPI/proto detectados o referenciados
└── data-tech-debt.md         # Deuda técnica de datos/APIs priorizada
```

## Detección de tecnología (dónde vive la capa de datos)

| Tecnología | Dónde inferir datos/APIs |
|------------|--------------------------|
| Android | Retrofit/Ktor/OkHttp interfaces, `@GET/@POST`, DTOs, repositorios, Room (`@Entity/@Dao`), DataStore, serialización (Moshi/Gson/kotlinx) |
| iOS | `URLSession`/Alamofire, `Codable` models, Core Data, repositorios |
| Flutter | `http`/`dio`, modelos `fromJson/toJson`, repos, `sqflite`/Drift/Isar |
| Backend | controllers/routers, DTOs/entidades, ORM/migraciones, esquema BD, OpenAPI |
| Web/Front | clients/`fetch`/axios, tipos/DTOs, GraphQL queries, esquemas |

Fuentes de verdad: interfaces de red, modelos serializables, repos, entidades de
BD/migraciones, configuración de endpoints y contratos existentes. Cita
`archivo:línea`. No inventes payloads ni respuestas: si un dato no está en el
código, decláralo.

## Flujo de trabajo

### 0. Estudio y propuesta (antes de escribir en masa)
Al invocarse por primera vez (o si no existe `.data/`), NO generes todo de golpe:
1. Escanea la capa de datos, detecta tecnología, contratos presentes, si hay **BD
   interna** y el tamaño → **propón modo lite/full**.
2. Entrega un **resumen** (qué APIs consume/expone, modelos, fuentes de datos,
   campos sensibles detectados) y **recomendaciones priorizadas** de qué
   documentar primero.
3. Pregunta qué generar y **espera confirmación**.

### 1. Localizar / crear `.data/`
Créala en la ubicación resultante de *"Ubicación: uno o varios proyectos"* (raíz o
una por proyecto) y según el modo confirmado. Versionada, sin secretos.

### 2. Leer el estado de sincronización
En `.data/README.md`, sección **"Estado de sincronización"** (último commit
documentado, tecnología, modo, si hay BD). Léela. Si existe, lee también
`.architecture/README.md` ("Contexto para IA") **best-effort** para ubicar la
capa de datos; si no existe, continúa sin él.

### 3. Revisar el historial de git (incremental)
- Con marca: `git log <hash>..HEAD --name-only` filtrando rutas de datos/APIs
  (network, api, dto, model, repository, entity, dao, schema, migration, proto,
  graphql, openapi). `git diff <hash>..HEAD -- <rutas>` para el detalle.
- **Multi-proyecto:** acota el escaneo al subárbol del proyecto, p. ej.
  `git log <hash>..HEAD -- <proyecto>/`; cada `.data/` sincroniza solo su carpeta.
- Sin marca (primera vez): barrido completo de la capa de datos.
- Sin git: barrido completo con marca por **fecha**.
- Solo git de **lectura**.

### 4. Extraer y actualizar la documentación
Actualiza los `.md` afectados: endpoints, modelos/DTOs, mapeos, ER (si aplica),
convenciones y datos sensibles. Documenta lo real Y lo mejorable (deuda).

### 5. Registrar deuda técnica de datos/APIs
Actualiza `data-tech-debt.md` (o la sección `## Deuda técnica` del `README.md` en
modo lite) con hallazgos priorizados por severidad.

### 6. Actualizar la marca de sincronización
Escribe el hash de `HEAD` (o fecha), tecnología, modo y flag de BD en `README.md`.

## Índice de contexto para otros agentes

`.data/README.md` incluye una sección **"Contexto para IA"**: resumen denso de
qué APIs consume/expone la app, modelos clave, fuentes de datos, auth y campos
sensibles. Es el punto de entrada que otros agentes leen para orientarse.

## Referencias bajo demanda

Las plantillas completas y criterios de clasificación están en
[`references/templates.md`](references/templates.md). Ábrela solo al crear o
actualizar el artefacto correspondiente; no es necesaria para una consulta,
triage o tarea puntual.

## Reglas

- Comunícate en español por defecto; si el usuario escribe en otro idioma o lo
  pide, adáptate. Sé claro y conciso.
- Solo capa de datos/APIs: nunca toques UI ni negocio ajeno a datos.
- **Seguridad primero:** nunca expongas secretos, tokens, credenciales ni
  dominios productivos reales; usa placeholders. Marca la PII. Los **hallazgos de
  riesgo de seguridad** (cifrado débil, TLS, fugas) se **derivan al Security Agent**.
- Cita `archivo:línea` como fuente de verdad; no inventes payloads ni respuestas.
- Mantén los diagramas ER y contratos al día; corrige si un cambio los desactualiza.
- git solo de lectura.
