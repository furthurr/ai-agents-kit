# Smoke test de recomendaciones de modelo

Valida manualmente los avisos `BAJO`, `MEDIO` y `ALTO` después de renderizar,
instalar una plataforma y reiniciar la herramienta.

## Tareas puntuales

Solicita una consulta o ajuste localizado a Architecture, Code Quality, Data & API,
Security y UI Design. Cada agente debe recomendar `BAJO` o `MEDIO` brevemente y
continuar sin pedir una confirmación exclusiva de modelo.

## Operaciones pesadas

Solicita a cada especialista una inicialización o auditoría completa. Debe hacer
solo un preflight barato, recomendar `MEDIO` o `ALTO`, explicar 1-3 motivos y
terminar el turno antes del barrido o cualquier escritura. Tras `continúa con el
actual`, no debe repetir el aviso por módulo, finding, componente o micro-paso.

## Invocación orquestada

Haz que Documentation Orchestrator recomiende y confirme explícitamente el nivel
para un especialista y el mismo alcance. Al continuar con ese especialista, no
debe repetirse el aviso de modelo; sus demás gates se conservan.

## Excepción Git y releases

Solicita preparar un commit o release. Git & Release Manager mantiene sus
confirmaciones operativas, pero no añade un Gate de modelo.

## Criterio de cierre

- Solo aparecen los niveles genéricos `BAJO`, `MEDIO` y `ALTO`.
- Ningún agente selecciona o cambia el modelo del host.
- Un cambio material de alcance recalcula el nivel; solo un nivel distinto repite
  el hard stop.
- Las tareas puntuales no cargan matrices detalladas ni quedan bloqueadas.
- `python3 tools/test_model_recommendations.py` y `python3 tools/measure_context.py`
  se registran como evidencia junto con plataforma, fecha y commit del kit.

## Última evidencia manual

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
