# Developer v2 candidato 1 — tarea Alta con Gemini

**Terminado: nueve celdas nuevas, todas con aceptación funcional.** No se sustituyó
ningún agente canónico/instalado. Identificador: `v2-high-v1-20261105`.

## Resultado principal

Mismo modelo `google/antigravity-gemini-3.8-flash`, mismo proyecto LocalLibrary
documentado y tarea Alta TASK-2 literal: reservas UI/API persistidas, idempotencia,
errores exactos y concurrencia con SQLite en disco. Tres repeticiones por brazo.

| Agregado de tres celdas | Developer actual | ODD histórico | Developer v2 |
|---|---:|---:|---:|
| Aceptación funcional externa | 3/3 | 3/3 | 3/3 |
| Suite original preservada | 3/3 | 3/3 | 3/3 |
| Tokens comparables | 4.840.915 | 4.706.960 | **3.759.510** |
| Duración sumada de conversaciones (s) | **743,413** | 869,484 | 781,535 |
| Herramientas | 122 | 138 | 121 |
| Eventos de pasos con métricas | 125 | 139 | 124 |
| Llamadas directas de lectura completadas | 44 | 48 | 47 |
| Respuestas de usuario simuladas | 0 | 0 | 0 |
| Errores de herramienta | 1 | 3 | 0 |

V2 frente a Developer: **−22,34 % tokens**, **+5,13 % tiempo**.
V2 frente a ODD: **−20,13 % tokens**, **−10,12 % tiempo**.
Las nueve celdas terminaron sin errores API ni timeouts. Los perfiles cargaron sus
skills primarias por contenido. No se detectaron accesos externos, skills ajenas ni
herramientas prohibidas en los controles implementados. Los hashes congelados siguen intactos.

El lote completo tardó **957,967 s de reloj**, incluyendo evaluación y coordinación.
La suma de conversaciones no es wall-clock ni espera humana. Preparación y preflights
se excluyen del consumo comparativo. Tokens=input+cache_read+cache_write+output;
reasoning separado en JSON. No hay ahorro monetario acreditado.

## Variabilidad, sin seleccionar éxitos

| Repetición | Developer tokens | ODD tokens | V2 tokens |
|---|---:|---:|---:|
| R1 | 1.694.167 | **1.075.478** | 1.180.383 |
| R2 | 1.207.824 | 1.447.187 | **1.037.833** |
| R3 | 1.938.924 | 2.184.295 | **1.541.294** |

V2 ahorra frente a Developer en 3/3 repeticiones y frente a ODD en 2/3. En R1 ODD
es más barato: no afirmar que V2 siempre gasta menos. El candidato alcanza el criterio
numérico fijado antes de ejecutar: ahorro agregado >=10% frente a ambos controles,
tiempo no peor en más de10% y ahorro de tokens en al menos2/3 repeticiones frente a cada uno.
Esto recomienda seguir validándolo en esta tarea, no promoverlo globalmente.

## Qué es el candidato

Fuentes del candidato, congeladas antes de las celdas:
- [Agente breve](candidato/agent.md).
- [Skill y procedimiento](candidato/SKILL.md).

Se parte del enfoque proporcional ODD, no del Developer compacto descartado. Se
eliminan formato obligatorio Specs/Tasks/Log, IDs S#/T#, cuotas heurísticas de
exploración, obligación general RED previo, línea `Risk` fija y contador de correcciones.
Se conserva intención/PLAN, alcance, desarrollo integral, verificación, consumidores,
continuidad bajo demanda, protección de datos y límites con SDD y otros agentes.
Se mantienen instrucciones de cierre documental, pero este ensayo no certifica su uso.

Agente+skill primaria runtime: Developer **13.399 bytes**, ODD **5.041**, V2 **3.224**.
Son tamaños de texto, no tokens estimados. El resto del contexto y las skills de
dominio se cargan según comportamiento. Se cambian procedimiento y longitud juntos:
no se aisló causalmente qué parte produce el ahorro.

V2 no impone `.odd/`, `.ODD/` ni otra carpeta de seguimiento. Puede mantener una nota
local si necesita continuidad; **en estas tres ejecuciones no la creó**. No se ha
probado todavía la continuidad larga de este candidato.

## Comportamiento observado

### Developer actual
- Implementó y verificó sin turnos adicionales de aprobación en las tres celdas.
- Cargó `data-api` en 3/3 y `ui-design` en 2/3.
- No creó seguimiento ni modificó documentación del proyecto.
- Ejecutó pruebas propias con resultados verdes; no se observó RED previo al primer
  cambio de producto. Su procedimiento no obliga a test-first general.

### ODD histórico
- Cargó `data-api` en 1/3; no cargó `ui-design`.
- Creó seguimiento `odd/tasks/` en 2/3; en R1 trabajó sin documento durable.
- Solo en R3 se observa RED antes del primer cambio de producto. En R1 y R2 editó
  modelos antes de observar RED: no se acredita fidelidad perfecta al test-first de ODD.
- Tuvo más herramientas, pasos registrados y correcciones en conjunto. Son
  observaciones, no prueba de que el documento o TDD sean la causa del sobrecoste.

