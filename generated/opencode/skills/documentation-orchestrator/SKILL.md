---
name: documentation-orchestrator
description: >-
  Coordina y comprueba la documentacion canonica de un proyecto. Use when the
  user asks for docs status, sync-check, bootstrap-core, sync-core,
  sync-existing, sync-domain, release-check, pre-release check, comprobar si la
  documentacion esta actualizada, actualizar las carpetas existentes o verificar
  si el proyecto esta listo para una release. Recomienda un modelo bajo, medio o
  alto y espera confirmacion antes de operar.
---

# Skill: Documentation Orchestrator

Referencia canonica para **coordinar** las skills documentales sin sustituirlas.
Administra el orden, alcance, estado y gates; cada skill especialista sigue siendo
la autoridad sobre su propia carpeta.

> **Alcance inviolable:** solo coordina documentacion e indices canonicos. No
> modifica codigo de producto, tests, CI ni Git remoto. No crea `.documentation/`.
> No selecciona ni cambia el modelo del host.

## Autoridad y especialistas

| Carpeta | Skill autoritativa | Clase |
| --- | --- | --- |
| `.navigator/` | `project-navigator` | Core |
| `.architecture/` | `architecture` | Core |
| `.data/` | `data-api` | Condicional: APIs, datos o persistencia |
| `.design/` | `ui-design` | Condicional: UI o sistema visual |
| `.quality/` | `code-quality` | Assurance recomendado |
| `.security/` | `security` | Assurance recomendado |

`.sdd/`, `.release/` y `graphify-out/` pertenecen a otros workflows. Se pueden
leer como contexto, pero esta skill nunca los crea, sincroniza ni modifica.

Cuando se activa un dominio, carga solo su skill. Si una regla de dominio entra
en conflicto con esta coordinacion, manda la skill especialista dentro de su
carpeta; esta skill manda sobre orden, seleccion y cierre global.

## Modos

| Modo | Contrato |
| --- | --- |
| `status` | Solo lectura; inventario, aplicabilidad y frescura. Alias natural: `sync-check`. |
| `bootstrap-core` | Propone inicializar solo `.navigator/` y `.architecture/`; nunca sobrescribe. |
| `sync-core` | Actualiza core existente; recomienda el core ausente sin crearlo. |
| `sync-existing` | Actualiza solo carpetas primarias existentes; no crea ausentes. |
| `sync-domain` | Actualiza los dominios explicitamente solicitados. |
| `release-check` | Solo lectura; gate documental y de riesgos criticos previo a release. |

Defaults: sin modo → `status`; "actualiza lo que tenemos" → `sync-existing`;
feature o bugfix → derivar a `sdd-spec`. Si pide "sincronizar todo" sin aclarar
si incluye carpetas ausentes, pregunta antes de elegir modo.

## Gate 0: modelo obligatorio

Antes de **cualquier** operacion, incluso `status`:

1. Haz un preflight barato y de solo lectura: detecta proyecto(s), carpetas,
   marcas disponibles, `git status` y nombres de archivos cambiados.
2. Clasifica tarea, alcance y complejidad con `references/workflows.md`.
3. Recomienda `bajo`, `medio` o `alto`, explica los motivos en pocas lineas y
   **detente**.
4. Continua solo si el usuario responde de forma explicita: `listo`, `continua`,
   `procede`, `ya seleccione el modelo` o `continua con el actual`.

En operaciones compuestas, muestra el nivel global y las fases que justifican un
nivel distinto. La confirmacion del Gate 0 satisface un aviso de modelo
especialista solo si lo menciona expresamente; los demas gates nunca se omiten.

El preflight no carga todas las skills, no lee el codigo completo y no escribe.
No afirmes conocer el modelo activo si el host no lo expone. Si cambia el alcance,
recalcula. Si el repo cambia mientras esperas, repite el preflight minimo.

## Flujo tras Gate 0

1. Resuelve uno o varios proyectos independientes; pregunta si hay empate.
2. Ejecuta un estado inicial y presenta el plan de carpetas y acciones.
3. Antes de escribir, espera aprobacion global del plan.
4. Ejecuta secuencialmente solo los dominios aprobados.
5. Conserva los gates propios de cada especialista. En `quality` y `security`,
   confirma el alcance de findings; no entres en remediacion de codigo.
6. Verifica artefactos y evidencia antes de marcar un dominio completado.
7. Cierra con estado inicial/final, acciones, bloqueos y recomendaciones.

Orden normal: `architecture` → `data-api` si aplica → `ui-design` si aplica →
`code-quality` si existe/esta seleccionado → `security` si existe/esta
seleccionado → `project-navigator` al final. En `bootstrap-core`, crea primero el
Navigator aprobado, documenta arquitectura y refresca solo la capa afectada del
Navigator al cierre **si fue creado en esa misma operacion**. Un Navigator que ya
existia requiere `sync-core` o alcance explicito para modificarse.

## Presupuesto de contexto

- Empieza por nombres de carpetas, READMEs, metadatos y `git diff --name-only`.
- Usa el ultimo commit documentado y filtra rutas antes de leer diffs completos.
- No cargues una skill especialista hasta que su dominio vaya a ejecutarse.
- No hagas auditorias completas desde `status` o `release-check`.
- Si faltan evidencias, escala de lectura puntual a profunda; nunca al reves.
- Repetir una operacion sin cambios no debe producir escrituras.

## Seguridad y fallos

- Nunca expongas secretos, credenciales, PII ni valores sensibles.
- Git es solo lectura (`status`, `log`, `diff`, `show`, `rev-parse`).
- Ejecuta un solo comando Git por llamada; no uses pipes ni separadores de shell.
- Si un dominio falla o no tiene evidencia, marca `Bloqueado`; no lo declares
  completado. Pregunta antes de continuar con dominios independientes.
- No instales herramientas ni ejecutes Graphify.
- `release-check` no versiona, no genera changelog y no crea tags; eso pertenece
  a `release-management`.

## Referencia bajo demanda

Lee [`references/workflows.md`](references/workflows.md) al clasificar una
operacion o ejecutar un modo. Contiene la matriz de modelo, estados, gates,
criterios de release y formato de informe.
