# Requisitos de corrección — Integridad del evaluador F07

- Modo SDD: standard
- Tipo de trabajo: bugfix de seguridad e integridad del laboratorio
- Intención: implementar tras aprobar Gates 1–3; la ejecución real F07 requiere revisión y autorización de sus límites
- Fase: 1 — Requirements
- Estado: aprobado para Design
- Gate 0: preflight ALTO presentado; usuario autorizó continuar («continúa»)
- Gate 1: aprobado explícitamente por el usuario («procede»)
- Spec principal: `.sdd/specs/laboratorio-evaluacion-sdd/`
- Hallazgos relacionados: SEC-0001, SEC-0002 en `.security/findings/`

## 1. Objetivo y alcance

Habilitar una evaluación F07 que preserve el ejercicio publicado y permita al host
decidir sus seis criterios sin confiar en resultados oficiales escritos por el
candidato. El código candidato seguirá ejecutándose fuera del proceso host.

Incluido: puente de almacenamiento, lectura independiente del estado de aplicación,
aislamiento del oráculo, rutas SQLite, carreras multiproceso, límites y errores,
calibración y revisión formal del circuito final.

Los cambios de este bugfix no autorizan llamadas al modelo ni certifican seguridad.
El waiver F01–F04 no cubre F07. Los hallazgos permanecerán pendientes hasta contar
con evidencia de remediación y reauditoría.

## 2. Distinción necesaria para preservar la medición

El contrato publicado define `StockStore(path)` y exige SQLite, conexiones por
llamada, transacciones, persistencia y recuperación. La **base de aplicación** es
estado que el candidato debe modificar legítimamente. No es el oráculo reservado.

El **estado confiable de evaluación** comprende criterios, resultados esperados,
agenda de pruebas, decisiones, registros oficiales y mecanismos de inspección del
host. La copia de evidencia utilizada para decidir un veredicto debe quedar fuera
de escritura del candidato y capturarse cuando sus procesos ya no puedan alterarla.

SEC-0001 debe revalidarse con esta distinción: compartir acceso a la base de
aplicación no demuestra por sí solo vulnerabilidad, pero confiar exclusivamente en
respuestas del candidato, compartir el oráculo o aceptar evidencia alterable sí
invalidaría la independencia. SEC-0002 requiere distinguir rutas de aplicación de
rutas confiables y comprobar sustituciones frente a la operación real de apertura.

Un mediador que implemente reservas, cancelación o atomicidad por el candidato
cambiaría el ejercicio. No se considerará remediación equivalente sin decisión
explícita y versionado de una condición nueva.

## 3. Comportamiento actual

- A01: CUANDO el prototipo evalúa F07 EL SISTEMA crea una base bajo `/tmp/work/.lab-eval-f07` e importa la entrega dentro del mismo proceso worker que prepara y serializa la respuesta RPC.
- A02: CUANDO comprueba stock durante los criterios F07 EL SISTEMA obtiene parte del estado mediante `get_stock` de la propia entrega, sin una inspección independiente congelada de las tablas que respalde el veredicto.
- A03: CUANDO el worker abre una base existente EL SISTEMA comprueba previamente la ruta mediante `lstat` y después la abre mediante `sqlite3.connect(path)`, sin impedir su sustitución entre esas operaciones.
- A04: CUANDO un candidato devuelve o emite datos al worker EL SISTEMA valida el JSON recibido, pero esa validación no acredita que el contenido describa el estado persistente real.

Fuente: `storage_rpc.py`, `criteria_f05_f07.py`, contrato F07. A01–A04 describen el
prototipo, no resultados de una ejecución real F07 ni una explotación demostrada.

## 4. Comportamiento esperado — criterios EARS

### H1 — Separación del oráculo y evidencia independiente

Como investigador, quiero que el veredicto dependa de comprobaciones externas al
candidato para medir persistencia e integridad, no solo respuestas declaradas.

- B01: MIENTRAS se ejecute una entrega F07 EL SISTEMA DEBERÁ impedirle leer o escribir criterios reservados, resultados esperados y registros oficiales de evaluación. (SEC-0001; principal R21, R44)
- B02: CUANDO decida un criterio F07 sobre stock o holds EL SISTEMA DEBERÁ contrastar las respuestas de la entrega con el estado persistente obtenido mediante un mecanismo confiable que no importe ni invoque código candidato en el host. (SEC-0001; R22, R28, R44)
- B03: CUANDO capture evidencia persistente para un veredicto EL SISTEMA DEBERÁ impedir que procesos candidatos o descendientes modifiquen la evidencia capturada después de su congelación. (SEC-0001; R42, R44)
- B04: SI una entrega devuelve un resultado correcto pero el estado persistente contradice el criterio ENTONCES EL SISTEMA DEBERÁ registrar incumplimiento funcional con evidencia de la discrepancia. (SEC-0001; R22, R27–R28)
- B05: SI no puede obtener o validar la evidencia independiente exigida ENTONCES EL SISTEMA DEBERÁ bloquear el éxito y registrar la causa de invalidez de evaluación o infraestructura. (R22, R28, R40)

