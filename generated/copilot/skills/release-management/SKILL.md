---
name: release-management
description: >-
  Ejecuta releases en español detectando la tecnología del repositorio; trae de
  fábrica los proyectos móviles (Android, iOS o Flutter): versionado semántico,
  actualización del archivo de versión correspondiente, creación de tags anotados
  (vX.Y.Z) y generación de CHANGELOG a partir de Conventional Commits. Úsala cuando
  el usuario pida "preparar una release", "sacar versión", "crear un tag", "generar
  changelog", "subir la versión" o "bump de versión". Si detecta una tecnología no
  soportada (Node, Rust, Python, Go, .NET, etc.), investiga en la web sus
  convenciones de versionado y genera un perfil reutilizable para darle soporte
  automáticamente. Todas las acciones que escriben en el repo o el remoto requieren
  confirmación explícita.
---

# Release Management (Android · iOS · Flutter · extensible)

Procedimiento para preparar **releases**. La skill **detecta la tecnología** del
repositorio y actualiza el archivo de versión correcto, crea el **tag anotado** y
genera el **CHANGELOG**, siempre en **español** y **solo tras confirmación**.
Soporta Android, iOS y Flutter de fábrica; para **otras tecnologías** se
auto-extiende investigando en la web y cacheando un perfil reutilizable
(ver Paso 1.5).

## Principios

- Comunícate **en español por defecto**; si el usuario escribe en otro idioma o lo pide, adáptate.
- **Nunca** modifiques versiones, crees tags ni hagas push sin **confirmación explícita**.
- **Siempre** muestra la versión actual, la versión propuesta y el CHANGELOG antes de aplicar.
- El versionado sigue **SemVer**: `MAJOR.MINOR.PATCH`.
- Si no puedes determinar la tecnología con certeza, **pregunta al usuario** en lugar de asumir.
- **Alcance:** esta skill cubre versionado, tags y CHANGELOG. Para **commits y push**
  del día a día usa la skill `git-commit`.
- Los comandos son **de referencia para bash/zsh**; adáptalos al shell/SO del
  usuario (PowerShell/cmd en Windows) y no dependas de utilidades Unix si no
  están disponibles. `agvtool` solo existe en macOS con Xcode.

## Carpeta canónica `.release/` (contexto del proyecto)

Cada proyecto guarda **cómo hace sus releases** en una carpeta `.release/` en la
raíz del repositorio (oculta, versionada, estilo `.github/`). Es la fuente de
contexto específica del proyecto y **complementa** (no sustituye) los perfiles
genéricos de `technologies/<slug>.md`.

```
.release/
├── README.md            # Contexto para IA: resumen de cómo se releasea aquí
├── config.md            # Convenciones: esquema de versión, tag, rama, formato de
│                        #   changelog, patrón de ticket, remote, distribución, entornos
├── scripts/             # Comandos/scripts reutilizables (release.sh, lanes, tasks…)
└── history.md           # (opcional) registro de releases anteriores
```

### Al iniciar SIEMPRE
1. Busca `.release/` en la raíz.
2. **Si existe:** lee `README.md`, `config.md` y `scripts/` para tener contexto y
   **respetar esas convenciones por encima de los defaults** de esta skill.
3. **Si no existe:** NO la generes de golpe. Al preparar el primer release, tras
   un **gate**, ofrécela con una plantilla mínima (ver abajo) y propón guardar los
   comandos usados como script reutilizable.

### Contenido y seguridad (imprescindible)
- Modo **documentado + materializable** (Opción C): registra los comandos en
  `config.md`/`README.md` y, si el usuario quiere, materialízalos como script en
  `scripts/`.
- Los scripts deben ser **idempotentes** y respetar los gates: proponer y ejecutar
  **solo tras confirmación**.
- **Antes de ejecutar** cualquier script de `scripts/`, **muestra su contenido** y
  revísalo con el usuario. No ejecutes scripts a ciegas: podrían haberse modificado
  o contener comandos peligrosos.
- **Nunca** guardes secretos, tokens ni keystores en `.release/`: usa solo
  **referencias y placeholders** (`${STORE_KEY}`, ruta esperada del keystore).

