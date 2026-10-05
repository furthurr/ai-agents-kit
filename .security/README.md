# Seguridad — AI Agents Kit

Estado canónico de seguridad del kit. Este repositorio distribuye agentes,
skills y herramientas de instalación; no es una aplicación móvil ni un servicio
de usuario.

## Estado de sincronización

- Plataforma/tecnología: Markdown, JSON, Python 3 (biblioteca estándar), Bash,
  PowerShell, GitHub Actions y configuraciones de agentes.
- Estándares aplicados: OWASP Top 10 for LLM Applications 2025, OWASP AI Agent
  Security, OWASP GitHub Actions guidance y CWE.
- Snapshot: working tree local observado el 2026-10-05; había modificaciones
  locales. No se usa `HEAD` como baseline ni se atribuyen cambios a él.
- Última actualización: 2026-10-05.
- Estado: auditoría inicial **entregada**. Hay 5 findings abiertos (2 Media,
  3 Baja). El diferencial SDD fue revisado y SEC-0005 se registró tras la
  autorización explícita.

## Contexto para IA

- **Perfil de riesgo:** artefactos de agentes que pueden leer repositorios y,
  según el host, editar archivos, ejecutar comandos o consultar la web; scripts
  que copian contenido entre el repositorio y directorios de usuario.
- **Superficie sensible:** permisos de herramientas y prompt injection en
  agentes; instrucciones de workspace leídas por SDD; importación mediante
  enlaces; persistencia de artefactos antiguos; dependencias npm de OpenCode y
  referencias de GitHub Actions.
- **Autenticación/red/almacenamiento de aplicación:** no hay servicio de
  aplicación, endpoints propios, usuarios finales ni almacenamiento de datos de
  usuario. Los accesos de red revisados son los de herramientas/CI.
- **PII/secretos:** el README publica datos de contacto del autor; no se copian
  sus valores aquí. Una búsqueda de formatos comunes de claves/tokens no halló
  coincidencias. Ver [`pii-secrets.md`](pii-secrets.md) para límites y ubicación.
- **Hallazgos abiertos:** 2 Media y 3 Baja en
  [`security-tech-debt.md`](security-tech-debt.md). El diferencial SDD está
  registrado como SEC-0005; los hallazgos siguen pendientes de remediación.
- **Dependencias:** el único manifiesto de paquetes detectado es
  `.opencode/package.json`; `npm audit` informó cero vulnerabilidades conocidas
  en el lockfile revisado. Ver [`dependencies.md`](dependencies.md).

## Índice

- Tablero: [`security-tech-debt.md`](security-tech-debt.md)
- Findings aprobados: [`findings/`](findings/)
- PII y secretos: [`pii-secrets.md`](pii-secrets.md)
- Dependencias: [`dependencies.md`](dependencies.md)
- Estándares cacheados: [`standards/`](standards/) — `agentic-ai.md`,
  `github-actions.md`, `python-shell-powershell.md`.