### H2 — Rutas y apertura de almacenamiento

Como operador, quiero que las rutas controladas por el candidato no redirijan
lecturas o escrituras confiables fuera del almacenamiento asignado.

- B06: CUANDO seleccione un almacén F07 EL SISTEMA DEBERÁ asignarle una identidad por intento y criterio que no permita resolver rutas del host ni de otros intentos desde datos candidatos. (SEC-0002; R07, R44)
- B07: SI una ruta o archivo asociado a una operación confiable se sustituye mediante symlink, hard link o renombrado concurrente ENTONCES EL SISTEMA DEBERÁ impedir que la operación alcance un destino no autorizado. (SEC-0002; R21, R44)
- B08: CUANDO verifique la protección de rutas EL SISTEMA DEBERÁ probar sustituciones concurrentes durante la apertura real y conservar evidencia del resultado, sin considerar suficiente un `lstat` anterior a la apertura. (SEC-0002; R22, R44)
- B09: SI detecta una ruta, identidad o copia de almacenamiento fuera del conjunto autorizado ENTONCES EL SISTEMA DEBERÁ detener esa evaluación y registrar una causa fija sin incluir contenido o secretos del destino. (SEC-0002; R40, R43–R44)

### H3 — Fidelidad al ejercicio y concurrencia

Como investigador, quiero mantener el contrato que se pretende medir y evitar que
una adaptación del harness resuelva las partes difíciles en lugar del candidato.

- B10: EL SISTEMA DEBERÁ evaluar F07-01–F07-06 y las regresiones del snapshot publicado sin delegar al harness la implementación de reservas, cancelaciones, idempotencia ni atomicidad de la entrega. (R08, R20, R23, R28)
- B11: CUANDO ejecute escenarios concurrentes F07 EL SISTEMA DEBERÁ permitir solapamiento real de llamadas desde procesos distintos sobre el mismo almacén, sin una serialización del runner que garantice artificialmente el resultado correcto. (R08, R22)
- B12: CUANDO compruebe persistencia y reinicialización EL SISTEMA DEBERÁ usar nuevas instancias o procesos sobre el mismo estado de aplicación sin reemplazarlo por respuestas almacenadas del harness. (R22–R23)
- B13: SI la remediación exige cambiar API, snapshot, criterios o garantías de concurrencia publicados ENTONCES EL SISTEMA DEBERÁ bloquear la condición original hasta una decisión explícita y registrar la adaptación como una versión experimental distinta. (R08, R10, R12, R20)
- B14: CUANDO prepare F07 con `lite-experimental` EL SISTEMA DEBERÁ etiquetarla como lite forzado experimental y excluirla de conclusiones sobre elegibilidad de lite canónico. (R17–R18, R47)

### H4 — Límites, transporte y clasificación

Como operador, quiero quitar el límite de tokens sin eliminar controles operativos
ni perder el registro de consumo disponible.

- B15: CUANDO no se configure tope de tokens reportados EL SISTEMA DEBERÁ conservar el consumo expuesto como telemetría sin detener la ejecución por su cantidad. (decisión del usuario; R30–R31)
- B16: CUANDO opere sin tope de tokens EL SISTEMA DEBERÁ conservar límites explícitos de USD reportado blando, tiempo, pasos y tamaño de salida antes de invocar al modelo. (R37–R38)
- B17: CUANDO reciba una respuesta RPC F07 EL SISTEMA DEBERÁ validar estructura, tipos, identidad y tamaño antes de utilizarla para decidir un criterio. (R22, R44)
- B18: CUANDO una entrega falle por importación, comportamiento o tipo de resultado EL SISTEMA DEBERÁ distinguir ese fallo candidato de fallos de transporte o evaluación sin convertirlo automáticamente en invalidez de infraestructura. (R27, R40)
- B19: CUANDO finalice o se interrumpa una evaluación supervisada EL SISTEMA DEBERÁ limpiar solo sus procesos y contenedores propios y registrar la limpieza fallida o no verificable. (R38–R42)

