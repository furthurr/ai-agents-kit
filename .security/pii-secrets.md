# Inventario de PII y secretos

| Dato | Tipo | Dónde aparece | Cifrado | Almacenamiento | Notas |
|---|---|---|---|---|---|
| Credenciales OpenCode del operador | Secreto de autenticación | Fuente de autenticación local autorizada, fuera de los artefactos de campaña | Gestionado por el cliente | HOME/XDG del usuario | No copiar, inspeccionar ni registrar valores. |
| Datos ReserveLab | Datos sintéticos de inventario/reservas | Snapshots, runs y DB de prueba | No aplica para datos sintéticos | `.agent-lab/sdd-escalation/` | Verificar que no se introduzcan datos reales; runs están fuera de Git por política local. |

No se identificó PII real en el alcance revisado; el repositorio completo no ha sido
inventariado en esta revisión puntual.
