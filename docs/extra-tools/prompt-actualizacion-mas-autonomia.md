# Prompt de actualización de MAS y modo autónomo

> **Estado:** documento operativo. Es un prompt listo para copiar y pegar en cualquier agente con acceso al repositorio y al `HOME` del usuario.
>
> **Actualizado:** 2026-11-11.
>
> **Contrato de referencia:** [modo-autonomo.md](modo-autonomo.md) (norma) y [compatibilidad-hosts.md](../compatibilidad-hosts.md) (mínimos por host).

## Propósito

Un único prompt que hace dos cosas a la vez:

1. Instalar la **última versión de MAS** (skills, agentes y referencias) en las seis plataformas soportadas.
2. **Activar el modo autónomo** documentado en [modo-autonomo.md](modo-autonomo.md), sin borrar configuración propia ni saltarse denegaciones del host.

Está pensado para reusarse: después de cada `git pull` del kit o de cada actualización del repositorio, porque **reinstalar MAS repone los `ask` de los agentes** y el perfil autónomo hay que volver a aplicarlo.

## Cuándo usarlo

- Acabas de actualizar el repositorio del kit y quieres la versión vigente instalada en tus máquinas.
- Has reinstalado una herramienta y ha perdido el perfil autónomo.
- quieres dejar las seis plataformas con el mismo inventario y el mismo modo de trabajo.

## Requisitos

- **Del kit:** `python3` (3.10+), `git` y `bash` (o PowerShell en Windows).
- **De los hosts:** ninguno es obligatorio. Si una plataforma no está instalada, su perfil se deja preparado y el informe lo indica; no se bloquea el resto.

## Prompt (copiar y pegar)

````text
Actualiza el MAS y activa el modo autónomo en las plataformas soportadas.

FUENTE
Repo: https://github.com/furthurr/ai-agents-kit (main; clona si no existe).
Norma: docs/extra-tools/modo-autonomo.md · Mínimos por host: docs/compatibilidad-hosts.md.

ALCANCE
Plataformas: copilot, opencode, kiro, claude, pi, antigravity (canonical/manifest.json).
No edites canonical/, adapters/ ni generated/. Sin commit/push/tag/release salvo petición.

0) DETECCIÓN (no asumas)
- Requisitos: python3 3.10+, git, bash|pwsh. Si faltan python3/git: para con aviso accionable.
- Por plataforma registra CLI/app/extensión + versión, y si existe su perfil previo (~/.copilot, ~/.config/opencode, ~/.kiro, ~/.claude, ~/.pi/agent, ~/.gemini/config).
- Versión por debajo del mínimo: instala igual, anota y cita el requisito.

