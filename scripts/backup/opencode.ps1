<#
.SYNOPSIS
    Importa los artefactos declarados de OpenCode para revisión.
.DESCRIPTION
    No modifica canonical/, adapters/ ni generated/. Guarda una instantánea scoped
    en imports\opencode\ para que sus cambios se revisen y promocionen explícitamente.
#>
[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot  = Split-Path -Parent (Split-Path -Parent $ScriptDir)
if ($env:XDG_CONFIG_HOME) {
    $OpencodeHome = Join-Path $env:XDG_CONFIG_HOME "opencode"
} else {
    $OpencodeHome = Join-Path $env:USERPROFILE ".config\opencode"
}
$AgentsDir = Join-Path $OpencodeHome "agent"
if (-not (Test-Path -LiteralPath $AgentsDir)) { $AgentsDir = Join-Path $OpencodeHome "agents" }
$args = @("$RepoRoot\tools\import_installed.py", "opencode", "--skills-dir", (Join-Path $OpencodeHome "skills"), "--agents-dir", $AgentsDir)
if ($DryRun) { $args += "--dry-run" }
& python @args
