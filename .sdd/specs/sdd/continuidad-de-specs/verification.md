# Verificación — Continuidad de specs y contexto selectivo

Modo SDD: standard
Fase: Verification
Estado: cerrada con evidencia estática y límites runtime documentados
Gate 4: aprobado por el usuario («si»)

## Implementación

- Entrada breve en agente/skill: comprobar relación antes de recomendar modo;
  cargar continuidad solo ante relación o ambigüedad relevante.
- Nueva `canonical/skills/sdd-spec/references/spec-continuity.md`: búsqueda localizada,
  enmiendas, gates, estados, evidencia histórica, discrepancias y lectura progresiva.
- Enlaces y precedencias en scope-depth.md; revalidación en integrity-gate.md.
- Plantillas existentes suficientes: sin nuevos archivos obligatorios ni expansión.
- Guía, uso y escenarios C01–C10 alineados; seis distribuciones regeneradas.
- Sin adaptadores nuevos, dependencias, índices/cachés, instalación global o Git remoto.
- La spec previa `sdd/alcance-calificacion-y-seleccion` conserva su evidencia y
  Gate 4 pendiente; esta ampliación no la cierra ni reescribe sus resultados.

## Ciclo y comandos observados

TDD focalizado para contrato textual; checks de documentación, render y presupuestos.

- RED: tras añadir test_spec_continuity_contract, ejecutar aislado con runpy:
  19 FAIL y 5 PASS de 24 checks, exit 1. Faltaba política, integración, precedencias
  y controles. Las cinco mutaciones no acreditaban contrato porque su presencia
  en fuente fallaba; se exigió alcanzar fuente real además de detectar el defecto.
- GREEN: implementar política e integración; 24/24 PASS, exit 0. Un negativo inicial
  no sustituía la variante con mayúscula; se corrigió mediante sustitución insensible
  a mayúsculas. Ningún caso negativo se omitió.
- Refactor: compactar agente/skill para respetar presupuestos existentes sin ampliarlos.
  Añadir límite independiente para referencia y escenarios estáticos de contexto.
- Suite final: 586/586 PASS, incluidas 24 comprobaciones de continuidad, mutaciones,
  paridad de referencias en seis plataformas y presupuestos. No es un RED/GREEN de
  conducta runtime de un LLM ni una simulación funcional del clasificador.

| Comando/check | Resultado |
|---|---|
| `python3 tools/render.py` | Exit 0; seis distribuciones regeneradas. |
| `python3 tools/test_sdd_contract.py` | 586/586, exit 0; ejecutado mediante subprocess con resumen de salida. |
| `python3 tools/test_model_recommendations.py` | 5 tests OK, exit 0. |
| `python3 tools/test_handoff_contract.py` | 34 tests OK, exit 0. |
| `python3 tools/test_integrity.py` | 415/415, exit 0; ejecución mediante subprocess con resumen. |
| `python3 tools/validate.py` | Exit 0: 10 skills, 6 agentes, 6 plataformas; paridad/reproducibilidad. |
| `python3 tools/check_links.py` | Exit 0: 69 archivos Markdown revisados. |
| `git diff --check` | Exit 0. |
| `git diff --stat` y diff selectivo | Fuentes, docs, tests y salidas SDD; sin cambios de adaptadores/permisos. |

## Contexto medido

Palabras/caracteres de archivos canónicos: no tokens reales. Límites anteriores
se conservaron. El contenido de specs/código y el costo de búsqueda no se incluyen.

| Componente | Palabras | Caracteres | Presupuesto |
|---|---:|---:|---|
| Agente | 1051 | 7553 | <1066 / <7580 |
| Skill | 2343 | 16357 | <2357 / <16378 |
| Plantillas | 837 | 5720 | ≤863 / ≤5722 |
| Continuidad bajo demanda | 809 | 5843 | <1200 / <9000 |
| Selección bajo demanda | 1083 | 7473 | <1400 / <11000 |

| Ruta estática ilustrativa | Instrucciones consideradas | Palabras | Caracteres |
|---|---|---:|---:|
| Cambio aislado | Agente + skill | 3394 | 23910 |
| Spec conocida | Agente + skill + continuidad | 4203 | 29753 |
| Enmienda con plantillas | Agente + skill + continuidad + selección + plantillas | 6123 | 42946 |
| Candidatas múltiples | Agente + skill + continuidad | 4203 | 29753 |

