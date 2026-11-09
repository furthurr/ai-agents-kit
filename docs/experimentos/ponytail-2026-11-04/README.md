# Experimento Ponytail — evidencia y decisión

**Decisión: conservar el MAS actual (A), sin incorporar la variante B ni una
regla mínima de ella.** La comparación terminó; el beneficio incremental quedó
inconcluso. No se demostró daño técnico de la propuesta ni equivalencia universal.

Fecha de ejecución: **2026-11-04**. Baseline:
`f3b58d58e0fd690d31c99131bbe5c85bc8ea2fcd`.

Este registro documental conserva los resultados del experimento. No introduce
instrucciones activas, cambios de agentes, skills, permisos ni distribución.
La decisión posterior del usuario fue descartar la integración y conservar
esta evidencia en el repositorio.

## Pregunta y variante evaluada

¿Convertir principios de Ponytail en disparadores operativos mejora el MAS ya
existente? No se instaló Ponytail ni se evaluó su producto o infraestructura.

La variante B experimental introducía:

| Regla | Intención |
|---|---|
| D1 | Evaluar reutilización semánticamente compatible, estándar y dependencias existentes; evitar flexibilidad especulativa. |
| D2 | Comprobar proporcionalmente consumidores y artefactos al cambiar contratos compartidos; declarar límites externos o dinámicos. |
| D3 | Conservar garantías y fronteras arquitectónicas al simplificar. |
| R1 | Revisar conexiones del diff sin ampliar la auditoría a defectos independientes. |
| R2 | Fundamentar hallazgos, distinguiendo defectos, riesgos condicionados y verificaciones pendientes. |
| R3 | Evaluar rendimiento y concurrencia con carga/topología conocidas, sin inventar despliegues. |

Se modificaban experimentalmente solo `canonical/skills/developer/SKILL.md`,
`canonical/agents/code-review.md` y una prueba textual en
`tools/test_context_efficiency.py`; los derivados se regeneraban oficialmente.
La comparación final usó snapshots externos A/B, sin activar B en la instalación
habitual. El parche no se integra con este registro.

## Resultado principal

Se completaron **60 celdas**: diez escenarios, dos brazos, tres repeticiones.
El filtro inicial de veinte celdas pasó. Modelo: `openai/gpt-6.1-sol`, host:
OpenCode **1.18.34**.

| Métrica | A | B |
|---|---:|---:|
| Celdas satisfactorias | 30/30 | 30/30 |
| Tokens observados, incluida caché y contador de razonamiento | 2.245.034 | 2.306.520 |
| Llamadas a herramientas | 304 | 305 |
| Pasos con `step_finish` | 208 | 213 |
| Tiempo comparable, repeticiones 2 y 3 | 868,158 s | 878,783 s |
| Coste reportado por host | 0 | 0 |

B registró **+2,74 % de tokens observados**. En las cuarenta celdas de las
repeticiones 2 y 3, sin interrupciones, registró **+1,22 % de tiempo agregado**.
Son sumas de duración de celdas concurrentes, no tiempo de reloj del lote.
El coste monetario real no es observable: el cero del host no acredita gratuidad
ni una factura. No hay conversión de caracteres a tokens o de tokens a dinero.

Las 42 implementaciones pasaron suites y oráculos externos. Las 18 inspecciones
respetaron solo lectura; no se observaron falsos positivos ni omisiones contra
la rúbrica. B no mejoró la calidad observada ni cumplió el ahorro prerregistrado.

## Interpretación y límites

- Ambos brazos alcanzaron el máximo de la rúbrica: hay efecto techo y no se
  demuestra que B nunca ayude en casos más difíciles.
- Diez escenarios sintéticos y un único modelo/host no representan todos los
  proyectos del MAS. Las otras cinco plataformas solo se comprobaron estáticamente.
- Los oráculos no son exhaustivos. La revisión de contenido con etiquetas ocultas
  tuvo ceguera limitada: el coordinador conocía el diseño y las métricas.
- La caché del proveedor no se reinició ni quedó completamente controlada.
- No se evaluaron reglas individuales. No se justifica aceptar D2 o una variante
  parcial a partir de un subconjunto favorable de B.
- La decisión práctica es no integrar instrucciones sin utilidad demostrada.
  Un fallo real y recurrente podría justificar un experimento nuevo y focalizado.

## Evidencia conservada

- [Protocolo y controles](protocolo.md): tratamientos, escenarios y reglas previas.
- [Resultados y trazabilidad](resultados.md): métricas por escenario y repetición,
  evaluación, checks, incidentes y hashes de los artefactos originales.

Este paquete es una **selección documental de evidencia**, no una copia completa
del runner ni de las sesenta trazas. No permite reproducir por sí solo las llamadas
ni reconstruir cada implementación. Los artefactos originales permanecían en una
ubicación temporal externa al incorporar este registro; su persistencia no está
garantizada. Los hashes de procedencia permiten contrastar copias recuperadas,
no sustituyen sus contenidos ni certifican independientemente los resultados.

## Estado al cerrar el experimento

Árbol Git limpio en el baseline indicado, `git diff --check` correcto, sin commits,
instalación global, Ponytail producto, cambios persistentes de permisos ni procesos
experimentales activos. Las adiciones documentales de esta carpeta son posteriores
a ese estado y no forman parte de A o B evaluados.

## Conservación posterior para otra sesión

Se recuperaron originales, evidencia y workspaces sintéticos aún disponibles en
[el paquete de continuidad](../continuidad-2026-11-04/README.md). El ZIP Ponytail
amplía la selección documental original sin cambiar la decisión ni los hashes
históricos; su inventario y verificación figuran en el manifest de preservación.
Para el contexto completo de la conversación, leer
[CONTINUAR-AQUI.md](../CONTINUAR-AQUI.md).
