# ODD ajustado con `.navigator` y `.architecture` — prueba exploratoria

**Terminado: una tarea Alta, una ejecución por variante, ambas funcionales. La ruta
de mapas se utilizó, pero no produjo ahorro en esta pareja: +55,77% tokens y +47,14%
duración.** No se recomienda integrar este parche como optimización general sobre
esta evidencia. Tampoco demuestra que los mapas sean inútiles en otros contextos.

Modelo solicitado `openai/gpt-6-luna`, variante CLI `max`, OpenCode1.18.34, timeout
1.800s simétrico. ID: `odd-context-routing-luna-max-v1`.

## Qué se cambió

- **Control:** ODD ajustado con estándares ya probado, NO el ODD histórico sin consultas.
- **Tratamiento:** exactamente ese mismo procedimiento más [ruta-contexto.md](ruta-contexto.md).
- Se conservaron las skills data-api/ui-design completas e idénticas normalizadas.
  No se probó un subagente, un núcleo de skills recortado ni un servicio de recuperación.
- Ambos recibieron el MISMO LocalLibrary documentado, TASK-2 literal y tres mapas
  mínimos del baseline: `.navigator/ai-context.md`, `.architecture/README.md` y
  `.architecture/flows.md`. Son [fixtures del experimento](fixtures/.navigator/ai-context.md),
  no cambios a documentación canónica del kit. No contienen soluciones de reservas
  ni pruebas ocultas; sus rutas/factos se contrastaron con código fuente.
- La referencia recibió las mismas notas. No se alteraron el comportamiento original,
  los oráculos ni requisitos para favorecer al tratamiento.

## Resultados de la única pareja

| Medida | ODD ajustado control | ODD ajustado + ruta selectiva |
|---|---:|---:|
| Conversación terminada y saludable | Sí | Sí |
| Nueve oráculos externos | 9/9 | 9/9 |
| Suite catalog restaurada + tests añadidos | Pasa | Pasa |
| Ambas skills cargadas antes de modificar | Sí | Sí |
| Tokens comparables | **1.781.135** | 2.774.390 |
| Duración conversacional (s) | **741,973** | 1.091,775 |
| Llamadas de herramientas | **60** | 63 |
| Eventos de pasos con métricas | **32** | 41 |
| Lecturas completas | 17 | **16** |
| Salida de herramientas read (bytes UTF-8) | 84.759 | **82.904** |
| Búsquedas/listados completados | **5** | 8 |
| Salida de búsquedas/listados (bytes UTF-8) | **26.431** | 27.474 |
| Contenido devuelto por skill (bytes UTF-8) | **31.344** | 32.311 |
| Mapas modificados / Markdown nuevo | 0 / 0 | 0 / 0 |

Los contadores de bytes son salida observada de herramientas, **no tokens estimados**
ni una medida completa de todo el contexto. Los tokens comparables son
input+cache_read+cache_write+output; reasoning separado (21.353 control,35.271 ruta).
No sumarlo ciegamente como si todos los proveedores contabilizaran igual. No se
calcula factura ni ahorro monetario a partir de coste host cero.

Wall-clock del lote **1.105,180s**, incluyendo coordinación/evaluación. La suma de
conversaciones no equivale a ese reloj ni al tiempo de una persona.

## Qué hizo realmente la nueva ruta

El tratamiento leyó:
1. `.navigator/ai-context.md`.
2. `.architecture/README.md`.
3. `.architecture/flows.md`.

El control tenía los mismos mapas disponibles y no los leyó. Ambos cargaron data-api
y ui-design. El tratamiento no creó ni sincronizó `.navigator`/`.architecture`, y
ningún brazo creó seguimiento Markdown nuevo.

**La localización funcionó, la optimización no quedó respaldada.** La salida de read
bajó solo1.855 bytes, pero aumentaron las búsquedas y los pasos. Sumando las salidas
observadas de read+búsquedas+skills, el volumen quedó prácticamente igual:142.534 vs
142.689 bytes. Ese subconjunto no mide todos los inputs, pero no muestra una reducción
sustancial de texto recuperado. El contenido también permanece en turnos posteriores.

