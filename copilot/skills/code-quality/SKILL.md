---
name: code-quality
description: >-
  Audita, documenta y ayuda a remediar las BUENAS PRÁCTICAS DE DESARROLLO y la
  calidad de código de cualquier proyecto (foco móvil: Kotlin/Java, Swift, Dart)
  en una carpeta canónica `.quality/`. Se basa en SonarQube: taxonomía Clean Code
  (Maintainability, Reliability, Security), tipos de issue (Bug, Code Smell,
  Security Hotspot), reglas por lenguaje (p. ej. kotlin:S1481) y métricas
  (cobertura, duplicación, complejidad, quality gate). Las reglas de Sonar son
  públicas: precarga familias comunes y hace fetch bajo demanda cacheando en
  `.quality/standards/`. Lleva los hallazgos con estado (pendiente/en
  progreso/resuelto) para continuar en varias sesiones, prioriza por severidad y
  remedia paso a paso con confirmación en cada micro-paso. Úsala para calidad de
  código, code smells, mantenibilidad, fiabilidad, cobertura de pruebas,
  complejidad, duplicación, convenciones y refactor seguro.
---

# Skill: Code Quality (buenas prácticas de desarrollo)

Esta skill es la **referencia canónica** para auditar, documentar y ayudar a
remediar la **calidad de código y buenas prácticas** de un proyecto, con foco en
**móvil (Kotlin/Java, Swift, Dart)**. Da a la IA y al equipo un estado claro de la
deuda de calidad y una ruta de mejora **paso a paso**. Complementa al agente
`Code Quality Agent`. Si el agente y esta skill divergen, **manda esta skill**.

> **Regla de alcance (inviolable):** esta skill trabaja SOLO **calidad de código y
> buenas prácticas** (mantenibilidad, fiabilidad, cobertura, complejidad,
> duplicación, convenciones, refactor seguro). No hace features ni cambios ajenos.
> **Los hallazgos de seguridad se derivan al `Security Agent`** (se mencionan, no
> se remedian aquí). **Nunca expone secretos:** usa placeholders.

## Base: SonarQube (reglas públicas, sin login)

- **Tipos de issue Sonar:** `Bug` (Reliability), `Code Smell` (Maintainability),
  `Security Hotspot` / `Vulnerability` (Security → derivar al Security Agent).
- **Clean Code taxonomy:** atributos (Consistency, Intentionality, Adaptability,
  Responsibility) × cualidades (Maintainability, Reliability, Security).
- **Severidades Sonar (modo MQR):** `Blocker` 🔴 · `High` 🟠 · `Medium` 🟡 · `Low`/`Info` 🟢,
  asignadas por calidad de software (equivalen a Blocker/Critical/Major/Minor/Info del modo *Standard*).
- **Métricas:** cobertura de pruebas, duplicación, complejidad ciclomática/cognitiva,
  deuda técnica estimada, **quality gate**.
- **Reglas por lenguaje** referenciadas por su ID: `kotlin:SXXXX`, `java:SXXXX`,
  `swift:SXXXX`, `dart:SXXXX`, etc.

> Las reglas de Sonar son **públicas**. Precarga las familias comunes; para el
> detalle de una regla concreta, **haz fetch** de la doc pública de Sonar y
> **guárdala** en `.quality/standards/<lenguaje>.md` (caché; no re-busques si ya
> está). Si el repo ya tiene `sonar-project.properties` o reportes de Sonar,
> **referéncialos** (no dupliques ni expongas tokens).

## Carpeta canónica: `.quality/`

Vive en una carpeta `.quality/` (oculta, versionada). Es la memoria persistente
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
producto) → una `.quality/` en la raíz; si los marcadores están en **subcarpetas
hermanas sin agregador** → una por proyecto. Ante la duda, **pregunta**.

⚠️ **Excepción Flutter / React Native / KMP:** si en la **raíz** hay
`pubspec.yaml` (Flutter) o `package.json` con `react-native`, `android/` e `ios/`
son **plataformas de un mismo proyecto** → una sola `.quality/` en la raíz.

