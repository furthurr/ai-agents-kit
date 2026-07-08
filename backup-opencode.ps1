<#
.SYNOPSIS
    Actualiza este repositorio con las skills y agentes de opencode instalados (Windows).

.DESCRIPTION
    Equivalente en PowerShell de backup-opencode.sh. Operación inversa a
    install-opencode.ps1.

    La instalación FUSIONA dos orígenes en un mismo destino, así que el respaldo
    DES-FUSIONA usando el repo como referencia de qué es base y qué es override:
        <config>\opencode\skills\<name>   -> opencode\skills\<name>   (si <name> es override conocido)
                                          -> copilot\skills\<name>    (si <name> es base conocida)
        <config>\opencode\agent\<name>.md -> opencode\agents\<name>.md (si es agente conocido)

    <config> es $env:XDG_CONFIG_HOME si está definida, o %USERPROFILE%\.config en
    caso contrario (misma lógica que install-opencode.ps1).

    Alcance (scoped): SÓLO respalda lo que el kit ya conoce. Las skills/agentes que
    tengas instalados pero NO existan en el repo se listan como aviso y NO se copian.

    No borra nada del repo: si algo del kit ya no está instalado, sólo te avisa para
    que decidas con git.

.PARAMETER DryRun
    Muestra lo que haría, sin copiar nada.

.EXAMPLE
    .\backup-opencode.ps1
    .\backup-opencode.ps1 -DryRun
#>
[CmdletBinding()]
param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# --- Rutas de la instalación (origen) ---
if ($env:XDG_CONFIG_HOME) {
    $OpencodeHome = Join-Path $env:XDG_CONFIG_HOME "opencode"
} else {
    $OpencodeHome = Join-Path $env:USERPROFILE ".config\opencode"
}
$SkillsInstalled = Join-Path $OpencodeHome "skills"
$AgentsInstalled = Join-Path $OpencodeHome "agent"
if (-not (Test-Path -LiteralPath $AgentsInstalled)) {
    $alt = Join-Path $OpencodeHome "agents"                 # fallback plural
    if (Test-Path -LiteralPath $alt) { $AgentsInstalled = $alt }
}

# --- Rutas del repo (destino) ---
$BaseSkills    = Join-Path $ScriptDir "copilot\skills"
$OverlaySkills = Join-Path $ScriptDir "opencode\skills"
$AgentsRepo    = Join-Path $ScriptDir "opencode\agents"

function Write-Info { param($m) Write-Host "-> $m" -ForegroundColor Blue }
function Write-Ok   { param($m) Write-Host "OK $m" -ForegroundColor Green }
function Write-Warn { param($m) Write-Host "!  $m" -ForegroundColor Yellow }

# --- Reemplaza el contenido de una skill conocida (refleja ediciones internas) ---
function Sync-Tree {
    param([string]$Src, [string]$Dest)
    if (Test-Path -LiteralPath $Dest) { Remove-Item -LiteralPath $Dest -Recurse -Force }
    $srcFull = (Resolve-Path -LiteralPath $Src).Path
    Get-ChildItem -LiteralPath $srcFull -Recurse -Force -File |
        Where-Object { $_.Name -ne ".DS_Store" } |
        ForEach-Object {
            $rel = $_.FullName.Substring($srcFull.Length).TrimStart('\', '/')
            $target = Join-Path $Dest $rel
            $targetDir = Split-Path -Parent $target
            if (-not (Test-Path -LiteralPath $targetDir)) {
                New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
            }
            Copy-Item -LiteralPath $_.FullName -Destination $target -Force
        }
}

# --- Respaldar skills conocidas (des-fusión base/override) ---
function Backup-Skills {
    if (-not (Test-Path -LiteralPath $SkillsInstalled)) {
        Write-Warn "No existe $SkillsInstalled - no hay skills de opencode instaladas."
        return
    }
    Write-Info "Respaldando skills <- $SkillsInstalled"
    Get-ChildItem -LiteralPath $SkillsInstalled -Directory | ForEach-Object {
        $name = $_.Name
        $overlay = Join-Path $OverlaySkills $name
        $base    = Join-Path $BaseSkills $name
        if (Test-Path -LiteralPath $overlay) {
            $dest = $overlay; $kind = "override (opencode/skills)"
        } elseif (Test-Path -LiteralPath $base) {
            $dest = $base; $kind = "base (copilot/skills)"
        } else {
            Write-Warn "skill ajena al kit, se ignora: $name"
            return
        }
        if ($DryRun) {
            Write-Host "    (dry-run) skill $name -> $dest"
            return
        }
        Sync-Tree -Src $_.FullName -Dest $dest
        Write-Ok "skill: $name -> $kind"
    }
    # Avisar (sin borrar) de skills del kit que ya no están instaladas
    $seen = @{}
    @(Get-ChildItem -LiteralPath $BaseSkills -Directory -ErrorAction SilentlyContinue) +
    @(Get-ChildItem -LiteralPath $OverlaySkills -Directory -ErrorAction SilentlyContinue) |
        ForEach-Object {
            if ($seen.ContainsKey($_.Name)) { return }
            $seen[$_.Name] = $true
            if (-not (Test-Path -LiteralPath (Join-Path $SkillsInstalled $_.Name))) {
                Write-Warn "en el repo pero NO instalada: $($_.Name) (no se toca)"
            }
        }
}

# --- Respaldar agentes conocidos (1:1) ---
function Backup-Agents {
    if (-not (Test-Path -LiteralPath $AgentsInstalled)) {
        Write-Warn "No existe $AgentsInstalled - no hay agentes de opencode instalados."
        return
    }
    Write-Info "Respaldando agentes <- $AgentsInstalled"
    Get-ChildItem -LiteralPath $AgentsInstalled -Filter "*.md" -File | ForEach-Object {
        $name = $_.Name
        $dest = Join-Path $AgentsRepo $name
        if (-not (Test-Path -LiteralPath $dest)) {
            Write-Warn "agente ajeno al kit, se ignora: $name"
            return
        }
        if ($DryRun) {
            Write-Host "    (dry-run) agente $name -> $dest"
            return
        }
        Copy-Item -LiteralPath $_.FullName -Destination $dest -Force
        Write-Ok "agente: $name"
    }
    # Avisar (sin borrar) de agentes del kit que ya no están instalados
    Get-ChildItem -LiteralPath $AgentsRepo -Filter "*.md" -File -ErrorAction SilentlyContinue | ForEach-Object {
        if (-not (Test-Path -LiteralPath (Join-Path $AgentsInstalled $_.Name))) {
            Write-Warn "en el repo pero NO instalado: $($_.Name) (no se toca)"
        }
    }
}

Write-Host ""
Write-Host "== Respaldo de Skills y Agentes de opencode al repositorio ==" -ForegroundColor White
Write-Host ""

if ($DryRun) { Write-Warn "Modo -DryRun: no se copiara nada." }

Backup-Skills
Write-Host ""
Backup-Agents

Write-Host ""
Write-Ok "Respaldo completado. Revisa los cambios con: git status && git diff"
