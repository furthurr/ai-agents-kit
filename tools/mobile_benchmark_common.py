#!/usr/bin/env python3
"""Controlled mobile benchmark infrastructure; never changes agent sources.

Protocol v2 writes only to a new external laboratory. Historical result files are
inputs, not output destinations. All model calls are explicit (not preflight).
"""
from __future__ import annotations

import argparse
import base64
from contextlib import contextmanager
import datetime
import fcntl
import fnmatch
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import shlex
import shutil
import signal
import stat
import subprocess
import tempfile
import time
import uuid
import xml.etree.ElementTree as ET
import zipfile

REPO = Path(__file__).resolve().parent.parent
PROTOCOL = 'mobile-benchmark-v2'
DEFAULT_MODEL = 'openai/gpt-6-luna'
ARMS = ('v2_reforzado', 'developer_actual', 'v2', 'build_mas', 'build_sin_mas')
DELTA_A = ('Vincula los criterios afectados con pruebas o checks observables, sin casos de relleno. '
           'Cuando modifiques código compartido, contrasta con el baseline disponible el comportamiento '
           'existente que no se pidió cambiar y añade regresión para protegerlo.')
DELTA_B = ('Al reanudar, contrasta el registro con el código y las verificaciones disponibles antes de '
           'continuar; los estados guardados no sustituyen evidencia vigente. Si cambia un requisito, '
           'actualiza su literal y reabre solo el trabajo afectado.')
SECRETS = ('*.env*', '*.pem', '*.key', '*.p12', '*.pfx', '*.jks', '*.keystore',
           '*.mobileprovision', '*credential*', '*.secret*', 'auth.json',
           '.npmrc', '.netrc', '.pypirc', '*antigravity-accounts*')
SKIP_DIRS = {'.git', '.gradle', 'build', 'DerivedData', '__MACOSX', '__pycache__',
             '.ssh', '.aws', 'secrets', 'node_modules', '.opencode', '.claude',
             '.gemini', '.agents', '.build', 'xcuserdata'}
MAS_DIRS = {'.architecture', '.data', '.design', '.quality', '.security', '.navigator', '.sdd'}
APPROVAL = ('El alcance descrito está autorizado para implementación y verificación. '
            'El plan técnico está aprobado; no se necesita una nueva aprobación rutinaria. '
            'No hagas commits ni publicaciones. Respeta los permisos y restricciones del host. '
            'El índice Git contiene el baseline inicial, sin commits; git diff muestra tus cambios.')
TOKEN_FORMULA = 'input + output + cache_read + cache_write + reasoning'


def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def write_json(path, value, exclusive=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x' if exclusive else 'w', encoding='utf-8') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write('\n')


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def safe_path(path):
    path = PurePosixPath(str(path))
    return not any(p in SKIP_DIRS or any(fnmatch.fnmatch(p.lower(), s) for s in SECRETS)
                   for p in path.parts)


def reinforce(text):
    lines = text.splitlines()
    for heading, delta in (('- **Comprobar.**', DELTA_A), ('- **Continuidad bajo demanda.**', DELTA_B)):
        matches = [i for i, line in enumerate(lines) if line.startswith(heading)]
        if len(matches) != 1:
            raise ValueError(f'Refuerzo no aplicable de forma inequívoca: {heading}')
        lines[matches[0]] += ' ' + delta
    return '\n'.join(lines) + '\n'


def primary_skill(arm):
    return 'developer' if arm == 'developer_actual' else 'developer-v2'


def agent_name(arm):
    return 'build' if arm.startswith('build_') else 'pilot-' + arm


def render(text):
    for token, name in (('{{mas_identity}}', 'mas-identity.md'),
                        ('{{project_context}}', 'project-context.md')):
        text = text.replace(token, (REPO / 'canonical/shared' / name).read_text().rstrip('\n'))
    if re.search(r'\{\{[^}]+\}\}|__(SKILL|DATA_API|UI_DESIGN)__', text):
        raise ValueError('Perfil con placeholders sin resolver')
    return text


def source_profile(arm):
    """Repository sources only: an installed profile must not silently override it."""
    if arm not in ARMS:
        raise ValueError(f'Brazo desconocido: {arm}')
    inputs, files = {}, {}

    def load(path):
        inputs[str(path.relative_to(REPO))] = sha(path)
        return path.read_text(encoding='utf-8')

    if arm.startswith('build_'):
        agent = ''  # Keep the runtime's native build agent, not a fabricated role.
    else:
        if arm == 'developer_actual':
            agent = render(load(REPO / 'canonical/agents/developer.md'))
        else:
            candidate = REPO / 'docs/experimentos/continuidad-developer-v2-refuerzos-2026-11-06/fuentes'
            agent = load(candidate / 'agent-candidato2.md').replace('__SKILL__', primary_skill(arm))
            skill = load(candidate / 'SKILL-candidato2.md')
            if arm == 'v2_reforzado':
                skill = reinforce(skill)
            for old, new in [('__SKILL__', primary_skill(arm)), ('__DATA_API__', 'data-api'),
                             ('__UI_DESIGN__', 'ui-design')]:
                skill = skill.replace(old, new)
            files[f'skills/{primary_skill(arm)}/SKILL.md'] = render(skill)
    if arm != 'build_sin_mas':
        domains = ['data-api', 'ui-design'] + (['developer'] if arm == 'developer_actual' else [])
        for domain in domains:
            source = REPO / 'canonical/skills' / domain
            for path in sorted(source.rglob('*')):
                if path.is_file() and not path.is_symlink() and safe_path(path.relative_to(source)):
                    if path.suffix != '.md':
                        continue  # Current required skill references are Markdown.
                    files[f'skills/{domain}/{path.relative_to(source)}'] = render(load(path))
    for name in ('mas-identity.md', 'project-context.md'):
        inputs[f'canonical/shared/{name}'] = sha(REPO / 'canonical/shared' / name)
    files['agent.md'] = render(agent)
    return {'arm': arm, 'sources': inputs, 'files': files}


def freeze_profile(profile, arm):
    definition = source_profile(arm)
    profile.mkdir(parents=True, exist_ok=False)
    for name, text in definition['files'].items():
        dest = profile / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding='utf-8')
    manifest = {'protocol': PROTOCOL, 'arm': arm, 'sources': definition['sources'],
                'files': {name: sha(profile / name) for name in definition['files']}}
    write_json(profile / 'manifest.json', manifest, exclusive=True)
    return manifest


def verify_profile(profile):
    manifest = read_json(profile / 'manifest.json')
    for name, digest in manifest['files'].items():
        if sha(profile / name) != digest:
            raise ValueError(f'Perfil congelado alterado: {name}')
    return manifest


def snapshot(workspace):
    result = {}
    for directory, dirs, names in os.walk(workspace, followlinks=False):
        base = Path(directory)
        dirs[:] = [d for d in dirs if safe_path((base / d).relative_to(workspace))
                   and not (base / d).is_symlink()]
        for name in names:
            path = base / name
            rel = path.relative_to(workspace)
            if safe_path(rel) and not path.is_symlink() and path.is_file():
                result[str(rel)] = sha(path)
    return result


