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
timestamped. Rutas por plataforma:

| Plataforma | Raíz de backup |
|------------|----------------|
| Copilot | `~/.copilot-backup/<AAAAMMDD-HHMMSS>/` |
| OpenCode | `~/.opencode-kit-backup/<AAAAMMDD-HHMMSS>/` |
| Kiro | `~/.kiro-kit-backup/<AAAAMMDD-HHMMSS>/` |

Dentro de cada backup, el contenido previo queda en `skills/` y `agents/`.

## Garantías del instalador

Los instaladores delegan en `tools/install_preflight.py`, que toma
`canonical/manifest.json` como fuente de verdad. De ahí se derivan tres
garantías verificadas por `tools/test_install.py`:

1. **No instalan de menos en silencio.** Si falta cualquier skill o agente
   declarado en el manifest, el script aborta con código distinto de cero
   **antes** de tocar el destino y no imprime que la instalación se completó.
   Una instalación parcial es peor que ninguna: se manifiesta como un agente que
   parece ignorar su alcance cuando en realidad falta un archivo.
2. **`--dry-run` no escribe nada.** No crea ni modifica directorios, ni siquiera
   los de destino.
3. **Verifican antes de declarar éxito.** Al terminar, comprueban que el destino
   contiene lo que el manifest declara.

Si el preflight aborta, casi siempre falta regenerar:

```bash
python3 tools/render.py
python3 tools/validate.py
```

Los instaladores también **informan** de skills o agentes presentes en el destino
que el manifest no declara (propios tuyos, o restos de una versión anterior del
kit). Solo lo informan: **nunca borran nada**, porque no hay forma fiable de
distinguir un artefacto obsoleto del kit de una skill propia. Retíralos a mano si
ya no aplican (ver *Desinstalar*).

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

## Restaurar un backup

Cada instalación sin `--force` deja el estado anterior en su raíz de backup (ver
*Destinos de instalación*). Para volver atrás, elige el backup por fecha y copia
su contenido sobre el destino. Ejemplo con Kiro:

```bash
ls ~/.kiro-kit-backup/                       # elige la marca de tiempo
BK=~/.kiro-kit-backup/20260831-120000        # ajusta a la tuya

cp -R "$BK"/skills/. ~/.kiro/skills/
cp -R "$BK"/agents/. ~/.kiro/agents/
```

Para las otras plataformas cambia la raíz de backup y el destino:

| Plataforma | Origen | Destino skills | Destino agentes |
|------------|--------|----------------|-----------------|
| Copilot | `~/.copilot-backup/<fecha>/` | `~/.copilot/skills/` | `~/.copilot/agents/` |
| OpenCode | `~/.opencode-kit-backup/<fecha>/` | `~/.config/opencode/skills/` | `~/.config/opencode/agent/` |
| Kiro | `~/.kiro-kit-backup/<fecha>/` | `~/.kiro/skills/` | `~/.kiro/agents/` |

En Windows (PowerShell):

```powershell
$BK = "$env:USERPROFILE\.kiro-kit-backup\20260831-120000"
Copy-Item -Path "$BK\skills\*" -Destination "$env:USERPROFILE\.kiro\skills" -Recurse -Force
Copy-Item -Path "$BK\agents\*" -Destination "$env:USERPROFILE\.kiro\agents" -Recurse -Force
```

Restaurar **fusiona**: recupera lo anterior, pero no elimina lo que el kit añadió
después. Si quieres partir de cero, desinstala primero y restaura luego.

## Desinstalar

Los instaladores no traen un modo de desinstalación automática: borrar en el
`HOME` del usuario es irreversible y el destino puede contener skills propias
junto a las del kit. El procedimiento es manual y explícito.

Primero revisa qué hay instalado y qué declara el manifest:

```bash
python3 tools/install_preflight.py --platform kiro --check-installed \
  --skills-dest ~/.kiro/skills --agents-dest ~/.kiro/agents
```

Lo que aparezca como *no declarado en el manifest* **no** pertenece al kit
(o es de una versión anterior): decide caso por caso.

Para retirar solo lo que el kit instaló, lista los nombres y bórralos tras
revisarlos. Con Kiro:

```bash
# 1. Ver qué se borraría (no borra nada)
python3 -c "import json;print('\n'.join(json.load(open('canonical/manifest.json'))['skills']))"

# 2. Borrar las skills del kit, una vez revisada la lista
for s in $(python3 -c "import json;print(' '.join(json.load(open('canonical/manifest.json'))['skills']))"); do
  rm -rf ~/.kiro/skills/"$s"
done

# 3. Borrar los agentes del kit
for a in ~/.kiro/agents/*.md; do echo "$a"; done   # revisa antes de borrar
```

Revisa siempre la lista del paso 1 antes de ejecutar el paso 2. Si tienes skills
propias con el mismo nombre que una del kit, respáldalas primero.

Alternativa sin borrar nada: restaura el backup previo a la primera instalación.

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
