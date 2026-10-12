# Requisitos — Condición experimental F10 sin SDD

- Modo SDD: standard
- Tipo de trabajo: feature del runner experimental
- Intención: implementar una condición alternativa; ningún lanzamiento real queda autorizado por esta spec
- Fase: Requirements
- Estado: aprobado para Design
- Gate 0: preflight técnico completado; continuación autorizada al validar alcance y elegir standard
- Gate 1: aprobado explícitamente por el usuario («sí»)
- Spec relacionada: `.sdd/specs/laboratorio-evaluacion-sdd/`
- Contrato público inmutable: `.agent-lab/sdd-escalation/catalog/contracts-f10.md`

## 1. Objetivo y alcance

Añadir al laboratorio una condición experimental alternativa para ejecutar F10 sin
instrucciones ni fases SDD. El candidato recibirá una sola tarea integral y el
contrato público de F10, implementará el ejercicio en el entorno aislado y su
primera entrega se evaluará externamente contra los seis criterios obligatorios.

La condición se limita a F10. Debe coexistir con `lite-experimental` y
`standard-autonomous`, no reemplazarlos ni alterar sus resultados. La condición
nueva registra su propia etiqueta y evidencia para que no se combine ni se
interprete como resultado de SDD.

Esta spec autoriza planificar e implementar el soporte del laboratorio. No autoriza
invocar un modelo, consumir presupuesto, iniciar una campaña ni repetir el intento
real anterior. Un lanzamiento posterior requiere preparación y kickoff explícitos
con modelo/variante y límites vigentes.

## Calificación del alcance medido por la condición

- Esfuerzo previsto del LLM: 8 🟠
- Referente: F10 con scaffold
- Justificación: se conservan los tres métodos de coordinación de saga; la dificultad
  proviene de persistencia durable, efectos en tres participantes, recuperación ante
  fallos y concurrencia, no de las fases de planificación que ahora se omiten.
- Atención: alta para aislamiento del oráculo, presupuesto y clasificación de fallos;
  los controles deben mantenerse aunque el prompt del candidato no use SDD.
- Esta calificación describe la tarea F10 que recibirá el modelo, no el esfuerzo de
  implementar el modo alternativo del runner.

## 2. Historias y criterios de aceptación EARS

### H1 — Ejecución directa, sin fases SDD

Como investigador, quiero comparar F10 con una instrucción directa para medir el
resultado sin imponer al candidato el flujo SDD.

- R1.1: CUANDO se solicite la condición `no-sdd` para F10 EL SISTEMA DEBERÁ crear una ejecución independiente desde el snapshot público base de F10, sin conversación ni artefactos de otros intentos.
- R1.2: CUANDO comience una ejecución `no-sdd` EL SISTEMA DEBERÁ entregar al candidato una sola instrucción integral para completar F10, junto con el contrato y las herramientas públicas ya permitidas, sin exigir etapas, aprobaciones, Quick Plan ni documentos SDD.
- R1.3: MIENTRAS se ejecute la condición `no-sdd` EL SISTEMA DEBERÁ permitir cambios únicamente en los puntos de implementación F10 publicados (`Saga.submit`, `Saga.step` y `Saga.get`) y mantener protegidos el contrato, el evaluador, los criterios reservados y el resto del scaffold.
- R1.4: CUANDO el candidato termine o alcance un límite EL SISTEMA DEBERÁ conservar el estado final y la primera entrega disponible; no deberá iniciar reparación ni otra ronda automáticamente.
- R1.5: SI el candidato termina sin crear documentos SDD ENTONCES EL SISTEMA DEBERÁ poder cerrar la ejecución y exportar la entrega sin clasificar la ausencia de esos documentos como fallo.

### H2 — Evaluación independiente y comparabilidad

Como evaluador, quiero usar el mismo oráculo reservado de F10 y distinguir esta
condición de las ejecuciones anteriores.

