# Estándares de calidad — Python

Fuente pública de SonarQube consultada el 2026-10-05. Caché limitada a la regla
aplicada en el hallazgo inicial; no representa un escaneo completo del lenguaje.

## `python:S1764` — expresiones idénticas en los operandos de una operación

- Descripción de Sonar: detecta operaciones binarias cuyos operandos izquierdo
  y derecho son iguales.
- Aplicación en este repositorio: una expresión booleana `or` contiene la misma
  condición `"$RepoRoot" in content` dos veces en
  `tools/test_integrity.py:163`. Las condiciones repetidas de las líneas
  167-170 también tienen valores idénticos pese a cambiar la forma de escribir
  las comillas.
- Clasificación del hallazgo: Code Smell / Maintainability; severidad asignada
  en este registro: Low por el impacto reducido y localizado en una prueba.
- Fuente oficial: [consulta de documentación de SonarQube sobre
  `python:S1764`](https://docs.sonarsource.com/sonarqube-server/quality-standards-administration/managing-rules/rules.md?ask=What%20is%20the%20Python%20rule%20python%3AS1764%20and%20what%20does%20it%20detect%3F&goal=Cache%20the%20public%20rule%20description%20for%20a%20Code%20Quality%20audit).
