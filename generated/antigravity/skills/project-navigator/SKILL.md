---
name: project-navigator
description: >-
  Localiza archivos, módulos y símbolos mediante contexto y mapas de `.navigator/`.
  Úsala para búsquedas puntuales y dependencias; bootstrap/update solo bajo petición.
  No modifica código de negocio.
---

# Skill: Project Navigator

## Identidad del MAS

MAS significa **Multi-Agent System**; `MAS:` se dirige al kit y `@<agente>` a un rol concreto.


Referencia canónica de **cómo navegar e indexar** un repositorio con mínimo de
tokens. `documentation-orchestrator` es la entrada core y la ejecuta localmente.
Si agente y skill divergen,
**manda esta skill**.

Objetivo: responder con la capa más barata suficiente y citar fuentes.

> **Alcance inviolable:** por defecto **solo lectura** del repo y de
> `.navigator/`. Escritura **solo** en `.navigator/` (bootstrap/update). No crea
> ni exporta `AGENTS.md` y no lo sobrescribe; esa guía pertenece a
> `documentation-orchestrator`. NO modifica código de negocio, UI,
> tests de producto, CI ni Git remoto.
> Si piden implementar features o refactors: **declarar límite**, aportar
> ubicación/mapa si ayuda, y detenerse.

## Cuándo usar

- Onboarding: qué es el proyecto, cómo está organizado
- Localizar módulos, símbolos, dependencias e impacto
- Antes de una feature/refactor cuando haga falta mapa sin reexplorar el repo
- Primera vez sin `.navigator/` → lectura degradada; proponer bootstrap si conviene
- Actualizar índices solo cuando el usuario lo pida o autorice el mantenimiento

## Flujo obligatorio al recibir una petición

1. **Clasificar** (consulta vs bootstrap/update vs fuera de alcance).
2. Ejecutar el **gate de disponibilidad** en cada petición: leer el `config.yaml`
   aplicable y comprobar en filesystem los artefactos de las capas candidatas
   (`references/config.md`). No inferir su estado desde mensajes anteriores.
   Resolver índices junto al `config.yaml` seleccionado, nunca desde el path del
   archivo consultado ni desde `project.root`.
3. Si falta contexto o está desfasado, ambiguo, inválido o ilegible → modo
   degradado (`references/config.md`) sin bloquear la consulta. Puedes recomendar
   mantenimiento a `documentation-orchestrator`, sin bootstrap/update automático
   ni exigir aceptación antes de responder con fuentes directas.
4. Elegir la **capa mínima** (tabla abajo); subir de capa solo si no basta.
5. Responder de forma concisa citando **fuente** (path de capa o `archivo:linea`).
6. Si hubo degradado: distinguir `capas_ausentes` de
   `capas_deshabilitadas` y declarar el límite de confianza.

### Clasificador pregunta → capa

| Tipo de pregunta | Capa inicial | Subir a si no basta |
| --- | --- | --- |
| Qué es / propósito / organización | 0 `ai-context.md` | 1 |
| En qué módulo / dependencias entre módulos | 1 `module-map.json` | 2 o 4 |
| Dónde se define un símbolo / firma | 2 `symbols.json` (si existe) | 4 |
| Relación X–Y / impacto de cambiar Z | 3 grafo (si existe y on) | 1 + 4 |
| Detalle de implementación | 4 código puntual (rango) | — |
| Bootstrap / indexar / actualizar | Escritura en `.navigator/` | — |

Detalle de capas y presupuestos: `references/layers.md`. Contratos normativos de
`module-map.json` y `symbols.json`: `references/schemas.md`.

### Reglas de consulta

Lee instrucciones/steering primero y aplica bajo demanda el
[contrato compartido](../documentation-orchestrator/references/project-context.md).
Esta skill conserva autoridad de formatos y disponibilidad. La consulta no
ejecuta bootstrap ni update. Navigator no exporta `AGENTS.md` ni modifica
instrucciones del proyecto;
si se solicita mantener `AGENTS.md`, remite esa operación al plan de
`documentation-orchestrator`. Baselines no verificables o desfasados solo aportan
pistas; valida decisiones en código y contratos.

- Preferir archivo + rango de líneas sobre leer directorios enteros
- No volcar grafo ni `symbols.json` / `module-map.json` completos al contexto
- No inventar entradas de índices; si faltan, degradar o proponer update
- Antes de afirmar que una capa está disponible o ausente, verificar su path
- Reportar solo capas relevantes para la consulta; no listar todas por rutina
- Empieza con una capa y pocos archivos; amplía si la evidencia no basta y explica por qué.
- Nunca “leer el repo entero” para compensar

## Bootstrap y update

Contrato de pasos, monorepo y propiedad de `AGENTS.md`:
`references/bootstrap.md`.

Resumen bootstrap:

1. Detectar stack y fuentes externas
2. Ubicación `.navigator/` (preguntar si ambiguo)
3. `config.yaml` + contexto breve + `module-map.json`
4. No bloquear si faltan symbols/grafo
5. Respetar exclude/secretos y ejecutar el gate post-bootstrap de integridad y presupuesto
6. Informar artefactos, gaps y presupuesto

Schemas: `references/schemas.md`. Plantillas: `references/templates/`.

Update: solo on_request; capas afectadas; no regenerar todo por defecto;
preguntar si `ai-context.md` tiene edición manual evidente.

## Artefactos en `.navigator/`

| Artefacto | Tras bootstrap | Notas |
| --- | --- | --- |
| `config.yaml` | Obligatorio | Contrato en `references/config.md` |
| `ai-context.md` | Obligatorio | Capa 0; breve, con referencias a detalle |
| `module-map.json` | Obligatorio | Capa 1 |
| `symbols.json` | Opt-in | Capa 2 best-effort |
| `graph/` | Opt-in | Capa 3; provider default `none` |
| `cache/` | No versionar | gitignore |

## Fuentes externas (híbrido Capa 0)

Detectar best-effort: `AGENTS.md`, `CLAUDE.md`, README, "Contexto para IA" en
`.architecture/`, `.data/`, `.quality/`, `.security/`, `.design/`, etc.
Referenciar; no sobrescribir. Detalle: `references/sources.md`.

## Formato de respuesta

- Conciso, orientado a la pregunta
- Indicar **fuentes** (p. ej. `.navigator/ai-context.md`, `src/foo.ts:42`)
- En degradado: `fuentes`, `capas_ausentes`, `capas_deshabilitadas` y confianza.
  `ausente` significa habilitada pero sin artefacto; `deshabilitada`, config en false
- No rellenar con especulación presentada como hecho indexado

## Criterios de concisión

| Artefacto / acción | Objetivo | Si se pasa |
| --- | --- | --- |
- `ai-context.md`: propósito y mapa general; referencia detalles, no los copies.
- `module-map.json`: responsabilidades breves; no enumeres todos los archivos.
- Respuestas: limita hits al conjunto pertinente y amplía si falta evidencia.
- Código: empieza con el rango mínimo y extiéndelo cuando la respuesta lo requiera.
- Bootstrap: acota `project.root` al producto o subproyecto solicitado.

## Relación con otras skills

No sustituye a architecture, security, quality, data-api ni ui-design: solo
navega e indexa. Puede señalar el especialista adecuado para documentar o remediar.

## Fuera de alcance

Si piden implementar features, refactors de producto o cambios de CI/Git remoto:
declarar límite, aportar mapa/ubicación si ayuda, y detenerse (no implementar).
