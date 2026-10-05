---
description: Ejecuta solo el escenario sintético offline del laboratorio SDD, sin modelos
---

Ejecuta el escenario sintético de `.agent-lab/sdd-escalation/`. No es una campaña con
modelos, no mide capacidad ni ejecuta soluciones candidatas.

Desde la raíz del repositorio:

1. Comprueba que `.agent-lab/sdd-escalation/runs/` existe.
2. Elige un ID local nuevo con letras, números y guiones; no reutilices un ID existente.
3. Ejecuta `python3 .agent-lab/sdd-escalation/lab.py simulate --output .agent-lab/sdd-escalation/runs --campaign-id <id-nuevo>` con ese ID como argumento citado.
4. Resume el JSON y señala el path del reporte. Explica que los outcomes son
   predefinidos y no representan resultados de SDD ni de modelos reales.

No llames `opencode run`, proveedores, candidatos, API de modelos o Docker.
No borres ni sobrescribas registros existentes para repetir la simulación.
No cambies modelo, variante, permisos globales o credenciales.
