#!/usr/bin/env python3
"""Comparativa de arneses externos sobre la tarea media-baja de Genera Android.

Cada brazo instala su arnés en un HOME/XDG de laboratorio aislado, recibe la misma
copia del proyecto y ejecuta la misma tarea con `openai/gpt-6-luna`. No toca el
HOME real durante la instalación ni el repositorio del MAS.

Ejemplos:
  python3 tools/real_android_harness_benchmark.py --install-only
  python3 tools/real_android_harness_benchmark.py --preflight
  python3 tools/real_android_harness_benchmark.py --run-only
  python3 tools/real_android_harness_benchmark.py --eval-only
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

REPO = Path(__file__).resolve().parent.parent
SPEC_DIR = REPO / 'docs/experimentos/real-android-gemini-2026-11-08'
BASE_ZIP = Path(os.environ.get("MOBILE_BENCHMARK_ANDROID_ARCHIVE",
    str(Path.home() / ".local/share/ai-agents-kit/fixtures/mobile-android.zip")))
CLI = Path.home() / '.opencode/bin/opencode'
JAVA_HOME = os.environ.get('JAVA_HOME', '/opt/homebrew/opt/openjdk@21')
ANDROID_HOME = os.environ.get('ANDROID_HOME', str(Path.home() / 'Developer/android'))

TASK_ID = '1'
GENERA_DIR = REPO / 'docs/experimentos/proyectos-arneses-comparativa/genera'
TASK = {
    'id': 'GBA-SEARCH-PROSPECTS',
    'title': 'Media-Baja — Búsqueda, Filtrado y Normalización de Prospectos (Genera)',
    'complexity': 'media-baja',
    'file': GENERA_DIR / 'tarea-1-media-baja-genera.md',
    'oracle_source': GENERA_DIR / 'OracleSearchProspectsTest.kt',
    'oracle_target': 'core/domain/src/test/java/mx/com/bancadigital/crm/domain/use_case/prospect/OracleSearchProspectsTest.kt',
    'gradle_oracle_task': ':core:domain:testReleaseUnitTest --tests "mx.com.bancadigital.crm.domain.use_case.prospect.OracleSearchProspectsTest"',
    'gradle_original_task': ':core:domain:testReleaseUnitTest --tests "mx.com.bancadigital.crm.domain.util.*"',
    'expected_paths': [
        'core/domain/src/main/java/mx/com/bancadigital/crm/domain/model/prospect/FixtureSource3.kt',
        'core/domain/src/main/java/mx/com/bancadigital/crm/domain/use_case/prospect/FixtureSource1.kt',
        'core/domain/src/test/java/mx/com/bancadigital/crm/domain/use_case/prospect/FixtureSource2.kt',
    ],
}

ARMS = ('v2_reforzado', 'wshobson', 'superpowers', 'ecc', 'gentle-ai', 'gstack', 'sdd',
        'superpowers-sdd', 'ecc-plan', 'cc-sdd', 'openspec', 'spec-kit')
DEFAULT_MODEL = 'openai/gpt-6-luna'

TIMEOUT = 1800
STEP_LIMIT = 60

SECRETS = ('*.env*', '*.pem', '*.key', '*.p12', '*.pfx', '*.jks', '*.keystore', '*credential*',
           '*.secret*', '*.p8', '*.cer', 'local.properties', 'google-services.json',
           '.secrets', '.secrets/*', '*/.ssh/*', '*/.aws/*', '*/.config/gh/*', '*/auth.json',
           '*/.npmrc', '*/.netrc', '*/.pypirc', '*antigravity-accounts*')

PROMPT_SUFFIX = (
    "\n\nPLAN TÉCNICO APROBADO POR EL USUARIO: El usuario ha aprobado formalmente el plan y la arquitectura. "
    "Estás en modo IMPLEMENTACIÓN directa tras aprobación. Implementa inmediatamente el código y los tests en los archivos requeridos "
    "usando la herramienta write o edit. Ejecuta la verificación con ./gradlew y concluye sin exploraciones innecesarias de otros módulos."
)

DELTA_A = ('Vincula los criterios afectados con pruebas o checks observables, sin casos de relleno. '
           'Cuando modifiques código compartido, contrasta con el baseline disponible el comportamiento '
           'existente que no se pidió cambiar y añade regresión para protegerlo.')
DELTA_B = ('Al reanudar, contrasta el registro con el código y las verificaciones disponibles antes de '
           'continuar; los estados guardados no sustituyen evidencia vigente. Si cambia un requisito, '
           'actualiza su literal y reabre solo el trabajo afectado.')

METHODOLOGY_PREFIXES = ('.sdd/', 'docs/superpowers/', '.claude/plans/', 'plans/',
                        '.opencode/', '.kiro/', 'openspec/', 'specs/', '.specify/')

SDD_SUFFIX = (
    "\n\nCONTEXTO DE EJECUCIÓN SDD: El usuario seleccionó explícitamente el agente `sdd` y aprueba el "
    "alcance y el plan; el Gate 3 queda cubierto por esta instrucción. Aplica la profundidad SDD "
    "proporcional que corresponda. Si el modo produce un `spec.md` (SDD-Tiny) o artefactos de Quick "
    "Plan (SDD-Lite), créalos antes de escribir el código de producto y actualízalos al cerrar con "
    "evidencia observada. No formules preguntas interactivas: no hay usuario disponible; continúa "
    "hasta dejar implementación, pruebas y verificación. Los tres archivos de producto son los "
    "indicados por la tarea; los artefactos bajo `.sdd/` son documentación del proceso SDD y no "
    "cuentan como código fuera de alcance."
)

SUPERPOWERS_SDD_SUFFIX = (
    "\n\nCONTEXTO SDD SUPERPOWERS: El usuario aprueba el alcance y el plan; implementa sin preguntas "
    "interactivas. Carga la skill `writing-plans` para producir un plan de implementación en "
    "`docs/superpowers/plans/` y después carga `subagent-driven-development` para ejecutarlo tarea por "
    "tarea con subagentes, revisión por tarea y verificación final. Los tres archivos de producto son "
    "los indicados por la tarea; el plan bajo `docs/superpowers/` es metodología y no cuenta como "
    "código fuera de alcance."
)

ECC_PLAN_SUFFIX = (
    "\n\nCONTEXTO PLAN ECC: El usuario aprueba el alcance y el plan; no formules preguntas "
    "interactivas. Antes de escribir código, invoca la herramienta `task` con `subagent_type: planner` "
    "para que el planificador ECC produzca un plan de implementación con fases, archivos y pruebas. "
    "Después implementa ese plan en el workspace, ejecuta `./gradlew :core:domain:testReleaseUnitTest` "
    "y verifica. Los tres archivos de producto son los indicados por la tarea; cualquier plan escrito "
    "bajo `docs/` o `.claude/plans/` es metodología y no cuenta como código fuera de alcance."
)

CC_SDD_SUFFIX = (
    "\n\nCONTEXTO CC-SDD: El usuario aprobó el alcance y el plan; no formules preguntas "
    "interactivas. Carga la skill `kiro-spec-quick` y ejecútala en modo `--auto` para generar "
    "`requirements.md`, `design.md` y `tasks.md`; marca las aprobaciones del `spec.json` como "
    "aprobadas por el usuario. Después carga `kiro-impl` para implementar las tareas y verifica con "
    "`./gradlew :core:domain:testReleaseUnitTest`. Los tres archivos de producto son los indicados; "
    "los artefactos bajo `.kiro/` y `.opencode/` son metodología y no cuentan como código fuera de "
    "alcance."
)

OPENSPEC_SUFFIX = (
    "\n\nCONTEXTO OPENSPEC: El usuario aprobó el alcance y el plan; no formules preguntas "
    "interactivas. Carga la skill `openspec-propose` para crear el cambio con proposal, specs, "
    "design y tasks; después carga `openspec-apply-change` para implementar las tareas. Usa la CLI "
    "`openspec` solo en local para leer/escribir el cambio; no publiques issues ni uses red. "
    "Verifica con `./gradlew :core:domain:testReleaseUnitTest`. Los tres archivos de producto son "
    "los indicados; los artefactos bajo `openspec/` son metodología."
)

SPEC_KIT_SUFFIX = (
    "\n\nCONTEXTO SPEC KIT: El usuario aprobó el alcance y el plan; no formules preguntas "
    "interactivas. Sigue el flujo Spec Kit leyendo y aplicando en orden los comandos "
    "`.opencode/commands/speckit.specify.md`, `speckit.plan.md`, `speckit.tasks.md` y "
    "`speckit.implement.md`. Usa la CLI `specify` solo en local; no publiques issues ni uses red. "
    "Verifica con `./gradlew :core:domain:testReleaseUnitTest`. Los tres archivos de producto son "
    "los indicados; los artefactos bajo `specs/` y `.specify/` son metodología."
)


def reinforce(text: str) -> str:
    """Reproduce los dos refuerzos del snapshot v2_reforzado histórico."""
    lines = text.splitlines()
    for heading, delta in (('- **Comprobar.**', DELTA_A), ('- **Continuidad bajo demanda.**', DELTA_B)):
        for i, line in enumerate(lines):
            if line.startswith(heading):
                lines[i] = line + ' ' + delta
                break
    return '\n'.join(lines) + '\n'



def now_stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, data, exclusive: bool = False):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x' if exclusive else 'w', encoding='utf-8') as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write('\n')


def read_json(path: Path):
    with path.open('r', encoding='utf-8') as handle:
        return json.load(handle)


def run(cmd, *, env=None, cwd=None, timeout=1800, log=None):
    use_shell = isinstance(cmd, str)
    started = time.monotonic()
    proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None, env=env,
                          capture_output=True, text=True, timeout=timeout,
                          shell=use_shell)
    elapsed = round(time.monotonic() - started, 3)
    if log is not None:
        log.parent.mkdir(parents=True, exist_ok=True)
        with log.open('a', encoding='utf-8') as handle:
            handle.write(f"\n$ {' '.join(map(str, cmd))}\n")
            handle.write(proc.stdout or '')
            handle.write(proc.stderr or '')
            handle.write(f"\n[exit={proc.returncode} elapsed={elapsed}s]\n")
    return proc


# --------------------------------------------------------------------------- paths

def lab_root() -> Path:
    return Path(tempfile.gettempdir()) / 'opencode' / 'proyectos-arneses-comparativa'


def arm_dirs(root: Path, arm: str):
    task = root / f'task_{TASK_ID}'
    return {
        'task': task,
        'workspace': task / 'runs' / arm,
        'profile': task / 'profiles' / arm,
        'home': task / 'profiles' / arm / 'home',
        'config': task / 'profiles' / arm / 'home' / '.config' / 'opencode',
        'evidence': task / 'evidence',
        'logs': task / 'install-logs',
    }


# --------------------------------------------------------------------------- project

def extract_project(target: Path):
    if target.exists():
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = target.parent / f'.tmp_{target.name}_{int(time.time() * 1000)}'
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True, exist_ok=True)
    run(['unzip', '-qo', str(BASE_ZIP), '-d', str(staging)], timeout=600)
    candidates = [p for p in staging.iterdir() if p.is_dir() and not p.name.startswith('__MACOSX')]
    project = next((p for p in candidates if (p / 'settings.gradle').exists()
                    or (p / 'settings.gradle.kts').exists()), None)
    if project is None:
        raise RuntimeError(f'No Gradle project found under {staging}')
    shutil.move(str(project), str(target))
    shutil.rmtree(staging, ignore_errors=True)


def prepare_workspace(root: Path, arm: str) -> Path:
    dirs = arm_dirs(root, arm)
    for key in ('workspace', 'profile'):
        if dirs[key].exists():
            shutil.rmtree(dirs[key])
    extract_project(dirs['workspace'])
    props = dirs['workspace'] / 'local.properties'
    content = props.read_text() if props.exists() else ''
    content = re.sub(r'sdk\.dir=.*', f'sdk.dir={ANDROID_HOME}', content)
    if 'sdk.dir=' not in content:
        content = f'sdk.dir={ANDROID_HOME}\n' + content
    props.write_text(content)
    dirs['config'].mkdir(parents=True, exist_ok=True)
    return dirs['workspace']


# --------------------------------------------------------------------------- installs

def _installer_env(home: Path, config: Path, extra=None) -> dict:
    env = dict(os.environ)
    for name in list(env):
        if name.startswith('OPENCODE_CONFIG') or name == 'OPENCODE_PURE':
            env.pop(name, None)
    env.update({
        'HOME': str(home),
        'XDG_CONFIG_HOME': str(config.parent),
        'OPENCODE_CONFIG_DIR': str(config),
        'OPENCODE_DISABLE_AUTOUPDATE': '1',
        'GIT_TERMINAL_PROMPT': '0',
    })
    if extra:
        env.update(extra)
    return env


def install_wshobson(root: Path, arm: str) -> dict:
    dirs = arm_dirs(root, arm)
    src = root / '_sources' / 'wshobson-agents'
    log = dirs['logs'] / f'{arm}.log'
    gen = run(['python3', 'tools/generate.py', '--harness', 'opencode', '--all', '--prune'],
              cwd=src, log=log, timeout=900)
    inst = run(['python3', 'tools/install_opencode.py', 'install', '--force'],
               cwd=src, env=_installer_env(dirs['home'], dirs['config']), log=log, timeout=600)
    linked = len(list((dirs['config'] / 'agents').glob('*.md'))) if (dirs['config'] / 'agents').exists() else 0
    skills = len([p for p in (dirs['config'] / 'skills').iterdir() if p.is_dir()]) if (dirs['config'] / 'skills').exists() else 0
    return {'arm': arm, 'ok': gen.returncode == 0 and inst.returncode == 0,
            'generate_exit': gen.returncode, 'install_exit': inst.returncode,
            'agents': linked, 'skills': skills,
            'detail': (inst.stdout + inst.stderr)[-1200:]}


def install_superpowers(root: Path, arm: str) -> dict:
    dirs = arm_dirs(root, arm)
    src = root / '_sources' / 'superpowers'
    cfg = dirs['config']
    log = dirs['logs'] / f'{arm}.log'
    try:
        dest = cfg / 'superpowers'
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src / 'skills', dest / 'skills')
        plugin_dest = dest / '.opencode' / 'plugins' / 'superpowers.js'
        plugin_dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src / '.opencode' / 'plugins' / 'superpowers.js', plugin_dest)
        (cfg / 'plugins').mkdir(parents=True, exist_ok=True)
        link = cfg / 'plugins' / 'superpowers.js'
        if link.exists() or link.is_symlink():
            link.unlink()
        link.symlink_to(plugin_dest)
        skills = len([p for p in (dest / 'skills').iterdir() if p.is_dir()])
        ok = True
        detail = f'plugin={plugin_dest} skills={skills}'
    except Exception as exc:  # noqa: BLE001
        ok, skills, detail = False, 0, repr(exc)
    with log.open('a', encoding='utf-8') as handle:
        handle.write(detail + '\n')
    return {'arm': arm, 'ok': ok, 'skills': skills, 'detail': detail}


def install_ecc(root: Path, arm: str) -> dict:
    dirs = arm_dirs(root, arm)
    src = root / '_sources' / 'ecc'
    log = dirs['logs'] / f'{arm}.log'
    build = run(['node', 'scripts/build-opencode.js'], cwd=src, log=log, timeout=600)
    inst = run(['node', 'scripts/install-apply.js', '--target', 'opencode',
                '--profile', 'developer', '--no-hooks', '--json'],
               cwd=src, env=_installer_env(dirs['home'], dirs['config']), log=log, timeout=900)
    skills = len([p for p in (dirs['config'] / 'skills').iterdir() if p.is_dir()]) if (dirs['config'] / 'skills').exists() else 0
    return {'arm': arm, 'ok': build.returncode == 0 and inst.returncode == 0,
            'build_exit': build.returncode, 'install_exit': inst.returncode,
            'skills': skills, 'detail': (inst.stdout + inst.stderr)[-1500:]}


def install_gentle_ai(root: Path, arm: str) -> dict:
    dirs = arm_dirs(root, arm)
    binary = root / '_bin' / 'gentle-ai'
    log = dirs['logs'] / f'{arm}.log'
    env = _installer_env(dirs['home'], dirs['config'], {
        'GENTLE_AI_HOME': str(dirs['profile'] / 'gentle-state'),
    })
    inst = run([str(binary), 'install', '--agents', 'opencode', '--scope', 'global',
                '--components', 'persona,skills,permissions,opencode-gentle-logo'],
               env=env, log=log, timeout=900)
    skills_root = dirs['config'] / 'skills'
    skills = len([p for p in skills_root.iterdir() if p.is_dir()]) if skills_root.exists() else 0
    return {'arm': arm, 'ok': inst.returncode == 0, 'install_exit': inst.returncode,
            'skills': skills, 'detail': (inst.stdout + inst.stderr)[-1500:]}


def install_gstack(root: Path, arm: str) -> dict:
    dirs = arm_dirs(root, arm)
    src = root / '_sources' / 'gstack'
    log = dirs['logs'] / f'{arm}.log'
    env = _installer_env(dirs['home'], dirs['config'], {
        'PATH': f"{root / '_bin' / 'bun' / 'bin'}:{os.environ.get('PATH', '')}",
    })
    inst = run([str(src / 'setup'), '--host', 'opencode', '--no-browser', '-q'],
               cwd=src, env=env, log=log, timeout=1800)
    skills_root = dirs['config'] / 'skills'
    skills = len([p for p in skills_root.iterdir() if p.is_dir()]) if skills_root.exists() else 0
    return {'arm': arm, 'ok': inst.returncode == 0, 'install_exit': inst.returncode,
            'skills': skills, 'detail': (inst.stdout + inst.stderr)[-1500:]}


def install_v2_reforzado(root: Path, arm: str) -> dict:
    """Instala el snapshot congelado del MAS (`v2_reforzado`) en su perfil aislado."""
    dirs = arm_dirs(root, arm)
    cfg = dirs['config']
    log = dirs['logs'] / f'{arm}.log'
    candidate = REPO / 'docs/experimentos/continuidad-developer-v2-refuerzos-2026-11-06/fuentes'
    skills_root = cfg / 'skills'
    skills_root.mkdir(parents=True, exist_ok=True)

    copied = []
    for domain in ('data-api', 'ui-design'):
        src = REPO / 'canonical/skills' / domain
        if src.exists():
            dest = skills_root / domain
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
            copied.append(domain)

    raw_skill = (candidate / 'SKILL-candidato2.md').read_text(encoding='utf-8')
    skill_text = reinforce(raw_skill)
    skill_text = (skill_text.replace('__SKILL__', 'developer-v2')
                  .replace('__DATA_API__', 'data-api')
                  .replace('__UI_DESIGN__', 'ui-design'))
    skill_dir = skills_root / 'developer-v2'
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / 'SKILL.md').write_text(skill_text, encoding='utf-8')

    agent_text = (candidate / 'agent-candidato2.md').read_text(encoding='utf-8')
    agent_text = agent_text.replace('__SKILL__', 'developer-v2')
    (dirs['profile'] / 'agent.md').write_text(agent_text, encoding='utf-8')

    config = {
        '$schema': 'https://opencode.ai/config.json',
        'share': 'disabled',
        'snapshot': False,
        'autoupdate': False,
        'formatter': False,
        'lsp': False,
        'plugin': [],
        'mcp': {},
        'skills': {'paths': [str(skills_root)]},
        'agent': {
            'pilot-v2_reforzado': {
                'mode': 'primary',
                'description': 'Baseline congelado v2_reforzado (MAS)',
                'prompt': agent_text,
                'steps': STEP_LIMIT,
                'temperature': 0.2,
            }
        },
        'default_agent': 'pilot-v2_reforzado',
    }
    (cfg / 'opencode.json').write_text(json.dumps(config, indent=2, ensure_ascii=False) + '\n',
                                        encoding='utf-8')
    with log.open('a', encoding='utf-8') as handle:
        handle.write(f'v2_reforzado skills={copied} skill=developer-v2 agent=pilot-v2_reforzado\n')
    return {'arm': arm, 'ok': True, 'skills': len(copied) + 1,
            'detail': f'skills={copied} skill=developer-v2 agent=pilot-v2_reforzado'}


def install_sdd(root: Path, arm: str) -> dict:
    """Instala el agente SDD y la skill `sdd-spec` del MAS en un perfil aislado."""
    dirs = arm_dirs(root, arm)
    cfg = dirs['config']
    log = dirs['logs'] / f'{arm}.log'
    skills_root = cfg / 'skills'
    skills_root.mkdir(parents=True, exist_ok=True)
    source = REPO / 'generated/opencode'

    copied = []
    for domain in ('sdd-spec', 'data-api', 'ui-design'):
        src = source / 'skills' / domain
        dest = skills_root / domain
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
        copied.append(domain)

    agent_text = (source / 'agents/sdd.md').read_text(encoding='utf-8')
    parts = agent_text.split('---', 2)
    if len(parts) == 3:
        agent_text = parts[2].lstrip('\n')
    (dirs['profile'] / 'agent.md').write_text(agent_text, encoding='utf-8')

    config = {
        '$schema': 'https://opencode.ai/config.json',
        'share': 'disabled',
        'snapshot': False,
        'autoupdate': False,
        'formatter': False,
        'lsp': False,
        'plugin': [],
        'mcp': {},
        'skills': {'paths': [str(skills_root)]},
        'agent': {
            'sdd': {
                'mode': 'primary',
                'description': 'Agente SDD del MAS (Spec-Driven Development)',
                'prompt': agent_text,
                'steps': STEP_LIMIT,
                'temperature': 0.2,
            }
        },
        'default_agent': 'sdd',
    }
    (cfg / 'opencode.json').write_text(json.dumps(config, indent=2, ensure_ascii=False) + '\n',
                                        encoding='utf-8')
    with log.open('a', encoding='utf-8') as handle:
        handle.write(f'sdd skills={copied} agent=sdd\n')
    return {'arm': arm, 'ok': True, 'skills': len(copied),
            'detail': f'skills={copied} agent=sdd'}


def install_superpowers_sdd(root: Path, arm: str) -> dict:
    """Reutiliza la instalación de superpowers; el flujo SDD se activa por prompt."""
    record = install_superpowers(root, arm)
    record = dict(record)
    record['arm'] = arm
    record['detail'] = (record.get('detail') or '') + ' | sdd=writing-plans+subagent-driven-development'
    return record


def install_ecc_plan(root: Path, arm: str) -> dict:
    """Reutiliza ECC; el plan se delega al subagente `planner` y el build implementa."""
    record = install_ecc(root, arm)
    record = dict(record)
    record['arm'] = arm
    record['detail'] = (record.get('detail') or '') + ' | plan=planner+build'
    return record


def install_cc_sdd(root: Path, arm: str) -> dict:
    """Instala las skills de cc-sdd en el workspace aislado."""
    dirs = arm_dirs(root, arm)
    log = dirs['logs'] / f'{arm}.log'
    workspace = dirs['workspace']
    stage = dirs['profile'] / 'cc-sdd-stage'
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True, exist_ok=True)
    inst = run(['npx', '--yes', 'cc-sdd@latest', '--opencode-skills', '--lang', 'es'],
               cwd=stage, log=log, timeout=900)
    ok = inst.returncode == 0
    skills = 0
    if ok:
        skills_src = stage / '.opencode' / 'skills'
        skills_dst = workspace / '.opencode' / 'skills'
        if skills_dst.exists():
            shutil.rmtree(skills_dst)
        shutil.copytree(skills_src, skills_dst)
        settings_src = stage / '.kiro' / 'settings'
        settings_dst = workspace / '.kiro' / 'settings'
        if settings_src.exists():
            if settings_dst.exists():
                shutil.rmtree(settings_dst)
            shutil.copytree(settings_src, settings_dst)
        skills = len([p for p in skills_dst.iterdir() if p.is_dir()])
        exclude = workspace / '.git' / 'info' / 'exclude'
        if exclude.parent.exists():
            current = exclude.read_text(encoding='utf-8') if exclude.exists() else ''
            additions = [line for line in ('.opencode/', '.kiro/settings/') if line not in current]
            if additions:
                exclude.write_text(current + ('\n' if current and not current.endswith('\n') else '')
                                   + '\n'.join(additions) + '\n', encoding='utf-8')
    return {'arm': arm, 'ok': ok, 'install_exit': inst.returncode, 'skills': skills,
            'detail': (inst.stdout + inst.stderr)[-1500:]}


def install_openspec(root: Path, arm: str) -> dict:
    """Inicializa OpenSpec en el workspace y deja sus skills/comandos locales."""
    dirs = arm_dirs(root, arm)
    workspace = dirs['workspace']
    log = dirs['logs'] / f'{arm}.log'
    env = {**os.environ, 'OPENSPEC_TELEMETRY': '0', 'DO_NOT_TRACK': '1'}
    inst = run(['openspec', 'init', '--tools', 'opencode', '--language', 'es', '--force'],
               cwd=workspace, env=env, log=log, timeout=600)
    skills = len([p for p in (workspace / '.opencode' / 'skills').iterdir() if p.is_dir()]) \
        if (workspace / '.opencode' / 'skills').exists() else 0
    exclude = workspace / '.git' / 'info' / 'exclude'
    if exclude.parent.exists():
        current = exclude.read_text(encoding='utf-8') if exclude.exists() else ''
        additions = [line for line in ('.opencode/', 'openspec/config.yaml',
                                       'openspec/specs/.gitkeep')
                     if line not in current]
        if additions:
            exclude.write_text(current + ('\n' if current and not current.endswith('\n') else '')
                               + '\n'.join(additions) + '\n', encoding='utf-8')
    return {'arm': arm, 'ok': inst.returncode == 0, 'install_exit': inst.returncode,
            'skills': skills, 'detail': (inst.stdout + inst.stderr)[-1500:]}


def install_spec_kit(root: Path, arm: str) -> dict:
    """Inicializa Spec Kit en el workspace con la integración OpenCode."""
    dirs = arm_dirs(root, arm)
    workspace = dirs['workspace']
    log = dirs['logs'] / f'{arm}.log'
    inst = run(['specify', 'init', '.', '--integration', 'opencode', '--force',
                '--ignore-agent-tools'], cwd=workspace, log=log, timeout=600)
    (workspace / 'specs').mkdir(exist_ok=True)
    commands = len(list((workspace / '.opencode' / 'commands').glob('speckit.*.md'))) \
        if (workspace / '.opencode' / 'commands').exists() else 0
    exclude = workspace / '.git' / 'info' / 'exclude'
    if exclude.parent.exists():
        current = exclude.read_text(encoding='utf-8') if exclude.exists() else ''
        additions = [line for line in ('.opencode/', '.specify/') if line not in current]
        if additions:
            exclude.write_text(current + ('\n' if current and not current.endswith('\n') else '')
                               + '\n'.join(additions) + '\n', encoding='utf-8')
    return {'arm': arm, 'ok': inst.returncode == 0, 'install_exit': inst.returncode,
            'skills': commands, 'detail': (inst.stdout + inst.stderr)[-1500:]}


INSTALLERS = {
    'v2_reforzado': install_v2_reforzado,
    'wshobson': install_wshobson,
    'superpowers': install_superpowers,
    'ecc': install_ecc,
    'gentle-ai': install_gentle_ai,
    'gstack': install_gstack,
    'sdd': install_sdd,
    'superpowers-sdd': install_superpowers_sdd,
    'ecc-plan': install_ecc_plan,
    'cc-sdd': install_cc_sdd,
    'openspec': install_openspec,
    'spec-kit': install_spec_kit,
}


# --------------------------------------------------------------------------- config

def strip_jsonc(text: str) -> str:
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    text = re.sub(r'(?m)^\s*//.*$', '', text)
    text = re.sub(r'(?m)//\s.*$', '', text)
    return text


def sandbox_config(workspace: Path) -> dict:
    ws = workspace.resolve()
    secrets_rules = {p: 'deny' for p in SECRETS}

    read_rules = {'*': 'deny', **secrets_rules}
    edit_rules = {'*': 'deny', **secrets_rules}
    write_rules = {'*': 'deny', **secrets_rules}

    for ws_p in (str(ws), str(workspace)):
        read_rules[ws_p] = 'allow'
        read_rules[ws_p + '/*'] = 'allow'
        edit_rules[ws_p] = 'allow'
        edit_rules[ws_p + '/*'] = 'allow'
        write_rules[ws_p] = 'allow'
        write_rules[ws_p + '/*'] = 'allow'

    for entry in ws.iterdir():
        if entry.is_symlink():
            continue
        rel = entry.name
        read_rules[rel] = 'allow'
        edit_rules[rel] = 'allow'
        write_rules[rel] = 'allow'
        if entry.is_dir():
            read_rules[rel + '/*'] = 'allow'
            edit_rules[rel + '/*'] = 'allow'
            write_rules[rel + '/*'] = 'allow'

    for p in SECRETS:
        read_rules.pop(p, None)
        edit_rules.pop(p, None)
        write_rules.pop(p, None)
        read_rules[p] = 'deny'
        edit_rules[p] = 'deny'
        write_rules[p] = 'deny'

    for ag in ('AGENTS.md', '*/AGENTS.md', str(ws / 'AGENTS.md'), str(workspace / 'AGENTS.md')):
        edit_rules.pop(ag, None)
        write_rules.pop(ag, None)
        edit_rules[ag] = 'deny'
        write_rules[ag] = 'deny'

    bash_rules = {
        '*': 'deny',
        './gradlew *': 'allow',
        './gradlew test*': 'allow',
        './gradlew :core:domain:test*': 'allow',
        './gradlew :app:test*': 'allow',
        './gradlew :core:data:test*': 'allow',
        './gradlew :core:security:test*': 'allow',
        './gradlew check*': 'allow',
        'gradlew *': 'allow',
        'git status*': 'allow',
        'git diff*': 'allow',
        'git log*': 'allow',
        'git show*': 'allow',
        'git ls-files*': 'allow',
        **secrets_rules,
    }

    return {
        'permission': {
            '*': 'deny',
            'read': read_rules,
            'edit': edit_rules,
            'write': write_rules,
            'bash': bash_rules,
            'glob': 'allow',
            'grep': 'allow',
            'list': 'allow',
            'todowrite': 'allow',
            'task': 'allow',
            'question': 'deny',
            'webfetch': 'deny',
            'websearch': 'deny',
            'google_search': 'deny',
            'lsp': 'deny',
            'external_directory': {
                '*': 'deny',
                str(ws): 'allow',
                str(ws) + '/*': 'allow',
                str(workspace): 'allow',
                str(workspace) + '/*': 'allow',
            },
        },
        'share': 'disabled',
        'snapshot': False,
        'autoupdate': False,
        'formatter': False,
        'lsp': False,
    }


def merge_sandbox(workspace: Path, config_dir: Path, arm: str | None = None) -> dict:
    json_path = config_dir / 'opencode.json'
    jsonc_path = config_dir / 'opencode.jsonc'
    base = {}
    if jsonc_path.exists() and not json_path.exists():
        base = json.loads(strip_jsonc(jsonc_path.read_text()))
        jsonc_path.rename(jsonc_path.with_suffix('.jsonc.original'))
    elif json_path.exists():
        try:
            base = json.loads(json_path.read_text())
        except json.JSONDecodeError:
            base = {}

    sandbox = sandbox_config(workspace)
    merged = dict(base)
    merged.update({k: v for k, v in sandbox.items() if k != 'permission'})

    permission = dict(base.get('permission') or {})
    sandbox_perm = sandbox['permission']
    for key, value in sandbox_perm.items():
        if key == 'external_directory':
            current = dict(permission.get('external_directory') or {})
            current.update(value)
            permission['external_directory'] = current
        else:
            permission[key] = value
    # OpenCode evaluates the wildcard rule in insertion order. If it lands last it
    # overrides the explicit read/edit/write allowances and hides file tools, so
    # keep it first for every arm.
    if '*' in permission:
        wildcard = permission.pop('*')
        permission = {'*': wildcard, **permission}
    merged['permission'] = permission

    merged.setdefault('default_agent', 'build')
    agent_cfg = dict(merged.get('agent') or {})
    build = dict(agent_cfg.get('build') or {})
    build.setdefault('mode', 'primary')
    build['steps'] = STEP_LIMIT
    agent_cfg['build'] = build
    merged['agent'] = agent_cfg
    merged['mcp'] = {}
    merged.setdefault('share', 'disabled')

    if arm == 'superpowers-sdd':
        agent_cfg['pilot-superpowers-sdd'] = {
            'mode': 'primary',
            'description': 'Piloto SDD de superpowers (writing-plans + subagent-driven-development)',
            'prompt': (
                'Eres el piloto SDD de superpowers. El usuario aprobó el alcance y el plan. '
                'Antes de tocar código, carga la skill `writing-plans` con la herramienta skill y '
                'crea el plan de implementación; después carga `subagent-driven-development` y '
                'ejecútalo con subagentes. No implementes inline ni omitas esas skills. '
                'Verifica con ./gradlew al cerrar.'
            ),
            'steps': STEP_LIMIT,
        }
        merged['agent'] = agent_cfg
        merged['default_agent'] = 'pilot-superpowers-sdd'

    if arm in ('v2_reforzado', 'sdd'):
        skills_dir = config_dir / 'skills'
        allowed = (('developer-v2', 'data-api', 'ui-design') if arm == 'v2_reforzado'
                   else ('sdd-spec', 'data-api', 'ui-design'))
        permission['skill'] = {'*': 'deny', **{name: 'allow' for name in allowed}}
        read_rules = dict(permission.get('read') or {})
        read_rules[str(skills_dir)] = 'allow'
        read_rules[str(skills_dir) + '/*'] = 'allow'
        read_rules[str(skills_dir) + '/**'] = 'allow'
        for sub in ('sdd-spec', 'sdd-spec/references', 'data-api', 'data-api/references',
                    'ui-design', 'ui-design/references'):
            read_rules[f'{skills_dir}/{sub}'] = 'allow'
            read_rules[f'{skills_dir}/{sub}/*'] = 'allow'
        profile_home = config_dir.parent.parent
        for base in {str(profile_home), str(profile_home).replace('/private/var', '/var')}:
            read_rules[base] = 'allow'
            read_rules[base + '/*'] = 'allow'
            read_rules[base + '/**'] = 'allow'
        permission['read'] = read_rules
        external = dict(permission.get('external_directory') or {})
        external[str(skills_dir)] = 'allow'
        external[str(skills_dir) + '/*'] = 'allow'
        external[str(skills_dir) + '/**'] = 'allow'
        for sub in ('sdd-spec', 'sdd-spec/references', 'data-api', 'data-api/references',
                    'ui-design', 'ui-design/references'):
            external[f'{skills_dir}/{sub}'] = 'allow'
            external[f'{skills_dir}/{sub}/*'] = 'allow'
        for base in {str(profile_home), str(profile_home).replace('/private/var', '/var')}:
            external[base] = 'allow'
            external[base + '/*'] = 'allow'
            external[base + '/**'] = 'allow'
        permission['external_directory'] = external
        merged['skills'] = {'paths': [str(skills_dir)]}
    elif arm in ('superpowers-sdd', 'ecc-plan'):
        skills_dir = config_dir / ('superpowers/skills' if arm == 'superpowers-sdd' else 'skills')
        read_rules = dict(permission.get('read') or {})
        external = dict(permission.get('external_directory') or {})
        for base in (str(skills_dir), str(skills_dir).replace('/private/var', '/var')):
            read_rules[base] = 'allow'
            read_rules[base + '/*'] = 'allow'
            read_rules[base + '/**'] = 'allow'
            external[base] = 'allow'
            external[base + '/*'] = 'allow'
            external[base + '/**'] = 'allow'
        profile_home = config_dir.parent.parent
        for base in {str(profile_home), str(profile_home).replace('/private/var', '/var')}:
            read_rules[base] = 'allow'
            read_rules[base + '/*'] = 'allow'
            read_rules[base + '/**'] = 'allow'
            external[base] = 'allow'
            external[base + '/*'] = 'allow'
            external[base + '/**'] = 'allow'
        permission['read'] = read_rules
        permission['external_directory'] = external
        permission['skill'] = 'allow'
        merged['skills'] = {'paths': [str(skills_dir)]}
    elif arm == 'cc-sdd':
        permission['skill'] = 'allow'
        merged['skills'] = {'paths': [str(workspace / '.opencode' / 'skills')]}
        agent_cfg['pilot-cc-sdd'] = {
            'mode': 'primary',
            'description': 'Piloto cc-sdd (spec antes de código)',
            'prompt': (
                'Eres el piloto cc-sdd. El usuario aprobó el alcance y el plan. Antes de cualquier '
                'implementación, carga la skill `kiro-spec-quick` y ejecútala completa en modo `--auto`; '
                'debes crear `.kiro/specs/<feature>/requirements.md`, `design.md`, `tasks.md` y '
                '`spec.json`. No escribas código de producto hasta que exista `tasks.md`. Después carga '
                '`kiro-impl` y ejecuta las tareas. No formules preguntas interactivas.'
            ),
            'steps': STEP_LIMIT,
        }
        merged['agent'] = agent_cfg
        merged['default_agent'] = 'pilot-cc-sdd'
    elif arm == 'openspec':
        permission['skill'] = 'allow'
        merged['skills'] = {'paths': [str(workspace / '.opencode' / 'skills')]}
        bash_rules = dict(permission.get('bash') or {})
        bash_rules['openspec'] = 'allow'
        bash_rules['openspec *'] = 'allow'
        permission['bash'] = bash_rules
        agent_cfg['pilot-openspec'] = {
            'mode': 'primary',
            'description': 'Piloto OpenSpec (propose + apply)',
            'prompt': (
                'Eres el piloto OpenSpec. El usuario aprobó el alcance y el plan. Carga la skill '
                '`openspec-propose` y crea el cambio con proposal/specs/design/tasks; después carga '
                '`openspec-apply-change` y ejecuta las tareas. No formules preguntas interactivas; '
                'no publiques issues ni uses red. Verifica con ./gradlew.'
            ),
            'steps': STEP_LIMIT,
        }
        merged['agent'] = agent_cfg
        merged['default_agent'] = 'pilot-openspec'
    elif arm == 'spec-kit':
        bash_rules = dict(permission.get('bash') or {})
        for pattern in ('specify', 'specify *', 'bash .specify/scripts/*',
                        'python3 .specify/scripts/*'):
            bash_rules[pattern] = 'allow'
        permission['bash'] = bash_rules
        agent_cfg['pilot-spec-kit'] = {
            'mode': 'primary',
            'description': 'Piloto Spec Kit (specify → plan → tasks → implement)',
            'prompt': (
                'Eres el piloto Spec Kit. El usuario aprobó el alcance y el plan. Sigue en orden los '
                'comandos `.opencode/commands/speckit.specify.md`, `plan.md`, `tasks.md` e '
                '`implement.md`; antes de escribir código debes crear y dejar evidencia de '
                '`specs/<feature>/spec.md`, `plan.md` y `tasks.md`. Si no existen esos artefactos, no '
                'implementes. No formules preguntas interactivas; no publiques issues ni uses red. '
                'Verifica con ./gradlew.'
            ),
            'steps': STEP_LIMIT,
        }
        merged['agent'] = agent_cfg
        merged['default_agent'] = 'pilot-spec-kit'

    json_path.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + '\n')
    if jsonc_path.exists():
        jsonc_path.unlink()
    return merged


# --------------------------------------------------------------------------- execution

def run_env(dirs: dict, config: Path) -> dict:
    env = dict(os.environ)
    for name in list(env):
        if name.startswith('OPENCODE_CONFIG') or name == 'OPENCODE_PURE':
            env.pop(name, None)
    env.update({
        'XDG_CONFIG_HOME': str(config.parent),
        'OPENCODE_CONFIG_DIR': str(config),
        'OPENCODE_DISABLE_PROJECT_CONFIG': '1',
        'OPENCODE_DISABLE_EXTERNAL_SKILLS': '1',
        'OPENCODE_DISABLE_CLAUDE_CODE': '1',
        'OPENCODE_DISABLE_CLAUDE_CODE_SKILLS': '1',
        'OPENCODE_DISABLE_CLAUDE_CODE_PROMPT': '1',
        'OPENCODE_DISABLE_AUTOUPDATE': '1',
        'JAVA_HOME': JAVA_HOME,
        'ANDROID_HOME': ANDROID_HOME,
        'PATH': f"{JAVA_HOME}/bin:{env.get('PATH', '')}",
    })
    return env


def arm_agent(config_dir: Path) -> str:
    path = config_dir / 'opencode.json'
    if not path.exists():
        return 'build'
    try:
        return read_json(path).get('default_agent') or 'build'
    except Exception:  # noqa: BLE001
        return 'build'


def preflight_arm(root: Path, arm: str, model: str) -> dict:
    dirs = arm_dirs(root, arm)
    cfg = dirs['config']
    env = run_env(dirs, cfg)
    agent = arm_agent(cfg)
    out = {'agent': agent}
    for name, cmd in (
        ('config', [str(CLI), 'debug', 'config']),
        ('skills', [str(CLI), 'debug', 'skill']),
        ('agent_default', [str(CLI), 'debug', 'agent', agent]),
        ('paths', [str(CLI), 'debug', 'paths']),
    ):
        proc = run(cmd, cwd=dirs['workspace'], env=env, timeout=120)
        out[name] = {'exit': proc.returncode,
                     'stdout': proc.stdout[-12000:],
                     'stderr': proc.stderr[-4000:]}
    record = {'arm': arm, 'model': model, 'checked_at': now_stamp(), **out}
    write_json(dirs['evidence'] / f'{arm}-preflight.json', record)
    return record


def prompt_for(arm: str) -> str:
    prompt = TASK['file'].read_text(encoding='utf-8') + PROMPT_SUFFIX
    if arm == 'sdd':
        prompt += SDD_SUFFIX
    elif arm == 'superpowers-sdd':
        prompt += SUPERPOWERS_SDD_SUFFIX
    elif arm == 'ecc-plan':
        prompt += ECC_PLAN_SUFFIX
    elif arm == 'cc-sdd':
        prompt += CC_SDD_SUFFIX
    elif arm == 'openspec':
        prompt += OPENSPEC_SUFFIX
    elif arm == 'spec-kit':
        prompt += SPEC_KIT_SUFFIX
    return prompt


def execute_arm(root: Path, arm: str, model: str) -> dict:
    dirs = arm_dirs(root, arm)
    workspace = dirs['workspace']
    cfg = dirs['config']
    prompt = prompt_for(arm)

    args = [str(CLI), 'run', '--format', 'json',
            '--title', f"HARNESS-{TASK_ID}-{arm}",
            '--model', model,
            '--agent', arm_agent(cfg),
            '--dir', str(workspace),
            prompt]

    started = time.monotonic()
    stderr_path = dirs['evidence'] / f'{arm}-stderr.log'
    stderr_path.parent.mkdir(parents=True, exist_ok=True)
    with stderr_path.open('w', encoding='utf-8') as stderr_file:
        proc = subprocess.Popen(args, cwd=str(workspace), env=run_env(dirs, cfg),
                                stdout=subprocess.PIPE, stderr=stderr_file, text=True)

        events = []
        tokens = {'total': 0, 'input': 0, 'output': 0, 'reasoning': 0, 'cache_read': 0, 'cache_write': 0}
        tools_called = 0
        steps = 0
        stop_reason = None
        error = None

        events_path = dirs['evidence'] / f'{arm}-events.jsonl'
        with events_path.open('w', encoding='utf-8') as raw:
            try:
                for line in proc.stdout:
                    line = line.strip()
                    if not line:
                        continue
                    raw.write(line + '\n')
                    try:
                        ev = json.loads(line)
                    except Exception:  # noqa: BLE001
                        continue
                    events.append(ev)
                    etype = ev.get('type')
                    if etype == 'tool_use':
                        tools_called += 1
                    elif etype == 'step_start':
                        steps += 1
                    elif etype == 'step_finish':
                        part = ev.get('part', {})
                        toks = part.get('tokens', {})
                        for key in ('total', 'input', 'output', 'reasoning'):
                            tokens[key] += toks.get(key, 0)
                        cache = toks.get('cache', {})
                        tokens['cache_read'] += cache.get('read', 0)
                        tokens['cache_write'] += cache.get('write', 0)
                        if part.get('reason'):
                            stop_reason = part.get('reason')
                    elif etype == 'error':
                        error = ev.get('error')
                proc.wait(timeout=TIMEOUT)
            except subprocess.TimeoutExpired:
                proc.kill()
                stop_reason = 'timeout'

    elapsed = round(time.monotonic() - started, 3)
    stderr_tail = ''
    try:
        stderr_tail = stderr_path.read_text(encoding='utf-8')[-3000:]
    except OSError:
        pass
    record = {
        'task_id': TASK_ID, 'task_name': TASK['id'], 'arm': arm, 'model': model,
        'agent': arm_agent(cfg),
        'steps': steps, 'tools_called': tools_called, 'tokens': tokens,
        'duration_seconds': elapsed, 'soft_stop_reason': stop_reason,
        'error': error, 'exit_code': proc.returncode, 'completed_at': now_stamp(),
        'stderr_tail': stderr_tail,
    }
    write_json(dirs['evidence'] / f'{arm}-run.json', record)
    return record


def evaluate_arm(root: Path, arm: str) -> dict:
    dirs = arm_dirs(root, arm)
    workspace = dirs['workspace']
    env = dict(os.environ)
    env.update({'JAVA_HOME': JAVA_HOME, 'ANDROID_HOME': ANDROID_HOME,
                'PATH': f"{JAVA_HOME}/bin:{env.get('PATH', '')}"})

    target = workspace / TASK['oracle_target']
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(TASK['oracle_source'], target)
    try:
        oracle = run(f"./gradlew {TASK['gradle_oracle_task']} --console=plain",
                     cwd=workspace, env=env, timeout=600)
    finally:
        if target.exists():
            target.unlink()

    original = run(f"./gradlew {TASK['gradle_original_task']} --console=plain",
                   cwd=workspace, env=env, timeout=600)

    status = run(['git', 'status', '--porcelain', '-uall'], cwd=workspace, timeout=60).stdout
    numstat = run(['git', 'diff', '--numstat', 'HEAD'], cwd=workspace, timeout=60).stdout

    changed = [line for line in status.splitlines() if line.strip()]
    untracked = [line[3:] for line in changed if line.startswith('??')]
    untracked_lines = 0
    for path in untracked:
        candidate = workspace / path
        if candidate.is_file():
            try:
                untracked_lines += sum(1 for _ in candidate.open('rb'))
            except OSError:
                pass

    added_lines = sum(int(n) for n in re.findall(r'^(\d+)\s', numstat, flags=re.M) if n.isdigit())
    touched = [line[3:].strip() for line in changed]

    methodology_files = [p for p in touched if p.startswith(METHODOLOGY_PREFIXES)]
    methodology_lines = 0
    for path in methodology_files:
        candidate = workspace / path
        if candidate.is_file():
            try:
                methodology_lines += sum(1 for _ in candidate.open('rb'))
            except OSError:
                pass
    product_lines = max(0, untracked_lines - methodology_lines)

    record = {
        'task_id': TASK_ID, 'arm': arm,
        'oracle_pass': oracle.returncode == 0,
        'original_suite_pass': original.returncode == 0,
        'functional_acceptance': oracle.returncode == 0 and original.returncode == 0,
        'changed_files': touched,
        'changed_count': len(touched),
        'untracked_count': len(untracked),
        'untracked_lines': untracked_lines,
        'product_lines': product_lines,
        'methodology_files': methodology_files,
        'methodology_lines': methodology_lines,
        'added_lines_tracked': added_lines,
        'new_tests_found': len(re.findall(r'Test\.kt', status)),
        'out_of_scope_files': [p for p in touched
                               if not any(p.endswith(e) for e in TASK['expected_paths'])
                               and not p.startswith(METHODOLOGY_PREFIXES)],
        'diff_summary': changed[:40],
    }
    if oracle.returncode != 0:
        record['oracle_error'] = (oracle.stdout + '\n' + oracle.stderr)[-2000:]
    if original.returncode != 0:
        record['original_error'] = (original.stdout + '\n' + original.stderr)[-2000:]

    write_json(dirs['evidence'] / f'{arm}-eval.json', record)
    return record


def build_summary(root: Path, arms) -> dict:
    results = {}
    for arm in arms:
        dirs = arm_dirs(root, arm)
        entry = {}
        for kind in ('install', 'preflight', 'run', 'eval'):
            path = dirs['evidence'] / f'{arm}-{kind}.json'
            if path.exists():
                entry[kind] = read_json(path)
        results[arm] = entry
    return {
        'experiment': 'proyectos-arneses-comparativa',
        'task': {k: (str(v) if isinstance(v, Path) else v) for k, v in TASK.items()},
        'recorded_at': now_stamp(),
        'arms': results,
    }


def main():
    parser = argparse.ArgumentParser(description='Comparativa de arneses externos — Genera Android')
    parser.add_argument('--arms', nargs='+', default=list(ARMS))
    parser.add_argument('--model', default=DEFAULT_MODEL)
    parser.add_argument('--root', type=Path, default=None)
    parser.add_argument('--output-dir', type=Path,
                        default=REPO / 'docs/experimentos/proyectos-arneses-comparativa')
    parser.add_argument('--install-only', action='store_true')
    parser.add_argument('--preflight', action='store_true')
    parser.add_argument('--run-only', action='store_true')
    parser.add_argument('--eval-only', action='store_true')
    args = parser.parse_args()

    root = (args.root or lab_root()).resolve()
    output = args.output_dir.resolve()
    arms = list(args.arms)
    root.mkdir(parents=True, exist_ok=True)
    output.mkdir(parents=True, exist_ok=True)

    print(f"Modelo: {args.model} | Tarea: {TASK['id']} | Brazos: {', '.join(arms)}")
    print(f"Lab: {root}\nSalida: {output}")

    for arm in arms:
        dirs = arm_dirs(root, arm)
        dirs['evidence'].mkdir(parents=True, exist_ok=True)
        dirs['logs'].mkdir(parents=True, exist_ok=True)

        if not args.run_only and not args.eval_only:
            print(f"\n> Preparando proyecto aislado para {arm}")
            prepare_workspace(root, arm)
            print(f"> Instalando arnés {arm}")
            record = INSTALLERS[arm](root, arm)
            write_json(dirs['evidence'] / f'{arm}-install.json', record)
            print(f"  instalación: ok={record['ok']} skills={record.get('skills')}")
            if not record['ok']:
                print('  [aviso] la instalación falló; el brazo se marcará como no ejecutable')
                continue
            merged = merge_sandbox(dirs['workspace'], dirs['config'], arm)
            print(f"  sandbox combinado; agentes={list((merged.get('agent') or {}).keys())[:6]}")
            if args.install_only:
                continue

        if args.preflight:
            print(f"> Preflight {arm}")
            pf = preflight_arm(root, arm, args.model)
            print(f"  agente={pf['agent']} config exit={pf['config']['exit']} "
                  f"skills exit={pf['skills']['exit']} agent exit={pf['agent_default']['exit']}")

        if args.install_only or args.preflight:
            summary = build_summary(root, arms)
            write_json(output / 'resultados.json', summary)
            continue

        if not args.eval_only:
            print(f"> Ejecutando {arm} con {args.model}")
            runrec = execute_arm(root, arm, args.model)
            print(f"  {runrec['duration_seconds']}s | {runrec['tokens']['total']} tokens | "
                  f"{runrec['steps']} pasos | stop={runrec['soft_stop_reason']} | exit={runrec['exit_code']}")

        print(f"> Evaluando {arm}")
        ev = evaluate_arm(root, arm)
        print(f"  oráculo={ev['oracle_pass']} suite={ev['original_suite_pass']} "
              f"aceptación={ev['functional_acceptance']} fuera_de_alcance={len(ev['out_of_scope_files'])}")

        write_json(output / 'resultados.json', build_summary(root, arms))

    summary = build_summary(root, arms)
    write_json(output / 'resultados.json', summary)
    print(f"\nResumen: {output / 'resultados.json'}")


if __name__ == '__main__':
    main()
