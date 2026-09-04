# Documentation Orchestrator

## Resumen

| Campo | Información |
|---|---|
| ID | `documentation-orchestrator` |
| Skill propia | [`documentation-orchestrator`](../../canonical/skills/documentation-orchestrator/SKILL.md) |
| Propósito | Coordinar el estado, bootstrap y sincronización de documentación canónica |
| Rol | Clasifica, ordena y conserva los gates de especialistas |
| No gestiona | `.sdd/`, `.release/` ni `graphify-out/` |

Es la puerta de entrada cuando una petición cruza varias áreas documentales. No
reemplaza a Architecture, Data & API, UI Design, Quality, Security o Project
Navigator: decide cuál aplica y carga la skill especialista correspondiente.

## Cuándo usarlo

- Para saber si la documentación está actualizada (`status` / `sync-check`).
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
| `bootstrap-core` | Propone crear únicamente `.navigator/` y `.architecture/`. |
| `sync-core` | Actualiza el core existente y recomienda el ausente. |
| `sync-existing` | Actualiza solo las carpetas documentales que ya existen. |
| `sync-domain` | Actualiza los dominios solicitados explícitamente. |
| `release-check` | Comprueba documentación y riesgos existentes sin versionar ni publicar. |

## Cómo trabaja

1. Hace un preflight barato y de solo lectura.
2. Recomienda manualmente un modelo `bajo`, `medio` o `alto` y espera confirmación.
3. Presenta un plan global de proyectos, dominios, orden y posibles escrituras.
4. Ejecuta especialistas en secuencia y conserva los gates propios de cada uno.
5. Verifica artefactos y evidencia antes de declarar un dominio completado.

El orden normal es Architecture, Data & API si aplica, UI Design si aplica, Quality,
Security y Project Navigator al final. El core está formado por Navigator y
Architecture; Data y Design son condicionales; Quality y Security son assurance
recomendado.

Cuando el usuario solicita continuar con el especialista real —o hacen falta su
rol o permisos—, emite un bloque **handoff** con identificador, origen/destino,
acción/motivo, proyecto, contexto, alcance de lectura/escritura y confirmación.
En ese caso no ejecuta la misma acción: espera un `Handoff Result` correlacionado.
El formato y las reglas viven en
[`references/handoff.md`](../../canonical/skills/documentation-orchestrator/references/handoff.md).

`write_scope` documenta la frontera esperada, pero no reemplaza los permisos del
host ni los gates del especialista.

## Ejemplos de uso

```text
@documentation-orchestrator ¿Está actualizada la documentación del proyecto?
```

```text
@documentation-orchestrator Actualiza solo arquitectura y seguridad. Presenta
primero el estado, el plan y las escrituras previstas.
```

## Qué puede modificar

Puede coordinar escrituras en las carpetas documentales canónicas de los
especialistas cuando el modo y los gates lo autorizan. No crea una carpeta
`.documentation/` propia ni duplica la documentación de los especialistas.

## Límites y confirmaciones

- Nunca modifica código de producto, tests, CI, configuración funcional ni Git remoto.
- No crea ni sincroniza `.sdd/`, `.release/` o `graphify-out/`.
- No selecciona ni cambia el modelo del host.
- Quality y Security conservan sus gates de alcance y no se convierten en una
  remediación masiva de código.
- `release-check` es solo lectura y no crea tags, CHANGELOG ni versiones.
