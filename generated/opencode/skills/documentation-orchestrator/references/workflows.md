# Workflows de Documentation Orchestrator

## Clasificador de intencion

| Peticion | Modo |
| --- | --- |
| "estado de la documentacion", "que falta", `sync-check` | `status` |
| "explica las capas", "localiza el módulo", "investiga dependencias", `inspect` | `inspect` |
| "inicia la documentacion core" | `bootstrap-core` |
| "actualiza el core" | `sync-core` |
| "actualiza lo que tenemos", "todo lo existente" | `sync-existing` |
| "actualiza arquitectura/datos/UI/calidad/seguridad" | `sync-domain` |
| "listo para release", `release-check`, `pre-release check` | `release-check` |
| "feature", "bugfix", "requirements", "design/tasks de spec" | Derivar a SDD |

Si la intencion o el dominio no son claros, pregunta antes de actuar. No uses un
modo con escritura para resolver una ambiguedad.

Una petición puntual de crear o actualizar el `README.md` raíz (también `readme.md`)
o mantener documentación Markdown bajo `docs/` (incluidos READMEs e índices)
se limita a los archivos y cambios aprobados. «Documenta el README.md» solicita
escritura documental; no se clasifica como consulta `inspect`. No
activa bootstrap ni sincroniza dominios no solicitados. Conserva el preflight,
el plan global y la gestión de `AGENTS.md` descritos aquí; no modifica código ni
configuración aunque estén dentro de `docs/`. Las capacidades del host deben
permitir tanto las guías como `AGENTS.md`: un parche con varias rutas necesita
permiso para todas, no basta con comprobar únicamente `AGENTS.md`.

Sin intención específica, conserva `status` como default. Una pregunta core
concreta usa `inspect`; no convierte `status` en investigación general.

"Sincroniza todo" es ambiguo: pregunta si significa solo carpetas existentes o
si desea inicializar ausentes. No existe un modo implicito que haga ambas cosas.

## Preflight técnico permitido

El preflight puede:

- Resolver raiz Git/workspace y detectar proyectos independientes.
- Comprobar existencia de carpetas y leer solo sus READMEs/metadatos de estado.
- Ejecutar Git de lectura para `HEAD`, estado y nombres cambiados.
- Contar proyectos, dominios y archivos relevantes.

No puede escribir, cargar todos los especialistas, leer el repo completo ni
ejecutar auditorias. Su objetivo es delimitar la operación, identificar evidencia
disponible y determinar qué decisiones o autorizaciones reales siguen pendientes.

Para dimensionar técnicamente el trabajo, considera proyectos independientes,
cantidad de archivos relevantes, disponibilidad de marcas útiles, cantidad de
dominios afectados, necesidad de reconstruir contratos/diagramas/inventarios y si
se solicita auditoría profunda o completa. Excluye archivos ajenos al alcance.
Un `release-check` sigue siendo una comprobación documental; evidencia desfasada,
fallida o incompleta se informa y puede motivar recomendar sincronización, no una
auditoría implícita.

## Estados documentales

| Estado | Criterio |
| --- | --- |
| `Vigente` | Marca verificable y sin cambios relevantes posteriores, incluidos cambios locales. |
| `Desfasado` | Hay cambios relevantes posteriores a la marca. |
| `Ausente` | La carpeta esperada no existe. |
| `No aplica` | No hay senales del dominio condicional. |
| `Sin marca` | Existe documentacion, pero no tiene baseline de sincronizacion. |
| `No verificable` | La evidencia disponible no permite afirmar frescura. |
| `Ambiguo` | No se pudo resolver proyecto, alcance o propiedad. |
| `Bloqueado` | La operacion fallo o un gate no fue aprobado. |

Para READMEs con hash, compara el hash con `HEAD` filtrando rutas del dominio y
revisa tambien el working tree. Para Navigator, comprueba `config.yaml`, capas
obligatorias y `source_commit` en `ai-context.md`, `module-map.json` y cada indice
habilitado que lo soporte. Solo puede ser `Vigente` si esas marcas representan el
mismo baseline aplicable y no hay cambios relevantes posteriores o locales.
`generated_at` informa antiguedad, pero nunca sustituye al commit. Si falta una
marca requerida, usa `No verificable`; no inventes `Vigente`.

Cambios locales relevantes impiden demostrar `Vigente`. Una sincronizacion puede
documentarlos con aprobacion, pero debe cerrar como pendiente de baseline Git; no
registre `HEAD` como si incluyera contenido sin commit. Para un release-check
verificable: commit de producto → sync documental → commit documental → check.

## Semantica de modos

### `inspect`

