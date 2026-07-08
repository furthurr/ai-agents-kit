# 🧠 Respaldo de Skills y Agentes — GitHub Copilot y opencode

Respaldo versionable de las **skills** y **agentes** personalizados para dos
asistentes de IA: **GitHub Copilot** y **opencode**. Clona el repo, ejecuta el
script correspondiente y tendrás exactamente la misma configuración que en tu
entorno original.

> Elige el script según el asistente que uses (`.sh` en macOS/Linux, `.ps1` en Windows):
> - `install.sh` / `install.ps1` → **GitHub Copilot** (`~/.copilot/`)
> - `install-opencode.sh` / `install-opencode.ps1` → **opencode** (`~/.config/opencode/`)

---

## 🎯 Alcance

Este respaldo cubre **únicamente skills y agentes**. Los *prompts* y *chatmodes*
de VS Code **no** forman parte de este repositorio de forma intencionada. Si lees
este proyecto (humano o IA), no lo trates como incompleto por no incluir prompts:
están fuera de alcance a propósito.

---

## 🗺️ Roadmap — soporte multi-agente

| Asistente | Estado | Carpeta | Script de instalación |
|-----------|--------|---------|------------------------|
| **GitHub Copilot** | ✅ Estable | `copilot/` | `install.sh` / `install.ps1` |
| **opencode** | ✅ Estable | `opencode/` | `install-opencode.sh` / `install-opencode.ps1` |
| Otros (Cursor, Claude, Windsurf…) | ⏳ Pendiente | — | — |

El soporte para **otros asistentes** se incorporará como **carpetas hermanas**
(`cursor/`, `claude/`…), cada una con sus propias skills y agentes y su ruta de
instalación. La estructura ya está preparada para crecer sin tocar lo existente.

---

## 📦 Contenido del respaldo

El repositorio mantiene **una base compartida** de skills y **una carpeta por
asistente** con sus adaptaciones.

### 🔷 Soporte GitHub Copilot (`copilot/`)

Instalación → `~/.copilot/skills/` y `~/.copilot/agents/`.

**Skills (8)** — todas en `copilot/skills/`. La columna **Agente** indica qué agente las orquesta:

| Skill | Propósito | Agente |
|-------|-----------|--------|
| **architecture** | Documenta y mantiene la arquitectura (arc42 + C4 en Mermaid + ADRs) en `.architecture/` | Architecture Agent |
| **code-quality** | Audita buenas prácticas y calidad de código (basado en SonarQube) en `.quality/` | Code Quality Agent |
| **data-api** | Documenta datos y APIs: endpoints, DTOs, contratos, ER en `.data/` | Data & API Agent |
| **git-commit** | Crea commits Conventional Commits en español y push con confirmación | Git & Release Manager |
| **release-management** | Releases: versionado SemVer, tags y CHANGELOG | Git & Release Manager |
| **sdd-spec** | Spec-Driven Development estilo Kiro (requirements/design/tasks/verification) | SDD |
| **security** | Auditoría de seguridad móvil (OWASP MASVS/MASTG/MASWE) en `.security/` | Security Agent |
| **ui-design** | Documenta y estandariza el sistema visual/design system en `.design/` | UI Design Agent |

> Son **8 skills** pero **7 agentes**: `git-commit` y `release-management` las
> orquesta un único agente, **Git & Release Manager**.

**Agentes (7)** — en `copilot/agents/`, formato `.agent.md` (frontmatter
`tools:` + `argument-hint` propio de Copilot):

| Archivo | Agente |
|---------|--------|
| `architecture.agent.md` | Architecture Agent |
| `code-quality.agent.md` | Code Quality Agent |
| `data-api.agent.md` | Data & API Agent |
| `git-release-manager.agent.md` | Git & Release Manager |
| `sdd.agent.md` | SDD (Spec-Driven Development) |
| `security.agent.md` | Security Agent |
| `ui-design.agent.md` | UI Design Agent |