def extract_project(archive, workspace, platform, arm):
    """No overwrite/traversal/credentials; preserve only safe framework links."""
    workspace.mkdir(parents=True, exist_ok=False)
    with zipfile.ZipFile(archive) as zf:
        framework_links = []
        prefix = f'app-crm-{platform}-enterprise'
        if not any(name.startswith(prefix + '/') for name in zf.namelist()):
            roots = {PurePosixPath(name).parts[0] for name in zf.namelist()
                     if PurePosixPath(name).parts and safe_path(name)}
            if len(roots) != 1:
                raise ValueError('El ZIP no tiene una raíz de proyecto inequívoca')
            prefix = roots.pop()
        for item in zf.infolist():
            path = PurePosixPath(item.filename)
            if path.is_absolute() or '..' in path.parts or '\\' in item.filename:
                raise ValueError(f'Ruta insegura en ZIP: {item.filename}')
            if not path.parts or path.parts[0] != prefix:
                continue
            rel = PurePosixPath(*path.parts[1:])
            if not rel.parts or not safe_path(rel):
                continue
            if stat.S_ISLNK(item.external_attr >> 16):
                # Versioned Apple frameworks include signed symbolic-link resources.
                # Dropping them breaks vendor signatures. Never restore arbitrary
                # project links, absolute links or links outside their own framework.
                bundles = [i for i, part in enumerate(rel.parts) if part.endswith('.framework')]
                if not bundles:
                    continue
                target_text = zf.read(item).decode('utf-8')
                target = PurePosixPath(target_text)
                if target.is_absolute() or '\\' in target_text or '\x00' in target_text:
                    raise ValueError('Enlace de framework inseguro')
                bundle = workspace.joinpath(*rel.parts[:bundles[-1] + 1])
                dest = workspace / str(rel)
                resolved = (dest.parent / target_text).resolve()
                if bundle.resolve() not in resolved.parents or not safe_path(resolved.relative_to(workspace.resolve())):
                    raise ValueError('Enlace fuera de su framework o a un archivo excluido')
                framework_links.append((dest, target_text, bundle))
                continue
            if 'local.properties' in rel.parts:
                continue  # Regenerated from the SDK path, never read from the app.
            if arm == 'build_sin_mas' and (any(p in MAS_DIRS for p in rel.parts) or
                                           rel.name in ('AGENTS.md', 'GEMINI.md')):
                continue
            dest = workspace / str(rel)
            if item.is_dir():
                dest.mkdir(parents=True, exist_ok=True)
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(zf.read(item))
                if item.external_attr >> 16 & 0o111:
                    dest.chmod(0o755)
        for dest, target, bundle in framework_links:
            resolved = (dest.parent / target).resolve()
            if bundle.resolve() not in resolved.parents:
                raise ValueError('Cadena de enlaces fuera de su framework')
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.symlink_to(target)
    return prefix


def bind_text(text, bindings):
    """Resolve anonymized fixture identifiers, never agent instructions or logic."""
    for source in sorted(bindings, key=len, reverse=True):
        text = re.sub(r'(?<!\w)' + re.escape(source) + r'(?!\w)',
                      lambda match: bindings[source], text)
    return text


def project_bindings(workspace, platform):
    bindings, runtime = {}, {}
    if platform == 'android':
        for pattern, old, suffix in [
            ('core/domain/src/main/java/**/domain/model/prospect/Prospect.kt',
             'com.example.mobilefixture', '.domain.model.prospect'),
            ('app/src/main/java/**/features/offline/buzon/AccesoBuzon.kt',
             'com.example.mobilefixture.tests1', '.features.offline.buzon')]:
            paths = list(workspace.glob(pattern))
            if len(paths) > 1:
                raise ValueError(f'Namespace ambiguo: {pattern}')
            if paths:
                package = re.search(r'^package\s+([\w.]+)', paths[0].read_text(), re.M)
                if not package or not package.group(1).endswith(suffix):
                    raise ValueError(f'No se pudo verificar el namespace de {paths[0]}')
                actual = package.group(1)[:-len(suffix)]
                bindings[old] = actual
                bindings[old.replace('.', '/')] = actual.replace('.', '/')
    else:
        projects = list(workspace.glob('**/*.xcodeproj/project.pbxproj'))
        if len(projects) != 1:
            raise ValueError('Se requiere un único proyecto Xcode identificable')
        project = projects[0]
        name = project.parent.stem
        bindings['FixtureProject'] = name
        bindings['FixtureModule'] = re.sub(r'\W', '_', name)
        imports = {match for path in workspace.glob('**/*FixtureComponent1Tests.swift')
                   for match in re.findall(r'@testable\s+import\s+(\w+)', path.read_text())}
        if len(imports) > 1:
            raise ValueError('Módulo Swift del target de pruebas ambiguo')
        if imports:
            bindings['FixtureModule'] = imports.pop()
        runtime.update(xcode_project_dir=str(project.parent.parent.relative_to(workspace)),
                       xcode_scheme=name)
        for path in workspace.glob('**/*FixtureComponent1.swift'):
            content = path.read_text()
            for kind, old in [('class', 'FixtureComponent1'), ('struct', 'FixtureComponent2'),
                              ('enum', 'FixtureComponent3')]:
                match = re.search(r'\b' + kind + r'\s+(\w*' + old + r')\b', content)
                if match:
                    if old in bindings and bindings[old] != match.group(1):
                        raise ValueError('Tipos de cola ambiguos')
                    bindings[old] = match.group(1)
            keys = re.findall(r'"([\w.]+\.chat\.pending\.actions\.v1)"', content)
            if keys:
                if len(set(keys)) != 1:
                    raise ValueError('Clave de persistencia de cola ambigua')
                bindings['benchmark.fixture.queue'] = keys[0]
    return bindings, runtime


def prepare_cell(root, tid, arm, platform, archive, meta, sdk=None):
    task = root / f'task_{tid}'
    ws, profile, inputs = task / 'runs' / arm, task / 'profiles' / arm, task / 'inputs' / arm
    if any(p.exists() for p in (ws, profile, inputs)):
        raise FileExistsError(f'Celda existente; usa un laboratorio nuevo: {tid}/{arm}')
    prefix = extract_project(archive, ws, platform, arm)
    bindings, runtime = project_bindings(ws, platform)
    runtime.update({key: bind_text(value, bindings) for key, value in meta.items()
                    if isinstance(value, str)})
    if platform == 'android':
        (ws / 'local.properties').write_text(f'sdk.dir={sdk}\n')
    else:
        project = ws / runtime['xcode_project_dir'] / (runtime['xcode_scheme'] + '.xcodeproj/project.pbxproj')
        if not project.is_file():
            raise FileNotFoundError(project)
        project.write_text(project.read_text().replace('IPHONEOS_DEPLOYMENT_TARGET = 26.2;',
                                                      'IPHONEOS_DEPLOYMENT_TARGET = 26.1;'))
    frozen = freeze_profile(profile, arm)
    # Give agents a working diff without copying private Git history or creating
    # commits. No user/global hooks, filters, credential helpers or config apply.
    evidence = task / 'evidence' / arm
    git_env = {**os.environ, 'GIT_CONFIG_GLOBAL': os.devnull, 'GIT_CONFIG_NOSYSTEM': '1'}
    for name, command in [('git-init', ['git', 'init', '--quiet']),
                          ('git-index', ['git', 'add', '--all'])]:
        command_record = run_logged(command, ws, evidence, name, 60, git_env)
        if command_record['exit_code'] != 0:
            raise RuntimeError('No se pudo preparar el índice Git del baseline; consulta los logs')
    inputs.mkdir(parents=True)
    for source, name in [(meta['file'], 'task.md'), (meta['oracle_source'], 'oracle' + meta['oracle_source'].suffix)]:
        (inputs / name).write_text(bind_text(source.read_text(), bindings), encoding='utf-8')
    write_json(inputs / 'manifest.json', {'protocol': PROTOCOL, 'platform': platform,
               'archive_prefix': prefix, 'bindings': bindings, 'runtime_metadata': runtime,
               'source_task_sha256': sha(meta['file']), 'source_oracle_sha256': sha(meta['oracle_source']),
               'task_sha256': sha(inputs / 'task.md'),
               'oracle_sha256': sha(inputs / ('oracle' + meta['oracle_source'].suffix)),
               'archive_sha256': sha(archive), 'profile': frozen,
               'workspace_baseline': snapshot(ws)}, exclusive=True)
    return ws


