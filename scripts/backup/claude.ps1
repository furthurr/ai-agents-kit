<#
.SYNOPSIS
    Importa los artefactos declarados de Claude Code para revisión.
.DESCRIPTION
    No modifica canonical/, adapters/ ni generated/. Guarda una instantánea
    scoped en imports\claude\ para que sus cambios se revisen y promocionen.
#>
[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot  = Split-Path -Parent (Split-Path -Parent $ScriptDir)
if ($env:CLAUDE_CONFIG_DIR) {
    $ClaudeHome = $env:CLAUDE_CONFIG_DIR
} else {
    $ClaudeHome = Join-Path $env:USERPROFILE ".claude"
}
$args = @(
    "$RepoRoot\tools\import_installed.py",
    "claude",
    "--skills-dir",
    (Join-Path $ClaudeHome "skills"),
    "--agents-dir",
    (Join-Path $ClaudeHome "agents")
)
if ($DryRun) { $args += "--dry-run" }
& python @args
