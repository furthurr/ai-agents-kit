# Estudio y crítica constructiva de agentes y skills — AI Agents Kit

- **Fecha del estudio:** 2026-10-09.
- **Proyecto:** `ai-agents-kit` / MAS (Multi-Agent System).
- **Repositorio analizado:** `/Users/pedrogomezvasquez/Documents/Repositorios/GITHUBREPOS/ai-agents-kit`.
- **Inventario revisado:** 6 agentes, 10 skills y distribución para 6 plataformas, según `canonical/manifest.json`.
- **Método:** lectura de fuentes canónicas, referencias principales, adaptadores, herramientas, pruebas, CI y documentación; comparaciones puntuales con artefactos generados.
- **Verificación:** revisión estática. Las ejecuciones de hosts se valoraron mediante la evidencia documentada; no se ejecutaron pruebas nuevas durante el estudio.
- **Estado de las acciones propuestas:** pendientes.

Las referencias `ruta:línea` son relativas al repositorio analizado y corresponden a los archivos observados durante el estudio. Antes de implementar una acción, comprobar su vigencia en las fuentes actuales.

## Resumen ejecutivo

**El proyecto tiene una base sólida como kit de trabajo con IA:** especialización, procedimientos reutilizables, contexto persistente y un pipeline de distribución bien pensado.

Su principal debilidad es que **varias garantías todavía dependen de que el modelo obedezca las instrucciones**, mientras que la evidencia de comportamiento real y la consistencia de los registros necesitan fortalecerse.

Conviene conservar la arquitectura canónica, la separación agente/skill y la trazabilidad. El próximo salto de calidad está en hacer esas reglas **más verificables, consistentes y económicas de utilizar**.

## Inventario de agentes y skills

| Agente | Skills principales | Responsabilidad |
|---|---|---|
| `sdd` | `sdd-spec` | Alcance, requisitos, diseño, tareas, implementación y verificación trazable. |
| `documentation-orchestrator` | `documentation-orchestrator`, `architecture`, `project-navigator` | Consultas core y mantenimiento de documentación e índices. |
| `code-review` | `code-quality`, `security` | Revisión de calidad y seguridad; registros separados y remediación guiada. |
| `data-api` | `data-api` | Datos, APIs, contratos, modelos y persistencia. |
| `ui-design` | `ui-design` | Sistema visual, componentes, tokens, accesibilidad visual y UX. |
| `git-release-manager` | `git-commit`, `release-management` | Commits, push, versiones, tags y CHANGELOG. |

Plataformas declaradas: Copilot, OpenCode, Kiro, Claude Code, Pi y Antigravity. La presencia de una distribución no acredita por sí sola comportamiento equivalente en todos los hosts.

---

## 1. Puntos buenos

### 1.1. Arquitectura de distribución bien planteada

La separación:

```text
canonical/ → adapters/ → generated/ → instalación
```

evita mantener manualmente seis versiones de los mismos procedimientos.

Además, `tools/validate.py:241` comprueba la reproducibilidad renderizando en un directorio temporal y comparando hashes. Es un control técnico útil para detectar diferencias entre las fuentes y lo distribuido.

**Valor:** facilita corregir y evolucionar el kit de manera consistente.

### 1.2. Buena diferenciación entre agente y skill

El agente define su rol y límites; la skill desarrolla el procedimiento, las plantillas y los estándares.

También es acertada la consolidación de roles:

- `code-review` reúne calidad y seguridad, conservando sus procedimientos separados.
- `documentation-orchestrator` atiende arquitectura y navegación mediante skills independientes.
- `git-release-manager` coordina commits y releases.

**Valor:** reduce agentes redundantes sin perder especialización.

### 1.3. Contexto persistente que aporta continuidad

Las carpetas `.architecture/`, `.navigator/`, `.quality/`, `.security/`, `.data/`, `.design/` y `.sdd/` ofrecen una estructura predecible para conservar conocimiento entre sesiones.

