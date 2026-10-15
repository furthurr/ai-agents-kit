# SEC-0001: Capacidades amplias del agente Code Review

- Estado: Mitigación implementada; pendiente validación de permisos efectivos por host
- Severidad: 🟡 Media
- Referencia: OWASP LLM06:2025 (Excessive Agency) · LLM01:2025 (Prompt Injection) · CWE-250
- Ubicación: `canonical/agents/code-review.md:39-45,64-70`; `adapters/copilot/agents/code-review.json:7-13`; `adapters/claude/agents/code-review.json:7-17`; `adapters/kiro/agents/code-review.json:5-19`; `adapters/opencode/agents/code-review.json:7-20`
- Fecha de detección: 2026-10-05

## Descripción del riesgo

Los adaptadores no aplican un control uniforme de mínimo privilegio para el
agente de revisión. Copilot enumera `edit` y `execute`; Claude enumera `Edit`,
`Write` y `Bash`; Kiro habilita `write` y `shell` y solo deniega un conjunto
pequeño de patrones. Opencode sí configura `ask` para edición y Bash, mientras
que `webfetch` está permitido. El rol revisa contenido de repositorios y su
instrucción de aprobación está expresada en el prompt, no como una restricción
consistente en todos los adaptadores.

Un contenido de repositorio manipulado podría inducir operaciones de escritura,
ejecución o acceso externo no previstas. La explotación y el impacto dependen
de los controles efectivos del host, que no se inspeccionaron en esta auditoría.

## Impacto, esfuerzo y recomendación

- Impacto potencial: cambios no autorizados en archivos o ejecución de comandos;
  exposición de contenido accesible al agente si se induce una acción de salida.
- Esfuerzo estimado: Medio.
- Recomendación: limitar por defecto las herramientas del modo de revisión y
  aplicar en el host aprobación ligada a la acción para escritura, ejecución y
  acceso externo; validar con pruebas de abuso de prompt injection inofensivas.

## Plan de remediación (no ejecutado)

- [ ] Separar revisión de solo lectura de escritura documental/remediación y
  aplicar capacidades mínimas por modo y plataforma.
- [ ] Verificar controles de host y probar que acciones de escritura/ejecución no
  ocurran sin aprobación explícita de esa operación.

## Bitácora

- 2026-10-14: separación explícita de capacidades por operación antes del contexto
  del workspace. `inspect` no ejecuta shell/tests ni envía contenido a servicios
  externos; documentación y remediación conservan alcances diferentes. Kiro pide
  aprobación de escritura/shell y conserva denegaciones destructivas; OpenCode
  pide aprobación de webfetch además de edición, Bash y delegación. No se inventan
  controles equivalentes en hosts que no los declaran en estos adaptadores.
  `test_code_review_contract.py`: 7 tests; `test_permissions.py`: 9 tests, todos OK.
  Límites y permisos por host documentados en `docs/agentes/code-review.md`.
  La separación es conversacional donde no hay perfiles efectivos por operación;
  pendiente prueba dinámica de hosts, sin declarar resuelto el riesgo completo.
  Probe adicional de OpenCode 1.18.34: edición/Bash rechazados y webfetch con
  aprobación/rechazo verificados con proveedor simulado; no acredita conducta LLM.

- 2026-10-05: hallazgo estático registrado; no se modificó código ni configuración.
