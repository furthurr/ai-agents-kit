<# Instala el inventario declarado; fusiona skills y conserva recursos personales. #>
[CmdletBinding()]
param([switch]$Force, [switch]$DryRun)
$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$SkillsDest = Join-Path $env:USERPROFILE ".gemini/config/skills"
$AgentsDest = Join-Path $env:USERPROFILE ".gemini/config/agents"
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$script:BackupRoot = $null
$Python = $null
foreach ($candidate in @("python3", "python")) {
    if (Get-Command $candidate -ErrorAction SilentlyContinue) {
        & $candidate -c 'import sys; sys.exit(sys.version_info.major != 3)' | Out-Null
        if ($LASTEXITCODE -eq 0) { $Python = $candidate; break }
    }
}
if (-not $Python) { Write-Host "Se requiere Python 3."; exit 1 }

function Invoke-Preflight {
    param([string[]]$Arguments)
    $output = & $Python (Join-Path $RepoRoot "tools/install_preflight.py") --platform antigravity @Arguments
    $code = $LASTEXITCODE
    foreach ($line in $output) { Write-Host $line }
    return ($code -eq 0)
}

function New-Directory {
    param([string]$Path)
    # .NET treats the path literally, including brackets and wildcard characters.
    [System.IO.Directory]::CreateDirectory($Path) | Out-Null
}

function Backup-Item {
    param([string]$Path, [string]$Section)
    if ($Force -or -not (Test-Path -LiteralPath $Path)) { return }
    if (-not $script:BackupRoot) {
        $base = Join-Path $env:USERPROFILE ".antigravity-kit-backup"
        $candidate = Join-Path $base $Timestamp
        $suffix = 0
        while (Test-Path -LiteralPath $candidate) {
            $suffix++
            $candidate = Join-Path $base "$Timestamp-$suffix"
        }
        New-Directory $candidate
        $script:BackupRoot = $candidate
    }
    $target = Join-Path $script:BackupRoot $Section
    New-Directory $target
    Copy-Item -LiteralPath $Path -Destination $target -Recurse -Force
    Write-Host "backup: $Path -> $target"
}

function Copy-Tree {
    param([string]$Src, [string]$Dest)
    New-Directory $Dest
    $full = (Get-Item -LiteralPath $Src).FullName
    foreach ($item in Get-ChildItem -LiteralPath $full -Recurse -Force) {
        $relative = $item.FullName.Substring($full.Length).TrimStart('\', '/')
        $target = Join-Path $Dest $relative
        if ($item.PSIsContainer) {
            New-Directory $target
        } else {
            New-Directory (Split-Path -Parent $target)
            if (Test-Path -LiteralPath $target -PathType Container) { throw "Destino de archivo es directorio: $target" }
            Copy-Item -LiteralPath $item.FullName -Destination $target -Force
        }
    }
}

try {
    if (-not (Invoke-Preflight -Arguments @("--check-source"))) { throw "Fuente incompleta; instalacion abortada." }
    $inventoryCode = @'
import json
import sys
from pathlib import Path
root = Path(sys.argv[1])
manifest = json.loads((root / 'canonical/manifest.json').read_text(encoding='utf-8'))
items = []
for section, names in [('skills', manifest['skills']), ('agents', manifest['agents'])]:
    for name in names:
        if section == 'agents':
            name = json.loads((root / 'adapters/antigravity/agents' / (name + '.json')).read_text(encoding='utf-8'))['filename']
        if not isinstance(name, str) or not name or name in ('.', '..') or any(c in name for c in '/\\\t\r\n'):
            raise ValueError('Nombre inseguro en inventario')
        if section == 'skills':
            canonical = root / 'canonical/skills' / name
            if not (canonical / 'SKILL.md').is_file():
                raise FileNotFoundError(f'Skill canonica ausente: {canonical}')
            for resource in canonical.rglob('*'):
                if resource.is_file():
                    source = root / 'generated/antigravity/skills' / name / resource.relative_to(canonical)
                    if not source.is_file():
                        raise FileNotFoundError(f'Recurso generado ausente: {source}')
        items.append({'section': section, 'name': name})
print(json.dumps(items))
'@
    $json = & $Python -c $inventoryCode $RepoRoot
    $code = $LASTEXITCODE
    if ($code -ne 0) { throw "No se pudo enumerar el inventario." }
    $inventory = ($json -join "`n") | ConvertFrom-Json
    foreach ($item in $inventory) {
        $src = Join-Path $RepoRoot "generated/antigravity/$($item.section)/$($item.name)"
        $destRoot = if ($item.section -eq "skills") { $SkillsDest } else { $AgentsDest }
        $dest = Join-Path $destRoot $item.name
        if ($DryRun) { Write-Host "(dry-run) $src -> $dest"; continue }
        Backup-Item -Path $dest -Section $item.section
        if ($item.section -eq "skills") {
            Copy-Tree -Src $src -Dest $dest
        } else {
            New-Directory $destRoot
            if (Test-Path -LiteralPath $dest -PathType Container) { throw "Destino de agente es directorio: $dest" }
            Copy-Item -LiteralPath $src -Destination $dest -Force
        }
    }
    if ($DryRun) { Write-Host "Dry-run finalizado: no se escribio nada."; exit 0 }
    if (-not (Invoke-Preflight -Arguments @("--check-installed", "--skills-dest", $SkillsDest, "--agents-dest", $AgentsDest))) {
        throw "Instalacion incompleta; se conservan los backups."
    }
    # Shared preflight checks entry points, not resource completeness or bytes.
    $verifyCode = @'
import json
import sys
from pathlib import Path
root, skills_dest, agents_dest = map(Path, sys.argv[1:])
manifest = json.loads((root / 'canonical/manifest.json').read_text(encoding='utf-8'))
for name in manifest['skills']:
    canonical = root / 'canonical/skills' / name
    for resource in canonical.rglob('*'):
        if resource.is_file():
            relative = resource.relative_to(canonical)
            source = root / 'generated/antigravity/skills' / name / relative
            installed = skills_dest / name / relative
            if not installed.is_file() or installed.read_bytes() != source.read_bytes():
                raise ValueError(f'Recurso instalado ausente o diferente: {installed}')
for agent_id in manifest['agents']:
    name = json.loads((root / 'adapters/antigravity/agents' / (agent_id + '.json')).read_text(encoding='utf-8'))['filename']
    source = root / 'generated/antigravity/agents' / name
    installed = agents_dest / name
    if not installed.is_file() or installed.read_bytes() != source.read_bytes():
        raise ValueError(f'Agente instalado ausente o diferente: {installed}')
'@
    $output = & $Python -c $verifyCode $RepoRoot $SkillsDest $AgentsDest
    $code = $LASTEXITCODE
    foreach ($line in $output) { Write-Host $line }
    if ($code -ne 0) { throw "Verificacion de recursos fallida; se conservan los backups." }
    Write-Host "Instalacion completada."
    if ($script:BackupRoot) { Write-Host "Backup previo de skills y agents: $script:BackupRoot" }
    exit 0
} catch {
    Write-Host "Instalacion fallida; se conservan los backups: $_"
    exit 1
}
