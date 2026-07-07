# 🧠 Respaldo de Skills y Agentes de GitHub Copilot

Respaldo versionable de las **skills** y **agentes** personalizados de GitHub Copilot, para poder **replicarlos de forma idéntica en cualquier otra instancia de VS Code** con un solo comando.

> Clona este repositorio en otra máquina, ejecuta el script de instalación y tendrás exactamente los mismos skills y agentes que en tu entorno original.

---

## 🎯 Alcance

Este respaldo cubre **únicamente skills y agentes**. Los *prompts* y *chatmodes* de
VS Code **no** forman parte de este repositorio de forma intencionada. Si lees este
proyecto (humano o IA), no lo trates como incompleto por no incluir prompts: están
fuera de alcance a propósito.

---

## 🗺️ Roadmap — soporte multi-agente

Hoy este repositorio da soporte a **GitHub Copilot** (carpeta `copilot/`). La
estructura está pensada para crecer: el soporte para **otros asistentes de IA**
(p. ej. Cursor, Claude, Windsurf) se incorporará como **carpetas hermanas** de
`copilot/` (`cursor/`, `claude/`…), cada una con sus propias skills y agentes y
su ruta de instalación. Mientras tanto, todo lo documentado aquí aplica al
soporte actual de **Copilot**.

---

## 📦 Contenido del respaldo

### Skills (8) — se instalan en `~/.copilot/skills/`

| Skill | Propósito |
|-------|-----------|
| **architecture** | Documenta y mantiene la arquitectura (arc42 + C4 en Mermaid + ADRs) en `.architecture/` |
| **code-quality** | Audita buenas prácticas y calidad de código (basado en SonarQube) en `.quality/` |
| **data-api** | Documenta datos y APIs: endpoints, DTOs, contratos, ER en `.data/` |
| **git-commit** | Crea commits Conventional Commits en español y push con confirmación |
| **release-management** | Releases: versionado SemVer, tags y CHANGELOG |
| **sdd-spec** | Spec-Driven Development estilo Kiro (requirements/design/tasks/verification) |
| **security** | Auditoría de seguridad móvil (OWASP MASVS/MASTG/MASWE) en `.security/` |
| **ui-design** | Documenta y estandariza el sistema visual/design system en `.design/` |

### Agentes (7) — se instalan en `~/.copilot/agents/`

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

## 🗂️ Estructura del repositorio

```
.
├── copilot/
│   ├── skills/          # -> ~/.copilot/skills/
│   │   ├── architecture/
│   │   ├── code-quality/
│   │   ├── data-api/
│   │   ├── git-commit/
│   │   ├── release-management/
│   │   ├── sdd-spec/
│   │   ├── security/
│   │   └── ui-design/
│   └── agents/          # -> ~/.copilot/agents/
│       └── *.agent.md
├── install.sh           # Restaurar en macOS / Linux
├── install.ps1          # Restaurar en Windows (PowerShell)
├── backup.sh            # Actualizar este repo desde tu entorno actual
└── README.md
```

---

## 🚀 Restaurar en otra instancia de VS Code

### Opción A — Script (recomendada)

**macOS / Linux:**

```bash
git clone <URL-DE-TU-REPOSITORIO>
cd <TU-REPO>
./install.sh
```

**Windows (PowerShell):**

```powershell
git clone <URL-DE-TU-REPOSITORIO>
cd <TU-REPO>
# Si PowerShell bloquea el script:
#   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install.ps1
```

> ℹ️ El repositorio es **público**: puedes clonarlo sin autenticación.

Opciones disponibles:

| Opción | Efecto |
|--------|--------|
| `--dry-run` / `-DryRun` | Muestra qué haría, sin copiar nada |
| `--force` / `-Force` | Sobrescribe sin preguntar |

> El instalador crea automáticamente una **copia de seguridad** de lo que ya tuvieras en `~/.copilot-backup/<fecha>` antes de sobrescribir.

Al terminar, **reinicia VS Code** para que detecte los nuevos skills y agentes.

### Opción B — Pídeselo a Copilot con la URL

En VS Code, abre Copilot Chat y escribe algo como:

> Clona el repositorio `<URL-DE-TU-REPOSITORIO>` y ejecuta su `install.sh` para restaurar mis skills y agentes de Copilot.

---

## 🔄 Actualizar el respaldo (cuando cambies algo)

Si creas o modificas skills/agentes en tu máquina y quieres versionarlos:

```bash
./backup.sh            # copia tu entorno actual hacia este repo
git add -A
git commit -m "chore: actualizar respaldo de skills y agentes"
git push
```

> `backup.sh` es la operación inversa de `install.sh`: sincroniza el repositorio con lo que tengas instalado globalmente.

---

## 📍 Rutas por sistema operativo

| Elemento | macOS | Linux | Windows |
|----------|-------|-------|---------|
| Skills | `~/.copilot/skills/` | `~/.copilot/skills/` | `%USERPROFILE%\.copilot\skills\` |
| Agentes | `~/.copilot/agents/` | `~/.copilot/agents/` | `%USERPROFILE%\.copilot\agents\` |

---

## ⚠️ Notas

- El respaldo es **solo skills + agentes**; los prompts/chatmodes quedan fuera de alcance intencionadamente.
- Los scripts **no borran** tus skills/agentes actuales sin respaldarlos primero.
- La carpeta `~/.copilot/ide/` (archivos `.lock` temporales) **no** forma parte del respaldo.
- El agente **Explore** es integrado de VS Code, no requiere respaldo.
- Revisa que ningún skill/agente contenga datos sensibles antes de hacer público el repositorio.
