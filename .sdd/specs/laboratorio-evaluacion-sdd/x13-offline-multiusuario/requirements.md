# Requisitos — X13: ReserveLab offline multiusuario recuperable

- **Modo SDD:** standard
- **Tipo de trabajo:** feature; ampliación experimental del laboratorio
- **Intención:** implementar el ejercicio, calibrarlo y preparar un intento real
- **Fase:** 1 — Requirements
- **Estado:** aprobado; ejercicio aún no implementado
- **Gate 0:** aprobado por el usuario («procede» tras el preflight de Requirements)
- **Gate 1:** aprobado por el usuario («procede» tras presentación de Requirements)
- **Gate 2:** aprobado por el usuario («procede» tras presentación de Design)
- **Gate 3:** aprobado por el usuario («procede» tras presentación de Tasks)
- **Próxima fase:** implementación en curso; Verification posterior
- **Identificador:** X13, extensión independiente del catálogo F01–F10
- **Dificultad prevista:** 13 en la escala extendida original; referencia orientativa
  del nuevo máximo 10. No es dificultad observada ni transformación matemática validada.
- **Elegibilidad lite canónico:** no; migración, autorización, concurrencia e integridad

## 1. Objetivo y referencia de dificultad

Medir si un modelo puede integrar una feature de alcance transversal sobre un pequeño
proyecto legado sintético: reservar recursos offline, sincronizar con una autoridad
remota simulada, preservar aislamiento entre usuarios y actualizar datos antiguos,
incluyendo fallos, reintentos y procesos concurrentes.

La referencia 13 proviene de la estimación documental de
`cobertura-pruebas-quality-gate` en el proyecto Android consultado: amplitud de lógica,
integración y verificación sobre código existente. X13 representa ese **perfil de
impacto integral**, sin reproducir sus ~949 archivos ni su objetivo de cobertura.
No se garantiza igual esfuerzo, consumo o tasa de fallo que en ese proyecto.

| Factor | F10 del laboratorio | X13 propuesto |
|---|---|---|
| Superficie candidata | Tres métodos con scaffold correcto | Feature distribuida por componentes, con legado funcional |
| Estado | Saga y tres participantes | Reservas locales/remotas, pendientes, recibos, sesión y migración |
| Concurrencia | Lock global correcto proporcionado | Admisión, dispatch, recuperación y cambio de sesión integrados |
| Autorización | Sin multitenancy ni usuarios | Tenant, autor, permisos y revocación |
| Offline | No | Escrituras pendientes y sincronización posterior |
| Migración | No | Datos v1 → v2 con interrupciones y reinicio |
| Verificación | Seis criterios de saga | Doce familias; regresión y escenarios de interacción |

El 13 mide una hipótesis de dificultad global, no que cada algoritmo sea más difícil
que la saga F10. El comportamiento proporcionado al candidato será inventariado:
no entregar una solución integrada disfrazada de scaffold ni inflar archivos sin lógica.

## 2. Alcance y términos

- **Tenant:** espacio aislado de recursos y reservas; identificador sintético.
- **Principal:** usuario sintético perteneciente a un tenant, con rol reader, writer
  o admin. La pertenencia y el permiso vigente los determina la autoridad simulada.
- **Reserva:** solicitud de unidades de un recurso; pendiente local hasta resolución
  remota, confirmada si consume capacidad, rechazada sin consumo o cancelada terminal.
- **Comando:** intención durable de crear o cancelar una reserva, con identidad estable
  `(tenant, command_id)` y payload inmutable que incluye autor y reserva objetivo.
- **Recibo:** resultado durable de un comando, emitido por la autoridad; una respuesta
  de transporte no sustituye el efecto persistente observado.
- **Sesión:** contexto activo `(tenant, usuario, generación)`; cambia de generación en
  cada entrada, cambio de usuario o logout para distinguir respuestas tardías.
- **Reinicio:** proceso nuevo que reconstruye el estado exclusivamente desde disco.
- **Offline:** transporte indisponible; no significa que la app rechace toda captura.

