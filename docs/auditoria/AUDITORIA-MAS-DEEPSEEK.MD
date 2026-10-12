# Auditoría del MAS (Multi-Agent System) — DeepSeek

- **Fecha:** 9 de octubre de 2026.
- **Proyecto auditado:** `ai-agents-kit` — MAS (Multi-Agent System).
- **Repositorio revisado:** `/Users/pedrogomezvasquez/Documents/Repositorios/GITHUBREPOS/ai-agents-kit` (rama principal, commit `03f30be`, versión `v1.0.0`).
- **Guía de auditoría aplicada:** `agent-doctor.md` (especificación de auditoría de skills y agentes).
- **Tipo de revisión:** auditoría estática sobre fuentes canónicas, adaptadores, herramientas y pruebas. No se ejecutaron agentes, instaladores ni hosts reales.
- **Estado:** diagnóstico y propuestas; **ninguna corrección aplicada** al repositorio.

> Las referencias `ruta:línea` corresponden a los archivos observados durante esta auditoría. Los números de línea pueden variar tras ediciones posteriores; verificar vigencia antes de implementar cualquier cambio.

---

## 1. Diagnóstico

El MAS tiene una **arquitectura de distribución sólida y bien pensada**: una única fuente canónica (`canonical/`) se proyecta a seis plataformas mediante adaptadores declarativos, con un validador no destructivo (`tools/validate.py`) que comprueba reproducibilidad por hashes. La separación agente/skill, los alcances de dominio y la trazabilidad son activos reales que conviene conservar.

Los problemas detectados son de **proceso y de costo de contexto**, no de diseño de fondo. Se concentran en cinco frentes:

1. **Ruido forzado por pruebas y plantillas** (identidad MAS y acrónimos de OWASP inyectados en todos los archivos, textos duplicados).
2. **Controles enunciados como "inviolables" que no tienen enforcement uniforme** entre hosts: dependen de que el modelo obedezca.
3. **Fricción desproporcionada** (micro-pasos obligatorios para cambios atómicos, lanzador Scalar obligatorio sin contrato).
4. **Carga de contexto excesiva** (hiper-fragmentación de referencias SDD, conocimiento general del modelo reexplicado).
5. **Debilidades en herramientas** (render no transaccional, preflight parcial, importador sigue enlaces, medición de contexto no representativa).

### Alcance revisado

- 6 agentes canónicos (`canonical/agents/`).
- 10 skills canónicas (`canonical/skills/*/SKILL.md`) y sus referencias.
- 6 adaptadores de plataforma y sus `platform.json` / `<agente>.json`.
- Herramientas: `render.py`, `validate.py`, `install_preflight.py`, `import_installed.py`, `measure_context.py`, `handoff_contract.py`, `test_mas_identity.py`, `retired_agents.json`.
- Documentación raíz (`README.md`) y de contexto.

### Límites del diagnóstico

- Revisión estática: no se ejecutaron agentes, instaladores ni smoke tests. No se acredita comportamiento runtime.
- No se cuantificaron ahorros de tokens, coste o tiempo; cualquier cifra de mejora sería especulativa.
- La paridad de archivos entre plataformas no garantiza comportamiento conversacional equivalente.

---

## 2. Resumen de hallazgos

| ID | Prioridad | Hallazgo | Acción recomendada |
|---|---|---|---|
| AUD-01 | Alta | Política de secretos permisiva y contradictoria en Git/release | Endurecer: secretos reales nunca se commitean |
| AUD-02 | Alta | Alcance "inviolable" solo garantizado por el prompt, no por el host | Matriz de capacidades + restricciones efectivas por host |
| AUD-03 | Alta | Contrato de `inspect` exige evidencia dentro de la carpeta canónica | Separar fuentes de lectura de fuentes de evidencia |
| AUD-04 | Alta | Contrato de identidad MAS fuerza acrónimos OWASP en todos los archivos | Desacoplar el test; exigirlos solo en seguridad/code-review |
| AUD-05 | Media | Duplicación de `Identidad del MAS` y `Contexto core compartido` | Fuente única + inyección en el render |
| AUD-06 | Media | Micro-pasos obligatorios para cambios atómicos (calidad/seguridad) | Remediación proporcional al riesgo |
| AUD-07 | Media | Hiper-fragmentación de referencias SDD (10 archivos) | Consolidar en módulos temáticos |
| AUD-08 | Media | Lanzador Scalar obligatorio en estado "bloqueado" | Hacerlo opt-in y bajo demanda |
| AUD-09 | Media | Cicatrices de prompt (`deep`/TDD estricto) y advertencias negativas | Reducir a una directiva simple |
| AUD-10 | Media | Conocimiento general del modelo reexplicado en `git-commit` | Podar tablas y secciones obvias |
| AUD-11 | Media | Activación solapada entre skills core de documentación | Precisar descripciones/triggers |
| AUD-12 | Media | `render.py` no transaccional (borra antes de reconstruir) | Publicación atómica desde staging |
| AUD-13 | Media | Preflight compartido no valida referencias ni bytes | Validar árbol completo y hashes |
| AUD-14 | Baja | `import_installed.py` sigue enlaces simbólicos | Rechazar/validar enlaces |
| AUD-15 | Baja | `measure_context.py` mide palabras, no contexto real por flujo | Medir por tarea representativa |

