# Verificación — Rúbrica de esfuerzo SDD anclada a ReserveLab

> Verificación histórica de la implementación inicial; la compactación debe volver a verificarse.

- **Modo SDD:** standard
- **Fase:** Verification
- **Estado:** verificación completada; cierre pendiente de aprobación
- **Gate 1:** aprobado
- **Gate 2:** aprobado
- **Gate 3:** aprobado
- **Reanudación de Verification:** autorizada por el usuario («continúa»)
- **Gate 4:** pendiente

## 1. Ciclo y suite final

TDD focalizado de contratos documentales; no se añadió motor de scoring ni se
realizaron inferencias nuevas para simular una validación empírica. RED observado
antes de editar canonical: 47 fallos de 474 checks SDD y un fallo de cinco tests
de exclusividad/formato. GREEN posterior: 474/474 y 5/5. Detalle en
`implementation-evidence-inicial.md`; la reanudación permitió ejecutar Verification inicial.

| Comando final | Resultado observado | Exit |
|---|---|---|
| `python3 -B tools/test_sdd_contract.py` | 474/474 comprobaciones correctas; incluye anclas, presentaciones, contrastes, diez negativos, modos/gates/routing y paridad. | 0 |
| `python3 -B tools/test_model_recommendations.py` | 5/5 tests correctos; exclusividad SDD y ausencia de recomendaciones activas de modelo. | 0 |
| `python3 -B tools/validate.py` | Validación correcta: 10 skills y 6 agentes en 6 plataformas; reproducibilidad de generated sin modificarlo. | 0 |
| `python3 -B tools/check_links.py` | Enlaces Markdown correctos: 66 archivos revisados. | 0 |
| `python3 -B tools/test_integrity.py` | 415/415 checks correctos; también ejecuta validación negativa, enlaces, identidad MAS y contratos core. | 0 |
| `git diff --check` | Sin errores de whitespace en el diff versionado. | 0 |

Ningún fallo propio o preexistente apareció en la suite prevista. No se afirma
haber ejecutado todas las suites del repositorio ni CI remota. Los logs se
observaron en las herramientas de esta sesión, no en archivos de log inventados.
El checker de enlaces revisa su alcance de 66 archivos, no acredita todas las
rutas de specs locales; `git diff --check` no incluye archivos untracked.

## 2. Matriz de requisitos y evidencia

Abreviatura **REF**: `canonical/skills/sdd-spec/references/feature-level.md`.
**SDD-tests**: `tools/test_sdd_contract.py`, ejecutado 474/474.
**Exclusividad**: `tools/test_model_recommendations.py`, ejecutado 5/5.
Los estados ✅ describen contrato/artefactos verificados, no conducta de un host real.

