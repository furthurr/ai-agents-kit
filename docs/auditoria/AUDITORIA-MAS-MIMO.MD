# Auditoría del MAS — skills, agentes y configuración de OpenCode

> Informe generado con **MiMo** (`xiaomi/mimo-v2.6-pro`) siguiendo la guía
> `~/Desktop/agent-doctor.md`. Fecha: **10 de octubre de 2026**.
> Alcance: solo diagnóstico y recomendaciones. No se modificó ningún archivo del MAS.

## Diagnóstico

**Conclusión principal.** El MAS tiene fronteras de responsabilidad bien diseñadas
(tabla de autoridad por carpeta, remisiones explícitas entre skills, carga bajo
demanda de `references/`), pero sufre **duplicación de contexto compartido** y
**activaciones demasiado amplias** que aumentan el coste de contexto y el riesgo de
elegir la skill equivocada. Además, la configuración global referencia un steering
que **no existe**, por lo que las instrucciones que los agentes prometen leer
"primero" nunca llegan. Nada de esto impide el funcionamiento; sí degrada de forma
previsible la selección, la mantenibilidad y el coste por activación.

**Alcance revisado** (estado de este equipo el 10/10/2026):

- `~/.config/opencode/`: `opencode.json`, `commands/` (2), `skills/` (14),
  `agent/` (6), `plugins/`, `skills-backup/`.
- `~/.agents/skills/` (5 skills: archify, computer-use, frontend-slides, orca-cli,
  orchestration).
- Documento guía: `~/Desktop/agent-doctor.md` (analizado como criterio, no auditado
  como skill).

**Limitaciones.** Auditoría estática de texto y configuración: no se ejecutaron los
flujos de las skills ni se midieron activaciones reales, coste ni precisión. No se
auditaron las fuentes del kit (`canonical/`, `generated/` de `ai-agents-kit`) ni su
duplicación interna. Las afirmaciones sobre el comportamiento del router son
hipótesis pendientes de evaluación.

## Hallazgos

### H1 — La configuración global referencia un `OPENCODE.md` inexistente

**Problema.** `opencode.json` declara `"instructions": ["OPENCODE.md"]`, pero ese
archivo no existe ni en `~/.config/opencode/` ni en la raíz del proyecto. El
steering global que los agentes dicen leer primero nunca se carga.

- Ubicación o fragmento: `~/.config/opencode/opencode.json` → `"instructions": ["OPENCODE.md"]`.
- Evidencia: **texto comprobado** — búsqueda recursiva sin resultados en ambas rutas.
- Impacto: dependencia muerta; cualquier regla que se asuma presente en ese archivo
  no se cumple, y el contrato "lee instrucciones y steering primero" solo se
  satisface por accidente en proyectos con `AGENTS.md`.
- Acción: **eliminar** la entrada o crear el archivo.
- Cambio mínimo recomendado: crear `~/.config/opencode/OPENCODE.md` con el steering
  mínimo real (identidad del MAS, precedencias) y alojar ahí el bloque compartido de
  H3; o borrar la clave `"instructions"` hasta que el archivo exista.

### H2 — `frontend-slides` está triplicado

**Problema.** Existen tres copias de la skill: una en `~/.agents/skills/`, otra en
`~/.config/opencode/skills/` y otra **dentro de sí misma**, como export de un plugin
Claude (`plugins/frontend-slides/skills/frontend-slides/SKILL.md`).

- Ubicación o fragmento: `~/.agents/skills/frontend-slides/SKILL.md`;
  `~/.config/opencode/skills/frontend-slides/SKILL.md`;
  `~/.config/opencode/skills/frontend-slides/plugins/frontend-slides/skills/frontend-slides/SKILL.md`.
- Evidencia: **texto comprobado** — tres rutas distintas; la copia de `.agents` y la
  de config son idénticas (contraste por `diff` sin diferencias).
- Impacto: activación ambigua entre copias, riesgo de desactualización divergente y
  peso muerto (el subárbol embebido duplica la skill completa).
- Acción: **eliminar** las copias redundantes; conservar una única fuente.
- Cambio mínimo recomendado: conservar `~/.config/opencode/skills/frontend-slides/`,
  eliminar la copia de `~/.agents/skills/` y sacar el subárbol `plugins/` a un repo
  de distribución fuera del directorio de la skill.

### H3 — El bloque «Identidad del MAS» está copiado en 16 archivos