---

## 3. Hallazgos detallados

### AUD-01 — Política de secretos permisiva y contradictoria

- **Prioridad:** Alta.
- **Ubicación:** `canonical/skills/git-commit/SKILL.md:34`, `:100-110`; reutilizada en `canonical/skills/release-management/SKILL.md:314`.
- **Evidencia (texto comprobado):**
  > "Si detectas archivos sensibles, **advierte** al usuario y pide autorización explícita antes de incluirlos […] **Nunca bloquees el flujo: el usuario decide.**"
  > Opción presentada al usuario: "**Incluirlo de todas formas** — necesito tu autorización explícita."
- **Descripción del problema:** una autorización conversacional se convierte en excepción válida para publicar credenciales. La directiva "nunca bloquees el flujo" coloca la conveniencia por encima de la política de no exponer secretos, y `release-management` hereda el mismo criterio al aplicar el Paso 1.5 de `git-commit`.
- **Impacto:** riesgo real de filtrar secretos al historial remoto; contradicción interna con la regla "Nunca expongas secretos" presente en el resto del kit.
- **Cambio mínimo propuesto:**
  1. Distinguir **"archivo potencialmente sensible"** (excluir con aviso, decisión del usuario) de **"secreto real"** (bloquear siempre).
  2. Para secretos reales: excluir del commit, sustituir por placeholder y sugerir control automatizado (p. ej. detección en CI).
  3. Unificar la redacción en `git-commit`, `release-management` y las skills de seguridad para que no exista la opción "incluir de todas formas" cuando se trate de un secreto confirmado.

---

### AUD-02 — Alcance "inviolable" solo garantizado por el prompt

- **Prioridad:** Alta.
- **Ubicación:** `adapters/opencode/agents/code-review.json:7-20`, `adapters/claude/agents/code-review.json:5-15`, `adapters/copilot/agents/code-review.json:8-15`, `adapters/kiro/agents/code-review.json:5-20`, `adapters/pi/agents/code-review.json:4-8`; definido en `canonical/agents/code-review.md:50-52`.
- **Evidencia (texto comprobado):** el alcance "no hagas features, UI, negocio ajeno ni Git/release" es texto de prompt. En la práctica:
  - OpenCode pide aprobación (`"edit": "ask"`, `"bash": {"*": "ask"}`).
  - Claude expone `Edit`, `Write`, `Bash` sin restricción declarada.
  - Copilot expone `edit` y `execute`.
  - Kiro permite `write`/`shell` con un conjunto limitado de `deny`.
  - Pi no declara `permissions`.
- **Descripción del problema:** las mismas instrucciones no producen las mismas restricciones efectivas. La frontera de confianza depende del host y algunos controles no son equivalentes ni verificables.
- **Impacto:** un agente que se supone de solo lectura/auditoría puede escribir según el host; comportamiento no uniforme y no auditable.
- **Cambio mínimo propuesto:**
  1. Definir una **matriz de capacidades mínimas por host** (qué herramientas puede tocar cada agente) y documentarla como límite cuando el host no las soporte.
  2. Aplicar las restricciones donde el host lo permita (permisos/deny explícitos) en lugar de confiar solo en el texto.
  3. Añadir pruebas de contrato que verifiquen la configuración de permisos por adaptador, no solo los hashes.

---

### AUD-03 — El contrato de `inspect` restringe la evidencia al scope canónico

- **Prioridad:** Alta.
- **Ubicación:** `canonical/skills/documentation-orchestrator/references/handoff.md:97-103`; `tools/handoff_contract.py:146-206`.
- **Evidencia (texto comprobado):**
  > "`evidence` contiene archivos existentes **dentro del `scope` original**".
  > Validación: una entrega `delivered` **exige evidencia no vacía** y debe caer dentro de las raíces del `scope`.