def cell_paths(root, tid, arm):
    task = root / f'task_{tid}'
    return task / 'runs' / arm, task / 'profiles' / arm, task / 'inputs' / arm, task / 'evidence' / arm


def task_prompt(root, tid, arm, platform):
    ws, profile, inputs, _ = cell_paths(root, tid, arm)
    manifest = verify_profile(profile)
    frozen = read_json(inputs / 'manifest.json')
    if sha(inputs / 'task.md') != frozen['task_sha256']:
        raise ValueError('La tarea congelada fue alterada')
    # Same authorization for every arm. No tactical coaching about how to solve it.
    return (f"{(inputs / 'task.md').read_text()}\n\n{APPROVAL}\n"
            f'Workspace: {ws}\nPlataforma: {platform}\n'), manifest


def native_prompt(root, tid, arm):
    task, _ = task_prompt(root, tid, arm, 'ios')
    ws, profile, _, _ = cell_paths(root, tid, arm)
    agent = (profile / 'agent.md').read_text()
    primary = profile / 'skills' / primary_skill(arm) / 'SKILL.md'
    # This is explicitly user-message transport, not a pretend native system role.
    parts = [agent]
    if primary.exists():
        parts.append(primary.read_text())
    if arm != 'build_sin_mas':
        parts.append('Skills de dominio disponibles bajo demanda (referencias relativas a cada skill):\n' +
                     '\n'.join(f'{name}: {profile / "skills" / name / "SKILL.md"}'
                               for name in ('data-api', 'ui-design')))
        steering = ws / 'AGENTS.md'
        if steering.is_file():
            parts.append(steering.read_text())
    parts.append(task)
    return '\n\n'.join(p for p in parts if p)


def terminate(proc):
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    proc.wait()


def run_logged(command, cwd, evidence, name, timeout, env=None, progress=None):
    """Real wall-clock timeout; drain both streams to disk, including on timeout."""
    evidence.mkdir(parents=True, exist_ok=True)
    out, err = evidence / f'{name}.stdout.log', evidence / f'{name}.stderr.log'
    started = time.monotonic()
    record = {'command': list(map(str, command)), 'cwd': str(cwd), 'started_at': stamp(),
              'stdout': str(out), 'stderr': str(err), 'timed_out': False, 'exit_code': None}
    with out.open('x') as stdout, err.open('x') as stderr:
        try:
            proc = subprocess.Popen(record['command'], cwd=cwd, env=env, stdout=stdout,
                                    stderr=stderr, text=True, start_new_session=True)
            while proc.poll() is None:
                reason = progress(out) if progress else None
                if reason or time.monotonic() - started >= timeout:
                    record['stop_reason'] = reason or 'timeout'
                    record['timed_out'] = not bool(reason)
                    terminate(proc)
                    break
                time.sleep(0.05)
            record['exit_code'] = proc.wait()
            # A successful launcher exit must not leave its build/test children
            # racing the evaluator. Only our own new process group is affected.
            try:
                os.killpg(proc.pid, 0)
            except ProcessLookupError:
                pass
            else:
                os.killpg(proc.pid, signal.SIGKILL)
                record['remaining_children_terminated'] = True
        except OSError as ex:
            record['launch_error'] = str(ex)
        except BaseException:
            if 'proc' in locals() and proc.poll() is None:
                terminate(proc)
            raise
    record['duration_seconds'] = round(time.monotonic() - started, 3)
    write_json(evidence / f'{name}.command.json', record, exclusive=True)
    return record


def events_from(path):
    events = []
    if Path(path).exists():
        for line in Path(path).read_text(encoding='utf-8', errors='replace').splitlines():
            try:
                value = json.loads(line)
                if isinstance(value, dict):
                    events.append(value)
            except json.JSONDecodeError:
                continue  # Raw stream remains on disk, including malformed lines.
    return events


def event_metrics(events, native=False):
    totals = dict.fromkeys(('input', 'output', 'cache_read', 'cache_write', 'reasoning'), 0)
    steps, tools, errors, stop, reported = 0, 0, [], None, 0
    for event in events:
        kind = event.get('type')
        if kind == 'tool_use':
            tools += 1
        if kind == 'error':
            errors.append(event.get('error', event))
        if kind == 'step_start':
            steps += 1
        if native and kind == 'PLANNER_RESPONSE':
            steps += 1
            tools += len(event.get('tool_calls') or [])
            for key in totals:
                totals[key] += event.get(key + '_tokens', 0)
            # Native cache counters may have provider-specific semantics.
        elif kind == 'step_finish':
            part = event.get('part', {})
            tok = part.get('tokens', {})
            reported += tok.get('total', 0)
            for key in ('input', 'output', 'reasoning'):
                totals[key] += tok.get(key, 0)
            for key in ('read', 'write'):
                totals['cache_' + key] += tok.get('cache', {}).get(key, 0)
            stop = part.get('reason', stop)
    finishes = [e for e in events if e.get('type') == ('PLANNER_RESPONSE' if native else 'step_finish')]
    measured = bool(finishes) and all(
        all(key + '_tokens' in e for key in ('input', 'output')) if native else
        all(key in e.get('part', {}).get('tokens', {}) for key in ('input', 'output', 'cache'))
        for e in finishes)
    return {'steps': steps, 'tools_called': tools, 'errors': errors, 'soft_stop_reason': stop,
            'tokens': {**totals, 'total': sum(totals.values()) if measured else None,
                       'reported_total': reported if not native and measured else None,
                       'formula': TOKEN_FORMULA, 'measured': measured,
                       'cross_runtime_comparable': not native}}


