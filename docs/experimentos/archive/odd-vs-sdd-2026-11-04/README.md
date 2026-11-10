# Experimento ODD vs SDD — evidencia y decisión

Fecha: **2026-11-04**. Identificador: `odd-vs-sdd-v2-20261104`.

**Decisión al archivar: conservar Developer y SDD vigentes; no integrar ni activar
ODD como efecto de este registro.** La evidencia justifica planificar un agente
ODD experimental opt-in, no sustituir SDD ni certificar superioridad universal.
La planificación solicitada es un entregable separado; no acredita implementación.

Hay una señal favorable de eficiencia para B. Un suplemento posterior completó
los escenarios afectados por cuota,
pero no sustituye la tercera repetición prerregistrada. Las dos repeticiones
completas muestran calidad equivalente en la rúbrica, **72,34 % menos tokens
observados** y **46,23 % menos duración agregada**. No sustituyen el protocolo
completo de tres repeticiones ni prueban superioridad universal.

La exploración Gemini se conserva como antecedente **no válido para inferir
ahorro metodológico**; sus porcentajes anteriores quedan rectificados en
[la nota de Gemini](gemini-flash.md).

## Pregunta

¿Mejora nuestro MAS al sustituir su flujo SDD por una adaptación de Organic Driven
Development de Gentle AI, manteniendo el modelo, host y resto del MAS?

Alcance elegido por el usuario: comparar las metodologías dentro del mismo MAS.
La comparación incluye Direct, Tiny y Lite del SDD vigente. No utiliza Standard
legacy como representante del MAS ni atribuye benchmarks de Gentle Shell a este kit.

A: MAS del baseline `f3b58d58e0fd690d31c99131bbe5c85bc8ea2fcd`.
B: mismo MAS, sustituyendo experimentalmente agente y skill SDD por
[ODD adaptado](tratamiento-b.md). Fuente externa estudiada: Gentle AI, commit
`3ea08cdfbdce671053c82377a4365915799abe57`. No se instalaron Engram ni RDD;
no se evaluó Gentle AI completo. El nombre `sdd-spec` de B era una interfaz de
laboratorio, no el nombre propuesto para la futura skill ODD.

## Resultado y cobertura

Se registraron **60 intentos únicos**: diez escenarios × dos brazos × tres
repeticiones. Hubo 56 celdas sin error de proceso, dos con artefactos funcionales
válidos pero cierre interrumpido y dos sin respuesta final. El proveedor devolvió
HTTP 429, `The usage limit has been reached`, en cuatro celdas de la repetición 3.
No se repitieron celdas ni se cambió de modelo para completar resultados.
Posteriormente, con autorización del usuario, se ejecutó un [suplemento separado](suplemento.md)
con ambos brazos para los tres escenarios afectados: **6/6 celdas correctas**.

Solo las repeticiones **1 y 2**, completas y anteriores al incidente de cuota,
aportan el siguiente resumen comparable y descriptivo:

| Métrica, 20 celdas por brazo | A: SDD | B: ODD adaptado |
|---|---:|---:|
| Aceptación funcional | 20/20 | 20/20 |
| Tokens: input + caché + output | 6.913.129 | 1.912.409 |
| Duración agregada de celdas | 2.294,312 s | 1.233,553 s |
| Llamadas a herramientas | 423 | 241 |
| Pasos con métricas | 316 | 216 |
| Respuestas simuladas de usuario para gates | 10 | 0 |

La duración suma celdas concurrentes; no es tiempo de reloj del lote. Los tokens
incluyen lectura de caché; reasoning se informa aparte. No se conoce el coste
monetario real. Las respuestas simuladas no miden tiempo humano.

En estas dos repeticiones, B usó menos tokens y duración en los diez escenarios
agregados. No se observó mejora de calidad: ambos alcanzaron el máximo de una
rúbrica sintética acotada. B también tiene instrucciones mucho más compactas;
no se separó el efecto de longitud del de las reglas metodológicas.

## Decisión

La regla previa exige comparación completa e interpretable. La repetición 3
incompleta impide promover B; no se eliminan datos parciales para forzar aceptación.
**Conservar SDD por ahora no es un rechazo técnico de ODD.**

La señal justifica una confirmación con elección natural de
profundidad SDD. Aquí los modos de A se eligieron previamente: incluso S03 recibió
recomendación Direct del agente, pero respetó la elección explícita Tiny. Este
ahorro no estima el de reemplazar automáticamente el SDD habitual de todos los
usuarios. Una confirmación requiere otro protocolo y nuevas ejecuciones, sin
sobrescribir v2 ni rescatar selectivamente una regla favorable.

## Evidencia conservada

Como en el registro de Ponytail, las tres entradas principales son este informe,
[el protocolo](protocolo.md) y [los resultados](resultados.md). Se conservan
además los anexos y JSON ya existentes para no perder trazabilidad ni borrar
incidentes. Este paquete es un registro histórico, no una instrucción activa.

- [Investigación y fuentes versionadas](investigacion.md).
- [Protocolo congelado](protocolo.md).
- [Tratamiento B completo y límites de adaptación](tratamiento-b.md).
- [Resultados detallados, controles e incidentes](resultados.md).
- [Suplemento de confirmación posterior](suplemento.md).
- [Exploración Gemini y rectificación metodológica](gemini-flash.md).
- [Reproducción y formato de evidencia](reproduccion.md).
- [Ledger de las sesenta celdas](evidencia/celdas.json).
- [Métricas y cobertura](evidencia/metricas.json).
- [Auditoría y repeticiones completas](evidencia/auditoria.json).
- [Congelación de 103 entradas](evidencia/congelacion.json).
- [Incidente v1, excluido de v2](evidencia/incidente-v1.json).
- [Runner, fixtures y oráculos](../../../../tools/odd_vs_sdd_experiment.py).
- [Auditor y exportador](../../../../tools/odd_vs_sdd_audit.py).

Las configuraciones experimentales se ejecutan en procesos y directorios
temporales externos. La entrega documental no activa B en el MAS habitual.

## Estado al cerrar el registro

No se modifican agentes, skills, permisos, instaladores ni distribución del MAS
por archivar este experimento. El manifiesto vigente sigue declarando cinco
agentes y once skills en seis plataformas. No se hicieron commits ni se limpiaron
los cambios documentales previos del usuario; el árbol local no está limpio.

Los JSON conservan salidas, contadores, snapshots y hashes, pero las trazas
completas siguen en ubicaciones temporales externas cuya permanencia no está
garantizada. Los hashes no sustituyen un contenido perdido. El runner actual
también sufrió una modificación posterior a la congelación, documentada en
[reproducción](reproduccion.md#advertencia-sobre-el-runner-actual); no se afirma
reproducibilidad byte a byte desde los scripts actuales.

## Conservación posterior para otra sesión

Las 60 trazas GPT saneadas y las seis del suplemento se copiaron posteriormente,
con hashes contrastados, a [ZIP del paquete de continuidad](../continuidad-2026-11-04/README.md).
No se cambian ledgers, fallos ni congelaciones. También se preservó el resumen
Gemini exploratorio como **no validado**; no se recuperaron intentos sobrescritos.
El contexto al día y la decisión de producto pendiente están en
[índice de experimentos](../../README.md).