- **Descripción del problema:** para `data-api` el `scope` es `.data/` y para `ui-design` es `.design/`. Un `inspect` correcto sobre un proyecto que no tenga esa carpeta (o cuya fuente real esté en código/configuración) no tiene forma válida de acreditar el resultado: o falta la evidencia o queda fuera del scope.
- **Impacto:** bloquea o invalida inspecciones legítimas; confunde **alcance de escritura** con **conjunto de fuentes admisibles de lectura/evidencia**.
- **Cambio mínimo propuesto:**
  - Diferenciar el contrato de evidencia según la acción:
    - `inspect`: admitir evidencia de cualquier fuente existente del proyecto, pertinente al dominio, aunque esté fuera de la carpeta canónica.
    - `bootstrap` / `sync` / `audit-documentation`: exigir evidencia dentro del `write_scope` autorizado.

---

### AUD-04 — El test de identidad fuerza acrónimos de OWASP en todos los archivos

- **Prioridad:** Alta.
- **Ubicación:** `tools/test_mas_identity.py:12` y `:27-33`; efecto en `canonical/skills/git-commit/SKILL.md:20-21`, `canonical/skills/ui-design/SKILL.md:19-20`, `canonical/skills/data-api/SKILL.md:23-24`, `canonical/skills/architecture/SKILL.md:20-21`, `canonical/skills/project-navigator/SKILL.md:15-16`, `canonical/skills/documentation-orchestrator/SKILL.md:18-19`.
- **Evidencia (texto comprobado):** `MARKERS = ("Multi-Agent System", "MAS:", "@<agente>", "MASVS", "MASWE", "MASTG")`, y `content_has_identity()` se aplica a **todos** los agentes y skills canónicos y a sus artefactos generados.
- **Descripción del problema:** el test obliga a incluir la frase "No confundas `MAS` con […] `MASVS`, `MASWE` o `MASTG` de OWASP" incluso en dominios sin relación con seguridad móvil. Es ruido semántico forzado por una aserción sintética.
- **Impacto:** ~6 líneas de boilerplate irrelevante en 16 archivos, cargadas en cada turno; acopla la evolución del kit a un test frágil.
- **Cambio mínimo propuesto:**
  1. Exigir `"MASVS"`, `"MASWE"`, `"MASTG"` **solo** en la skill `security` y en el agente `code-review`.
  2. Para el resto, exigir únicamente `"Multi-Agent System"`, `"MAS:"`, `"@<agente>"`.
  3. Reemplazar la verificación de texto literal por una verificación del **propósito** de identidad (p. ej. sección presente), evitando forzar contenido.

---

### AUD-05 — Duplicación de `Identidad del MAS` y `Contexto core compartido`

- **Prioridad:** Media.
- **Ubicación:** `## Identidad del MAS` idéntico en los 6 agentes y las 10 skills (p. ej. `canonical/agents/code-review.md:16-21`, `canonical/agents/data-api.md:16-21`, `canonical/agents/git-release-manager.md:16-21`); `## Contexto core compartido` idéntico en `code-review.md:3-14`, `data-api.md:3-14`, `ui-design.md:3-14`, `git-release-manager.md:3-14`, `sdd.md:20-31`, `documentation-orchestrator.md:52-63`.
- **Evidencia (texto comprobado):** bloques byte a byte repetidos.
- **Descripción del problema:** hay múltiples lugares que actualizar y riesgo de contradicción. Además, `git-release-manager` recibe el bloque de contexto core que le ordena consultar `.architecture/` y `.navigator/`, cuando su propio alcance le prohíbe tocar arquitectura o índices.
- **Impacto:** mantenimiento frágil, tokens redundantes y un bloque fuera de lugar para el agente Git/release.
- **Cambio mínimo propuesto:**
  1. Mantener el texto de identidad y contexto en un **fragmento único** e inyectarlo en el render.
  2. Excluir a `git-release-manager` del bloque de contexto core (una fuente, una regla).
  3. Conservar los artefactos generados autosuficientes (el render resuelve la duplicación sin cambiar la distribución).

---

### AUD-06 — Micro-pasos obligatorios para cambios atómicos

