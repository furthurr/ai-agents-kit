<#
.SYNOPSIS
    Instala las skills y agentes de este repo en Kiro (Windows).

.DESCRIPTION
    Equivalente en PowerShell de install-kiro.sh. A diferencia de install.ps1
    (GitHub Copilot en %USERPROFILE%\.copilot\) e install-opencode.ps1 (opencode),
    este script instala en las rutas globales de Kiro:
        generated\kiro\skills\  ->  %USERPROFILE%\.kiro\skills\
        generated\kiro\agents\  ->  %USERPROFILE%\.kiro\agents\

    Los artefactos se generan desde canonical\ y adapters\kiro\ mediante
    tools\render.py. No se instalan fuentes editables ni overlays.

    Antes de sobrescribir, respalda lo existente (salvo -Force).

.PARAMETER Force
    Sobrescribe sin crear backup previo.

.PARAMETER DryRun
    Muestra lo que haria, sin copiar nada.

.EXAMPLE
    .\install-kiro.ps1
    .\install-kiro.ps1 -Force
    .\install-kiro.ps1 -DryRun
#>
[CmdletBinding()]
param(
    [switch]$Force,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot  = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"

# --- Rutas destino ---
$KiroHome   = Join-Path $env:USERPROFILE ".kiro"
$SkillsDest = Join-Path $KiroHome "skills"
$AgentsDest = Join-Path $KiroHome "agents"
$BackupRoot = Join-Path $env:USERPROFILE ".kiro-kit-backup\$Timestamp"

# --- Rutas origen ---
$SkillsSrc = Join-Path $RepoRoot "generated\kiro\skills"
$AgentsSrc = Join-Path $RepoRoot "generated\kiro\agents"

function Write-Info { param($m) Write-Host "-> $m" -ForegroundColor Blue }
function Write-Ok   { param($m) Write-Host "OK $m" -ForegroundColor Green }
function Write-Warn { param($m) Write-Host "!  $m" -ForegroundColor Yellow }

# --- Copia el contenido de un arbol excluyendo basura de macOS (.DS_Store) ---
# Fusiona sin borrar lo previo (equivalente a rsync sin --delete / cp -R).
function Copy-Tree {
    param([string]$Src, [string]$Dest)
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

# --- Respalda una ruta existente antes de sobrescribir ---
function Backup-Item {
    param([string]$Path, [string]$Label)
    if ($Force) { return }
    if (-not (Test-Path -LiteralPath $Path)) { return }
    $backupPath = Join-Path $BackupRoot $Label
    New-Item -ItemType Directory -Force -Path $backupPath | Out-Null
    Copy-Item -LiteralPath $Path -Destination $backupPath -Recurse -Force
    Write-Warn "backup: $(Split-Path $Path -Leaf) -> $backupPath"
}

# --- Instala las skills (una subcarpeta por skill) de un directorio origen ---
function Install-SkillsFrom {
    param([string]$Base)
    if (-not (Test-Path -LiteralPath $Base)) { return }
    Get-ChildItem -LiteralPath $Base -Directory | ForEach-Object {
        $name = $_.Name
        $dest = Join-Path $SkillsDest $name
        if ($DryRun) {
            Write-Host "    (dry-run) skill $name -> $dest"
            return
        }
        Backup-Item -Path $dest -Label "skills"
        Copy-Tree -Src $_.FullName -Dest $dest
        Write-Ok "skill: $name"
    }
}

# --- Instala skills generadas ---
function Install-Skills {
    if (-not (Test-Path -LiteralPath $SkillsSrc)) {
        Write-Warn "No hay skills que instalar."
        return
    }
    Write-Info "Instalando skills -> $SkillsDest"
    if (-not $DryRun) { New-Item -ItemType Directory -Force -Path $SkillsDest | Out-Null }
    Install-SkillsFrom -Base $SkillsSrc
}

# --- Instala los agentes (uno por archivo .md) ---
function Install-Agents {
    if (-not (Test-Path -LiteralPath $AgentsSrc)) {
        Write-Warn "No existe $AgentsSrc - se omiten agentes."
        return
    }
    Write-Info "Instalando agentes -> $AgentsDest"
    if (-not $DryRun) { New-Item -ItemType Directory -Force -Path $AgentsDest | Out-Null }
    Get-ChildItem -LiteralPath $AgentsSrc -Filter "*.md" -File | ForEach-Object {
        $name = $_.Name
        $dest = Join-Path $AgentsDest $name
        if ($DryRun) {
            Write-Host "    (dry-run) agente $name -> $dest"
            return
        }
        Backup-Item -Path $dest -Label "agents"
        Copy-Item -LiteralPath $_.FullName -Destination $dest -Force
        Write-Ok "agente: $name"
    }
}

Write-Host ""
Write-Host "== Instalacion de Skills y Agentes en Kiro ==" -ForegroundColor White
Write-Host ""

if ($DryRun) { Write-Warn "Modo -DryRun: no se copiara nada." }
if ($Force)  { Write-Warn "Modo -Force: no se crearan backups." }

Install-Skills
Write-Host ""
Install-Agents

Write-Host ""
Write-Ok "Instalacion completada."
if (-not $DryRun -and -not $Force -and (Test-Path -LiteralPath $BackupRoot)) {
    Write-Info "Backups del contenido previo en: $BackupRoot"
}
Write-Host ""
Write-Info "Reinicia Kiro para que detecte las nuevas skills y agentes."
