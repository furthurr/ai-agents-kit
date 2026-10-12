# Auditoría y Guía de Optimización: MAS (Multi-Agent System) en Google Antigravity

> **Basado en la especificación Agent Doctor (`agent-doctor.md`)**  
> **Fecha:** Octubre 2026  
> **Repositorio auditado:** `ai-agents-kit`  
> **Destino:** Google Antigravity / Ecosistema Multi-Host (Copilot, Claude, Kiro, OpenCode, Pi)

---

## 1. Introducción y Propósito

El repositorio **`ai-agents-kit`** define la arquitectura y las instrucciones de un sistema multiagente (**MAS**) compuesto por 6 agentes especialistas y 10 skills modulares, diseñado para distribuirse entre 6 plataformas de desarrollo de IA.

Esta auditoría aplica los principios de **Agent Doctor**, una metodología centrada en la eficiencia, utilidad y calidad de las instrucciones para modelos de lenguaje. El objetivo no es acortar textos por estética, sino:
1. Eliminar fricción innecesaria y bloqueos burocráticos.
2. Evitar el consumo redundante de tokens de contexto.
3. Asegurar que las instrucciones sean claras, autónomas y proporcionales al riesgo real de cada tarea.
4. Garantizar compatibilidad y máxima fluidez en entornos como **Google Antigravity**.

---

## 2. Resumen Ejecutivo del Diagnóstico

### Fortalezas del proyecto
- **Arquitectura canónica desacoplada:** La lógica común se mantiene en `canonical/` y se proyecta a cada host mediante adaptadores declarativos en `adapters/` usando `tools/render.py`. Esto previene desviaciones manuales entre plataformas.
- **Validación no destructiva:** `tools/validate.py` garantiza que los artefactos generados en `generated/` sean 100% reproducibles a partir de las fuentes canónicas.
- **Controles de seguridad bien concebidos:** Restricción estricta de alcance inviolable (las skills de documentación no modifican código ni tocan Git remoto; las acciones destructivas en Git exigen confirmación).

### Oportunidades de mejora detectadas
- **Contratos de prueba artificiales:** Se obliga a incluir texto repetido y acrónimos irrelevantes en todos los agentes y skills únicamente para pasar aserciones de tests unitarios (`test_mas_identity.py`).
- **Explicación de conocimientos generales:** Se gastan cientos de tokens explicando conceptos que los modelos modernos ya dominan de fábrica (ej. qué es `feat` o cómo usar `git add`).
- **Hiper-fragmentación documental:** En el flujo SDD se obliga al modelo a encadenar la lectura de hasta 10 archivos de referencia independientes durante una sola tarea.
- **Fricción desproporcionada en correcciones:** Las skills de calidad y seguridad exigen confirmaciones iterativas paso a paso incluso para arreglar una sola línea de código.
- **Cicatrices de prompts pasados (*prompt scars*):** Reglas acumuladas para evitar errores de modelos antiguos (como prohibir opciones obsoletas o vetar nombres de modelos).

---

## 3. Detalle de los Hallazgos

---

### Hallazgo 1: Boilerplate duplicado y acrónimos forzados por tests sintéticos
* **Ubicación:**
  * `canonical/agents/*.md` (las 6 definiciones de agentes).
  * `canonical/skills/git-commit/SKILL.md` (líneas 16–21).
  * `canonical/skills/ui-design/SKILL.md` (líneas 15–21).
  * `tools/test_mas_identity.py` (líneas 12 y 27–33).
* **Descripción del problema:**
  * Cada agente incluye un bloque idéntico de 13 líneas llamado `## Contexto core compartido` que le ordena consultar `.architecture/README.md`, `.navigator/` y `references/project-context.md`. Esto se le inyecta incluso al agente `git-release-manager`, cuyo alcance prohíbe tocar código de negocio o arquitectura.
  * El test `test_mas_identity.py` busca rígidamente en cada archivo los marcadores:
    `"Multi-Agent System"`, `"MAS:"`, `"@<agente>"`, `"MASVS"`, `"MASWE"`, `"MASTG"`.
    Debido a este test, skills como `git-commit` o `ui-design` están obligadas a incluir la frase:
    > *"No confundas MAS con MASVS, MASWE o MASTG de OWASP."*
* **Impacto:** Ruido semántico innecesario, sobrecarga de contexto en cada turno y advertencias fuera de lugar en dominios no relacionados con seguridad móvil.

---

### Hallazgo 2: Explicaciones de conceptos estándar que la IA ya conoce
* **Ubicación:**
  * `canonical/skills/git-commit/SKILL.md` (líneas 212–246 y 294–330).
