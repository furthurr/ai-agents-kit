# Resultado de remediación — REC-05: validar instalaciones completas

## Identificación

- **Estado local:** implementado y verificado en fixtures; integrado pendiente de commit/CI.
- **Sesión:** coordinadora e implementadora exclusiva en el worktree principal.
- **Fecha:** 2026-10-12.
- **Rama / baseline:** `main`, HEAD `43fd2dc` (`v1.3.0`) más cambios locales preexistentes de Developer y esta tanda. Staging vacío al iniciar.

## Diagnóstico y cambio

El preflight común comprobaba la presencia de los archivos principales, pero podía dejar pasar referencias ausentes o alteradas. Ahora renderiza las fuentes canónicas a un directorio temporal, deriva los paths y hashes esperados, y compara los recursos esperados de `generated/<plataforma>/` antes de copiar. Después de copiar, verifica cada archivo esperado y su hash antes de informar éxito.

Los seis wrappers siguen usando el mismo preflight. Se mantienen el backup previo, `--dry-run` y la preservación de contenido extra del perfil del usuario.

## Verificación

| Comando | Resultado |
|---|---|
| `python3 -B tools/test_install.py` | 250/250; ejecuta los seis wrappers Bash en perfiles temporales, rechaza referencias anidadas ausentes/alteradas antes de escribir y verifica el postflight. Incluye paridad estática Bash/PowerShell. |
| `python3 -B tools/test_antigravity_install.py` | 22/22. |
| `python3 -B tools/test_retired_agents.py` | 26/26. |
| `python3 -B tools/validate.py` | 11 skills, 5 agentes y 6 plataformas. |
| `git diff --check` | Correcto. |

## Límites y entrega

- Pruebas de instalación en perfiles temporales; no se escribió en perfiles reales.
- La paridad PowerShell está verificada estáticamente en los seis wrappers; no se ejecutaron nativamente todos en Windows en esta sesión.
- No hay commit ni CI remota todavía. Estado propuesto: **Integrado pendiente de verificación** hasta preparar y revisar el commit de publicación.
