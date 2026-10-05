# Estándar cacheado — agentes de IA

Consulta: 2026-10-05. Perfil aplicado a definiciones de agente, instrucciones,
fuentes de contexto y herramientas configuradas en este kit. No sustituye una
evaluación del permiso efectivo de cada host.

## Controles relevantes

- **OWASP Top 10 for LLM Applications 2025 — LLM01 Prompt Injection:** el texto
  externo o recuperado puede alterar la conducta del modelo; separar instrucciones
  y datos con etiquetas no constituye por sí solo una frontera de seguridad.
- **LLM06 Excessive Agency:** limitar herramientas, funcionalidad, autonomía y
  permisos al mínimo necesario; tratar las salidas del modelo como no confiables;
  exigir autorización externa al modelo para acciones de impacto.
- **OWASP AI Agent Security Cheat Sheet:** validar herramientas y parámetros en
  el límite de ejecución, aplicar aprobación humana ligada a la acción concreta,
  restringir por rol/alcance y probar prompt injection directa e indirecta con
  herramientas instrumentadas.
- **CWE-250:** ejecución con privilegios/capacidades superiores a los mínimos
  necesarios. Aplicable al análisis de agentes que exponen escritura, shell o
  ejecución de comandos.
- **CWE-1427:** datos externos usados para construir el contexto de un LLM sin
  distinguir de forma efectiva el contenido no confiable de las directivas del
  sistema. Aplica al análisis de fuentes del workspace incluidas en contexto.

## Uso en esta auditoría

Se usó para SEC-0001 y SEC-0005, incluida la reevaluación diferencial de
artefactos SDD. La configuración efectiva de permisos del host no se inspeccionó;
cuando el impacto depende de ella, se documenta explícitamente esa limitación.

## Fuentes

- OWASP LLM Top 10 (2025): <https://genai.owasp.org/llm-top-10/>
- OWASP LLM06: <https://genai.owasp.org/llmrisk/llm062025-excessive-agency/>
- OWASP AI Agent Security Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html>
- OWASP Prompt Injection Prevention Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html>
- CWE-250: <https://cwe.mitre.org/data/definitions/250.html>
- CWE-1427: <https://cwe.mitre.org/data/definitions/1427.html>