def profile_observation(profile, arm, events):
    observed = None if arm.startswith('build_') else False
    states = {}
    mismatches = []
    permission_errors = []
    for event in events:
        part = event.get('part', {})
        state = part.get('state', {})
        if part.get('type') == 'tool' or part.get('tool'):
            states[part.get('callID', str(len(states)))] = state.get('status')
        if state.get('status') == 'error':
            message = str(state.get('error', '')) + ' ' + str(state.get('output', ''))
            if re.search(r'permission|not allowed|denied|rejected', message, re.I):
                permission_errors.append({'tool': part.get('tool'), 'call_id': part.get('callID'),
                                          'message': message})
        if part.get('tool') == 'skill' and state.get('status') == 'completed':
            name = state.get('input', {}).get('name', '')
            source = profile / 'skills' / name / 'SKILL.md'
            if not re.fullmatch(r'[a-z0-9-]+', name) or not source.is_file():
                mismatches.append(name)
                continue
            expected = source.read_text()
            if expected.startswith('---\n'):
                expected = expected.split('---', 2)[-1].strip()
            if expected not in state.get('output', ''):
                mismatches.append(name)
            elif not arm.startswith('build_') and name == primary_skill(arm):
                observed = True
    return {'primary_loaded_by_content': observed,
            'pending_tools': [key for key, status in states.items() if status in ('running', 'pending')],
            'skill_content_mismatches': mismatches, 'permission_errors': permission_errors}


def opencode_configuration(root, tid, arm, model, platform='android', steps=60):
    if not re.fullmatch(r'[a-zA-Z0-9_-]+/[^\s/]+', model):
        raise ValueError('Se requiere un identificador explícito proveedor/modelo')
    ws, profile, _, _ = cell_paths(root, tid, arm)
    secrets = {p: 'deny' for p in SECRETS}
    secrets.update({f'*/{p}': 'deny' for p in SECRETS})
    read, edit = {'*': 'deny'}, {'*': 'deny'}
    for p in (str(ws.resolve()), str(ws)):
        for rules in (read, edit):
            rules.update({p: 'allow', p + '/*': 'allow'})
    for p in (str(profile.resolve() / 'skills'), str(profile / 'skills')):
        read.update({p: 'allow', p + '/*': 'allow'})
    if ws.exists():
        for entry in ws.iterdir():
            if not entry.is_symlink() and safe_path(entry.name):
                for rules in (read, edit):
                    rules[entry.name] = 'allow'
                    if entry.is_dir():
                        rules[entry.name + '/*'] = 'allow'
    for rules in (read, edit):
        rules.update(secrets)
    for name in ('AGENTS.md', '*/AGENTS.md', 'GEMINI.md', '*/GEMINI.md'):
        edit[name] = 'deny'
    commands = {'*': 'deny', 'git status*': 'allow', 'git diff*': 'allow',
                'git ls-files*': 'allow', 'pwd': 'allow', 'pwd -L': 'allow', 'pwd -P': 'allow',
                'ls': 'allow', 'ls *': 'allow', 'rg *': 'allow', 'head': 'allow', 'head *': 'allow'}
    if platform == 'android':
        commands.update({p: 'allow' for p in ('./gradlew *', './gradlew :core:domain:test*',
                        './gradlew :app:test*', './gradlew :core:data:test*', './gradlew :core:security:test*')})
    else:
        commands.update({'xcodebuild *': 'allow', 'xcrun simctl list*': 'allow'})
    commands.update(secrets)
    skills = {} if arm == 'build_sin_mas' else {'data-api': 'allow', 'ui-design': 'allow'}
    if not arm.startswith('build_'):
        skills[primary_skill(arm)] = 'allow'
    permission = {'*': 'deny', 'read': read, 'edit': edit, 'write': dict(edit), 'bash': commands,
                  'glob': 'allow', 'grep': 'allow', 'list': 'allow', 'todowrite': 'allow',
                  'skill': {'*': 'deny', **skills}, 'task': 'deny', 'question': 'deny',
                  'external_directory': {'*': 'deny', str(ws): 'allow', str(ws) + '/*': 'allow',
                                         str(profile / 'skills'): 'allow', str(profile / 'skills') + '/*': 'allow'}}
    # Existing CLI is 1.18.34. Retain its schema rather than silently migrating hosts.
    agent = {'model': model, 'steps': steps, 'temperature': 0.2, 'permission': permission}
    if not arm.startswith('build_'):
        agent.update(mode='primary', description='Frozen experimental snapshot: ' + arm,
                     prompt=(profile / 'agent.md').read_text())
    return {'$schema': 'https://opencode.ai/config.json',
            'model': model, 'small_model': model, 'enabled_providers': [model.split('/', 1)[0]],
            'share': 'disabled', 'snapshot': False,
            'autoupdate': False, 'formatter': False, 'lsp': False, 'plugin': [], 'mcp': {},
            'instructions': [] if arm == 'build_sin_mas' else [str(ws / 'AGENTS.md')],
            'skills': {'paths': [str(profile / 'skills')]}, 'agent': {agent_name(arm): agent}}


def readonly_rg():
    for candidate in (shutil.which('rg'), Path.home() / '.cache/opencode/bin/rg'):
        if candidate and Path(candidate).is_file():
            return Path(candidate).resolve()
    raise FileNotFoundError('Restricted search requires ripgrep')


