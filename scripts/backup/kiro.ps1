<#
.SYNOPSIS
    Importa los artefactos declarados de Kiro para revisión.
.DESCRIPTION
    No modifica canonical/, adapters/ ni generated/. Guarda una instantánea scoped
    en imports\kiro\ para que sus cambios se revisen y promocionen explícitamente.
#>
[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot  = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$KiroHome = Join-Path $env:USERPROFILE ".kiro"
$args = @("$RepoRoot\tools\import_installed.py", "kiro", "--skills-dir", (Join-Path $KiroHome "skills"), "--agents-dir", (Join-Path $KiroHome "agents"))
if ($DryRun) { $args += "--dry-run" }
& python @args