| Requisito | Tareas | Test o revisión | Evidencia | Estado |
|---|---|---|---|---|
| R01 | 1.1, 2.1, 4.2, 5.1 | Revisar alcance completo solicitado, no proyecto/dependencias | REF: Comparación del esfuerzo, pasos 1–2; SDD-tests: alcance previo/feature completa | ✅ |
| R02 | 1.1, 2.1, 4.2, 5.1 | Diez dimensiones en protocolo y perfiles concretos | REF: Comparación del esfuerzo; `test_lab_effort_rubric` comprueba conceptos por sección | ✅ |
| R03 | 1.1, 2.1, 3.2, 4.2 | Contrastar infraestructura y trabajo pendiente, mismo comportamiento F10 | REF: F10-scaffold=8 frente a F10-sin-scaffold=9; checks de supuestos y negativo reutilización | ✅ |
| R04 | 1.1, 2.1, 4.2 | Revisión ordinal, sin suma ni proxies de tamaño/riesgo | REF: protocolo y procedencia; `test_lab_effort_rubric` comprueba ausencia de fórmula como regla | ✅ |
| R05 | 1.1, 2.1, 3.2 | Revisar datos esenciales frente a supuestos no esenciales | REF: paso 5 y Emisión; `test_feature_level_contract`: no provisional; docs/sdd-smoke.md: datos faltantes | ✅ |
| R06 | 1.1, 2.1, 4.2 | F01=1 en perfil y caso, mutante F01=2 rechazado | `effort_contract_errors`, `test_lab_effort_rubric`; REF: F01-base | ✅ |
| R07 | 1.1, 2.1, 4.2 | X13=10 en perfil y caso, mutante X13=9 rechazado | Mismos checks; REF: X13-base y resultado no redefine esfuerzo | ✅ |
| R08 | 1.1, 2.1, 5.1 | Diez filas/descriptores y revisión cualitativa de 2–9 | REF: Perfiles comparables; `effort_contract_errors`; sección 3 de este documento | ✅ |
| R09 | 1.1, 2.1, 4.2 | F10 con scaffold=8, mutante=10 rechazado; contrastar tres métodos | REF: alcance F10 y F10-scaffold; `effort_contract_errors`, negativos | ✅ |
| R10 | 1.1, 2.1, 3.2, 4.2 | 10+ por garantías adicionales e interacciones | REF: Superior al referente X13 y X13-ampliado; negativo exceso sin dimensiones | ✅ |
| R11 | 1.1, 2.1, 5.1 | Revisar superioridad material tras descontar soporte; no puntaje calculado | REF: Superior al referente X13; no señal aislada/volumen; contraste sintético etiquetado | ✅ |
| R12 | 1.1–1.2, 2.1–2.2, 3.1–3.2, 4.2 | Cuatro campos y motivos/supuestos | REF: bloque Emisión; agente/skill/plantillas; SDD-tests: formato y consumidores | ✅ |
| R13 | 1.1, 2.1, 4.2 | Enumerar 1–10/10+ y emojis; detectar notas/emojis inválidos | `effort_contract_errors`: dominio y tabla de presentación; negativos 7/8/10/11 | ✅ |
| R14 | 1.2, 2.1–2.2, 3.1–3.2, 4.2 | Exclusividad, momento, no repetir y reanálisis | `test_feature_level_contract`, Exclusividad; REF: Emisión | ✅ |
| R15 | 1.2, 2.1, 4.2 | Inspección de representación numérica e indicador separados | REF: Emisión; SDD-tests: campos indicador/numérico; no se introdujo DTO público nuevo | ✅ |
| R16 | 1.1–1.2, 2.1–2.2, 3.1–3.2, 4.3, 5.1 | Modos/gates/modelos/routing intactos; esfuerzo separado del resultado/riesgo | SDD-tests, Exclusividad y diff de agente/skill; REF: Emisión | ✅ |
| R17 | 1.1–1.2, 2.1–2.2, 3.1–3.2, 4.2 | Verde no habilita lite; negativo habilita-lite rechazado | REF: F07-verde-standard; `test_lab_effort_rubric` y `test_modes_remain_proportional` | ✅ |
| R18 | 1.1, 2.1, 3.1–3.2, 4.2 | Resultado parcial, C12 separado y admin_create, sin frontera universal | REF: Procedencia; `test_lab_effort_rubric`; contraste con veredictos locales leídos en Requirements | ✅ |
| R19 | 1.2, 2.2, 3.1–3.2, 4.1–4.2, 5.1 | Paridad en seis plataformas y docs activas actualizadas | SDD-tests y validate.py; 24 diffs generated; búsqueda de etiqueta antigua en canonical/docs sin coincidencias | ✅ |
| R20 | 1.2, 4.1, 4.3, 5.1 | Revisar pipeline y rutas alteradas frente al estado inicial | implementation-evidence-inicial.md; git status/diffs; adapters/manifest/renderer/instaladores/CI/.gitignore sin diff | ✅ |
| R21 | 1.1, 2.1, 3.1, 4.1, 5.1 | Rúbrica autosuficiente, sin import/test dependiente del laboratorio | REF: perfiles/contrastes/procedencia; SDD-tests usa canonical/generated, sin acceder a .agent-lab | ✅ |
| R22 | 1.1–1.2, 3.2, 4.2, 5.1–5.2 | Suites documentales y negativos, límites declarados | 474/474 + 5/5; docs/sdd-smoke.md: E01–E07 pendientes; secciones 1/5 de este documento | ✅ |

## 3. Revisión cualitativa de consistencia

- F01 mantiene formato exacto, validación de tipos/límites y ausencia de I/O/mutación;
  no se le añade persistencia o complejidad histórica para elevar su ancla 1.
- F02–F04 distinguen predicados/límites, reglas de redondeo ordenadas y agrupación
  con conflictos/idempotencia: descriptores observables, no cantidad de archivos.
- F05/F06 y F08/F09 se agrupan como perfiles cercanos. No se afirma equivalencia
  empírica; los descriptores reconocen concurrencia durable, recuperación y
  convergencia y explicitan infraestructura y límites de cada ejercicio.