def run_opencode(root, tid, arm, platform, cli, model, timeout, steps, tokens, env=None, probe_only=False):
    ws, profile, inputs, evidence = cell_paths(root, tid, arm)
    prompt, manifest = task_prompt(root, tid, arm, platform)
    config = opencode_configuration(root, tid, arm, model, platform, steps)
    evidence.mkdir(parents=True, exist_ok=True)
    write_json(evidence / 'request.json', {'prompt': prompt, 'profile': manifest, 'config': config,
               'instruction_delivery': 'opencode_agent_and_skill', 'runtime': str(cli)}, exclusive=True)
    runtime_env = dict(os.environ if env is None else env)
    # These entry points live outside the editable participant workspace.
    bindir = root / f'task_{tid}' / 'readonly-bin' / arm
    bindir.mkdir(parents=True, exist_ok=False)
    helper = bindir / 'readonly.py'
    shutil.copyfile(REPO / 'tools/mobile_benchmark_readonly.py', helper)
    runtime_env['BENCHMARK_RG'] = str(readonly_rg())
    runtime_env['BENCHMARK_GIT'] = shutil.which('git') or '/usr/bin/git'
    for command in ('ls', 'rg', 'git', 'head'):
        wrapper = bindir / command
        wrapper.write_text('#!/bin/sh\nexec ' + shlex.join([
            str(Path(__import__('sys').executable).resolve()), str(helper), str(ws.resolve()), command]) + ' "$@"\n')
        wrapper.chmod(0o755)
    # Do not prepend wrappers to the host PATH: OpenCode itself invokes git/rg
    # for project discovery and native tools. Apply them only in participant bash.
    shell_env = bindir / 'participant.bashenv'
    shell_env.write_text('export PATH=' + shlex.quote(str(bindir)) + ':"$PATH"\n')
    runtime_env['SHELL'] = '/bin/bash'
    runtime_env['BASH_ENV'] = str(shell_env)
    if platform == 'android':
        runtime_env['ORG_GRADLE_PROJECT_allowPlaceholderCredentials'] = 'true'
    for name in list(runtime_env):
        if name.startswith('OPENCODE_CONFIG') or name == 'OPENCODE_PURE':
            runtime_env.pop(name)
    host = root / f'task_{tid}' / 'hosts' / arm
    host.mkdir(parents=True, exist_ok=True)
    runtime_env.update(OPENCODE_CONFIG_CONTENT=json.dumps(config), XDG_CONFIG_HOME=str(host),
                       OPENCODE_DISABLE_PROJECT_CONFIG='1', OPENCODE_DISABLE_EXTERNAL_SKILLS='1',
                        OPENCODE_DISABLE_CLAUDE_CODE='1', OPENCODE_DISABLE_AUTOUPDATE='1')

    frozen = read_json(inputs / 'manifest.json')
    names = list(frozen['workspace_baseline'])
    source = next((name for name in names if name.endswith(('.kt', '.swift'))),
                  'gradlew' if 'gradlew' in names else names[0])
    checks = []
    for label, command in [
        ('native-glob', [str(cli), '--pure', 'debug', 'rg', 'files', '--glob', source, '--limit', '2']),
        ('native-read', [str(cli), '--pure', 'debug', 'file', 'read', source]),
        ('participant-shell', ['/bin/bash', '-c', 'pwd && git status --short && ls'])]:
        check = run_logged(command, ws, evidence, 'probe-' + label, 45, runtime_env)
        output = Path(check['stdout']).read_text()
        passed = check['exit_code'] == 0
        if label == 'native-glob':
            passed = passed and source in output.splitlines()
        elif label == 'native-read':
            try:
                data = json.loads(output)
                content = base64.b64decode(data['content']) if data.get('encoding') == 'base64' else data['content'].encode()
                passed = passed and content == (ws / source).read_bytes()
            except (ValueError, KeyError, TypeError):
                passed = False
        checks.append({'name': label, 'passed': passed, 'command': check})
    tooling_ready = all(check['passed'] for check in checks)
    write_json(evidence / 'tooling-probe.json', {'passed': tooling_ready, 'model_calls': 0, 'checks': checks}, exclusive=True)
    if probe_only:
        return {'tooling_ready': tooling_ready}
    if not tooling_ready:
        record = {'run_status': 'tooling_error', 'attribution_ready': False, 'model_calls': 0}
        write_json(evidence / 'run.json', record, exclusive=True)
        return record

    def budget(path):
        metrics = event_metrics(events_from(path))
        if metrics['tokens']['total'] is not None and metrics['tokens']['total'] > tokens:
            return 'token_limit'
        if metrics['steps'] > steps:
            return 'step_limit'
        return None

    run = run_logged([str(cli), 'run', '--pure', '--format', 'json',
                      '--title', f'Mobile benchmark {platform} {tid} {arm}', '--model', model,
                      '--agent', agent_name(arm), '--dir', str(ws), prompt], ws, evidence,
                     'inference', timeout, runtime_env, budget)
    events = events_from(run['stdout'])
    metrics = event_metrics(events)
    observation = profile_observation(profile, arm, events)
    if metrics['tokens']['total'] is not None and metrics['tokens']['total'] > tokens:
        run['stop_reason'] = 'token_limit'
    elif metrics['steps'] > steps:
        run['stop_reason'] = 'step_limit'
    healthy = (run['exit_code'] == 0 and not run.get('stop_reason') and
               not metrics['errors'] and metrics['soft_stop_reason'] == 'stop' and
               metrics['tokens']['measured'] and not observation['pending_tools'] and
               not run.get('remaining_children_terminated'))
    valid = (healthy and observation['primary_loaded_by_content'] is not False and
             not observation['skill_content_mismatches'] and not observation['permission_errors'])
    record = {**run, **metrics, **observation, 'protocol': PROTOCOL, 'task_id': tid, 'arm': arm, 'model': model,
              'run_status': 'complete' if healthy else 'runtime_error', 'attribution_ready': healthy,
              'profile_sha256': sha(profile / 'manifest.json'), 'completed_at': stamp()}
    record['attribution_ready'] = valid
    record['session_ids'] = sorted({e['sessionID'] for e in events if e.get('sessionID')})
    record['trace_sha256'] = sha(run['stdout'])
    if healthy and not valid:
        record['run_status'] = 'permission_blocked' if observation['permission_errors'] else 'profile_not_observed'
    verify_profile(profile)
    write_json(evidence / 'run.json', record, exclusive=True)
    return record


def junit_report(paths, expected_class=None):
    cases = {}
    for path in paths:
        tree = ET.parse(path)
        for case in tree.iter('testcase'):
            cls = case.get('classname', '')
            if expected_class and cls != expected_class:
                continue
            key = cls + '/' + case.get('name', '')
            cases[key] = ('failed' if case.find('failure') is not None or case.find('error') is not None
                          else 'skipped' if case.find('skipped') is not None else 'passed')
    executed = sum(status != 'skipped' for status in cases.values())
    return {'executed': executed, 'failed': sum(s == 'failed' for s in cases.values()), 'cases': cases}


def suite_status(command, report, expected_min=1):
    if command.get('timed_out'):
        return 'infrastructure_timeout'
    if command.get('launch_error'):
        return 'infrastructure_error'
    if command.get('remaining_children_terminated'):
        return 'infrastructure_error'
    if command['exit_code'] != 0:
        text = '\n'.join(Path(command[k]).read_text(errors='replace') for k in ('stdout', 'stderr'))
        if any(message in text for message in ('database is locked', 'Unable to find a destination',
                                               'SDK location not found', 'Could not resolve all files',
                                               'license agreements', 'Connection refused',
                                               'Faltan credenciales en local.properties',
                                               'a sealed resource is missing or invalid',
                                               'signature of')):
            return 'infrastructure_error'
        if report.get('failed'):
            return 'tests_failed'
        if re.search(r'\.swift:\d+:\d+: error:|e: file:|\.kt:\d+:\d+|Kotlin compiler:', text):
            return 'build_failed'
        return 'runner_error_unclassified'
    if report.get('parse_error'):
        return 'report_invalid'
    if report.get('executed', 0) == 0:
        return 'no_tests_executed'
    if report['executed'] < expected_min:
        return 'incomplete_test_execution'
    if report.get('failed'):
        return 'tests_failed'
    if 'unknown' in report.get('cases', {}).values():
        return 'unverified_test_status'
    return 'passed'


@contextmanager
def oracle_injection(inputs, target, expected_sha):
    if target.exists() or target.is_symlink():
        raise FileExistsError(f'No se sobrescribe un archivo del participante: {target}')
    if sha(inputs) != expected_sha:
        raise ValueError('Oráculo congelado alterado')
    if target.parent.is_symlink():
        raise ValueError('No se inyectan oráculos a través de enlaces simbólicos')
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(inputs, target)
    try:
        yield
    finally:
        target.unlink(missing_ok=True)


def authorized_test_migrations(ws, missing, platform, tid):
    """Only the exact assertion migration required by Android T2 is authorized."""
    if platform != 'android' or str(tid) != '2':
        return {}
    old_name = 'un fallo de la cola deja el contador en cero'
    paths = list(ws.glob('app/src/test/**/AccesoBuzonViewModelTest.kt'))
    if len(paths) != 1:
        return {}
    path = paths[0]
    result = subprocess.run(['git', 'show', ':' + str(path.relative_to(ws))],
                            cwd=ws, capture_output=True, text=True, check=False)
    def bodies(text):
        found = {}
        for match in re.finditer(r'@Test\s+fun\s+`([^`]+)`[^\n]*\{', text):
            depth, end = 1, match.end()
            while end < len(text) and depth:
                depth += (text[end] == '{') - (text[end] == '}')
                end += 1
            found[match.group(1)] = re.sub(r'\s+', '', text[match.end():end - 1])
        return found
    old = bodies(result.stdout).get(old_name)
    if not old or 'assertFalse(vm.hayAltas.value)' not in old:
        return {}
    expected = old.replace('assertFalse(vm.hayAltas.value)', 'assertTrue(vm.hayAltas.value)')
    addition = 'assertTrue(vm.estadoAcceso.valueisEstadoAccesoBuzon.Error)'
    migrations = {}
    for name, body in bodies(path.read_text()).items():
        if addition in body and body.replace(addition, '', 1) == expected:
            for identity in missing:
                if identity.endswith('.AccesoBuzonViewModelTest/' + old_name):
                    migrations[identity] = identity.rsplit('/', 1)[0] + '/' + name
    return migrations