### H5 — Calibración y habilitación

Como responsable del laboratorio, quiero evidencia de que el evaluador acepta una
referencia correcta y rechaza errores y manipulación antes de lanzar F07.

- B20: CUANDO calibre el circuito final F07 EL SISTEMA DEBERÁ evaluar la referencia confiable como 6/6 y el skeleton como 0/6 por comportamiento ausente, sin llamadas a modelos. (R20–R28)
- B21: CUANDO calibre el circuito final F07 EL SISTEMA DEBERÁ rechazar mutaciones de sobreventa, doble cancelación, respuesta sin persistencia y escritura de evidencia oficial, registrando criterio y causa para cada prueba. (SEC-0001; R22, R28, R44)
- B22: CUANDO presente la remediación para revisión EL SISTEMA DEBERÁ vincular fuente final, fingerprints, pruebas negativas, calibración y limitaciones a SEC-0001 y SEC-0002. (R10, R42–R45)
- B23: SI falta revisión formal válida para el alcance F07 o existen hallazgos bloqueantes pendientes ENTONCES EL SISTEMA DEBERÁ rechazar el launch F07 antes de cualquier llamada al modelo, sin aceptar el waiver F01–F04. (R21, R43–R44)
- B24: SI falta autorización explícita del intento o alguno de sus límites declarados ENTONCES EL SISTEMA DEBERÁ rechazar el launch F07 antes de cualquier llamada al modelo. (R37, R59–R60)

## 5. Comportamiento inalterado — anti-regresión

- I01: EL SISTEMA DEBERÁ SEGUIR ejecutando entregas candidatas fuera del proceso host y sin montar el repositorio, las credenciales o el socket Docker en el contenedor candidato.
- I02: EL SISTEMA DEBERÁ SEGUIR propagando los IDs de modelo y variante suministrados explícitamente por el operador y verificando sus recibos sin elegir otros.
- I03: EL SISTEMA DEBERÁ SEGUIR preservando los reportes históricos F01/F02 y registrando diferencias de condiciones sin combinar sus tasas.
- I04: EL SISTEMA DEBERÁ SEGUIR manteniendo el waiver de revisión limitado a F01–F04 sin afirmar revisión ejecutada o certificación de seguridad.
- I05: EL SISTEMA DEBERÁ SEGUIR separando `lite-experimental` y `standard-autonomous` de las profundidades y aprobaciones humanas del SDD canónico.
- I06: EL SISTEMA DEBERÁ SEGUIR manteniendo `.agent-lab/` ignorado por Git y sin modificar `.gitignore`.

## 6. Decisiones que debe resolver Design

1. Frontera de proceso/usuario/namespace para oráculo, inspección SQLite y evidencia congelada, preservando el acceso de la aplicación a su propia DB.
2. Qué observaciones de tablas y transacciones necesita cada criterio, incluidas carreras y fallos inyectados; no añadir reglas secretas al candidato.
3. Protección frente a sustitución de rutas SQLite y archivos auxiliares (`-wal`, `-shm`, journals), incluyendo inspección y transferencia de evidencia.
4. Cómo aislar la codificación de respuesta RPC del código candidato y verificar que un JSON válido no sustituya evidencia persistente.
5. Estrategia de regresión/calibración con RED reproducible: distinguir fallos de manipulación demostrados de riesgos detectados solo por inspección.

No se fija aquí una arquitectura ni se exige que la DB de aplicación sea inaccesible
al candidato: eso contradice el contrato actual. Si no puede obtenerse el aislamiento
requerido sin alterar ese contrato, B13 exige explicitar la decisión antes de seguir.

## 7. Contexto consultado y trazabilidad inicial

- Contrato público: `.agent-lab/sdd-escalation/catalog/contracts-f05-f07.md`, reglas comunes y F07-01–F07-06.
- Prototipo: `runner/src/lab_runner/storage_rpc.py`, `evaluation/criteria_f05_f07.py` y `review_gate.py`.
- Seguridad: `.security/README.md` y los hallazgos SEC-0001/SEC-0002.
- Spec principal: requisitos R07–R12, R17–R28, R30–R31, R37–R45, R47, R59–R60.
- No se encontraron `AGENTS.md`, `.sdd/steering/` ni instancia Navigator aplicable; se usaron fuentes directas.

Gate 1 aprobado: se autoriza Design. Implementación y lanzamiento F07 conservan
sus gates y autorizaciones correspondientes.
