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
$KiroHome = Join-Path $env:USERPROFILE ".kiro"
$args = @("$ScriptDir\tools\import_installed.py", "kiro", "--skills-dir", (Join-Path $KiroHome "skills"), "--agents-dir", (Join-Path $KiroHome "agents"))
if ($DryRun) { $args += "--dry-run" }
& python @args
