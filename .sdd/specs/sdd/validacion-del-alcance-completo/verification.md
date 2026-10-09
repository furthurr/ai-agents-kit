# Verificación — Presentación y validación del alcance completo

Modo SDD: standard
Fase: Verification
Estado: cerrada con evidencia estática y límites runtime documentados
Gate 4: aprobado por el usuario («si»)

## Implementación y acuerdos

- Política común en scope-depth.md: alcance funcional completo, validación explícita
  previa, pregunta conjunta, respuesta solo modo, ajustes y aprobación vigente.
- Formato de feature-level.md: Alcance definido completo antes de nota/atención/modo.
  Reutilizar solo aprobación explícita de la misma versión; cuotas de frases retiradas.
- Agente/skill con entrada breve y flujos direct/lite ligados a alcance validado;
  Quick Plan no vuelve a calificar ni solicita aprobación rutinaria de requirements.
- Continuidad/integridad conservan versiones, historia, gates y exposición de
  diferencias funcionales durante formalización. Seleccionar ejecutor no valida alcance.
- Documentación incluye ejemplo completo y escenarios A01–A19 pendientes de runtime.
- Seis distribuciones regeneradas; plantillas existentes sin expansión ni cambios de adaptadores.
- Evidencia de specs anteriores conservada: continuidad cerrada y Gate 4 de alcance
  inicial pendiente. La regla local de resumen breve queda sustituida, no publicada.
- Sin instalación global, commit, push, bump, tag o release en esta ampliación.

## Ciclo de pruebas

TDD focalizado del contrato textual. No representa un ciclo de comprensión runtime LLM.

1. RED: reemplazar checks del resumen por test_full_scope_contract y ejecutarlo
   aisladamente con runpy: 13 FAIL, 8 PASS de 21 comprobaciones, exit 1. Faltaban
   alcance completo, validación, respuestas, integración e invariantes de modos.
   Los negativos exigían además alcanzar la fuente real; sin ese antecedente los
   PASS de detección no acreditaban un contrato correcto.
2. GREEN: implementar reglas y entradas; mismas comprobaciones 21/21 PASS, exit 0.
3. Complementar negativos de espera previa, versión aceptada y alcance actualizado
   y checks de diferencias/autoridad; 27 comprobaciones del nuevo bloque en suite final.
   Son cobertura adicional del contrato ya implementado, no RED nuevo inventado.
4. Refactor: compactar entradas sin ampliar presupuestos; revisar orden de
   presentación/calificación/validación y evitar calificación repetida en Quick Plan.
5. Suite final: 613/613 PASS, exit 0, con regresiones previas, negativos, gates,
   routing, reanudación, presupuestos y paridad byte a byte de referencias.

## Comandos y resultados

| Comando/check ejecutado | Resultado observado |
|---|---|
| `python3 tools/render.py` | Exit 0; seis distribuciones desde canonical. |
| `python3 tools/test_sdd_contract.py` | 613/613, exit 0; ejecutado con subprocess y salida resumida. |
| `python3 tools/test_model_recommendations.py` | 5 tests OK, exit 0. |
| `python3 tools/test_handoff_contract.py` | 34 tests OK, exit 0. |
| `python3 tools/test_integrity.py` | 415/415, exit 0; subprocess con resumen. |
| `python3 tools/validate.py` | Exit 0: 10 skills, 6 agentes, 6 plataformas; paridad/reproducibilidad. |
| `python3 tools/check_links.py` | Exit 0: 69 archivos Markdown revisados. |
| `git diff --check` | Exit 0. |
| Búsqueda selectiva en canonical/docs | Sin reglas operativas de resumen de 1–3 frases; resumen de ejecución no es alcance. |
| `git diff --stat`, diff selectivo y status | Solo fuentes SDD/docs/tests/generados y nueva spec; sin staging ni cambios de versión. |

## Matriz de requisitos

Filas agrupadas cubren todos los IDs indicados; prueba de instrucciones, no conducta real.