Navigator distingue contexto ausente, desfasado y no verificable, y permite continuar con fuentes directas. Esto está definido en `canonical/skills/project-navigator/SKILL.md:40`.

**Valor:** ayuda a evitar que cada sesión comience desde cero.

### 1.4. Buenos controles SDD contra el cumplimiento ficticio

Son especialmente valiosas estas reglas:

- No marcar tareas completas sin artefacto o evidencia.
- No llamar TDD a pruebas añadidas sin observar un fallo previo.
- No utilizar pruebas tautológicas.
- Conservar evidencia histórica cuando cambia un requisito.
- Separar profundidad documental de estrategia de pruebas.

Referencias: `canonical/skills/sdd-spec/references/integrity-gate.md:5` y `canonical/skills/sdd-spec/references/testing.md:50`.

**Valor:** combate problemas frecuentes de los agentes: declarar éxito prematuramente y generar pruebas que aparentan verificar.

### 1.5. Estándares pertinentes

EARS, arc42, C4, ADRs, OpenAPI, JSON Schema, Conventional Commits, SemVer y OWASP proporcionan vocabulario y estructuras reconocibles.

**Valor:** los resultados pueden ser revisados por personas y no quedan sujetos exclusivamente al estilo del modelo.

### 1.6. Pruebas útiles de infraestructura

El proyecto incluye pruebas negativas del validador, instalación en perfiles temporales, preservación de backups y comprobaciones de `dry-run`.

Por ejemplo, `tools/test_antigravity_install.py:173` contempla recursos de referencia ausentes y comprueba que la instalación falle antes de escribir.

**Valor:** existe trabajo de ingeniería más allá de redactar prompts.

### 1.7. Honestidad respecto a los límites de la evidencia

El README distingue distribución, pruebas con fixtures y comportamiento real en el host. Los documentos de smoke mantienen escenarios pendientes en lugar de declararlos aprobados.

Referencias: `README.md:17` y `docs/code-review-smoke.md:3`.

**Valor:** permite evaluar la madurez del proyecto sin confundir intención con resultados.

---

## 2. Puntos que se pueden mejorar

### 2.1. Mejora principal por agente

| Agente | Evaluación constructiva |
|---|---|
| **SDD** | Tiene rigor y trazabilidad, pero acumula decisiones de alcance, ejecutor, profundidad, esfuerzo, pruebas y gates. Conviene simplificar la interacción y automatizar comprobaciones mecánicas. |
| **Documentation Orchestrator** | La autoridad de cada carpeta está bien definida. El siguiente paso es automatizar frescura, validación de índices e inventarios para reducir mantenimiento manual. |
| **Code Review** | La separación de dominios es buena. Necesita checklists concretos, criterios de severidad contextualizados y registros de hallazgos verificables automáticamente. |
| **Data & API** | Cubre contratos, DTOs y persistencia. Scalar debería ser una integración opt-in con un alcance de escritura explícito. |
| **UI Design** | Es fuerte como documentación del sistema visual. Puede incorporar evidencia visual y verificaciones de teclado, foco, escalado de texto y tamaños de interacción, según plataforma. |
| **Git & Release Manager** | Tiene procedimientos claros, pero necesita corregir la política de secretos y hacer más fiable el análisis de commits para versionado. |

### 2.2. Reducir duplicación dentro de las fuentes canónicas

Aunque se evita duplicar prompts entre plataformas, dentro de `canonical/` se repiten:

- Identidad del MAS.
- Contexto core compartido.
- Detección de proyectos.
- Reglas de derivación a SDD.
- Confirmaciones y límites generales.

Por ejemplo, el bloque de contexto compartido aparece en los seis agentes.

**Propuesta:** mantener fragmentos comunes que el renderer ensamble y reducir instrucciones repetidas cuando se cargan agente y skill juntos. Los artefactos distribuidos pueden seguir siendo autosuficientes.

