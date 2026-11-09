## Carpeta canónica: `.data/`

Toda la documentación de datos/APIs autorizada vive en una carpeta `.data/`
(oculta, estilo `.github/`) que **se versiona** con el repo. Las consultas y las
implementaciones de producto no requieren crearla. Créala solo si está incluida
en el plan documental aprobado. **Nunca** incluyas secretos, tokens, credenciales ni
dominios productivos reales: usa **placeholders**.

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

## Flujo de trabajo

### 0. Estudio y propuesta (antes de escribir en masa)
Solo para una operación documental solicitada (o un estudio pedido). Una consulta
puntual o una implementación de producto no inicia este preflight de escritura.
NO generes toda la documentación de golpe:
1. Escanea la capa de datos, detecta tecnología, contratos presentes, si hay **BD
   interna** y el tamaño → **propón modo lite/full**.
2. Entrega un **resumen** (qué APIs consume/expone, modelos, fuentes de datos,
   campos sensibles detectados) y **recomendaciones priorizadas** de qué
   documentar primero.
3. Pregunta qué generar y **espera confirmación**.

### 1. Localizar / crear `.data/`
Si el plan documental aprobado incluye crearla y no existe, créala en la ubicación
resultante de *"Ubicación: uno o varios proyectos"* (raíz o una por proyecto) y
según el modo confirmado. Versionada, sin secretos.

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

## Referencias bajo demanda

Las plantillas completas y criterios de clasificación están en
[`references/templates.md`](references/templates.md). Ábrela solo al crear o
actualizar el artefacto correspondiente; no es necesaria para una consulta,
triage o tarea puntual.