- **Prioridad:** Media.
- **Ubicación:** `canonical/skills/code-quality/SKILL.md:173-181`; `canonical/skills/security/SKILL.md:165-173`.
- **Evidencia (texto comprobado):**
  > "Solicita aprobación antes del primer micro-paso y de cada siguiente; ejecuta **UN solo micro-paso** autorizado […] Detente y espera OK antes del siguiente micro-paso."
- **Descripción del problema:** la regla es absoluta. Un hallazgo que consiste en corregir una constante o un método deprecado en un archivo obliga igualmente a un plan "paso 1 de N" con confirmaciones repetidas.
- **Impacto:** burocracia interactiva que frena correcciones rápidas y seguras; contradice el principio de libertad proporcional a la operación.
- **Cambio mínimo propuesto:**
  - **Cambio atómico (bajo riesgo:** localizado, reversible, sin contrato público ni migración): proponer el diff completo, explicarlo y pedir **una sola confirmación**.
  - **Cambio estructural (alto riesgo):** conservar la división por micro-pasos con confirmación en cada uno.

---

### AUD-07 — Hiper-fragmentación de referencias en SDD

- **Prioridad:** Media.
- **Ubicación:** `canonical/skills/sdd-spec/references/` (10 archivos: `agent-routing.md`, `ears-reference.md`, `feature-level.md`, `integrity-gate.md`, `navigator-context.md`, `quality-bar.md`, `scope-depth.md`, `spec-continuity.md`, `templates.md`, `testing.md`); consumo encadenado descrito en `canonical/skills/sdd-spec/SKILL.md:118-152`, `:193-255`.
- **Evidencia (texto comprobado):** el flujo indica cargar referencias distintas en preflight, alcance, fase 1, fase 2, fase 3, implementación y verificación.
- **Descripción del problema:** un ciclo típico exige 5–7 lecturas de archivo en secuencia, fragmentando la memoria de trabajo y añadiendo latencia.
- **Impacto:** más operaciones de disco, mayor probabilidad de perder el hilo del objetivo.
- **Cambio mínimo propuesto:** consolidar en 4 módulos temáticos, actualizando las referencias dentro de `SKILL.md` y del agente `sdd`:
  | Consolidado | Absorbe |
  |---|---|
  | `execution.md` | `scope-depth.md`, `feature-level.md`, `agent-routing.md` |
  | `quality.md` | `quality-bar.md`, `testing.md`, `integrity-gate.md` |
  | `templates.md` | `templates.md`, `ears-reference.md` |
  | `context.md` | `navigator-context.md`, `spec-continuity.md` |

---

### AUD-08 — Lanzador Scalar obligatorio en estado "bloqueado"

- **Prioridad:** Media.
- **Ubicación:** `canonical/agents/data-api.md:45-47`; `canonical/skills/data-api/SKILL.md:185-200`; `canonical/skills/data-api/references/api-docs.md:18-33`.
- **Evidencia (texto comprobado):**
  > "prepara el lanzador manual de Scalar […] **aunque todavía falte OpenAPI**; déjalo bloqueado hasta que exista un contrato válido."
- **Descripción del problema:** se ordena crear un artefacto y lógica condicional (estado `bloqueado`) para una herramienta opcional que aún no tiene datos que mostrar. Además, la ruta `scripts/` queda fuera del `write_scope` natural de `.data/`.
- **Impacto:** archivos auxiliares y complejidad en el proyecto del usuario sin valor inmediato; tensión con el alcance de datos.
- **Cambio mínimo propuesto:**
  - Crear el lanzador **solo si** (1) existe o se aprueba un contrato OpenAPI válido y (2) el usuario solicita explícitamente documentación interactiva local.
  - Alternativa: mantenerlo dentro de `.data/` o declarar una extensión de alcance explícita y opt-in.

---

### AUD-09 — Cicatrices de prompt (`deep` / TDD estricto) y advertencias negativas

- **Prioridad:** Media.
- **Ubicación:** `canonical/agents/sdd.md:60-63`; `canonical/skills/sdd-spec/SKILL.md:69-86`, `:89-93`.
- **Evidencia (texto comprobado):**
  > "`deep` y TDD estricto son opciones retiradas. Si el usuario solicita cualquiera de ellas, informa la retirada, propone `standard` […]"
  > "No recomiendes ni menciones modelos/proveedores LLM, no califiques fases o tareas […]