**Beneficio:** menos lugares que actualizar y menor riesgo de contradicciones.

### 2.3. Medir el coste real por flujo

`tools/measure_context.py:16` suma palabras de agentes, skills y referencias. Es útil como inventario, pero no representa el contexto realmente consumido por una tarea ni incluye todos los recursos anidados.

**Propuesta:** medir consultas representativas y registrar:

- Archivos y referencias leídos.
- Tokens de entrada y salida.
- Interacciones necesarias con el usuario.
- Tiempo y corrección del resultado.
- Comparación con una ejecución sin el kit.

Esto permitiría demostrar cuándo el contexto persistente compensa su coste de mantenimiento.

### 2.4. Contextualizar reglas de arquitectura y severidad

Algunas recomendaciones están redactadas como reglas universales:

- Un único módulo/adaptador toca almacenamiento.
- Un único composition root.
- Colores hardcodeados en muchos lugares pueden clasificarse como críticos.
- Dominios reales aparecen junto a secretos dentro de la severidad crítica de datos.

Referencias:

- `canonical/skills/sdd-spec/references/quality-bar.md:8`.
- `canonical/skills/ui-design/references/templates.md:106`.
- `canonical/skills/data-api/references/templates.md:93`.

**Propuesta:** distinguir preferencia arquitectónica, defecto de mantenibilidad y riesgo concreto. Un dominio público no equivale a una credencial; una duplicación visual tampoco tiene siempre impacto crítico.

### 2.5. Ampliar la calibración de esfuerzo más allá de ReserveLab

La rúbrica indica que no predice tokens, tiempo o coste. Eso es positivo. Sin embargo, sus referentes se concentran en lógica, persistencia, concurrencia y coordinación.

Referencia: `canonical/skills/sdd-spec/references/feature-level.md:22`.

**Propuesta:** añadir contrastes representativos de UI, accesibilidad, rendimiento, contratos y refactors. Evaluar también si publicar siempre una nota numérica ayuda al usuario a elegir el flujo.

### 2.6. Hacer los commits coherentes con la naturaleza del proyecto

La regla «solo archivos `.md` → `docs`» de `canonical/skills/git-commit/SKILL.md:243` es demasiado simple para este repositorio: **los prompts Markdown contienen comportamiento del producto**.

Además, el comando `git log ... --oneline` recomendado por release no muestra los footers `BREAKING CHANGE` que después se pide analizar.

Referencias: `canonical/skills/release-management/SKILL.md:185` y `:249`.

**Propuesta:** clasificar commits por intención y leer mensajes completos para detectar cambios incompatibles.

---

## 3. Problemas que se tienen que solucionar

Los identificadores `EST-*` pertenecen a este estudio. La prioridad indica el orden recomendado de trabajo; no sustituye la severidad de Sonar u OWASP ni los IDs existentes del proyecto.

### EST-001 — La política de Git permite incluir secretos con autorización

- **Prioridad:** alta.
- **Estado:** pendiente.
- **Evidencia:** `canonical/skills/git-commit/SKILL.md:34` y `:105`; `canonical/skills/release-management/SKILL.md:314` reutiliza esa verificación.

La skill dice «Nunca bloquees el flujo: el usuario decide» y permite incluir archivos sensibles con autorización explícita.

**Problema:** contradice la política general de no exponer secretos y convierte una autorización conversacional en excepción para publicar credenciales.

**Solución propuesta:** distinguir archivos potencialmente sensibles de secretos reales. Los secretos reales deben excluirse, sustituirse por referencias o placeholders y detectarse mediante un control automatizado.

**Criterio de cierre:** la política es coherente entre Git, release y seguridad; un fixture con credenciales ficticias detectables bloquea su inclusión, y se documenta el tratamiento de archivos públicos que solo parecen sensibles.

### EST-002 — Los límites “inviolables” no tienen enforcement uniforme

