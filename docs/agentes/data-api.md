# Data & API Agent (retirado)

`data-api` ya no se distribuye como agente independiente. La skill
[`data-api`](../../canonical/skills/data-api/SKILL.md) permanece activa y la usa
**Developer** bajo demanda para implementar contratos, APIs, modelos, serialización,
persistencia e integraciones. Documentation Orchestrator la ejecuta localmente para
consultar o actualizar `.data/` mediante sus propios modos y gates.

Para implementar una característica que combine API, UI o negocio, selecciona
[`Developer`](developer.md). Para aplicar metodología Spec-Driven Development,
selecciona `sdd` explícitamente; Developer no activa SDD.

Las instalaciones anteriores pueden conservar el prompt del agente retirado hasta
que se solicite la migración opt-in `--migrate-retired-agents`; la actualización
normal instala el agente Developer y no elimina archivos locales.
