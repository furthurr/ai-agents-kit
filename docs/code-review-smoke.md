# Smoke test de Code Review

Estado: escenarios definidos, no ejecutados en un host real para esta feature.
Los tests de contratos de prompts y validadores no sustituyen estos escenarios.
Usa un proyecto desechable; registra plataforma, versión, fecha, commit y evidencia.

## Preparación

Renderiza y valida el kit. Instala una plataforma solo cuando lo autorice el
usuario, retira las copias antiguas del kit según
[la guía](instalacion.md#actualizar-a-code-review) y reinicia el host.
Debe aparecer `code-review`; las dos skills siguen instaladas.
El preflight es informativo: cada operación autorizada continúa en el mismo turno,
sin exigir «continúa» ni confirmación de modelo. Un aviso ya comunicado para el
mismo alcance no se repite al cargar otra skill o recibir un handoff.
Compara el árbol de archivos antes/después cuando el caso sea de solo lectura.

## Escenarios

| Caso | Petición | Resultado esperado |
|---|---|---|
| Solo calidad | Solo calidad: revisa complejidad de este módulo, sin escribir | Usa Sonar, no escanea seguridad ni crea `.quality/`, cachés o marcas |
| Solo seguridad | Solo seguridad: revisa TLS y almacenamiento, sin escribir | Usa OWASP/CWE, incluye configuración relevante, sin análisis de calidad ni escrituras |
| Completa | Revisión completa de calidad y seguridad del módulo, sin escribir | Ambas skills, un preflight, resumen con dominio y severidad original; sin archivos |
| Documental | Audita y documenta ambos dominios de este módulo | Findings verificados en ambas carpetas; todas las severidades, sin selección posterior; duplicados agrupados |
| Estado | Explica QLT-0001 y después SEC-0001 | Usa cada procedimiento; conserva IDs/estados y no dispara auditoría global |
| Dominio no autorizado | Solo calidad, con un riesgo de TLS observable | Informa y ofrece ampliar; no escribe `.security/` ni remedia el riesgo |
| Remediación | Propón corregir SEC-0001 | Explica plan; espera autorización antes del primer micro-paso y de cada siguiente |
| Cambio complejo | Corrección que requiere rediseñar auth | Recomienda SDD con referencia, se detiene antes de código y no cambia de agente |
| Fallo parcial | Una revisión documental de ambos no puede completar seguridad | No declara completos ambos; informa el bloqueo y no omite resultados silenciosamente |

No uses secretos reales en fixtures: solo placeholders. Una dependencia solo se
declara vulnerable cuando hay fuente verificable; cobertura solo con medición.

## Handoff productor–receptor

Con documentación existente y plan autorizado, pide al orquestador derivar ambos
dominios al agente real. Debe emitir `target: code-review`, la acción indicada y
`scope: [.quality/, .security/]`, sin ejecutar también esas revisiones localmente.

- `inspect`: `write_scope: none`, `requires_confirmation: false`; sin escrituras.
- `sync`: `write_scope: [.quality/, .security/]`, `requires_confirmation: true`.
  Una autorización efectiva de esa misma sesión evita repetir la pregunta;
  copiar `gate_state` a otra sesión no concede autorización por sí solo.
- Una escritura conjunta entregada exige evidencia existente de cada dominio.
- Repite con solo `.quality/` y solo `.security/`: no amplía el dominio recibido.
- Prueba listas vacías/duplicadas, scope ajeno, targets antiguos, discrepancias
  de escritura, rutas con `..`, raíces redirigidas por symlink y evidencia del
  dominio no seleccionado: el receptor rechaza antes de ejecutar.

## Cierre y evidencia

Marca cada caso ejecutado solo con resultado observado y evidencia. La migración
no elimina IDs ni mueve `.quality/` o `.security/`. Los prompts viejos del home
no se eliminan automáticamente; no borrar las skills por confundir sus nombres.

Checks mecánicos: `python3 tools/test_code_review_contract.py`,
`python3 tools/test_handoff_contract.py` y `python3 tools/test_model_recommendations.py`.
Estos comandos validan contratos y distribución, no el comportamiento conversacional
de todos los modelos/hosts.
