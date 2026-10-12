# Backlog de hallazgos específicos no recurrentes

- **Fecha:** 2026-10-10.
- **Base:** los cinco informes originales de esta carpeta.
- **Resultado:** 20 acciones específicas identificadas en una sola fuente.
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
| 3 | FUT-14 | Actualizar memoria documental y automatizar frescura | E | Alta |
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
| 16 | FUT-07 | Reconciliar copias de `frontend-slides` | M | Media |
| 17 | FUT-19 | Incorporar evidencia visual y accesibilidad | E | Media |
| 18 | FUT-20 | Ampliar evidencia nativa de instaladores PowerShell | E | Media |
| 19 | FUT-16 | Ampliar calibración de esfuerzo SDD | E | Media-baja |
| 20 | FUT-10 | Gestionar backups obsoletos fuera del catálogo activo | M | Baja |

## 3. Fichas de trabajo futuro

### FUT-01 — Seleccionar intención antes del flujo documental de UI/datos

- **Fuente:** G H03, líneas 126–163.
- **Hallazgo:** instrucciones como «si no existe, créala» pueden activar extracción o documentación ante una consulta o cambio puntual.
- **Ámbito:** skills canónicas `ui-design` y `data-api`.
- **Cómo resolver:** definir tres ramas breves: consulta sin persistencia; implementación localizada y verificación proporcional; documentación/sync autorizados. Condicionar creación de carpetas a la intención real y requisitos del proyecto.
- **Cuándo retomarlo:** junto a REC-03/REC-04 o antes de ampliar workflows de esos especialistas.
- **Cierre:** explicar DTOs y estilos sin crear carpetas; implementar un cambio puntual sin extracción global; inicializar documentación cuando se solicite explícitamente.

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

### FUT-07 — Reconciliar copias de `frontend-slides`

- **Fuente:** M H2, 51–67.
- **Hallazgo:** tres copias locales, una de ellas embebida como distribución plugin, crean riesgo de divergencia y posible ambigüedad de descubrimiento.
- **Cómo resolver:** inventariar contenido, versiones y consumidores; verificar qué directorios descubre el runtime; escoger fuente mantenida y separar exportes de distribución del catálogo activo.
- **Cuándo retomarlo:** en mantenimiento de instalación local o ante selección duplicada.
- **Cierre:** no hay copias activas competidoras sin justificación; exportes conservados donde sus consumidores los necesiten. No borrar una copia solo porque coincida el nombre.

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
| FUT-01 | Pendiente | — | 2026-10-10 | — | Coordinar con REC-03/04. |
| FUT-02 | Pendiente | — | 2026-10-10 | — | Comprobar precarga efectiva de Claude. |
| FUT-03 | Pendiente | — | 2026-10-10 | — | Coordinar contrato de findings con FUT-13. |
| FUT-04 | Pendiente | — | 2026-10-10 | — | Revisar presupuesto de navegación. |
| FUT-05 | Pendiente | — | 2026-10-10 | — | Delimitar dependencias del orquestador. |
| FUT-06 | Pendiente | — | 2026-10-10 | — | Confirmar ruta y carga efectiva del steering local. |
| FUT-07 | Pendiente | — | 2026-10-10 | — | Inventariar copias y consumidores. |
| FUT-08 | Pendiente | — | 2026-10-10 | — | Comprobar soporte de metadato y comando. |
| FUT-09 | Pendiente | — | 2026-10-10 | — | Contrastar catálogo y agente integrado. |
| FUT-10 | Pendiente | — | 2026-10-10 | — | Verificar recuperabilidad de backups. |
| FUT-11 | Pendiente | — | 2026-10-10 | — | Acotar investigación de nuevas tecnologías. |
| FUT-12 | Pendiente | — | 2026-10-10 | — | Inventariar IDs antes de remediar por referencia. |
| FUT-13 | Pendiente | — | 2026-10-10 | — | Identificar cobertura real y versiones. |
| FUT-14 | Pendiente | — | 2026-10-10 | — | Contrastar inventario y memoria vigente. |
| FUT-15 | Pendiente | — | 2026-10-10 | — | Contextualizar ejemplos y severidad. |
| FUT-16 | Pendiente | — | 2026-10-10 | — | Añadir casos diversos a la rúbrica. |
| FUT-17 | Pendiente | — | 2026-10-10 | — | Coordinar con REC-15. |
| FUT-18 | Pendiente | — | 2026-10-10 | — | Revisar lectura del rango de release. |
| FUT-19 | Pendiente | — | 2026-10-10 | — | Seleccionar controles visuales aplicables. |
| FUT-20 | Pendiente | — | 2026-10-10 | — | Inventariar evidencia nativa por instalador. |

### Historial de cambios de estado

| Fecha | ID | Transición | Responsable / baseline / rama | Resumen y evidencia | Pendientes |
|---|---|---|---|---|---|
| 2026-10-10 | FUT-01 a FUT-20 | Inicialización → Pendiente | Preparación documental | Tablero individual preparado, sin fixes ejecutados. | Asignación y verificación de vigencia. |

Al retomar una entrada: comprobar vigencia y consumidores, localizar deuda existente, acotar el cambio, ejecutar verificación proporcional y registrar resultado. La coordinadora actualiza estados e historial al recibir evidencia y verificar la integración. Actualizar ambas síntesis si una nueva auditoría convierte un punto específico en recurrente.
