# Estándar cacheado — Python, Bash y PowerShell de tooling

Consulta: 2026-10-05. Perfil aplicado a instaladores e importadores locales; no
es una certificación de plataforma Windows ni una guía completa de hardening.

## Controles relevantes

- Preferir APIs de biblioteca sobre comandos del sistema. Si la ejecución de un
  proceso es necesaria, mantener ejecutable y argumentos separados, validar
  valores contra allowlists y evitar construir comandos de shell con datos no
  confiables.
- Al copiar archivos desde ubicaciones controlables por el usuario, resolver y
  validar el destino/origen y decidir expresamente cómo manejar enlaces
  simbólicos; no seguirlos implícitamente fuera de la raíz autorizada.
- Ejecutar con privilegios mínimos y validar paths antes de leer, escribir o
  copiar. Un directorio local de importación puede contener datos sensibles aunque
  esté ignorado por Git.
- CWE-59 cubre acceso a través de enlaces que resuelven a recursos no previstos;
  CWE-250 cubre capacidades/privilegios superiores a los necesarios.

## Uso en esta auditoría

No se hallaron llamadas a `eval`/`Invoke-Expression` en las fuentes de scripts
revisadas. SEC-0003 documenta el seguimiento de enlaces del importador. Las
herramientas Python inspeccionadas emplean principalmente APIs de biblioteca;
`npm audit` no es una auditoría de código ni de dependencias de sistema.

## Fuentes

- OWASP OS Command Injection Defense Cheat Sheet:
  <https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html>
- CWE-59: <https://cwe.mitre.org/data/definitions/59.html>
- CWE-250: <https://cwe.mitre.org/data/definitions/250.html>
