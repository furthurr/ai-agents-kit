# ODD con agrupación de operaciones — dos parejas GPT-6 Luna max

**Completado: cuatro conversaciones sanas, sin timeouts ni errores API. No hay una
variante eficiente aceptada.** El tratamiento redujo el agregado bruto de tokens
28,78%, pero la aceptación congelada fue1/2 por brazo y no ahorró en ambas parejas.
La ejecución barata tratada R2 falló la suite conjunta: no cuenta como victoria.

Modelo `openai/gpt-6-luna`, `--variant max`, OpenCode1.18.34; timeout1800s y60 pasos
simétricos. ID `odd-batching-luna-max-v1`. Sin mezclar cohortes/modelos ni reemplazar
fallos. No hubo preflights de inferencia ni sondeos de disponibilidad adicionales.

## Qué cambió y qué no

- Control: ODD con estándares de la cohorte GPT completa, no el original sin dominios.
- Tratamiento: el mismo cuerpo normalizado más [agrupacion.md](agrupacion.md).
- Skills data-api/ui-design completas e idénticas normalizadas:23665 bytes por brazo.
  La skill ODD pasó de6763 a7591 bytes: **828 bytes más**, no una compresión.
- TASK-2 literal, LocalLibrary documentado, permisos, referencia y oráculos idénticos;
  sin mapas nuevos, subagentes ni recuperación externa. No se cambió clasificación
  o seguimiento ODD según el brazo ni se limitaron pruebas para ganar por ahorro.
- Dos parejas nuevas concurrentes, envío control/tratamiento y tratamiento/control.
- Límite de cuatro invocaciones, sin aprobaciones simuladas adicionales. Congelación
  previa con preflight offline explícito y referencia43+9. Fuentes intactas al cierre.

## Resultados completos

Duración de invocación CLI del transport saneado; las cifras de `records` incluyen
también un pequeño overhead de procesamiento y se conservan sin reescribir.

| Celda | Tokens comparables | Segundos | Pasos | Herramientas | Suite conjunta | Oráculos / originales separados |
|---|---:|---:|---:|---:|---|---|
| Control R1 | 2200208 | 936,056 |33|52|57 OK|9 OK /43 OK|
| Agrupación R1 |2724914|1131,287|38|68|56 OK|9 OK /43 OK|
| Control R2 |3686133|1197,428|49|88|59 tests,5 errores|9 OK /43 OK|
| Agrupación R2 |1467539|798,913|28|54|57 tests,3 errores|9 OK /43 OK|

| Agregado de las dos repeticiones | Control | Agrupación |
|---|---:|---:|
| Tokens comparables |5886341|4192453|
| Segundos sumados |2133,484|1930,200|
| Pasos |82|66|
| Herramientas |140|122|
| Rondas con varias herramientas |20|24|
| Aceptación congelada |1/2|1/2|
| Ambas skills completas antes del producto |2/2|2/2|
| README leído y propuesta explícita de orquestador |2/2|2/2|

Agregado bruto: **−28,7766% tokens, −9,5283% tiempo**. Por pareja: **R1 +23,8480%**,
**R2 −60,1876%** tokens. El ahorro agregado no cumple el criterio de dirección en
ambas parejas ni aceptación completa. No seleccionar soloR2 ni solo casos verdes.
Con solo los éxitosR1, el tratamiento fue más caro, pero ese subconjunto tampoco
reemplaza el resultado del lote completo.

Consumo observable total de las cuatro conversaciones: **10078794 tokens comparables**.
Presupuesto nominal20 millones,5 millones/celda; máximo observado3686133,49 pasos y
1197,428s. Ningún límite se alcanzó; cuatro invocaciones exactas y ninguna repetida.
Wall-clock del lote2378,616s, con coordinación/evaluación. Evaluaciones externas
sumadas105,610s; referencia previa22,876s. No son tiempos humanos ni una factura.
El consumo del agente investigador/preparación fuera de esas conversaciones no está
medido por el arnés: **desconocido, no cero**. No se llamó a otros modelos desde el arnés.

## Aceptación: por qué las dos R2 fallan

Ambos agentes observaron suites verdes con sus settings locales. La evaluación
congelada ejecuta los originales restaurados más los tests añadidos usando SQLite
en disco. En ambasR2, el test de replay cierra la conexión dentro de `TestCase`:

- Control: `catalog/tests/test_reservations.py:179`, `close_old_connections()`.
- Tratamiento: `catalog/tests/test_reservations.py:181`, `connection.close()`.

La suite conjunta informa `Cannot operate on a closed database`, seguido de fallos
en otros tests. Los43 originales por separado y los nueve oráculos externos pasan
en ambas. Se mantienen las calificaciones1/2: no son un fallo demostrado del flujo
de reservas por los nueve oráculos, pero sí entregas que incumplen la suite exigida.
No corregimos sus tests ni dimos feedback al modelo para rescatarlas.

## Consultas, aplicación y cierre

Las cuatro conversaciones cargaron ODD, data-api y ui-design por contenido íntegro;
ambos dominios antes del primer producto. Todas leyeron README; tres además leyeron
`docs/lab-context.md`. Ambas fuentes permanecen sin editar. No se crearon ni
sincronizaron carpetas canónicas. Los tres archivos originales de tests son idénticos
al baseline en las cuatro soluciones.

