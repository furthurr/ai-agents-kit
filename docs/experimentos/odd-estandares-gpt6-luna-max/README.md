# ODD histórico / ODD ajustado — GPT-6 Luna max

**Estado: lote parcial; ambos brazos agotaron 600s en R1, R2/R3 no iniciados.**
No existe base suficiente para recomendar uno por eficiencia ni por calidad completa.

## Modelo y configuración

`openai/gpt-6-luna`, variante CLI `--variant max`, registrada en cada invocación,
OpenCode 1.18.34. El catálogo expone `max` y el runner la incluyó explícitamente;
la aplicación interna efectiva por el proveedor no es observable. Se omitió
temperatura porque el catálogo indica que el modelo no la admite. Mismo modelo,
variante, permisos, proyecto, tarea, oráculos y límite configurado para ambos brazos.
No se usa ni intenta acceder a Gemini. Nueva cohorte, no mezclar sus métricas con Gemini.

## Resultado R1

| Métrica observada hasta el corte | ODD histórico | ODD ajustado |
|---|---:|---:|
| Conversación | Timeout 600s | Timeout 600s |
| Nueve oráculos externos | 9/9 | 0/9 |
| Suite `catalog` restaurada + pruebas añadidas | Falla una prueba añadida por el agente | Falla; implementación incompleta |
| Aceptación global del snapshot | No | No |
| Tokens observados parciales | 1.076.576 | 523.574 |
| Duración | 600,257s | 600,256s |
| data-api / ui-design cargadas | 0 / 0 | 1 / 1 |

Los tokens son parciales y no comparan entregas completas. La variante ajustada
cargó ambas skills pero el detector no acredita que ambas se cargaran antes del
primer cambio de producto. El original aprobó los nueve oráculos externos, pero su
suite `catalog` incluye una prueba propia fallida de confirmación UI. No atribuir
un fallo definitivo del método: ambas ejecuciones se cortaron antes de terminar.

El protocolo fijó detener nuevas repeticiones tras timeout. Se conservaron ambas
trazas, archivos y evaluaciones. No se repitieron celdas selectivamente ni se
aumentó el límite en medio de la cohorte. R2/R3 quedaron sin iniciar. Wall-clock
614,615s incluye evaluación externa posterior. No hubo error API tipado en los
registros de corte. No se conoce si el timeout se debe al nivel de razonamiento,
al proveedor, al flujo o a otra causa.

## Preflight y diferencias con Gemini

La primera preparación comprobó que este modelo expone `apply_patch` en lugar de
`edit`; el preflight heredado falló antes de inferencia comparativa. Se adaptó para
aceptar cualquiera de las dos. En la segunda preparación, el modelo editó el archivo
pero intentó ejecutar unittest con el directorio de trabajo del laboratorio anterior;
el host lo denegó. Se precisó el directorio del preflight y se usó una tercera raíz.
Los dos preflights reales de esa raíz pasaron con `--variant max`, al igual que la
referencia con 43 pruebas originales y nueve externas. Estos intentos de preparación
no son celdas ni se incluyen en métricas comparativas. Están preservados por separado.

El timeout anterior de Gemini y los 403 del reintento siguen registrados en sus lotes.
No se mezclan modelos, tiempos ni tokens, ni se borran esos errores. Los cinco checks
focalizados Gemini previos no se repitieron con GPT y no acreditan este modelo.

## Evidencia y límites

- [Protocolo](protocolo.md), [freeze](evidencia/freeze.json).
- [Resumen por celda](evidencia/summary-audit.json), [parada](evidencia/batch-result.json).
- [Preflight](evidencia/preflight.json), [referencia](evidencia/reference-proof.json).
- [Tratamientos](evidencia/treatments.json), [contratos](evidencia/cases.json).
- [Laboratorio y trazas](laboratorio.tar.gz), [hashes](preservacion.json).
- [Incidentes de preparación](incidentes-preflight.md).

La aceptación externa es una señal acotada, no certificación de seguridad/estándares.
El análisis de cargas y orden usa trazas de herramientas, no razonamiento privado.
Tokens/cache no son factura. El host limita herramientas, no es sandbox OS.
No se instalaron ni modificaron agentes canónicos o configuraciones globales.

**Siguiente decisión:** un límite mayor requeriría un protocolo y una cohorte nueva;
no debe reescribirse ni completarse retroactivamente esta ejecución. Antes de gastar
más tiempo/inferencia conviene decidir si el nuevo presupuesto es aceptable.
