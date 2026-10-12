# Developer Agent

| Campo | Información |
|---|---|
| ID | `developer` |
| Skill propia | [`developer`](../../canonical/skills/developer/SKILL.md) |
| Skills de dominio | `data-api` y `ui-design`, bajo demanda |
| Propósito | Planear e implementar características de producto completas en UI, datos/APIs y lógica de negocio |
| Documentación canónica | `.data/`, `.design/`, `.architecture/` y `.navigator/` se consultan según el impacto; actualizar requiere decisión del usuario |

## Modos

- **PLAN:** se solicita con `PLAN`, `PLAN:` o una petición de solo planificación.
  Developer inspecciona en modo de solo lectura, resuelve preguntas esenciales,
  presenta alcance, impactos, implicaciones, secuencia y verificación, y espera
  aprobación antes de implementar. Si se pidió solo el plan, se detiene ahí.
- **IMPLEMENTACIÓN:** una petición clara y acotada puede ejecutarse directamente.
  La ambigüedad o el impacto amplio/multicapa requieren aclaración y aprobación del
  plan antes de editar.

PLAN es un protocolo conversacional, no sustituye los permisos ni el modo de solo
lectura que controle el host.

## Relación con skills y agentes

- `data-api` aporta estándares para contratos, modelos, serialización, persistencia
  e integraciones. `ui-design` aporta estándares para componentes, tokens, temas,
  accesibilidad y UX. Developer las carga solo cuando necesita ese conocimiento;
  sus fronteras documentales no impiden una implementación multicapa.
- Las antiguas entradas de agente `data-api` y `ui-design` se retiraron. Sus skills
  permanecen disponibles para Developer y para el trabajo documental local de
  Documentation Orchestrator.
- Developer no carga `sdd-spec`, no recomienda ni invoca `sdd` automáticamente y no
  crea `.sdd/`. La metodología SDD se activa solo al seleccionar explícitamente SDD.
- `documentation-orchestrator` mantiene documentación; `code-review` audita calidad
  y seguridad; `git-release-manager` opera commits y releases con su autorización.
  No se invocan agentes automáticamente.

## Documentación al finalizar

Developer revisa el diff y pregunta si corresponde actualizar documentación solo
cuando una fuente canónica existente quedó desfasada. Indica la ruta y el motivo con:

> ⚠️ ¿Quieres actualizar la documentación con lo realizado?

Si acepta, prepara contexto portable para continuar manualmente con Documentation
Orchestrator. No repite el aviso si la documentación afectada ya quedó actualizada y
verificada dentro de la tarea.

## Ejemplos

```text
@developer PLAN: agrega recuperación de contraseña. Analiza pantallas, API,
validaciones, estados de error, pruebas e implicaciones antes de implementar.
```

```text
@developer Implementa el nuevo estado vacío de la lista usando los componentes y
tokens existentes; añade una prueba focalizada y verifica el módulo.
```