- Solo lectura y cero persistencia: no bootstrap, sync, export ni configuración
  de herramientas. No modifica producto, tests, CI ni instrucciones del proyecto.
- Ejecuta localmente `architecture` para explicar arquitectura y
  `project-navigator` para localizar módulos/símbolos o investigar impacto, bajo
  demanda; usa ambas secuencialmente solo si la pregunta lo necesita, sin handoff.
- Sigue [contexto compartido](project-context.md): steering y README de
  arquitectura primero, capas mínimas y comprobación de frescura; ausencia,
  desfase, ambigüedad o datos ilegibles degradan a fuentes directas sin bloqueo
  por sí solos y sin generación automática.
- Conserva gates reales de mantenimiento y export de cada skill.
- En peticion mixta, responde la lectura separable y pide autorización pendiente
  para mantenimiento; la consulta no la concede ni ejecuta escrituras.
- Cierra con hallazgos, fuentes, confianza/limitaciones y recomendaciones opcionales.
  No crea handoff ni estado `delivered`; responder no acredita sincronizacion
  ni permite declarar contexto vigente sin evidencia.

### `status`

- Solo lectura y cero persistencia.
- Informa core, condicionales, assurance y contexto externo existente.
- Las carpetas externas (`.sdd/`, `.release/`, `graphify-out/`) se listan solo si
  afectan la consulta; no se juzgan como documentacion gestionada.
- Recomienda el siguiente modo minimo suficiente.

### Gestión del bloque documental en `AGENTS.md`

El `documentation-orchestrator` es el único responsable de crear y mantener la
guía portable de documentación en el `AGENTS.md` raíz del proyecto resuelto.
Navigator detecta y lee ese archivo como fuente externa, pero no lo exporta ni lo
sobrescribe.

- En toda operación aprobada que cree o actualice documentación, incluye la ruta
  de `AGENTS.md` y esta escritura en el plan global antes de empezar. La aprobación
  global existente cubre la guía si su acción y ruta aparecen en ese plan; no
  añade un gate separado.
- Si un plan ya aprobado omitió esa ruta o acción, solicita ampliar su aprobación
  antes de escribir el archivo; no interpretes la aprobación de carpetas como
  autorización implícita ni cierres omitiendo la guía en silencio.
- Después de las actualizaciones documentales aprobadas, construye una guía breve
  desde carpetas, READMEs y contratos realmente verificados. Describe propósito,
  puntos de entrada, responsable y cómo distinguir fuentes de verdad de índices
  auxiliares; debe poder usarse sin instalar el MAS. Solo lista carpetas presentes.
  Si `.sdd/` o `.release/` están presentes, identifícalas como workflows externos a
  este orquestador, sin sincronizarlas.
- Gestiona únicamente el bloque entre `<!-- ai-agents-kit:documentation:start -->`
  y `<!-- ai-agents-kit:documentation:end -->` en el `AGENTS.md` raíz:
  - Si falta el archivo, créalo con un único bloque gestionado.
  - Si existe sin bloque, añade el bloque y preserva el contenido existente.
  - Si existe exactamente un par válido, reemplaza solo su interior y preserva
    todo el texto exterior.
  - Si el contenido resultante es igual, no escribas el archivo.
  - Ante marcadores incompletos, duplicados o mal formados, o instrucciones
    incompatibles, no escribas; informa el conflicto y pide una decisión.
  - Si `AGENTS.md` es enlace simbólico, no es archivo regular o es ilegible,
    no sigas el enlace ni modifiques el destino; informa el bloqueo.
- Verifica al cierre el contenido resultante, un único par válido de marcadores
  y la preservación del texto exterior existente. Si los permisos del host impiden
  editarlo, informa el bloqueo; no eludas la restricción mediante otras herramientas.
- No copies README/specs completos, no inventes carpetas y no incluyas secretos.
- `inspect`, `status` y `release-check` son solo lectura; nunca crean ni actualizan
  `AGENTS.md`. La instalación del kit tampoco modifica archivos del proyecto.
- No crees ni actualices `CLAUDE.md`, `GEMINI.md`, Copilot ni otros archivos de
  instrucciones de host dentro de esta entrega.

El campo histórico `sources.export_agents_md` de Navigator es legado ignorado; no
habilita una segunda vía de escritura ni autoriza modificar la configuración del
proyecto consumidor.

### `bootstrap-core`

- Solo considera `.navigator/` y `.architecture/` ausentes.
- Presenta propuesta y espera aprobacion antes de crear.
- Respeta la autorizacion de bootstrap de Project Navigator y el estudio/propuesta
  inicial de Architecture.
