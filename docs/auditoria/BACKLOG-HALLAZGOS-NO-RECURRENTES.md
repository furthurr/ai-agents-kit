# Backlog de hallazgos específicos no recurrentes

- **Fecha:** 2026-10-10.
- **Revisión de vigencia/estado:** 2026-10-13, contraste de fuentes canónicas, CI v3.2.0, historial Git y configuración local OpenCode.
- **Alcance MAS:** 19 acciones FUT aplicables; FUT-07 queda excluido por corresponder a skills de terceros en la configuración local de OpenCode.
- **Estado FUT aplicable al MAS:** 4 cerrados (FUT-08/10/14/17); 7 implementados parcial o íntegramente con validación pendiente (FUT-01/02/04/05/09/11/20); 8 confirmados abiertos (FUT-03/06/12/13/15/16/18/19).
- **Revalidación base:** `main` HEAD `10373b3` (v3.2.0), CI SUCCESS [run 38352143368](https://github.com/furthurr/ai-agents-kit/actions/runs/38352143368); `test_documentation_core.py` 17/17 y `validate.py` correctos antes del cambio FUT-01 actual.
- **Revalidación FUT-01 local:** `test_context_efficiency.py` 12/12, `test_integrity.py` 416/416, `validate.py` correcto y enlaces 91/91. Cambios de FUT-01 están locales, sin CI remota ni smoke conductual.
- **Base:** los cinco informes originales de esta carpeta.
- **Resultado:** 20 acciones originales; FUT-14 se reabrió y corrigió el 2026-10-12; FUT-17 se cerró tras validar ejemplos reales del historial.
- **Estado inicial:** pendiente de verificar vigencia; ninguna remediación acreditada por esta síntesis.
- **Documento principal:** [Consolidado de hallazgos recurrentes](CONSOLIDADO-HALLAZGOS-RECURRENTES.md).

## 1. Propósito y reglas

Este documento conserva problemas y recomendaciones que no se repiten con el mismo significado concreto en otros informes. **Una única mención no implica menor importancia:** los IDs ambiguos de seguridad y la documentación desfasada pueden afectar decisiones operativas.

Algunos puntos pertenecen a familias recurrentes, pero tienen una acción específica única: por ejemplo, la activación amplia de Graphify está en REC-10; su campo `trigger` y comando no mapeado se conservan aquí como FUT-08.

- Se cuenta la fuente, no el número de párrafos que mencionan el punto.
- Los IDs `FUT-*` son de esta síntesis y deben vincularse a registros existentes, sin reemplazar IDs históricos.
- Las referencias de líneas corresponden a los informes originales. Comprobar las rutas citadas y el estado actual antes de implementar.
- Los puntos de MiMo afectan la instalación local de OpenCode y skills externas; no prueban un defecto de `canonical/`.
- Las hipótesis se mantienen como hipótesis. En particular, la ausencia de una definición local de `build` no demuestra que el agente integrado no exista.
- Las propuestas de umbrales o rutas de las fuentes no se convierten automáticamente en requisitos.

### Fuentes

| Clave | Informe |
|---|---|
| A | [Antigravity](AUDITORIA-MAS-ANTIGRAVITY.md) |
| D | [DeepSeek](AUDITORIA-MAS-DEEPSEEK.MD) |
| G | [GPT](AUDITORIA-MAS-GPT.md) |
| M | [MiMo](AUDITORIA-MAS-MIMO.MD) |
| E | [Estudio de agentes y skills](Estudio-agentes-y-skills-ai-agents-kit.md) |

## 2. Orden recomendado para retomar

Prioridad de atención, no severidad Sonar/OWASP. Cada entrada tiene **1/5 fuentes**.

| Orden | ID | Acción específica | Fuente | Prioridad |
|---:|---|---|:---:|---|
| 1 | FUT-12 | Reconciliar IDs de seguridad duplicados | E | Alta |
| 2 | FUT-01 | Separar consulta, implementación y mantenimiento en UI/datos | G | Alta |
| — | FUT-14 | Actualizar memoria documental y automatizar frescura | E | Cerrado tras corrección |
| 4 | FUT-06 | Resolver referencia a `OPENCODE.md` inexistente | M | Alta si sigue vigente |
| 5 | FUT-13 | Concretar/versionar checklists y evidencias | E | Media-alta |
| 6 | FUT-03 | Usar referencias de seguridad del estándar aplicable | G | Media-alta |
| 7 | FUT-18 | Leer mensajes completos para detectar incompatibilidades | E | Media-alta |
| 8 | FUT-02 | Evitar precarga conjunta de Git y release en Claude | G | Media |
| 9 | FUT-15 | Contextualizar reglas arquitectónicas y severidades | E | Media |
| 10 | FUT-17 | Clasificar commits por intención, no extensión | E | Media |
| 11 | FUT-05 | Continuar ramas independientes autorizadas ante bloqueos | G | Media |
| 12 | FUT-04 | Permitir ampliar presupuestos de navegación | G | Media |
| 13 | FUT-09 | Completar catálogo `/skill` y comprobar `build` | M | Media |
| 14 | FUT-08 | Resolver metadato/comando específico de Graphify | M | Media |
| 15 | FUT-11 | Acotar investigación web de releases | M | Media |
| 16 | FUT-19 | Incorporar evidencia visual y accesibilidad | E | Media |
| 17 | FUT-20 | Ampliar evidencia nativa de instaladores PowerShell | E | Media |
| 18 | FUT-16 | Ampliar calibración de esfuerzo SDD | E | Media-baja |
| 19 | FUT-10 | Gestionar backups obsoletos fuera del catálogo activo | M | Baja |

FUT-07 queda conservado en el anexo local de abajo y no participa en este orden del MAS.

### Aplicabilidad al MAS desarrollado — revisión 2026-10-13

| ID | ¿Aplica? | Alcance y motivo |
|---|---|---|
| REC-16 | Sí | Evalúa utilidad/coste del MAS en tareas reales. `developer-smoke.md` prescribe comparar baseline/post con consumo/tiempo del host, pero no hay ejecuciones/resultados; bytes/palabras siguen siendo solo proxy. |
| FUT-09 | Parcial: entorno local | Afecta el comando `/skill` de `~/.config/opencode/commands/skill.md`, no los artefactos distribuidos del MAS. Importa al usar el MAS junto a skills instaladas en `~/.agents/skills/`; el agente `build` sí existe. |
| FUT-07 | No; fuera de alcance del MAS | Es una skill de terceros en configuración local de OpenCode; no pertenece a `canonical/`, adapters ni generated del kit. Se retira de los totales/prioridades del MAS y se conserva solo como anexo local. |
| FUT-17 | Sí; cerrado | Cambios de comportamiento del MAS viven en prompts Markdown; el contrato y los commits `f432f4a` (`feat` de prompt) / `6f6f10d` (`docs` descriptivo) demuestran la clasificación por intención. |
| FUT-20 | Sí | Los instaladores PowerShell distribuyen el MAS en Windows; la cobertura nativa actual solo prueba Antigravity, no todos los wrappers del kit. |

## 3. Fichas de trabajo futuro

### FUT-01 — Seleccionar intención antes del flujo documental de UI/datos

- **Fuente:** G H03, líneas 126–163.
- **Hallazgo:** instrucciones como «si no existe, créala» pueden activar extracción o documentación ante una consulta o cambio puntual.
- **Ámbito:** skills canónicas `ui-design` y `data-api`.
- **Cómo resolver:** definir tres ramas breves: consulta sin persistencia; implementación localizada y verificación proporcional; documentación/sync autorizados. Condicionar creación de carpetas a la intención real y requisitos del proyecto.
- **Cuándo retomarlo:** junto a REC-03/REC-04 o antes de ampliar workflows de esos especialistas.
- **Cierre:** explicar DTOs y estilos sin crear carpetas; implementar un cambio puntual sin extracción global; inicializar documentación cuando se solicite explícitamente.
- **Implementación local 2026-10-13:** `ui-design` y `data-api` ahora separan consulta sin persistencia, implementación de producto mediante Developer y documentación/auditoría explícitamente solicitada; crear `.design/`/`.data/` requiere plan y aprobación documental. Se propagó a seis hosts.
- **Verificación:** `test_context_efficiency.py` 12/12; `test_integrity.py` 416/416; `validate.py` correcto; enlaces 94/94. **Estado:** implementado en fuente/distribuciones, runtime smoke pendiente; no cerrar hasta probar consulta sin escritura, implementación localizada y documentación solicitada en host real.

### FUT-02 — Corregir precarga de skills en Claude

- **Fuente:** G H05, 199–226.
- **Hallazgo:** el adaptador de `git-release-manager` precarga `git-commit` y `release-management`, aunque el agente indica seleccionar solo la aplicable.
- **Ámbito:** `adapters/claude/agents/git-release-manager.json` y capacidad efectiva de cargar skills.
- **Cómo resolver:** comprobar semántica vigente de `skills` y herramienta `Skill`; retirar precarga conjunta si la selección runtime es viable; cargar ambas solo cuando la operación lo requiera.
- **Cuándo retomarlo:** al trabajar REC-09 o medir contexto de Git con REC-16.
- **Cierre:** commit sin procedimiento de release precargado; release con disponibilidad de ambas cuando corresponda; aprobaciones conservadas.

### FUT-03 — Adaptar el contrato de findings al estándar aplicable

- **Fuente:** G H09, 341–370.
- **Hallazgo:** la skill permite tecnologías no móviles, pero la plantilla exige MASVS/MASWE, incentivando mapeos artificiales.
- **Ámbito:** skill `security` y plantilla de hallazgos.
- **Cómo resolver:** exigir estándar aplicable, versión/identificador y evidencia; añadir CWE cuando exista mapeo verificable; permitir declarar mapeos no disponibles.
- **Cuándo retomarlo:** antes de usar el flujo de seguridad en web/backend; coordinar con FUT-13.
- **Cierre:** hallazgos móviles con referencias pertinentes y hallazgos no móviles sin acrónimos forzados ni IDs inventados.
- **Distinción:** REC-11 trata acrónimos en identidad de otras skills, no el contrato de findings de seguridad.

### FUT-04 — Hacer ampliable el presupuesto de navegación

- **Fuente:** G H08, 306–338, especialmente 312 y 318–328.
- **Hallazgo:** máximos rígidos de capas/archivos pueden truncar investigaciones transversales.
- **Ámbito:** `project-navigator/SKILL.md`.
- **Cómo resolver:** convertir máximos en presupuesto inicial; justificar ampliación por fuentes necesarias; mantener lectura selectiva y referencias precisas.
- **Cuándo retomarlo:** al revisar REC-17 o ante una consulta transversal que el presupuesto no cubra.
- **Cierre:** consulta que requiere más de tres archivos resuelta con evidencia suficiente, sin volcar el repositorio.

### FUT-05 — Continuar trabajo independiente ya autorizado

- **Fuente:** G H08, 306–339, especialmente 313–314 y 318–339.
- **Hallazgo:** el orquestador exige una nueva decisión ante un bloqueo aunque otras ramas sean independientes y estén autorizadas.
- **Ámbito:** skill `documentation-orchestrator` y workflows.
- **Cómo resolver:** distinguir dependencias de trabajo paralelo independiente; continuar únicamente ramas autorizadas; informar bloqueos; pedir decisión si cambian alcance, dependencias o coste relevante.
- **Cuándo retomarlo:** al ajustar workflows multi-dominio.
- **Cierre:** una rama bloqueada no frena las independientes; las dependientes sí quedan detenidas; resultado final declara parciales y pendientes, sin éxito global ficticio.

### FUT-06 — Resolver steering local ausente

- **Fuente:** M H1, 35–49.
- **Hallazgo:** `opencode.json` declara `instructions: ["OPENCODE.md"]`, pero la auditoría no encontró el archivo en config ni proyecto.
- **Ámbito:** configuración local del usuario, no defecto canónico demostrado.
- **Cómo resolver:** confirmar reglas de resolución de rutas y existencia actual; crear steering mínimo en una ruta realmente cargada o retirar la referencia inválida; vincular cualquier bloque compartido a REC-09.
- **Cuándo retomarlo:** antes de depender de ese steering o centralizar allí instrucciones.
- **Cierre:** prueba de carga efectiva del archivo o eliminación de la dependencia; precedencias e identidad no se asumen por accidente.

### FUT-07 — Fuera de alcance del MAS: copias locales de `frontend-slides`

- **Fuente:** M H2, 51–67.
- **Hallazgo:** tres copias locales, una de ellas embebida como distribución plugin, crean riesgo de divergencia y posible ambigüedad de descubrimiento.
- **Cómo resolver:** inventariar contenido, versiones y consumidores; verificar qué directorios descubre el runtime; escoger fuente mantenida y separar exportes de distribución del catálogo activo.
- **Cuándo retomarlo:** en mantenimiento de instalación local o ante selección duplicada.
- **Cierre:** no hay copias activas competidoras sin justificación; exportes conservados donde sus consumidores los necesiten. No borrar una copia solo porque coincida el nombre.
- **Decisión de alcance (2026-10-13):** no pertenece al MAS distribuido; es una skill de terceros en configuración local de OpenCode. El usuario la excluye del plan de trabajo del MAS. No se movió ni borró copia; al revalidar, ya no existía en ninguno de los roots ni en backups. Una restauración requiere solicitud independiente y fuente/version aprobada.

### FUT-08 — Resolver `trigger` y comando de Graphify

- **Fuente:** M H4, 88–106.
- **Hallazgo:** `trigger: /graphify` no figura en la especificación citada y no hay comando correspondiente declarado en `commands/`.
- **Cómo resolver:** comprobar soporte real del host para el campo; retirarlo si no aporta funcionalidad o crear un comando válido si esa interfaz es requerida; tratar la descripción amplia mediante REC-10.
- **Cuándo retomarlo:** al normalizar frontmatters o habilitar `/graphify`.
- **Cierre:** invocación documentada y funcional o metadato sin efecto retirado; no declarar un fallo de runtime solo por un campo adicional.

### FUT-09 — Alinear descubrimiento manual y catálogo real

- **Fuente:** M H7, 150–165 y pendientes 274–275.
- **Hallazgo:** `/skill` omite `~/.agents/skills/`; `agent: build` no tiene definición local, pero puede ser integrado.
- **Cómo resolver:** contrastar directorios de descubrimiento soportados; añadir fuentes faltantes con etiqueta de origen y deduplicación; comprobar disponibilidad de `build` antes de cambiarlo.
- **Cuándo retomarlo:** al actualizar el comando `/skill` o instalar skills en nuevos orígenes.
- **Cierre:** catálogo manual coincide con skills disponibles y sus orígenes; comando ejecutable. No registrar «build inexistente» sin comprobar el runtime.

### FUT-10 — Gestionar backups obsoletos

- **Fuente:** M H9, 187–199.
- **Hallazgo:** backups de julio con nombres retirados quedan junto a la configuración activa, aunque la fuente indica que no los carga el catálogo.
- **Cómo resolver:** comprobar contenido y recuperabilidad; archivar fuera del árbol activo o aplicar una retención acordada; verificar disponibilidad de versiones históricas antes de eliminar.
- **Cuándo retomarlo:** mantenimiento de configuración y espacio, después de problemas funcionales.
- **Cierre:** copias históricas identificadas, recuperables cuando corresponda y fuera del catálogo activo. No atribuirles activaciones que el informe no observó.

### FUT-11 — Delimitar investigación web de releases

- **Fuente:** M H10, 201–215.
- **Hallazgo:** soporte de tecnologías nuevas mediante investigación web sin un límite explícito de fuentes/tiempo o alcance suficientemente claro.
- **Cómo resolver:** priorizar caché fiable y documentación oficial; acordar presupuesto de investigación y criterio de salida; validar perfil generado antes de aplicarlo; documentar fuentes y versión tecnológica.
- **Cuándo retomarlo:** antes de incorporar una tecnología no soportada.
- **Cierre:** perfil trazable y reutilizable; investigación no se expande silenciosamente; aplicación del perfil autorizada. Las «dos fuentes» propuestas por M son orientativas, no una garantía universal.

### FUT-12 — Garantizar IDs de seguridad inequívocos

- **Fuente:** E EST-003, 224–236.
- **Hallazgo:** problemas distintos comparten `SEC-0001` y `SEC-0002`; el tablero y el conjunto de findings no cubren el mismo alcance.
- **Cómo resolver:** inventariar registros; asignar IDs únicos; conservar aliases y referencias históricas con alcance explícito; generar índice general y validación de duplicados/estados.
- **Cuándo retomarlo:** antes de solicitar remediaciones por ID. **Prioridad alta aunque tenga una sola fuente.**
- **Cierre:** un ID identifica un único hallazgo; todos los alcances se localizan; pruebas detectan duplicación y discrepancia de estado; no se pierde trazabilidad al reconciliar.

### FUT-13 — Concretar checklists y evidencias anunciadas

- **Fuente:** E §2.1, 118 y EST-004, 238–250.
- **Hallazgo:** se anuncia cobertura móvil precargada sin checklist detallado y versionado suficiente; Code Review también necesita controles concretos y registros comprobables.
- **Cómo resolver:** distribuir controles, versiones, aplicabilidad, evidencias esperadas y fuentes oficiales; alinear descripción con cobertura real; incorporar validaciones mecánicas de registros donde aporten valor.
- **Cuándo retomarlo:** antes de afirmar cobertura reproducible de auditoría; coordinar con FUT-03/FUT-15.
- **Cierre:** las plataformas anunciadas disponen de checklist verificable; informe distingue comprobado, no aplicable y no verificable; cobertura no depende solo del conocimiento del modelo.

### FUT-14 — Reconciliar memoria documental con los contratos vigentes

- **Fuente:** E §2.1, 117; EST-007, 280–296; Bloque D, 372.
- **Hallazgo:** backlog y contexto conservan inventarios/modos obsoletos: cuatro profundidades SDD, solo SDD como escritor de producto, cinco plataformas y omisión de Antigravity.
- **Cómo resolver:** identificar fuente vigente de inventario y responsabilidades; actualizar documentos operativos; separar historia de instrucciones actuales; automatizar comprobaciones de frescura, inventario e índices Navigator.
- **Cuándo retomarlo:** antes de confiar en esos contextos para nuevas decisiones y tras modificar contratos.
- **Cierre:** documentos operativos y fuentes coinciden; baseline verificable o límites declarados; inconsistencias detectadas automáticamente cuando sea viable. No sobrescribir historia como si hubiera sido errónea en su fecha.
- **Revisión 2026-10-13:** se corrigió la deriva de `.navigator/ai-context.md` y `.architecture/07-crosscutting.md` contra manifest, `scope-depth.md`, catálogo y guía de uso. El cambio de Developer en v3.2 no altera el inventario ni los modos.
- **Estado:** cerrado tras corregir la deriva; baseline de fuentes `10373b3`. `test_documentation_core.py` detecta desajustes de inventario/modos; la regeneración general de mapas sigue manual (`update.strategy: manual`). CI v3.2 SUCCESS.

### FUT-15 — Contextualizar severidad y preferencias arquitectónicas

- **Fuente:** E §2.4, 153–168 y §2.1, 118.
- **Hallazgo:** preferencias de módulos/composition root se presentan como universales; colores hardcodeados o dominios públicos pueden recibir severidad crítica sin un riesgo equivalente.
- **Cómo resolver:** distinguir preferencia, deuda de mantenibilidad y riesgo concreto; definir severidad por impacto/exposición/contexto; añadir ejemplos y excepciones; revisar plantillas de UI, datos y barra de calidad SDD.
- **Cuándo retomarlo:** antes de ordenar remediaciones por severidad de esos registros.
- **Cierre:** dominio público no se equipara automáticamente a credencial; duplicación visual tiene severidad justificada; decisiones arquitectónicas admiten contexto y razones.

### FUT-16 — Ampliar calibración de esfuerzo SDD

- **Fuente:** E §2.5, 170–176.
- **Hallazgo:** ejemplos concentrados en lógica, persistencia y coordinación no representan bien UI, accesibilidad, rendimiento, contratos y refactors.
- **Cómo resolver:** añadir casos contrastados de esos dominios; comprobar consistencia de recomendaciones; evaluar si mostrar siempre una nota numérica ayuda al usuario.
- **Cuándo retomarlo:** al cambiar rúbrica o incorporar nuevos dominios.
- **Cierre:** casos diversos conducen a recomendaciones comprensibles; la nota no se presenta como predicción de tokens, tiempo o coste.

### FUT-17 — Clasificar commits por cambio de comportamiento

- **Fuente:** E §2.6, 178–186.
- **Hallazgo:** «solo `.md` → `docs`» falla en un producto cuyo comportamiento reside en prompts Markdown.
- **Cómo resolver:** elegir tipo por intención y efecto, no extensión; incluir ejemplos de cambios de instrucciones, documentación y correcciones de comportamiento.
- **Cuándo retomarlo:** junto a REC-15 o antes de automatizar changelog.
- **Cierre:** cambios funcionales en prompts reciben `feat`/`fix` cuando corresponda; documentación puramente descriptiva sigue usando `docs`.
- **Verificación actual:** `canonical/skills/git-commit/SKILL.md:221-222` ordena clasificar por intención. `f432f4a feat(developer)` aporta un cambio de comportamiento en prompts y `6f6f10d docs(readme)` modifica solo el README. Estado **Cerrado**.

### FUT-18 — Detectar cambios incompatibles en mensajes completos

- **Fuente:** E §2.6, 180–186.
- **Hallazgo:** el flujo de release recomienda `git log --oneline` y después analizar footers `BREAKING CHANGE`, que ese formato no muestra.
- **Cómo resolver:** leer subject y cuerpo completos para el rango de release; detectar `!` y footers según convención; conservar referencias a commits que justifican el bump.
- **Cuándo retomarlo:** antes de la siguiente selección automatizada de versión.
- **Cierre:** fixture con footer incompatible provoca la propuesta de bump adecuada aunque el título no tenga `!`; título, cuerpo y rango están cubiertos.

### FUT-19 — Incorporar evidencia visual y accesibilidad

- **Fuente:** E §2.1, 120 y Bloque D, 377.
- **Hallazgo/recomendación:** complementar documentación visual con verificaciones observadas de teclado, foco, escalado de texto y tamaños de interacción según plataforma.
- **Cómo resolver:** seleccionar controles aplicables; registrar capturas o evidencia reproducible, entorno y resultados; separar auditoría visual de conclusiones no comprobadas sobre accesibilidad global.
- **Cuándo retomarlo:** en cambios visuales relevantes o auditorías de UI solicitadas.
- **Cierre:** controles aplicables tienen evidencia y resultado; limitaciones explícitas; no inferir comportamiento de teclado solo de una captura.

### FUT-20 — Ampliar evidencia nativa de PowerShell

- **Fuente:** E Bloque C, 361–366, especialmente 365.
- **Hallazgo/recomendación:** extender las pruebas nativas a instaladores que aún no tienen esa evidencia.
- **Cómo resolver:** inventariar scripts y cobertura por entorno; ejecutar casos de instalación, referencias faltantes, backups y dry-run en PowerShell compatible; registrar versión y plataforma.
- **Cuándo retomarlo:** al modificar instaladores o antes de afirmar compatibilidad nativa completa.
- **Cierre:** matriz por instalador con evidencia ejecutada o bloqueo explícito; pruebas en otro shell no se presentan como validación nativa.
- **Relacionado:** REC-05 cubre la integridad común; REC-08, la disciplina de evidencia. Esta entrada conserva el trabajo específico de PowerShell.

## 4. Cobertura de los informes originales

Esta tabla permite comprobar que la consolidación no pierde los bloques de hallazgos o recomendaciones. Los resúmenes y listas finales remiten a los mismos temas y no aumentan sus frecuencias.

| Fuente / bloque original | Destino en la síntesis |
|---|---|
| A Hallazgos 1–8 | 1 → REC-09/11; 2 → REC-15; 3 → REC-13; 4 → REC-12; 5 → REC-14; 6 → REC-17; 7 → REC-04; 8 → REC-10. |
| D AUD-01 a AUD-05 | REC-01, REC-02, REC-03, REC-11, REC-09, respectivamente. |
| D AUD-06 a AUD-10 | REC-12, REC-13, REC-04, REC-14, REC-15, respectivamente. |
| D AUD-11 a AUD-15 | REC-10, REC-06, REC-05, REC-07, REC-16/17, respectivamente. |
| G H01 a H05 | REC-03; REC-04; FUT-01; REC-01; FUT-02. |
| G H06 a H10 | REC-09/14; REC-10; FUT-04/05; FUT-03; REC-08. |
| M H1 a H6 | FUT-06; FUT-07; REC-09; REC-10/FUT-08; REC-10; REC-09. |
| M H7 a H11 | FUT-09; REC-02; FUT-10; FUT-11; REC-10. |
| E §2.1, mejoras por agente | SDD → REC-09/12 y FUT-16; orquestador → FUT-14; Code Review → FUT-13/15; datos → REC-04; UI → FUT-19; Git/release → REC-01 y FUT-17/18. |
| E §2.2 a §2.6 | REC-09; REC-16; FUT-15; FUT-16; FUT-17/18. |
| E EST-001 a EST-005 | REC-01; REC-02; FUT-12; FUT-13; REC-05. |
| E EST-006 a EST-009 | REC-04; FUT-14; REC-06; REC-07. |
| E §4 y Bloque C | REC-08; trabajo nativo específico → FUT-20. |
| E Bloque D | REC-09/16 y FUT-14/15/16/17/18/19; simplificación de interacción SDD vinculada a REC-09/12. |

Los elementos positivos de los informes se resumen como principios a conservar en el documento principal. Las cifras de ahorro estimadas por A no se consideran mejoras demostradas; REC-16 exige medición.

## 5. Registro para futuras sesiones

Aplicar el [Protocolo de remediación](PROTOCOLO-REMEDIACION.md). La sesión coordinadora mantiene el tablero; la implementadora registra su trabajo en `seguimiento/<ID>.md` usando la [plantilla de resultado](PLANTILLA-RESULTADO.md).

Estados: **pendiente → confirmado → en curso → corregido en rama → integrado pendiente de verificación → cerrado**. Usar **bloqueado** con causa y estado previo, o **no vigente** con evidencia actual. `Pendiente` incluye verificar vigencia. No crear fichas vacías para todos los IDs: abrirlas al asignar la sesión.

| ID | Estado | Responsable / rama | Última actualización | Evidencia | Próxima acción |
|---|---|---|---|---|---|
| FUT-01 | Implementado; smoke pendiente | Coordinación / `main` worktree | 2026-10-13 | UI/Data separan consulta, implementación y documentación aprobada; propagado a seis hosts. Tests estáticos 12/12, integrity 416/416, validate y links 94/94 pasan | Ejecutar los tres escenarios de cierre en host; CI remota posterior al cambio aún no disponible. |
| FUT-02 | Implementado y distribuido; runtime pendiente | Coordinación / `main` | 2026-10-12 | Claude adapter no precarga ambas skills; `Skill` sigue disponible; contrato de carga bajo demanda incluido en `test_context_efficiency.py` (11/11). `shutil.which("claude")` da `None` en este entorno | Probar carga dinámica cuando haya host/CLI Claude disponible. |
| FUT-03 | Confirmado | Coordinación / `main` | 2026-10-12 | La plantilla de findings sigue usando una referencia móvil como forma principal y no fija claramente estándar aplicable, versión y mapeo no disponible | Coordinar contrato de findings con FUT-13; permitir mapeos aplicables/no aplicables sustentados. |
| FUT-04 | Implementado y distribuido; smoke pendiente | Coordinación / `main` | 2026-10-12 | Navigator tiene presupuesto inicial ampliable; suite contractual actual `test_context_efficiency.py` 11/11. No se ejecutó una consulta real de más de tres archivos | Contrastar con una consulta transversal real instrumentada. |
| FUT-05 | Implementado y distribuido; smoke pendiente | Coordinación / `main` | 2026-10-12 | Workflows preservan ramas independientes autorizadas; contrato `test_context_efficiency.py` 11/11. No se ejecutó un flujo conversacional bloqueado/independiente | Confirmar en smoke que pregunta solo ante cambios de alcance, dependencias o autorización. |
| FUT-06 | Confirmado | Coordinación / configuración OpenCode local | 2026-10-12 | `~/.config/opencode/opencode.json` todavía referencia `OPENCODE.md`; no se encontró ese archivo en la configuración ni en el workspace actual | Confirmar resolución efectiva de ruta y retirar o satisfacer la referencia local. |
| FUT-07 | Fuera de alcance del MAS (local) | Configuración OpenCode, no `main` | 2026-10-13 | Skill de terceros; su ausencia actual en `.agents` y `.config/opencode` corresponde al entorno local, no a los artefactos distribuidos del kit | Mantenerla fuera del plan MAS; restaurarla solo en una tarea separada y con fuente/version aprobada. |
| FUT-08 | Cerrado localmente | Coordinación / configuración OpenCode local | 2026-10-12 | Skill Graphify cargada en la sesión actual; frontmatter no contiene `trigger`; la descripción está limitada a solicitudes explícitas | Ninguno para el hallazgo del metadato; configuración local, no artefacto versionado del kit. |
| FUT-09 | Implementado parcialmente; catálogo pendiente | Coordinación / configuración OpenCode local | 2026-10-12 | `opencode agent list` confirma `build (primary)`; `commands/skill.md` cataloga `~/.config/opencode/skills/` y `.opencode/skills/`, pero omite `~/.agents/skills/` | Añadir origen `.agents` con procedencia/deduplicación si el catálogo debe cubrir todas las skills disponibles. |
| FUT-10 | Cerrado localmente | Coordinación / configuración OpenCode local | 2026-10-12 | Backups fechados permanecen en `skills-backup/` con sus `SKILL.md`; separados de `skills/` y del catálogo activo. Se conserva recuperación, sin borrar archivos | Ninguno; mantener separados del catálogo activo. |
| FUT-11 | Implementado y cargado; prueba de flujo pendiente | Coordinación / `main` y configuración local | 2026-10-12 | Fuentes canónica/global limitan búsqueda a caché y hasta dos fuentes oficiales; la skill está cargada en la sesión actual. No se ha ejecutado una release real no soportada | Probar el flujo en un proyecto fixture y registrar perfil/fuentes sin exceder alcance ni aplicar escrituras. |
| FUT-12 | Confirmado | Coordinación / `main` | 2026-10-12 | `.security/findings/` aún contiene dos archivos `SEC-0001` y dos `SEC-0002`; el tablero maestro solo cubre F07 y no indexa todos los findings | Inventariar referencias, asignar IDs únicos/aliases e incluir validación de duplicados y estados; requiere aprobación de remediación de seguridad. |
| FUT-13 | Confirmado | Coordinación / `main` | 2026-10-12 | Las fuentes actuales no distribuyen checklists concretos y versionados para toda la cobertura anunciada de auditoría/Code Review | Identificar controles, versiones, aplicabilidad y evidencia antes de afirmar cobertura reproducible. |
| FUT-14 | Cerrado tras corrección de deriva | Coordinación / baseline `10373b3` | 2026-10-13 | `.navigator/ai-context.md` actualizado a 11/5/6 y `direct`/`tiny`/`lite` + `standard` legacy; `.architecture/07-crosscutting.md` actualizado; `test_documentation_core.py` 17/17; CI v3.2 SUCCESS | Regeneración general Navigator sigue manual; reabrir si aparece otra deriva; conservar documentos históricos. |
| FUT-15 | Confirmado | Coordinación / `main` | 2026-10-12 | Criterios de severidad actuales describen niveles generales, sin resolver explícitamente preferencias arquitectónicas frente a riesgos/contexto como dominio público | Contextualizar ejemplos, severidad e impacto por exposición verificable. |
| FUT-16 | Confirmado | Coordinación / `main` | 2026-10-12 | La rúbrica de esfuerzo conserva contrastes concentrados en F10/X13; no aparecen ejemplos de UI, accesibilidad, rendimiento y contratos | Añadir casos diversos y comprobar recomendaciones consistentes, sin convertir la nota en predicción de coste/tiempo. |
| FUT-17 | Cerrado | Coordinación / `main` `10373b3` | 2026-10-13 | `git-commit` clasifica por intención; `f432f4a feat(developer)` incluye cambios funcionales de prompts y `6f6f10d docs(readme)` modifica solo README | Ninguna; reabrir si reaparece la clasificación basada solo en extensión. |
| FUT-18 | Confirmado | Coordinación / `main` | 2026-10-12 | `release-management` aún ejemplifica `git log --oneline` y no exige leer cuerpos/footer completos aunque su tabla menciona `BREAKING CHANGE` | Leer mensajes completos del rango y validar fixture con footer breaking sin `!` en el título. |
| FUT-19 | Confirmado | Coordinación / `main` | 2026-10-12 | UI define WCAG y accesibilidad pertinente, pero no un protocolo de controles observados/evidencia visual por plataforma | Seleccionar controles aplicables y registrar entorno, capturas/resultados y límites. |
| FUT-20 | Implementado parcialmente; PowerShell nativo pendiente | Coordinación / CI `main` | 2026-10-13 | Tests locales instaladores 250/250 y Antigravity 22/22; CI v3.2 (run 38352143368) prueba Windows Antigravity, pero no los demás wrappers PowerShell de Copilot/OpenCode/Kiro/Claude/Pi | Añadir/ejecutar los demás instaladores en PowerShell Windows, o registrar bloqueos por wrapper. |

### Historial de cambios de estado

| Fecha | ID | Transición | Responsable / baseline / rama | Resumen y evidencia | Pendientes |
|---|---|---|---|---|---|
| 2026-10-10 | FUT-01 a FUT-20 | Inicialización → Pendiente | Preparación documental | Tablero individual preparado, sin fixes ejecutados. | Asignación y verificación de vigencia. |
| 2026-10-11 | FUT-14 | Pendiente → No vigente | Contraste de las fuentes operativas actuales | Navigator y arquitectura listan seis plataformas; catálogo/uso describen `direct`, `lite`, `standard` y UI/Data como especialistas implementadores. Las referencias contrarias están en documentos históricos/specs cerradas, no en el contexto operativo actual. | Ninguna corrección activa; conservar la evidencia histórica. |
| 2026-10-12 | FUT-14 | No vigente → Confirmado → Cerrado | Revalidación y actualización documental coordinada; baseline fuentes `8fea7bb` | Se detectó deriva nueva en `.navigator/ai-context.md` (10/6 skills-agentes y sin Tiny) y `.architecture/07-crosscutting.md`; ambos corregidos contra manifest, contratos SDD y catálogo vigente. Aserción enfocada 1/1; enlaces 91/91. | No hay corrección activa para esta deriva; la regeneración general de mapas sigue manual y el test verifica inventario/modos, no toda frescura. La suite documental completa falla por un diff local posterior de Developer. |
| 2026-10-11 | FUT-02/04/05/08/11 | Pendiente → Implementado localmente | Adaptador Claude, Navigator/orchestrator y skills OpenCode locales | Preload Claude eliminado; presupuestos cualitativos/ampliables; tareas independientes continúan; Graphify acotado; investigación web de release limitada a caché y dos fuentes oficiales | Render/host smoke cuando se integre; skills globales OpenCode son locales y requieren reinicio. |
| 2026-10-12 | FUT-01/03/06/07/12/13/15/16/18/19 | Pendiente → Confirmado | Revisión coordinadora sobre `main` `8fea7bb` y configuración local | Se comprobó vigencia en skills/plantillas, presencia de IDs duplicados, referencia OPENCODE.md ausente, copias frontend-slides y cobertura/evidencia que falta; CI actual SUCCESS | Siguen abiertos; ejecutar las acciones descritas en el tablero. FUT-12 requiere gate de remediación de seguridad. |
| 2026-10-12 | FUT-08 | Implementado localmente; reinicio pendiente → Cerrado localmente | Configuración OpenCode global actual | Skill Graphify disponible en la sesión y metadato `trigger` ausente; descripción acotada | Ninguno para retirar el metadato; sigue siendo una configuración personal no versionada. |
| 2026-10-12 | FUT-09 | Pendiente → Implementado parcialmente | Configuración OpenCode actual | `build` aparece como agente primary; comando `/skill` aún omite `~/.agents/skills/` | Corregir el catálogo si debe enumerar también ese origen. |
| 2026-10-12 | FUT-10 | Pendiente → Cerrado localmente | `~/.config/opencode/skills-backup/` | Backups fechados y recuperables están fuera de `skills/` y del catálogo `/skill`; no se eliminó contenido | Ninguno; conservar la separación. |
| 2026-10-12 | FUT-11 | Implementado; reinicio pendiente → Cargado; prueba pendiente | Skill local activa y fuente canónica | Límite de dos fuentes oficiales presente; skill visible/cargada en la sesión actual | Probar el flujo en la siguiente release de tecnología no soportada. |
| 2026-10-12 | FUT-17 | Pendiente → Implementado en fuente; verificación pendiente | `canonical/skills/git-commit/SKILL.md` | Regla por intención/no extensión está presente. | Verificar ejemplos contrastados en el historial antes de cerrar. |
| 2026-10-12 | FUT-17 | Implementado en fuente; verificación pendiente → Cerrado | `main` `10373b3`; historial `f432f4a` y `6f6f10d` | Cambio funcional de prompts clasificado `feat(developer)` y cambio solo documental clasificado `docs(readme)`; ambos coinciden con el criterio. | Ninguno; reabrir si reaparece clasificación basada en extensión. |
| 2026-10-12 | FUT-20 | Pendiente → Implementado parcialmente | CI actual `38323348763` | Job nativo Windows valida Antigravity; los demás wrappers PowerShell no tienen ejecución nativa demostrada | Completar evidencia nativa por wrapper. |
| 2026-10-13 | FUT-01 | Confirmado → Implementado en fuentes/distribuciones; smoke pendiente | `main` worktree, cambio coordinado con REC-01 | Skills UI/Data separan consulta read-only, implementación por Developer y documentación solicitada; `test_context_efficiency.py` 12/12, integrity 416/416, validate y links pasan | Ejecutar consulta, cambio localizado y documentación explícita en host real antes de cerrar. |
| 2026-10-13 | FUT-07 | Confirmado → Inventario completado; decisión de consolidación pendiente | Configuración local OpenCode y `~/.agents/skills/` | Los dos árboles son idénticos (163 archivos, sin Git); incluyen bundles plugin idénticos; OpenCode 1.18.34 advierte skills duplicadas | Acordar fuente raíz y tratamiento del bundle antes de mover o archivar copias. |
| 2026-10-13 | FUT-07 | Inventario duplicado → Bloqueado por ausencia de la copia elegida | Revisión posterior de `~/.agents`, `~/.config/opencode/skills`, `skills-backup` y `.skill-lock.json` | Ya no se encuentra ningún árbol frontend-slides en esas rutas; no hay copia de respaldo ni origen/version fijados en el lockfile | Confirmar restauración desde una fuente/version acordada o declarar que el skill fue retirado. |
| 2026-10-13 | FUT-07 | Bloqueado local → Excluido del alcance MAS | Decisión del usuario | `frontend-slides` es una skill de terceros del entorno OpenCode local, no artefacto distribuido por el MAS | No incluir en el plan ni en los totales del MAS; mantenimiento local queda fuera de este alcance. |

Al retomar una entrada: comprobar vigencia y consumidores, localizar deuda existente, acotar el cambio, ejecutar verificación proporcional y registrar resultado. La coordinadora actualiza estados e historial al recibir evidencia y verificar la integración. Actualizar ambas síntesis si una nueva auditoría convierte un punto específico en recurrente.
