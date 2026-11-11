# Compatibilidad de hosts

Matriz de versiones, formatos distribuidos y comportamiento con hosts antiguos.
El objetivo es no romper una instalación existente: cuando una versión vieja no
puede leer un formato nuevo, el kit lo avisa y conserva el contenido previo; no
borra agentes ni configuraciones ajenas.

Consulta: **2026-11-10**. Las versiones “validadas” son las comprobadas en este
repositorio o en la máquina de auditoría; no sustituyen un smoke runtime del host.

| Plataforma | Host | Mínimo | Validado | Formato distribuido | Comportamiento con versión antigua |
|---|---|---|---|---|---|
| `copilot` | GitHub Copilot CLI / VS Code | CLI 1.x o VS Code actual | CLI 1.0.109; VS Code 1.145.3 | `~/.copilot/skills/` + `~/.copilot/agents/*.agent.md` | El formato `.agent.md` y los alias de tools son estables. `argument-hint` solo aplica a VS Code; Copilot cloud lo ignora. |
| `opencode` | OpenCode | 1.18+ | 1.18.34 (V1) y 2.2.7 (V2) | `~/.config/opencode/skills/` + `~/.config/opencode/agent/*.md` | Se conserva el frontmatter V1 a propósito: OpenCode 1.x lo usa de forma nativa y OpenCode 2.x lo traduce. En V2, `temperature` no se envía; los permisos y el modo siguen funcionando. |
| `kiro` | Kiro IDE / Kiro CLI | IDE 1.0+; CLI 2.37+ con motor V3, o CLI 3.x | IDE 1.4.154; CLI 2.37.1 con motor V3 opt-in | `~/.kiro/skills/` + `~/.kiro/agents/*.md` (Markdown V3) | Kiro CLI 2.x en motor V2 ignora los `.md`. El instalador avisa y **no toca** los agentes JSON existentes. Activa V3 con `kiro-cli settings chat.agentEngine v3` o `kiro-cli --v3`; también puedes usar el IDE. `--strict-host` aborta antes de copiar si V3 no está activo. |
| `claude` | Claude Code | 2.1+ | 2.1.322 | `~/.claude/skills/` + `~/.claude/agents/*.md` | `user-invocable` no es un campo de subagente de Claude Code y se ignora; en VS Code sirve para ocultar la copia Claude del selector. No impide cargar el agente. |
| `pi` | Pi | 0.99+ | 0.99.2 y 1.5.2 | `~/.pi/agent/skills/` + `~/.pi/agent/prompts/*.md` | Las rutas, `argument-hint` y `$ARGUMENTS` se mantienen en 1.x. Los agentes son prompt templates: no crean subagentes aislados ni permisos por rol. |
| `antigravity` | Google Antigravity App / CLI | 2.31+ | 2.31.0 | `~/.gemini/config/skills/` + `~/.gemini/config/agents/*.md` | App y CLI leen la ruta compartida. El CLI también lee `~/.gemini/antigravity-cli/skills/` y `~/.gemini/skills/` con prioridad; evita duplicar nombres si usas esas rutas. |

## Kiro: V2, V3 y compatibilidad

Kiro CLI 2.37 incorpora el motor V3, pero el valor predeterminado sigue siendo
V2. La diferencia importa:

- **V2** lee agentes JSON (`~/.kiro/agents/*.json`) y usa `toolsSettings`/`allowedTools`.
- **V3** lee agentes Markdown (`*.md`) y usa `tools` + `permissions.rules`.
- **CLI 3.x** usa V3 por defecto.

El instalador distribuye Markdown V3 porque es el formato del IDE 1.x y del motor
V3. Si detecta una CLI 2.x en motor V2:

1. Instala igualmente las skills y los agentes Markdown.
2. Avisa de que la CLI actual no cargará los `.md`.
3. No modifica ni elimina los agentes JSON que ya existan.
4. Con `--strict-host` / `-StrictHost`, aborta antes de copiar.

Para actualizar una CLI 2.x:

```bash
kiro-cli update
kiro-cli settings chat.agentEngine v3
kiro-cli --version
```

Si prefieres no cambiar el motor global, usa `kiro-cli --v3` solo en la sesión
que necesite los agentes del kit. Revisa los JSON antiguos con
`kiro-cli agent upgrade <directorio> --dry-run` antes de convertir.

## OpenCode: por qué no se migra a V2 nativo

OpenCode 2.x acepta el frontmatter V1 y lo traduce. Migrar el adaptador a
`permissions` nativo rompería OpenCode 1.x, que no entiende esos campos. Por eso
el kit mantiene V1 como formato común:

- OpenCode 1.x: formato nativo.
- OpenCode 2.x: compatibilidad documentada; `temperature` se ignora porque V2 no
  envía el body de request del agente.
- La ruta `agent/` sigue siendo válida; V2 también descubre `agents/`.

Si en el futuro se retira la traducción V1, el adaptador necesitará una variante
por versión y el instalador deberá elegirla. Hoy no es necesario y hacerlo
rompería instalaciones antiguas.

## Pi

Las rutas de Pi (`<agent-dir>/skills` y `<agent-dir>/prompts`) y la sustitución
`$ARGUMENTS` son estables entre 0.99 y 1.5. La actualización a 1.x es recomendable,
pero no exige cambios en los artefactos.

## Antigravity

La ruta `~/.gemini/config/` es compartida por la App y el CLI. El CLI añade dos
rutas de mayor prioridad (`~/.gemini/antigravity-cli/skills/` y
`~/.gemini/skills/`). Si tienes una skill con el mismo nombre en ambas, gana la
del CLI. El instalador no borra esas rutas ni modifica credenciales, settings,
`GEMINI.md` ni `AGENTS.md`.

## Comprobación local

```bash
python3 tools/host_compat.py --matrix
python3 tools/host_compat.py --check kiro
python3 tools/host_compat.py --check opencode
python3 tools/host_compat.py --check pi
```

`--strict` convierte un aviso de incompatibilidad en código de salida distinto de
cero. Los instaladores lo usan solo para Kiro cuando se pasa `--strict-host`.
En `--dry-run` se omite la detección de versión: algunos hosts crean estado local
incluso al responder `--version`, y el dry-run no debe escribir nada.

## Referencias oficiales

- [OpenCode: agents](https://opencode.ai/docs/agents/), [skills](https://opencode.ai/docs/skills/) y [migración V1→V2](https://opencode.ai/docs/migrate-v1/)
- [Kiro: configuración de agentes](https://kiro.dev/docs/custom-agents/configuration-reference/), [skills](https://kiro.dev/docs/skills/), [CLI V3](https://kiro.dev/docs/cli/v3/) y [referencia 2.x](https://kiro.dev/docs/cli/2x-reference/)
- [Claude Code: subagentes](https://code.claude.com/docs/en/sub-agents) y [skills](https://code.claude.com/docs/en/skills)
- [GitHub Copilot: custom agents](https://docs.github.com/en/copilot/reference/custom-agents-configuration) y [agent skills](https://docs.github.com/en/copilot/concepts/customizations/agent-skills)
- [VS Code: custom agent file reference](https://code.visualstudio.com/docs/agents/reference/custom-agent-file-reference)
- [Pi: configuración](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/configuration.md), [skills](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md) y [prompt templates](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/prompt-templates.md)
- [Antigravity: skills](https://antigravity.google/docs/skills/), [subagentes](https://antigravity.google/docs/subagents/) y [discovery](https://antigravity.google/docs/customization-discovery/)
