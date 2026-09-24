# Perfil de release — Python (kit documental)

- **Señales de detección:** herramientas auxiliares `tools/*.py`; el repositorio es
  un kit documental de agentes/skills, no un paquete Python publicable. No contiene
  `pyproject.toml` ni `setup.py`.
- **Archivo(s) de versión:** `VERSION` → contenido completo del archivo (sin clave);
  `.release/config.md` define esta fuente como canónica para el proyecto.
- **Formato de versión:** SemVer puro `MAJOR.MINOR.PATCH`; sin build number ni
  metadatos adicionales.
- **Bump:** seguir `.release/config.md`: breaking change → MAJOR; nueva capacidad
  compatible (`feat`) → MINOR; correcciones, documentación, refactor o mantenimiento
  compatible → PATCH. Mientras siga en `0.x`, la compatibilidad no se considera
  estable.
- **Herramienta CLI (si existe):** ninguna; actualizar manualmente `VERSION`.
- **Convención de tag:** `vX.Y.Z`, anotado.
- **CHANGELOG:** `CHANGELOG.md` en la raíz, en español; anteponer una entrada agrupada
  por Conventional Commits desde el tag anterior.
- **Notas / edge cases:** PyPA define `[project].version` en `pyproject.toml` y PEP 440
  para metadatos de distribuciones Python. Este repositorio no se empaqueta ni publica
  como distribución Python; sus convenciones locales en `.release/config.md` prevalecen.
- **Fuentes:** <https://packaging.python.org/en/latest/specifications/pyproject-toml/>,
  <https://peps.python.org/pep-0621/>,
  <https://packaging.python.org/en/latest/specifications/version-specifiers/> —
  investigado el 2026-09-23.