[Auditoría focalizada](auditoria.json): contrastamos modelos/migraciones, rutas y
JSON, transacciones con conditional UPDATE y reintentos, templates, CSRF web, mensajes
visibles, consumidores y preservación de renew. Hay evidencia de aplicación real,
no solo de nombres de skills. No es certificación exhaustiva visual o de seguridad.
El fixture no tiene `.data/.design`; no se certificó declaración explícita de cada
carpeta ausente en todos los cierres. Todos detectaron README desactualizado y
nombraron `documentation-orchestrator`, sin ejecutar el ciclo documental.

Un diagnóstico HTTP complementario posterior mostró otro límite: agrupaciónR1
devuelve403 HTML, no401 JSON, ante POST anónimo cuando se activa la comprobación
CSRF real. El Client normal de las suites no lo detecta. **Es HTTP de la aplicación,
no error del proveedor.** [Corrección y ambos intentos del diagnóstico](correccion-diagnostico.md)
se conservan; el primer intento dio400 por contexto de host inválido y no se usa
para calificar producto. Ningún diagnóstico cambió las notas congeladas.

## Dónde creció o disminuyó la ejecución

| Operación observable | Control total | Agrupación total |
|---|---:|---:|
| Lecturas |38|34|
| Búsquedas/listados |11|16|
| Llamadas que incluyen escritura de producto |14|8|
| Llamadas que incluyen escritura de tests |11|4|
| Comandos que incluyen pruebas |21|16|
| Escrituras de notas ODD |7|7|
| Errores de herramienta |3|2|

Parches mixtos cuentan en producto y tests: no sumar esas columnas como herramientas
únicas. Menos llamadas no equivale por sí solo a menos trabajo. Los20→24 pasos
multiherramienta y14→8 parches con producto son señales de agrupación, no prueba de
que todas fueran independientes o de que ella causara el ahorro agregado.

- EnR1, el tratamiento tuvo **más** rondas38vs33, búsquedas9vs2 y seguimiento durable.
- EnR2, el tratamiento tuvo menos rondas28vs49 y no creó nota; el control sí.
- Cada brazo creó una nota en total, en repeticiones opuestas. En ambas parejas el
  miembro sin nota fue más barato. Es una asociación con n2, no autorización para
  prohibir seguimiento ni atribuirle toda la diferencia.
- Pasos con solo escrituras de nota contabilizan583649 tokens en tratadoR1 y548642
  en controlR2. Incluyen contexto anterior: no son estimaciones de ahorro al borrarlas.
- Cache-read agregado:5600384→3944448; representa1655936 de1693888 tokens de reducción
  bruta. Input250817→217267; output35140→30738.
  Reasoning numérico63081→62280, separado. No almacenar ni analizar texto privado.
- El output de los cierres finales solo fue400/346/352/354 tokens según celda. No
  explica el coste acumulado ni justifica recortar el cierre documental.

[Ventanas temporales](analisis-trayectorias.json) separan preproducto, escrituras y
verificación/cierre. No son una atribución causal por herramienta. Las trazas
también conservan cambios posteriores a verde, pruebas repetidas y errores denegados.

## Decisión

**No integrar, instalar ni declarar eficiente este candidato.** Falla el criterio
predefinido por aceptación incompleta y ahorro inconsistente entre parejas; además
hay un límite de contrato detectado en el caso tratado que pasó las suites congeladas.
La agrupación es observable en parte y puede ser una palanca, pero esta muestra no
separa su efecto de seguimiento, búsquedas y decisiones de pruebas/corrección.

No ejecutar otra batería por este resultado ni modificar la variante retrospectivamente.
Quedan pendientes un ODD eficiente aceptado, mayor fidelidad de pruebas y evidencia
en otros dominios/tareas. No se altera la decisión independiente de Developer candidato2.

## Verificación, evidencia y reproducción

- [Protocolo previo](protocolo.md), [tratamiento](agrupacion.md).
- `evidencia/summary-final.json`: métricas, ledger y carga mecánica; su campo de
  auditoría manual pendiente se complementa con `auditoria.json`, no se sobrescribe.
- `evidencia/freeze.json`, `offline-preflight.json`, `reference-proof.json`,
  `budget.json`, `batch-result.json`, `preparation-verifications.json`.
- `laboratorio.tar.gz` y `preservacion.json`: todas las conversaciones saneadas,
  intentos, invocaciones, snapshots, evaluaciones, diagnósticos y hashes. Sin raw
  transport/razonamiento privado, credenciales, entornos, Git, estáticos o SQLite.
- `exportacion.json`: hashes de JSON complementarios exportados.
- Scripts: `tools/odd_batching.py`, `odd_batching_report.py`, `test_odd_batching.py`,
  `export_odd_batching_evidence.py` y el diagnóstico HTTP de esta carpeta.
- 77 pruebas offline/regresión pasaron:56 `test_odd*.py` +21 de transporte/arnés
  relacionado. Referencia43+9 y43 separados pasaron antes de congelar. Preflight
  solo offline, nunca reportado como dos preflights reales de inferencia.
- Después pasaron3 pruebas del exportador:80 comprobaciones unitarias/regresión
  en total, sin sumar otra vez los runs iniciales de17/55 tests. JSON, sumas temporales,
  AST Python, contadores contra records, originales intactos y freeze verificados.

Raíz nueva: `/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/odd-batching-luna-max-v1`.
Los scripts dependen del Python venv histórico; revisar rutas/dependencias antes de
reproducir en otra máquina. Recrear otra raíz y congelación bajo nueva autorización,
no sobrescribir esta. Los permisos del host no son sandbox OS.

Sin cambios en canonical/generated/adaptadores, agentes instalados, documentación
canónica o plan del Escritorio. Sin commits/push/releases. Archivos previos preservados;
este paquete y los scripts nuevos siguen locales/untracked. Índices canónicos sin sync.
