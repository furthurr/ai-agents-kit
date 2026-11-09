# Developer actual / ODD histórico / Developer v2 — tarea Alta

Protocolo previo a celdas: v2-high-v1-20261105. Nueva cohorte independiente.
Modelo único solicitado: `google/antigravity-gemini-3.8-flash`; host OpenCode habitual.

## Objetivo y tratamientos

Probar candidato Developer v2 basado en simplificación de ODD, sin sustituir agente
canónico/instalado. Comparar Developer actual, ODD histórico ya medido y v2-candidato1.
«ODD propuesto» se operacionaliza como el tratamiento experimental histórico, NO la
propuesta v1.1 completa, que no tiene implementación runtime validada.

Developer y ODD conservan contenido fuente con sustituciones de identificadores.
V2 usa solo agente+skill de candidato, sin cargar además Developer actual. Skills de
dominio con contenido idéntico normalizado entre brazos. Permisos/configuración
equivalentes salvo nombres, rutas e instrucciones del procedimiento. No agente SDD.

V2 elimina formato Specs/Tasks/Log, S#/T#, cuotas de exploración, RED obligatorio
cuando existe runner, fórmula Risk y contador de correcciones. Conserva intención,
alcance, desarrollo integral, verificación, continuidad bajo demanda, secretos y
cierre documental. No lleva instrucciones específicas de reservas/SQLite/oráculo.

## Escenario y aceptación

Mismo baseline LocalLibrary documentado, commit upstream
`3120b4302bf87a1b8c84d06662c2b8787f7da5f8`, fuente y documentación idénticas al ensayo
anterior. Misma tarea TASK-2 literal: reserva UI/API con idempotencia, errores exactos,
modelo Reservation y concurrencia real con SQLite en disco. Mismos nueve tests externos
y restauración de 43 tests originales en copia de evaluación. Referencia validada
antes de inferencia. No nuevos requisitos ocultos ni soluciones visibles al agente.

Tres repeticiones x tres brazos = nueve celdas NUEVAS; no reutilizar los resultados
anteriores como brazo control. En cada repetición tres procesos concurrentes máximo,
orden rotado Developer/ODD/v2, ODD/v2/Developer, v2/Developer/ODD.

Mismo presupuesto: 60 pasos/invocación, 600s/invocación, máximo6 invocaciones por celda.
El simulador solo responde aprobación de plan pedido antes de cambiar producto,
limitada al alcance original; no añade gates ni feedback oculto, no contesta decisiones
funcionales nuevas. No hay fase obligatoria de actualización documental posterior:
se observa si se propone y qué archivos cambia; no afirmar ciclo documental completo.

## Controles y reglas

Preparación y preflight real de los tres perfiles (prompt, skill por contenido,
lectura/edición y unittest) separados de métricas de tareas. Congelar candidato,
perfiles, baseline, contratos, scripts, oráculos y referencia antes de las nueve celdas.
Verificar hashes antes/después de llamadas. No ajustar candidato tras ver resultados.
Directorios e intentos exclusivos, conservar fallos, sin retries selectivos.
Fallo API/timeout/carga o error del arnés detiene nuevas repeticiones; fallos funcionales
se conservan y no impiden replicar. Oráculos no se muestran como feedback al agente.

Denegar secretos y herramientas de red/delegación; allowlist Django/tests/git lectura.
Misma autenticación habitual del host sin leer/copiar credenciales. Límites del host,
no sandbox OS: código Python escrito no tiene aislamiento universal acreditado.

## Análisis fijado

Calidad primero: nueve oráculos y >=43 tests originales, cobertura omitida/regresiones,
evidencia de pruebas reales y código entregado. Flujo y aceptación funcional separados.
Observar lecturas, herramientas, pasos, pruebas RED/GREEN, seguimiento, cierre y pausas.
No inferir calidad solo por cantidad de tests o documentos.

Tokens=input+cache_read+cache_write+output; reasoning aparte. Duración sumada no es
wall-clock ni tiempo humano; checks externos fuera del contador conversacional.
Sin métricas => desconocido. Coste host no acredita factura. Preparación aparte.

Para recomendar candidato en ESTA tarea: 3/3 correctos, sin pérdida esencial observada,
y ahorro agregado de tokens >=10% frente a ODD y Developer; tiempo con empeoramiento
<=10%, y ahorro de tokens en al menos2/3 repeticiones frente a cada control. Si no
cumple, reportar cercanía, trade-off o rechazo sin retocar umbral. No significancia
ni promoción general por una sola tarea; PLAN, continuidad larga y cierre documental
seguirán sin certificar aunque los tests de reservas pasen.