- Si Navigator ya existia al iniciar, no lo refresca ni sobrescribe; recomienda
  `sync-core` si debe incorporar la nueva documentacion de Architecture.
- No inicializa Data, Design, Quality ni Security; solo las recomienda cuando
  sean aplicables o convenientes.

### `sync-core`

- Actualiza `.navigator/` y/o `.architecture/` solo si ya existen y estan
  desfasados o el usuario confirma un estado no verificable.
- Reporta el core ausente sin crearlo.

### `sync-existing`

- Selecciona entre Navigator, Architecture, Data, Design, Quality y Security
  exclusivamente las carpetas que ya existen.
- Tras el triage, omite carpetas vigentes y dominios sin cambios relevantes.
- Nunca crea una carpeta ausente; la recomienda con prioridad y motivo.
- En Quality/Security persiste todos los findings verificados dentro del plan
  aprobado sin pedir filtros de severidad; nunca entra en Fase B de remediacion.
  Ambos dominios se derivan a `code-review` cuando se elige handoff; se combinan
  solo con accion, proyecto y via coincidentes, sin incluir carpetas ausentes.

### `sync-domain`

- Requiere una lista explicita de dominios.
- Si la carpeta no existe, propone usar el especialista para inicializarla y se
  detiene; no convierte silenciosamente `sync-domain` en bootstrap.
- Aplica la misma deteccion incremental y gates que `sync-existing`.

### `release-check`

Solo lectura. Empieza por el estado documental y consume findings existentes; no
reescanea el codigo ni ejecuta `release-management`.

Resultados:

- `APTO`: no hay bloqueadores ni advertencias.
- `APTO CON ADVERTENCIAS`: no hay bloqueadores, pero falta evidencia opcional.
- `NO APTO`: existe al menos un bloqueador.

Bloqueadores por defecto:

- Cualquier core cuyo estado no sea `Vigente`, incluidos `Sin marca`,
  `No verificable`, `Ambiguo` o `Bloqueado`.
- Cualquier carpeta documental existente y aplicable esta desfasada.
- Cualquier dominio aplicable esta `Ambiguo` o `Bloqueado`.
- Hay cambios locales relevantes sin baseline Git verificable.
- Hallazgo `Critica` o `🔴` abierto en `.security/`.
- Hallazgo `Blocker` o `🔴` abierto en `.quality/`.
- Spec SDD declarada para la release sin verificacion/cierre verificable.

Advertencias por defecto:

- Quality o Security no inicializadas: riesgo no evaluado.
- Data/Design aplicables pero ausentes.
- Estado `Sin marca` o `No verificable` en un dominio no core.
- No se puede asociar con certeza una spec activa a la release.

No comprueba version, changelog, tag ni publicacion. Deriva esas tareas a
`release-management` despues de obtener un resultado apto.

## Gates de ejecución

1. **G1 Plan global:** proyectos, dominios, orden y escrituras propuestas;
   espera aprobacion antes de escribir, reutilizando autorizacion efectiva de la
   misma operacion y alcance en la sesion.
2. **G2 Especialista:** cada skill conserva sus decisiones pendientes;
   Quality/Security reutilizan la autorizacion documental del mismo alcance en
   la sesion y no vuelven a seleccionar severidades. Un handoff no acredita por
   si solo la autorizacion; `gate_state` sigue siendo contexto.
3. **G3 Fallo:** marca la rama bloqueada y continúa las ramas independientes ya
   autorizadas. Pregunta solo si cambian dependencias, alcance o autorización; el
   cierre global debe indicar resultados parciales.
4. **G4 Cierre:** verificar artefactos y evidencia antes del informe final;
   en operaciones de escritura incluye el resultado del bloque de `AGENTS.md`,
   sus marcadores y la preservación del texto exterior. No declares la operación
   completamente entregada si la guía sigue pendiente o bloqueada.
   Validacion tecnica, sin pregunta humana adicional automatica.

El preflight técnico no sustituye estos controles ni acredita autorizacion.

## Informe final compacto

Usa una tabla por proyecto:

| Carpeta | Estado inicial | Accion | Estado final | Evidencia/nota |
| --- | --- | --- | --- | --- |

En operaciones de escritura añade siempre una fila para `AGENTS.md`: creado,
actualizado, sin cambios, pendiente de autorización o bloqueado, con evidencia
o motivo. La tabla puede incluir archivos además de carpetas. No fuerces una
escritura si la guía ya coincide con las fuentes verificadas.

Despues incluye solo si aplica:

- Bloqueos.
- Carpetas ausentes recomendadas.
- Findings nuevos/resueltos/pendientes por conteo, sin duplicar detalles.
- Siguiente accion minima.
