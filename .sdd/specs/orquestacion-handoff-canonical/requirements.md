# Orquestación con handoff canónico — Requirements

Feature: `orquestacion-handoff-canonical`
Modo: `standard`
Fecha: 2026-09-03

## Resumen

Añadir al kit un mecanismo de **orquestación portable** entre agentes, basado en
un **contrato de handoff estructurado** que funciona igual en Copilot, OpenCode y
Kiro **sin depender de APIs de subagentes**. El único coordinador autorizado en
este incremento es `documentation-orchestrator`; los especialistas reciben el
handoff y ejecutan su propio dominio con sus gates intactos.

La coordinación hoy ya existe a nivel de contexto compartido (carpetas canónicas)
y de skills cargadas secuencialmente. Este incremento formaliza el **pase de
contexto verificado** entre el orquestador y el especialista, sin introducir
llamadas automáticas entre agentes.

## Decisiones de alcance (locked)

| # | Decisión | Valor |
|---|----------|-------|
| D1 | Alcance del incremento 1 | Contrato + ampliar `documentation-orchestrator`. SDD emitirá handoffs en el incremento 2. |
| D2 | Ubicación del contrato | `canonical/skills/documentation-orchestrator/references/handoff.md` (bajo demanda) |
| D3 | Forma del handoff | Bloque Markdown estructurado que el usuario copia/invoca |
| D4 | Campos de emisión | Requeridos: `handoff_id, source, target, action, handoff_reason, project_root, scope, context_refs, write_scope, requires_confirmation, status`. Opcional: `gate_state` |
| D5 | Quién emite | Solo `documentation-orchestrator` (incremento 1). Especialistas no emiten. |
| D6 | Qué se delega | Solo trabajo documental (`status`, `sync`, bootstrap documental, lectura). Manual siempre: commit/push/tag/release, remediación security/quality, implementación de código, Graphify |
| D7 | Estado de delegación | Sin carpeta nueva; se reutiliza el estado existente (READMEs, findings, gates) |
| D8 | Validación | Test de contrato que verifica campos obligatorios y `write_scope` acotado |

## Contexto y steering leídos

- `docs/arquitectura-del-kit.md` (patrón canonical→adapters→generated; el
  orquestador "no depende de APIs de subagentes", §208–225).
- `docs/vision.md` (principios: contexto selectivo, alcance inviolable,
  confirmación explícita).
- `docs/mejoras.md` (backlog: P0.5 permisos/prompt injection abiertos; P2 integración
  Navigator↔Architecture; regla "medir coste de texto nuevo").
- `canonical/skills/documentation-orchestrator/SKILL.md` y
  `canonical/agents/documentation-orchestrator.md` (modos, Gate 0, gates G1–G4).
- `canonical/manifest.json` (inventario: 10 skills, 9 agentes, 3 plataformas).
- Sin `AGENTS.md` ni `.sdd/steering/` en este repositorio.

## Historias de usuario

- **H1.** Como coordinador documental, cuando el trabajo deba continuar con el
  agente especialista real quiero emitir un handoff estructurado para entregar
  contexto verificado, sin repetir una acción que el orquestador ya ejecutó.
- **H2.** Como usuario, al recibir un handoff quiero saber exactamente a qué agente
  va, sobre qué carpeta, con qué permisos de escritura y si requiere confirmación.
- **H3.** Como mantenedor del kit, quiero que el contrato viva bajo demanda
  (`references/`), para no pagar su coste en cada turno del orquestador.
- **H4.** Como mantenedor, quiero que ningún handoff delegue acciones que exigen
  confirmación humana (commit/push/tag/release, remediación, implementación de
  código, Graphify).
- **H5.** Como mantenedor, quiero que el coste de contexto sea medible y aprobado
  antes de cerrar el incremento.
- **H6.** Como mantenedor, quiero una prueba que valide que todo handoff emitido
  tiene los campos obligatorios y un `write_scope` acotado a la carpeta del dominio.

## Criterios EARS

### H1 — Emisión del handoff

- CUANDO el usuario solicite continuar con el agente especialista real o el
  trabajo requiera su rol o permisos EL SISTEMA DEBERÁ emitir un bloque de
  handoff con los campos obligatorios de D4.
- SI el orquestador ya ejecutó una acción mediante la skill del dominio ENTONCES
  EL SISTEMA NO DEBERÁ emitir un handoff para repetir esa misma acción.
- CUANDO se emita un handoff EL SISTEMA DEBERÁ marcar el dominio pendiente del
  especialista y esperar su resultado o evidencia antes de reanudar.