Incluye creación/cancelación de reservas, consultas, persistencia local, cola de
sincronización, validación/autorización, autoridad remota simulada, proyección de
resultados, migración v1→v2 y regresiones de consultas/formato del proyecto base.
Los cambios deben cruzar dominio, almacenamiento, sincronización, sesión/autorización
y fachada de consultas; Design fijará las responsabilidades y contratos públicos.

Base: Python stdlib, pytest y SQLite, con datos sintéticos. Transporte y reloj
controlables, sin servicios de Internet, pagos reales, credenciales ni UI Android.
No requiere importar código o datos del proyecto bancario.

Fuera: disponibilidad bajo fallos infinitos, pérdida de disco, particiones permanentes,
cryptografía/autenticación real, rendimiento de producción, fairness universal,
construcción de un CRDT general o réplica completa de una app móvil.

## 3. Historias y criterios EARS

### H1 — Ejercicio independiente sobre legado verificable

Como investigador, quiero medir integración sobre una base realista y reproducible.

- **X13-R01:** EL SISTEMA DEBERÁ registrar X13 como ejercicio adicional sin sustituir
  F10 ni alterar los contratos o resultados históricos del catálogo de diez features.
- **X13-R02:** EL SISTEMA DEBERÁ proporcionar un snapshot independiente con consultas
  y comportamientos v1 funcionales, fixtures de datos antiguos y tests públicos verdes
  de esos comportamientos antes de cambios candidatos.
- **X13-R03:** EL SISTEMA DEBERÁ declarar archivos editables, APIs protegidas,
  dependencias, comportamientos v1 que se conservan y capacidades ya proporcionadas.

### H2 — Admitir operaciones offline sin prometer confirmación

Como writer, quiero capturar reservas sin conexión y conservar mis intenciones.

- **X13-R04:** CUANDO un writer/admin autorizado capture una creación o cancelación
  offline EL SISTEMA DEBERÁ guardar conjuntamente intención y estado local aplicable
  antes de informar que la captura fue aceptada localmente.
- **X13-R05:** MIENTRAS una creación no tenga resolución remota EL SISTEMA DEBERÁ
  presentarla como pendiente, sin declararla confirmada ni descontar capacidad remota.
- **X13-R06:** SI una captura es inválida o carece de autorización local ENTONCES
  EL SISTEMA DEBERÁ rechazarla sin cambiar reservas, cola ni recibos persistidos.
- **X13-R07:** CUANDO se repita la misma identidad de comando con el mismo payload
  válido EL SISTEMA DEBERÁ conservar una sola intención; SI el payload válido difiere
  ENTONCES EL SISTEMA DEBERÁ reportar conflicto sin reemplazar la intención original.

### H3 — Sincronizar con un único efecto durable

Como usuario, quiero que reintentos y fallos de red no dupliquen mis operaciones.

- **X13-R08:** CUANDO se restablezca el transporte y se ejecute la sincronización
  EL SISTEMA DEBERÁ procesar los pendientes del principal correspondiente conservando
  la identidad y el payload originales de cada comando.
- **X13-R09:** CUANDO lleguen duplicados de un comando a la autoridad EL SISTEMA
  DEBERÁ devolver su recibo durable original sin repetir el efecto; un payload distinto
  bajo la misma identidad deberá producir conflicto sin modificar el efecto previo.
- **X13-R10:** SI el efecto remoto se confirma pero su respuesta se pierde ENTONCES
  EL SISTEMA DEBERÁ mantener el pendiente recuperable hasta obtener el mismo recibo,
  sin inventar éxito ni marcarlo entregado antes del efecto.
- **X13-R11:** SI falla la persistencia de un acuse local ENTONCES EL SISTEMA DEBERÁ
  permitir recuperar el resultado remoto sin duplicar efectos ni perder la intención.

### H4 — Conservar capacidad y terminalidad bajo concurrencia

Como responsable de recursos, quiero que dos clientes no consuman las mismas unidades.

- **X13-R12:** CUANDO varias réplicas soliciten capacidad escasa del mismo tenant
  EL SISTEMA DEBERÁ confirmar únicamente reservas factibles sin volver negativa la
  disponibilidad; cada rechazo deberá dejar cero consumo atribuible a esa solicitud.
