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
3. **G3 Fallo:** si una rama se bloquea, preguntar antes de continuar con ramas
   independientes.
4. **G4 Cierre:** verificar artefactos y evidencia antes del informe final;
   validacion tecnica, sin pregunta humana adicional automatica.

El preflight técnico no sustituye estos controles ni acredita autorizacion.

## Informe final compacto

Usa una tabla por proyecto:

| Carpeta | Estado inicial | Accion | Estado final | Evidencia/nota |
| --- | --- | --- | --- | --- |

Despues incluye solo si aplica:

- Bloqueos.
- Carpetas ausentes recomendadas.
- Findings nuevos/resueltos/pendientes por conteo, sin duplicar detalles.
- Siguiente accion minima.
