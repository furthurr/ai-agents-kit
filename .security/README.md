# Seguridad — ai-agents-kit / laboratorio SDD

Registro de revisión puntual de seguridad del circuito experimental F07. No es una
certificación del repositorio completo ni del sandbox.

## Estado de sincronización

- Plataforma/tecnología: Python, pytest, SQLite, Docker y OpenCode; runner local de laboratorio.
- Estándar aplicado: OWASP ASVS 5.0.0 (controles generales de límite de confianza e integridad) + CWE.
- Alcance: ejecución/evaluación F07, supervisor/inspector y proxy observado; otros dominios por revisar.
- Última actualización: 2026-10-07.

## Contexto para IA

- Perfil de riesgo: candidato LLM no confiable modifica lógica y se ejecuta para medir reservas concurrentes e integridad del inventario.
- Superficie sensible: `sandbox_lab_run`, MCP del candidato, `storage_rpc.py`, SQLite de evaluación y worker en Docker.
- PII/secretos: no son el objeto de este piloto; inventario en `pii-secrets.md`, sin valores.
- Hallazgos SEC-0001/SEC-0002 resueltos en el alcance F07 revisado; decisión y límites en `reviews/f07-2026-10-07.md`.
- Dependencias vulnerables: SCA no ejecutado; ver `dependencies.md`.

La excepción del usuario para omitir revisión formal está limitada a F01–F04
(`.agent-lab/sdd-escalation/runtime/pilot-review-waiver.json`). No cubre F07 y no es
un certificado de seguridad. La reauditoría técnica F07 fue realizada por el asistente
IA y no encontró bloqueantes pendientes en el alcance comprobado. El registro final
debe vincular fuentes/imagen y no sustituye gates SDD ni autorización de gasto/modelos.

## Índice

- Hallazgos: `findings/`
- Tablero: `security-tech-debt.md`
- PII/secretos: `pii-secrets.md`
- Dependencias: `dependencies.md`
- Estándar utilizado: `standards/python-runner.md`
