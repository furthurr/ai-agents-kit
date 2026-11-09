# ODD experimental con estándares — ajuste aplicado y pruebas

**Estado: ajuste implementado en perfiles aislados; cinco checks focalizados pasan.
Comparación principal PARCIAL por timeout del ODD original en R2.** No instalar/promover
por este lote ni completar retrospectivamente su tercera repetición.

ID `odd-standards-v1-20261105`. Modelo solicitado único:
`google/antigravity-gemini-3.8-flash`, OpenCode1.18.34.

## 1. Cambio realizado

Se conservó íntegro el cuerpo histórico del [ODD original](../odd-vs-sdd-2026-11-04/tratamiento-b.md)
y se añadió [ajuste.md](ajuste.md). No se reescribieron los siete pasos, el test-first,
la clasificación, los registros Specs/Tasks/Log ni la fórmula de riesgo.

El ajuste exige:
- Cargar data-api o ui-design según el dominio; ambas si corresponde, ninguna si no.
  Usar el contenido y no repetir cargas mientras siga disponible.
- Localizar una entrada documental pertinente cuando no se conocen sus fuentes y
  contrastar contratos/componentes/decisiones con código, sin explorar todo por rutina.
- Verificar estándares y consumidores, sin transformar cada tarea en auditoría.
- Detectar cierre documental con independencia de las skills; señalar ruta+motivo y
  proponer documentation-orchestrator cuando corresponda, sin edición canónica o
  cambio de agente automático. Una nota ODD no sustituye documentación del proyecto.

Fuente completa runtime: [SKILL ajustada](evidencia/adjusted-SKILL.md), con namespaces
de laboratorio. Agente+skill: original5.044 bytes; ajustado7.065. Son bytes, no tokens.
El wrapper es equivalente tras sustituir identificadores; la diferencia de procedimiento
es exclusivamente el bloque añadido, verificada por pruebas offline.

No se modificaron ODD histórico, candidatos Developer, plan del Escritorio,
`canonical/`, adaptadores, `generated/`, configuración global ni agentes instalados.
No se añade ODD al catálogo y no se depreca ningún agente con este experimento.

## 2. Cinco comprobaciones focalizadas del ajustado

Una ejecución independiente por caso, no agregada a las métricas de reservas:

| Caso | Resultado observado |
|---|---|
| PLAN API/backend | Solo data-api por contenido; sin escrituras ni intentos de escribir |
| PLAN visual/CSS | Solo ui-design por contenido; sin escrituras ni intentos de escribir |
| PLAN función pura | Ninguna skill de dominio; código intacto |
| Saludo cambiado con documentación de uso obsoleta | Implementación y test correctos; identificó docs/usage.md y el literal desfasado, propuso documentation-orchestrator sin editarla |
| Test adicional sin cambio funcional/documental | Solo cambió el test; ninguna skill de dominio ni recomendación documental innecesaria |

Los cinco checks mecánicos pasaron; los cierres positivo y negativo se revisaron
también por su texto. En el caso positivo se observó RED real del saludo antes de
cambiar su implementación y GREEN posterior. Un assert externo confirmó la función;
en el negativo, función y documentación conservaron sus bytes y pasaron dos tests.

No bootstrap ni seguimiento persistente en estas fixtures pequeñas. No se ejecutó
documentation-orchestrator: se comprobó la recomendación y espera, no una actualización
documental de principio a fin.

**Límites semánticos:** el plan visual propuso padding/border-radius además del color
pedido; no se implementaron. Seleccionar la skill correcta no garantiza una propuesta
mínima. Los planes no ejecutan los comandos propuestos: se evaluó selección/solo lectura,
no la viabilidad de todo el plan. La plantilla heredada ofrece unittest incluso en
los casos Django, por lo que no debe tomarse como validación del runner recomendado
en esos planes; la tarea principal sí usa manage.py test.

## 3. Tarea Alta: qué se ejecutó y por qué se detuvo

Se planificaron seis celdas nuevas: ODD original y ajustado x tres repeticiones.
Mismo LocalLibrary documentado, TASK-2 literal, referencia revalidada, nueve oráculos
externos y restauración de los43 tests originales. No se reutilizaron resultados
históricos como controles. Modelo, permisos, herramientas y límites equivalentes.

| Intento | Conversación dentro de límite | Snapshot pasa originales+externos | Tokens observados | Conversación (s) |
|---|---|---|---:|---:|
| Original R1 | Sí | Sí | 1.320.944 | 244,967 |
| Ajustado R1 | Sí | Sí | 2.193.720 | 256,402 |
| Original R2 | **No: timeout600s** | Sí | 2.188.042* | 600,187* |
| Ajustado R2 | Sí | Sí | 2.228.204 | 229,355 |
| Original/Ajustado R3 | **No iniciados por regla de parada** | No aplicable | Desconocido | Desconocido |

*Contadores capturados hasta el corte, no coste/tiempo de una conversación terminada.*

ODD original R2 devolvió código funcional, pero no completó la conversación antes
del timeout configurado. El runner terminó su proceso (`returncode:-15`, `timeout:true`)
y evaluó los archivos preservados: la suite de57 tests (originales restaurados más
adicionales) y los9 externos pasaron. No hubo un error API tipado en la traza; la causa
del bloqueo/cierre tardío no está determinada. No atribuirlo sin evidencia a cuota,
a un bug funcional ni a una incapacidad de ODD.