* **Descripción del problema:**
  * La skill contiene una tabla de 15 líneas explicando los tipos de Conventional Commits (`feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, etc.), seguida de una sección que repite: *"Archivos nuevos → feat; correcciones → fix"*.
  * Además, incluye una tabla de comandos elementales de terminal (`git add <archivo>`, `git commit -m "mensaje"`, `git push origin <rama>`) y una tabla de resolución de problemas obvios (*"nothing to commit → usa git add"*; *"permission denied → verifica credenciales"*).
* **Impacto:** Desperdicio de ~100 líneas (~600 tokens) por cada vez que se carga la skill de Git. Los modelos fundacionales ya poseen este conocimiento.

---

### Hallazgo 3: Hiper-fragmentación de referencias en SDD (Spec-Driven Development)
* **Ubicación:**
  * `canonical/skills/sdd-spec/references/` (10 archivos Markdown independientes).
* **Descripción del problema:**
  * La carpeta `references/` contiene: `agent-routing.md`, `ears-reference.md`, `feature-level.md`, `integrity-gate.md`, `navigator-context.md`, `quality-bar.md`, `scope-depth.md`, `spec-continuity.md`, `templates.md` y `testing.md`.
  * Durante un ciclo típico de SDD, la instrucción guía al modelo a leer 5 a 7 de estos archivos en secuencia (uno para el preflight, otro para la profundidad, otro para el routing, otro para la barra de calidad, otro para testing, etc.).
* **Impacto:** Alta latencia por múltiples operaciones de lectura de archivos, fragmentación de la memoria de trabajo del modelo y mayor probabilidad de perder el hilo del objetivo central de la tarea.

---

### Hallazgo 4: Fricción desproporcionada por micro-pasos obligatorios en remediaciones
* **Ubicación:**
  * `canonical/skills/code-quality/SKILL.md` (líneas 173–182).
  * `canonical/skills/security/SKILL.md` (líneas 165–174).
* **Descripción del problema:**
  * Las instrucciones de remediación exigen sin excepción:
    > *"Solicita aprobación antes del primer micro-paso y de cada siguiente; ejecuta UN solo micro-paso autorizado y muestra el diff mínimo y por qué. Detente y espera OK antes del siguiente micro-paso."*
  * Si un hallazgo consiste en corregir una constante o cambiar un método deprecado en un único archivo, la regla fuerza al agente a crear un plan de "paso 1 de N" y exigir que el usuario responda "OK" repetidamente.
* **Impacto:** Burocracia interactiva extrema que frustra al usuario y frena correcciones rápidas y seguras.

---

### Hallazgo 5: Cicatrices de prompts antiguos (*prompt scars*)
* **Ubicación:**
  * `canonical/agents/sdd.md` (líneas 60–69).
  * `canonical/skills/sdd-spec/SKILL.md` (líneas 69–86 y 87–94).
* **Descripción del problema:**
  * Instrucciones defensivas extensas dedicadas a desaconsejar opciones retiradas:
    > *"`deep` y TDD estricto son opciones retiradas. Si el usuario solicita cualquiera de ellas, informa la retirada, propone `standard` o TDD focalizado y espera su aceptación..."*
  * Prohibiciones repetitivas de formato: *"No recomiendes ni menciones modelos/proveedores LLM, no califiques fases o tareas, no añadas pausas..."*
* **Impacto:** El prompt pierde espacio instruyendo sobre lo que *no* debe existir en lugar de describir el procedimiento directo.

---

### Hallazgo 6: Presupuestos numéricos de tokens calculados por heurística de caracteres
* **Ubicación:**
  * `canonical/skills/project-navigator/SKILL.md` (líneas 132–144).
* **Descripción del problema:**
  * Se establece una tabla de presupuesto rígida: `ai-context.md` ~500 (tope ~700); `module-map.json` ~1–2k (tope ~4k); Respuesta típica ~200–600 (tope ~1k); regla de cálculo: `~4 chars ≈ 1 token`.
* **Impacto:** Un LLM no puede hacer autocomputo aritmético determinista de sus propios tokens en tiempo de respuesta. Exigir límites numéricos rígidos introduce confusión en lugar de guiar la concisión cualitativa.

---

### Hallazgo 7: Generación obligatoria de lanzador de Scalar en estado "bloqueado"
* **Ubicación:**
  * `canonical/skills/data-api/SKILL.md` (líneas 185–206).
* **Descripción del problema:**
  * La skill ordena crear un lanzador manual para la herramienta web Scalar incluso si en el proyecto no existe ninguna especificación OpenAPI, dejándolo configurado en estado `bloqueado`.
* **Impacto:** Genera archivos auxiliares y lógica condicional compleja en el proyecto del usuario para una herramienta opcional que ni siquiera tiene datos que mostrar.

---

### Hallazgo 8: Ambigüedad y solapamiento en triggers de activación
* **Ubicación:**
  * Frontmatters de `documentation-orchestrator/SKILL.md`, `architecture/SKILL.md` y `project-navigator/SKILL.md`.
* **Descripción del problema:**
  * En plataformas con descubrimiento semántico de skills (como Google Antigravity o Copilot), una solicitud simple como *"explícame la arquitectura"* o *"localiza el módulo de pagos"* activa a la vez `documentation-orchestrator` (modo `inspect`), `architecture` y `project-navigator`.
* **Impacto:** Competencia entre skills y posible carga duplicada de contexto en la ventana del agente.

---

## 4. Propuesta Integral de Solución (Paso a Paso)

A continuación se detalla cómo remediar cada punto de manera ordenada y segura, preservando la integridad del kit.

---

### Paso 1: Limpieza del Contrato de Identidad MAS y Desacoplamiento de Tests

1. **Editar `tools/test_mas_identity.py`:**
   * Modificar la comprobación para que los marcadores `"MASVS"`, `"MASWE"`, `"MASTG"` sean obligatorios **únicamente** en la skill `security` y en el agente `code-review`.
   * Para el resto de skills y agentes, exigir únicamente `"Multi-Agent System"`, `"MAS:"` y `"@<agente>"`.
2. **Limpiar las skills no relacionadas:**
   * En `canonical/skills/git-commit/SKILL.md`, `ui-design/SKILL.md`, `data-api/SKILL.md`, etc., remover la mención forzada a OWASP.
3. **Desacoplar `git-release-manager.md`:**
   * Retirar el bloque `## Contexto core compartido` de `canonical/agents/git-release-manager.md`, ya que este agente nunca interactúa con la arquitectura del proyecto ni con índices de navegación.
   * Ajustar `tools/test_documentation_core.py` para excluir a `git-release-manager` de la obligatoriedad de dicho bloque.

---

### Paso 2: Poda de Conocimiento General en `git-commit`

1. **Eliminar de `canonical/skills/git-commit/SKILL.md`:**
   * La tabla descriptiva de tipos de Conventional Commits (`feat`, `fix`, etc.).
   * La sección "Determinar tipo y ámbito".
   * La sección "Comandos de referencia" (`git add`, `git commit -m`, etc.).
   * La tabla "Solución de problemas" básica.
2. **Conservar únicamente las particularidades del proyecto:**
   * Redacción en español con verbo en imperativo y límite de 72 caracteres.
   * Regla de un solo commit estructurado por defecto.
   * Extracción automática de ticket desde el nombre de la rama (`Refs: ABC-123`).
   * **Paso 1.5 — Detección proactiva de archivos sensibles** (credenciales, `.env`, keystores) con advertencia al usuario antes del commit.
   * Confirmación explícita previa obligatoria antes de ejecutar `git commit` o `git push`.

---

### Paso 3: Consolidación de Referencias en `sdd-spec`

Reducir los 10 archivos de `canonical/skills/sdd-spec/references/` a **4 módulos temáticos cohesivos**:

| Archivo consolidado | Archivos originales que absorbe | Contenido principal |
|---|---|---|
| `execution.md` | `scope-depth.md`, `feature-level.md`, `agent-routing.md` | Criterios de modos (`direct`, `lite`, `standard`), rúbrica de esfuerzo y enrutamiento a especialistas. |
| `quality.md` | `quality-bar.md`, `testing.md`, `integrity-gate.md` | Criterios de diseño limpio, testing adaptativo y validación de evidencias antes del cierre. |
| `templates.md` | `templates.md`, `ears-reference.md` | Plantillas formales de artefactos (`requirements`, `design`, `tasks`, `verification`) y sintaxis EARS. |
| `context.md` | `navigator-context.md`, `spec-continuity.md` | Consumo selectivo de índices de navegación y trazabilidad de specs previas. |

*Actualizar las referencias directas dentro de `canonical/skills/sdd-spec/SKILL.md` y `canonical/agents/sdd.md`.*

---

### Paso 4: Remediación Proporcional al Riesgo en Calidad y Seguridad

Actualizar la sección `Fase B — Remediación guiada` en `canonical/skills/code-quality/SKILL.md` y `canonical/skills/security/SKILL.md`:

* **Para cambios atómicos / directos (bajo riesgo):**
  * Si la corrección es localizada, no altera contratos públicos ni estructuras de persistencia y se verifica con una prueba puntual:
  * El agente propone el diff completo de una sola vez, explica el porqué y solicita una **única confirmación explícita**. Al ser aprobada, aplica el cambio y verifica.
* **Para cambios estructurales (alto riesgo):**
  * Si el hallazgo requiere tocar múltiples módulos, migrar datos o rediseñar flujos de seguridad/sesión, se mantiene la división por micro-pasos con confirmación en cada uno.

---

### Paso 5: Limpieza de Cicatrices de Prompts (*Prompt Scars*)

1. En `canonical/agents/sdd.md` y `canonical/skills/sdd-spec/SKILL.md`:
   * Reemplazar los párrafos dedicados a explicar la retirada histórica de `deep` y TDD estricto por una directiva simple:
     > *"Si una spec histórica o una solicitud solicita un modo no soportado, informa que los modos vigentes son direct, lite y standard, y propone standard."*
   * Eliminar advertencias negativas repetitivas sobre no mencionar proveedores o modelos de IA.

---

### Paso 6: Sustitución de Presupuestos de Tokens por Criterios de Concisión

En `canonical/skills/project-navigator/SKILL.md`:
* Sustituir la tabla de números de tokens y la fórmula `~4 chars ≈ 1 token` por pautas de contenido:
  * `ai-context.md`: *"Documento condensado de máximo 2 secciones (propósito y organización general); omitir listados exhaustivos de archivos."*
  * `module-map.json`: *"Limitar las descripciones de responsabilidades a una sola frase por módulo."*
  * Respuestas a consultas: *"Entregar únicamente la respuesta concisa y las referencias `archivo:línea`; no volcar código ni árboles de directorios no solicitados."*

---

### Paso 7: Carga Bajo Demanda de Scalar

En `canonical/skills/data-api/SKILL.md`:
* Cambiar la regla del Paso 7:
  * No crear scripts de Scalar de forma preventiva en estado "bloqueado".
  * Crear el lanzador de Scalar **únicamente si**:
    1. Se detecta un archivo de contrato OpenAPI válido (`openapi.yaml` / `openapi.json`).
    2. El usuario solicita explícitamente disponer de documentación interactiva local.

---

### Paso 8: Clarificación de Triggers de Activación

Ajustar las descripciones en el frontmatter de las skills core:
* **`documentation-orchestrator`:**
  > *"Coordina el estado, auditoría y sincronización documental del proyecto (`status`, `sync-check`, `sync-core`, `release-check`). No usar para consultas directas de diseño o navegación rápida."*
* **`architecture`:**
  > *"Documenta y consulta la estructura del sistema, límites entre módulos, patrones arquitectónicos, diagramas C4 y decisiones (ADRs) en `.architecture/`."*
* **`project-navigator`:**
  > *"Localiza rápidamente archivos, módulos y símbolos en el código con consumo mínimo de contexto mediante `.navigator/`."*

---

### Paso 9: Pipeline de Ejecución y Validación

Una vez aplicadas las modificaciones en `canonical/` y `tools/`:
1. Ejecutar las pruebas de contrato de Python:
   ```bash
   python3 -m unittest tools/test_validate.py tools/test_integrity.py tools/test_mas_identity.py tools/test_documentation_core.py
   ```
2. Renderizar los artefactos para las 6 plataformas:
   ```bash
   python3 tools/render.py
   ```
3. Validar reproducibilidad y enlaces:
   ```bash
   python3 tools/validate.py
   python3 tools/check_links.py
   ```

---

## 5. Beneficios e Impacto Esperado

1. **Ahorro de Contexto:** Reducción estimada de entre 800 y 1,500 tokens por turno en interacciones cotidianas de Git, calidad y SDD.
2. **Menor Latencia:** Al unificar las 10 referencias de SDD en 4 archivos temáticos, se reducen las lecturas de disco consecutivas en más de un 50%.
3. **Experiencia de Usuario Fluida:** Eliminación de aprobaciones repetitivas para correcciones menores de 2 líneas de código.
4. **Mantenibilidad:** El código de pruebas deja de exigir acrónimos arbitrarios de OWASP en dominios no relacionados, facilitando la evolución futura del kit.
5. **Máxima Eficacia en Antigravity:** Los subagentes y skills operarán con instrucciones precisas, reduciendo falsos positivos de activación y acelerando la resolución de tareas.
