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

## Identidad del MAS

En este kit, `MAS` significa **Multi-Agent System** (sistema multiagente): agentes,
skills, orquestación, handoffs, adaptadores y artefactos generados. `MAS:` dirige
una instrucción al sistema completo; `@<agente>` dirige a un agente concreto. No
confundas `MAS` con un modelo/proveedor LLM ni con `MASVS`, `MASWE` o `MASTG` de OWASP.

## Aviso de modelo

Antes de operar, recomienda `BAJO` para consultas de estado y `MEDIO` para
revisiones o micro-remediaciones localizadas. Para auditoría
inicial/completa, falta de baseline o análisis transversal, carga
`references/model-selection.md` y aplica su hard stop. No repitas un nivel ya
confirmado por Code Review o Documentation Orchestrator para el mismo alcance y
dominios seleccionados. Nunca nombres
modelos/proveedores ni cambies el modelo del host.
La primera respuesta visible debe comenzar con
`Nivel recomendado: BAJO|MEDIO|ALTO — <motivo breve>.`, salvo esa confirmación previa.
Clasifica antes de inspeccionar el proyecto. Una solicitud pesada explícita basta:
carga solo la matriz, emite el hard stop y termina el turno sin más herramientas.
Para lo puntual, termina el turno tras el aviso antes de trabajar; reanuda cuando
el usuario indique continuar, sin confirmar el modelo ni repetir la recomendación.

Esta skill es la **referencia canónica** para auditar, documentar y ayudar a
remediar la **calidad de código y buenas prácticas** de un proyecto, con foco en
**móvil (Kotlin/Java, Swift, Dart)**. Da a la IA y al equipo un estado claro de la
deuda de calidad y una ruta de mejora **paso a paso**. Complementa al agente
`Code Review Agent`. Si el agente y esta skill divergen, **manda esta skill**.

> **Regla de alcance (inviolable):** esta skill trabaja SOLO **calidad de código y
> buenas prácticas** (mantenibilidad, fiabilidad, cobertura, complejidad,
> duplicación, convenciones, refactor seguro). No hace features ni cambios ajenos.
> **Los hallazgos de seguridad requieren la skill `security`**, no este
> procedimiento. Code Review puede aplicarla en la misma sesión si seguridad
> está autorizada; en solo calidad informa y ofrece ampliar, sin registrar ni
> remediar el otro dominio. **Nunca expone secretos:** usa placeholders.

## Base: SonarQube (reglas públicas, sin login)

- **Tipos de issue Sonar:** `Bug` (Reliability), `Code Smell` (Maintainability),
  `Security Hotspot` / `Vulnerability` (Security → procedimiento `security`).
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
> **guárdala** solo en operaciones documentales autorizadas en
> `.quality/standards/<lenguaje>.md` (caché; no re-busques si ya
> está). Si el repo ya tiene `sonar-project.properties` o reportes de Sonar,
> **referéncialos** (no dupliques ni expongas tokens).
> En una consulta de solo lectura, usa la documentación en memoria: sin escrituras
> de cachés, findings o marcas de sincronización.

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
2. Clasifica intención: consulta/inspección = solo lectura; auditar y documentar,
   inicializar o sincronizar = persistencia en el alcance solicitado.
3. **Si NO existe:** una consulta no crea `.quality/`; una auditoría documental
   solicitada realiza el scan y registra los hallazgos verificados.
4. **Si YA existe:** lee el estado relevante. Si ya se pidió auditar/sincronizar,
   revalida pendientes y nuevos sin volver a ofrecer el mismo reescaneo; verifica
   los resueltos antes de cambiar su estado. Una consulta puntual no dispara un
   escaneo completo. Ofrece remediar como una operación aparte.
5. Actualiza la marca de sincronización solo tras una operación documental,
   cubriendo el alcance realmente auditado; no declares vigente todo un proyecto
   después de una revisión parcial.

> El usuario puede mejorar la calidad en **varias sesiones**: el estado de cada
> hallazgo queda persistido en `findings/` y en el tablero maestro.

## Fase A — Auditoría (siempre primero)

1. Detecta lenguajes/tecnología (Kotlin/Java, Swift, Dart u otra → fetch reglas).
2. Recorre el código buscando incumplimientos de reglas Sonar: code smells,
   bugs de fiabilidad, complejidad excesiva, duplicación, cobertura insuficiente,
   convenciones. Cita `archivo:línea`. No inventes; si no puedes verificar, marca
   "por revisar". Si detectas un **Security Hotspot/Vulnerability**, regístralo
   como nota; Code Review aplica `security` si ese dominio está autorizado
   (no lo remedies con este procedimiento).
3. **Presenta la lista priorizada** (severidad, regla Sonar, cualidad, ubicación)
   **antes de escribir**; este análisis es de solo lectura.