- **Prioridad:** alta.
- **Estado:** pendiente.
- **Evidencia:** `adapters/copilot/agents/code-review.json:7`, `adapters/claude/agents/code-review.json:7`, `adapters/kiro/agents/code-review.json:5` y `adapters/opencode/agents/code-review.json:7`.

Code Review dispone de edición y ejecución en varios adaptadores. OpenCode solicita aprobación para edición y Bash, pero los controles no son equivalentes entre plataformas.

**Problema:** las mismas instrucciones no garantizan las mismas restricciones efectivas. El tratamiento del workspace y de la web como fuentes de instrucciones necesita una frontera de confianza explícita.

La explotación no está demostrada por esta revisión; la falta de uniformidad sí es visible. Las políticas efectivas del host deben verificarse.

**Solución propuesta:** definir capacidades mínimas por modo, aplicar restricciones donde el host las permita y probar escrituras o comandos fuera de alcance con fixtures inocuos.

**Criterio de cierre:** existe una matriz de capacidades y límites por host, con evidencia de las aprobaciones efectivas y de los intentos fuera de alcance. Los controles no soportados quedan documentados como limitaciones.

### EST-003 — IDs de seguridad duplicados

- **Prioridad:** alta para la trazabilidad.
- **Estado:** pendiente.
- **Evidencia:** `.security/findings/SEC-0001-capacidades-amplias-code-review.md:1` y `.security/findings/SEC-0001-candidate-controls-evaluation-database.md:1`.

Dos problemas distintos utilizan `SEC-0001`. También hay dos `SEC-0002`. El tablero actual está limitado a F07, mientras la carpeta conserva hallazgos de otros alcances.

**Problema:** una instrucción como «remedia SEC-0001» es ambigua. El identificador deja de ser una referencia estable.

**Solución propuesta:** garantizar unicidad dentro del proyecto, identificar explícitamente el alcance y generar un índice general desde los findings. Preservar referencias históricas al reconciliar los IDs.

**Criterio de cierre:** no hay IDs ambiguos; el índice permite localizar todos los hallazgos y sus alcances; una comprobación detecta duplicados e inconsistencias de estado.

### EST-004 — Checklist móvil precargado sin concreción suficiente

- **Prioridad:** media-alta.
- **Estado:** pendiente.
- **Evidencia:** `canonical/skills/security/SKILL.md:48`.

Se anuncia un checklist MASVS/MASWE/Top 10 precargado por plataforma. En los archivos de esa skill se encontraron los ocho grupos MASVS y plantillas, pero no un checklist detallado y versionado de controles y pruebas por plataforma.

**Problema:** el modelo debe completar la cobertura con su conocimiento. Esto reduce reproducibilidad y puede producir auditorías diferentes entre modelos.

**Solución propuesta:** distribuir controles concretos, versión del estándar, criterios de aplicabilidad, evidencias esperadas y enlaces oficiales. Ajustar la descripción a la cobertura realmente incluida.

**Criterio de cierre:** cada plataforma anunciada dispone de un checklist reproducible con versión y fuentes verificables; el informe distingue controles comprobados, no aplicables y no verificables.

### EST-005 — El preflight compartido puede aceptar skills incompletas

- **Prioridad:** media-alta.
- **Estado:** pendiente.
- **Evidencia:** `tools/install_preflight.py:97` y `:126`; comprobaciones adicionales en `scripts/install/antigravity.ps1:146`.

La comprobación común verifica principalmente la existencia de `SKILL.md` y los agentes. No comprueba de forma general todos los recursos referenciados ni su contenido. Antigravity incorpora comprobaciones adicionales de recursos y bytes en sus wrappers.

**Problema:** puede existir el archivo principal de una skill y faltar una referencia necesaria sin que el preflight compartido lo detecte.

**Solución propuesta:** centralizar la validación del árbol completo y sus hashes para todas las plataformas, antes y después de copiar.