| Requisito | Tareas | Evidencia | Estado |
|---|---|---|---|
| 1.1–1.4 | 1, 4, 6 | scope-depth.md/Alcance completo y validación, formato y ejemplo completo; test_full_scope_contract comprueba campos | PASS estático |
| 1.5–1.7 | 1, 5, 6 | Sin recorte/invención, aclaración esencial; negativo de cuota y comportamiento principal en lugar del conjunto | PASS estático |
| 2.1–2.3 | 2, 3, 6 | Espera previa, pregunta conjunta y tabla de respuestas; negativos de validación implícita, espera tardía y selección que valida | PASS estático |
| 2.4–2.6 | 2, 6 | Misma versión vigente, 10/10+ y tratamiento sin nota de bug/consulta; negativo de versión indiscriminada | PASS estático |
| 3.1–3.4 | 2, 3, 6 | Conjunto actualizado, no delta, aprobación incompatible y entregas; negativos de actualización/versiones | PASS estático |
| 4.1–4.2 | 3, 6 | SKILL.md/Modo direct y Quick Plan; tests de alcance validado/sin spec/sin Gates 1–3 | PASS estático |
| 4.3–4.4 | 3, 6 | Gate 1 conservado, negativo de equivalencia, comparación de formalización en integrity-gate.md | PASS estático |
| 4.5–4.6 | 3, 6 | spec-continuity.md: versión vigente, enmienda completa, reanudación sin reinicio; regresiones previas y nuevas | PASS estático |
| 4.7–4.8 | 3, 6 | Routing manual previo conservado, validación no inferida por ejecutor, planificación no autoriza código; suite SDD y handoff | PASS estático |

## Contexto y RNF

Medidas de archivos de instrucciones: palabras/caracteres, no tokens reales ni cuota
de alcance mostrado. Budgets anteriores intactos; salida funcional completa es variable.

| Componente | Palabras | Caracteres | Límite anterior |
|---|---:|---:|---|
| Agente | 1054 | 7570 | <1066 / <7580 |
| Skill | 2335 | 16310 | <2357 / <16378 |
| Plantillas | 837 | 5720 | ≤863 / ≤5722 |
| Selección/alcance | 1364 | 9523 | <1400 / <11000 |
| Rúbrica/formato | 909 | 6447 | <1774 / <12303 |
| Continuidad | 848 | 6160 | <1200 / <9000 |

| RNF | Evidencia | Estado |
|---|---|---|
| RNF-1: alcance completo y validación vigentes | Campos/reglas, tabla de respuestas, negativos de espera y aprobación | PASS estático |
| RNF-2: presupuestos sin recorte funcional | Checks de contexto y ausencia de cuotas operativas de frases | PASS |
| RNF-3: coherencia de seis distribuciones | render, validate, paridad de referencias y entradas | PASS |
| RNF-4: decisiones independientes | Gates 1–4, validación/elección, solo planificación y routing conservados | PASS estático |
| RNF-5: resumen retirado, historia conservada | Revisión selectiva, docs actuales, specs anteriores sin sobrescritura | PASS de revisión |

Quality bar: separación política/renderer/adaptadores; sin nuevas dependencias,
infraestructura, índices ni caché. DI, UI y BD de negocio no aplican. Evidencia
honesta y errores explícitos, sin abstracciones anticipadas ni certificado runtime.

## Límites y cierre

- Smoke conversacional A01–A19/C01–C10: NO EJECUTADO; expectativas documentadas.
- Tests textuales no certifican comprensión del usuario ni decisiones en seis hosts.
- No se midieron tokens reales; presentación completa puede consumir más salida.
- No se instaló globalmente. Tras instalar por separado, reiniciar OpenCode para
  cargar instrucciones nuevas; esta sesión conserva el contrato ya cargado.
- Estado local sin commit/push/release. Gate 4 propio aprobado por el usuario («si»);
  cierre con evidencia estática y limitaciones declaradas. Smoke runtime permanece
  no ejecutado; esta aprobación no cierra por inferencia otra spec.
