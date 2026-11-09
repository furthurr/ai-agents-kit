# ODD original vs ajustado — GPT-6 Luna max, 1.800s

**Estado: seis conversaciones completadas; ajustado 3/3 aceptaciones, original
2/3 según la regla de evaluación.** Nueva cohorte independiente con timeout
simétrico de1.800s, autorizada después de dos timeouts en el ensayo de600s.
Modelo solicitado `openai/gpt-6-luna`, variante CLI `max`, OpenCode1.18.34.
La variante se pasó explícitamente en cada llamada; la aplicación interna del
parámetro por el proveedor no se observa directamente.

## Resultado agregado

| Tres ejecuciones | ODD original | ODD ajustado |
|---|---:|---:|
| Conversaciones sanas | 3/3 | 3/3 |
| Nueve oráculos externos | 3/3 | 3/3 |
| Aceptación global predefinida | 2/3 | 3/3 |
| `data-api` por contenido | 0/3 | 3/3 |
| `ui-design` por contenido | 0/3 | 3/3 |
| Ambas antes del primer cambio de producto | 0/3 | 3/3 |
| Tokens comparables | 6.161.781 | 8.428.119 |
| Duración sumada (s) | 2.474,107 | 3.049,399 |
| Herramientas | 166 | 190 |
| Errores de herramienta | 7 | 5 |
| Respuestas simuladas | 0 | 0 |

El ajustado gastó **36,78% más tokens** y **23,25% más tiempo agregado**. Este
sobrecoste total se debe especialmente a la tercera ejecución; no prueba que en
todas las tareas o repeticiones el ajuste sea más caro, ni cuál regla causó el coste.
No se mide factura: tokens comparables=input+cache-read/write+output, reasoning
aparte; caché tiene precios potencialmente distintos. Suma de duración no es reloj.
Wall-clock del lote **3.230,919s** con evaluaciones y coordinación.

| Repetición | Original tokens / segundos | Ajustado tokens / segundos |
|---|---:|---:|
| R1 | 1.670.647 / 828,334 | **1.426.132 / 695,426** |
| R2 | 3.110.694 / 992,060 | **3.058.192 / 1.241,966** |
| R3 | **1.380.440 / 653,713** | 3.943.795 / 1.112,007 |

El ajustado usó menos tokens en2/3 repeticiones pero el coste elevado R3 domina la
suma. Se mantienen todas las celdas, incluso las desfavorables. n=3 no demuestra
significancia ni causalidad; longitud de instrucciones, consultas y método varían juntos.

## Qué significa la aceptación 2/3

En R2, ODD original pasó los **nueve oráculos externos** pero falló la suite conjunta
`catalog`, que contiene los archivos originales restaurados MÁS pruebas adicionales
creadas por el agente. La falla procedió de una prueba añadida que cierra la conexión
SQLite dentro de un `TestCase`, generando `Cannot operate on a closed database` y
errores posteriores. No es evidencia de que los nueve oráculos detectaran un bug de
producto. La regla predefinida exige ambas suites verdes y por ello cuenta como fallo.

Después del lote se ejecutaron por separado los módulos originales restaurados
`catalog.tests.test_models`, `test_forms` y `test_views` en esa misma solución:
**43/43 pasaron**. Esta comprobación diagnóstica adicional NO cambia la calificación
congelada: deja claro que el rojo provino de tests añadidos, no de los43 originales.

## Consultas, documentación y procedimiento

- Ajustado: cargó ambas skills por contenido y antes de modificar producto en3/3;
  leyó README en3/3 y `docs/lab-context.md` en2/3. Indicó en3/3 que README no
  mencionaba reservas y propuso `documentation-orchestrator`, sin editarlo.
- Original: no cargó ninguna skill de dominio en3/3; no leyó directamente README
  ni el contexto de proyecto y no propuso actualización documental en el cierre.
- Ajustado creó seguimiento `odd/tasks/reservation-flow.md` en1/3; original no
  creó Markdown de seguimiento en las tres. No se detectó bootstrap de documentación.
- Un detector mecánico observó RED antes del primer cambio de producto en3/3 por
  brazo. La semántica de cada RED requiere revisión específica: orden no acredita
  exhaustivamente test-first ni la aplicación de todos los estándares.
- Hubo llamadas denegadas/fallos de herramientas recuperados: 7 en original y5 en
  ajustado. No se relajaron permisos. No se detectaron errores API ni timeouts.
  Los deny de host no son sandbox OS ni certificación de seguridad universal.

Las tres recomendaciones documentales son una señal real de detección en este
proyecto/modelo, no prueban por sí solas que el orquestador actualice correctamente
la documentación: no se seleccionó ni ejecutó. No afirmar riesgo acumulativo
eliminado o equivalencia integral de agentes.

## Método y límites

Ambos brazos se ejecutaron nuevamente desde el mismo baseline documentado y mismo
TASK-2/LocalLibrary, con oráculos externos y los archivos de tests originales
restaurados en copia aislada. Orden de envío alternado y dos procesos concurrentes.
Dos preflights reales y referencia43+9 pasaron; inputs congelados intactos al cierre.
El único cambio operativo planeado respecto al lote anterior GPT fue timeout600→1800s;
no se reconstruye como si el lote anterior hubiera terminado. Las métricas de Gemini
permanecen en cohortes separadas. No se ejecutaron los cinco checks focalizados con
GPT en esta cohorte; los resultados con Gemini no deben atribuirse a este modelo.

**Conclusión:** para esta tarea, el ajuste hizo consistentemente las consultas y
la detección documental que se buscaban y tuvo 3/3 entregas aceptadas; el original
no hizo esas consultas y dejó una suite con error propio. El coste agregado del ajuste
fue mayor, con gran variabilidad, por lo que la decisión es un trade-off real entre
disciplina observada y consumo, no «igual de barato» ni superioridad universal.

## Evidencia

- [Protocolo](protocolo.md), [freeze](evidencia/freeze.json).
- [Detalle por celda y trazas de comportamiento](evidencia/summary-audit.json).
- [Resultados del lote](evidencia/batch-result.json), [preflights](evidencia/preflight.json).
- [Referencia](evidencia/reference-proof.json), [presupuesto](evidencia/budget.json).
- [Diagnóstico aislado 43 tests originales](verificaciones.json).
- [Laboratorio y trazas saneadas](laboratorio.tar.gz), [hashes](preservacion.json).

No se modificaron agentes instalados/canónicos ni el plan del Escritorio; sin commits
ni push. Archivos locales anteriores preservados. El lote600s previo y los dos lotes
Gemini parciales conservan sus fallos y no se incluyen en esta tabla.
