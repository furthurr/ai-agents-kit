# Verificación — Simplificación del agente SDD

- Modo SDD: standard
- Fase: Verification
- Estado: en progreso; automatización completada, smoke interactivo pendiente
- Gate 4: pendiente
- Requisitos: `requirements.md`, Gate 1 aprobado
- Diseño: `design.md`, Gate 2 aprobado
- Plan: `tasks.md`, Gate 3 aprobado

## Alcance verificado

Se verificó el contrato canónico y su propagación a Copilot, OpenCode, Kiro,
Claude Code y Pi. No se modificaron specs históricas ni se ejecutó instalación
global. Los cambios locales ajenos estaban presentes y fueron preservados.

## Ciclo de pruebas

- Estrategia: caracterización/regresión del contrato declarativo; no TDD
  productivo. Esta feature modifica reglas documentales y checks de contrato,
  no lógica runtime del renderer.
- Baseline: `python3 tools/test_sdd_contract.py` → **211/211**; también pasaron
  baseline de recomendaciones **141/141** e integridad **391/391** antes de editar.
- RED del contrato: **187/213** después de actualizar fuentes y expectativas pero
  antes de sincronizar las salidas derivadas; los fallos correspondieron a
  referencias/agentes generados todavía antiguos. No se presenta como RED de
  comportamiento conversacional ni como TDD.
- GREEN: `python3 tools/test_sdd_contract.py` → **213/213**.
- Suite final: comandos y resultados en la tabla de evidencia siguiente.
- Excepciones: los escenarios manuales que requieren ejecutar el agente instalado
  en cada plataforma siguen pendientes; los checks textuales no los sustituyen.

## Suite final

| Check | Resultado | Evidencia |
|---|---:|---|
| Contrato SDD | ✅ 213/213 | `python3 tools/test_sdd_contract.py` |
| Recomendaciones por fase | ✅ 141/141 | `python3 tools/test_model_recommendations.py` |
| Integridad del kit | ✅ 391/391 | `python3 tools/test_integrity.py` |
| Handoff y contratos relacionados | ✅ 33 tests | `python3 tools/test_handoff_contract.py` |
| Validación negativa | ✅ 16/16 | `python3 tools/test_validate.py` |
| Instalación en HOME temporal | ✅ 124/124 | `python3 tools/test_install.py` |
| Identidad MAS | ✅ 223/223 | `python3 tools/test_mas_identity.py` |
| Code Review preexistente | ✅ 7 tests | `python3 tools/test_code_review_contract.py` |
| Enlaces Markdown | ✅ 4/4 | `python3 tools/check_links.py && python3 tools/test_links.py` |
| Validación de distribución | ✅ | `python3 tools/validate.py` — 10 skills, 8 agentes, 5 plataformas |
| Paridad del render SDD | ✅ | `python3 tools/render.py --output <tmp>` + comparación de los cinco árboles SDD |
| Formato del diff | ✅ | `git diff --check` |

## Matriz de trazabilidad

`✅` significa evidencia automatizada o estática suficiente para el contrato del
repositorio. `⚠️` significa que la política está documentada y cubierta por
checks textuales, pero falta observar el flujo conversacional en un host instalado.

