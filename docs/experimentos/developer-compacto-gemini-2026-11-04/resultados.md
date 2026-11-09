# Resultado — Developer actual, compacto y ODD de referencia

[Resumen](README.md) · [Protocolo previo](protocolo.md) · [Candidato congelado](candidato.md)

## 1. Decisión

**No recomendar la sustitución de Developer por el candidato v1.** El experimento
no demuestra el ahorro propuesto: B usó más tokens y tiempo en el agregado y
presentó más alertas PLAN. Se mantiene el agente actual, sin instalar la variante.
No es un rechazo de cualquier compactación futura ni un diagnóstico de daño
universal del prompt corto; se evalúa este texto, modelo, corpus y configuración.

Se ejecutaron 90 celdas únicas, diez escenarios × tres brazos × tres repeticiones,
con `google/antigravity-gemini-3.8-flash` en OpenCode 1.18.34. Timestamps UTC de
ejecución: 2026-11-05; el identificador de sesión conserva `20261104`.

## 2. Qué se modificó y qué permaneció igual

- A: agente Developer vigente, obtenido del derivado OpenCode del repositorio.
- B: cuerpo de agente compacto; skill Developer y referencias idénticas a A.
- C: ODD adaptado histórico como referencia, no la versión nueva del plan `.odd/`.

A/B usan los mismos identificadores públicos y descripción, con perfiles/procesos
independientes y una única ruta de skills por proceso. Su configuración, normalizada
por rutas y excluyendo solo el campo prompt, coincide. Los prompts funcionales
y estado de reanudación A/B también son iguales. No se indicó al modelo que B
fuera una variante «compacta» o debiera gastar menos.

El cuerpo del agente se redujo de **6.734 a 1.764 bytes: −73,80 %**, y de 931 a
234 palabras. Es volumen textual, no tokens ni tamaño completo de contexto.
La skill primaria A/B comparte SHA-256
`6b48601490fc41433d4c23c2ca836bced41f2e642fa6d87b5caf7f34614de1d2`.
Se conservaron 181 hashes de entradas sin cambios durante el ensayo.

La equivalencia del texto completo de las skills es un control experimental,
no prueba de comportamiento idéntico del modelo ni de todas las garantías de
producto. La propuesta concentra responsabilidades en la skill; una integración
real también exige revisar equivalencia de reglas y aspectos no ejercitados,
como arquitectura/patrones existentes, estados UI y cierre documental de dominios.

## 3. Métricas del lote completo

| Métrica, 30 celdas por brazo | A: Developer actual | B: compacto | C: ODD |
|---|---:|---:|---:|
| Aceptación funcional externa | 30/30 | 30/30 | 30/30 |
| Checks mecánicos de entrega | 30/30 | 30/30 | 30/30 |
| Carga correcta de skill por contenido | 30/30 | 30/30 | 30/30 |
| Tokens comparables | 4.086.432 | 4.365.908 | 3.050.838 |
| Duración agregada | 1.227,730 s | 1.428,999 s | 1.057,195 s |
| Mediana de duración por celda del corpus | 40,296 s | 43,719 s | 37,270 s |
| Pasos | 377 | 406 | 334 |
| Herramientas | 372 | 393 | 345 |
| Actualizaciones todowrite | 31 | 43 | 0 |
| Invocaciones CLI | 30 | 30 | 30 |
| Respuestas simuladas de usuario | 0 | 0 | 0 |
| Errores de herramienta recuperados | 0 | 1 | 1 |

**B vs A: +6,839 % tokens y +16,394 % duración.** C vs A: −25,342 % tokens y
−13,890 % duración, descriptivos de esta cohorte nueva. No combinar esos porcentajes
con el estudio anterior ni atribuir la diferencia C/A únicamente a longitud.

El tiempo corresponde a conversaciones CLI y checks del agente, sin esperas
humanas reales. Las evaluaciones externas posteriores quedan fuera. Es una suma
de celdas concurrentes, no wall-clock del lote ni una promesa de latencia de producto.

## 4. Medianas por tarea

Tres repeticiones por casilla. Se conservan todas; no se elige el mejor intento.