---

### 🟢 Soporte opencode (`opencode/`)

Instalación → `~/.config/opencode/skills/` y `~/.config/opencode/agent/`.

**Compatibilidad de skills**: las 8 skills de `copilot/skills/` son compatibles
con opencode sin cambios (sólo requieren `name` + `description` en el
frontmatter, que ya tienen).

**Overrides de skills (1)** — en `opencode/skills/`, sobrescriben la versión
base cuando difieren:

| Skill | Notas |
|-------|-------|
| **sdd-spec** | Variante opencode con frontmatter y formato adaptados al loader de opencode. |

**Agentes (7)** — en `opencode/agents/`, formato `.md` con frontmatter
`mode: all`, `temperature` y `permission` (en lugar de `tools:` de Copilot):

| Archivo | Agente |
|---------|--------|
| `architecture.md` | Architecture Agent |
| `code-quality.md` | Code Quality Agent |
| `data-api.md` | Data & API Agent |
| `git-release-manager.md` | Git & Release Manager |
| `sdd.md` | SDD (Spec-Driven Development) |
| `security.md` | Security Agent |
| `ui-design.md` | UI Design Agent |

> 💡 ¿Por qué hay dos carpetas de agentes? Los agentes de `copilot/agents/`
> **no** son compatibles con opencode porque declaran `tools: [...]` y
> `argument-hint` propios de GitHub Copilot. `opencode/agents/` contiene la
> versión adaptada con `mode`, `temperature` y permisos.

---

## 🗂️ Estructura del repositorio

```
.
├── copilot/                         # Soporte GitHub Copilot
│   ├── skills/                      # -> ~/.copilot/skills/  (8 skills base, compatibles con opencode)
│   │   ├── architecture/
│   │   ├── code-quality/
│   │   ├── data-api/
│   │   ├── git-commit/
│   │   ├── release-management/
│   │   ├── sdd-spec/
│   │   ├── security/
│   │   └── ui-design/
│   └── agents/                      # -> ~/.copilot/agents/  (formato Copilot: tools + argument-hint)
│       ├── architecture.agent.md
│       ├── code-quality.agent.md
│       ├── data-api.agent.md
│       ├── git-release-manager.agent.md
│       ├── sdd.agent.md
│       ├── security.agent.md
│       └── ui-design.agent.md
├── opencode/                        # Soporte opencode
│   ├── skills/                      # -> ~/.config/opencode/skills/  (overrides sobre la base copilot)
│   │   └── sdd-spec/                # override opencode de sdd-spec
│   └── agents/                      # -> ~/.config/opencode/agent/    (formato opencode: mode + temperature + permission)
│       ├── architecture.md
│       ├── code-quality.md
│       ├── data-api.md
│       ├── git-release-manager.md
│       ├── sdd.md
│       ├── security.md
│       └── ui-design.md
├── install.sh                       # Instalar soporte Copilot (macOS / Linux)
├── install.ps1                      # Instalar soporte Copilot (Windows PowerShell)
├── install-opencode.sh              # Instalar soporte opencode (macOS / Linux)
├── install-opencode.ps1             # Instalar soporte opencode (Windows PowerShell)
├── backup.sh                        # Respaldar Copilot (macOS / Linux): ~/.copilot/ -> copilot/
├── backup-opencode.sh               # Respaldar opencode (macOS / Linux): ~/.config/opencode/ -> repo
├── backup-opencode.ps1              # Respaldar opencode (Windows PowerShell)
└── README.md
```

---

## ✅ Requisitos previos

