# Tareas — Guía documental gestionada en AGENTS.md

- Modo SDD: lite
- Fase: Quick Plan
- Estado: implementado, renderizado y verificado estáticamente.

- [x] 1.1 [TDD focalizado] RED: añadir a `tools/test_documentation_core.py` checks para la propiedad del orquestador, marcadores y preservación, idempotencia, conflictos, modos de solo lectura y no exportación por Navigator; observar fallos antes de editar prompts (Req 1.1–1.10).
  - Evidencia: baseline previo 12/12; RED observado en el contrato nuevo antes de los cambios canónicos; GREEN focalizado posterior 3/3 (`test_orchestrator_manages_portable_agents_md_documentation_block`, `test_navigator_delegates_agents_md_ownership_to_orchestrator`, `test_read_only_specialists_keep_write_gates`). La suite completa detectó además fallos concurrentes ajenos en contratos de agentes modificados durante esta sesión.
- [x] 1.2 GREEN: actualizar `documentation-orchestrator` y `project-navigator` para incluir el contrato de `AGENTS.md`, retirar la exportación directa competidora, conservar el gate global y limitar la escritura a operaciones aprobadas (Req 1.1–1.10).
  - Evidencia: contratos canónicos en `canonical/skills/documentation-orchestrator/{SKILL.md,references/workflows.md,references/project-context.md}` y `canonical/skills/project-navigator/{SKILL.md,references/bootstrap.md,references/config.md,references/sources.md,references/templates/config.template.yaml}`; tres tests contractuales focalizados pasan.
- [x] 1.3 Alinear las guías de uso y escenarios smoke existentes con la nueva propiedad y los límites de escritura, sin prometer comportamiento runtime (Req 1.1–1.10).
  - Evidencia: `docs/agentes/documentation-orchestrator.md`, `docs/agentes/project-navigator.md`, `docs/uso.md` y `docs/documentation-orchestrator-smoke.md` describen el plan global, la propiedad única y los casos de seguridad; `python3 -B tools/check_links.py` final revisa 85 archivos sin enlaces rotos.
- [x] 1.4 Renderizar las seis distribuciones desde fuentes canónicas y verificar contratos, paridad, enlaces y diff; registrar evidencia y límites runtime en `verification.md` (Req 1.1–1.10).
  - Evidencia: `tools/render.py`, `tools/validate.py`, contratos completos, enlaces y `git diff --check` pasan sobre el estado combinado solicitado. El smoke LLM no se ejecutó y no se declara comportamiento runtime.
