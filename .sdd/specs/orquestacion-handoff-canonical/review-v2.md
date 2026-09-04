# Segunda auditoría final — orquestacion-handoff-canonical

Fecha: 2026-09-03

## Dictamen

**APTO CONDICIONADO como MVP canonical portable por contrato y distribución.**
No se declara estable ni portable en comportamiento hasta ejecutar el smoke en
las tres plataformas y versionar la entrega atómicamente.

## Problemas corregidos durante la reauditoría

- Eliminada la doble ejecución: skill local o handoff, nunca ambas.
- `mode` ambiguo sustituido por `action` + `handoff_reason`.
- Handoff situado antes del cierre global.
- Añadidos `handoff_id`, `project_root`, status y resultado correlacionado.
- Añadido protocolo receptor mínimo a seis agentes, centralizado en la referencia.
- Aclarado que `write_scope` no es un permiso técnico ni un sandbox.
- Añadido validador semántico reutilizable (`tools/handoff_contract.py`).
- Parser estricto: rechaza campos duplicados, extra, claves inválidas y texto libre.
- Tabla cerrada de confirmación y escritura.
- Rutas seguras: multiproyecto, absolutas, Windows, `..`, fragmentos y symlinks.
- Bootstrap permite carpeta ausente, pero rechaza scope existente que escape.
- Evidencia correlacionada al `handoff_id`, `project_root` y scope original.
- Ambos ejemplos canónicos se validan automáticamente.
- CI valida el repositorio antes de regenerar `generated/`.
- Smoke productor–receptor añadido a la documentación.

## Valor para el proyecto

**Suma** porque aporta una continuidad portable entre agentes reales, conserva
sus roles/gates, evita duplicación y ofrece contrato/test reutilizable sin añadir
una skill o un agente nuevo. La lógica detallada permanece bajo demanda.

El coste fijo es **+345 palabras** y el contrato bajo demanda **+742 palabras**.
Es mayor que la primera estimación, pero está justificado por seis receptores y
por controles que evitaron falsos positivos y rutas inseguras. No se debe ampliar
a SDD hasta demostrar su utilidad en el smoke y medir una tarea real.

## Riesgos restantes

### Medio — Smoke conversacional pendiente

Los 24 tests demuestran contrato, parser, distribución y receptores declarados;
no demuestran que todos los modelos produzcan/consuman el bloque igual. Ejecutar
`docs/documentation-orchestrator-smoke.md` en Copilot, OpenCode y Kiro.

### Medio — Enforcement runtime dependiente del host

El parser no es invocado automáticamente por los hosts. Las restricciones de
runtime siguen siendo instrucciones al modelo y permisos de plataforma. Esto está
documentado y no debe presentarse como aislamiento técnico.

### Entrega — Baseline Git pendiente

Canonical, generated, tests, CI, docs y spec deben entrar en una revisión atómica.
Hasta entonces el working tree valida, pero `HEAD` no contiene la implementación.

### Baja — Coste/ahorro real no medido

`measure_context.py` cuenta palabras, no tokens por tarea ni turnos adicionales.
No afirmar ahorro hasta comparar un flujo con y sin handoff.

## Recomendación

1. Ejecutar el smoke en las tres plataformas.
2. Registrar versiones/modelos/fecha/evidencia.
3. Medir al menos un flujo multi-dominio con y sin handoff.
4. Solo después decidir si habilitar handoff desde SDD.
