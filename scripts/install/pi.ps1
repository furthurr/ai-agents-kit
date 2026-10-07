<#
.SYNOPSIS
    Instala las skills y agentes de este repo en Pi (Windows).

.DESCRIPTION
    Equivalente en PowerShell de install-pi.sh. Pi descubre skills desde
    <agent-dir>\skills\ y prompt templates desde <agent-dir>\prompts\.
    El directorio se toma de $env:PI_CODING_AGENT_DIR o %USERPROFILE%\.pi\agent.

        generated\pi\skills\  ->  <agent-dir>\skills\
        generated\pi\agents\  ->  <agent-dir>\prompts\

    Los artefactos se generan desde canonical\ y adapters\pi\ mediante
    tools\render.py. No se instalan fuentes editables ni overlays.

    Antes de sobrescribir, respalda lo existente (salvo -Force).

.PARAMETER Force
    Sobrescribe sin crear backup previo.

.PARAMETER DryRun
    Muestra lo que haria, sin copiar nada.

.EXAMPLE
    .\install-pi.ps1
    .\install-pi.ps1 -Force
    .\install-pi.ps1 -DryRun
#>
[CmdletBinding()]
param(
    [switch]$Force,
    [switch]$DryRun,
    [Alias("migrate-retired-agents")][switch]$MigrateRetiredAgents,
    [Alias("approve-retired-file")][string[]]$ApproveRetiredFile = @(),
    [Alias("approve-retired-sha256")][string[]]$ApproveRetiredSha256 = @(),
    [Alias("additional-agents-dest")][string[]]$AdditionalAgentsDest = @()
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot  = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"

# --- Rutas destino ---
if ($env:PI_CODING_AGENT_DIR) {
    $PiDir = $env:PI_CODING_AGENT_DIR
} else {
    $PiDir = Join-Path $env:USERPROFILE ".pi\agent"
}
$SkillsDest = Join-Path $PiDir "skills"
$AgentsDest = Join-Path $PiDir "prompts"
$BackupRoot = Join-Path $env:USERPROFILE ".pi-kit-backup\$Timestamp"

# --- Rutas origen ---
$SkillsSrc = Join-Path $RepoRoot "generated\pi\skills"
$AgentsSrc = Join-Path $RepoRoot "generated\pi\agents"

function Write-Info { param($m) Write-Host "-> $m" -ForegroundColor Blue }
function Write-Ok   { param($m) Write-Host "OK $m" -ForegroundColor Green }
function Write-Warn { param($m) Write-Host "!  $m" -ForegroundColor Yellow }
function Write-Err  { param($m) Write-Host "X  $m" -ForegroundColor Red }

# --- Preflight compartido ---
$Python = $null
foreach ($candidate in @("python", "python3")) {
    if (Get-Command $candidate -ErrorAction SilentlyContinue) { $Python = $candidate; break }
}

function Invoke-Preflight {
    param([string[]]$Arguments)
    if (-not $Python) {
        Write-Err "Se requiere Python 3 para verificar la instalacion."
        return $false
    }
    $preflight = Join-Path $RepoRoot "tools\install_preflight.py"
    & $Python $preflight --platform pi @Arguments | Out-Host
    return ($LASTEXITCODE -eq 0)
}

# --- Copia el contenido de un arbol excluyendo basura de macOS ---
function Invoke-RetiredMigration {
    param([switch]$ValidateOnly)
    if (-not $Python) { exit 1 }
    $options = @("--agents-dest", $AgentsDest, "--skills-dest", $SkillsDest, "--backup-root", (Join-Path $env:USERPROFILE ".ai-agents-kit-retired-backups"))
    if ($ValidateOnly) {
        $options += "--validate-migration"
        if ($MigrateRetiredAgents) { $options += "--migration-requested" }
    } else {
        $options += "--migrate-retired-agents"
        if ($DryRun) { $options += "--dry-run" }
    }
    foreach ($path in $ApproveRetiredFile) { $options += @("--approve-retired-file", $path) }
    foreach ($sha in $ApproveRetiredSha256) { $options += @("--approve-retired-sha256", $sha) }
    foreach ($dest in $AdditionalAgentsDest) { $options += @("--additional-agents-dest", $dest) }
    & $Python (Join-Path $RepoRoot "tools/install_preflight.py") --platform pi @options | Out-Host
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
Invoke-RetiredMigration -ValidateOnly

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

# --- Instala las skills de un directorio origen ---
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
        Write-Err "No existe $SkillsSrc"
        exit 1
    }
    Write-Info "Instalando skills -> $SkillsDest"
    if (-not $DryRun) { New-Item -ItemType Directory -Force -Path $SkillsDest | Out-Null }
    Install-SkillsFrom -Base $SkillsSrc
}

# --- Instala los agentes como prompt templates ---
function Install-Agents {
    if (-not (Test-Path -LiteralPath $AgentsSrc)) {
        Write-Err "No existe $AgentsSrc"
        exit 1
    }
    Write-Info "Instalando prompt templates -> $AgentsDest"
    if (-not $DryRun) { New-Item -ItemType Directory -Force -Path $AgentsDest | Out-Null }
    Get-ChildItem -LiteralPath $AgentsSrc -Filter "*.md" -File | ForEach-Object {
        $name = $_.Name
        $dest = Join-Path $AgentsDest $name
        if ($DryRun) {
            Write-Host "    (dry-run) template $name -> $dest"
            return
        }
        Backup-Item -Path $dest -Label "prompts"
        Copy-Item -LiteralPath $_.FullName -Destination $dest -Force
        Write-Ok "template: $name"
    }
}

Write-Host ""
Write-Host "== Instalacion de Skills y Agentes en Pi ==" -ForegroundColor White
Write-Host ""

if ($DryRun) { Write-Warn "Modo -DryRun: no se copiara nada." }
if ($Force)  { Write-Warn "Modo -Force: omite backup de sobrescritura vigente; retirada siempre con backup." }

if (-not (Invoke-Preflight @("--check-source"))) {
    Write-Err "Instalacion abortada. Regenera los artefactos: python tools\render.py"
    exit 1
}

Install-Skills
Write-Host ""
Install-Agents
Write-Host ""

if ($DryRun) {
    if ($MigrateRetiredAgents) { Invoke-RetiredMigration }
    Write-Ok "Dry-run finalizado: no se escribio nada."
    exit 0
}

if (-not (Invoke-Preflight @("--check-installed", "--skills-dest", $SkillsDest, "--agents-dest", $AgentsDest))) {
    Write-Err "La instalacion quedo incompleta; no se declara completada."
    exit 1
}

if ($MigrateRetiredAgents) { Invoke-RetiredMigration }
Write-Ok "Instalacion completada."
if (-not $Force -and (Test-Path -LiteralPath $BackupRoot)) {
    Write-Info "Backups del contenido previo en: $BackupRoot"
    Write-Info "Para restaurar: Copy-Item -Path '$BackupRoot\skills\*' -Destination '$SkillsDest' -Recurse -Force"
}
Write-Host ""
Write-Info "Reinicia Pi para que detecte las nuevas skills y comandos."
Write-Info "Skills: /skill:<nombre>  ·  Agentes: /<nombre> <tarea>"
