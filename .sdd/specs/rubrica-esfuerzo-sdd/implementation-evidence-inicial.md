# Evidencia de implementación — Rúbrica de esfuerzo SDD

> Evidencia histórica de la implementación inicial; no acredita la iteración de compactación.

- **Modo SDD:** standard
- **Fase:** Implementación
- **Estado:** implementación inicial realizada; su Verification está en verification-inicial.md
- **Gate 3:** aprobado por el usuario («procede»)
- **Gate 4 inicial:** resultados en verification-inicial.md

## Ciclo observado

TDD focalizado del contrato documental, no de un motor numérico ni de inferencias
de un modelo. Se modificaron primero las pruebas y luego las fuentes canónicas.

| Paso | Comando | Resultado observado |
|---|---|---|
| RED | `python3 -B tools/test_sdd_contract.py` | Exit 1; 427/474 comprobaciones correctas, 47 fallos por nueva etiqueta/bloque, casos y protocolo ReserveLab ausentes; generated aún tenía la salida anterior. |
| RED | `python3 -B tools/test_model_recommendations.py` | Exit 1; 5 tests ejecutados, 1 fallo en `test_sdd_alone_owns_feature_scoring_not_model_selection_gates`: no existía `Esfuerzo previsto del LLM:` en el agente. |
| Generación | `python3 -B tools/render.py` | Exit 0; seis plataformas regeneradas mediante el pipeline existente. |
| GREEN | `python3 -B tools/test_sdd_contract.py` | Exit 0; 474/474 comprobaciones correctas. |
| GREEN | `python3 -B tools/test_model_recommendations.py` | Exit 0; 5/5 tests correctos. |
| Ajuste mínimo | Refuerzo del control negativo y wrapping de skill | El mutante debe producir exactamente el diagnóstico esperado, no solo contenerlo entre fallos ajenos; sin abstracciones nuevas. |
| GREEN final de implementación | `python3 -B tools/render.py && python3 -B tools/test_sdd_contract.py && python3 -B tools/test_model_recommendations.py` | Exit 0; render correcto, 474/474 checks y 5/5 tests. |
| Inspección | `git diff --check` y revisión de diffs/rutas | Sin errores de whitespace en el diff versionado inspeccionado; cambios generados solo en las cuatro rutas SDD previstas por plataforma. |

Los resultados se observaron en la salida de herramientas de esta sesión; no se
inventan logs persistidos ni una ejecución CI remota. Los validadores completos,
enlaces e integridad del pipeline se ejecutarán en Verification; aún no acreditados.

## Artefactos por tarea completada

| Tarea | Artefacto/evidencia |
|---|---|
| 1.1 | `tools/test_sdd_contract.py`: `effort_contract_errors`, `table_rows` y `test_lab_effort_rubric`; RED y GREEN anteriores. |
| 1.2 | `tools/test_model_recommendations.py`: detector nuevo y exclusividad SDD; checks de consumidores/plantillas en `test_sdd_contract.py`; RED y GREEN. |
| 2.1 | `canonical/skills/sdd-spec/references/feature-level.md`: protocolo, perfiles 1–10, 10+, emisión, presentaciones, contrastes y procedencia. |
| 2.2 | `canonical/agents/sdd.md`, `canonical/skills/sdd-spec/SKILL.md` y `references/templates.md`: bloque nuevo/delegación sin modificar políticas operativas. |
| 3.1 | `docs/catalogo.md`, `docs/uso.md`, `docs/agentes/sdd.md`, `docs/agentes/README.md`. |
| 3.2 | `docs/sdd-smoke.md`, `docs/model-recommendations-smoke.md`: E01–E07 y registro manual pendiente. |
| 4.1 | `generated/` actualizado por render; `git diff --name-only -- generated/`: 24 archivos, cuatro consumidores SDD por plataforma, ningún otro agente/skill. |
| 4.2 | GREEN final, diez controles negativos y presente archivo de evidencia. |

La tarea 4.3 cubre la transición visible de implementación a Verification y se
cerrará al reanudar con evidencia del resumen emitido. Las tareas 5.1/5.2 permanecen
pendientes; no se crea `verification.md` ni se declara cierre anticipado.

## Cobertura discriminante

Las tablas canónicas se inspeccionan por sección/ID: perfiles, presentaciones y
casos de contraste. F01=1, F10-scaffold=8 y X13=10 se comprueban contra expectativas
explícitas independientes. Se enumeran las once presentaciones válidas y se exige
que no exista otra nota en la tabla. Los contrastes comprueban razones/supuestos
específicos, no longitud del texto ni cantidad de archivos.

Diez mutaciones detectadas con un único diagnóstico pertinente cada una:
F01=2, X13=9, F10-scaffold=10; emojis erróneos para 7/8/10; `11 🔴` en lugar de
`10+ 🔴`; eliminación de infraestructura proporcionada; exceso sin saga/compensación;
y nota verde que habilita lite. También se conservan los checks de modos, gates,
routing, ausencia de recomendaciones activas de modelo y referencias idénticas
en las seis plataformas.

Estos tests validan el contrato distribuido, no un clasificador automático ni el
razonamiento real del LLM. Los escenarios manuales E01–E07 siguen **no ejecutados**.

## Preservación y límites

Antes de escribir se verificó que canonical/tools/docs/adapters/generated no tenían
diffs ajenos. Se preservaron los cambios preexistentes en
`.sdd/specs/laboratorio-evaluacion-sdd/tasks.md`, `.security/`, el comando local
`lab-pilot` y specs locales del laboratorio. No se editaron laboratorio ignorado,
specs históricas, `.gitignore`, adapters, manifest, renderer, instaladores o CI.
No se instalaron configuraciones globales ni se ejecutaron modelos/Docker.

La rúbrica conserva 10/11 familias de Luna/MAX, C12 válido y fallo admin_create;
no presenta X13 como superado. El valor histórico 13 y los rangos F01–F10 no se
migran. La referencia instalada es autosuficiente sin `.agent-lab`.

Los consumidores de OpenCode generados no sustituyen la configuración cargada
en esta sesión. Si el usuario decide instalarlos posteriormente, deberá cerrar
y reiniciar OpenCode para que se carguen; esta feature no instala automáticamente.