| Requisito | Para qué | Notas |
|-----------|----------|-------|
| **git** | Clonar este repositorio | Cualquier versión reciente |
| **bash** | Ejecutar `install.sh`, `install-opencode.sh`, `backup.sh`, `backup-opencode.sh` | macOS / Linux |
| **PowerShell 5+** | Ejecutar `install.ps1`, `install-opencode.ps1`, `backup-opencode.ps1` | Windows |
| **rsync** *(opcional)* | Copia de skills en opencode | Si no está, `install-opencode.sh` y `backup-opencode.sh` usan `cp` automáticamente |
| **Cliente destino** | Usar lo instalado | Ten instalado **GitHub Copilot** y/o **opencode** según el soporte que vayas a restaurar |

---

## 🚀 Restaurar en otra instancia

Elige el script según el asistente que vayas a usar. Puedes ejecutar ambos
si coexisten Copilot y opencode en la misma máquina.

### 🔷 Instalar soporte **GitHub Copilot**

**macOS / Linux:**

```bash
git clone https://github.com/furthurr/ai-agents-kit.git
cd ai-agents-kit
./install.sh
```

**Windows (PowerShell):**

```powershell
git clone https://github.com/furthurr/ai-agents-kit.git
cd ai-agents-kit
# Si PowerShell bloquea el script:
#   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install.ps1
```

> ℹ️ El repositorio es **público**: puedes clonarlo sin autenticación.

Al terminar, **reinicia tu cliente de Copilot** para que detecte los nuevos skills y agentes.

---

### 🟢 Instalar soporte **opencode**

**macOS / Linux:**

```bash
git clone https://github.com/furthurr/ai-agents-kit.git
cd ai-agents-kit
./install-opencode.sh
```

**Windows (PowerShell):**

```powershell
git clone https://github.com/furthurr/ai-agents-kit.git
cd ai-agents-kit
# Si PowerShell bloquea el script:
#   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install-opencode.ps1
```

> ℹ️ Si ejecutas opencode **dentro de WSL**, su configuración vive en el sistema de
> archivos de Linux: en ese caso usa `./install-opencode.sh` **dentro de WSL**, no
> el script de PowerShell.

Qué hace:

1. Instala las 8 skills base desde `copilot/skills/` en
   `~/.config/opencode/skills/`.
2. Aplica los overrides de `opencode/skills/` encima (p. ej. `sdd-spec`).
3. Instala los 7 agentes adaptados desde `opencode/agents/` en
   `~/.config/opencode/agent/` (opencode también acepta `agents/`).

Al terminar, **reinicia opencode** para que detecte las nuevas skills y agentes.

---

### Opciones comunes de los scripts

| Opción (sh) | Opción (ps1) | Efecto |
|-------------|--------------|--------|
| `--dry-run` | `-DryRun` | Muestra qué haría, sin copiar nada |
| `--force` | `-Force` | Sobrescribe sin crear backup previo |

> Antes de sobrescribir, los scripts crean una **copia de seguridad** de lo que
> ya tuvieras:
> - Copilot → `~/.copilot-backup/<fecha>/`
> - opencode → `~/.opencode-kit-backup/<fecha>/`

### Opción B — Pídeselo a Copilot con la URL

En tu cliente de Copilot, abre el chat y escribe algo como:

> Clona el repositorio `https://github.com/furthurr/ai-agents-kit.git` y ejecuta
> su `install.sh` para restaurar mis skills y agentes de Copilot.

---

## 🧭 Cómo usar (invocar) tras instalar

### 🔷 GitHub Copilot

- Las **skills** se cargan **automáticamente** cuando tu petición coincide con su
  `description`; no hace falta invocarlas a mano.
- Los **agentes** se invocan **mencionándolos** en el chat (p. ej. `@Architecture Agent …`)
  o eligiéndolos en el selector de agentes.

### 🟢 opencode

- Las **skills** se activan mediante la herramienta `skill` cuando la tarea coincide
  con su descripción.
- Los **agentes** se seleccionan como **agente principal** (conmutador de agentes) o
  se delegan como **subagentes** (herramienta Task); también puedes referirlos por su nombre.