- F10=8 se justifica por tres métodos sobre participantes, schema, helpers y locks
  correctos. F10-sin-scaffold=9 cambia soporte, no comportamiento funcional:
  construye ledgers/participantes/locking, pero no exige toda la composición X13.
- El 9 es una interpolación documental, no una prueba histórica adicional.
- X13=10 comprende offline, autoridad, sesiones, permisos, migración y recuperación;
  C12/evaluador no se suma al esfuerzo candidato. Su resultado parcial no cambia nota.
- El ejemplo 10+ añade saga/compensación externa pendiente y sus interacciones con
  todo X13. Tiene dimensiones concretas, no una suma arbitraria o palabra de riesgo.

## 4. Invariantes, RNF y quality bar

| Invariante | Evidencia | Resultado |
|---|---|---|
| F01=1/X13=10; rangos históricos intactos | Anclas/negativos correctos; no cambios realizados en catálogo/veredictos/specs históricos | ✅ |
| Solo 1–10 o 10+, icono correcto y exceso explicado | Tabla enumerada, seis contrastes y negativos en SDD-tests | ✅ |
| Verde no altera lite ni autoriza gates | F07 standard, negativo habilita-lite y checks de modos/gates | ✅ |
| Canonical manda y generated es reproducible | Paridad byte a byte de referencias; validate.py correcto en seis plataformas | ✅ |
| Preservación de historia/ajenos/globales | Estado inicial/final y ausencia de escrituras fuera de alcance; sin instalación global | ✅ |

| RNF | Evidencia | Resultado |
|---|---|---|
| RNF-1 autosuficiencia sin laboratorio instalado | Descriptores/supuestos en REF; tests no importan laboratorio; no enlaces obligatorios hacia carpeta ignorada | ✅ |
| RNF-2 paridad en seis plataformas | SDD-tests y validate.py; generated solo cambia cuatro consumidores por host | ✅ |
| RNF-3 políticas intactas | Diff acotado a reglas de scoring; pruebas de modos, gates, routing y ausencia de recomendación activa | ✅ |
| RNF-4 preservar historia/cambios ajenos | Estadísticas de las cinco rutas preexistentes sin variación: 87 inserciones/85 borrados; misma lista de untracked ajenos; no herramientas de escritura usadas sobre ellos | ✅ |
| RNF-5 sin red/modelos/dependencias; Python 3.10 compatible | No dependencias nuevas; helpers con tipos built-in y stdlib compatibles con 3.10; ejecución local Python correcta | ✅ por inspección de compatibilidad; ejecución nativa 3.10 no acreditada |

Quality bar: se conserva el límite canonical → adapters → generated, sin invertir
dependencias o crear scorer ficticio. Helpers locales tipados y reutilización de
harness, sin catches vacíos, mocks o capas runtime anticipadas. DI, persistencia,
I/O de UI y singletons no aplican a esta feature documental. PBT omitido con razón
en Tasks: no hay propiedad algebraica de una decisión ordinal.

Auditoría de Tasks: 1.1/1.2 corresponden a ambos tests; 2.1/2.2 a cuatro fuentes;
3.1/3.2 a seis docs; 4.1 a render/24 consumidores; 4.2 a RED/GREEN/evidencia;
4.3 al resumen visible seguido de «continúa»; 5.1 a suite final; 5.2 a este archivo.
No hay requisito huérfano ni tarea implementada sin artefacto/evidencia.

## 5. Límites y gate de cierre

- E01–E07 de host real **no ejecutados**. Se entregan escenarios y criterios; no se
  declara validación empírica del razonamiento de un modelo ni éxito del benchmark.
- No se realizaron campañas, reevaluaciones Docker o nuevas llamadas de modelos.
- No se instalaron consumidores ni se validó runtime de las seis aplicaciones.
- No se certifica ejecución nativa Python 3.10 ni CI remota; compatibilidad de
  helpers verificada por inspección. Suites observadas con **Python 3.12.4**
  (`python3 --version`) en el entorno local.
- Conservación de archivos ajenos contrastada con estado/diffs y las rutas escritas;
  no se presenta como una comparación criptográfica de todo el workspace ignorado.
- No hay commit, push ni release; estos requieren petición/autorización separada.

**Gate 4 pendiente:** ¿Cierro la spec o cubrimos los huecos?