### Estructura

```
.quality/
├── README.md                 # Contexto para IA + estado de sincronización + lenguajes + quality gate
├── findings/                 # Un archivo por hallazgo, con estado y micro-pasos (memoria de sesión)
│   └── QLT-0001-*.md
├── quality-tech-debt.md      # Índice de hallazgos priorizados por severidad (tablero maestro)
├── metrics.md                # Cobertura, duplicación, complejidad, deuda técnica estimada
└── standards/                # Reglas Sonar cacheadas por lenguaje (fetch bajo demanda)
```

## Flujo al iniciar (lectura de estado primero)

1. Busca `.quality/`.
2. **Si NO existe:** realiza el **scan/auditoría** (solo lectura), presenta la
   **lista priorizada** y, tras el **gate** de confirmación de alcance (ver Fase A),
   crea la documentación (findings + tablero + métricas); luego **ofrece empezar la
   remediación**.
3. **Si YA existe:** lee el estado y **ofrece re-escanear** para (a) confirmar
   **pendientes**, (b) detectar **nuevos** hallazgos, (c) marcar **resueltos** los
   que ya no aplican. Luego ofrece **continuar** por donde se quedó.
4. Actualiza la marca de sincronización (hash de `HEAD` o fecha).

> El usuario puede mejorar la calidad en **varias sesiones**: el estado de cada
> hallazgo queda persistido en `findings/` y en el tablero maestro.

## Fase A — Auditoría (siempre primero)

1. Detecta lenguajes/tecnología (Kotlin/Java, Swift, Dart u otra → fetch reglas).
2. Recorre el código buscando incumplimientos de reglas Sonar: code smells,
   bugs de fiabilidad, complejidad excesiva, duplicación, cobertura insuficiente,
   convenciones. Cita `archivo:línea`. No inventes; si no puedes verificar, marca
   "por revisar". Si detectas un **Security Hotspot/Vulnerability**, regístralo
   como nota y **deriva al Security Agent** (no lo remedies aquí).
3. **Presenta la lista priorizada** (severidad, regla Sonar, cualidad, ubicación)
   **antes de escribir**; este análisis es de solo lectura.
4. **Gate (espera confirmación) antes de persistir en masa:** el escaneo genera
   **un archivo por hallazgo** en `findings/`, que en repos grandes pueden ser
   muchos. Confirma el **alcance** (todo, solo `Blocker`/`High`, top-N…) antes de
   crearlos. **Atajo "genera todo":** si el usuario ya lo autoriza ("genera todo",
   "sin preguntar"), omite la confirmación y persiste directo.
5. Al confirmar, crea por cada incumplimiento un **finding** en
   `findings/QLT-NNNN-*.md` y una fila en `quality-tech-debt.md` con severidad,
   **regla Sonar** (ID), cualidad (Maintainability/Reliability), impacto y estado
   `Pendiente`; luego ofrece iniciar la remediación (Fase B).

## Fase B — Remediación guiada (paso a paso, con confirmación)

Trabaja **un hallazgo a la vez**, y **cada hallazgo dividido en micro-pasos**:

1. **Explica** el hallazgo y por qué es deuda (breve, con su regla Sonar).
2. **Propón el plan** dividido en micro-pasos numerados ("paso 1 de N").
3. Ejecuta **UN solo micro-paso**; muestra el **diff mínimo** y **por qué**.
4. **Detente y espera OK** antes del siguiente micro-paso.
5. Actualiza el estado del finding (`Pendiente` → `En progreso` → `Resuelto`) y su
   bitácora, para poder continuar luego.
6. Al cerrar el hallazgo, márcalo `Resuelto` en el tablero y pasa al siguiente
   **solo si el usuario lo autoriza**.

**Reglas de remediación (no negociables):**
- Nunca encadenes varios cambios sin confirmación.
- Nada de "refactor masivo" opaco: cada paso pequeño, explicado y reversible.
- No cambies comportamiento sin avisar; preserva la lógica salvo que el fix lo exija.
- Si un paso toca seguridad, deriva; si toca otro dominio, avisa antes.

