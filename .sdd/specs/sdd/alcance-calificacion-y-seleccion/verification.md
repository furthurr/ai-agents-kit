# Verificación — Alcance, calificación y selección de profundidad SDD

Modo SDD: standard
Fase: Verification
Estado: verificación automatizada completada; cierre pendiente
Gate 4: pendiente

## Resumen de implementación

- Agente y skill definen alcance común antes de modo y publican calificación antes
  de recomendar profundidad. Conservan elecciones previas, autorización y gates.
- Nueva referencia `canonical/skills/sdd-spec/references/scope-depth.md` contiene
  elegibilidad, casos 1–10+, atención controlable y división segura.
- Rúbrica conserva anclas y escala ordinal; atención se separa de esfuerzo.
  Presentación rutinaria omite referente/factores; artefactos conservan trazabilidad.
- Direct tiene cierre breve sin spec; lite conserva Quick Plan y evidencia compacta.
  Standard conserva sus Gates 1–4. Bugfix no trivial sigue en standard, sin nota.
- Documentación y escenarios manuales alineados; seis distribuciones regeneradas.
- Sin adaptadores nuevos, dependencias, instalación global, commit, push ni release.

## Ciclo de pruebas observado

Estrategia: TDD focalizado para contrato textual y checks para documentación/render.

1. RED: después de añadir `test_scope_depth_contract`, se ejecutó aisladamente
   mediante runpy. Resultado: 49 comprobaciones FAIL, exit 1. Faltaban la política
   común, reglas de selección, presentación y controles de atención/integración.
2. GREEN: tras implementar fuentes, misma función aislada: 49 PASS, exit 0.
3. Regresión: actualizar aserciones sustituidas por el contrato aprobado y mantener
   pruebas de anclas, negativos, gates, routing, reanudación y testing.
4. Refactor: compactar textos y plantillas para conservar los presupuestos existentes
   de contexto; añadir presupuesto separado para la política bajo demanda.
5. Suite final: 546/546 comprobaciones SDD, exit 0, incluidas paridad de referencias
   generadas, condiciones de atención, casos de división y presupuestos de contexto.

Durante verificación hubo fallos de presupuesto de contexto y espacios finales de
Markdown. Se corrigieron sin ampliar los presupuestos originales ni retirar controles;
los checks finales pasan. No se declara RED de conducta LLM: son contratos textuales.

## Comandos y resultados

| Comando/check ejecutado | Resultado observado |
|---|---|
| `python3 tools/render.py` | Exit 0; seis distribuciones regeneradas desde canonical. |
| `python3 tools/test_sdd_contract.py` | 546/546, exit 0; ejecución final mediante subprocess con salida resumida. |
| `python3 tools/test_model_recommendations.py` | 5 tests, OK, exit 0. |
| `python3 tools/test_handoff_contract.py` | 34 tests, OK, exit 0. |
| `python3 tools/test_integrity.py` | 415/415, exit 0; incluye validate, negativos de validación, enlaces e identidad/core. |
| `python3 tools/validate.py` | Exit 0: 10 skills y 6 agentes en 6 plataformas; paridad/reproducibilidad. |
| `python3 tools/check_links.py` | Exit 0: 68 archivos Markdown revisados. |
| `git diff --check` | Exit 0 después de corregir espacios finales. |
| `git diff --stat`, diff selectivo y `git status --short` | Fuentes/docs/tests y SDD generado; nueva referencia/spec visibles como no rastreadas, sin staging. |

## Matriz de requisitos

Las filas agrupadas cubren todos los IDs del grupo; evidencia de instrucciones y
checks estáticos, no certificación runtime del agente.

