# Documentation Orchestrator

## Resumen

| Campo | Información |
|---|---|
| ID | `documentation-orchestrator` |
| Skill propia | [`documentation-orchestrator`](../../canonical/skills/documentation-orchestrator/SKILL.md) |
| Propósito | Resolver consultas de arquitectura/navegación, coordinar documentación y mantener su guía portable aprobada en `AGENTS.md` |
| Rol | Clasifica, ordena y conserva los gates de especialistas |
| No gestiona | `.sdd/`, `.release/` ni `graphify-out/` |

Es la entrada responsable del core, incluso para consultas puntuales. Ejecuta
localmente las skills separadas `architecture` y `project-navigator`, cargadas
bajo demanda; conservan autoridad sobre `.architecture/` y `.navigator/`.
También ejecuta localmente las skills `data-api` y `ui-design` para mantener sus
carpetas documentales; Quality/Security puede ejecutarlas localmente o continuar con
el agente vigente `code-review`, sin duplicar acciones.

## Cuándo usarlo

- Para saber si la documentación está actualizada.
- Para entender la arquitectura, localizar código o investigar dependencias.
- Para preparar la documentación base del proyecto.
- Para revisar o actualizar la documentación existente, completa o de un tema concreto.
- Para comprobar si la documentación está lista para publicar.

Si la petición es una feature o un bugfix de producto, recomienda Developer. SDD se
usa únicamente cuando el usuario selecciona explícitamente esa metodología. Si es un
commit, una versión o un tag, recomienda Git & Release Manager.

## Referencia de modos (opcional)

No necesitas elegir ni escribir estos nombres: describe lo que quieres y el agente
selecciona el modo adecuado.

| Modo | Qué hace |
|---|---|
| `status` | Solo lectura: inventario, aplicabilidad y frescura. |
| `inspect` | Consulta e investigación core de solo lectura, sin bootstrap, sync, exportación ni handoff core. |
| `bootstrap-core` | Propone crear únicamente `.navigator/` y `.architecture/`; puede incluir la guía gestionada de `AGENTS.md` en el plan. |
| `sync-core` | Actualiza el core existente, recomienda el ausente e incluye `AGENTS.md` en el plan de escritura. |
| `sync-existing` | Actualiza solo las carpetas documentales que ya existen e incluye `AGENTS.md` en el plan de escritura. |
| `sync-domain` | Actualiza los dominios solicitados explícitamente e incluye `AGENTS.md` en el plan de escritura. |
| `release-check` | Comprueba documentación y riesgos existentes sin versionar ni publicar. |

## Flujo de ejecución

1. Hace un preflight barato y de solo lectura, sin recomendar ni seleccionar modelos.
2. En `inspect`, `status` y `release-check`, inspecciona e informa sin escrituras. Para modos
   con escritura presenta el plan global de proyectos, dominios, orden y la acción
   sobre el `AGENTS.md` raíz, y espera su aprobación antes de escribir.
3. Ejecuta especialistas en secuencia y conserva los gates propios de cada uno;
   una autorización efectiva del mismo alcance en la sesión puede reutilizarse.
4. Verifica artefactos y evidencia antes de declarar un dominio completado.

El orden normal es skill Architecture local, Data API/UI local si aplica, Code Review
para calidad/seguridad seleccionadas y skill Project Navigator local al final. El
core está formado por las dos skills; Data y Design son condicionales; Quality y
Security son assurance recomendado.

Cuando el usuario solicita continuar con `code-review` —o hacen falta su
rol o permisos— en calidad/seguridad, emite un bloque **handoff** con identificador, origen/destino,
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
@documentation-orchestrator Explícame las capas del proyecto y dónde se gestiona autenticación.
```

```text
@documentation-orchestrator Prepara la documentación base de este proyecto.
```

```text
@documentation-orchestrator Revisa y actualiza la documentación existente que afecta a autenticación.
```

```text
@documentation-orchestrator ¿Está actualizada la documentación del proyecto?
```

```text
@documentation-orchestrator Comprueba si la documentación está lista para publicar.
```

## Qué puede modificar

Los agentes pueden leer directamente contexto relevante: arquitectura entra
por `.architecture/README.md`; Navigator resuelve instancia/config y empieza por
`ai-context.md` o `module-map.json`. Verifican baseline y cambios antes de afirmar
vigencia. Ausencia, desfase, ambigüedad o ilegibilidad llevan a fuentes directas;
código, steering y contratos son autoridad. La lectura no autoriza mantenimiento.
Una consulta local devuelve fuentes y limitaciones, sin estado `delivered` ni
afirmación de sincronización. Los IDs de agentes retirados no heredan permisos.

Puede coordinar escrituras en carpetas documentales canónicas cuando el modo y los
gates lo autorizan. No crea una carpeta
`.documentation/` propia ni duplica la documentación de los especialistas. En el
`AGENTS.md` raíz solo mantiene el bloque entre los marcadores
`ai-agents-kit:documentation:start/end`; conserva todo el texto exterior y se
detiene si los marcadores o instrucciones existentes son ambiguos o incompatibles.

## Límites y confirmaciones

- Nunca modifica código de producto, tests, CI, configuración funcional ni Git remoto.
- No crea ni sincroniza `.sdd/`, `.release/` o `graphify-out/`.
- No modifica `CLAUDE.md`, `GEMINI.md` ni otros archivos de instrucciones de host.
- No recomienda ni selecciona niveles, modelos o proveedores LLM.
- La autorización documental de Quality/Security se reutiliza para el mismo
  alcance en la sesión, sin pedir otro filtro de severidad; no autoriza remediar.
  Un `gate_state` recibido no concede autorización ni permisos técnicos.
- `release-check` es solo lectura y no crea tags, CHANGELOG ni versiones.