## Severidad (alineada a Sonar, modo MQR)

- **🔴 Blocker:** alta probabilidad de impacto en producción (crashes, p. ej. NPE
  o force-unwrap; fugas de recursos; bugs de fiabilidad graves).
- **🟠 High:** bugs o smells de alto impacto, complejidad/duplicación severa.
- **🟡 Medium:** smells relevantes, cobertura baja en módulos clave.
- **🟢 Low/Info:** convenciones, nombres, mejoras menores.

Cada hallazgo indica **impacto**, **esfuerzo** y **remediación** recomendada.

## Índice de contexto para otros agentes

`.quality/README.md` incluye una sección **"Contexto para IA"**: resumen denso del
stack, quality gate, métricas y hallazgos abiertos por severidad. Es el punto de
entrada que otros agentes (p. ej. SDD) leen para orientarse.

## Plantillas

### `README.md`
```markdown
# Calidad de código — <Proyecto>

Estado canónico de la calidad. Léelo antes de auditar o remediar.

## Estado de sincronización
- Lenguajes detectados: <p. ej. Kotlin, Swift>
- Último commit documentado: `<hash>` (o fecha si no hay git)
- Última actualización: <YYYY-MM-DD>

## Contexto para IA (resumen denso)
- Stack y build: <lenguajes, gestor de build, framework de test>
- Quality gate: <passed/failed y condiciones clave>
- Métricas actuales: <cobertura, duplicación, complejidad>
- Hallazgos abiertos: <nº por severidad; enlace a quality-tech-debt.md>
- Reglas Sonar de referencia: <familias/lenguajes en standards/>

## Índice
- Tablero de hallazgos: `quality-tech-debt.md`
- Detalle por hallazgo: `findings/`
- Métricas: `metrics.md`
- Reglas cacheadas: `standards/`
```

### `findings/QLT-NNNN-titulo.md`
```markdown
# QLT-NNNN: <título>

- Estado: Pendiente | En progreso | Resuelto
- Severidad: 🔴 Blocker / 🟠 High / 🟡 Medium / 🟢 Low
- Regla Sonar: `kotlin:SXXXX` · Cualidad: Maintainability | Reliability
- Ubicación: `archivo:línea`
- Fecha detección: <YYYY-MM-DD>

## Descripción
<qué regla se incumple y por qué importa>

## Plan de remediación (micro-pasos)
- [ ] Paso 1: <...>
- [ ] Paso 2: <...>

## Bitácora
- <YYYY-MM-DD> Paso 1 aplicado: <qué cambió y por qué>
```

### `quality-tech-debt.md` (tablero maestro)
```markdown
# Calidad — Tablero de hallazgos

| ID | Severidad | Regla | Cualidad | Hallazgo | Ubicación | Estado |
|----|-----------|-------|----------|----------|-----------|--------|
| QLT-0001 | 🟠 | kotlin:S3776 | Maintainability | Complejidad cognitiva alta | `archivo:línea` | Pendiente |
```

### `metrics.md`
```markdown
# Métricas de calidad
- Cobertura de pruebas: <%> (fuente: JaCoCo/…)
- Duplicación: <%>
- Complejidad: <resumen>
- Deuda técnica estimada: <tiempo>
- Quality gate: <passed/failed y condiciones>
```

## Reglas

- Comunícate en español por defecto; si el usuario escribe en otro idioma o lo
  pide, adáptate. Sé claro y conciso.
- Solo calidad/buenas prácticas: no features; seguridad se deriva al Security Agent.
- Auditar primero (solo lectura), documentar los hallazgos tras confirmar el
  alcance (nunca arreglar en silencio), remediar paso a paso con confirmación.
- Persistencia: el estado vive en `.quality/` para continuar en varias sesiones.
- Nunca expongas secretos ni tokens (p. ej. de `sonar-project.properties`).
- Cita `archivo:línea` y la regla Sonar; no inventes. git solo de lectura.
