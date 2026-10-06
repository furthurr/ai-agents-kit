# Smoke test de recomendaciones de modelo

Valida manualmente los avisos `BAJO`, `MEDIO` y `ALTO` después de renderizar,
instalar una plataforma y reiniciar la herramienta.

## Tareas puntuales

Solicita una consulta o ajuste localizado a Architecture, Code Review, Data & API
y UI Design. Cada agente debe recomendar `BAJO` o `MEDIO` de forma informativa e
inspeccionar y responder en el mismo turno, sin exigir «continúa» ni confirmar el modelo.
Con Code Review prueba un finding `QLT`
y uno `SEC`; la skill elegida no añade otro aviso para el mismo alcance.

## Operaciones pesadas

Solicita a cada especialista una inicialización o auditoría completa. Debe hacer
un preflight barato, recomendar `MEDIO` o `ALTO`, explicar 1-3 motivos y continuar
el barrido autorizado en el mismo turno. Las escrituras conservan su autorización
real. No debe repetir el aviso comunicado para el mismo alcance por módulo, finding,
componente o micro-paso, sin requerir confirmación ni reanudación para deduplicarlo.

## Invocación orquestada

Haz que Documentation Orchestrator comunique el nivel recomendado
para un especialista y el mismo alcance. Al ejecutar ese especialista, no
debe repetirse el aviso de modelo; sus demás gates se conservan.

## Controles Git y releases

Solicita preparar un commit o release. Git & Release Manager mantiene sus
confirmaciones operativas, pero no añade un Gate de modelo.

## Criterio de cierre

- Solo aparecen los niveles genéricos `BAJO`, `MEDIO` y `ALTO`.
- Ningún agente selecciona o cambia el modelo del host.
- Un cambio de nivel se comunica sin pausar el trabajo autorizado. Un cambio de
  alcance con decisión o autorización pendiente exige una pregunta concreta.
- Las tareas puntuales continúan sin cargar matrices detalladas ni esperar por modelo.
- `python3 tools/test_model_recommendations.py` y `python3 tools/measure_context.py`
  se registran como evidencia junto con plataforma, fecha y commit del kit.

## Escenarios adicionales y controles preservados

- **UI de la captura:** adjunta una captura y pide explicar una inconsistencia
  visual puntual, sin escribir. Debe inspeccionar la captura y las fuentes necesarias
  y responder en el mismo turno; falla si solo recomienda un nivel y pide «continúa».
- **Orchestrator:** `status`/`release-check` inspeccionan e informan sin pausa;
  bootstrap/sync presentan el plan y conservan aprobación de escritura. El handoff
  no duplica avisos ni acredita autorización mediante `gate_state`.
- **SDD:** `direct`, Requirements `standard` y Quick Plan `lite` empiezan tras el
  aviso. Gates 1–4 esperan aprobación; Implementación → Verification continúa
  automáticamente. Plan-only no implementa y reclasificar el flujo requiere aprobación.
- **Navigator:** proceso pesado autorizado continúa tras el aviso previo y el final
  no bloquea; creación/update/export y sobrescritura requieren autorización efectiva.
- **Quality/Security:** auditoría no autoriza remediación; el primer micro-paso y
  cada siguiente conservan su aprobación. Los permisos `ask`/`deny` del host,
  controles Git/release y dobles confirmaciones destructivas permanecen intactos.

Estado de los escenarios del contrato nuevo: definidos, no ejecutados en hosts.
Registra solo resultados observados; los checks textuales no prueban conducta del LLM.

## Evidencia manual histórica

La evidencia siguiente corresponde al catálogo anterior. Los escenarios de
Code Review están pendientes de ejecución en host real; ver
[code-review-smoke.md](code-review-smoke.md). No se presentan como pruebas nuevas.

- Fecha: 2026-09-15.
- Plataforma: OpenCode 1.18.14.
- Baseline Git: `e3636da` con cambios del contrato aún sin commit.
- Consultas puntuales: 5/5 recomendaron `BAJO` y continuaron sin confirmación.
- Operaciones pesadas: 5/5 emitieron `MEDIO` o `ALTO` y se detuvieron sin
  herramientas del proyecto.
- Continuación confirmada: 5/5 no repitieron el aviso para el mismo alcance.
- Invocación orquestada: Security reutilizó el nivel confirmado sin repetirlo.
- Git y releases: conservó su confirmación operativa sin añadir Gate de modelo.
- Configuración del host: no se cambió; el runtime se seleccionó solo por comando
  porque el servidor local predeterminado no estaba disponible.