- **X13-R13:** CUANDO una cancelación autorizada se confirme EL SISTEMA DEBERÁ liberar
  una sola vez la capacidad previamente consumida por la reserva, si la hubo.
- **X13-R14:** CUANDO una cancelación se resuelva antes de una creación retrasada
  de la misma reserva EL SISTEMA DEBERÁ conservar una marca terminal durable que
  impida que esa creación consuma recursos o reactive la reserva.
- **X13-R15:** CUANDO lleguen recibos o snapshots fuera de orden EL SISTEMA DEBERÁ
  conservar la versión autoritativa más reciente de cada reserva; un dato antiguo
  no deberá degradar la proyección ni resucitar una reserva cancelada.

### H5 — Aislamiento al cambiar de usuario

Como usuario, quiero que pendientes o respuestas de otra sesión no se mezclen con la mía.

- **X13-R16:** CUANDO se cambie de tenant/usuario o se cierre sesión EL SISTEMA
  DEBERÁ invalidar la generación anterior e impedir nuevos envíos iniciados bajo ella.
- **X13-R17:** SI una solicitud ya enviada termina después del cambio ENTONCES
  EL SISTEMA DEBERÁ atribuir su recibo únicamente al contexto original y abstenerse
  de publicarlo en la vista o caché del principal activo distinto.
- **X13-R18:** CUANDO se consulten reservas, pendientes o cachés locales EL SISTEMA
  DEBERÁ limitar los resultados al principal autorizado, incluso si otro tenant usa
  los mismos identificadores de recurso, reserva o comando.
- **X13-R19:** CUANDO un usuario vuelva a su sesión EL SISTEMA DEBERÁ recuperar sus
  pendientes originales sin ejecutarlos con la identidad de un usuario intermedio.

### H6 — Autorización vigente en la autoridad

Como responsable del sistema, quiero evitar escrituras con permisos revocados.

- **X13-R20:** EL SISTEMA DEBERÁ permitir a reader consultar únicamente reservas y
  recibos propios, a writer además crear/cancelar reservas propias, y a admin consultar
  y gestionar reservas de otros usuarios únicamente dentro de su tenant; ningún rol
  deberá obtener acceso a otro tenant por su condición administrativa.
- **X13-R21:** CUANDO un comando nuevo vaya a aplicarse en la autoridad EL SISTEMA
  DEBERÁ verificar pertenencia, permiso y propiedad vigentes conjuntamente con la
  decisión de aplicar el efecto; un comando denegado deberá tener cero efecto.
- **X13-R22:** SI se revoca un permiso tras captura offline y antes de aplicación
  remota ENTONCES EL SISTEMA DEBERÁ registrar rechazo permanente sin consumo/liberación
  de recursos ni reintento indefinido de esa intención.
- **X13-R23:** CUANDO se reintente un comando ya resuelto EL SISTEMA DEBERÁ conservar
  el recibo histórico aun si cambian después sus permisos; un principal distinto no
  autorizado no deberá poder recuperar ese recibo ni apropiarse de su identidad.

### H7 — Workers concurrentes y recuperación

Como operador, quiero reiniciar workers sin abandonar ni ejecutar incorrectamente pendientes.

- **X13-R24:** CUANDO dos procesos intenten enviar un mismo pendiente EL SISTEMA
  DEBERÁ coordinar sus reclamaciones y preservar la intención; los duplicados posibles
  de transporte deberán seguir produciendo un solo efecto remoto.
- **X13-R25:** SI un worker muere antes del envío, después del efecto remoto o antes
  del acuse local ENTONCES EL SISTEMA DEBERÁ permitir que un proceso nuevo recupere
  el pendiente y llegue a su resultado durable tras cesar los fallos.
- **X13-R26:** CUANDO un intento antiguo entregue un acuse tras una recuperación
  EL SISTEMA DEBERÁ impedir que sobrescriba la reclamación o el estado más reciente.
- **X13-R27:** MIENTRAS exista trabajo de otro usuario no activo EL SISTEMA DEBERÁ
  conservarlo sin hacerlo visible ni enviarlo bajo el principal activo.

### H8 — Migrar datos antiguos sin perder recuperación

