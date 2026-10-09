# Smoke transversal: ausencia de recomendaciones LLM

Este documento mantiene los resultados del contrato anterior como evidencia
histórica y define los checks manuales actuales. Ningún agente debe recomendar
niveles, modelos o proveedores LLM.

## Contrato actual

- Prueba tareas puntuales y operaciones amplias con Documentation Orchestrator,
  Architecture, Code Review, Data & API, Project Navigator y UI Design.
- Ninguna respuesta recomienda un nivel/cambio LLM ni pregunta qué modelo usar.
- Los agentes completan consultas autorizadas; estudios, propuestas, escrituras,
  remediaciones y operaciones de Git conservan sus aprobaciones propias.
- Un handoff no crea una recomendación LLM ni sustituye los gates del receptor.

## SDD

- Presenta un alcance de feature ambiguo y confirma que no emite clasificación hasta
  analizarlo y definirlo.
- Tras definir alcance, emite el bloque `Esfuerzo previsto del LLM: <nota e icono>`
  una sola vez antes de recomendar profundidad; 1–7 🟢 o 🟠 con atención especial,
  8–9 🟠, 10 🔴 y superior a X13: exactamente `10+ 🔴`.
  Registra referente, factores y supuestos en la spec sin mostrarlos rutinariamente según la
  [rúbrica compartida](../canonical/skills/sdd-spec/references/feature-level.md).
- Contrasta las condiciones manuales en
  [sdd-smoke](sdd-smoke.md#esfuerzo-previsto-del-llm-referencia-reservelab) y los
  [ejemplos opcionales](sdd-effort-examples.md). Verde no habilita lite.
  No presentes ejemplos ni checks textuales como inferencias ejecutadas.
- No repite la clasificación al pasar por Requirements, Design, Tasks,
  Implementación o Verification; no pausa ni pregunta por el modelo.
- Si cambia sustancialmente el alcance, vuelve a analizarlo antes de actualizar la
  clasificación. Esto no altera las aprobaciones de fase, alcance o implementación.

## Gates que se preservan

- Orchestrator presenta el plan global y espera autorización antes de escribir.
- SDD `standard` mantiene Gates 1–4; planificar no autoriza implementar.
- Quality/Security mantienen la aprobación del primer y cada siguiente micro-paso.
- Git/release mantiene sus confirmaciones operativas y las acciones destructivas,
  incluida la doble confirmación.
- Los permisos `ask`/`deny` del host permanecen efectivos.

Registra solo resultados observados con plataforma, versión, fecha y commit del kit.
Los checks textuales no prueban conducta del LLM.

## Evidencia manual histórica

La evidencia siguiente corresponde al catálogo anterior, que recomendaba niveles
de modelo. No acredita el contrato actual. Los escenarios de Code Review estaban
pendientes de ejecución en host real; ver
[code-review-smoke.md](code-review-smoke.md). No se presentan como pruebas nuevas.

- Fecha: 2026-09-15.
- Plataforma: OpenCode 1.18.14.
- Baseline Git: `e3636da` con cambios del contrato aún sin commit.
- Consultas puntuales: 5/5 recomendaron `BAJO` y continuaron sin confirmación.
- Operaciones pesadas: 5/5 emitieron `MEDIO` o `ALTO` y se detuvieron sin
  herramientas del proyecto.
- Continuación confirmada: 5/5 no repitieron el aviso para el mismo alcance.
- Invocación orquestada: Security reutilizó el nivel confirmado sin repetirlo.
- Git y releases: conservó su confirmación operativa.
- Configuración del host: no se cambió; el runtime se seleccionó solo por comando
  porque el servidor local predeterminado no estaba disponible.