No atribuir causalmente todo el aumento a las notas: variaron la secuencia de trabajo,
el razonamiento registrado y las correcciones. En su cierre, el tratamiento describió
haber corregido un bloqueo SQLite durante pruebas concurrentes. n=1 no separa estas
causas. Pasar los oráculos no acredita igual calidad visual, seguridad o mantenibilidad.

## Documentación al cierre

Ambos detectaron que el README no menciona reservas y preguntaron por actualización
manual, sin editarlo. El control nombró explícitamente `documentation-orchestrator`;
el tratamiento propuso preparar contexto para que el usuario seleccione la actualización,
pero **no nombró explícitamente al responsable**. No se ejecutó ese flujo documental.

El primer extractor automático omitió esa segunda propuesta porque reconocía
«documentación» pero no «documental». Se conservó `summary-audit.json` como salida
inicial y se corrigió SOLO el análisis, con una prueba de regresión. Usar
**`summary-final.json`** para el cierre revisado. Las trazas, entradas del modelo,
calificaciones y métricas no cambiaron. El bloque `underlying` conserva el esquema
heredado de tres repeticiones; el tamaño real de esta prueba es el nivel superior:
dos celdas, una por variante.

## Interpretación y siguiente alternativa

No se alcanzó el criterio exploratorio fijado de ahorro>=10% y tiempo no peor en
más de10%. No adoptar esta ruta como lectura inicial general por motivos de ahorro.
Los mapas pueden ser útiles cuando localizar módulos/consumidores sea difícil,
pero en este proyecto relativamente pequeño la consulta no sustituyó suficiente
exploración como para compensar los pasos/contexto adicionales observados.

Mantenerlos como fuentes bajo demanda, no como una obligación de leer todo antes
de cada cambio. Si se autoriza otra optimización, estudiar reducir de verdad el
contenido recuperado: núcleos breves de skills y referencias concretas por símbolo/
contrato. No eliminar estándares ni afirmar que un subagente será gratuito.
Esta prueba no evaluó esas alternativas y no autoriza ejecutarlas automáticamente.

Una pareja no prueba causalidad, significancia, peor rendimiento universal o que
los mapas nunca ayuden. Repetir en otros contextos requeriría otra cohorte autorizada.
No se mezclan datos con ensayos anteriores ni se retocó el parche tras ver resultados.

## Verificación y evidencia

- [Protocolo previo](protocolo.md), [copia congelada](evidencia/protocol.md).
- [Resultado FINAL revisado](evidencia/summary-final.json).
- [Configuración del ensayo](evidencia/navigation-plan.json), [tratamientos](evidencia/treatments.json).
- [Congelación](evidencia/freeze.json), [preflights](evidencia/preflight.json).
- [Referencia revalidada](evidencia/reference-proof.json), [contratos](evidencia/cases.json).
- [Registro del lote](evidencia/batch-result.json), [verificaciones](verificaciones.json).
- [Skill completa de la nueva variante](evidencia/adjusted-SKILL.md).
- [Laboratorio/trazas saneadas](laboratorio.tar.gz), [manifest y hashes](preservacion.json).

Fuentes: `tools/odd_context_routing.py`, `tools/odd_context_routing_report.py` y sus
tests. Los preflights y la referencia43+9 pasaron antes de congelar. Ambas invocaciones
pasaron dentro de1.800s, sin errores API/timeouts. No se reinició ningún modelo al
interrumpirse la espera del terminal: el lote de fondo ya terminó y se recogió intacto.

No se modificaron agentes instalados/canónicos, `.navigator`/`.architecture` del kit,
estándares de dominio ni plan del Escritorio. Sin commits/push. Las restricciones de
herramientas no son un sandbox OS. Para reproducir, revisar rutas absolutas, recrear
dependencias/estáticos y usar otra raíz/congelación, sin sobrescribir esta evidencia.
