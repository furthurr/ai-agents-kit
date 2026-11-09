# GPT-6 Luna / Copilot — LL-SEARCH (media-baja)

**6 invocaciones iniciales, 5 entregas aceptadas.**

| Configuración | Tokens comparables | Tiempo | Pasos | Tests nuevos | Oráculos | Conjunta | Aceptación |
|---|---:|---:|---:|---:|---|---|---|
| SDD instalado | 161.046 | 54,895 s | 8 | 0 | FAIL (8 fallos, 0 errores) | 56 ejecutados; 8 fallos, 0 errores | awaiting_operator_review_not_automatically_a_gate |
| Build sin MAS | 268.877 | 79,462 s | 12 | 9 | 13/13 | 65/65 | PASS |
| Developer instalado | 926.176 | 173,055 s | 21 | 8 | 13/13 | 64/64 | PASS |
| Candidato2 + dos refuerzos | 926.483 | 202,044 s | 24 | 8 | 13/13 | 64/64 | PASS |
| Build con MAS | 942.307 | 158,098 s | 26 | 5 | 13/13 | 61/61 | PASS |
| Developer v2 candidato2 | 1.009.926 | 213,299 s | 26 | 7 | 13/13 | 63/63 | PASS |

## Alcance y límites

- Solo LL-SEARCH. No se ejecutó TASK-2 Alta.
- Mismos snapshots, checkout, tarea, oráculos y allowlists de las pruebas previas; copias nuevas, sin soluciones reutilizadas.
- Modelo nativo `github-copilot/gpt-6-luna`, sin variante explícita. Temperatura no soportada; predeterminado del proveedor.
- 1.800 s / 60 pasos / umbral 5 M tokens por invocación. Sin reintentos, inferencias auxiliares ni respuestas simuladas.
- Una pausa o bloqueo no equivale a implementación fallida ni a permiso para reanudar. Consultar final_text en resultados.json.
- Fidelidad procedural no certificada; aceptación funcional y entrega de pruebas se mantienen separadas.
- n=1, proveedor/tokenizer/caché/latencia distintos; no concluir superioridad universal. Tokens no equivalen a factura.
- Se preserva la fricción del prompt heredado: el Python compartido está fuera del workspace; no se ampliaron permisos.
- Evidencia anterior intacta; sin cambios globales, commits ni push.

Total observado: 4.234.815 tokens comparables, 880,853 s y 117 pasos.

Ver resultados.json, los dos archivos de evidencia y manifest.json de esta revisión.
