# GPT-6 Luna / Copilot — TASK-2 Alta

**6 invocaciones iniciales, 0 entregas aceptadas.**

| Configuración | Tokens | Tiempo | Pasos | Tests nuevos | Originales | Oráculos | Bordes | Conjunta | Resultado |
|---|---:|---:|---:|---:|---|---|---|---|---|
| SDD instalado | 118.389 | 67,211 s | 6 | 0 | 43/43 | FAIL | FAIL | 52 ejecutados; 9 fallos, 0 errores | Pausa real; sin entrega |
| Build sin MAS | 725.466 | 262,163 s | 22 | 6 | 43/43 | 9/9 | FAIL | 58 ejecutados; 1 fallos, 0 errores | No aceptado: bordes |
| Candidato2 + dos refuerzos | 1.286.458 | 301,894 s | 28 | 7 | 43/43 | 9/9 | FAIL | 59 ejecutados; 0 fallos, 4 errores | No aceptado: bordes |
| Developer v2 candidato2 | 1.365.817 | 889,118 s | 31 | 6 | 43/43 | 9/9 | FAIL | 58/58 | No aceptado: bordes |
| Build con MAS | 1.600.225 | 311,863 s | 37 | 6 | 43/43 | 9/9 | FAIL | 58/58 | No aceptado: bordes |
| Developer instalado | 1.968.716 | 304,169 s | 36 | 8 | 43/43 | 9/9 | FAIL | 60/60 | No aceptado: bordes |

## Lectura

- Solo TASK-2 Alta. No se reanuda el SDD de media-baja ni se interpreta esta petición como su aprobación.
- Mismo contrato congelado, checkout, perfiles, oráculos y bordes; copias nuevas sin soluciones reutilizadas.
- Modelo nativo `github-copilot/gpt-6-luna`, sin variante explícita. Temperatura no soportada; predeterminado del proveedor.
- 1.800 s / 60 pasos / umbral 5 M por invocación. Sin reintentos, inferencias auxiliares ni aprobaciones simuladas.
- Aceptación completa exige funcionalidad, oráculos, bordes, check/migraciones y pruebas nuevas persistidas.
- Una pausa de gate o una aprobación pendiente no es una implementación fallida; revisar final_text.
- Fidelidad procedural no certificada; n=1 y proveedor distinto impiden conclusiones causales o universales.
- No se ampliaron permisos ni se corrigieron trayectorias. Evidencia anterior intacta; sin commits ni push.

Total observado: 7.065.071 tokens comparables, 2136,418 s y 160 pasos.