- R2.1: CUANDO exista una primera entrega congelada de F10 `no-sdd` EL SISTEMA DEBERÁ evaluarla externamente contra los seis criterios obligatorios F10-01–F10-06, sin exponer resultados, criterios reservados ni diagnósticos al candidato.
- R2.2: CUANDO registre una ejecución `no-sdd` EL SISTEMA DEBERÁ incluir su etiqueta de condición, modelo/variante efectivos, snapshot y digest del contrato, límites, telemetría disponible, entrega y evidencia por criterio bajo un identificador de run nuevo.
- R2.3: CUANDO reporte el resultado `no-sdd` EL SISTEMA DEBERÁ separarlo de `lite-experimental` y `standard-autonomous`, conservar resultados históricos y advertir que un único intento no estima confiabilidad ni superioridad general.
- R2.4: SI no puede congelarse la entrega o completarse de forma íntegra la evaluación externa ENTONCES EL SISTEMA DEBERÁ registrar el intento como incompleto o inválido con causa, no como fallo funcional ni éxito.

### H3 — Límites y protecciones inalterados

Como operador, quiero que omitir SDD no reduzca el aislamiento ni los controles
operativos del laboratorio.

- R3.1: CUANDO se prepare una ejecución real `no-sdd` EL SISTEMA DEBERÁ exigir autorización explícita, modelo y variante exactos verificados y límites operativos explícitos antes de cualquier invocación.
- R3.2: MIENTRAS se ejecute un candidato F10 EL SISTEMA DEBERÁ mantener el aislamiento del candidato, la separación del evaluador/oráculo, la limpieza de recursos propios y la exclusión de secretos del contexto y de los registros.
- R3.3: CUANDO se agote un límite o falle la infraestructura EL SISTEMA DEBERÁ detener o clasificar el run conforme a los controles existentes, preservando evidencia y sin exceder automáticamente el límite configurado.
- R3.4: EL SISTEMA DEBERÁ SEGUIR manteniendo sin cambios el contrato público F10, los seis criterios de evaluación y los resultados históricos de la ejecución `lite-experimental` previa.
- R3.5: EL SISTEMA DEBERÁ SEGUIR tratando `lite-experimental`, `standard-autonomous` y `no-sdd` como condiciones experimentales del laboratorio, no como profundidades ni aprobaciones del SDD canónico.

## 3. Exclusiones y supuestos

- La nueva condición solo soportará F10; no habilita F01–F09 ni X13.
- La evaluación conserva el oráculo F10 existente y no proporciona feedback reservado ni reparación automática.
- Se reutilizan las fronteras de aislamiento, autenticación, transporte y controles existentes, sujeto a verificación en Design; no se presupone que la documentación por sí sola pruebe su seguridad.
- El modelo y la variante se seleccionarán y confirmarán al preparar un futuro run; no se fijan en esta spec.
- Los presupuestos del intento anterior no se heredan. No se define un nuevo presupuesto hasta el kickoff correspondiente.
- El resultado se considera una condición experimental distinta y no una comparación perfectamente controlada si cambian el modelo, el scaffold, el contrato, los límites u otras condiciones registradas.

## 4. Contexto y continuidad

El runner actual acepta solo `lite-experimental` y `standard-autonomous`; para F10
ambos crean etapas de planificación antes de implementación y Verification. El run
histórico F10 (`pilot-03e56ba6-743c-4150-9db6-f9709c0ebd49`) fue `lite-experimental`
forzado, success 6/6; permanece intacto y no equivale a esta condición.

Fuentes comprobadas: `.agent-lab/sdd-escalation/README.md`,
`results/f10-first-real-pilot.md`, `catalog/contracts-f10.md`,
`runner/src/lab_runner/pilot.py` y `runner/src/lab_runner/pilot_cli.py`. La spec
principal relacionada conserva Gate 3 aprobado y una implementación parcial; esta
spec vinculada añade una condición experimental acotada sin reabrir ni sustituir
sus resultados históricos.

Gate 1 aprobado: requisitos autorizados para Design.