Conforme al protocolo, se esperó la celda ajustada en curso y se detuvieron nuevas
repeticiones. **Cuatro intentos preservados, tres conversaciones saludables y una
interrumpida.** Ningún reintento selectivo, cambio del candidato ni aumento de timeout.

El lote parcial tardó892,449s de reloj con coordinación/evaluación. Los contadores
comparables son input+cache_read+cache_write+output, reasoning aparte. No son factura.
Los checks focalizados, preflights y preparación se informan separados.

## 4. Consultas y conducta en los dos intentos por brazo

| Observación hasta el corte | Original | Ajustado |
|---|---:|---:|
| data-api cargada por contenido | 0/2 | **2/2** |
| ui-design cargada por contenido | 0/2 | **2/2** |
| Ambas antes de primer cambio de producto | 0/2 | **2/2** |
| Cargas por skill/ejecución ajustada | No aplicable | **Una** |
| Bootstrap de .data/.design/.architecture/.navigator | 0 | **0** |
| Seguimiento odd/tasks creado | 2/2 | **0/2** |
| Errores de herramienta registrados | 2 | **0** |

Ambos snapshots ajustados pasan aceptación funcional y preservación de pruebas originales.
No se detectaron accesos externos, skills ajenas ni herramientas prohibidas en los
controles implementados. Se verificó contenido de la skill primaria en los cuatro
intentos, incluido el interrumpido. Los inputs congelados siguen intactos.

**El ajuste corrigió la selección de skills en lo observado, pero no acredita toda
la disciplina del procedimiento.** En las dos celdas ajustadas no se observa RED antes
del primer cambio de producto, aunque el test-first histórico siguió en sus instrucciones.
Los detectores de orden no certifican semántica perfecta de cada test.

### Pendiente: documentación del proyecto real

En las celdas ajustadas principales no se observaron llamadas directas de lectura a
README/`docs/lab-context.md`, cambios documentales ni propuestas de actualización al
cierre. El original solo leyó su propio registro ODD en R1. Los casos simples con una
entrada documental clara sí activaron la revisión/recomendación correcta.

Por tanto, **no declarar eliminado el riesgo acumulativo**: se verificó consulta de
estándares por skill, no descubrimiento documental fiable de un proyecto existente
ni aplicación exhaustiva de todos sus estándares. El silencio del cierre no prueba
que no hubiera documentación pertinente o desactualizada.

## 5. Qué se puede concluir sobre eficiencia

La comparación agregada permanece **sin resultado concluyente**. No usar la duración
de600s del control cortado para proclamar que el ajustado es más rápido. No sumar este
lote a otros ni reemplazar el intento por uno exitoso.

En R1, única pareja de conversaciones completas, el ajustado consumió2.193.720 frente
a1.320.944 tokens: no hay evidencia de ahorro en esa pareja. Coinciden más instrucciones
y consultas pertinentes, pero una sola pareja no aísla causas ni estima coste típico.
La variabilidad y el intento incompleto impiden una recomendación global de eficiencia.

**Conclusión:** variante implementada, selección/cierre focalizados5/5 y carga de ambos
dominios2/2 en tarea Alta, sin regresiones funcionales detectadas. Es evidencia inicial
favorable al ajuste de consultas, no una certificación del ODD completo ni razón para
cambiar la decisión pendiente de implementar el nuevo Developer.

Las terceras repeticiones no están hechas. Si se autoriza continuar, definir un lote
nuevo o suplemento separado, con sus inputs/identificador; conservar este original
como parcial. Una nueva ejecución no lo completa retroactivamente. No ejecutar más
modelos por el mero hecho de leer esta recomendación.

## Evidencia y reproducción

- [Ajuste fuente](ajuste.md), [protocolo previo](protocolo.md).
- [Skill compilada completa](evidencia/adjusted-SKILL.md).
- [Métricas y conducta](evidencia/summary-audit.json).
- [Cinco comprobaciones y respuestas completas](evidencia/consultation-summary.json).
- [Casos focalizados](evidencia/probe-cases.json), [contratos Alta](evidencia/cases.json).
- [Preflights](evidencia/preflight.json), [referencia revalidada](evidencia/reference-proof.json).
- [Congelación](evidencia/freeze.json), [tratamientos/tamaños](evidencia/treatments.json).
- [Parada del lote](evidencia/batch-result.json), [verificaciones](verificaciones.json).
- [Laboratorio y trazas saneadas](laboratorio.tar.gz), [manifest/SHA256](preservacion.json).

Código nuevo: `tools/odd_standards_benchmark.py`, `tools/odd_standards_report.py` y
sus tests. Reutilización privada del kernel y de cinco fixtures anteriores; adaptación
explícita del actor v2→adjusted y loader del namespace. Scripts anteriores intactos.

Se preservan fuentes, perfiles, baseline, referencia, oráculos, árboles finales y
trazas sin razonamiento privado, credenciales, venv, `.git`, bases SQLite ni estáticos
derivados. La reproducción exige revisar rutas/paquetes y nueva raíz/congelación para
inferencia nueva. Permisos no son sandbox OS; SQLite con hilos no certifica sistemas
distribuidos. Un proyecto tutorial/modelo y este lote parcial no prueban generalización.
No se hizo commit/push ni cambios en agentes instalados o en el plan del Escritorio.
