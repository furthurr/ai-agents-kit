# Confirmación complementaria tras cuota — protocolo

El usuario autorizó continuar con lo mínimo necesario tras recuperar cuota. Se
repiten en una raíz nueva y por pares completos A/B los tres escenarios afectados
por errores de proveedor: S08, S09 y S10; una repetición nueva por brazo, seis
celdas. Se mantienen modelo, prompts, perfiles, fixtures, gates y oráculos v2.
Las celdas v2 y sus fallos permanecen intactos. El suplemento no reemplaza la
tercera repetición prerregistrada, no reescribe sus métricas ni convierte el
criterio original de promoción en cumplido. Es evidencia descriptiva adicional,
con la limitación de que los escenarios ya se conocen y la cuota/caché cambiaron.

Antes de las celdas se ejecutan prepare, probe y freeze con el runner v2 intacto;
se comprueban los hashes congelados y se identifican como repetición 4. Orden
AB para S08 y S10, BA para S09; máximo dos celdas en paralelo, un intento cada
una. Se conservan resultados, errores, métricas y trazas saneadas; se aplica la
auditoría posterior existente, con verificación manual de S09 y S10. Si hay un
nuevo error se informa, sin repetir ni seleccionar éxitos. La decisión final debe
distinguir evidencia v2 y suplemento y conservar las limitaciones originales.

## Resultado

Las seis celdas se ejecutaron el 2026-11-04 con el mismo modelo y host: **6/6
pasaron** y todos los procesos terminaron con código cero. La carga correcta del
tratamiento, integridad de los 103 hashes, pruebas originales, rutas de lectura y
gates pasaron la auditoría. S09 se revisó manualmente: los dos planes cubren trim,
vacíos, duplicados ordenados y TypeError sin implementar. S10 diagnosticó la
división por cero y mantuvo solo lectura en ambos brazos.

| Tres celdas por brazo | A: SDD | B: ODD adaptado |
|---|---:|---:|
| Aceptación | 3/3 | 3/3 |
| Tokens observados | 565.544 | 166.162 |
| Duración agregada | 185,772 s | 117,249 s |
| Llamadas a herramientas | 47 | 26 |

En esta confirmación pequeña, B registra **−70,62 % tokens** y **−36,89 % tiempo**.
La duración es suma de celdas concurrentes, no tiempo de reloj. No se agregan
estos valores al lote original. Persisten el efecto techo, la selección previa de
modos de A y el uso de un solo modelo/host; no hay evidencia suficiente para
afirmar que reemplazar SDD en producción conserva todas sus garantías.

Se congelaron los 103 hashes de perfiles, runner y fixtures antes de la primera
celda. Hashes SHA-256 registrados antes de ejecutar: runner suplementario
`1ea17cde5541ed68cf29f8972ba620709d1bc2acd9bc2bd14b8f005b5f9cd7da`;
texto anterior de este protocolo
`eb8bebeb3cf7568498a4a1af5c37ec9a9b72f67542ad7dd2b4a72656b46f872b`.
Este resultado se añadió después, por lo que el hash del archivo actual difiere.
Evidencia: [celdas](evidencia/suplemento/celdas.json),
[auditoría](evidencia/suplemento/auditoria.json),
[métricas](evidencia/suplemento/metricas.json) y
[congelación](evidencia/suplemento/congelacion.json). El resumen automático
`complete_repetitions_only` del auditor está vacío porque solo reconoce r1–r3;
los valores de esta tabla proceden de las seis celdas r4, no de ese campo.
