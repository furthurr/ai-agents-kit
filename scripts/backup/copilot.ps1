<#
.SYNOPSIS
    Importa los artefactos declarados de GitHub Copilot para revisión.
.DESCRIPTION
    No modifica canonical/, adapters/ ni generated/. Guarda una instantánea scoped
    en imports\copilot\ para que sus cambios se revisen y promocionen explícitamente.
#>
[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot  = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$args = @("$RepoRoot\tools\import_installed.py", "copilot", "--skills-dir", "$env:USERPROFILE\.copilot\skills", "--agents-dir", "$env:USERPROFILE\.copilot\agents")
if ($DryRun) { $args += "--dry-run" }
& python @args