def evaluation_record(root, tid, arm, baseline, oracle, original):
    ws, profile, inputs, evidence = cell_paths(root, tid, arm)
    frozen = read_json(inputs / 'manifest.json')
    current = snapshot(ws)
    changed = [name for name in current.keys() | frozen['workspace_baseline'].keys()
               if current.get(name) != frozen['workspace_baseline'].get(name)]
    missing = sorted(set(baseline.get('report', {}).get('cases', {})) -
                     set(original.get('report', {}).get('cases', {})))
    migrations = authorized_test_migrations(ws, missing, frozen.get('platform'), tid)
    migrations = {old: new for old, new in migrations.items()
                  if new in original.get('report', {}).get('cases', {})}
    if migrations:
        original['authorized_test_migrations'] = migrations
        original['migration_basis'] = 'T2 required error visibility; all other test statements retained'
        missing = sorted(set(missing) - migrations.keys())
    if missing:
        original['status'] = 'baseline_tests_missing'
        original['missing_baseline_tests'] = missing
    run = read_json(evidence / 'run.json')
    accepted = all(s['status'] == 'passed' for s in (baseline, oracle, original))
    valid = (run.get('attribution_ready', False) and baseline['status'] == 'passed' and
             not any(s['status'] in ('infrastructure_error', 'infrastructure_timeout', 'no_tests_executed',
                                     'runner_error_unclassified', 'report_invalid', 'unverified_test_status',
                                     'incomplete_test_execution')
                     for s in (oracle, original)))
    record = {'protocol': PROTOCOL, 'task_id': tid, 'arm': arm, 'baseline': baseline,
              'oracle': oracle, 'original': original, 'oracle_pass': oracle['status'] == 'passed',
              'original_suite_pass': original['status'] == 'passed',
              'artifact_acceptance': accepted, 'valid_for_agent_comparison': valid,
              'functional_acceptance': accepted if valid else None,
              'diff_summary': sorted(changed),
              'new_tests_found': sum(bool(re.search(r'(Test|Tests)\.(kt|swift)$', p)) for p in changed)}
    verify_profile(profile)
    write_json(evidence / 'eval.json', record, exclusive=True)
    return record


def preflight(platform, tasks, archive, runtime, cli, java=None, sdk=None):
    errors = []
    runtime_version = None
    for arm in ARMS:
        source_profile(arm)
    for meta in tasks.values():
        for key in ('file', 'oracle_source'):
            if not meta[key].is_file():
                errors.append(f'Falta {meta[key]}')
    if not archive.is_file():
        errors.append(f'Falta ZIP de aplicación: {archive}; usa --base-zip')
    if not Path(cli).is_file():
        errors.append(f'Falta runtime: {cli}')
    elif runtime == 'opencode':
        try:
            version = subprocess.run([str(cli), '--version'], capture_output=True, text=True, timeout=10)
            runtime_version = version.stdout.strip() if version.returncode == 0 else None
        except (OSError, subprocess.TimeoutExpired):
            runtime_version = None
        if runtime_version != '1.18.34':
            errors.append('Este adaptador conserva la configuración de OpenCode 1.18.34; '
                          'selecciona ese CLI con --cli. Otros runtimes requieren validar su contrato')
    if shutil.which('git') is None:
        errors.append('Falta Git para preparar el índice del baseline')
    if runtime == 'antigravity':
        if not os.environ.get('ANTIGRAVITY_LS_ADDRESS'):
            errors.append('Antigravity: falta ANTIGRAVITY_LS_ADDRESS; iniciar desde su entorno nativo')
        errors.append('agentapi no ofrece en su ayuda un contrato verificable de finalización y '
                      'cancelación aislada. No se lanzará inferencia nativa sin ese contrato; '
                      'usa --runtime opencode para la comparación controlada')
    if platform == 'android':
        if not java or not (Path(java) / 'bin/java').is_file():
            errors.append('Falta JDK; usa --java-home')
        if not sdk or not Path(sdk).is_dir():
            errors.append('Falta Android SDK; usa --android-home')
    elif shutil.which('xcodebuild') is None or shutil.which('xcrun') is None:
        errors.append('Faltan Xcode/xcrun')
    return {'protocol': PROTOCOL, 'platform': platform, 'runtime': runtime,
            'runtime_version': runtime_version,
            'sources_valid': True, 'ready': not errors, 'errors': errors,
            'native_context_isolation': False if runtime == 'antigravity' else None}


def new_root(platform):
    return Path(tempfile.gettempdir()) / 'opencode' / f'{platform}-benchmark-{uuid.uuid4().hex[:12]}'


def validate_root(root):
    resolved = root.resolve()
    if resolved == REPO or REPO in resolved.parents or resolved in REPO.parents:
        raise ValueError('El laboratorio debe estar fuera del repositorio y no ser un ancestro suyo')


def summary(root, tasks, arms):
    result = {'protocol': PROTOCOL, 'token_formula': TOKEN_FORMULA, 'tasks': {}}
    for tid in tasks:
        cells = {}
        for arm in arms:
            _, _, _, evidence = cell_paths(root, tid, arm)
            if (evidence / 'baseline.suite.json').exists():
                cells[arm] = {'run_status': 'not_started', 'valid_for_agent_comparison': False,
                              'functional_acceptance': None,
                              'baseline': read_json(evidence / 'baseline.suite.json')}
            if (evidence / 'run.json').exists():
                cells.setdefault(arm, {'functional_acceptance': None, 'valid_for_agent_comparison': False})
                cells[arm].update(read_json(evidence / 'run.json'))
                if (evidence / 'eval.json').exists():
                    cells[arm].update(read_json(evidence / 'eval.json'))
        result['tasks'][tid] = {'arms': cells}
    return result


def xcresult_report(data, expected_class=None):
    cases = {}

    def visit(node, parents=(), suites=()):
        names = (*parents, node.get('name', ''))
        if node.get('nodeType') in ('Test Suite', 'Unit test bundle', 'UI test bundle'):
            suites = (*suites, node.get('name', ''))
        if node.get('nodeType') == 'Test Case':
            # Do not compare result-bundle/device/run IDs across baseline and
            # regression. Test bundle, suite and case names are the stable identity.
            key = '/'.join((*suites, node.get('name', '')))
            if expected_class is None or expected_class in names or expected_class in key:
                result = node.get('result')
                cases[key] = {'Passed': 'passed', 'Failed': 'failed', 'Skipped': 'skipped',
                              'Expected Failure': 'skipped'}.get(result, 'unknown')
        for child in node.get('children', []):
            visit(child, names, suites)

    for node in data.get('testNodes', []):
        visit(node)
    return {'executed': sum(s in ('passed', 'failed') for s in cases.values()),
            'failed': sum(s == 'failed' for s in cases.values()), 'cases': cases}


