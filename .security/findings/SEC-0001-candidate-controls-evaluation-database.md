# SEC-0001: El candidato puede modificar la base SQLite de evaluación

- Estado: Resuelto en el alcance F07 revisado
- Severidad: 🟠 Alta
- Referencia: OWASP ASVS 5.0.0 (separación de activos e integridad) · CWE-284 · CWE-693
- Ubicación: `.agent-lab/sdd-escalation/runner/src/lab_runner/storage_rpc.py:89-136`; `runner/src/lab_runner/sandbox_tools.py:366-370`
- Fecha detección: 2026-10-07

## Descripción del riesgo

El worker RPC crea/abre la base de datos evaluada en `/tmp/work/.lab-eval-f07`. El
candidato tiene `sandbox_lab_run` cuyo proceso corre dentro de `/tmp/work`; el worker
importa `feature.py` y llama sus métodos bajo el mismo usuario y namespace del
contenedor de evaluación. Por ello, una entrega puede abrir el archivo SQLite,
alterar `stock`/`holds`, o coordinar cambios para falsificar los resultados que
comprueban la suite. La evaluación de concurrencia/integridad no es independiente
del candidato.

Este diseño F07 aún no ha sido usado para una campaña real. Los checks locales
actuales solo prueban el worker/infraestructura con código confiable.

## Plan de remediación (micro-pasos)

- [ ] Paso 1: diseñar un mediador donde el almacén SQLite y el oráculo de evaluación estén fuera del namespace/escritor del candidato; exponer únicamente operaciones del contrato F07 mediante RPC acotado.
- [ ] Paso 2: añadir pruebas negativas que intenten leer/modificar DB y criterios, manipular IDs, crear symlinks y escapar rutas; cubrir carreras multiproceso y cleanup.
- [ ] Paso 3: reevaluar permisos, límites y hashes en el contenedor final; actualizar fingerprints y solicitar revisión formal de seguridad del código final.

## Bitácora

- 2026-10-07: reauditoría real de código/fuentes y evidencia Docker final documentada en `../reviews/f07-2026-10-07.md`. Acceso legítimo a DB de aplicación preservado; oráculo/control/evidencia separados, falsos estados rechazados y escritores terminados. Resolución limitada al alcance y supuestos del informe; no certificación.

- 2026-10-07: observado por inspección del código; no se han hecho llamadas F07. Revisión limitada al puente runner/evaluador actual.
- 2026-10-07: revalidación en Wave 1 de la sub-spec `aislamiento-evaluador-f07`: el acceso a la DB de aplicación es legítimo; se reprodujeron respuestas sin persistencia y un escritor posterior al retorno. Evidencia `results/f07-wave1-boundary.md` en el laboratorio. El probe de separación UID es viable, pero falta el supervisor/inspector definitivo. Hallazgo sigue pendiente; no es revisión final ni certificación.
