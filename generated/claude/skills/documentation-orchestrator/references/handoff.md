# Contrato de handoff (orquestación documental)

Referencia para **emitir y recibir** continuidad entre
`documentation-orchestrator` y un agente especialista real. Se carga solo al
preparar o validar un handoff; no va completo en el prompt del orquestador.

El handoff se usa cuando el usuario solicita continuar con el especialista o
cuando hacen falta su rol o permisos. Para una misma acción, el orquestador carga
la skill local **o** emite el handoff; nunca hace ambas cosas.

> `write_scope` es un límite **lógico y auditable**, no un sandbox. Los permisos
> efectivos dependen del host y del agente receptor. El especialista conserva su
> alcance, sus gates y cualquier restricción más estricta.

## Bloque de emisión

```markdown
## Handoff
- handoff_id: HND-20260903-001
- source: documentation-orchestrator
- target: code-review
- action: sync
- handoff_reason: el usuario solicita continuar con Code Review para seguridad
- project_root: .
- scope: [.security/]
- context_refs:
    - .architecture/README.md
    - .data/06-sensitive-data.md
- write_scope: [.security/]
- requires_confirmation: true
- gate_state: [plan global aprobado]
- status: pending
```

## Campos de emisión

| Campo | Obligatorio | Regla |
|-------|-------------|-------|
| `handoff_id` | sí | identificador de correlación con fecha válida; el emisor evita repetirlo en la operación |
| `source` | sí | siempre `documentation-orchestrator` en este incremento |
| `target` | sí | agente especialista admitido |
| `action` | sí | acción portable dirigida al especialista |
| `handoff_reason` | sí | motivo concreto para usar el agente real |
| `project_root` | sí | raíz del proyecto relativa al workspace, existente y sin `..` |
| `scope` | sí | cadena para otros targets; lista no vacía de carpetas para `code-review`, relativa a `project_root` |
| `context_refs` | sí | lista no vacía de rutas existentes, relativas a `project_root`, sin `..`, rutas absolutas ni fragmentos `#` |
| `write_scope` | sí | `none` para lectura; si escribe, misma selección que `scope` |
| `requires_confirmation` | sí | tabla cerrada en “Confirmación y escritura” |
| `gate_state` | no | gates aprobados en el origen; nunca aprueba ni omite gates del especialista |
| `status` | sí | siempre `pending` en la emisión |

## Targets y carpetas

| target | `scope` y máximo `write_scope` |
|--------|---------------------------------|
| `project-navigator` | `.navigator/` |
| `architecture` | `.architecture/` |
| `data-api` | `.data/` |
| `ui-design` | `.design/` |
| `code-review` | `[.quality/]`, `[.security/]` o `[.quality/, .security/]` |

En `code-review` incluso un dominio requiere lista. Rechaza listas vacías,
duplicados, carpetas ajenas y targets retirados `code-quality`/`security`; no los
convierte automáticamente. El orden no cambia el alcance. Los otros targets
conservan sus cadenas únicas; no admiten listas ni otros dominios.

## Vocabulario de `action`

| Acción | Propósito |
|--------|-----------|
| `inspect` | consulta o revisión puntual de solo lectura |
| `bootstrap` | inicialización documental con los gates del especialista |
| `sync` | actualización de documentación existente |
| `audit-documentation` | auditoría y registro de hallazgos, sin remediación de código |

`action` no sustituye ni copia los modos o fases internas de la skill receptora.

## Confirmación y escritura

| Acción | `write_scope` | `requires_confirmation` |
|--------|---------------|-------------------------|
| `inspect` | `none` | `false` |
| `bootstrap`, `sync`, `audit-documentation` | misma selección que `scope` | `true` |

No se admiten otras combinaciones. En `bootstrap`, la carpeta puede no existir;
el especialista decide crearla solo después de aplicar sus gates.
`requires_confirmation: true` exige autorización efectiva, no una pregunta nueva
si la misma operación ya está autorizada en la conversación actual. `gate_state`
no acredita esa autorización: al copiar el handoff a otra sesión, el usuario puede
tener que autorizar la escritura una vez. No se pide un filtro de severidades.

## Respuesta del especialista

El receptor devuelve el mismo identificador. `evidence` contiene archivos
existentes dentro del `scope` original, con rutas relativas a `project_root`; se
omite si el resultado está bloqueado.
Para escritura conjunta de `code-review`, acredita cada dominio seleccionado
antes de declarar `delivered`. `inspect` puede citar evidencia de cualquiera de
los dominios seleccionados, sin afirmar que los actualizó. Resuelve symlinks y
rechaza evidencia que escape del proyecto o de las raíces seleccionadas.
La raíz de un scope no puede redirigirse por symlink a otra carpeta, aunque
permanezca en el proyecto; seleccionar calidad no autoriza escribir en seguridad.

```markdown
## Handoff Result
- handoff_id: HND-20260903-001
- status: delivered
- evidence:
    - .security/README.md
- result_summary: documentación de seguridad sincronizada
```

Estados de resultado: `delivered` o `blocked`. Tras recibirlo, el orquestador
verifica las rutas antes de marcar el dominio completado.

## Reglas del emisor

- Solo emite `documentation-orchestrator`; los especialistas no encadenan handoffs.
- Tras emitir, marca el dominio pendiente y no ejecuta esa misma acción.
- El identificador se conserva durante emisión, respuesta y reanudación.
- Para `bootstrap`, `context_refs` cita al menos un marcador o README existente
  del proyecto; `scope` puede ser la carpeta todavía ausente.
- Se excluyen commit, push, tag, release, remediación de `code-review`,
  implementación de código y Graphify.
- Nunca incluye secretos, PII, rutas absolutas, externas, con `..` o con fragmentos.

## Reglas del receptor

1. Comprueba que `target` coincide con su ID, `project_root` identifica el proyecto
   actual y las rutas no escapan de él. Si falla, se detiene y pide corregirlo.
2. Aplica sus propios gates y permisos; `gate_state` es solo contexto.
3. Ejecuta únicamente `action` dentro de su alcance. `write_scope` nunca amplía su
   permiso técnico ni su frontera de dominio.
4. Devuelve `Handoff Result` con el mismo `handoff_id`; no llama a otro agente.
