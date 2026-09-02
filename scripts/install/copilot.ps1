<#
.SYNOPSIS
    Restaura las skills y agentes de GitHub Copilot en Windows.

.DESCRIPTION
    Copia el contenido de este repositorio a las rutas globales:
        generated\copilot\skills\  ->  %USERPROFILE%\.copilot\skills\
        generated\copilot\agents\  ->  %USERPROFILE%\.copilot\agents\

    Antes de sobrescribir, hace una copia de seguridad de lo existente.

.PARAMETER Force
    Sobrescribe sin crear backup previo.

.PARAMETER DryRun
    Muestra lo que haría, sin copiar nada.

.EXAMPLE
    .\install.ps1
    .\install.ps1 -Force
    .\install.ps1 -DryRun
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
$CopilotHome = Join-Path $env:USERPROFILE ".copilot"
$SkillsDest  = Join-Path $CopilotHome "skills"
$AgentsDest  = Join-Path $CopilotHome "agents"
$BackupRoot  = Join-Path $env:USERPROFILE ".copilot-backup\$Timestamp"

function Write-Info { param($m) Write-Host "-> $m" -ForegroundColor Blue }
function Write-Ok   { param($m) Write-Host "OK $m" -ForegroundColor Green }
function Write-Warn { param($m) Write-Host "!  $m" -ForegroundColor Yellow }
function Write-Err  { param($m) Write-Host "X  $m" -ForegroundColor Red }

# --- Preflight compartido ---
# tools\install_preflight.py define que significa "instalacion completa" para los
# seis instaladores, tomando canonical\manifest.json como fuente de verdad.
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
    & $Python $preflight --platform copilot @Arguments
    return ($LASTEXITCODE -eq 0)
}

function Copy-Section {
    param(
        [string]$Src,
        [string]$Dest,
        [string]$Label
    )

    if (-not (Test-Path $Src)) {
        Write-Err "No existe el origen '$Src'."
        exit 1
    }

    Write-Info "Instalando $Label -> $Dest"

    if ($DryRun) {
        Get-ChildItem -Path $Src -Recurse -File | ForEach-Object {
            Write-Host "    (dry-run) $($_.FullName)"
        }
        return
    }

    # Backup de lo existente
    if (-not $Force -and (Test-Path $Dest) -and (Get-ChildItem -Path $Dest -Force -ErrorAction SilentlyContinue)) {
        $backupPath = Join-Path $BackupRoot $Label
        New-Item -ItemType Directory -Force -Path $backupPath | Out-Null
        Copy-Item -Path (Join-Path $Dest "*") -Destination $backupPath -Recurse -Force
        Write-Warn "Backup del contenido previo en: $backupPath"
    }

    New-Item -ItemType Directory -Force -Path $Dest | Out-Null
    Copy-Item -Path (Join-Path $Src "*") -Destination $Dest -Recurse -Force
    Write-Ok "$Label instalado."
}

Write-Host ""
Write-Host "== Restauracion de Skills y Agentes de GitHub Copilot ==" -ForegroundColor White
Write-Host ""

if ($DryRun) { Write-Warn "Modo -DryRun: no se copiara nada." }
if ($Force) { Write-Warn "Modo -Force: no se crearan backups." }

# Verificar el origen antes de tocar el destino: una instalacion incompleta es
# peor que ninguna, porque se manifiesta como un agente que ignora su alcance.
if (-not (Invoke-Preflight @("--check-source"))) {
    Write-Err "Instalacion abortada. Regenera los artefactos: python tools\render.py"
    exit 1
}

Copy-Section -Src (Join-Path $RepoRoot "generated\copilot\skills") -Dest $SkillsDest  -Label "skills"
Copy-Section -Src (Join-Path $RepoRoot "generated\copilot\agents") -Dest $AgentsDest  -Label "agents"

Write-Host ""
if ($DryRun) {
    Write-Ok "Dry-run finalizado: no se escribio nada."
    exit 0
}

if (-not (Invoke-Preflight @("--check-installed", "--skills-dest", $SkillsDest, "--agents-dest", $AgentsDest))) {
    Write-Err "La instalacion quedo incompleta; no se declara completada."
    exit 1
}

Write-Ok "Restauracion completada."
if (Test-Path $BackupRoot) {
    Write-Info "Copias de seguridad guardadas en: $BackupRoot"
    Write-Info "Para restaurar: Copy-Item -Path '$BackupRoot\skills\*' -Destination '$SkillsDest' -Recurse -Force"
}
Write-Host ""
Write-Info "Reinicia tu cliente de Copilot para que detecte los cambios."