4. **Persistencia sin filtro redundante:** una auditoría documental autorizada
   guarda todos los hallazgos verificados de todas las severidades. Agrupa las
   ocurrencias de la misma causa con sus ubicaciones y preserva IDs existentes.
   Reutiliza la autorización explícita de la sesión para la misma operación y
   proyecto; no pidas otra selección de severidades. Consulta/`inspect` no escribe.
   Pregunta solo por decisiones pendientes: ambigüedad de proyecto, ampliaciones,
   sobrescritura manual o volumen que impida completar el alcance y requiera lotes.
   No trunques resultados ni transfieras esa autorización a remediación.
5. Dentro de ese alcance, crea por cada incumplimiento distinto un **finding** en
   `findings/QLT-NNNN-*.md` y una fila en `quality-tech-debt.md` con severidad,
   **regla Sonar** (ID), cualidad (Maintainability/Reliability), impacto y estado
   `Pendiente`; luego ofrece iniciar la remediación (Fase B).

## Fase B — Remediación guiada (paso a paso, con confirmación)

Trabaja **un hallazgo a la vez**, y **cada hallazgo dividido en micro-pasos**:

### Gate de ruta: corrección directa o recomendación de SDD

Antes de proponer los micro-pasos, clasifica la ruta. La **severidad por sí sola
no decide** si hace falta SDD.

La corrección puede continuar directamente solo si el resultado esperado está
claro, es localizado y reversible, permanece dentro de calidad, no cambia un
contrato público ni un esquema/migración, no exige una decisión arquitectónica o
coordinación entre capas/módulos y su riesgo se controla con pruebas focalizadas.
Puede corregir un defecto observable si el comportamiento esperado es inequívoco
y el cambio sigue cumpliendo todas esas condiciones.

Recomienda continuar con `SDD (Spec-Driven Development)` si falla alguna condición anterior, en
particular cuando falten requisitos o criterios de aceptación, se introduzca o
cambie comportamiento de forma amplia, se crucen módulos/capas, se alteren
contratos o persistencia, o exista riesgo relevante de regresión, concurrencia o
integridad. Entonces:

1. Explica brevemente qué criterios activaron la recomendación.
2. Cita el `QLT-NNNN`, las ubicaciones y la evidencia disponible.
3. Ofrece una instrucción copiable para `SDD (Spec-Driven Development)` que incluya esa referencia.
4. **Detente antes de modificar código y pregunta qué prefiere el usuario.** No
   cambies de agente ni crees artefactos `.sdd/` automáticamente.
5. Si el usuario prefiere seguir aquí, aclara primero lo ambiguo y continúa solo
   si el alcance resultante es seguro, queda dentro de calidad y respeta todos los
   gates; en caso contrario, explica el bloqueo.

Cuando el usuario regrese tras implementar la spec, reaudita y verifica el
hallazgo antes de marcarlo `Resuelto`.

1. **Explica** el hallazgo y por qué es deuda (breve, con su regla Sonar).
2. **Propón el plan** dividido en micro-pasos numerados ("paso 1 de N").
3. Solicita aprobación antes del primer micro-paso y de cada siguiente; ejecuta
   **UN solo micro-paso** autorizado y muestra el **diff mínimo** y **por qué**.
4. **Detente y espera OK** antes del siguiente micro-paso.
5. Actualiza el estado del finding (`Pendiente` → `En progreso` → `Resuelto`) y su
   bitácora, para poder continuar luego.
6. Al cerrar el hallazgo, márcalo `Resuelto` en el tablero y pasa al siguiente
   **solo si el usuario lo autoriza**.

**Reglas de remediación (no negociables):**
- Nunca encadenes varios cambios sin confirmación.
- Nada de "refactor masivo" opaco: cada paso pequeño, explicado y reversible.
- No cambies comportamiento sin avisar; preserva la lógica salvo que el fix lo exija.
- Si un paso toca seguridad, requiere el procedimiento `security` y su autorización;
  si toca otro dominio, avisa antes.

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

## Referencias bajo demanda

Las plantillas completas y criterios de clasificación están en
[`references/templates.md`](references/templates.md). Ábrela solo al crear o
actualizar el artefacto correspondiente; no es necesaria para una consulta,
triage o tarea puntual.

La matriz y el gate para operaciones pesadas están en
[`references/model-selection.md`](references/model-selection.md); no la cargues
para consultas o remediaciones inequívocamente puntuales.

## Reglas

- Comunícate en español por defecto; si el usuario escribe en otro idioma o lo
  pide, adáptate. Sé claro y conciso.
- Solo calidad/buenas prácticas: no features; seguridad usa su propia skill.
- Auditar primero, documentar dentro del alcance solicitado sin repetir filtros;
  las consultas son sin escrituras y la remediación requiere aprobación aparte.
- Persistencia: el estado vive en `.quality/` para continuar en varias sesiones.
- Nunca expongas secretos ni tokens (p. ej. de `sonar-project.properties`).
- Cita `archivo:línea` y la regla Sonar; no inventes. git solo de lectura.
