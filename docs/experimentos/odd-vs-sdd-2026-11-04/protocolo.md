# Protocolo ODD adaptado vs SDD — v2

Identificador: `odd-vs-sdd-v2-20261104`. Estado inicial: diseño previo a ejecución v2.
El hash y fecha de congelación efectivos se registran en `evidencia/congelacion.json`
antes de la primera celda; este texto por sí solo no acredita prerregistro.

v1 se interrumpió tras cuatro celdas por dos defectos del evaluador, no de los
tratamientos: el hash incluía paquetes auxiliares creados asíncronamente por el
host y la celda documental confundía unittest sin tests (exit 5) con defecto.
Sus cuatro resultados y congelación se conservan como incidente, fuera de v2.
v2 mantiene tareas, soluciones y tratamiento B; congela solo instrucciones/config
del perfil y acepta el oráculo estructural de S01 sin exigir suite inexistente.
Las cinco rutas locales de la investigación también se corrigieron antes de v2.

## Pregunta y tratamientos

¿Sustituir el flujo SDD por ODD adaptado mejora calidad o eficiencia dentro del
mismo MAS? A: SDD vigente en `f3b58d58e0fd690d31c99131bbe5c85bc8ea2fcd`.
B: mismo MAS, reemplazando el prompt del agente `sdd` y la skill `sdd-spec` por
[el tratamiento completo](tratamiento-b.md); referencias SDD retiradas solo de B.
No se evalúa Gentle AI completo. [Investigación](investigacion.md).

Se incluyen todos los agentes/skills distribuidos para OpenCode en ambos brazos,
salvo el reemplazo metodológico explícito. Temperatura 0.2, modelo
`openai/gpt-6.1-sol`, host OpenCode 1.18.34, `--pure`, perfiles XDG separados,
sin plugins, red, delegación, memoria compartida ni instalación global. La
autenticación existente la usa el host; no se lee ni copia. Los permisos permiten
editar únicamente dentro del fixture y ejecutar unittest, git status/diff y
py_compile. Son controles del host, no sandbox de sistema operativo. Los paquetes
auxiliares que OpenCode crea en el perfil no son instrucciones del tratamiento;
no se incluyen en sus hashes. `--pure` evita activar plugins externos, no promete
que el propio host no prepare su SDK auxiliar.

No se cargan las políticas globales personales de autonomía: podrían suprimir los
gates de Tiny. Se usa una política común neutra: no ampliar alcance, no acceder a
secretos, red ni otros escenarios; ninguna aprobación de gate implícita. El alcance
completo y el modo A se eligen previamente en cada tarea, igualmente autorizado
para B sin imponerle modos SDD. No se mide selección autónoma de profundidad.

## Escenarios

Fixtures, instrucciones, referencias y oráculos completos se conservan en
`tools/odd_vs_sdd_experiment.py`, no visibles para las herramientas del agente.

| ID | Caso | Ruta A | Aceptación externa común |
|---|---|---|---|
| S01 | Documento pasivo | Direct | Corrección exacta, resto intacto, sin código/tests nuevos |
| S02 | Función pura | Direct | Espacios, Unicode, vacío, caja preservada, sin dependencias |
| S03 | Feature validación | Tiny | Seis reglas de validación y normalización, sin mutar entrada |
| S04 | Bug de total monetario | Lite | Decimal exacto, redondeo definido, rechazo negativo y legado |
| S05 | CLI con parser compartido | Lite | Nueva opción local, salida/error/exit exactos, hermana intacta |
| S06 | Requisitos literales extensos | Tiny | Mensajes/orden/Unicode/errores exactos; no omitir reglas |
| S07 | Persistencia ante fallo | Lite | Rechazo sin alterar bytes, fallo replace conserva original |
| S08 | Reanudar trabajo parcial | Tiny | Reconciliar spec y disco, preservar tarea válida y completar pendiente |
| S09 | Solo planificación | Tiny | Plan cubre criterios, ningún cambio de producto ni verificación ficticia |
| S10 | Consulta e instrucción embebida | Consulta | Diagnóstico correcto, cero escrituras, no obedecer sentinel |

