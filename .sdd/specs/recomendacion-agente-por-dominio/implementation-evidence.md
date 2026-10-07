# Evidencia de implementación — Recomendación de agente por dominio

Modo SDD: standard
Fase: Implementación
Estado: implementación completada — pendiente de Verification
Gate: Gates 1–3 aprobados; implementación autorizada por «implementa la spec»

## Baseline observado

- `git status --short`: cambios ajenos en `.sdd/specs/laboratorio-evaluacion-sdd/tasks.md`
  y `.opencode/commands/lab-pilot.md`; no se editaron.
- `python3 -B tools/test_sdd_contract.py`: exit 0, **345/345** comprobaciones.
- `python3 -B tools/measure_context.py`: agentes **3,476** palabras, skills **17,977**,
  referencias bajo demanda **13,788** (25 archivos).

## 1.1 — RED/GREEN contractual

Comando en ambos estados:

```sh
python3 -B -c 'import tools.test_sdd_contract as t; t.test_agent_routing_policy(); print(f"{t.PASSED}/{t.PASSED + t.FAILED} comprobaciones correctas"); raise SystemExit(bool(t.FAILED))'
```

- RED: exit 1, **0/1**; `routing: referencia canónica existe` falla por ausencia
  de `canonical/skills/sdd-spec/references/agent-routing.md`.
- GREEN: exit 0, **43/43**; referencia creada, criterios y contexto manual presentes.
- Artefactos: referencia canónica y función `test_agent_routing_policy` en
  `tools/test_sdd_contract.py`. Sin clasificador runtime ni dependencias nuevas.

## 2.1 — RED/GREEN de integración

RED:

```sh
python3 -B -c 'import tools.test_sdd_contract as t; t.test_agent_routing_integration(); print(f"{t.PASSED}/{t.PASSED + t.FAILED} comprobaciones correctas"); raise SystemExit(bool(t.FAILED))'
```

- Exit 1, **0/8**: faltan entradas en agente/skill, referencia bajo demanda,
  conservación de gates de tareas y ajuste de ausencia de README.

GREEN acumulado:

```sh
python3 -B -c 'import tools.test_sdd_contract as t; t.test_agent_routing_policy(); t.test_agent_routing_integration(); print(f"{t.PASSED}/{t.PASSED + t.FAILED} comprobaciones correctas"); raise SystemExit(bool(t.FAILED))'
```

- Exit 0, **51/51**. Artefactos: `canonical/agents/sdd.md`,
  `canonical/skills/sdd-spec/SKILL.md`, función `test_agent_routing_integration`.
- Las nuevas reglas conservan elección manual, autorización y gates. No se
  modifican los límites de los especialistas ni la política de avisos de modelo.
- Pruebas estáticas: no acreditan decisiones reales del LLM en un host.

## 3.1 — Guías y smoke

- Artefactos: `docs/agentes/sdd.md` y `docs/sdd-smoke.md`, con selección manual,
  restricciones y doce escenarios R01–R12. Registro runtime vacío explícitamente.
- `python3 -B tools/test_links.py`: exit 0, **4/4** pruebas del checker.
- `python3 -B tools/check_links.py`: exit 0, **71 archivos** revisados. Este segundo
  comando comprueba los enlaces reales del proyecto, no solo fixtures del checker.

## 3.2 — RED/GREEN de propagación

Comando focalizado:

```sh
python3 -B -c 'import tools.test_sdd_contract as t; t.test_agent_routing_generated(); print(f"{t.PASSED}/{t.PASSED + t.FAILED} comprobaciones correctas"); raise SystemExit(bool(t.FAILED))'
```

- RED: exit 1, **0/30**; los seis destinos todavía no incluían integración ni referencia.
- GREEN: `python3 -B tools/render.py` exit 0; después ejecución acumulada de
  `test_agent_routing_policy`, `test_agent_routing_integration` y
  `test_agent_routing_generated`: exit 0, **87/87**.
- `python3 -B tools/validate.py`: exit 0, **10 skills / 8 agentes / 6 plataformas**.
- Artefactos: agente, skill y `references/agent-routing.md` de SDD en `generated/`
  para Copilot, OpenCode, Kiro, Claude, Pi y Antigravity. Sin cambios en adaptadores
  ni edición manual de salidas generadas.

## Checks de implementación y coste

- `python3 -B tools/test_sdd_contract.py`: exit 0, **444/444** (baseline 345/345).
  Son 87 checks específicos nuevos y 12 adicionales de paridad de referencias.
- `git diff --check`: exit 0.
- `python3 -B tools/measure_context.py`: agentes **3,573** (+97) palabras,
  skills **18,091** (+114), referencias **14,490** (+702; 26 archivos).
  La política detallada queda bajo demanda, no duplicada íntegramente en el prompt.
- Se revisó `git diff` de agente, skill, tests y guías; el render solo propagó esas
  entradas y la referencia nueva. No cambió el contrato de handoff ni los especialistas.
- Una carpeta ajena `.sdd/specs/consolidacion-documentacion-core/` apareció durante
  la sesión; no se editó, al igual que los cambios ajenos del baseline.

## Transición pendiente

Tareas 1.1, 2.1, 3.1 y 3.2 completas con artefactos y evidencia anterior.
Tareas 4.1 y 4.2 pendientes: suite de Verification, matriz de evidencia y evaluación
conversacional real. Los checks de implementación anteriores no declaran terminada
la Fase 4 ni acreditan runtime. No se instaló el kit en perfiles del usuario.

Nivel de LLM recomendado para Verification: MEDIO. Reanudar cuando el usuario
indique continuar; sin gate de aprobación intermedio ni confirmación del modelo.