> Ejemplos de disparo (ambos clientes): *"documenta la arquitectura"* → agente de
> arquitectura; *"prepara un commit"* → Git & Release Manager; *"audita seguridad"*
> → Security Agent.

---

## 🩺 Verificar y restaurar copia de seguridad

### Verificar la instalación

**Copilot** (macOS / Linux):

```bash
ls ~/.copilot/skills ~/.copilot/agents
```

**Copilot** (Windows PowerShell):

```powershell
Get-ChildItem "$env:USERPROFILE\.copilot\skills", "$env:USERPROFILE\.copilot\agents"
```

**opencode** (macOS / Linux):

```bash
ls ~/.config/opencode/skills ~/.config/opencode/agent
```

**opencode** (Windows PowerShell):

```powershell
Get-ChildItem "$env:USERPROFILE\.config\opencode\skills", "$env:USERPROFILE\.config\opencode\agent"
```

Deberías ver las carpetas de skills y los `.md` de agentes. Reinicia tu cliente y
confirma que los agentes aparecen en el selector.

### Restaurar desde una copia de seguridad

Los scripts guardan lo anterior antes de sobrescribir. Para revertir, localiza la
fecha del backup e inspecciona su contenido antes de copiarlo de vuelta:

**Copilot** (macOS / Linux):

```bash
ls ~/.copilot-backup/            # elige la carpeta <fecha>
# copia el contenido de sus subcarpetas de vuelta a ~/.copilot/skills y ~/.copilot/agents
```

**Copilot** (Windows PowerShell):

```powershell
Get-ChildItem "$env:USERPROFILE\.copilot-backup\"   # elige la carpeta <fecha>
Copy-Item "$env:USERPROFILE\.copilot-backup\<fecha>\skills\*" "$env:USERPROFILE\.copilot\skills\" -Recurse -Force
Copy-Item "$env:USERPROFILE\.copilot-backup\<fecha>\agents\*" "$env:USERPROFILE\.copilot\agents\" -Recurse -Force
```

**opencode** (macOS / Linux):

```bash
ls ~/.opencode-kit-backup/       # elige la carpeta <fecha>
cp -R ~/.opencode-kit-backup/<fecha>/skills/. ~/.config/opencode/skills/
cp -R ~/.opencode-kit-backup/<fecha>/agents/. ~/.config/opencode/agent/
```

**opencode** (Windows PowerShell):

```powershell
Get-ChildItem "$env:USERPROFILE\.opencode-kit-backup\"   # elige la carpeta <fecha>
Copy-Item "$env:USERPROFILE\.opencode-kit-backup\<fecha>\skills\*" "$env:USERPROFILE\.config\opencode\skills\" -Recurse -Force
Copy-Item "$env:USERPROFILE\.opencode-kit-backup\<fecha>\agents\*" "$env:USERPROFILE\.config\opencode\agent\"  -Recurse -Force
```

---

## 🔄 Actualizar el respaldo (cuando cambies algo)

Si creas o modificas skills/agentes en tu máquina y quieres versionarlos:

**Copilot** (macOS / Linux):

```bash
./backup.sh            # copia ~/.copilot/ hacia copilot/
git add -A
git commit -m "chore: actualizar respaldo de skills y agentes (copilot)"
git push
```

> `backup.sh` es la operación inversa de `install.sh`: sincroniza el repositorio
> con lo que tengas instalado en `~/.copilot/`. **Sólo cubre Copilot**; para opencode
> usa `backup-opencode.sh` / `backup-opencode.ps1` (más abajo).

**Copilot** (Windows PowerShell) — aún no hay `backup.ps1`; respalda manualmente:

```powershell
Copy-Item "$env:USERPROFILE\.copilot\skills\*" copilot\skills\ -Recurse -Force
Copy-Item "$env:USERPROFILE\.copilot\agents\*" copilot\agents\ -Recurse -Force
git add -A
git commit -m "chore: actualizar respaldo de skills y agentes (copilot)"
git push
```

