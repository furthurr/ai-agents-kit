---
name: security
description: >-
  Audita seguridad de aplicaciones y registra findings OWASP/CWE en `.security/`.
  Úsala ante peticiones de revisar autenticación, red/TLS, almacenamiento, PII,
  secretos, permisos o vulnerabilidades; la calidad general corresponde a code-quality.
---

# Skill: Security (auditoría y remediación guiada)

## Identidad del MAS

MAS significa **Multi-Agent System**; `MAS:` se dirige al kit y `@<agente>` a un rol concreto.


Esta skill es la **referencia canónica** para auditar, documentar y ayudar a
remediar la seguridad de un proyecto, con foco en **móvil (Android, iOS,
Flutter)**. Da a la IA y al equipo un estado claro de riesgos y una ruta de
solución **paso a paso**. Complementa al agente `Code Review Agent`. Si el agente y
esta skill divergen, **manda esta skill**.

> **Regla de alcance (inviolable):** esta skill trabaja SOLO **seguridad**
> (auditoría, hallazgos, remediación segura, hardening). No hace features ni
> cambios ajenos a seguridad. **Nunca expone secretos, tokens ni certificados:**
> documenta su existencia con placeholders.

## Estándares (abiertos, sin herramientas propietarias)

- **OWASP MASVS** — 8 grupos de control: `STORAGE`, `CRYPTO`, `AUTH`, `NETWORK`,
  `PLATFORM`, `CODE`, `RESILIENCE`, `PRIVACY`.
- **OWASP MASWE** — debilidades concretas mapeadas a esos grupos.
- **OWASP MASTG** — pruebas específicas por plataforma (Android/iOS/Flutter).
- **OWASP Mobile Top 10 (2024)** — M1..M10.
- **CWE** — identificador estándar de cada debilidad (ej. CWE-319).

> No se usan reglas de herramientas comerciales (p. ej. Checkmarx). Cada hallazgo
> se referencia con **MASVS + MASWE + CWE**, que son abiertos y universales.

### Cobertura precargada (móvil) y por fetch (otras)
- **Android / iOS / Flutter:** usa el checklist MASVS/MASWE/Top 10 **precargado**
  (los 8 grupos de control de arriba). No requiere red.
- **Otra tecnología** (web, backend, etc.): busca en la web el estándar
  correspondiente (OWASP ASVS/Top 10, CWE, guía del framework), **resúmelo** y
  **guárdalo** solo en operaciones documentales autorizadas en
  `.security/standards/<tech>.md` para reutilizarlo (caché). No
  vuelvas a buscar si ya existe y sigue vigente.
- En una consulta de solo lectura usa los estándares en memoria, sin escrituras
  de cachés, findings ni marcas de sincronización.

## Carpeta canónica: `.security/`

Vive en una carpeta `.security/` (oculta, versionada). Es la memoria persistente
que permite **continuar en varias sesiones**. Su ubicación depende del número de
proyectos: **una en la raíz** si es un solo producto (aunque sea monorepo
multi-módulo), o **una por proyecto** si hay varios proyectos/apps independientes
en carpetas separadas (nunca mezcles proyectos distintos en una sola).

### Ubicación: uno o varios proyectos

**Detección (primera vez):** escanea las subcarpetas de primer nivel —y
contenedores típicos de monorepo como `apps/`, `packages/`, `services/`— buscando
marcadores de proyecto: `settings.gradle(.kts)` / `build.gradle` (Android/JVM),
`*.xcodeproj` / `*.xcworkspace` / `Podfile` (iOS), `pubspec.yaml` (Flutter),
`package.json` (JS/TS). Si hay un **agregador en la raíz** (o todo es un mismo
producto) → una `.security/` en la raíz; si los marcadores están en **subcarpetas
hermanas sin agregador** → una por proyecto. Ante la duda, **pregunta**.

⚠️ **Excepción Flutter / React Native / KMP:** si en la **raíz** hay
`pubspec.yaml` (Flutter) o `package.json` con `react-native`, `android/` e `ios/`
son **plataformas de un mismo proyecto** → una sola `.security/` en la raíz.

