# Resultados MAI-Code-1.1-Flash

**12 invocaciones iniciales; 2 entregas aceptadas en media-baja, 0 en alta.**

## LL-SEARCH — media-baja

| Configuración | Tokens comparables | Tiempo | Pasos | Tests nuevos | Conjunta | Aceptación |
|---|---:|---:|---:|---:|---|---|
| Candidato2 + dos refuerzos | 300.089 | 71,999 s | 19 | 4 | 60/60 | PASS |
| Developer v2 candidato2 | 442.495 | 102,347 s | 25 | 6 | 62 ejecutados; 2 fallos, 0 errores | FAIL: pruebas propias |
| Developer instalado | 447.363 | 99,510 s | 21 | 3 | 59/59 | PASS |
| Build sin MAS | 526.942 | 137,607 s | 29 | 4 | 60 ejecutados; 1 fallos, 0 errores | FAIL: pruebas propias |
| SDD instalado | 559.988 | 109,861 s | 22 | 4 | 56 ejecutados; 0 fallos, 1 errores | FAIL: fixture propia (Language duplicado) |
| Build con MAS | 1.813.691 | 235,936 s | 60 | 0 | 56 ejecutados; 8 fallos, 0 errores | Incompleto: límite de 60 pasos |

## TASK-2 — alta

| Configuración | Tokens comparables | Tiempo | Pasos | Tests nuevos | Conjunta | Aceptación |
|---|---:|---:|---:|---:|---|---|
| Developer instalado | 326.202 | 120,303 s | 20 | 0 | 52 ejecutados; 9 fallos, 0 errores | Pausa de plan + bloqueo de ruta; sin entrega |
| Candidato2 + dos refuerzos | 1.014.153 | 347,520 s | 34 | 0 | 52/52 | FAIL: 401/CSRF y sin tests nuevos |
| SDD instalado | 1.127.460 | 163,058 s | 39 | 0 | 52 ejecutados; 9 fallos, 0 errores | Bloqueado: confundió ruta del workspace |
| Developer v2 candidato2 | 1.761.607 | 284,626 s | 43 | 0 | 52/52 | FAIL: 401/CSRF y sin tests nuevos |
| Build sin MAS | 1.878.537 | 286,385 s | 53 | 0 | 52/52 | FAIL: 401/CSRF y sin tests nuevos |
| Build con MAS | 1.910.433 | 210,305 s | 60 | 0 | 52 ejecutados; 9 fallos, 0 errores | Incompleto: límite de 60 pasos |

## Interpretación y límites

- Todos conservan 43/43 originales separados y sus métodos AST. Check y consistencia de migraciones pasan.
- Media-baja: las entregas de Build sin MAS, candidato2 y SDD pasan los 13 oráculos aislados, pero fallan sus propias pruebas. Esto no equivale a un defecto funcional externo demostrado. Build con MAS deja trabajo incompleto y falla 8 de los 13 oráculos.
- SDD media-baja: 60 tests descubiertos, 56 ejecutados y un error de setUpClass por crear Language("English") duplicado. Los cuatro tests nuevos no llegaron a ejecutarse.
- Alta: Build sin MAS, candidato2 y reforzado pasan 9/9 oráculos y 52/52 conjunta, pero no conservan tests nuevos y fallan 1/5 bordes (403 en vez de 401 con CSRF real).
- Developer alta solicita aprobación del plan, sin cambios, tras intentos sobre la ruta equivocada. Es una pausa sin implementación evaluable, no una implementación de reservas fallida.
- SDD alta termina bloqueado por confundir el directorio del Python compartido con el workspace. No pidió selección SDD-Lite ni cargó sdd-spec. El estado automático `awaiting_user_gate_or_mode_review` del primer exportador era una heurística incorrecta; la revisión lo corrige sin sobrescribir esa evidencia.
- Build con MAS alcanza 60 pasos en ambas tareas; la traza contiene el cierre nativo “Maximum steps reached” aunque el recolector registra stop_reason=null. No se presenta como terminación completa.
- Fricción real: hubo lecturas/rutas/comandos denegados. Varios participantes intentaron inspeccionar el directorio de la .venv compartida, no su workspace. Los probes sí demostraron acceso permitido al workspace correcto; no se relajaron permisos ni se corrigieron trayectorias. El prompt heredado no nombra explícitamente la ruta del workspace, aunque CLI/cwd sí: es una limitación experimental.
- No se certifica fidelidad procedural completa de ningún perfil. SDD media-baja carga sdd-spec pero no deja artefactos .sdd en el workspace autorizado.
- No hubo reintentos del operador, continuación automática, reparación de participantes ni inferencias auxiliares. La pausa de Developer y el bloqueo SDD no se reanudaron.

Total observado: **12.108.960 tokens comparables**, **2169,457 s**, **425 pasos**. Reasoning numérico separado; no es factura, preparación/investigador desconocidos.

Evidencia inicial intacta en low/, high/, sdd-low/ y sdd-high/. La revisión posterior conserva los oráculos aislados y resultados-revisados.json. Los cuatro archivos se verificaron íntegramente por SHA256; manifest-revision.json cubre las auditorías suplementarias y esta revisión. Sin commits/push ni cambios globales.