**opencode** (macOS / Linux):

```bash
./backup-opencode.sh   # sincroniza el repo con ~/.config/opencode/
git add -A
git commit -m "chore: actualizar respaldo de skills y agentes (opencode)"
git push
```

**opencode** (Windows PowerShell):

```powershell
.\backup-opencode.ps1
git add -A
git commit -m "chore: actualizar respaldo de skills y agentes (opencode)"
git push
```

> `backup-opencode.sh` / `backup-opencode.ps1` son la operación inversa de
> `install-opencode.*` y **des-fusionan** usando el repo como referencia: cada skill
> vuelve a `copilot/skills/` (base) o a `opencode/skills/` (override) según de dónde
> saliera, y los agentes a `opencode/agents/`. Sólo respaldan lo que el kit ya conoce
> (**scoped**): las skills/agentes ajenos a este repo se listan como aviso y **no** se
> copian, y **nunca borran** nada del repo (si algo del kit ya no está instalado, sólo
> te avisan). Admiten `--dry-run` / `-DryRun` para previsualizar.

---

## 📍 Rutas por sistema operativo

### 🔷 GitHub Copilot

| Elemento | macOS | Linux | Windows |
|----------|-------|-------|---------|
| Skills | `~/.copilot/skills/` | `~/.copilot/skills/` | `%USERPROFILE%\.copilot\skills\` |
| Agentes | `~/.copilot/agents/` | `~/.copilot/agents/` | `%USERPROFILE%\.copilot\agents\` |
| Backup   | `~/.copilot-backup/<fecha>/` | `~/.copilot-backup/<fecha>/` | `%USERPROFILE%\.copilot-backup\<fecha>\` |

### 🟢 opencode

| Elemento | macOS / Linux | Windows |
|----------|---------------|---------|
| Skills | `~/.config/opencode/skills/` | `%USERPROFILE%\.config\opencode\skills\` |
| Agentes | `~/.config/opencode/agent/` (también acepta `agents/`) | `%USERPROFILE%\.config\opencode\agent\` |
| Backup   | `~/.opencode-kit-backup/<fecha>/` | `%USERPROFILE%\.opencode-kit-backup\<fecha>\` |

> opencode respeta `XDG_CONFIG_HOME`: si está definida, las rutas usan
> `$XDG_CONFIG_HOME/opencode/...` en lugar de `~/.config/opencode/...`.

---

## ⚠️ Notas

- El respaldo es **solo skills + agentes**; los prompts/chatmodes quedan fuera de alcance intencionadamente.
- Los scripts **no borran** tus skills/agentes actuales sin respaldarlos primero (salvo `--force` / `-Force`).
- La carpeta `~/.copilot/ide/` (archivos `.lock` temporales) **no** forma parte del respaldo.
- El agente **Explore** es integrado de VS Code, no requiere respaldo.
- Las skills de `copilot/skills/` son **compatibles con opencode** sin cambios; `opencode/skills/` sólo guarda los overrides necesarios.
- Los agentes de `copilot/agents/` **no** son compatibles con opencode (formato distinto): cada uno tiene su versión adaptada en `opencode/agents/`.
- **opencode** tiene instalador y respaldo en las dos plataformas (`install-opencode.sh`/`.ps1`, `backup-opencode.sh`/`.ps1`). El respaldo **des-fusiona** base/override y es *scoped*: sólo toca lo que el kit conoce y no borra nada del repo.
- **Copilot**: el respaldo automático (`backup.sh`) sólo existe para macOS/Linux; en Windows el respaldo de Copilot es manual (ver "Actualizar el respaldo").
- Revisa que ningún skill/agente contenga datos sensibles antes de hacer público el repositorio.

---

## Autor

Pedro G. V. `@furthurr`

- GitHub: https://github.com/furthurr
- Email: pedrogvas@gmail.com

## Licencia

Apache-2.0
