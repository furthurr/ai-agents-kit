# Developer actual vs compacto — prueba con Gemini

**Estado: terminado. Decisión: no adoptar el candidato v1; mantener Developer
actual.** Se comparó Developer vigente (A), una variante
compacta de su agente (B) y ODD experimental como referencia (C), con
`google/antigravity-gemini-3.8-flash`.

La única diferencia pretendida entre A/B es el cuerpo del agente: **6.734 vs
1.764 bytes**. La skill Developer y sus referencias son **idénticas byte a byte**.
Se conservan permisos y configuración normalizados, identificadores públicos y
prompts funcionales. Es una ablación del prompt, no una conversión de Developer
a ODD ni una edición del agente instalado.

Las 90 celdas pasaron los criterios funcionales, pero B registró **6,84 % más
tokens** y **16,39 % más duración agregada** que A. No cumplió el umbral previo
de ahorro y no ganó en tokens totales en ninguna de las tres repeticiones.
Un cuerpo más corto no garantizó menos contexto acumulado ni menos pasos.

| Métrica, 30 celdas por brazo | A: actual | B: compacto | C: ODD referencia |
|---|---:|---:|---:|
| Aceptación funcional | 30/30 | 30/30 | 30/30 |
| Tokens comparables observados | 4.086.432 | 4.365.908 | 3.050.838 |
| Duración sumada de celdas | 1.227,730 s | 1.428,999 s | 1.057,195 s |
| Pasos con métricas | 377 | 406 | 334 |
| Herramientas | 372 | 393 | 345 |

El tiempo suma celdas concurrentes, no wall-clock del lote ni espera humana.
Tokens = input + cache-read/write + output; reasoning se informa aparte. Coste
monetario real desconocido. C es referencia de método diferente, no control puro
de longitud, y no se mezcla esta cohorte con la del experimento anterior.

## Diseño

Diez tareas × tres perfiles × tres repeticiones = 90 celdas ejecutadas.
La hipótesis es ahorrar tokens sin perder controles ni calidad, manteniendo una
duración comparable. El candidato está congelado antes de las tareas; no se ajusta
para corregir un escenario observado. A/B se evalúan en una cohorte nueva y no se
mezclan con los números del ensayo anterior.

No hubo errores API, timeouts, métricas ausentes ni reejecuciones selectivas. Las
181 entradas permanecieron intactas. B ahorró tokens en seis escenarios agregados,
pero los costes de otros casos superaron esos ahorros. Se conservaron los casos
desfavorables: no se usa una mediana favorable para sustituir la decisión sobre
consumo total.

En fidelidad hay una alerta adicional: B ejecutó py_compile en las tres tareas de
solo planificación, frente a una en A. No cambió fuentes, pero genera bytecode;
pasar los tests no certifica que PLAN permaneciera estrictamente sin efectos.
El registro distingue aceptación funcional y checks mecánicos de la revisión
semántica completa del contrato.

Los tres preflights reales pasaron: agente resuelto, skill por contenido, lectura,
edición y unittest. Las siete pruebas offline de equivalencia pasaron; entre ellas
se comparan árboles de skills, configuración, prompts de tareas y estado sembrado.
Se congelaron 181 entradas antes del filtro. Los timestamps de evidencia están
en UTC y pueden ser 2026-11-05 aunque el identificador de sesión sea 20261104.

## Fuentes y herramientas

- [Protocolo y reglas previas](protocolo.md).
- [Candidato y trazabilidad de responsabilidades](candidato.md).
- [Tratamientos](tratamientos.md).
- [Adaptador de ejecución](../../../tools/developer_compact_benchmark.py).
- [Pruebas offline](../../../tools/test_developer_compact_benchmark.py).
- [Analizador](../../../tools/developer_compact_report.py).
- [Resultados detallados y explicación](resultados.md).
- [Reproducción](reproduccion.md).
- [Ledger de 90 celdas](evidencia/records.json), [métricas](evidencia/summary.json)
  y [auditoría](evidencia/audit.json).
- [Equivalencia A/B](evidencia/equivalence.json), [congelación](evidencia/freeze.json),
  [perfiles](evidencia/profiles.json) y [procedencia](evidencia/provenance.json).

No se modifica `canonical/`, `adapters/`, `generated/` ni el perfil personal. El
host gestiona su autenticación habitual sin lectura/copia de credenciales por el
evaluador. Un buen resultado solo podrá recomendar una integración posterior;
no autoriza instalación, cambio de defaults, commits o publicación.

## Qué aprendimos

La hipótesis de recuperar ahorro simplemente eliminando repetición **no quedó
confirmada para esta variante**. La skill idéntica no produjo la misma secuencia
de acciones: B realizó más pasos, más llamadas y más actualizaciones de tareas.
La compactación puede modificar atención y estrategia además del tamaño inicial.
No se concluye que toda compactación sea perjudicial ni que todo el ahorro ODD
procediera de un prompt menor. Cualquier v2 requiere otro protocolo: no se retoca
este candidato después de observar resultados para declararlo aprobado.

## Conservación posterior para otra sesión

Las 90 trazas sanitizadas se copiaron con sus hashes a
[un ZIP del paquete de continuidad](../continuidad-2026-11-04/README.md), sin
alterar los datos o retocar el candidato congelado. El paquete incluye también
las herramientas actuales y el plan ODD, identificado como propuesta histórica.
[CONTINUAR-AQUI.md](../CONTINUAR-AQUI.md) conserva la discusión posterior y las
opciones todavía no aprobadas por el usuario.
