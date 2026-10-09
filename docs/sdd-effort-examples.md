# Ejemplos y procedencia de la rúbrica de esfuerzo SDD

> **Solo respaldo opcional.** Agente, skill y referencia operativa no requieren
> cargar este documento para puntuar. Conserva ejemplos explícitos y fuentes de la
> calibración; no es un scorer ni evidencia de inferencias nuevas.

La definición aplicable permanece en
[`feature-level.md`](../canonical/skills/sdd-spec/references/feature-level.md).
Estas salidas detalladas ejemplifican notas y atención; el contexto de una
feature real siempre se debe analizar por separado.

## Salidas por nota

| Nota | Primera línea |
|---|---|
| 1 | Esfuerzo previsto del LLM: 1 🟢 |
| 2 | Esfuerzo previsto del LLM: 2 🟢 |
| 3 | Esfuerzo previsto del LLM: 3 🟢 |
| 4 | Esfuerzo previsto del LLM: 4 🟢 |
| 5 | Esfuerzo previsto del LLM: 5 🟢 |
| 6 | Esfuerzo previsto del LLM: 6 🟢 |
| 7 | Esfuerzo previsto del LLM: 7 🟢 |
| 8 | Esfuerzo previsto del LLM: 8 🟠 |
| 9 | Esfuerzo previsto del LLM: 9 🟠 |
| 10 | Esfuerzo previsto del LLM: 10 🔴 |
| 10+ | Esfuerzo previsto del LLM: 10+ 🔴 |

Las notas 1–7 pueden mostrar 🟠 con complicaciones concretas; por ejemplo, 6 🟠
para reservas concurrentes controlables. Referente, 2–4 motivos y supuestos quedan
en la spec si existe, no en la presentación rutinaria. No publiques enteros mayores
de 10. La nota orienta; no prueba elegibilidad del modo.

## Casos detallados

F10-sin-scaffold y X13-ampliado son contrastes sintéticos, no ejercicios construidos
ni resultados medidos. Describen diferencias de soporte, no una conversión de los
rangos históricos del laboratorio.

| Caso | Nota | Referente | Justificación | Supuestos relevantes |
|---|---|---|---|---|
| F01 | 1 🟢 | F01 | Formato exacto y validación estricta. | Función pura, sin I/O, mutación ni regresión de otras capas. |
| F10-scaffold | 8 🟠 | F10 | Saga durable, compensación recuperable y ventanas intent/effect/ack. | Tres métodos; participantes, locks, schema y validadores correctos ya proporcionados. |
| F10-sin-scaffold | 9 🟠 | Entre F10 y X13 | Mismo comportamiento de saga, construyendo participantes, ledgers y locking. | Contraste sintético; no añade autorización, migración ni captura offline. |
| X13 | 10 🔴 | X13 | Offline/sync, autorización/aislamiento, sesión, migración y fencing combinados. | Puertos/IPC/reloj/fixtures dados; coordinación candidata pendiente; no construir el evaluador. |
| X13-ampliado | 10+ 🔴 | Superior a X13 | Añade saga y compensación externa, fallos e interacciones con sesión/permisos/migración. | Contraste sintético con ledgers/compensaciones no proporcionados. |
| F07 | 6 🟠 | F07 | Concurrencia entre procesos, escasez e integridad de reintegro único. | Lite es evaluable con mecanismo, pruebas concurrentes y recuperación acotada; si faltan garantías, standard. |

## Interacciones breves

- **1 / direct:** trim de una función pura, sin modificar espacios internos.
  Selección → cambio localizado → pruebas de límites → evidencia breve, sin spec.
- **2 / direct:** predicados locales con límites inclusivos y orden estable.
  Aclarar rango invertido → selección → pruebas → resumen, sin spec.
- **3 / direct:** calculadora pura de ejemplo, sin pagos reales ni persistencia.
  Aclarar redondeo → selección → pruebas → resumen, sin spec.
- **4 / lite:** normalizar contactos y resolver duplicados en memoria.
  Aclarar conflictos → selección → Quick Plan → implementación y verification.
- **6 / lite:** reservas con garantía definida, mecanismo adecuado y pruebas reales.
  Mostrar 6 🟠, advertir reservas simultáneas y ofrecer lite o standard.
- **10 / standard o división:** offline/sync multiusuario. Ofrecer entregas de
  consulta, edición, sincronización y conflictos solo si la separación es segura.
  Reevaluar cada entrega; si alguna sigue 10/10+, evaluar otra división o standard.

Estos ejemplos son ilustrativos, no pruebas nuevas ejecutadas. Las pruebas lite
reportadas por el usuario motivan la preferencia 4–9, no certifican todos los casos.

## Procedencia ReserveLab

Las fuentes locales se consultaron al preparar la rúbrica. La definición operativa
es autosuficiente; estas referencias detalladas no tienen que estar instaladas para
usar SDD:

- `.agent-lab/sdd-escalation/runner/src/lab_runner/catalog.py`: rangos originales y
  factores F01–F10; se conservan, no se recalculan.
- Contratos `.agent-lab/sdd-escalation/catalog/`: `contracts.md`,
  `contracts-f05-f07.md`, `contracts-f08-f09.md`, `contracts-f10.md` y
  `contracts-x13.md`, con scaffold, garantías y criterios.
- `.sdd/specs/laboratorio-evaluacion-sdd/x13-offline-multiusuario/requirements.md`
  y `design.md`: alcance de X13 y comparación con F10.
- Resultado `.agent-lab/sdd-escalation/results/x13-level13-verdict.md` y `.json`:
  Luna/MAX obtuvo **10/11 familias funcionales**, C12 válido y falló
  `admin_create` (X13-C08). Fue aceptación suplementaria acotada **post-hoc**;
  conserva `invalid_infrastructure` del intento original. C12 mide validez del
  circuito, no capacidad funcional.

X13 es un referente superior acordado por alcance transversal, no prueba superada
completamente ni frontera universal de capacidad. Su nivel histórico 13 no es
puntuación SDD ni se obtiene mediante conversión matemática.