Como usuario previo, quiero actualizar el proyecto sin perder reservas ni pendientes.

- **X13-R28:** CUANDO se abra un almacén v1 compatible EL SISTEMA DEBERÁ migrar a v2
  conservando identidades, propiedad, estados, capacidad y comandos/recibos existentes
  según el mapeo público fijado antes del intento.
- **X13-R29:** SI se interrumpe una migración ENTONCES EL SISTEMA DEBERÁ dejar un
  estado reconocible v1 o v2 que pueda abrirse y recuperarse sin intervención manual;
  no deberá anunciar v2 con conversiones incompletas.
- **X13-R30:** CUANDO se repita inicialización/migración o dos procesos la soliciten
  concurrentemente EL SISTEMA DEBERÁ obtener una sola conversión lógica sin duplicar,
  borrar ni volver a ejecutar efectos previamente confirmados.
- **X13-R31:** SI el esquema es incompatible o los datos antiguos incumplen el
  contrato de migración ENTONCES EL SISTEMA DEBERÁ reportar el error sin reparar
  silenciosamente, borrar o modificar el contenido original.

### H9 — Regresión y composición de escenarios

Como evaluador, quiero verificar interacciones, no solo funciones aisladas.

- **X13-R32:** EL SISTEMA DEBERÁ conservar las consultas, orden, validación y formatos
  del legado que el contrato declare inalterados, utilizando fixtures independientes
  de las modificaciones candidatas a tests públicos.
- **X13-R33:** CUANDO se combinen migración, offline, revocación, cambio de usuario,
  respuestas fuera de orden y reinicios EL SISTEMA DEBERÁ preservar simultáneamente
  aislamiento, capacidad, recibos estables y terminalidad.
- **X13-R34:** CUANDO termine un schedule finito y justo con servicios recuperados
  y el principal correspondiente activo EL SISTEMA DEBERÁ resolver todos sus pendientes
  dentro del límite de pasos de recuperación publicado antes del intento.

### H10 — Calibración y evidencia independiente

Como investigador, quiero confiar en el evaluador antes de usar un resultado del modelo.

- **X13-R35:** EL SISTEMA DEBERÁ fijar contrato público, snapshot, criterios externos,
  escenarios, semillas y límites antes de cualquier intento real; los escenarios
  reservados deberán permanecer fuera del acceso del candidato.
- **X13-R36:** CUANDO se calibre el evaluador EL SISTEMA DEBERÁ aceptar una referencia
  confiable y rechazar la base incompleta y mutaciones representativas de cada una
  de las doce familias; cada rechazo deberá corresponder al defecto introducido.
- **X13-R37:** CUANDO se evalúe un candidato EL SISTEMA DEBERÁ contrastar sus respuestas
  con datos durables inspeccionados independientemente y un oráculo ajeno al candidato.
- **X13-R38:** EL SISTEMA DEBERÁ ejecutar candidato e inspección de sus DB dentro del
  aislamiento Docker aprobado para X13, manteniendo oráculo/evidencia protegidos,
  y verificar limpieza al terminar; no ejecutar código ni abrir DB candidatas en host.
- **X13-R39:** EL SISTEMA DEBERÁ registrar por criterio evidencia y clasificación de
  fallos funcionales, infraestructura y presupuesto, junto con los hashes de condiciones,
  modelo/variante efectivos, pasos, tiempo, tokens disponibles y costo reportado.
- **X13-R40:** CUANDO se declare éxito funcional completo EL SISTEMA DEBERÁ exigir
  las doce familias obligatorias y todas las regresiones fijadas, separando ese resultado
  del cumplimiento SDD y de los tests autodeclarados por el candidato.

## 4. Doce familias obligatorias de aceptación

Cada familia podrá tener varios casos; 12/12 significará familias completas, no doce
asserts. Fallar un caso obligatorio impide declarar completa su familia.