**Criterio de cierre:** una referencia ausente o alterada se detecta en cada distribución; una fuente incompleta falla antes de escribir; una copia incompleta no declara instalación exitosa.

### EST-006 — Alcances incompatibles entre el handoff de datos y Scalar

- **Prioridad:** media.
- **Estado:** pendiente.
- **Evidencia:** `canonical/skills/documentation-orchestrator/references/handoff.md:54`, `canonical/skills/data-api/SKILL.md:185` y `canonical/skills/data-api/references/api-docs.md:35`.

El contrato limita el `write_scope` de `data-api` a `.data/`, pero la documentación REST pide crear un lanzador en `scripts/`.

**Problema:** no queda resuelto cómo completar esa operación respetando el alcance recibido.

**Solución propuesta:** establecer una extensión explícita del alcance, colocar el lanzador dentro de una ruta autorizada o convertirlo en una operación opt-in separada.

**Criterio de cierre:** el contrato y la skill expresan una regla compatible; un handoff restringido a `.data/` no escribe en `scripts/`; la creación opcional del lanzador tiene autorización y ruta explícitas.

### EST-007 — Memoria documental del proyecto desfasada

- **Prioridad:** media.
- **Estado:** pendiente.
- **Evidencia:** `docs/mejoras.md:246`, `.navigator/ai-context.md:15` y `.architecture/README.md:17`.

Ejemplos comprobados:

- El backlog atribuye cuatro profundidades a SDD y dice que es el único que escribe producto; el contrato actual tiene tres profundidades y UI/Data también permiten implementar.
- Navigator enumera cinco plataformas.
- El contexto de arquitectura omite Antigravity.

**Problema:** otros agentes consumen estos documentos como contexto. La información desactualizada puede propagarse a sus decisiones.

**Solución propuesta:** reconciliar el backlog con los contratos actuales y automatizar las comprobaciones de inventario y referencias obsoletas.

**Criterio de cierre:** documentos operativos y fuentes coinciden en inventario, modos y responsabilidades; el historial está identificado como histórico; las marcas de sincronización representan un baseline verificable o declaran sus límites.

### EST-008 — Render no transaccional

- **Prioridad:** media.
- **Estado:** pendiente.
- **Evidencia:** `tools/render.py:78`; el proyecto también lo registra en `.architecture/arch-tech-debt.md:18`.

El renderer elimina la salida de una plataforma antes de reconstruirla. Una excepción puede dejar salidas parciales o versiones mezcladas entre plataformas.

**Solución propuesta:** generar en staging, validar y publicar al completar. Definir si la publicación es atómica por plataforma o para la matriz completa.

**Criterio de cierre:** fallos controlados durante la generación no sustituyen una distribución válida por contenido parcial; la recuperación está probada y documentada.

### EST-009 — Importación que sigue enlaces simbólicos

- **Prioridad:** baja.
- **Estado:** pendiente.
- **Evidencia:** `tools/import_installed.py:50` y `.security/findings/SEC-0003-importador-sigue-enlaces.md`.

El importador copia sin exigir que las rutas resueltas permanezcan dentro del origen autorizado. Puede importar contenido externo a la skill.

El riesgo observado es de copia local inadvertida; no implica que se haya producido una filtración.

**Solución propuesta:** rechazar enlaces o validar su destino antes de copiar, con una política explícita para enlaces internos y externos.

**Criterio de cierre:** fixtures con enlaces a destinos externos no copian contenido ajeno; la política y los errores son claros; el dry-run conserva cero escrituras.

---

## 4. Brecha de evidencia de comportamiento real

Las pruebas de distribución y contratos textuales son útiles, pero no demuestran por sí solas que un LLM respete el flujo en una sesión real.

Evidencias del alcance actual:

- `tools/test_code_review_contract.py:2` describe sus pruebas como contratos estáticos, no prueba de comportamiento runtime.
- `docs/code-review-smoke.md:3` mantiene sus escenarios sin ejecución en un host real para esa feature.
- `docs/documentation-orchestrator-smoke.md:190` registra escenarios del contrato actual como pendientes.
- `docs/sdd-smoke.md` mantiene matrices pendientes y distingue evidencia histórica de escenarios actuales.
- `docs/antigravity-smoke.md:4` mantiene pendiente el runtime de la aplicación aunque existan pruebas nativas de scripts.

**Trabajo recomendado:** seleccionar escenarios representativos, ejecutarlos en hosts reales y registrar versión, fuente probada, petición, herramientas observadas, cambios de archivos y resultado. Conservar fallos y ejecuciones incompletas.

**Criterio de cierre:** las afirmaciones de compatibilidad se vinculan a una matriz de evidencia fechada por host y versión, sin extrapolar pruebas de copia de archivos a comportamiento del modelo.

---

## 5. Lista de trabajo para retomar

### Bloque A — Confianza y límites

- [ ] **EST-001:** unificar la política de secretos entre Git, release y seguridad.
- [ ] **EST-002:** definir y comprobar capacidades efectivas por modo y host.
- [ ] **EST-003:** reconciliar IDs de seguridad y crear un índice verificable de todos los alcances.

### Bloque B — Integridad del procedimiento y distribución

- [ ] **EST-004:** concretar y versionar los checklists móviles anunciados.
- [ ] **EST-005:** validar recursos completos y bytes en el preflight compartido.
- [ ] **EST-006:** resolver el alcance de escritura del lanzador Scalar.
- [ ] **EST-007:** actualizar contexto y backlog frente al catálogo vigente.
- [ ] **EST-008:** hacer robusta la publicación de artefactos ante fallos del render.
- [ ] **EST-009:** controlar enlaces y rutas en la importación.

### Bloque C — Evidencia real

- [ ] Ejecutar los smoke tests pendientes de los contratos actuales.
- [ ] Documentar límites y resultados por host y versión.
- [ ] Ampliar pruebas nativas de PowerShell a los instaladores que aún no tienen esa evidencia.
- [ ] Comprobar handoffs y gates con escenarios observados, además de contratos estáticos.

### Bloque D — Simplificación y utilidad

- [ ] Consolidar fragmentos compartidos y reducir instrucciones duplicadas.
- [ ] Simplificar la interacción SDD conservando decisiones y gates relevantes.
- [ ] Automatizar frescura, inventarios y validación de índices Navigator.
- [ ] Medir contexto, interacciones, tiempo y calidad por flujo representativo.
- [ ] Contextualizar severidades y reglas arquitectónicas.
- [ ] Ampliar ejemplos de esfuerzo a UI, accesibilidad, rendimiento y refactors.
- [ ] Clasificar commits por intención y analizar mensajes completos para el bump.
- [ ] Incorporar evidencia visual y verificaciones de accesibilidad según plataforma.

## 6. Registro de seguimiento

Completar una fila cuando se trabaje una acción. Mantener los checkboxes abiertos hasta contar con la evidencia del criterio de cierre correspondiente.

| Fecha | Acción / EST-ID | Estado | Cambios realizados | Evidencia / commit | Siguiente paso |
|---|---|---|---|---|---|
| — | — | Pendiente | — | — | — |

## Conclusión

La arquitectura canónica, la separación de responsabilidades y la trazabilidad son activos que merece la pena conservar. El orden recomendado es:

1. Corregir secretos y límites efectivos de herramientas.
2. Restablecer la integridad de IDs, checklists, alcances e instalación.
3. Ejecutar los escenarios conversacionales pendientes con evidencia por host y versión.
4. Simplificar instrucciones, automatizar frescura y medir utilidad real.

**Objetivo:** que el buen diseño del kit se convierta en resultados verificables, consistentes y sostenibles para quien lo utiliza.
