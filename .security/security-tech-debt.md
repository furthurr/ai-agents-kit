# Seguridad — Tablero de hallazgos

Estado al 2026-10-05. La reevaluación diferencial de los artefactos SDD se cerró
con SEC-0005 tras recibir autorización explícita. Todos los findings permanecen
Pendientes de remediación.

| ID | Severidad | Hallazgo | Referencia | Ubicación | Estado |
|----|-----------|----------|------------|-----------|--------|
| SEC-0001 | 🟡 Media | Capacidades amplias del agente Code Review sin controles de acción uniformes en los adaptadores | OWASP LLM06/LLM01 · CWE-250 | `adapters/{copilot,claude,kiro,opencode}/agents/code-review.json` | Pendiente |
| SEC-0005 | 🟡 Media | Instrucciones del workspace entran en contexto SDD junto a herramientas de escritura/ejecución | OWASP LLM01/LLM06 · CWE-1427 · CWE-250 | `canonical/agents/sdd.md:62-70`; `generated/{copilot,claude,kiro}/agents/sdd.*` | Pendiente |
| SEC-0002 | 🟢 Baja | Acciones de CI referenciadas por tags mutables | GitHub Actions hardening · CWE-829 | `.github/workflows/ci.yml:14-16` | Pendiente |
| SEC-0003 | 🟢 Baja | El importador sigue enlaces simbólicos del directorio instalado | CWE-59 | `tools/import_installed.py:32-53` | Pendiente |
| SEC-0004 | 🟢 Baja | Instalaciones pueden conservar agentes obsoletos | OWASP LLM06 · CWE-250 (impacto de privilegios condicional) | `scripts/install/opencode.sh:101-110,133-144`; `tools/install_preflight.py:119-135` | Pendiente |