| ID | Familia | Requisitos |
|---|---|---|
| X13-C01 | Base independiente, superficies y regresiones | R01–R03, R32 |
| X13-C02 | Captura offline, validación y atomicidad local | R04–R06 |
| X13-C03 | Identidades, conflictos y deduplicación durable | R07, R09 |
| X13-C04 | Entrega recuperable, respuesta perdida y acuse fallido | R08, R10–R11 |
| X13-C05 | Escasez concurrente y cancelación con liberación única | R12–R13 |
| X13-C06 | Cancelación antes de creación y proyecciones fuera de orden | R14–R15 |
| X13-C07 | Cambio de sesión, respuesta tardía y aislamiento | R16–R19, R27 |
| X13-C08 | Propiedad, roles, revocación y recibos históricos | R20–R23 |
| X13-C09 | Reclamaciones, muerte de proceso y acuses obsoletos | R24–R26 |
| X13-C10 | Migración, interrupción, repetición y rechazo intacto | R28–R31 |
| X13-C11 | Escenarios combinados y convergencia acotada | R33–R34 |
| X13-C12 | Integridad del circuito, calibración y reporte | R35–R40 |

C12 califica la validez del circuito: un fallo del harness invalida el intento,
no demuestra incapacidad del candidato. Su reporte distinguirá de forma explícita
las 11 familias de comportamiento de la validación externa del circuito.

## 5. Casos límite y decisiones funcionales

- Identificadores iguales en tenants distintos: identidades independientes.
- Mismo tenant/comando, otro autor o payload: conflicto y acceso no concedido.
- Capacidad insuficiente: rechazo remoto, nunca confirmación optimista offline.
- Cancelación de reserva todavía no creada: marca terminal; creación tardía sin efecto.
- Revocación posterior a un efecto: no deshace ese efecto; conserva el recibo original.
- Logout con petición en vuelo: puede haberse aplicado en el contexto original;
  no se promete deshacerla. El acuse solo puede afectar ese contexto.
- Migración con acuse perdido previo: recuperar el recibo, no duplicar el efecto.
- Workers sin trabajo: resultado vacío sin cambios funcionales durables.
- Transporte: entrega al menos una vez con deduplicación del efecto, no transporte
  exactamente una vez ni una transacción distribuida local/remota.
- Serialización global permitida para integridad; no se exige throughput paralelo.

## 6. Requisitos no funcionales y decisiones de Design

1. Datos exclusivamente sintéticos; dependencias y superficie de edición acotadas.
2. Faults controlables y reloj lógico inyectable; pruebas sin depender de sleeps,
   red externa o latencias reales. Incluir muerte real de proceso, no solo excepciones.
3. Contrato público de entradas, salidas, errores, estados/versiones, permisos y
   fixtures v1 completo antes de modelos, sin reglas de negocio ocultas.
4. Evaluación acotada y reproducible: mínimo dos tenants, dos réplicas y tres usuarios,
   límites de volumen, disruptions y recuperación fijados en Design y calibrados.
5. Costos ausentes son N/A; costo cliente USD0 no significa factura cero. Separar
   tiempo de generación y evaluación cuando la instrumentación lo permita.

Design definirá APIs/DTOs, versiones autoritativas, persistencia y mecanismos de
reclamación/migración; inventariará scaffold y legado, y trazará ejemplos públicos,
regresiones, PBT/metamórficos y mutaciones. No fijar presupuestos de modelos por
herencia de F10: el nuevo manifiesto requiere límites y kickoff propios.

## 7. Trazabilidad y autorización

Hereda comparabilidad/evidencia de la spec principal: R03–R12, R18–R23,
R27–R45 y R59–R60. R01 de la principal sigue describiendo exactamente F01–F10;
X13 es una extensión separada, no una campaña de trece features ni un cambio retroactivo.

Fuentes: contratos públicos F08–F10 y README del laboratorio; contexto de
`.architecture/README.md` y `.security/README.md`. Navigator solo orientó sobre el
kit: carece de baseline verificable y no indexa el ejercicio; no se declara vigente.
No se encontraron steering/AGENTS locales ni `.data/README.md`; el contrato de datos
del ejercicio quedará en Design, sin bootstrap de documentación de dominio.

Gate 0 y Gate 1 aprobados. Design, Tasks, implementación y
Verification seguirán los gates standard. Una aprobación de esta spec no sustituye
el manifiesto y kickoff de un intento real ni autoriza repeticiones automáticas.