- **Descripción del problema:** el prompt gasta párrafos sobre opciones históricas que ya no existen y sobre lo que *no* debe decirse, en lugar de describir el procedimiento vigente.
- **Impacto:** espacio instruccional desperdiciado y ruido que puede inducir al modelo a mencionar justamente lo prohibido.
- **Cambio mínimo propuesto:** sustituir por una directiva simple:
  > "Si una spec o solicitud pide un modo no soportado, indica que los modos vigentes son `direct`, `lite` y `standard` y propone `standard`."

---

### AUD-10 — Conocimiento general reexplicado en `git-commit`

- **Prioridad:** Media.
- **Ubicación:** `canonical/skills/git-commit/SKILL.md:212-226` (tabla de tipos Conventional Commits), `:292-319` (comandos de referencia), `:321-329` (solución de problemas).
- **Evidencia (texto comprobado):** tablas que explican `feat`, `fix`, `docs`, el uso de `git add`/`git commit -m` y respuestas a "nothing to commit" o "permission denied".
- **Descripción del problema:** son conocimientos que los modelos fundacionales ya poseen; se repiten en cada carga de la skill.
- **Impacto:** ~100 líneas de ruido por carga; sobrecarga de contexto sin ganancia.
- **Cambio mínimo propuesto:** conservar solo las **particularidades del proyecto** (redacción en español, imperativo, 72 caracteres, un commit con secciones, ticket desde la rama, detección de sensibles y confirmación explícita) y eliminar las tablas genéricas.

---

### AUD-11 — Activación solapada entre skills core de documentación

- **Prioridad:** Media.
- **Ubicación:** descripciones en `canonical/skills/documentation-orchestrator/SKILL.md:3-10`, `canonical/skills/architecture/SKILL.md:3-12`, `canonical/skills/project-navigator/SKILL.md:3-7`.
- **Evidencia (texto comprobado):** `documentation-orchestrator` dice "explain architecture, locate modules"; `architecture` dice "entender la arquitectura"; `project-navigator` dice "localizar módulos". Una consulta simple como "explícame la arquitectura" puede activar las tres.
- **Descripción del problema:** disparadores amplios y superpuestos; en hosts con descubrimiento semántico compiten por activarse.
- **Impacto:** carga duplicada de contexto y comportamiento impredecible.
- **Cambio mínimo propuesto:** precisar cada descripción con operación, objeto y resultado:
  - `documentation-orchestrator`: coordinación de estado/sincronización documental (no consultas directas).
  - `architecture`: estructura, límites, decisiones y diagramas en `.architecture/`.
  - `project-navigator`: localización puntual de archivos/módulos/símbolos con `.navigator/`.

---

### AUD-12 — `render.py` no transaccional

- **Prioridad:** Media.
- **Ubicación:** `tools/render.py:74-108`, en particular `:78-79`.
- **Evidencia (código comprobado):**
  ```python
  output = generated_root / platform
  if output.exists():
      shutil.rmtree(output)
  ```
- **Descripción del problema:** se elimina la salida de una plataforma **antes** de reconstruirla. Una excepción a mitad del render deja artefactos parciales o mezclados entre plataformas.
- **Impacto:** una `generated/` inválida puede pasar por copia/instalación; difícil de detectar sin `validate.py`.
- **Cambio mínimo propuesto:** renderizar en un directorio de staging, validar y publicar al completar (intercambio atómico por plataforma o para la matriz completa); documentar y probar la recuperación ante fallo.

---

### AUD-13 — El preflight compartido no valida referencias ni bytes

- **Prioridad:** Media.
- **Ubicación:** `tools/install_preflight.py:85-113` (`check_source`).
- **Evidencia (código comprobado):** `--check-source` comprueba que exista `SKILL.md` por skill y el archivo de cada agente; **no** verifica los recursos referenciados (`references/`, plantillas, `technologies/`) ni sus hashes.
- **Descripción del problema:** puede existir el archivo principal de una skill y faltar una referencia necesaria sin que el preflight compartido lo detecte; los wrappers de Antigravity añaden comprobaciones propias.
- **Impacto:** instalación declarada "completa" con contenido incompleto; comportamiento distinto entre plataformas.
- **Cambio mínimo propuesto:** centralizar la validación del **árbol completo y sus hashes** para todas las plataformas, antes de copiar y después de instalar.

---

### AUD-14 — `import_installed.py` sigue enlaces simbólicos

