# Resultado de remediación — REC-05: validar instalaciones completas

## Identificación

- **Estado actual:** Cerrado sobre `main` HEAD `8fea7bb`. **Estado en la entrega original:** implementado y verificado en fixtures, aún sin commit/CI.
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
- En la entrega original no había commit ni CI remota; el estado propuesto era **Integrado pendiente de verificación**.

## Revalidación integrada — 2026-10-13

- **Baseline actual:** `main` HEAD `10373b3e9510cc71049eb37c5393b4e18415e40d` (`v3.2.0`).
- **Verificación focalizada local:** `python3 -B tools/test_install.py` 250/250; `python3 -B tools/test_antigravity_install.py` 22/22; `git diff --check` correcto.
- **CI integrada actual:** [run 38352143368](https://github.com/furthurr/ai-agents-kit/actions/runs/38352143368), SUCCESS para el mismo HEAD. Incluye tests generales de instaladores y job nativo `windows-latest` para Antigravity.
- **Criterios:** los seis wrappers usan el preflight común que compara rutas/hashes de fuente y destino; pruebas temporales rechazan recursos ausentes/alterados antes de declarar éxito.
- **Límite separado:** la evidencia nativa de todos los demás wrappers PowerShell sigue abierta en FUT-20; no invalida el cierre de REC-05 sobre los criterios integrados de integridad.
- **Cierre:** REC-05 **Cerrado**.