1) git -C <repo> pull --ff-only
2) python3 tools/render.py && python3 tools/validate.py → si falla, para y reporta; no instales incompleto.
3) Suite: test_install, test_integrity, test_host_compat, test_antigravity_install + bash -n scripts/install/*.sh scripts/backup/*.sh.
4) Instala MAS en las 6 (bash o ps1) aunque el host no esté instalado (solo copian perfiles):
   scripts/install/{copilot,opencode,kiro,claude,pi,antigravity}.sh → confirma "Instalación completada" ×6.
5) AUTONOMÍA con tools/configure_autonomy.py: dry-run y luego --apply.
   Aplica si la superficie existe o hay perfil previo; si no, omite y reporta.
   opencode: --host opencode (+ --project RUTA solo si ese proyecto tiene opencode.json con ask).
   claude: --host claude · pi: --host pi.
   kiro: --host kiro --network (CLI 2.37+/3.x; si V3 no está activo, indica `kiro-cli settings chat.agentEngine v3`).
   copilot-cli: --host copilot-cli --project <repo> (solo si CLI/extensión disponible; --command solo con identificadores literales o :*).
   antigravity: app solo si existe la app; cli solo si hay `agy`; ide solo si hay extensión.
   Justifica cada --network. Si el dry-run de un host falla, no lo fuerces: sigue con los demás y reporta el error.
6) VERIFICACIÓN
   - Dry-run repetido por host aplicado → "sin cambios" (idempotencia).
   - Skills instaladas idénticas a generated/<plataforma>/skills.
   - Agentes de opencode/kiro pueden diferir (ask→allow): confirma que los deny siguen.
   - Solo afirma "runtime" en hosts instalados y arrancados; en ausentes, solo perfil escrito y válido.
   - Respaldos presentes en ~/.ai-agents-kit-autonomy/backups/ y en la raíz de backup de cada plataforma.
7) INFORME: tabla plataforma | host detectado (versión) | MAS sí/no | autonomía sí/no/parcial | pasos manuales; más archivos creados, rutas de respaldo, límites y qué reiniciar. Un host ausente no bloquea el resto.

REGLAS
No borres contenido ajeno (los instaladores solo fusionan e informan). No expongas secretos. No inventes ajustes: UI pendiente (Antigravity App → Settings → General → Permission Settings → Turbo; Kiro IDE → Agent Autonomy → Autopilot) se reporta como paso manual. Autonomy ≠ sandbox: permitir shell/red no protege secretos. Tras cada actualización del MAS, reaplica el modo autónomo (la reinstalación repone los ask).
````

## Ajustes opcionales

| Si quieres… | Añade o cambia |
|---|---|
| Autorizar comandos concretos en Copilot | `--command "npm test"` (solo identificadores literales o con sufijo `:*`) |
| No abrir la red en los sandboxes | Quita `--network` de Kiro y Antigravity |
| Incluir reglas `ask` de un proyecto OpenCode | `--project /ruta/del/proyecto` en el paso 5 de opencode |
| Trabajar sobre otro clon | Sustituye `<repo>` por la ruta local |

## Qué esperar al terminar

- Las seis plataformas con **11 skills y 5 agentes** instalados y verificados por hash.
- Los agentes de **opencode** y **kiro** con `ask` promovidos a `allow` y sus `deny` intactos (`.sdd/**`, `task`, comandos destructivos).
- Ficheros de autonomía por host: `opencode.json` + `ai-agents-kit-autonomy.md`, `~/.claude/settings.json` + `CLAUDE.md`, `~/.kiro/settings/permissions.yaml` + steering, `~/.gemini/AGENTS.md` + `~/.gemini/antigravity-cli/settings.json`, `~/.pi/agent/APPEND_SYSTEM.md` y, en Copilot, `permissions-config.json` + `settings.json` + instrucciones.
- Respaldos en `~/.ai-agents-kit-autonomy/backups/` y en la raíz de backup de cada plataforma (`~/.copilot-backup`, `~/.opencode-kit-backup`, `~/.kiro-kit-backup`, `~/.claude-kit-backup`, `~/.pi-kit-backup`, `~/.antigravity-kit-backup`).

## Verificación posterior

```bash
python3 tools/host_compat.py --matrix
python3 tools/host_compat.py --check kiro
python3 tools/host_compat.py --check opencode
python3 tools/host_compat.py --check pi
```

Un dry-run de `tools/configure_autonomy.py` por host debe indicar **"sin cambios"**: es la señal de que el perfil ya está aplicado y es idempotente.

## Límites que conviene recordar

- El modo autónomo **no es un sandbox**: permitir shell o red no protege secretos por sí mismo; los `deny` siguen siendo la barrera real.
- Persisten los límites de cada host: `ask` de otros ámbitos, políticas administradas, workspace trust, gates de extensiones y revisores de artefactos.
- En **Antigravity App** y **Kiro IDE** los permisos se ajustan en la interfaz; el script solo escribe las reglas globales y lo deja anotado como paso manual.
- La automatización cubre instalación, permisos e instrucciones. **No** sustituye un smoke con modelo ni demuestra conducta de los agentes.

## Referencias

- [modo-autonomo.md](modo-autonomo.md) — contrato del modo autónomo por host.
- [compatibilidad-hosts.md](../compatibilidad-hosts.md) — versiones mínimas, formatos y hosts antiguos.
- [instalacion.md](../instalacion.md) — instaladores, destinos, backups y restauración.
- [permisos-hosts.md](../permisos-hosts.md) — capacidades y fronteras de confianza por host.
