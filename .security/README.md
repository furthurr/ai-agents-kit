# Seguridad — ai-agents-kit / laboratorio SDD

Registro de hallazgos del kit y revisión puntual del circuito experimental F07.
No es una certificación del repositorio completo ni del sandbox.

## Revalidación del kit MAS 3.2.0 — 2026-10-14

- Alcance: los cinco findings históricos del kit, sobre `10373b3` y cambios locales.
- SEC-0005/SEC-0001: políticas y mitigaciones distribuidas; comprobación del motor
  de permisos en OpenCode 1.18.34 con proveedor local simulado. Pendiente resistencia
  dinámica de LLM y controles efectivos de los otros hosts.
- SEC-0003: importación sin enlaces en orígenes estables, 9 tests OK.
- SEC-0002: cuatro referencias de Actions fijadas a SHA oficiales y Dependabot mensual.
- SEC-0004: migración opt-in ya implementada, revalidada con 26 tests; no se han
  migrado perfiles reales ni ejecutado los instaladores nativamente en Windows.
- Los IDs SEC-0001/SEC-0002 están repetidos entre kit y F07; se conservan y
  desambiguan por archivo en el tablero. No confundir sus estados.
- Evidencia y límites: [`reviews/remediacion-mas-3.2.0.md`](reviews/remediacion-mas-3.2.0.md).

## Estado de sincronización F07

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
