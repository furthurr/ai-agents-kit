---
name: security
description: >-
  Audita, documenta y ayuda a remediar la SEGURIDAD de aplicaciones (enfocada en
  móvil: Android, iOS y Flutter) en una carpeta canónica `.security/`. Se basa en
  estándares abiertos: OWASP MASVS, MASWE, MASTG y OWASP Mobile Top 10, con
  referencias CWE (sin depender de herramientas propietarias). Para móvil trae el
  checklist precargado por plataforma; para otras tecnologías busca el estándar en
  la web y lo cachea. Lleva la lista de hallazgos con estado (pendiente/en
  progreso/resuelto) para continuar en varias sesiones, prioriza por severidad y
  remedia paso a paso con confirmación del usuario en cada micro-paso. Úsala para
  seguridad, auditoría, buenas prácticas, PII/secretos, cifrado, red/TLS,
  almacenamiento, autenticación, permisos, dependencias vulnerables y hardening.
---

# Skill: Security (auditoría y remediación guiada)

Esta skill es la **referencia canónica** para auditar, documentar y ayudar a
remediar la seguridad de un proyecto, con foco en **móvil (Android, iOS,
Flutter)**. Da a la IA y al equipo un estado claro de riesgos y una ruta de
solución **paso a paso**. Complementa al agente `Security Agent`. Si el agente y
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
  **guárdalo** en `.security/standards/<tech>.md` para reutilizarlo (caché). No
  vuelvas a buscar si ya existe y sigue vigente.

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
2. **Si NO existe:** realiza el **scan/auditoría** (solo lectura), presenta la
   **lista priorizada** y, tras el **gate** de confirmación de alcance (ver Fase A),
   crea la documentación (findings + tablero + PII); luego **ofrece al usuario
   empezar la remediación**.
3. **Si YA existe:** lee el estado y **ofrece re-escanear** para (a) confirmar qué
   puntos siguen **pendientes**, (b) detectar **nuevos** hallazgos, (c) marcar como
   **resueltos** los que ya no aplican. Luego ofrece **continuar** la remediación
   por donde se quedó.
4. Actualiza la marca de sincronización (hash de `HEAD` o fecha).

> El usuario puede resolver los problemas en **varias sesiones**: el estado de
> cada hallazgo queda persistido en `findings/` y en el tablero maestro.

## Fase A — Auditoría (siempre primero)

1. Detecta plataforma/tecnología (Android/iOS/Flutter u otra → fetch estándar).
2. Recorre los 8 grupos MASVS (o el checklist de la tecnología) buscando
   debilidades, citando `archivo:línea`. No inventes; si no puedes verificar algo,
   márcalo como "por revisar".
3. **Presenta la lista priorizada** (severidad, referencia MASVS/MASWE/CWE,
   ubicación) **antes de escribir**; este análisis es de solo lectura.
4. **Gate (espera confirmación) antes de persistir en masa:** el escaneo genera
   **un archivo por hallazgo** en `findings/`, que en repos grandes pueden ser
   muchos. Confirma el **alcance** (todo, solo `Crítica`/`Alta`, top-N…) antes de
   crearlos. **Atajo "genera todo":** si el usuario ya lo autoriza ("genera todo",
   "sin preguntar"), omite la confirmación y persiste directo.
5. Al confirmar, crea por cada debilidad un **finding** en `findings/SEC-NNNN-*.md`
   y una fila en `security-tech-debt.md` con severidad, referencia
   (MASVS/MASWE/CWE), impacto y estado `Pendiente`; luego ofrece iniciar la
   remediación (Fase B).

## Fase B — Remediación guiada (paso a paso, con confirmación)

Trabaja **un hallazgo a la vez**, y **cada hallazgo dividido en micro-pasos**:

1. **Explica** el hallazgo y por qué es riesgo (breve, con su ref MASVS/CWE).
2. **Propón el plan** dividido en micro-pasos numerados (ej. "paso 1 de 4").
3. Ejecuta **UN solo micro-paso**; muestra el **diff mínimo** y **por qué**.
4. **Detente y espera OK** del usuario antes del siguiente micro-paso.
5. Actualiza el estado del finding (`Pendiente` → `En progreso` → `Resuelto`) y su
   bitácora de micro-pasos, para poder continuar luego.
6. Al cerrar el hallazgo, márcalo `Resuelto` en el tablero y pasa al siguiente
   **solo si el usuario lo autoriza**.

**Reglas de remediación (no negociables):**
- Nunca encadenes varios cambios sin confirmación.
- Nada de "fix masivo" opaco: cada paso es pequeño, explicado y reversible.
- Si un paso toca algo fuera de seguridad, avisa antes.
- Nunca escribas secretos reales; usa placeholders.

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
- Auditar primero (solo lectura), documentar los hallazgos tras confirmar el
  alcance (nunca arreglar en silencio), remediar paso a paso con confirmación.
- Persistencia: el estado vive en `.security/` para continuar en varias sesiones.
- Nunca expongas secretos; usa placeholders. Marca la PII.
- Cita `archivo:línea`; no inventes. git solo de lectura.