**Problema.** El mismo bloque explicativo sobre qué significa `MAS` (y sus advertencias
de confusión con el proveedor del modelo) aparece en 10 `SKILL.md` y los 6 archivos
de agente. El bloque «Contexto core compartido» está copiado además en los 6 agentes.
No hay fuente única: una corrección exige 16 ediciones sincronizadas.

- Ubicación o fragmento: 10 skills (`architecture`, `code-quality`, `data-api`,
  `documentation-orchestrator`, `git-commit`, `project-navigator`, `release-management`,
  `sdd-spec`, `security`, `ui-design`) y los 6 agentes de `~/.config/opencode/agent/`.
- Evidencia: **texto comprobado** — 16 coincidencias de `Identidad del MAS` y 6 de
  `Contexto core` (recuento por búsqueda literal).
- Impacto: contexto repetido en cada activación, riesgo de deriva entre copias y
  confusión `MAS` (sistema multiagente) / `MAS` (proveedor MiMo) donde no se aclare.
- Acción: **simplificar**.
- Cambio mínimo recomendado: definir el bloque una sola vez (p. ej. en `OPENCODE.md`,
  ver H1) y dejar en cada archivo 1–2 líneas con enlace; o reducir cada copia a la
  glosa mínima «MAS = Multi-Agent System; no confundir con el proveedor del modelo».

### H4 — `graphify` se activa para «cualquier pregunta» y usa un campo fuera de spec

**Problema.** Su descripción declara activación para "any question about a codebase,
project content, architecture, or file relationships", lo que captura consultas que
corresponden a `architecture`, `project-navigator` o `documentation-orchestrator`.
Además usa `trigger: /graphify`, campo no previsto en la especificación de Agent
Skills, y una convención `/graphify` no mapeada a `commands/`.

- Ubicación o fragmento: `~/.config/opencode/skills/graphify/SKILL.md`
  (frontmatter `description` y `trigger`).
- Evidencia: **texto comprobado** en el frontmatter; **hipótesis pendiente** sobre qué
  copia carga el router en la práctica.
- Impacto: falsos positivos de activación hacia una skill pesada (pipeline de grafos)
  cuando basta una lectura o un mapa de módulos.
- Acción: **simplificar** la descripción y **eliminar** el campo `trigger`.
- Cambio mínimo recomendado: restringir la descripción a casos propios (construir o
  consultar `graphify-out/`, grafos de conocimiento, exportes Neo4j/GraphML, MCP) y
  eliminar `trigger`, o mapearlo a un comando real en `commands/` si se conserva la
  sintaxis `/graphify`.

### H5 — Solapamientos de ámbito sin desempate en la descripción

**Problema.** Tres grupos compiten por la misma petición:

- `documentation-orchestrator` ↔ `project-navigator` ↔ `architecture`
  («explain architecture», «locate modules»).
- `orchestration` ↔ `orca-cli` (ambas listan "handoff" como disparador; el desempate
  está solo en el cuerpo de `orchestration`, no en la descripción que ve el router).
- `archify` ↔ `architecture` (ambas cubren «diagramas» sin límite declarado).

