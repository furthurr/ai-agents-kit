<#
.SYNOPSIS
    Importa los artefactos declarados de Pi a imports/ para revision.

.DESCRIPTION
    Equivalente en PowerShell de backup-pi.sh. Copia solo los artefactos
    declarados en canonical/manifest.json desde la instalacion local de Pi
    a imports/pi/<fecha>/ para revision manual.

.PARAMETER DryRun
    Muestra lo que haria, sin copiar nada.

.EXAMPLE
    .\backup-pi.ps1
    .\backup-pi.ps1 -DryRun
#>
[CmdletBinding()]
param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot  = Split-Path -Parent (Split-Path -Parent $ScriptDir)

if ($env:PI_CODING_AGENT_DIR) {
    $PiDir = $env:PI_CODING_AGENT_DIR
} else {
    $PiDir = Join-Path $env:USERPROFILE ".pi\agent"
}

$SkillsDir = Join-Path $PiDir "skills"
$AgentsDir = Join-Path $PiDir "prompts"

$importScript = Join-Path $RepoRoot "tools\import_installed.py"
$pyArgs = @("pi", "--skills-dir", $SkillsDir, "--agents-dir", $AgentsDir)
if ($DryRun) { $pyArgs += "--dry-run" }

$Python = $null
foreach ($candidate in @("python", "python3")) {
    if (Get-Command $candidate -ErrorAction SilentlyContinue) { $Python = $candidate; break }
}
if (-not $Python) {
    Write-Host "X  Se requiere Python 3." -ForegroundColor Red
    exit 1
}

& $Python $importScript @pyArgs
exit $LASTEXITCODE