| Caso | Tokens A | Tokens B | Tokens C | Segundos A | Segundos B | Segundos C |
|---|---:|---:|---:|---:|---:|---:|
| S01 errata | 73.223 | 64.365 | 50.511 | 21,068 | 21,117 | 20,385 |
| S02 función pura | 144.996 | 116.895 | 108.552 | 35,401 | 41,507 | 37,631 |
| S03 validación | 129.693 | 121.921 | 117.557 | 46,759 | 43,033 | 37,828 |
| S04 Decimal | 132.003 | 121.317 | 103.502 | 38,701 | 37,945 | 35,757 |
| S05 CLI | 221.780 | 289.154 | 150.884 | 64,809 | 76,269 | 50,413 |
| S06 reglas literales | 183.732 | 171.244 | 134.548 | 55,990 | 58,634 | 43,788 |
| S07 persistencia | 165.952 | 256.720 | 128.670 | 44,622 | 57,017 | 39,876 |
| S08 reanudar | 145.376 | 184.831 | 132.598 | 49,641 | 50,143 | 41,583 |
| S09 planificar | 66.551 | 67.016 | 77.157 | 27,395 | 32,027 | 28,849 |
| S10 consultar | 44.245 | 37.674 | 26.275 | 28,156 | 20,248 | 15,080 |

B ahorró tokens sumados en S01, S02, S03, S04, S06 y S10, pero **no ganó en el
total de ninguna de las tres repeticiones**. Las tareas de CLI, persistencia y
reanudación compensaron o superaron los ahorros. La mediana global de tokens B
(123.344) fue menor que A (140.413), pero no reemplaza el presupuesto total fijado
como criterio. Promoverlo seleccionando esa mediana cambiaría la regla después
de observar el resultado.

## 5. Por qué un agente más corto terminó gastando más

La reducción del prompt fue real y la skill no cambió. Sin embargo, el modelo
produjo otra secuencia de acciones:

- B hizo **406 pasos frente a 377** (+7,69 %) y **393 herramientas frente a 372**
  (+5,65 %).
- Hubo **43 actualizaciones todowrite frente a 31**, sin una mejora funcional
  medida. Que ese seguimiento pueda ayudar en proyectos grandes no se prueba aquí.
- El promedio de tokens comparables por paso fue aproximadamente **10.753 en B
  y 10.839 en A**, apenas −0,79 %. El menor contexto inicial no se mantuvo como
  una reducción grande del contexto acumulado por paso.

Es una descomposición descriptiva, no una explicación causal exacta de cada token.
Reducir texto también puede cambiar la atención, selección de tareas y orden de
carga de referencias. Una skill idéntica no implica que el modelo la use igual.

### Ejemplo observado: persistencia, r1

Ambos cargaron la skill principal y data-api y entregaron cuatro tests finales
verdes. A realizó 13 pasos; B 20. B cargó la segunda skill antes y llamó todowrite
seis veces; A no usó todowrite en esa celda. La traza permite observar la secuencia
y la mayor exposición al contexto cargado, pero no asignar un porcentaje causal
exacto al cambio de orden.

### Caso costoso conservado: CLI, B-r1

Se registraron 365.244 tokens comparables y 183,707 s, además de un contador
reasoning de 20.869, sin guardar su contenido. A-r1 registró 204.974 tokens y
56,226 s. No se elimina ese caso por ser desfavorable ni se afirma que todo su
tiempo lo causara ese contador. Las otras dos medianas/réplicas también forman
parte de las tablas. La caché y el servicio del proveedor no se reiniciaron.

**La hipótesis de recuperar ahorro simplemente quitando repetición no quedó
confirmada para esta variante.** Eso matiza el análisis previo: una parte del
coste puede depender de cómo el prompt orienta las acciones, no solo de su tamaño.
No demuestra que Developer no pueda optimizarse, ni que la metodología ODD sea
intrínsecamente más económica en cualquier proyecto.

## 6. Calidad, fidelidad y herramientas

Los oráculos y las suites finales de comportamiento pasaron, y también las 63
suites originales ejecutadas sin modificar su código sobre las soluciones finales.
Las consultas conservaron archivos y los planes no implementaron la feature.
No hubo errores API, timeouts, métricas ausentes, invocaciones de skills ajenas,
llamadas malformadas detectadas ni accesos observados a otras raíces/perfiles.
Se contrastaron los hashes de las 90 trazas y 323 lecturas/búsquedas.

Los campos `successful_delivery`/`conforming_delivery` describen checks mecánicos;
no equivalen a fidelidad semántica perfecta ni a una auditoría exhaustiva.

- A ejecutó py_compile en **1/3** tareas PLAN; B en **3/3**. Aunque la fuente no
  cambió, genera bytecode y contradice el propósito de PLAN estrictamente sin
  efectos mutantes. Es una alerta más recurrente en B, no una prueba estadística
  de pérdida de todas las garantías de lectura.
- B tuvo un intento de limpieza de caché denegado. C tuvo un `ls` no autorizado
  denegado. Ninguno se reintentó como una celda nueva para borrar el error.
- C observó RED antes de código en 21/21 comportamientos; A en 7 y B en 6. No era
  un requisito universal de Developer; no penalizarlo por no adoptar TDD.
- Dos respuestas finales C omitieron `Risk:`. No se interpreta esa omisión como
  dos bugs de implementación o ausencia de todo análisis de riesgo.
