# Instalación

Los instaladores copian los artefactos de `generated/<plataforma>/` a las rutas
globales de cada herramienta. **No edites `generated/` a mano**: se regenera por
completo en cada render.

## Requisitos

- **Python 3** — render, validación, métricas e importación
- **Bash** (macOS/Linux) o **PowerShell** (Windows) — scripts de install/backup
- **Git** — versionar cambios del kit (recomendado)
- La herramienta destino instalada (Copilot CLI/IDE, OpenCode o Kiro)

## Flujo recomendado

Siempre en este orden:

1. Renderizar artefactos  
2. Validar paridad y reproducibilidad  
3. (Opcional) Medir coste de contexto  
4. Instalar la plataforma deseada  
5. Reiniciar Copilot, OpenCode o Kiro  

### macOS / Linux

```bash
python3 tools/render.py
python3 tools/validate.py
python3 tools/measure_context.py   # opcional

./scripts/install/copilot.sh       # GitHub Copilot
./scripts/install/opencode.sh      # OpenCode
./scripts/install/kiro.sh          # Kiro
```

### Windows (PowerShell)

```powershell
python tools/render.py
python tools/validate.py
python tools/measure_context.py    # opcional

.\scripts\install\copilot.ps1
.\scripts\install\opencode.ps1
.\scripts\install\kiro.ps1
```

Puedes instalar **varias plataformas** en la misma máquina; cada script es
independiente.

## Opciones de los instaladores

| Opción | Bash | PowerShell | Efecto |
|--------|------|------------|--------|
| Dry-run | `--dry-run` | `-DryRun` | Muestra qué haría sin copiar |
| Force | `--force` | `-Force` | Omite el backup previo de lo instalado |
| Ayuda | `-h` / `--help` | (según script) | Uso del script |

Ejemplos:

```bash
./scripts/install/opencode.sh --dry-run
./scripts/install/opencode.sh --force
```

## Destinos de instalación

| Plataforma | Skills | Agentes |
|------------|--------|---------|
| Copilot | `~/.copilot/skills/` | `~/.copilot/agents/` |
| OpenCode | `~/.config/opencode/skills/` (o `$XDG_CONFIG_HOME/opencode/skills/`) | `~/.config/opencode/agent/` |
| Kiro | `~/.kiro/skills/` | `~/.kiro/agents/` |

Antes de sobrescribir, los instaladores (salvo `--force`) crean un backup local
timestamped (p. ej. bajo `~/.opencode-kit-backup/<fecha>/` según plataforma).

## Tras instalar

1. **Reinicia** la herramienta para que cargue skills y agentes nuevos.
2. Comprueba que aparecen los agentes del [catálogo](catalogo.md).
3. Abre un proyecto de prueba y prueba una petición simple (p. ej. documentar
   arquitectura o preparar un commit en dry-run conversacional).

Detalle de uso diario: [uso.md](uso.md).

## Importar cambios hechos en la instalación local

Si editaste skills/agentes **ya instalados** en tu máquina y quieres revisarlos
sin pisar la fuente del repo:

```bash
./scripts/backup/copilot.sh --dry-run
./scripts/backup/opencode.sh --dry-run
./scripts/backup/kiro.sh --dry-run
```

En Windows: `scripts\backup\*.ps1`.

Comportamiento:

- **No sobrescriben** `canonical/` ni `adapters/`.
- Copian solo elementos declarados en el manifest a `imports/<plataforma>/<fecha>/`.
- Skills o agentes ajenos al kit se listan como aviso y **no se copian**.
- Tú decides qué promover manualmente a `canonical/` o `adapters/`.

La carpeta `imports/` está en `.gitignore` (puede contener configuración local).

Herramienta relacionada: `tools/import_installed.py` (usada por el flujo de
importación).

## Actualizar el kit

```bash
git pull
python3 tools/render.py
python3 tools/validate.py
./scripts/install/<plataforma>.sh
# reiniciar la herramienta
```

## Seguridad

- No incluyas secretos, tokens ni credenciales en fuentes, adapters, generated o
  imports.
- Revisa siempre el dry-run si no estás seguro del destino.
- Los agentes de Git/release **exigen confirmación** antes de commit, push o tag;
  eso no sustituye tu criterio al instalar en una máquina compartida.
