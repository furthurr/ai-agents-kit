<# Exporta el inventario instalado para revision; tolera instalacion parcial. #>
[CmdletBinding()]
param([switch]$DryRun)
$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Python = $null
foreach ($candidate in @("python3", "python")) {
    if (Get-Command $candidate -ErrorAction SilentlyContinue) {
        & $candidate -c 'import sys; sys.exit(sys.version_info.major != 3)' | Out-Null
        if ($LASTEXITCODE -eq 0) { $Python = $candidate; break }
    }
}
if (-not $Python) { Write-Host "Se requiere Python 3."; exit 1 }
$arguments = @("antigravity", "--skills-dir", (Join-Path $env:USERPROFILE ".gemini/config/skills"),
    "--agents-dir", (Join-Path $env:USERPROFILE ".gemini/config/agents"))
if ($DryRun) { $arguments += "--dry-run" }
try {
    & $Python (Join-Path $RepoRoot "tools/import_installed.py") @arguments
    $code = $LASTEXITCODE
    exit $code
} catch {
    Write-Host "Exportacion fallida: $_"
    exit 1
}