### Developer v2
- Implementó y añadió pruebas sin pedir aprobación rutinaria, sin seguimiento y
  sin errores de herramienta registrados.
- Cargó `data-api` en 1/3; no cargó `ui-design`. La menor consulta de estándares
  coincide con parte de la reducción de contexto, pero no prueba que siempre sea adecuada.
- No se observó RED antes del primer cambio de producto. En R3 sí hubo tests rojos
  posteriores y correcciones antes de terminar verde; quitar test-first obligatorio
  no significó quitar las pruebas.
- Sus 47 lecturas superan las44 de Developer: no explicar el ahorro como «simplemente
  leyó menos». Se observaron diferencias en contenido cargado y secuencia de ejecución.

Las consultas de skills son un límite importante: **no se acreditó igual aplicación
de todos los estándares del MAS**. La aceptación UI del oráculo no es auditoría visual,
de accesibilidad o seguridad. No transformar menor consumo en equivalencia integral.
Tampoco se debe llamar «incumplimiento» a cada skill no cargada sin revisar pertinencia.

Ningún brazo leyó directamente README o `docs/lab-context.md` ni actualizó esos
documentos; tampoco propuso el cierre documental en su texto final. Las notas ODD
no son documentación canónica del proyecto. La documentación estaba disponible,
pero no había un enlace nuevo que forzara su consulta ni una fase posterior de actualización.

## Verificación y límites metodológicos

Se reutilizaron sin modificar el baseline, la tarea y los nueve oráculos del ensayo
[LocalLibrary anterior](../real-project-gemini-2026-11-05/README.md). No se reutilizaron
sus resultados como controles: las tres variantes se ejecutaron nuevamente en esta cohorte.
Cada evaluación restauró los43 tests originales en una copia independiente. Se validó
antes la referencia contra original43+externos9 y se ejecutaron tres preflights reales.

El arnés nuevo importa una instancia privada del runner anterior y cambia explícitamente
nombres, raíz, modelo de brazos y entradas del nuevo experimento. No modifica el
archivo histórico ni carga el agente SDD. Los cuerpos Developer/ODD y las skills de
dominio se verificaron por igualdad de contenido tras sustituciones de identificadores.
No se añade a V2 información específica de reservas, SQLite ni tests ocultos.

El presupuesto fue idéntico, configurado60 pasos, 600s y máximo6 invocaciones por celda.
Cada celda usó una sola invocación. **ODD R3 expuso63 eventos `step_finish`** pese a
`steps:60` configurado: no se acredita que el contador SDK sea un hard cap equivalente
al límite del host. Se conserva completo, sin truncar ni reintentar. No se supera el
timeout. Todos recibieron la misma configuración de límites.

Los detectores RED son evidencia de orden de herramientas, no certificación semántica
de que cada RED reproduzca exactamente el comportamiento faltante. La fidelidad al
flujo se distingue de pasar los tests. Permisos del host no son un sandbox OS ni un
bloqueo de red universal para código Python generado. Caché/proveedor no herméticos;
rotación del orden no aleatoriza la finalización. n=3 y una sola tarea no prueban significancia.

**Conclusión:** hay evidencia favorable a Developer v2 en calidad funcional y consumo
para esta tarea Alta. Es compatible con la hipótesis del usuario de simplificar ODD
y gastar menos, pero no garantiza el resultado en todas las tareas ni demuestra por
sí solo igualdad de integración, PLAN, continuidad, documentación o seguridad.
No se sustituye Developer, no se instala V2 y no se retoca el candidato para reinterpretarlo.

## Evidencia y reproducción

- [Protocolo prerregistrado](protocolo.md), [copia congelada](evidencia/protocol.md).
- [Métricas y comportamiento por celda](evidencia/summary-audit.json).
- [Congelación](evidencia/freeze.json), [preflights](evidencia/preflight.json).
- [Contratos exactos](evidencia/cases.json), [tamaños/tratamientos](evidencia/treatments.json).
- [Referencia revalidada en esta cohorte](evidencia/reference-proof.json).
- [Registro del lote](evidencia/batch-result.json), [dependencias](evidencia/dependencies.lock.txt).
- [Verificaciones y límites de cierre](verificaciones.json).
- [Laboratorio y trazas saneadas](laboratorio.tar.gz), [manifest de hashes](preservacion.json).

Código nuevo: `tools/developer_v2_high_benchmark.py`, `tools/developer_v2_high_report.py`
y sus tests. Preparación/pruebas no alteraron `canonical/`, `generated/`, adaptadores
ni configuración global. No hay commits/push. Se conservan los cambios locales anteriores.

El archivo incluye candidato resuelto en perfiles, baseline, oráculos, referencia,
árboles finales y trazas. `dependencies/` preserva runner/freeze históricos y helpers
de análisis/transporte usados, sin leer/copiar credenciales. No incluye venv, Git ni
bases SQLite. La reproducción requiere revisar rutas absolutas `REPO`/`SOURCE`, instalar
dependencias y regenerar estáticos. Para inferencia nueva usar otra raíz, adaptar rutas
y congelar de nuevo; no sobrescribir celdas ni afirmar reproducción exacta del proveedor.
