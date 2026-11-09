# Protocolo — compactación de Developer

Identificador: `developer-compact-v1-20261104`. La fecha de la sesión es 2026-11-04;
los timestamps de ejecución/congelación se registran en UTC y pueden ser 2026-11-05.
Modelo fijo: `google/antigravity-gemini-3.8-flash`, integración Antigravity del host
OpenCode existente. No se modifica el agente instalado ni se activa un reemplazo.

## Hipótesis y brazos

¿Reducir la repetición del prompt de Developer, manteniendo su skill, disminuye
tokens sin perder calidad, autorizaciones, pruebas ni cierre documental?

| ID opaco | Tratamiento | Intervención |
|---|---|---|
| A | Developer actual | Agente completo y skill Developer actuales. |
| B | Developer compacto | [Cuerpo compacto](candidato.md); misma skill y referencias que A, byte a byte. |
| C | ODD experimental de referencia | Tratamiento B histórico, sin cambios de método. |

A/B usan el mismo identificador de agente y de skill, cada uno en su proceso y
perfil independiente. La ruta opaca A/B difiere, no el texto de sus skills ni el
prompt funcional de la tarea. Solo se configura un directorio de skills por
proceso. No se informa al modelo que un brazo es «compacto» o debe gastar menos.
Se comprueba por preflight el prompt resuelto y el cuerpo íntegro de skill.

El namespace evita homónimos globales. Los nombres de las skills de dominio se
adaptan mecánicamente; no se renombran agentes colaboradores como si fueran skills.
Se verifica que los árboles de skills A/B sean idénticos y que el agente B sea
más corto. La longitud se informa como bytes/palabras, no se convierte a tokens.

C conserva `odd/tasks/` del tratamiento ensayado, no las decisiones `.odd/` o
integración de producto posteriores. No se cambia ODD para favorecer al candidato.
Los números del experimento anterior no se mezclan con esta cohorte nueva.

## Harness y privacidad

Se reutilizan sin editar las funciones de ejecución/evaluación/sanitización de
`tools/gemini_three_way.py`, con un adaptador nuevo que monta A/B/C y sustituye
únicamente el orden y las identidades de laboratorio. Los hashes de ambos scripts,
fixtures, perfiles, tests y documentos del protocolo se congelan antes de celdas.

Mismo plugin y autenticación normal del host, sin leer/copiar credenciales ni
exportar configuración global. Sin `--pure`, cambio de XDG o instalación global.
Los permisos y herramientas son iguales entre A/B, normalizando las rutas de
su fixture/perfil. No se relajan durante el lote. Los controles no son sandbox OS.
Se declaran herramientas personalizadas heredadas y se audita su eventual uso.
El host/plugin y la caché no son completamente herméticos ni se reinician.

Se conservan todos los intentos, trazas sanitizadas, respuestas públicas,
contadores, snapshots, errores API y denegaciones. No se guarda razonamiento
privado ni headers/cookies/cuerpos arbitrarios de errores. No se borran raíces
ni se sobrescriben celdas para reintentar. Los intentos fallidos no desaparecen.

## Escenarios, ejecución y aprobaciones

Diez tareas S01–S10 del ensayo anterior: errata, función pura, validación,
Decimal, CLI compartida, reglas literales, persistencia, reanudación, plan y consulta
con instrucción incrustada. Mismas condiciones, fixtures y oráculos por brazo.
Validar baseline y soluciones antes del preflight. Índice Git sintético, sin
commits, para comparar cambios locales sin tocar el repositorio del usuario.

S08: A/B reciben el mismo `WORK.md` y autorización de completar T2; C su registro
equivalente. Sesiones nuevas con estado sembrado, no compactación o continuidad
de varias semanas. No se introduce ninguna selección de modo ni gates SDD.
El simulador solo aprueba un plan del mismo alcance si el flujo lo pide sin
haber cambiado producto; no aprueba una ampliación funcional ni reintenta errores.

Preflight por brazo: contenido correcto de skill, lectura/edición reales y
unittest. Filtro: 10 × 3 = 30 celdas, una repetición. Si los controles de acceso,
integración y entradas permanecen válidos, completar r2/r3: 90 celdas acumuladas.
Un fallo funcional ordinario no se elimina ni obliga a detener la réplica.
Errores API, timeouts, contaminación o acceso a otra raíz en el filtro impiden
continuar hasta registrar el límite, sin cambiar la configuración a mitad de lote.

Orden A/B/C contrabalanceado con seis permutaciones fijadas en el runner, tres
procesos concurrentes como máximo. 32 pasos y 240 s por invocación, mismas
herramientas y oportunidades de autocorrección. Hasta la aprobación acotada de
plan prevista por el harness, no se añaden conversaciones de optimización.

## Evaluación y decisión previas

1. Separar aceptación funcional, checks mecánicos, errores de herramientas y
   fidelidad semántica. Oráculos, suites finales y código original de tests se
   ejecutan externamente sobre las soluciones finales.
2. Revisión específica A/B: PLAN sin efectos mutantes, no `.sdd/`, sin delegación,
   alcance no ampliado, pruebas reales y cierre no ficticio. Distinguir omisiones
   de presentación, comandos denegados y violaciones ejecutadas. Los tests pequeños
   no acreditan todas las garantías del contrato de Developer.
3. Promover solo como **candidato recomendado para integración posterior** si B
   mantiene aceptación completa, no introduce regresiones esenciales ni un patrón
   nuevo de incumplimiento y reduce tokens totales al menos 10 % frente a A, sin
   empeorar duración agregada más de 10 %. Exigir dirección favorable de tokens
   en al menos dos repeticiones y seis escenarios; no seleccionar un subconjunto.
4. Si ahorra menos, es inconcluso respecto al umbral. Si hay regresiones de calidad,
   no las compensan tokens. Si el resultado queda parcial/no interpretable, no
   declarar equivalencia ni aprobación. No ajustar el candidato dentro de v1.
5. C solo contextualiza cuánto se aproxima B al ODD de referencia. No concluir
   que cada regla ODD es necesaria o que Developer deba adoptar su método.
6. Son descripciones n=3 por escenario, sin significancia estadística garantizada.
   Ni el éxito del candidato ni esta autorización de prueba equivalen a instalar,
   cambiar canonical/generated, hacer commits o sustituir el agente habitual.

## Métricas y límites

Input, cache-read/write y output separados; total comparable = su suma.
Reasoning separado y SDK total como contraste, sin almacenar contenido privado.
Pasos, herramientas, invocaciones, turnos simulados y duración de la conversación
CLI, excluyendo evaluación externa posterior. Las duraciones sumadas de celdas
concurrentes no son wall-clock del lote. Métrica ausente es desconocida, no cero.
Coste del host cero no acredita una factura gratuita ni ahorro monetario.

Comparar sumas de la misma cohorte y medianas por tarea, manteniendo fallos.
Efecto techo posible; escenarios pequeños Python, sin UI/API distribuida ni revisión
ciega. La compactación puede cambiar la atención del modelo además del tamaño del
contexto: no atribuir todo el resultado a bytes sin una ablación adicional.