- Ubicación o fragmento: frontmatter de `documentation-orchestrator`, `project-navigator`,
  `architecture`, `orchestration` ("Use `orca-cli` for full ownership handoffs …
  unless asked to supervise, monitor, or coordinate a DAG"), `orca-cli`, `archify`.
- Evidencia: **texto comprobado** en descripciones; no se midieron activaciones reales.
- Impacto: el router puede cargar la skill equivocada o cargar dos; el usuario repite
  la petición o recibe un flujo de más peso del necesario.
- Acción: **simplificar** (límites en la descripción), antes de proponer cualquier
  enrutador nuevo.
- Cambio mínimo recomendado: añadir en cada descripción una cláusula de límite:
  «hallazgos de calidad → code-quality; mapa de módulos → project-navigator;
  documentación canónica → documentation-orchestrator»; «handoff de ownership →
  orca-cli; coordinación supervisada/DAG → orchestration»; «diagramas HTML exportables
  → archify; arc42/ADR en `.architecture/` → architecture».

### H6 — Seis dominios duplican el contrato entre skill y agente

**Problema.** `data-api`, `ui-design`, `documentation-orchestrator`,
`code-quality`↔`code-review`, `sdd-spec`↔`sdd` y `git-commit`+`release-management`
↔`git-release-manager` declaran su alcance en dos capas con redacción casi literal:
la descripción del agente repite la de la skill en vez de referenciarla.

- Ubicación o fragmento: `~/.config/opencode/agent/*.md` (6) frente a las `SKILL.md`
  homónimas del mismo dominio.
- Evidencia: **texto comprobado** (pares con el mismo ámbito declarado);
  **hipótesis pendiente** sobre divergencias ya existentes entre ambas copias.
- Impacto: dos fuentes por regla; al cambiar una, la otra queda desactualizada sin
  señal alguna.
- Acción: **simplificar** (una fuente responsable por regla).
- Cambio mínimo recomendado: que la descripción del agente declare responsabilidad,
  permisos y condición de escalado, y remita a la skill para las reglas de alcance;
  no copiar la sección completa.

### H7 — `/skill` no indexa `~/.agents/skills/` y delega en un agente `build` no definido

**Problema.** El comando `commands/skill.md` solo escanea
`~/.config/opencode/skills/` y `.opencode/skills/`, dejando invisibles las 5 skills
de `~/.agents/skills/`. Su frontmatter declara `agent: build`, nombre sin definición
local en `agent/`.

- Ubicación o fragmento: `~/.config/opencode/commands/skill.md`
  (frontmatter `agent: build`; pasos 1–2 del flujo).
- Evidencia: **texto comprobado** del comando y del listado de `agent/`;
  **hipótesis pendiente** de que `build` sea un agente integrado del runtime.
- Impacto: el descubrimiento manual no coincide con el catálogo real; si `build` no
  existiera, el comando fallaría al invocarse.
- Acción: **simplificar**.
- Cambio mínimo recomendado: añadir el escaneo de `~/.agents/skills/` con origen
  `global-agents`, y confirmar el agente `build` o apuntar al agente por defecto real.

### H8 — Permisos redundantes e inconsistencia deny/allow entre agentes

**Problema.** En `sdd.md`, `"*": "ask"` ya cubre todas las reglas siguientes
(`rm *`, `git push*`, etc.), que resultan redundantes. En
`documentation-orchestrator.md` se usa `"git *": "deny"` con lista de excepciones
(`git status*`, `git log*`, `git diff*`, `git show*`, `git rev-parse*`), mientras el
resto de agentes usa `"ask"`. Todos conceden `webfetch: "allow"`, incluido el agente
de solo lectura documental.

- Ubicación o fragmento: bloques `permission` de `~/.config/opencode/agent/sdd.md` y
  `~/.config/opencode/agent/documentation-orchestrator.md`.
- Evidencia: **texto comprobado** de los bloques; **hipótesis pendiente** de la
  precedencia real deny/allow entre patrones según la especificación de OpenCode.
- Impacto: ruido en la revisión de permisos y falsa sensación de control; acceso de
  red abierto sin necesidad declarada.
- Acción: **simplificar**.
- Cambio mínimo recomendado: quitar las reglas subsumidas por `"*": "ask"`; reservar
  `deny` a los agentes de solo lectura; cambiar `webfetch` a `"ask"` salvo donde sea
  requisito del flujo.

### H9 — `skills-backup/` conserva copias obsoletas en el árbol de configuración

**Problema.** `~/.config/opencode/skills-backup/` contiene
`git-commit-push-20260707-002519` y `sdd-spec-20260707-001802`, copias de julio con
el nombre antiguo `git-commit-push`. El catálogo no las carga, pero ocupan sitio y
confunden al inspeccionar la config.

- Ubicación o fragmento: `~/.config/opencode/skills-backup/`.
- Evidencia: **texto comprobado** (listado del directorio).
- Impacto: bajo; es mantenimiento muerto junto a las fuentes vivas.
- Acción: **eliminar** (o mover fuera del árbol de config).
- Cambio mínimo recomendado: mover el directorio a un backup externo
  (`~/Backups/opencode-skills-backup/`) o eliminarlo si las versiones están en git.

### H10 — `release-management` amplía el alcance con investigación web no acotada

**Problema.** La skill encarga "investigar en la web" las convenciones de cualquier
tecnología no soportada y generar perfiles en caliente, sin límite de fuentes ni de
tiempo; con `webfetch: "allow"` esa expansión es silenciosa.

- Ubicación o fragmento: `~/.config/opencode/skills/release-management/SKILL.md`
  (descripción y procedimiento 1.5.c: "Investiga en la web (solo si no hay caché fiable)").
- Evidencia: **texto comprobado**.
- Impacto: alcance no delimitado; una petición de release puede convertirse en una
  investigación abierta poco verificable.
- Acción: **cargar bajo demanda** con límite explícito.
- Cambio mínimo recomendado: acotar a «máximo 2 fuentes oficiales de la tecnología,
  plantilla reutilizable cacheada y validación del usuario antes de aplicar el
  perfil»; si no hay caché fiable, detenerse y pedir alcance.

### H11 — Descripciones con claims de amplitud injustificados

**Problema.** Varias descripciones se anuncian como universales: "cualquier proyecto"
(`architecture`, `code-quality`, `data-api`, `project-navigator`), "TODO lo relacionado
con DATOS y APIs" (`data-api`), "TODO lo visual" (`ui-design`). La amplitud se declara
en vez de derivarse de disparadores concretos.

- Ubicación o fragmento: frontmatter (`description`) de `architecture`, `code-quality`,
  `data-api`, `ui-design`, `project-navigator`.
- Evidencia: **texto comprobado** en los `SKILL.md`; sin medida de activaciones.
- Impacto: prioridad injustificada frente a skills más específicas y activación en
  tareas que no requieren el flujo completo.
- Acción: **simplificar**.
- Cambio mínimo recomendado: mantener la cobertura del dominio, pero explicitar
  disparadores («tokens/temas/componentes → ui-design»; «endpoints/DTOs/contratos →
  data-api»; «estilos de código y code smells → code-quality») y quitar los
  cuantificadores absolutos.

## Elementos que conviene conservar

- **Tabla de autoridad por carpeta** de `documentation-orchestrator`
  (`.architecture/`, `.design/`, `.data/`, `.quality/`, `.security/`): resuelve
  conflictos de propiedad sin necesidad de un enrutador nuevo.
- **Remisiones explícitas entre skills**: `git-commit` → `release-management` para
  versionado; `sdd-spec/references/agent-routing.md` con lista cerrada de candidatos
  y decisión manual del usuario; `code-quality` y `security` distinguiendo auditoría
  documental de remediación con micro-pasos.
- **Carga bajo demanda de `references/`** en `architecture`, `code-quality`,
  `data-api`, `project-navigator` y `sdd-spec`: buen patrón de disclosure progresiva.
  No sustituirlo por un documento enorme ni por muchos archivos que deban cargarse
  siempre.
- **Permisos restrictivos por defecto** (`edit: "ask"`, `bash: "*": "ask"`) y los
  modos proporcionales (lite/full en `data-api`; direct/lite/standard en `sdd-spec`).
- **Delimitación `computer-use` ↔ `orca-cli`** declarada en la descripción: es el
  modelo a imitar en H5.
- **`opencode-db-maintenance` y `opencode-project-icon`**: dominio acotado, resultado
  claro y activación específica; no requieren cambios.

## Verificación

Comprobado en este equipo el 10 de octubre de 2026:

| Comprobación | Resultado |
|---|---|
| `instructions` de `opencode.json` vs existencia de `OPENCODE.md` | Referencia rota: archivo ausente en config y en raíz del proyecto |
| Copias de `frontend-slides` (búsqueda de `SKILL.md`) | 3: `.agents`, `config/skills` y `config/skills/frontend-slides/plugins/...` |
| Coincidencias de `Identidad del MAS` | 16 archivos (10 skills + 6 agentes) |
| Coincidencias de `Contexto core` en `agent/` | 6 de 6 agentes |
| Frontmatter de `graphify` | `trigger: /graphify` presente; descripción de activación abierta |
| `commands/skill.md` | Escanea solo `~/.config/opencode/skills` y `.opencode/skills`; declara `agent: build` |
| Bloques `permission` de `sdd.md` y `documentation-orchestrator.md` | Reglas redundantes; estrategias `ask`/`deny` distintas; `webfetch: allow` general |
| `skills-backup/` | 2 copias obsoletas de 2026-07-07 (`git-commit-push`, `sdd-spec`) |
| `release-management/SKILL.md` | "investiga en la web" en descripción y en el paso 1.5.c |
| Claims de amplitud en descripciones | 5 coincidencias literales ("cualquier proyecto", "TODO lo …") |

Pendiente de verificación con ejecución (fuera del alcance de esta auditoría estática):

1. Precedencia real de los patrones `deny`/`allow` en OpenCode (H8).
2. Confirmación de si `build` es agente integrado del runtime (H7).
3. Tareas de referencia (positivas y negativas de activación) para medir éxito de
   tarea, activaciones incorrectas y coste de contexto antes y después de aplicar los
   cambios; no se atribuyen mejoras de precisión ni de coste sin esa medición.
4. Comprobación de referencias cruzadas y rutas de `references/` tras cualquier
   edición.