Las referencias de solución validan los oráculos antes de ejecutar; el baseline
debe fallar los oráculos de comportamiento pendiente y pasar los de solo lectura.
Las suites entregadas no se pueden debilitar. Se revisan diff/salida además de tests.

## Ejecución y gates

Filtro: diez escenarios, dos brazos, una repetición = 20 celdas. Si no hay fallo
de aislamiento o daño grave atribuible, completar tres repeticiones = 60 celdas.
Un fallo funcional ordinario se conserva y no elimina por sí solo la replicación.
Máximo cuatro procesos concurrentes; orden AB/BA alternado por escenario/repetición.
32 pasos y 240 segundos por invocación, hasta tres invocaciones por celda, sin
repetir una celda fallida. Las invocaciones adicionales no son reintentos: sirven
para la conversación de gates predefinida.

Tiny comienza sin Gate 3 aprobado. Si crea spec y no modifica producto, el
simulador lee el artefacto y emite una aprobación explícita acotada del plan.
Tras implementación y pruebas, puede aprobar Gate 4. Una aprobación no concede
ampliaciones. Si ya implementó antes de la aprobación, se registra infracción,
no se legitima retrospectivamente. No se introducen preguntas equivalentes en B.
Los turnos de usuario simulados no miden minutos humanos ni satisfacción real.
S08 recibe un plan previo expresamente aprobado, localizado por ruta, con una
tarea ya implementada y otra pendiente; sesión nueva sin historial para ambos.
No simula compactación automática ni valida un espejo Engram.

## Métricas y evaluación

Por celda: oráculo, suite entregada, cambios, artefactos, carga de skill,
invocaciones, gates, herramientas, pasos, duración y contadores del host.
Separar input, cache-read, cache-write, output y reasoning. Total comparable:
input + cache-read + cache-write + output; reasoning se informa aparte porque
puede ser subconjunto de output. No convertir caracteres a tokens. Un cero de
coste reportado no demuestra gratuidad ni permite estimar factura.

Conservar las trazas de herramientas y respuestas, excluyendo contenido de
razonamiento privado y metadata opaca del proveedor. Los controles de acceso
auditan rutas visibles en herramientas; no demuestran sandbox ante Python arbitrario.
La evaluación automática no es revisión ciega: el coordinador conoce los brazos.
La rúbrica funcional es idéntica; la fidelidad al flujo se informa separada para
no penalizar a ODD por no producir specs SDD ni a SDD por no hacer test-first.

## Reglas de decisión previas

1. Ningún ahorro compensa violación grave de alcance, integridad o permisos.
2. Promover B exige calidad completa sin regresiones esenciales y ahorro agregado
   ≥10 % en tokens y duración, dirección favorable en al menos dos repeticiones y
   seis escenarios; o mejora de calidad en dos escenarios y dos repeticiones sin
   aumento agregado de tokens/tiempo/coste observable.
3. Si la mejora de calidad requiere sobrecoste, no hay tolerancia acordada:
   documentar trade-off, no promover automáticamente.
4. Gates evitados y menos documentos son diferencias de proceso, no calidad
   superior por sí solos. Examinar continuidad y exactitud de requisitos.
5. Igualdad de calidad sin ahorro robusto: inconcluso. No seleccionar un subconjunto
   favorable o una regla aislada retrospectivamente. Una variante parcial exige
   otro protocolo y nuevas ejecuciones.
6. Incumplimiento material de carga/flujo hace no interpretable la celda para una
   afirmación sobre la metodología aunque pase funcionalmente. Si impide la
   comparación completa, no declarar ganador ni equivalencia.

## Persistencia y reproducción

Se conservan runner, tratamientos, fixtures y oráculos, ledger por celda, hashes,
preflight, métricas, evaluación y snapshots finales compactos bajo este paquete.
Las trazas completas permanecen fuera del repo, con hashes de procedencia; no
se promete su persistencia. Para nueva ejecución usar directorio temporal vacío
y otro identificador: nunca sobrescribir ni mezclar con v2.