### Estructura

```
.security/
├── README.md                 # Contexto para IA + estado de sincronización + plataforma/perfil de riesgo
├── findings/                 # Un archivo por hallazgo, con estado y micro-pasos (memoria de sesión)
│   └── SEC-0001-*.md
├── security-tech-debt.md     # Índice de hallazgos priorizados por severidad (tablero maestro)
├── pii-secrets.md            # Inventario de PII y secretos (existencia, ubicación, SIN valores)
├── dependencies.md           # Dependencias con vulnerabilidades conocidas (SCA/SBOM)
└── standards/                # Checklists por tecnología (precargado móvil; fetch para otras)
```

## Flujo al iniciar (lectura de estado primero)

1. Busca `.security/`.
2. Clasifica intención: consulta/inspección = solo lectura; auditar y documentar,
   inicializar o sincronizar = persistencia en el alcance solicitado.
3. **Si NO existe:** una consulta no crea `.security/`; una auditoría documental
   solicitada realiza el scan y registra los hallazgos verificados.
4. **Si YA existe:** lee el estado relevante. Si ya se pidió auditar/sincronizar,
   revalida pendientes y nuevos sin volver a ofrecer el mismo reescaneo; verifica
   los resueltos antes de cambiar su estado. Una consulta puntual no dispara un
   escaneo completo. Ofrece remediar como una operación aparte.
5. Actualiza la marca de sincronización solo tras una operación documental,
   cubriendo el alcance realmente auditado; no declares vigente todo un proyecto
   después de una revisión parcial.

> El usuario puede resolver los problemas en **varias sesiones**: el estado de
> cada hallazgo queda persistido en `findings/` y en el tablero maestro.

## Fase A — Auditoría (siempre primero)

1. Detecta plataforma/tecnología (Android/iOS/Flutter u otra → fetch estándar).
2. Recorre los 8 grupos MASVS (o el checklist de la tecnología) buscando
   debilidades, citando `archivo:línea`. No inventes; si no puedes verificar algo,
   márcalo como "por revisar".
3. **Presenta la lista priorizada** (severidad, referencia MASVS/MASWE/CWE,
   ubicación) **antes de escribir**; este análisis es de solo lectura.
4. **Persistencia de hallazgos:** una auditoría documental autorizada guarda todos
   los hallazgos verificados de todas las severidades. Agrupa las ocurrencias de la
   misma causa con sus ubicaciones y preserva los IDs existentes.
   Reutiliza la autorización explícita de la sesión para la misma operación y
   proyecto; no pidas otra selección de severidades. Consulta/`inspect` no escribe.
   Pregunta solo por decisiones pendientes: ambigüedad de proyecto, ampliaciones,
   sobrescritura manual o volumen que impida completar el alcance y requiera lotes.
   No trunques resultados ni transfieras esa autorización a remediación.
5. Dentro de ese alcance, crea por cada debilidad distinta un **finding** en `findings/SEC-NNNN-*.md`
   y una fila en `security-tech-debt.md` con severidad, referencia
   (MASVS/MASWE/CWE), impacto y estado `Pendiente`; luego ofrece iniciar la
   remediación (Fase B).

## Fase B — Remediación proporcional al riesgo

Trabaja un hallazgo a la vez. Después de elegir la ruta directa o SDD, clasifica la
corrección por alcance y reversibilidad antes de pedir autorización:

### Gate de ruta: corrección directa o recomendación de SDD

La **severidad por sí sola no decide** si hace falta SDD; aplica estos criterios
de ruta antes de proponer el cambio.

La corrección puede continuar directamente si el resultado seguro esperado está
claro, es localizado y reversible, permanece dentro de seguridad, no rediseña
flujos de autenticación/autorización ni protocolos, no requiere migrar datos o
credenciales, no cruza módulos/capas y puede verificarse con pruebas focalizadas.

Recomienda continuar con `/sdd` si falla alguna condición anterior,
especialmente ante requisitos o compatibilidad ambiguos, rediseño de
auth/sesión/autorización, migraciones de almacenamiento o criptografía, cambios de
confianza de red/pinning, ciclo de vida de PII, coordinación multiplataforma o
riesgos relevantes de regresión, disponibilidad o integridad. Entonces:

1. Explica brevemente qué criterios activaron la recomendación.
2. Cita el `SEC-NNNN`, referencias OWASP/CWE, ubicaciones y evidencia disponible.
3. Ofrece una instrucción copiable para `/sdd` que incluya esa referencia.
4. **Detente antes de modificar código y pregunta qué prefiere el usuario.** No
   cambies de agente ni crees artefactos `.sdd/` automáticamente.
5. Si el usuario prefiere seguir aquí, aclara primero lo ambiguo y continúa solo
   si el alcance resultante es seguro, queda dentro de seguridad y respeta todos
   los gates; en caso contrario, explica el bloqueo.

Cuando el usuario regrese tras implementar la spec, reaudita y verifica el
hallazgo antes de marcarlo `Resuelto`.

- **Atómica y bajo riesgo:** corrección localizada, reversible, sin contrato,
  migración ni cambio de frontera de seguridad, y verificable con pruebas focalizadas.
  Explica el hallazgo, presenta el diff completo y pide una sola aprobación antes
  de aplicarlo.
- **Estructural o de riesgo elevado:** varios módulos, credenciales/PII, auth/sesión,
  criptografía, red, persistencia o garantías de integridad. Divide en micro-pasos
  y pide aprobación antes de cada paso.
- No escribas antes de la autorización aplicable. Verifica, actualiza estado/bitácora
  después de la evidencia y no pases a otro hallazgo sin permiso.

**Reglas de remediación (no negociables):**
- Nunca encadenes cambios estructurales sin las confirmaciones requeridas.
- Nada de "fix masivo" opaco: cada paso es pequeño, explicado y reversible.
- Si un paso toca algo fuera de seguridad, avisa antes.
- Nunca escribas secretos reales; usa placeholders.
- Al publicar, los secretos confirmados quedan excluidos sin excepción de
  autorización; informa ubicación y motivo, nunca valores. Un nombre sospechoso
  no equivale a una credencial: distingue configuración pública y placeholders.
  Para Git/release, aplica la política y el control acotado de
  [git-commit](../git-commit/SKILL.md), sin afirmar detección universal.

## Severidad

- **🔴 Crítica:** secretos/keys hardcodeados, PII sin cifrar o en logs, tráfico en
  claro (cleartext), validación de certificado deshabilitada, cripto rota, sin
  pinning donde se requiere, deserialización insegura.
- **🟠 Alta:** almacenamiento sensible sin cifrar, auth/local débil, componentes
  exportados sin protección, dependencias con CVE conocidas.
- **🟡 Media:** falta de hardening (root/jailbreak, anti-tamper), permisos
  excesivos, logging verboso en producción.
- **🟢 Baja:** mejoras menores, documentación o endurecimiento opcional.

Cada hallazgo indica **impacto**, **esfuerzo** y **remediación** recomendada.

## Índice de contexto para otros agentes

`.security/README.md` incluye una sección **"Contexto para IA"**: resumen denso del
perfil de riesgo, superficie sensible, PII/secretos y hallazgos abiertos por
severidad. Es el punto de entrada que otros agentes (p. ej. SDD) leen para orientarse.

## Referencias bajo demanda

Las plantillas completas y criterios de clasificación están en
[`references/templates.md`](references/templates.md). Ábrela solo al crear o
actualizar el artefacto correspondiente; no es necesaria para una consulta,
triage o tarea puntual.

## Reglas

- Comunícate en español por defecto; si el usuario escribe en otro idioma o lo
  pide, adáptate. Sé claro y conciso.
- Solo seguridad: no hagas features ni cambios ajenos.
- Auditar primero y documentar dentro del alcance solicitado;
  las consultas son sin escrituras y la remediación requiere aprobación aparte.
- Persistencia: el estado vive en `.security/` para continuar en varias sesiones.
- Nunca expongas secretos; usa placeholders. Marca la PII.
- Cita `archivo:línea`; no inventes. git solo de lectura.
