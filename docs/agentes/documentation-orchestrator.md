# Documentation Orchestrator

## Resumen

| Campo | Información |
|---|---|
| ID | `documentation-orchestrator` |
| Skill propia | [`documentation-orchestrator`](../../canonical/skills/documentation-orchestrator/SKILL.md) |
| Propósito | Resolver consultas de arquitectura/navegación y coordinar estado, bootstrap y sincronización documental |
| Rol | Clasifica, ordena y conserva los gates de especialistas |
| No gestiona | `.sdd/`, `.release/` ni `graphify-out/` |

Es la entrada responsable del core, incluso para consultas puntuales. Ejecuta
localmente las skills separadas `architecture` y `project-navigator`, cargadas
bajo demanda; conservan autoridad sobre `.architecture/` y `.navigator/`.
También coordina otros dominios mediante sus skills o los agentes vigentes
Data & API, UI Design y Code Review, sin duplicar acciones.

## Cuándo usarlo

- Para saber si la documentación está actualizada (`status` / `sync-check`).
- Para explicar capas, localizar módulos o investigar dependencias (`inspect`).
- Para inicializar el core documental (`.navigator/` + `.architecture/`).
- Para sincronizar las carpetas documentales existentes.
- Para actualizar dominios concretos, como arquitectura y seguridad.
- Para comprobar si la documentación cumple el gate previo a una release.

Si la petición es una feature o un bugfix, redirige al agente SDD. Si es un commit,
una versión o un tag, redirige a Git & Release Manager.

## Modos

| Modo | Qué hace |
|---|---|
| `status` | Solo lectura: inventario, aplicabilidad y frescura. |
| `inspect` | Consulta e investigación core de solo lectura, sin bootstrap, sync, exportación ni handoff core. |
| `bootstrap-core` | Propone crear únicamente `.navigator/` y `.architecture/`. |
| `sync-core` | Actualiza el core existente y recomienda el ausente. |
| `sync-existing` | Actualiza solo las carpetas documentales que ya existen. |
| `sync-domain` | Actualiza los dominios solicitados explícitamente. |
| `release-check` | Comprueba documentación y riesgos existentes sin versionar ni publicar. |

## Flujo de ejecución

1. Hace un preflight barato y de solo lectura, sin recomendar ni seleccionar modelos.
2. En `inspect`, `status` y `release-check`, inspecciona e informa sin escrituras. Para modos
   con escritura presenta el plan global de proyectos, dominios y orden, y espera
   su aprobación antes de escribir.
3. Ejecuta especialistas en secuencia y conserva los gates propios de cada uno;
   una autorización efectiva del mismo alcance en la sesión puede reutilizarse.
4. Verifica artefactos y evidencia antes de declarar un dominio completado.

El orden normal es skill Architecture local, Data & API si aplica, UI Design si
aplica, Code Review para calidad/seguridad seleccionadas y skill Project Navigator
local al final. El core está formado por las dos skills; Data y Design son
condicionales; Quality y Security son assurance recomendado.

Cuando el usuario solicita continuar con el especialista real —o hacen falta su
rol o permisos— en datos, UI o calidad/seguridad, emite un bloque **handoff** con identificador, origen/destino,
acción/motivo, proyecto, contexto, alcance de lectura/escritura y confirmación.
En ese caso no ejecuta la misma acción: espera un `Handoff Result` correlacionado.
El formato y las reglas viven en
[`references/handoff.md`](../../canonical/skills/documentation-orchestrator/references/handoff.md).

`write_scope` documenta la frontera esperada, pero no reemplaza los permisos del
host ni los gates del especialista.
Calidad y seguridad conservan sus skills y se derivan al mismo agente `code-review`;
solo se agrupan con acción, proyecto y vía coincidentes. `scope` contiene una
lista de una o ambas carpetas y la evidencia debe respetar esa selección.

## Ejemplos de uso

```text
@documentation-orchestrator inspect: explica las capas y localiza autenticación.
Cita fuentes, confianza y límites; no crees índices ni documentación.
```

```text
@documentation-orchestrator bootstrap-core: presenta el plan para inicializar el core.
```

```text
@documentation-orchestrator sync-core: actualiza solo el core existente.
```

```text
@documentation-orchestrator ¿Está actualizada la documentación del proyecto?
```

```text
@documentation-orchestrator Actualiza solo arquitectura y seguridad. Presenta
primero el estado, el plan y las escrituras previstas.
```

## Qué puede modificar

Los seis agentes pueden leer directamente contexto relevante: arquitectura entra
por `.architecture/README.md`; Navigator resuelve instancia/config y empieza por
`ai-context.md` o `module-map.json`. Verifican baseline y cambios antes de afirmar
vigencia. Ausencia, desfase, ambigüedad o ilegibilidad llevan a fuentes directas;
código, steering y contratos son autoridad. La lectura no autoriza mantenimiento.
Una consulta local devuelve fuentes y limitaciones, sin estado `delivered` ni
afirmación de sincronización. Los IDs de agentes retirados no heredan permisos.

Puede coordinar escrituras en las carpetas documentales canónicas de los
especialistas cuando el modo y los gates lo autorizan. No crea una carpeta
`.documentation/` propia ni duplica la documentación de los especialistas.

## Límites y confirmaciones

- Nunca modifica código de producto, tests, CI, configuración funcional ni Git remoto.
- No crea ni sincroniza `.sdd/`, `.release/` o `graphify-out/`.
- No recomienda ni selecciona niveles, modelos o proveedores LLM.
- La autorización documental de Quality/Security se reutiliza para el mismo
  alcance en la sesión, sin pedir otro filtro de severidad; no autoriza remediar.
  Un `gate_state` recibido no concede autorización ni permisos técnicos.
- `release-check` es solo lectura y no crea tags, CHANGELOG ni versiones.