def run_suite(root, tid, arm, platform, meta, phase, timeout=600, env=None,
              destination='platform=iOS Simulator,name=iPhone 17'):
    ws, _, inputs, evidence = cell_paths(root, tid, arm)
    meta = {**meta, **read_json(inputs / 'manifest.json').get('runtime_metadata', {})}
    expected_class = None
    expected_min = 1
    if phase == 'oracle':
        source = inputs / ('oracle.kt' if platform == 'android' else 'oracle.swift')
        if platform == 'android':
            expected_class = shlex.split(meta['gradle_oracle_task'])[-1]
            expected_min = source.read_text().count('@Test')
        else:
            expected_class = meta['xcode_oracle_test'].rsplit('/', 1)[-1]
            expected_min = len(re.findall(r'\bfunc\s+test\w*\s*\(', source.read_text()))
        if expected_min < 1:
            raise ValueError('El oráculo no declara pruebas reconocibles')
    if platform == 'android':
        env = {**(os.environ if env is None else env),
               'ORG_GRADLE_PROJECT_allowPlaceholderCredentials': 'true'}
        target = meta['gradle_oracle_task'] if phase == 'oracle' else shlex.split(meta['gradle_original_task'])[0]
        command = ['./gradlew', *shlex.split(target), '--console=plain', '--rerun-tasks', '--no-build-cache']
        module = ws.joinpath(*shlex.split(target)[0].strip(':').split(':')[:-1])
        reports = module / 'build/test-results'
        if ws.resolve() not in reports.resolve().parents:
            raise ValueError('Directorio de resultados fuera del workspace')
        if reports.exists():
            # Preserve, but remove from discovery, results of a previous phase.
            # Timestamps alone can mistakenly accept a recent stale report.
            evidence.mkdir(parents=True, exist_ok=True)
            shutil.move(str(reports), str(evidence / f'{phase}-previous-test-results'))
        command_record = run_logged(command, ws, evidence, phase, timeout, env)
        paths = []
        for path in sorted(reports.glob('**/TEST-*.xml')):
            if not path.is_symlink() and ws.resolve() in path.resolve().parents:
                saved = evidence / f'{phase}-reports' / path.relative_to(reports)
                saved.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, saved)
                paths.append(saved)
        try:
            report = junit_report(paths, expected_class)
        except (ET.ParseError, OSError) as ex:
            report = {'executed': 0, 'failed': 0, 'cases': {}, 'parse_error': str(ex)}
    else:
        result = evidence / f'{phase}.xcresult'
        command = ['xcodebuild', 'test', '-scheme', meta.get('xcode_scheme', 'FixtureProject'), '-destination', destination,
                   '-parallel-testing-enabled', 'NO', '-maximum-concurrent-test-simulator-destinations', '1',
                   '-derivedDataPath', str(evidence / f'derived-{phase}'), '-resultBundlePath', str(result),
                   '-only-testing:' + (meta['xcode_oracle_test'] if phase == 'oracle' else meta['xcode_original_test']),
                   'IPHONEOS_DEPLOYMENT_TARGET=26.1']
        command_record = run_logged(command, ws / meta.get('xcode_project_dir', 'FixtureProject'), evidence, phase, timeout, env)
        report = {'executed': 0, 'failed': 0, 'cases': {}}
        if result.exists() and not command_record['timed_out']:
            extracted = run_logged(['xcrun', 'xcresulttool', 'get', 'test-results', 'tests',
                                    '--path', str(result), '--compact'], ws, evidence,
                                   phase + '-report', 30, env)
            if extracted['exit_code'] == 0:
                try:
                    report = xcresult_report(read_json(extracted['stdout']), expected_class)
                except (json.JSONDecodeError, OSError) as ex:
                    report['parse_error'] = str(ex)
    status = suite_status(command_record, report, expected_min)
    record = {'status': status, 'command': command_record, 'report': report,
              'expected_min': expected_min, 'scope': 'oracle' if phase == 'oracle' else 'full_unit_test_target'}
    write_json(evidence / f'{phase}.suite.json', record, exclusive=True)
    return record


def evaluate(root, tid, arm, platform, meta, timeout=600, env=None,
             destination='platform=iOS Simulator,name=iPhone 17'):
    ws, profile, inputs, evidence = cell_paths(root, tid, arm)
    verify_profile(profile)
    baseline = read_json(evidence / 'baseline.suite.json')
    if baseline['status'] != 'passed':
        raise ValueError('Baseline no verificado; no se atribuirán fallos al agente')
    if not read_json(evidence / 'run.json').get('attribution_ready'):
        raise ValueError('Finalización/perfil no verificados; no se ejecutará evaluación concurrente o atribuible')
    frozen = read_json(inputs / 'manifest.json')
    meta = {**meta, **frozen.get('runtime_metadata', {})}
    source = inputs / ('oracle.kt' if platform == 'android' else 'oracle.swift')
    target = ws / meta['oracle_target']
    if ws.resolve() not in target.resolve().parents:
        raise ValueError('Destino de oráculo fuera del workspace')
    before = snapshot(ws)
    with oracle_injection(source, target, frozen['oracle_sha256']):
        oracle = run_suite(root, tid, arm, platform, meta, 'oracle', timeout, env, destination)
    if snapshot(ws) != before:
        raise ValueError('El evaluador alteró fuentes del participante')
    original = run_suite(root, tid, arm, platform, meta, 'original', timeout, env, destination)
    return evaluation_record(root, tid, arm, baseline, oracle, original)


