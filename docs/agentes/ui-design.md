# UI Design Agent (retirado)

`ui-design` ya no se distribuye como agente independiente. La skill
[`ui-design`](../../canonical/skills/ui-design/SKILL.md) permanece activa y la usa
**Developer** bajo demanda para componentes, tokens, temas, accesibilidad visual,
UX y sistema de diseño. Documentation Orchestrator la ejecuta localmente para
consultar o actualizar `.design/` mediante sus propios modos y gates.

Para implementar una característica que combine UI, datos o negocio, selecciona
[`Developer`](developer.md). Para aplicar metodología Spec-Driven Development,
selecciona `sdd` explícitamente; Developer no activa SDD.

Las instalaciones anteriores pueden conservar el prompt del agente retirado hasta
que se solicite la migración opt-in `--migrate-retired-agents`; la actualización
normal instala el agente Developer y no elimina archivos locales.
