# Tratamientos y aislamiento de la intervención

La comparación principal es **A vs B**. C es referencia ODD, no el objetivo de
la actualización. No se añade un agente al manifiesto ni se toca la instalación.

| ID | Agente público en el proceso | Skill primaria | Fuente |
|---|---|---|---|
| A | `dc-developer` | `dc-developer` | Agente Developer completo y skill actual. |
| B | `dc-developer` | `dc-developer` | [Candidato compacto](candidato.md) y misma skill actual. |
| C | `dc-odd` | `do-odd-workflow` | Tratamiento ODD histórico sin cambios de método. |

Se monta solo la ruta del perfil correspondiente en cada proceso CLI nuevo.
Los nombres A/B opacos evitan presentar una expectativa de «optimización» al
modelo; no constituyen un estudio ciego del coordinador. Ambos perfiles tienen
igual identificador y descripción, prompts funcionales iguales y documentos
sembrados iguales, excepto las rutas de workspace que distinguen las celdas.

La diferencia pretendida es el texto del agente. En A/B, las once skills y todas
sus referencias coinciden byte a byte tras la misma sustitución de nombres de
invocación; los agentes colaboradores conservan sus nombres reales. Se comprueba
igualdad de configuración normalizando rutas y excluyendo exclusivamente el
campo prompt. El directorio de skills por proceso es único y se contrasta el
cuerpo íntegro cargado, no solo un indicador por nombre.

El agente completo A se obtiene del derivado OpenCode del repositorio. B concentra
procedimiento repetido en la skill ya existente, conservando guardas explícitas
que no podían darse por eliminadas: SDD, delegación/cambio de agente, UI/contratos,
secretos, evidencias y cierre documental. La tabla del candidato muestra el mapa
de responsabilidades; no se afirma equivalencia semántica exhaustiva antes de probar.

C utiliza la extracción de instrucciones de
[tratamiento-b.md](../odd-vs-sdd-2026-11-04/tratamiento-b.md). Su registro sigue
siendo `odd/tasks/`, como en el control anterior; no incorpora las decisiones
`.odd/` del plan de producto. Los tres comparten el transporte Antigravity y
los controles de herramientas del harness anterior, sin leer credenciales.

Las estadísticas estáticas iniciales del cuerpo del agente, incluido el mismo
footer de laboratorio, son A: 6.734 bytes/931 palabras; B: 1.764 bytes/234 palabras.
No son tokens reales ni tamaño completo del contexto: la skill, metadatos,
instrucciones comunes e historial también se incorporan durante la ejecución.