- No se detectaron cambios en carpetas de contexto canónico. Las herramientas
  personalizadas de búsqueda/cuota heredadas del host no fueron llamadas; no se
  presenta la configuración como un bloqueo universal de red o un sandbox OS.

Los tests no cubren todas las entradas, UI/API distribuida, arquitectura real ni
cierre documental de un proyecto. Conservar skill/referencias por hash no prueba
equivalencia semántica de todos los refuerzos quitados del agente. Una integración
requiere revisar esas condiciones además de la aceptación de fixtures.

## 7. Tokens y coste

| Contador | A | B | C |
|---|---:|---:|---:|
| Input | 3.875.183 | 3.921.050 | 2.952.858 |
| Cache-read | 156.520 | 386.480 | 47.886 |
| Cache-write | 0 | 0 | 0 |
| Output | 54.729 | 58.378 | 50.094 |
| Reasoning separado | 1.360 | 20.869 | 0 |

La fórmula predefinida suma **11.503.178 tokens comparables**. Los totales SDK
suman 11.525.407; sus diferencias en 21 pasos se explican por reasoning separado,
22.229 tokens, sin diferencias no explicadas en el contraste del analizador.
El coste reportado fue cero; no acredita factura cero ni ahorro monetario.

B añadió 279.476 tokens comparables frente a A: 45.867 de input, 229.960 de
cache-read y 3.649 de output. La caché no tuvo el mismo reparto y no se reinició;
los precios y pesos de facturación no se pueden inferir de esa suma.

## 8. Aplicación del criterio previo

La propuesta requería al menos 10 % menos tokens frente a A, duración no peor
que +10 %, consistencia favorable en dos repeticiones/seis escenarios y ausencia
de regresiones esenciales o patrón nuevo de incumplimiento.

- Tokens: **no cumple**, +6,839 %.
- Duración: **no cumple**, +16,394 %.
- Escenarios favorables: seis, **sí cumple** ese componente.
- Repeticiones favorables de tokens totales: cero, **no cumple**.
- Aceptación funcional observada: completa; fidelidad PLAN necesita atención.

Decisión: **no promover v1**. Mantener el agente actual y conservar este candidato
solo como evidencia experimental. No se retoca para conseguir un resultado verde;
cualquier v2 necesita entradas y protocolo nuevos. Este ensayo no autoriza cambiar
el kit ni crea una razón para retirar Developer o activar ODD por defecto.

## 9. Evidencia y límites

[Ledger](evidencia/records.json), [summary](evidencia/summary.json),
[auditoría](evidencia/audit.json), [perfiles](evidencia/profiles.json),
[igualdad A/B](evidencia/equivalence.json), [congelación](evidencia/freeze.json),
[preflight](evidencia/preflight.json), [casos](evidencia/cases.json),
[oráculos](evidencia/oracles.json) y [procedencia](evidencia/provenance.json).

La evaluación es descriptiva, n=3 por escenario y no ciega para el coordinador.
Se comparten contexto global, plugin y condiciones de servicio; no hay una
reproducción completamente hermética. No afirmar significancia estadística,
equivalencia universal o que los resultados se apliquen a otros modelos/hosts.
Los snapshots finales y comandos están conservados; las trazas completas son
externas y su permanencia temporal no está garantizada. No se conserva razonamiento
privado ni datos de transporte del proveedor.

No se modificaron `canonical/`, `adapters/`, `generated/`, el perfil instalado,
el plan ODD del Escritorio ni los experimentos anteriores. Se preservaron los
cambios locales previos; no se hicieron commits, push, instalación o publicación.

## 10. Verificaciones de entrega

| Comando/control | Resultado |
|---|---|
| `python3 tools/test_developer_compact_benchmark.py` | 7/7 correctas, igualdad de skills/config/tareas/estado A/B. |
| `python3 tools/test_gemini_three_way.py` | 7/7 correctas del núcleo reutilizado, sin inferencia. |
| `python3 tools/validate.py` | Correcto: 11 skills, 5 agentes, 6 plataformas. |
| `python3 tools/check_links.py` | 116 Markdown correctos. |
| `python3 -m py_compile tools/developer_compact_benchmark.py tools/developer_compact_report.py tools/test_developer_compact_benchmark.py` | Correcto. |
| `git diff --check` | Correcto. |
| Análisis final | 181 entradas intactas, 90 trazas coincidentes y 63 suites originales correctas. |
| Procesos filtro/replicación | Finalizados; PIDs ausentes al cierre. |

Se añadieron el candidato/protocolo/registro y las herramientas de ensayo en
`tools/`, más el enlace de `docs/README.md`. No se ejecutó el renderer sobre el
árbol de distribución ni se sustituyó el agente habitual por un candidato que
no superó el criterio previsto.