- **Prioridad:** Baja.
- **Ubicación:** `tools/import_installed.py:32-53`.
- **Evidencia (código comprobado):** usa `shutil.copytree` / `shutil.copy2` sobre `source` sin comprobar que la ruta resuelta permanezca dentro del origen autorizado.
- **Descripción del problema:** una instalación con enlaces puede importar contenido externo a la skill.
- **Impacto:** copia local inadvertida de contenido ajeno; riesgo observado de copia, no filtración demostrada.
- **Cambio mínimo propuesto:** rechazar enlaces o validar su destino antes de copiar, con política explícita para enlaces internos y externos; mantener la garantía de cero escrituras en `--dry-run`.

---

### AUD-15 — `measure_context.py` no mide el contexto real por flujo

- **Prioridad:** Baja.
- **Ubicación:** `tools/measure_context.py:12-22`; presupuestos numéricos en `canonical/skills/project-navigator/SKILL.md:132-143`.
- **Evidencia (código comprobado):** el script suma palabras de agentes, skills y referencias directas; no representa el contexto consumido por una tarea ni incluye recursos anidados.
- **Descripción del problema:** no permite demostrar que el contexto persistente compensa su coste; los topes (`~500 tokens`, `~4 chars ≈ 1 token`) son heurísticas que un modelo no calcula de forma fiable.
- **Impacto:** decisiones de diseño basadas en una métrica que no refleja el uso real.
- **Cambio mínimo propuesto:**
  1. Medir tareas representativas y registrar archivos/referencias leídas, tokens de entrada/salida, interacciones con el usuario y corrección del resultado, comparando con una ejecución sin el kit.
  2. Sustituir los topes numéricos rígidos por **criterios cualitativos de concisión** (documentar como recomendación, no como garantía).

---

## 4. Elementos que conviene conservar

- **Arquitectura canónica desacoplada** (`canonical/` → `adapters/` → `generated/`): evita seis versiones manuales; el validador no destructivo por hashes es un control valioso.
- **Separación agente/skill** y roles consolidados (`code-review` reúne calidad y seguridad, `documentation-orchestrator` coordina core).
- **Alcances de dominio explícitos** con "mandato de la skill sobre el agente" y gates de derivación a SDD.
- **Controles de integridad de SDD** (no marcar tareas sin evidencia, no llamar TDD sin observar un fallo, criterios EARS, trazabilidad).
- **Estándares reconocibles** (EARS, arc42, C4, ADR, OpenAPI, JSON Schema, Conventional Commits, SemVer, OWASP).
- **Honestidad sobre límites de evidencia** (README y documentos de smoke distinguen distribución, fixtures y runtime real).
- **Contrato de handoff** con validación estructural en `handoff_contract.py` (campos cerrados, protección de rutas, rechazo de symlinks que escapan).

---

## 5. Verificación

**Comprobaciones realizadas (estáticas):** lectura de las 6 definiciones de agentes, 10 skills y sus referencias, 6 adaptadores, herramientas y pruebas de contrato; revisión de `README.md` y documentación de contexto. Las afirmaciones sobre líneas citan el contenido observado.

**Pendientes de verificación (requieren ejecución):**

- `python3 tools/render.py` y `python3 tools/validate.py` tras cualquier cambio en `canonical/`/`adapters/`.
- Pruebas de contrato: `python3 -m unittest tools/test_validate.py tools/test_integrity.py tools/test_mas_identity.py tools/test_documentation_core.py tools/test_handoff_contract.py`.
- Smoke tests en hosts reales para respaldar los cambios de permisos (AUD-02) y de contrato de evidencia (AUD-03).
- Prueba de fallo controlado del render para confirmar la publicación atómica (AUD-12).

**Criterio de cierre sugerido por hallazgo:** aplicar el cambio mínimo, actualizar el test/contrato correspondiente y obtener evidencia ejecutada; no declarar resuelto un hallazgo solo por edición del texto.

---

## 6. Orden de trabajo recomendado

1. **Confianza y límites:** AUD-01 (secretos), AUD-02 (permisos por host), AUD-04 (test de identidad).
2. **Integridad del procedimiento:** AUD-03 (evidencia de `inspect`), AUD-08 (Scalar opt-in), AUD-12 (render atómico), AUD-13 (preflight), AUD-14 (importación).
3. **Simplificación y utilidad:** AUD-05 (duplicación), AUD-06 (remediación proporcional), AUD-07 (consolidar SDD), AUD-09 (cicatrices), AUD-10 (poda de `git-commit`), AUD-11 (triggers).
4. **Medición:** AUD-15 (contexto real por flujo).

*Documento de auditoría elaborado como apoyo de revisión. Las propuestas no modifican el comportamiento del kit hasta ser aplicadas y verificadas.*
