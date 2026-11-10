# Inventario de PII y secretos

| Dato | Tipo | Dónde aparece | Cifrado | Almacenamiento | Notas |
|---|---|---|---|---|---|
| Credenciales OpenCode del operador | Secreto de autenticación | Fuente de autenticación local autorizada, fuera de los artefactos de campaña | Gestionado por el cliente | HOME/XDG del usuario | No copiar, inspeccionar ni registrar valores. |
| Datos ReserveLab | Datos sintéticos de inventario/reservas | Snapshots, runs y DB de prueba | No aplica para datos sintéticos | `.agent-lab/sdd-escalation/` | Verificar que no se introduzcan datos reales; runs están fuera de Git por política local. |

No se identificó PII real en el alcance revisado; el repositorio completo no ha sido
inventariado en esta revisión puntual.

## Alcance adicional: Genera Android/iOS — 2026-11-10

Se confirmaron rutas personales e identificadores internos en evidencias móviles.
El árbol no comprimido se anonimiza con placeholders y métricas históricas. Se
reescribieron con autorización las refs locales del historial; no se publicó ni
se purgaron objetos/reflogs. Después se autorizó eliminar la nota local de
continuidad porque conservaba referencias privadas. Su retirada del árbol de
trabajo está pendiente de commit. Los nueve avisos iniciales en comprimidos no confirmaban
datos de Genera y se descartaron tras decodificar las evidencias. No se confirmó
una credencial operativa de Genera. Los datos de otros proyectos de laboratorio
quedan fuera del alcance acordado. Seguimiento: [SEC-0006](findings/SEC-0006-exposicion-evidencias-moviles.md).