| Requisito | Tareas | Evidencia | Estado |
|---|---|---|---|
| 1.1–1.5 | 1, 4, 6 | SKILL.md, sección común; scope-depth.md/Definición común; test_scope_depth_contract y docs/agentes/sdd.md | Verificado estáticamente |
| 2.1–2.3 | 1, 2, 4, 6 | feature-level.md/Formato de salida, Registro interno; templates.md; tests de momento/presentación y plantillas | Verificado estáticamente |
| 2.4–2.5 | 2, 4, 6 | feature-level.md/colores; casos 6-controlado y 10; test_scope_depth_contract y negativos de atención | Verificado estáticamente |
| 2.6–2.7 | 2, 6 | agente/skill/feature-level.md; test_feature_level_contract conserva reanálisis y exclusión de bugs/consultas/exploraciones | Verificado estáticamente |
| 3.1–3.3 | 1, 4, 6 | scope-depth.md/Recomendación base y Casos de decisión; aserciones de tabla 1–3 y 4–9 | Verificado estáticamente |
| 3.4–3.5 | 2, 3, 6 | scope-depth.md/Complicaciones controlables; testing.md; casos 6-controlado/6-sin-garantías | Verificado estáticamente |
| 3.6–3.8 | 1, 3, 6 | scope-depth.md/Selección y continuidad; agente/skill; pruebas de selección, gates y autorización | Verificado estáticamente |
| 4.1–4.5 | 3, 4, 6 | scope-depth.md/Entregas incrementales; integrity-gate.md/Atención y entregas; escenarios A08/A09/A12 | Verificado estáticamente |
| 5.1 | 1, 4, 6 | SKILL.md/Modo direct; política y ejemplos 1/2/3; testing y evidencia breve | Verificado estáticamente |
| 5.2–5.3 | 1, 6 | Quick Plan y Flujo con gates; test_lite_quick_plan_contract, test_variants_and_evidence y Gates 1–4 | Verificado estáticamente |
| 5.4–5.6 | 3, 6 | agent-routing.md; barrera del agente; suites de routing y handoff conservadas | Verificado estáticamente |
| 5.7 | 1, 3, 6 | skill/política: solo planificación; tests de Quick Plan e intención | Verificado estáticamente |

## RNF y barra de calidad

| RNF | Evidencia | Estado |
|---|---|---|
| RNF-1: coherencia en seis distribuciones | render, validate y paridad byte a byte de referencias en test_sdd_contract | PASS |
| RNF-2: permisos/ejecutor/gates conservados | tests de routing, Gate 1–4 y handoff; diff sin adaptadores/permisos modificados | PASS estático |
| RNF-3: esfuerzo/atención/modo/intención separados | feature-level.md, scope-depth.md y templates; casos 6 naranja y selección | PASS estático |
| RNF-4: evidencia lite/direct proporcional | integrity-gate.md, testing.md y SKILL.md/Modo direct | PASS estático |
| RNF-5: sin reglas activas contradictorias | búsqueda selectiva en canonical/docs y diff: momento anterior y selección automática retirados; Quick Plan automático solo tras elegir lite | PASS de revisión |

Quality bar: responsabilidades separadas entre agente, política y renderer; sin lógica
duplicada por adaptador, infraestructura nueva ni abstracciones anticipadas. Tests
textuales honestos, errores corregidos y criterios transversales conservados. DI,
hilo UI y persistencia de producto no aplican a este ajuste del kit.

## Límites y seguimiento

- Smoke runtime nuevo A01–A12: NO EJECUTADO; documentado en docs/sdd-smoke.md.
- Paridad estática no acredita razonamiento ni conducta real en seis hosts.
- Pruebas lite reportadas por el usuario motivan política, no certifican todos los casos.
- Instalación local no ejecutada. La sesión activa conserva instrucciones ya cargadas.
  Para usar la actualización hay que instalarla por separado y reiniciar OpenCode.
- No quedan requisitos sin evidencia estática; validación runtime permanece como
  limitación explícita, no como requisito falsamente aprobado.

## Cierre

Implementación y verificación automatizada terminadas. Gate 4 pendiente de decisión
del usuario: cerrar con esta evidencia y limitaciones, o realizar smoke runtime adicional.