| Requisito | Tarea(s) | Test/check | Evidencia | Estado |
|---|---|---|---|---|
| R1.1 | 2.1, 2.2, 2.4, 3.2 | Contrato SDD | `canonical/skills/sdd-spec/SKILL.md`; `213/213` | ✅ |
| R1.2 | 2.2, 2.5, 4.2 | Smoke §13 | `docs/sdd-smoke.md:199-213`; ejecución interactiva pendiente | ⚠️ |
| R1.3 | 2.2, 3.2 | Contrato SDD | criterios de `direct`/`lite` y fallback `standard`; `213/213` | ✅ |
| R1.4 | 2.2, 3.2 | Contrato SDD | Quick Plan exclusivo de `lite`; `213/213` | ✅ |
| R2.1 | 2.1, 2.3, 3.2 | Contrato SDD | tres estrategias vigentes; `213/213` | ✅ |
| R2.2 | 2.3, 2.5, 4.2 | Smoke §14 | `docs/sdd-smoke.md:215-230`; ejecución interactiva pendiente | ⚠️ |
| R2.3 | 2.3, 3.2 | Referencia de testing | `canonical/skills/sdd-spec/references/testing.md`; `213/213` | ✅ |
| R2.4 | 2.3, 3.2 | Integrity + contrato | `integrity-gate.md`; evidencia RED/GREEN contractual | ✅ |
| R2.5 | 2.2, 2.3, 3.2 | Contrato SDD | separación de profundidad y testing; `213/213` | ✅ |
| R3.1 | 2.2, 2.3, 3.2 | Contrato + modelo | `model-selection.md`; `213/213`, `141/141` | ✅ |
| R3.2 | 2.2, 2.3, 3.2 | Integridad + enlaces | `test_integrity.py`, `test_links.py` | ✅ |
| R3.3 | 2.2, 2.5, 4.2 | Smoke §6 | `docs/sdd-smoke.md:106-116`; ejecución interactiva pendiente | ⚠️ |
| R3.4 | 2.3, 3.2 | Referencias SDD | PBT condicionado a invariante claro; `testing.md` | ✅ |
| R3.5 | 2.2, 2.3, 3.3 | Métricas y revisión | `design.md` = 187 líneas; no se trasladó carga `deep` a `standard` | ✅ |
| R4.1 | 2.2, 2.5, 4.2 | Smoke §13–14 | política de reanudación en `SKILL.md`; ejecución histórica pendiente | ⚠️ |
| R4.2 | 2.2, 2.5, 3.3 | Revisión de diff | specs históricas no modificadas; sin migración automática | ✅ |
| R4.3 | 2.2, 3.2 | Contrato de reanudación | marcadores/gates ambiguos requieren aclaración; `213/213` | ✅ |
| R4.4 | 2.1, 3.2 | Contrato de rutas | rutas planas/agrupadas y cinco salidas; `213/213` | ✅ |
| R5.1 | 2.4, 2.5, 3.1, 3.2 | Render/validación | cinco adapters y árboles generados; `validate.py` correcto | ✅ |
| R5.2 | 2.2, 2.5, 3.3 | Grep + contrato | menciones retiradas solo explicativas; smoke interactivo pendiente | ⚠️ |
| R5.3 | 2.1, 3.2 | Contrato SDD | checks de opciones vigentes y retiradas; `213/213` | ✅ |
| R5.4 | 1.1, 3.1, 3.3 | Integridad/diff | render temporal, sin reset/clean, `git diff --check` | ✅ |

## Self-check de RNF

| RNF | Evidencia | Estado |
|---|---|---|
| RNF-1 Consistencia entre cinco hosts | `test_sdd_contract.py` y `validate.py`; referencias generadas coinciden con canonical | ✅ |
| RNF-2 Reproducibilidad | render temporal con `--output`, comparación sin diferencias y `validate.py` correcto | ✅ |
| RNF-3 Preservación del working tree | revisión de `git status`; no se ejecutó render destructivo sobre `generated/`, y `test_validate.py` confirma validación no destructiva | ✅ |
| RNF-4 Proporcionalidad | `design.md` 187 líneas; `model-selection.md` 441 palabras; sin dependencia PBT nueva | ✅ |

## Quality-bar spot-check

- Capas, DI, singleton, I/O, persistencia y tipos de aplicación: no aplican a un
  cambio documental del contrato; no se añadieron capas, mocks ni dependencias.
- Errores e integridad: `integrity-gate.md` conserva evidencia RED/GREEN y la
  prohibición de marcar tareas sin artefacto.
- Testing adaptativo: la opción retirada no aparece en tablas de estrategias;
  TDD focalizado, regresión y caracterización permanecen.
- PBT: sigue condicionado a un invariante claro y a un test real; no se añadió una
  dependencia.

## Smoke manual pendiente

`docs/sdd-smoke.md` conserva 29 escenarios y documenta los nuevos casos de retirada
de `deep` y TDD estricto. No se ejecutó el agente instalado en repositorios
desechables para las cinco plataformas, por lo que aún no se ha observado en vivo:

1. rechazo de `deep` y aceptación de `standard`;
2. rechazo de TDD estricto y aceptación de TDD focalizado;
3. reanudación de specs históricas con esos marcadores;
4. separación entre aceptación de alternativa y aprobación de gates;
5. plan-only y transición completa de gates.

No se inventa esa evidencia. Estos huecos deben cubrirse antes de cerrar Gate 4 o
aceptarse explícitamente como limitación de esta verificación documental.

## Estado de cierre

La suite automatizada y la distribución están verdes. Gate 4 permanece pendiente
por los escenarios interactivos indicados arriba.