### Plantilla mínima de `.release/README.md`
```markdown
# Releases de este proyecto (contexto para IA)

- **Tecnología:** <detectada>
- **Esquema de versión:** <SemVer | SemVer+build | …>
- **Convención de tag:** `<vX.Y.Z>`
- **Rama de release:** `<main | release/*>`
- **CHANGELOG:** `<CHANGELOG.md, formato>`
- **Patrón de ticket:** `<[A-Z]+-[0-9]+>`
- **Distribución:** <stores / CI / manual>
- **Scripts disponibles:** ver `scripts/`
```

### Tras cada release
Ofrece **actualizar** `scripts/` con los comandos que funcionaron y añadir una
entrada a `history.md` (versión, fecha, notas). Confirma antes de escribir.

## Paso 1 — Detectar la tecnología del proyecto

Identifica el tipo de proyecto según los archivos presentes (usa la búsqueda de archivos):

| Tecnología | Señales de detección |
|------------|----------------------|
| **Flutter** | `pubspec.yaml` con clave `version:` y/o dependencia `flutter:` |
| **Android** | `build.gradle` / `build.gradle.kts` con `versionName` y `versionCode`; carpeta `app/` |
| **iOS** | Carpeta `*.xcodeproj` / `*.xcworkspace`, `Info.plist`, `project.pbxproj` |
| **Otra tecnología** | Cualquier otra señal (`package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, `*.csproj`, `composer.json`, `pom.xml` no-Android…) → **auto-extensión** (Paso 1.5) |

Notas:
- Un repo **Flutter** también contiene carpetas `android/` e `ios/`, pero la versión se
  gestiona desde `pubspec.yaml`. **Si hay `pubspec.yaml` con `version:`, trátalo como Flutter.**
- Si el repo tiene múltiples plataformas nativas por separado (no Flutter), pregunta cuál versionar.
- Si la tecnología **no** es Android/iOS/Flutter, no te detengas: pasa a la
  **auto-extensión** (Paso 1.5) para darle soporte.

## Paso 1.5 — Soporte para nuevas tecnologías (auto-extensión con web)

Cuando la tecnología detectada **no** sea Android/iOS/Flutter, la skill se
extiende sola en 4 subpasos. **Requiere la herramienta `web`** (el agente debe
tenerla habilitada).

### 1.5.a — Consulta la caché de tecnologías
Antes de investigar, busca un perfil ya generado en el **catálogo de la skill**:
`technologies/<slug>.md` (p. ej. `technologies/node.md`, `technologies/rust.md`),
relativo a la carpeta de esta skill. Si existe y sigue vigente, **úsalo** y salta
directo al Paso 2. Así el soporte queda disponible para todos los proyectos.
Si no está ahí, revisa también `.release/technologies/<slug>.md` en el proyecto
(caché local usada cuando la carpeta de la skill es de solo lectura).

### 1.5.b — Identifica el ecosistema por señales

| Ecosistema | Señal principal | Archivo de versión típico |
|------------|-----------------|---------------------------|
| Node / npm | `package.json` | `package.json` → `"version"` |
| Rust | `Cargo.toml` | `Cargo.toml` → `[package] version` |
| Python | `pyproject.toml` / `setup.py` | `pyproject.toml` → `[project] version` |
| Go | `go.mod` | solo tags `vX.Y.Z` (sin archivo) |
| .NET | `*.csproj` | `<Version>` en el `.csproj` |
| PHP / Composer | `composer.json` | `composer.json` → `"version"` (o solo tags) |
| Java/Kotlin (no Android) | `pom.xml` / `build.gradle` | `<version>` / `version =` |

> La tabla es orientativa. Si la señal no está aquí o hay dudas, **investiga en
> la web** (1.5.c) antes de asumir.

### 1.5.c — Investiga en la web (solo si no hay caché fiable)
Usa `web` para consultar la **documentación oficial** del ecosistema y confirma:
1. **Dónde vive la versión** (archivo y clave exacta).
2. **Formato de versión** (SemVer puro, ¿hay build number/metadata?).
3. **Cómo se hace el bump** (¿manual, `npm version`, `cargo set-version`…?).
4. **Convención de tag** (`vX.Y.Z`, `X.Y.Z`, prefijos por paquete en monorepos).
5. **CHANGELOG** (ubicación y convención esperada).

Prioriza fuentes oficiales (docs del gestor de paquetes/lenguaje). Registra las
URLs consultadas y la fecha.

### 1.5.d — Genera el perfil y confirma (GATE)
Con lo investigado, redacta el perfil usando esta **plantilla** y muéstralo al
usuario para su aprobación **antes** de guardarlo o aplicar nada:

```markdown
# Perfil de release — <Tecnología>

- **Señales de detección:** <archivos/patrones>
- **Archivo(s) de versión:** `<ruta>` → clave `<clave>`
- **Formato de versión:** <SemVer | SemVer+build | otro>
- **Bump:** <cómo subir MAJOR/MINOR/PATCH y el build si aplica>
- **Herramienta CLI (si existe):** `<comando>`
- **Convención de tag:** `<vX.Y.Z | ...>`
- **CHANGELOG:** `<ubicación/convención>`
- **Notas / edge cases:** <…>
- **Fuentes:** <URLs> — investigado el <fecha>
```

Tras el **sí** del usuario, guarda el perfil en `technologies/<slug>.md` (queda
cacheado y reutilizable) y continúa el flujo normal (Paso 2 en adelante) usando
ese perfil como referencia de versión, tag y CHANGELOG.

> Si la carpeta de la skill es de **solo lectura** (skill distribuida o versionada
> aparte) y no puedes escribir ahí, guarda el perfil en `.release/technologies/<slug>.md`
> del proyecto y avísale al usuario: el soporte quedará disponible al menos para ese repo.

## Paso 2 — Leer la versión actual y el historial

```bash
git describe --tags --abbrev=0 2>/dev/null   # último tag (si existe); 2>/dev/null es solo bash/zsh
git log <ultimo-tag>..HEAD --oneline         # commits desde el último tag
```

Lee la versión actual según la tecnología detectada (ver "Ubicación de la versión
por tecnología"). Si no hay tags previos, usa todo el historial relevante para el
CHANGELOG.

> **Estados de git a contemplar:** si el repo **no tiene commits** aún, deténte y
> avísale al usuario (no hay nada que versionar). Si `git describe` falla por **no
> haber tags**, usa `git log` completo. En **HEAD detached** o sin upstream,
> adviértelo antes de proponer push.

## Ubicación de la versión por tecnología

> **Antes de editar, confirma el archivo real.** No asumas rutas ni que el valor
> es un literal. Si hay **varias apps** en el repo (monorepo) o **varios archivos
> de versión**, pregunta al usuario **cuál** versionar antes de continuar.

### Flutter — `pubspec.yaml`
```yaml
version: 1.2.3+45
```
- Formato: `<versionName>+<buildNumber>` → `1.2.3` es SemVer, `45` es el build incremental.
- En cada release: sube el `versionName` según el bump y el `buildNumber` en **+1**.
- En Flutter la versión vive **solo aquí**: NO edites `android/` ni `ios/` (se derivan de `pubspec.yaml`).

### Android — `build.gradle(.kts)` del módulo de aplicación
```kotlin
versionCode = 3
versionName = "0.0.3"
```
- **No asumas la carpeta `app/`.** Localiza el módulo con el plugin
  `com.android.application` (o el `build.gradle(.kts)` que declare `versionName`);
  puede llamarse `app`, `mobile`, `androidApp`, `composeApp` (KMP), etc.
- `versionName` → SemVer visible. `versionCode` → entero incremental (**+1** en cada release).
- ⚠️ **Si el valor NO es un literal** (p. ej. `versionCode = computeCode()`,
  se lee de `gradle.properties`/`version.properties`, o de una variable), **no lo
  edites a ciegas**: localiza la **fuente real** del valor y edita ahí, o explícale
  al usuario y pide cómo proceder. Editar el literal equivocado puede romper el build.

### iOS — Xcode
Preferentemente en la configuración del target (`*.xcodeproj/project.pbxproj`):
```
MARKETING_VERSION = 1.2.3;          // CFBundleShortVersionString (SemVer)
CURRENT_PROJECT_VERSION = 45;       // CFBundleVersion (build incremental)
```
- ⚠️ **`MARKETING_VERSION` y `CURRENT_PROJECT_VERSION` aparecen VARIAS veces**
  (una por configuración Debug/Release y por target). Debes actualizar **todas**
  las ocurrencias del target correcto de forma consistente, no solo la primera.
- **Preferible usar `agvtool`** (actualiza todo de forma segura) si el proyecto lo soporta:
  ```bash
  agvtool new-marketing-version 1.2.3   # versión SemVer (todas las configs)
  agvtool new-version -all 45           # build number (todas las configs)
  ```
- Si hay **varios targets** (app, extensiones, watch), pregunta cuál versionar.
- Alternativamente, algunos proyectos definen la versión en `Info.plist`
  (`CFBundleShortVersionString` / `CFBundleVersion`); si usan `$(MARKETING_VERSION)`
  como variable, la fuente real sigue siendo el `pbxproj`.
- En cada release: sube `MARKETING_VERSION` según el bump y `CURRENT_PROJECT_VERSION` en **+1**.

## Paso 3 — Determinar el bump (SemVer)

Analiza los tipos de Conventional Commits desde el último tag y sugiere:

| Situación en los commits | Bump | Ejemplo |
|--------------------------|------|---------|
| Algún `BREAKING CHANGE:` o `feat!`/`fix!` | **MAJOR** | `1.2.3` → `2.0.0` |
| Al menos un `feat` (sin breaking) | **MINOR** | `1.2.3` → `1.3.0` |
| Solo `fix`, `perf`, `refactor`, etc. | **PATCH** | `1.2.3` → `1.2.4` |

Presenta la sugerencia y permite que el usuario la ajuste. El **build number**
(`versionCode` / `buildNumber` / `CURRENT_PROJECT_VERSION`) siempre **+1**.

## Paso 4 — Generar el CHANGELOG

Agrupa los commits por tipo desde el último tag. Formato sugerido:

```markdown
## [vX.Y.Z] - AAAA-MM-DD

### Funcionalidades
- <descripción del feat> (TICKET-123)

### Correcciones
- <descripción del fix> (TICKET-123)

### Rendimiento / Refactor
- <descripción>

### Otros
- <chore, docs, build, ci...>
```

- Extrae el ticket de cada commit si está presente (patrón `[A-Z]{2,10}-[0-9]+`).
  **Descarta falsos positivos** que no son tickets (`UTF-8`, `SHA-256`, `COVID-19`,
  `BASE-64`, `ISO-8601`, etc.); ante la duda, no lo incluyas.
- Omite secciones vacías.
- Ubicación por defecto: `CHANGELOG.md` en la raíz; si el perfil `technologies/<slug>.md`
  o `.release/config.md` define otra ubicación/convención, respétala. Si el archivo
  existe, **antepón** la nueva versión arriba; si no, propón crearlo.

## Paso 5 — Confirmar con el usuario

Muestra un resumen y pregunta explícitamente:

- Tecnología detectada y archivo de versión que se modificará.
- Versión actual → versión propuesta (SemVer y build number).
- CHANGELOG generado.
- ¿Aplicar los cambios de versión, commitear y crear el tag?

**No apliques nada** hasta recibir confirmación.

## Paso 6 — Aplicar cambios de versión

Solo tras confirmación, actualiza el archivo correspondiente a la tecnología:

- **Flutter** → `pubspec.yaml`: `version: <nueva>+<build+1>`.
- **Android** → `build.gradle(.kts)` del módulo de app (`com.android.application`): `versionName` y `versionCode` (+1).
- **iOS** → `MARKETING_VERSION` y `CURRENT_PROJECT_VERSION` (+1) en el target/`Info.plist`.
- **Otra tecnología** → aplica lo definido en su perfil `technologies/<slug>.md`
  (archivo, clave, formato y herramienta CLI si la hay).

Y actualiza/crea el CHANGELOG con la nueva sección (por defecto `CHANGELOG.md` en la
raíz; respeta la ubicación/convención del perfil o de `.release/config.md`).

## Paso 7 — Commit, tag y push (solo tras confirmación)

Antes de commitear, aplica la verificación de archivos sensibles de la skill
`git-commit` (Paso 1.5). Este commit solo agrega el archivo de versión y el
CHANGELOG; mantén el mismo criterio si añades otros archivos.

```bash
# Commit del bump y changelog
git add <archivo-version> <changelog>   # <changelog> = CHANGELOG.md por defecto (o el del perfil)
git commit -m "chore(release): preparar versión vX.Y.Z"

# Tag anotado
git tag -a vX.Y.Z -m "Release vX.Y.Z"

# Push (rama + tag) — solo si el usuario confirma
git push origin <rama-actual>
git push origin vX.Y.Z
```

- Pregunta por separado antes de hacer push de la rama y del tag.
- En **monorepos** donde versionas un paquete concreto, usa el prefijo de tag que
  indique el perfil/convención (p. ej. `paquete-vX.Y.Z`) en lugar de `vX.Y.Z`.
- Si el push del tag falla, explica el motivo; **no** uses `--force`.

## Comandos de referencia

```bash
git describe --tags --abbrev=0        # último tag
git tag -l                            # listar tags
git log <ultimo-tag>..HEAD --oneline  # commits desde el último tag
git tag -a vX.Y.Z -m "Release vX.Y.Z" # crear tag anotado
git push origin vX.Y.Z                # push del tag
git tag -d vX.Y.Z                     # borrar tag local (solo si se pide)
```

## Solución de problemas

| Problema | Solución |
|----------|----------|
| No se detecta la tecnología | Revisa señales de otros ecosistemas y aplica la **auto-extensión** (Paso 1.5); si sigue sin quedar clara, pregunta al usuario. |
| Repo Flutter con carpetas android/ e ios/ | Versiona desde `pubspec.yaml`, no en las nativas. |
| No hay tags previos | Usa todo el historial para el CHANGELOG y parte de la versión actual del archivo. |
| Tag ya existe | Avisa al usuario; no lo sobrescribas sin confirmación explícita. |
| Push del tag rechazado | Verifica permisos/remote; nunca uses `--force` sin confirmación. |
| Versión inconsistente | Alinea el archivo de versión con el último tag antes de continuar. |