Estas composiciones no son lecturas reales observadas ni un costo total de sesión.
La ruta con enmienda incluye referencias opcionales según operación; no obliga
a cargar plantillas/selección cuando no se necesitan. Candidatas múltiples puede
requerir más contenido de proyecto que una spec conocida aunque el texto fijo coincida.
No se declara ahorro ni equivalencia entre caracteres y tokens. No hay caché persistente.

## Matriz de requisitos

Cobertura del contrato escrito; filas agrupadas cubren todos los IDs indicados.

| Requisito | Tareas | Evidencia | Estado |
|---|---|---|---|
| 1.1–1.4 | 1, 5, 7 | agente/skill, spec-continuity.md/Búsqueda localizada; escenarios C01/C02/C08 y tests de política | PASS estático |
| 1.5–1.6 | 1, 5, 7 | distinción de relaciones y no afirmar ausencia global; negativo de búsqueda y caso código-spec | PASS estático |
| 2.1–2.3 | 2, 7 | Enmiendas y gates: actual/propuesto, ID y precedencia; negativo no evade y caso nota-2-enmienda | PASS estático |
| 2.4–2.6 | 2, 7 | dependencias/aprobaciones afectadas, autorización y no implementar; negativo y caso gate-3-pendiente | PASS estático |
| 3.1–3.2 | 3, 7 | Estado y evidencia, integrity-gate.md; revalidación selectiva e historia, negativo de revalidación | PASS estático |
| 3.3–3.5 | 3, 5, 7 | spec cerrada, vigencia/legacy/autoridad; casos cerrada, C06/C08 y pruebas de reanudación previas | PASS estático |
| 4.1–4.2 | 3, 7 | Impacto y continuidad; casos código-spec/cambios-relacionados y negativo no sumar | PASS estático |
| 4.3–4.4 | 3, 7 | elección ligada a alcance aceptado; scope-depth.md y escenarios C09/C10 | PASS estático |
| 5.1–5.2 | 1, 4, 7 | carga condicional en entradas y Contexto proporcional; C01/C02; lectura progresiva | PASS estático |
| 5.3–5.4 | 3, 4, 7 | reutilizar/revalidar según fuentes/alcance; sin índice/caché persistentes; C10 | PASS estático |
| 5.5–5.6 | 4, 7 | test_sdd_effort_context_budgets y tablas de este reporte; presupuesto y límites de medición | PASS estático |

## RNF y calidad

| RNF | Evidencia | Resultado |
|---|---|---|
| RNF-1: contexto acotado | Presupuestos originales más referencia independiente, checks PASS | PASS |
| RNF-2: enmienda no evade acuerdos/gates | Normas, casos nota-2/gate-3 y mutaciones negativas; suites previas conservadas | PASS estático |
| RNF-3: evidencia histórica no acredita cambio | Estado/evidencia e integrity; negativo de revalidación | PASS estático |
| RNF-4: paridad reproducible | render, validate y checks de referencias idénticas | PASS |
| RNF-5: elecciones y lectura por alcance/impacto | Contexto proporcional, Impacto/continuidad, entradas condicionales y escenarios | PASS estático |

Barra de calidad: responsabilidades separadas sin lógica por adaptador, capa de
infraestructura ni duplicación extensa de workflow. Sin dependencias de testing.
DI/UI/persistencia de negocio no aplican. Pruebas negativas reales sobre instrucciones,
sin declarar comportamiento LLM observado. Plantillas existentes no se expandieron.

## Límites y cierre

- Smoke runtime C01–C10: NO EJECUTADO; documentado en docs/sdd-smoke.md.
- No hay medición de tokens/búsquedas/lecturas reales ni certificación en seis hosts.
- No se instaló globalmente; cerrar/reiniciar OpenCode después de instalar por
  separado es necesario para cargar la actualización, no basta este cambio de archivos.
- Sin commit, push, release ni cierre automático de la spec anterior.
- Gate 4 de esta ampliación aprobado por el usuario («si»). Se cierra con evidencia
  estática y los límites declarados; smoke runtime continúa no ejecutado.
