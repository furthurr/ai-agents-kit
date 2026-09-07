# Workflows de Documentation Orchestrator

## Clasificador de intencion

| Peticion | Modo |
| --- | --- |
| "estado de la documentacion", "que falta", `sync-check` | `status` |
| "inicia la documentacion core" | `bootstrap-core` |
| "actualiza el core" | `sync-core` |
| "actualiza lo que tenemos", "todo lo existente" | `sync-existing` |
| "actualiza arquitectura/datos/UI/calidad/seguridad" | `sync-domain` |
| "listo para release", `release-check`, `pre-release check` | `release-check` |
| "feature", "bugfix", "requirements", "design/tasks de spec" | Derivar a SDD |

Si la intencion o el dominio no son claros, pregunta antes del Gate 0. No uses un
modo con escritura para resolver una ambiguedad.

"Sincroniza todo" es ambiguo: pregunta si significa solo carpetas existentes o
si desea inicializar ausentes. No existe un modo implicito que haga ambas cosas.

## Preflight permitido antes del Gate 0

El preflight puede:

- Resolver raiz Git/workspace y detectar proyectos independientes.
- Comprobar existencia de carpetas y leer solo sus READMEs/metadatos de estado.
- Ejecutar Git de lectura para `HEAD`, estado y nombres cambiados.
- Contar proyectos, dominios y archivos relevantes.

No puede escribir, cargar todos los especialistas, leer el repo completo ni
ejecutar auditorias. El objetivo es recomendar el modelo, no resolver la tarea.

## Nivel de modelo

| Tarea base | Nivel inicial |
| --- | --- |
| `status` | Bajo |
| `release-check` con documentacion verificable | Bajo |
| `sync-domain` con un dominio, marca valida y hasta 20 archivos relevantes | Bajo |
| `sync-core` incremental | Medio |
| `sync-existing` incremental | Medio |
| `bootstrap-core` pequeno/mediano | Medio |
| Auditoria inicial o completa de Quality/Security | Alto |
| Arquitectura grande/ambigua o monorepo complejo | Alto |

Sube un nivel, con tope `alto`, por cualquiera de estas condiciones relevantes:

- Varios proyectos independientes o monorepo ambiguo.
- Mas de 100 archivos relevantes.
- No hay marca util y hace falta barrido completo.
- Cambios cruzados entre cuatro o mas dominios.
- Es necesario reconstruir contratos, diagramas o inventarios extensos.
- El usuario solicita auditoria profunda/completa.

No subas por archivos ajenos al alcance. Un `release-check` no se vuelve auditoria
profunda: si la evidencia esta desfasada, falla o advierte y recomienda sincronizar.

Para operaciones compuestas, informa tambien niveles por fase cuando difieran.
Ejemplo: `bootstrap-core` puede recomendar `medio` global, `bajo` para Navigator y
`medio` para Architecture. El usuario puede mantener el nivel global o cambiarlo
por fase. Si el Gate 0 expuso la recomendacion de Navigator y fue confirmado, su
aviso de modelo queda satisfecho y no se repite.

### Salida y hard stop

```text
Preflight documental

Tarea detectada: <modo>
Alcance: <proyecto(s) y carpetas>
Complejidad: <baja|media|alta>
Modelo recomendado: <bajo|medio|alto>

Motivos:
- <1-3 razones verificables>

Antes de continuar:
1. Cambia manualmente al modelo recomendado y responde "listo".
2. Responde "continua con el actual" para conservarlo.
3. Indica otro alcance para recalcular.
```

Termina el turno despues de esta salida. El agente no puede cambiar el modelo.

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

### `status`

- Solo lectura y cero persistencia.
- Informa core, condicionales, assurance y contexto externo existente.
- Las carpetas externas (`.sdd/`, `.release/`, `graphify-out/`) se listan solo si
  afectan la consulta; no se juzgan como documentacion gestionada.
- Recomienda el siguiente modo minimo suficiente.

### `bootstrap-core`

- Solo considera `.navigator/` y `.architecture/` ausentes.
- Presenta propuesta y espera aprobacion antes de crear.
- Respeta el aviso/gate de bootstrap de Project Navigator y el estudio/propuesta
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
- En Quality/Security persiste solo findings aprobados y nunca entra en Fase B de
  remediacion de codigo.

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

## Gates tras seleccionar modelo

1. **G1 Plan global:** proyectos, dominios, orden y escrituras propuestas.
2. **G2 Especialista:** cada skill conserva su gate; Quality/Security confirman
   alcance de findings.
3. **G3 Fallo:** si una rama se bloquea, preguntar antes de continuar con ramas
   independientes.
4. **G4 Cierre:** verificar artefactos y evidencia antes del informe final.

El Gate 0 no sustituye ninguno de estos gates. Solo puede satisfacer otro aviso
de **modelo** si mostro la recomendacion de esa fase y el usuario la confirmo.

## Informe final compacto

Usa una tabla por proyecto:

| Carpeta | Estado inicial | Accion | Estado final | Evidencia/nota |
| --- | --- | --- | --- | --- |

Despues incluye solo si aplica:

- Bloqueos.
- Carpetas ausentes recomendadas.
- Findings nuevos/resueltos/pendientes por conteo, sin duplicar detalles.
- Siguiente accion minima.
