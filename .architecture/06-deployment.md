# 6. Distribución e instalación

## 6.1 Modelo de entrega

No se observa un servicio propio que desplegar. La entrega consiste en renderizar
el árbol `generated/<plataforma>/` y copiarlo desde el repositorio a los
directorios de configuración del usuario con scripts Bash o PowerShell. La guía
de instalación define el render, validación, instalación y reinicio del host
como el flujo recomendado (`../docs/instalacion.md:14-22`).

## 6.2 Plataformas y destinos

| Host | Skills | Agentes / prompts | Configuración opcional |
|---|---|---|---|
| GitHub Copilot | `~/.copilot/skills/` | `~/.copilot/agents/` | — |
| OpenCode | `~/.config/opencode/skills/` | `~/.config/opencode/agent/` | `$XDG_CONFIG_HOME/opencode/` |
| Kiro | `~/.kiro/skills/` | `~/.kiro/agents/` | — |
| Claude Code | `~/.claude/skills/` | `~/.claude/agents/` | `$CLAUDE_CONFIG_DIR` |
| Pi | `<agent-dir>/skills/` | `<agent-dir>/prompts/` | `$PI_CODING_AGENT_DIR`; default `~/.pi/agent` |
| Antigravity 2.0 | `~/.gemini/config/skills/` | `~/.gemini/config/agents/` | Runtime pendiente de smoke |

Fuente de la matriz y detalles de Pi: `../docs/instalacion.md:68-88`.
Los directorios son propiedad del entorno del usuario; el repo no controla el
descubrimiento ni la carga de esos archivos después de la copia.
Antigravity CLI documenta una ruta distinta de skills y el instalador 2.0 no la
cubre (`../docs/arquitectura-del-kit.md:107-138`).

La evidencia documentada para scripts Antigravity es de 22/22 pruebas nativas
por OS en Linux, macOS y Windows con Python 3.10 (run 37510771502).
El workflow actual tiene un job general Ubuntu y jobs nativos Antigravity en
macOS/Windows (`../.github/workflows/ci.yml:10-73`). Esto no acredita runtime ni
la migración PowerShell de agentes retirados (`../docs/desarrollo.md:125-154`).

## 6.3 Requisitos de ejecución

- Python 3 para las herramientas de render/validación/importación.
- Bash en macOS/Linux o PowerShell en Windows para wrappers de instalación y
  backup (`../docs/instalacion.md:7-12, 24-48`).
- El cliente host debe estar instalado. Tras actualizar, se recomienda
  reiniciarlo para recargar skills/agentes (`../docs/instalacion.md:161-168`).

## 6.4 Seguridad operacional y reversibilidad

- Antes de copiar, el instalador comprueba que el árbol generado contiene todos
  los artefactos declarados; después comprueba el destino
  (`../tools/install_preflight.py:74-96, 99-137`).
- En instalación normal, el contenido previo se respalda; `--force` omite ese
  backup y `--dry-run` no copia. Las raíces por host están descritas en
  `../docs/instalacion.md:53-60, 99-110`.
- El instalador informa de elementos no declarados y no los elimina. No hay
  desinstalación automática; una restauración de backup es manual
  (`../docs/instalacion.md:135-139, 191-229`).
- `imports/` se mantiene local/ignorada por Git porque puede contener
  configuración importada (`../.gitignore:21-23`).

## 6.5 Infraestructura no aplicable

En el alcance documentado no aparecen bases de datos, servicios de red,
orquestadores ni una topología de despliegue server-side. La sección describe
entrega a entornos locales; no implica un análisis de infraestructura externa ni
de la configuración interna de los seis hosts. El laboratorio local `.agent-lab/`
queda fuera de este pipeline de distribución; su runner experimental no convierte
el kit en un servicio runtime.