- CUANDO el especialista reciba un handoff válido EL SISTEMA DEBERÁ conservar sus
  gates, ejecutar solo su alcance y devolver un resultado con el mismo `handoff_id`.
- CUANDO el handoff se refiera a un dominio aplicable
  EL SISTEMA DEBERÁ incluir en `context_refs` las rutas exactas del contexto
  verificado (p. ej. `.architecture/README.md`, `.data/06-sensitive-data.md`).
- CUANDO el handoff se emita EL SISTEMA DEBERÁ limitar `write_scope` a la carpeta
  canónica del dominio destino (p. ej. `.data/`), sin rutas ajenas.

### H2 — Legibilidad del handoff

- CUANDO el usuario lea un handoff EL SISTEMA DEBERÁ mostrar `target`, `action`,
  `handoff_reason`, `scope` y `write_scope` de forma inequívoca.
- CUANDO `requires_confirmation` sea `true` EL SISTEMA DEBERÁ indicarlo
  explícitamente en el bloque.
- SI el handoff omite algún campo obligatorio ENTONCES EL SISTEMA DEBERÁ no
  considerarlo un handoff válido.

### H3 — Contrato bajo demanda

- EL SISTEMA DEBERÁ mantener el contrato en
  `canonical/skills/documentation-orchestrator/references/handoff.md`.
- EL SISTEMA DEBERÁ cargar el contrato solo al emitir o validar un handoff.
- EL SISTEMA DEBERÁ mantener el delta de contexto medible con
  `tools/measure_context.py` y aprobado por el usuario.

### H4 — Límites de delegación

- EL SISTEMA DEBERÁ excluir del handoff: commit, push, tag, release, remediación de
  `security`/`code-quality`, implementación de código y ejecución de Graphify.
- SI un dominio destino no es un especialista documental válido
  ENTONCES EL SISTEMA DEBERÁ no emitir el handoff.
- SI `write_scope` sale de la carpeta canónica del dominio
  ENTONCES EL SISTEMA DEBERÁ rechazar el handoff.
- CUANDO la acción sea de solo lectura EL SISTEMA DEBERÁ usar
  `write_scope: none` y `requires_confirmation: false`.
- EL SISTEMA DEBERÁ usar rutas relativas al proyecto, existentes y sin `..` en
  `context_refs` y `evidence`.
- EL SISTEMA DEBERÁ tratar `gate_state` como información del origen, sin aprobar
  ni omitir gates del agente especialista.

### H5 — Coste medible

- CUANDO se cierre el incremento EL SISTEMA DEBERÁ reportar el delta de palabras
  (agentes, skills, referencias) antes y después del cambio.

### H6 — Validación

- CUANDO se emita un handoff EL SISTEMA DEBERÁ ser verificable por una prueba que
  analice instancias válidas e inválidas, campos, correlación, rutas seguras,
  confirmación y `write_scope` acotado.

## Edge cases y errores

1. **Dominio sin carpeta existente**: el handoff debe recomendar bootstrap, no
   crearla por su cuenta.
2. **`target` no válido**: rechazar; no emitir.
3. **`write_scope` fuera de la carpeta del dominio**: rechazar; no emitir.
4. **Handoff con `requires_confirmation` omitido en escritura**: inválido.
5. **Token `{{...}}` sin resolver dentro del contrato**: `validate.py` ya lo
   rechaza; el contrato no debe introducir tokens nuevos.
6. **Ruta absoluta, externa o con `..`**: handoff inválido.
7. **Acción de solo lectura con `write_scope` distinto de `none`**: inválido.

## Supuestos

- El incremento 1 cubre solo documentación; `sdd` emitirá handoffs en el incremento 2.
- La portabilidad se garantiza por el bloque Markdown (sin APIs de subagentes).
- No se crea carpeta de delegación nueva.
- Los especialistas no emiten handoffs; solo los reciben y ejecutan su dominio.

## Fuera de alcance (incremento 1)

- Llamadas automáticas `task`/subagentes en OpenCode (piloto posterior).
- Emisión de handoffs desde `sdd` o cualquier especialista.
- Delegación de commits, releases, remediaciones o implementación de código.

## RNF clave (se auditarán en design y Fase 4)

1. **Coste de contexto**: delta medible y aprobado (H5).
2. **Portabilidad**: sin dependencia de APIs de subagentes (H3).
3. **Seguridad**: sin secretos, sin rutas fuera del dominio (H4).
4. **Idempotencia**: repetir una coordinación sin cambios no produce escrituras.
5. **Trazabilidad**: `context_refs` y `evidence` citan archivos reales.
