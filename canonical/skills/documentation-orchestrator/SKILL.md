---
name: documentation-orchestrator
description: >-
  Coordina status, bootstrap, sincronización y comprobaciones de documentación canónica.
  Úsala para docs status, sync-check, bootstrap-core, sync-core, sync-existing,
  sync-domain, release-check o coordinación documental entre dominios. Para consultas
  puntuales usa project-navigator o architecture según el resultado solicitado.
---

# Skill: Documentation Orchestrator

{{mas_identity}}


Referencia canonica para **coordinar** las skills documentales sin sustituirlas.
Administra el orden, alcance, estado y gates; cada skill especialista sigue siendo
la autoridad sobre su propia carpeta.

> **Alcance inviolable:** solo coordina documentacion e indices canonicos. Como
> parte de una operación documental de escritura aprobada, puede crear/actualizar
> únicamente el bloque documental gestionado y delimitado en el `AGENTS.md` raíz
> del proyecto resuelto.
> No modifica codigo de producto, tests, CI ni Git remoto. No crea `.documentation/`.

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

El core se ejecuta localmente: carga `architecture` o `project-navigator` bajo
demanda, sin handoff para consultas ni mantenimiento core. Conserva ambas skills
y destinos separados. `.data/` y `.design/` también se actualizan localmente con
`data-api` y `ui-design`: sus antiguos agentes fueron retirados y sus skills siguen
siendo la autoridad de cada carpeta. Para quality/security, elige una sola vía:
carga la skill localmente o prepara un handoff al agente real `code-review`. Si una
regla de dominio entra en conflicto con esta coordinación, manda la skill especialista
dentro de su carpeta; esta skill manda sobre orden, selección y cierre global.

Los dominios quality y security conservan sus skills y carpetas, pero su agente
receptor es `code-review`. Para la misma accion, mismo proyecto y via aprobada,
puedes agruparlos en un handoff cuyo `scope` seleccione ambas carpetas. Si solo
un dominio esta aprobado/existe en `sync-existing`, selecciona solo ese dominio.
No amplias permisos ni cambias una accion para poder agruparla.

## Modos

| Modo | Contrato |
| --- | --- |
| `status` | Solo lectura; inventario, aplicabilidad y frescura. Alias natural: `sync-check`. |
| `inspect` | Consulta de arquitectura o navegación, solo lectura y cero persistencia; skills core locales bajo demanda. |
| `bootstrap-core` | Propone inicializar solo `.navigator/` y `.architecture/`; nunca sobrescribe. El plan puede incluir la guía gestionada en `AGENTS.md`. |
| `sync-core` | Actualiza core existente; recomienda el core ausente sin crearlo. Incluye `AGENTS.md` solo en un plan aprobado de escritura. |
| `sync-existing` | Actualiza solo carpetas primarias existentes; no crea ausentes. Incluye `AGENTS.md` solo en un plan aprobado de escritura. |
| `sync-domain` | Actualiza los dominios explicitamente solicitados; incluye `AGENTS.md` solo en un plan aprobado de escritura. |
| `release-check` | Solo lectura; gate documental y de riesgos criticos previo a release. |

Defaults: sin modo → `status` si no hay intención específica; preguntas sobre
capas, módulos, símbolos o impacto → `inspect`; "actualiza lo que tenemos" → `sync-existing`;
feature o bugfix de producto → recomienda `developer`; solicita `sdd` solo si el usuario
elige explícitamente esa metodología. Si pide "sincronizar todo" sin aclarar
si incluye carpetas ausentes, pregunta antes de elegir modo.

## Preflight técnico

Antes de **cualquier** operacion, incluso `status`:

1. Haz un preflight barato y de solo lectura: detecta proyecto(s), carpetas,
   marcas disponibles, presencia de `AGENTS.md`, `git status` y nombres de
   archivos cambiados.
2. Clasifica la tarea y el alcance con `references/workflows.md`.
3. Usa los datos del preflight para delimitar el plan y comprobar los gates aplicables.
   El preflight no acredita autorizacion de escritura.

El preflight no carga todas las skills, no lee el codigo completo y no escribe.
Si el repo cambia durante una espera por decision real, repite el preflight minimo.

## Flujo de ejecución

1. Resuelve uno o varios proyectos independientes; pregunta si hay empate.
2. Ejecuta un estado inicial y presenta el plan de carpetas y acciones cuando aplique.
   Para operaciones de escritura, incluye la ruta de `AGENTS.md` raíz y si se
   creará o actualizará su bloque gestionado. `inspect`, `status` y `release-check`
   continuan con lectura e informe en el mismo turno y no escriben.
   En `inspect`, investiga la pregunta con contexto mínimo o fuentes directas,
   sin plan de escritura ni inventario global obligatorio.
3. Antes de escribir, espera aprobacion global del plan; reutiliza autorizacion
   efectiva de la misma operacion y alcance en la sesion, sin confundir un aviso
   o metadatos de handoff con autorizacion.
4. Ejecuta siempre core aquí con su skill bajo demanda. Ejecuta `.data/` y `.design/`
   aquí con sus skills. Para quality/security elige una sola vía: ejecuta aquí su
   skill o emite handoff a `code-review` si el usuario lo pide o hacen falta su rol
   o permisos; nunca ambas para la misma acción (`references/handoff.md`).
5. Tras un handoff, marca el dominio pendiente del especialista y espera su
   resultado o evidencia antes de reanudar; no ejecuta esa misma accion.
6. Ejecuta secuencialmente solo los dominios aprobados que no fueron derivados.
7. Conserva las decisiones pendientes de cada especialista. En `quality` y
   `security`, el plan autorizado cubre todos los findings verificados del alcance:
   no pide un filtro por severidad ni repite esa aprobacion en la misma sesion;
   no entres en remediacion de codigo. `gate_state` no concede autorizacion.
8. Verifica artefactos y evidencia antes de marcar un dominio completado.
9. Cierra con estado inicial/final, acciones, bloqueos y recomendaciones.

Orden normal: `architecture` → `data-api` si aplica → `ui-design` si aplica →
revisión `code-review` de los dominios quality/security seleccionados (skills
locales o handoff) → `project-navigator` al final. En `bootstrap-core`, crea primero el
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
- Si un dominio falla, marca `Bloqueado` y no lo declares completado. Continúa con
  dominios independientes ya autorizados; pregunta solo si cambian alcance,
  dependencias o autorización. El informe final conserva los resultados parciales.
- En una consulta `inspect`, ausencia, desfase o contexto ilegible no es fallo de
  ejecución documental: degrada a fuentes directas sin bloquear ni autoactualizar.
- No instales herramientas ni ejecutes Graphify.
- `release-check` no versiona, no genera changelog y no crea tags; eso pertenece
  a `release-management`.

## Referencia bajo demanda

Lee [`references/project-context.md`](references/project-context.md) para consumo
selectivo de arquitectura y Navigator. No exige cargar otros workflows ni todas
las skills. Navigator conserva autoridad de formatos y disponibilidad.

Lee [`references/workflows.md`](references/workflows.md) al clasificar una
operacion o ejecutar un modo. Contiene estados, gates, criterios de release y
formato de informe, además del contrato de la guía gestionada en `AGENTS.md`.

Lee [`references/handoff.md`](references/handoff.md) solo si el trabajo debe
continuar con el agente especialista real; define el formato, los campos, las
exclusiones y la regla que impide duplicar la misma accion.