def main_for(platform, tasks, archive_default, cli_default, argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    task_selection = parser.add_mutually_exclusive_group()
    task_selection.add_argument('--tasks', nargs='+', choices=list(tasks), default=list(tasks))
    task_selection.add_argument('--task', choices=[*tasks, 'all'])
    arm_selection = parser.add_mutually_exclusive_group()
    arm_selection.add_argument('--arms', nargs='+', choices=ARMS, default=list(ARMS))
    arm_selection.add_argument('--arm', choices=[*ARMS, 'all'])
    parser.add_argument('--root', type=Path, help='Laboratorio externo; nunca se sobrescriben celdas')
    parser.add_argument('--base-zip', type=Path, default=archive_default)
    parser.add_argument('--tooling-probe-only', action='store_true', help='Verify native tools and restricted shell without model calls')
    parser.add_argument('--runtime', choices=['opencode', 'antigravity'],
                        default='opencode' if platform == 'android' else 'antigravity')
    parser.add_argument('--cli', type=Path)
    parser.add_argument('--model', default=DEFAULT_MODEL)
    parser.add_argument('--java-home', type=Path, default=Path('/opt/homebrew/opt/openjdk@21'))
    parser.add_argument('--android-home', type=Path, default=Path.home() / 'Developer/android')
    parser.add_argument('--destination', default='platform=iOS Simulator,name=iPhone 17')
    parser.add_argument('--timeout', type=float, default=1800)
    parser.add_argument('--test-timeout', type=float, default=600)
    parser.add_argument('--steps', type=int, default=60)
    parser.add_argument('--token-limit', type=int, default=5_000_000)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--preflight-only', action='store_true', help='Diagnóstico sin inferencia ni escrituras')
    mode.add_argument('--prepare-only', action='store_true', help='Congelar perfiles/tareas y extraer copias limpias')
    mode.add_argument('--baseline-only', action='store_true', help='Preparar y probar el baseline sin llamar al LLM')
    mode.add_argument('--run-prepared', action='store_true', help='Ejecutar celdas previamente preparadas')
    mode.add_argument('--eval-only', action='store_true', help='Evaluar una ejecución registrada, no una carpeta arbitraria')
    args = parser.parse_args(argv)
    args.cli = args.cli or (Path.home() / '.gemini/antigravity/bin/agentapi'
                            if args.runtime == 'antigravity' else cli_default)
    if (not all(math.isfinite(v) for v in (args.timeout, args.test_timeout)) or
            min(args.timeout, args.test_timeout, args.steps, args.token_limit) <= 0):
        parser.error('Los presupuestos deben ser positivos y finitos')
    tids = list(tasks) if args.task == 'all' else [args.task] if args.task else args.tasks
    arms = list(ARMS) if args.arm == 'all' else [args.arm] if args.arm else args.arms
    if len(set(tids)) != len(tids) or len(set(arms)) != len(arms):
        parser.error('No se permiten celdas duplicadas')
    if (args.run_prepared or args.eval_only) and args.root is None:
        parser.error('--run-prepared/--eval-only requieren --root')
    if platform == 'android' and args.runtime != 'opencode':
        parser.error('Android utiliza el runtime OpenCode')
    selected = {tid: tasks[tid] for tid in tids}
    check = preflight(platform, selected, args.base_zip, args.runtime, args.cli,
                      args.java_home, args.android_home)
    args.runtime_version = check.get('runtime_version')
    if args.preflight_only:
        print(json.dumps(check, ensure_ascii=False, indent=2))
        return 0 if check['ready'] else 2
    root = (args.root or new_root(platform)).resolve()
    validate_root(root)
    # Preparation/evaluation do not need model credentials or a live model runtime.
    if not (args.prepare_only or args.baseline_only or args.eval_only) and not check['ready']:
        print(json.dumps(check, ensure_ascii=False, indent=2))
        return 2
    if args.runtime == 'antigravity' and not (args.prepare_only or args.baseline_only or args.eval_only):
        return 2
    if not args.run_prepared and not args.eval_only and root.exists() and any(root.iterdir()):
        raise FileExistsError('Laboratorio no vacío; usa uno nuevo o --run-prepared')
    if (args.run_prepared or args.eval_only) and not (root / 'experiment.json').is_file():
        raise FileNotFoundError('No hay un experimento v2 preparado en --root')
    root.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, 'GIT_CONFIG_GLOBAL': os.devnull, 'GIT_CONFIG_NOSYSTEM': '1'}
    if platform == 'android':
        env.update(JAVA_HOME=str(args.java_home), ANDROID_HOME=str(args.android_home),
                   PATH=str(args.java_home / 'bin') + os.pathsep + env.get('PATH', ''),
                   ORG_GRADLE_PROJECT_allowPlaceholderCredentials='true')
    # A lock protects prepare/run/eval on the same laboratory, including separate
    # CLI invocations. Never overlap an evaluator and a still-running model call.
    with (root / '.benchmark.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as ex:
            raise RuntimeError('Ya hay una ejecución activa en este laboratorio') from ex
        return run_matrix(root, platform, tasks, tids, arms, args, env)


def run_matrix(root, platform, tasks, tids, arms, args, env):
    settings = {'protocol': PROTOCOL, 'platform': platform, 'runtime': args.runtime,
                'runtime_version': args.runtime_version,
                'runtime_path': str(args.cli.resolve()),
                'runtime_sha256': sha(args.cli) if args.cli.is_file() else None,
                'model': args.model, 'steps': args.steps, 'token_limit': args.token_limit,
                'timeout': args.timeout, 'test_timeout': args.test_timeout,
                'destination': args.destination if platform == 'ios' else None,
                'java_home': str(args.java_home.resolve()) if platform == 'android' else None,
                'android_home': str(args.android_home.resolve()) if platform == 'android' else None,
                'placeholder_credentials': platform == 'android',
                'harness': {name: sha(REPO / 'tools' / name) for name in
                            ('mobile_benchmark_common.py', 'mobile_benchmark_readonly.py', f'real_{platform}_' +
                             ('gemini' if platform == 'android' else 'antigravity') + '_benchmark.py')}}
    manifest = root / 'experiment.json'
    if manifest.exists():
        if read_json(manifest) != settings:
            raise ValueError('Configuración/arnés distintos al laboratorio congelado')
    else:
        write_json(manifest, settings, exclusive=True)
    print(f'Laboratorio {PROTOCOL}: {root}')
    success = True
    for tid in tids:
        for arm in arms:
            if not args.run_prepared and not args.eval_only:
                prepare_cell(root, tid, arm, platform, args.base_zip, tasks[tid], args.android_home)
            ws, profile, inputs, evidence = cell_paths(root, tid, arm)
            verify_profile(profile)
            if args.prepare_only:
                continue
            if args.tooling_probe_only:
                probe = run_opencode(root, tid, arm, platform, args.cli, args.model,
                                     args.timeout, args.steps, args.token_limit, env, probe_only=True)
                success = success and probe['tooling_ready']
                print(f'{tid}/{arm}: tooling probe {"passed" if probe["tooling_ready"] else "failed"}; model calls: 0')
                continue
            if not args.eval_only:
                if (evidence / 'run.json').exists():
                    raise FileExistsError('Esta celda ya tiene inferencia; usa una nueva repetición')
                frozen = read_json(inputs / 'manifest.json')
                if snapshot(ws) != frozen['workspace_baseline']:
                    raise ValueError('Workspace modificado antes de la inferencia')
                if (evidence / 'baseline.suite.json').exists():
                    baseline = read_json(evidence / 'baseline.suite.json')
                else:
                    baseline = run_suite(root, tid, arm, platform, tasks[tid], 'baseline',
                                         args.test_timeout, env, args.destination)
                if baseline['status'] != 'passed':
                    success = False
                    print(f'{tid}/{arm}: baseline {baseline["status"]}; inferencia omitida')
                    continue
                if snapshot(ws) != frozen['workspace_baseline']:
                    raise ValueError('La preparación del baseline alteró archivos fuente; revisar antes de gastar tokens')
                if args.baseline_only:
                    continue
                run = run_opencode(root, tid, arm, platform, args.cli, args.model,
                                   args.timeout, args.steps, args.token_limit, env)
                # Provider failure is not an agent failure. Preserve partial work, do
                # not launch a potentially concurrent evaluator on an unhealthy run.
                if not run['attribution_ready']:
                    success = False
                    print(f'{tid}/{arm}: ejecución no válida; consulta evidence/{arm}/run.json')
                    write_json(root / 'resultados.json', summary(root, tids, arms))
                    continue
            result = evaluate(root, tid, arm, platform, tasks[tid], args.test_timeout, env, args.destination)
            success = success and result['functional_acceptance']
            write_json(root / 'resultados.json', summary(root, tids, arms))
    if not args.prepare_only:
        write_json(root / 'resultados.json', summary(root, tids, arms))
    return 0 if success else 1
