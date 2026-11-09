#!/usr/bin/env python3
"""Benchmark arnés multi-modelo para Proyecto Real Android CRM.

Soporta ejecución y evaluación parametrizada de cualquier modelo y proveedor:
  - github-copilot/mai-code-1.1-flash
  - openai/gpt-6.1-terra
  - github-copilot/gemini-3.8-flash
sobre las tareas y perfiles metodológicos definidos.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

REPO = Path(__file__).resolve().parent.parent
BASE_ZIP = Path(os.environ.get("MOBILE_BENCHMARK_ANDROID_ARCHIVE",
    str(Path.home() / ".local/share/ai-agents-kit/fixtures/mobile-android.zip")))
SPEC_DIR = REPO / 'docs/experimentos/real-android-gemini-2026-11-08'
DEFAULT_ROOT = Path('/tmp/real-android-benchmark')

CLI = str(Path.home() / ".local/bin/opencode")
JAVA_HOME = '/opt/homebrew/opt/openjdk@21'
ANDROID_HOME = os.environ.get("ANDROID_HOME", str(Path.home() / "Library/Android/sdk"))

TIMEOUT = 1800
STEP_LIMIT = 60
TOKEN_LIMIT = 5_000_000

ARMS = ('v2_reforzado', 'developer_actual', 'v2', 'build_mas', 'build_sin_mas')

DELTA_A = ('Vincula los criterios afectados con pruebas o checks observables, sin casos de relleno. '
           'Cuando modifiques código compartido, contrasta con el baseline disponible el comportamiento '
           'existente que no se pidió cambiar y añade regresión para protegerlo.')
DELTA_B = ('Al reanudar, contrasta el registro con el código y las verificaciones disponibles antes de '
           'continuar; los estados guardados no sustituyen evidencia vigente. Si cambia un requisito, '
           'actualiza su literal y reabre solo el trabajo afectado.')

SECRETS = ('*.env*', '*.pem', '*.key', '*.p12', '*.pfx', '*.jks', '*.keystore', '*credential*',
           '*.secret*', '*/.ssh/*', '*/.aws/*', '*/.config/gh/*', '*/auth.json',
           '*/.npmrc', '*/.netrc', '*/.pypirc', '*antigravity-accounts*')

TASKS = {
    '1': {
        'id': 'GBA-SEARCH-PROSPECTS',
        'title': 'Media-Baja — Búsqueda, Filtrado y Normalización de Prospectos',
        'complexity': 'media-baja',
        'file': SPEC_DIR / 'tarea-1-media-baja.md',
        'oracle_source': SPEC_DIR / 'oraculos/OracleSearchProspectsTest.kt',
        'oracle_target': 'core/domain/src/test/java/com/example/mobilefixture/domain/use_case/prospect/OracleSearchProspectsTest.kt',
        'gradle_oracle_task': ':core:domain:testReleaseUnitTest --tests "com.example.mobilefixture.domain.use_case.prospect.OracleSearchProspectsTest"',
        'gradle_original_task': ':core:domain:testReleaseUnitTest --tests "com.example.mobilefixture.domain.util.*"',
    },
    '2': {
        'id': 'GBA-BUZON-RETRY-UI',
        'title': 'Media-Alta — Remediación QLT-0017 y Gestión de Altas en Conflicto',
        'complexity': 'media-alta',
        'file': SPEC_DIR / 'tarea-2-media-alta.md',
        'oracle_source': SPEC_DIR / 'oraculos/OracleBuzonRetryUiTest.kt',
        'oracle_target': 'app/src/test/java/com/example/mobilefixture/tests1/features/offline/buzon/OracleBuzonRetryUiTest.kt',
        'gradle_oracle_task': ':app:testDebugUnitTest --tests "com.example.mobilefixture.tests1.features.offline.buzon.OracleBuzonRetryUiTest"',
        'gradle_original_task': ':app:testDebugUnitTest --tests "com.example.mobilefixture.tests1.features.offline.buzon.AccesoBuzonViewModelTest"',
    },
    '3': {
        'id': 'GBA-QUEUE-CONCURRENCY-CIPHER',
        'title': 'Alta — Deduplicación Atómica, Cifrado por Campo y Concurrencia en Cola Offline',
        'complexity': 'alta',
        'file': SPEC_DIR / 'tarea-3-alta.md',
        'oracle_source': SPEC_DIR / 'oraculos/OracleQueueConcurrencyCipherTest.kt',
        'oracle_target': 'core/data/src/test/java/com/example/mobilefixture/data/local/offline/OracleQueueConcurrencyCipherTest.kt',
        'gradle_oracle_task': ':core:data:testReleaseUnitTest --tests "com.example.mobilefixture.data.local.offline.OracleQueueConcurrencyCipherTest"',
        'gradle_original_task': ':core:data:testReleaseUnitTest --tests "com.example.mobilefixture.data.local.offline.OfflineQueueStoreTest"',
    }
}


def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, data, exclusive=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x' if exclusive else 'w', encoding='utf-8') as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write('\n')


def read_json(path):
    with path.open('r', encoding='utf-8') as handle:
        return json.load(handle)


def reinforce(text):
    lines = text.splitlines()
    for heading, delta in (('- **Comprobar.**', DELTA_A), ('- **Continuidad bajo demanda.**', DELTA_B)):
        matches = [i for i, line in enumerate(lines) if line.startswith(heading)]
        if matches:
            lines[matches[0]] += ' ' + delta
    return '\n'.join(lines) + '\n'


def primary_skill(arm):
    return 'developer' if arm == 'developer_actual' else 'developer-v2'


def agent_name(arm):
    return 'build' if arm.startswith('build_') else 'pilot-' + arm


def extract_base_project(target_dir):
    if not BASE_ZIP.exists():
        raise FileNotFoundError(f"Project zip not found at {BASE_ZIP}")
    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    temp_dir = target_dir.parent / f'.tmp_{target_dir.name}_{int(time.time() * 1000)}'
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(['unzip', '-qo', str(BASE_ZIP), '-d', str(temp_dir)], check=True)
    unzipped = temp_dir / 'app-crm-android-enterprise'
    shutil.move(str(unzipped), str(target_dir))
    shutil.rmtree(temp_dir)


def prepare_local_properties(workspace):
    local_props = workspace / 'local.properties'
    content = ""
    if local_props.exists():
        content = local_props.read_text()
    if 'sdk.dir=' in content:
        content = re.sub(r'sdk\.dir=.*', f'sdk.dir={ANDROID_HOME}', content)
    else:
        content = f'sdk.dir={ANDROID_HOME}\n' + content
    local_props.write_text(content)


def prepare_workspace(root, task_id, arm):
    task_dir = root / f'task_{task_id}'
    workspace = task_dir / 'runs' / arm
    profile = task_dir / 'profiles' / arm
    skills = profile / 'skills'
    hosts = task_dir / 'hosts' / arm

    if workspace.exists():
        shutil.rmtree(workspace)
    if profile.exists():
        shutil.rmtree(profile)
    if hosts.exists():
        shutil.rmtree(hosts)

    extract_base_project(workspace)
    prepare_local_properties(workspace)

    skills.mkdir(parents=True, exist_ok=True)
    (hosts / 'opencode').mkdir(parents=True, exist_ok=True)

    mas_folders = ['.architecture', '.data', '.design', '.quality', '.security', '.navigator', '.sdd']
    if arm == 'build_sin_mas':
        agents_md = workspace / 'AGENTS.md'
        if agents_md.exists():
            agents_md.unlink()
        for folder in mas_folders:
            p = workspace / folder
            if p.exists():
                shutil.rmtree(p)
    else:
        installed_skills = Path.home() / '.gemini/config/skills'
        if not installed_skills.exists():
            installed_skills = REPO / 'canonical/skills'
        for domain in ('data-api', 'ui-design'):
            domain_src = installed_skills / domain
            if domain_src.exists():
                dest = skills / domain
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(domain_src, dest)

    candidate_dir = REPO / 'docs/experimentos/continuidad-developer-v2-refuerzos-2026-11-06/fuentes'

    if arm == 'developer_actual':
        installed_dev = Path.home() / '.gemini/config/skills/developer'
        if not installed_dev.exists():
            installed_dev = REPO / 'canonical/skills/developer'
        dest = skills / 'developer'
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(installed_dev, dest)

        agent_file = Path.home() / '.gemini/antigravity/canonical/agents/developer.md'
        if not agent_file.exists():
            agent_file = REPO / 'canonical/agents/developer.md'
        (profile / 'agent.md').write_text(agent_file.read_text())

    elif arm in ('v2', 'v2_reforzado'):
        raw_skill = (candidate_dir / 'SKILL-candidato2.md').read_text()
        if arm == 'v2_reforzado':
            raw_skill = reinforce(raw_skill)
        skill_text = raw_skill.replace('__SKILL__', primary_skill(arm)).replace('__DATA_API__', 'data-api').replace('__UI_DESIGN__', 'ui-design')
        skill_path = skills / primary_skill(arm)
        skill_path.mkdir(parents=True, exist_ok=True)
        (skill_path / 'SKILL.md').write_text(skill_text)

        raw_agent = (candidate_dir / 'agent-candidato2.md').read_text()
        agent_text = raw_agent.replace('__SKILL__', primary_skill(arm))
        (profile / 'agent.md').write_text(agent_text)


def configuration(root, task_id, arm, model):
    task_dir = root / f'task_{task_id}'
    workspace = task_dir / 'runs' / arm
    profile = task_dir / 'profiles' / arm
    skills = profile / 'skills'

    ws_res = workspace.resolve()
    sk_res = skills.resolve()
    secrets_rules = {p: 'deny' for p in SECRETS}

    read_rules = {'*': 'deny', **secrets_rules}
    edit_rules = {'*': 'deny', **secrets_rules}
    write_rules = {'*': 'deny', **secrets_rules}

    for ws_p in (str(ws_res), str(workspace)):
        read_rules[ws_p] = 'allow'
        read_rules[ws_p + '/*'] = 'allow'
        edit_rules[ws_p] = 'allow'
        edit_rules[ws_p + '/*'] = 'allow'
        write_rules[ws_p] = 'allow'
        write_rules[ws_p + '/*'] = 'allow'

    for sk_p in (str(sk_res), str(skills)):
        read_rules[sk_p] = 'allow'
        read_rules[sk_p + '/*'] = 'allow'

    if ws_res.exists():
        for entry in ws_res.iterdir():
            if not entry.is_symlink():
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
        read_rules[p] = 'deny'
        edit_rules.pop(p, None)
        edit_rules[p] = 'deny'
        write_rules.pop(p, None)
        write_rules[p] = 'deny'

    for ag in ('AGENTS.md', '*/AGENTS.md', str(ws_res / 'AGENTS.md'), str(workspace / 'AGENTS.md')):
        edit_rules.pop(ag, None)
        edit_rules[ag] = 'deny'
        write_rules.pop(ag, None)
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
        **secrets_rules
    }

    permission = {
        '*': 'deny',
        'read': read_rules,
        'edit': edit_rules,
        'write': write_rules,
        'bash': bash_rules,
        'glob': 'allow',
        'grep': 'allow',
        'list': 'allow',
        'todowrite': 'allow',
        'task': 'deny',
        'question': 'deny',
        'webfetch': 'deny',
        'websearch': 'deny',
        'google_search': 'deny',
        'lsp': 'deny',
        'external_directory': {
            '*': 'deny',
            str(ws_res) + '/*': 'allow',
            str(ws_res): 'allow',
            str(sk_res) + '/*': 'allow',
            str(sk_res): 'allow',
            str(workspace) + '/*': 'allow',
            str(workspace): 'allow',
            str(skills) + '/*': 'allow',
            str(skills): 'allow'
        },
        'skill': {'*': 'deny'}
    }

    if arm != 'build_sin_mas':
        permission['skill'].update({'data-api': 'allow', 'ui-design': 'allow'})
        if not arm.startswith('build_'):
            permission['skill'][primary_skill(arm)] = 'allow'

    agent = {'model': model, 'steps': STEP_LIMIT, 'temperature': 0.2, 'permission': permission}
    if not arm.startswith('build_'):
        agent.update(mode='primary', description='Frozen experimental snapshot: ' + arm,
                     prompt=(profile / 'agent.md').read_text())

    return {
        '$schema': 'https://opencode.ai/config.json',
        'share': 'disabled',
        'snapshot': False,
        'autoupdate': False,
        'formatter': False,
        'lsp': False,
        'plugin': [],
        'mcp': {},
        'instructions': [] if arm == 'build_sin_mas' else [str(workspace / 'AGENTS.md')],
        'skills': {'paths': [str(skills)]},
        'agent': {agent_name(arm): agent}
    }


def make_environment(root, task_id, arm, cfg):
    env = dict(os.environ)
    for name in list(env):
        if name.startswith('OPENCODE_CONFIG') or name == 'OPENCODE_PURE':
            del env[name]
    env.update(
        OPENCODE_CONFIG_CONTENT=json.dumps(cfg),
        OPENCODE_DISABLE_PROJECT_CONFIG='1',
        OPENCODE_DISABLE_EXTERNAL_SKILLS='1',
        OPENCODE_DISABLE_CLAUDE_CODE='1',
        OPENCODE_DISABLE_CLAUDE_CODE_SKILLS='1',
        OPENCODE_DISABLE_CLAUDE_CODE_PROMPT='1',
        OPENCODE_DISABLE_AUTOUPDATE='1',
        JAVA_HOME=JAVA_HOME,
        ANDROID_HOME=ANDROID_HOME,
        PATH=f"{JAVA_HOME}/bin:{env.get('PATH', '')}"
    )
    return env


def execute_arm(root, task_id, arm, model):
    task_meta = TASKS[str(task_id)]
    prompt_text = task_meta['file'].read_text(encoding='utf-8')
    prompt_text += (
        "\n\nPLAN TÉCNICO APROBADO POR EL USUARIO: El usuario ha aprobado formalmente el plan y la arquitectura. "
        "Estás en modo IMPLEMENTACIÓN directa tras aprobación. Implementa inmediatamente el código y los tests en los archivos requeridos "
        "usando la herramienta write o edit. Ejecuta la verificación con ./gradlew y concluye sin exploraciones innecesarias de otros módulos."
    )
    task_dir = root / f'task_{task_id}'
    workspace = task_dir / 'runs' / arm

    cfg = configuration(root, task_id, arm, model)
    write_json(task_dir / 'configs' / f'{arm}.json', cfg)

    env = make_environment(root, task_id, arm, cfg)
    args = [
        CLI, 'run', '--format', 'json',
        '--title', f"TASK-{task_id}-{arm}",
        '--model', model,
        '--agent', agent_name(arm),
        '--dir', str(workspace),
        prompt_text
    ]

    started = time.monotonic()
    proc = subprocess.Popen(args, cwd=str(workspace), env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    events = []
    total_tokens = {'total': 0, 'input': 0, 'output': 0, 'reasoning': 0, 'cache_read': 0, 'cache_write': 0}
    tools_called = 0
    steps = 0
    soft_stop_reason = None
    conversation_error = None

    try:
        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except Exception:
                continue
            events.append(ev)
            ev_type = ev.get('type')
            if ev_type == 'tool_use':
                tools_called += 1
            elif ev_type == 'step_start':
                steps += 1
            elif ev_type == 'step_finish':
                part = ev.get('part', {})
                toks = part.get('tokens', {})
                for k in ('total', 'input', 'output', 'reasoning'):
                    total_tokens[k] += toks.get(k, 0)
                cache = toks.get('cache', {})
                total_tokens['cache_read'] += cache.get('read', 0)
                total_tokens['cache_write'] += cache.get('write', 0)
                if part.get('reason'):
                    soft_stop_reason = part.get('reason')
            elif ev_type == 'error':
                conversation_error = ev.get('error')

        proc.wait(timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        proc.kill()
        soft_stop_reason = 'timeout'

    elapsed = round(time.monotonic() - started, 3)

    run_record = {
        'task_id': task_id,
        'task_name': task_meta['id'],
        'arm': arm,
        'model': model,
        'steps': steps,
        'tools_called': tools_called,
        'tokens': total_tokens,
        'duration_seconds': elapsed,
        'soft_stop_reason': soft_stop_reason,
        'error': conversation_error,
        'exit_code': proc.returncode,
        'completed_at': stamp()
    }

    write_json(task_dir / 'evidence' / f'{arm}-run.json', run_record)
    return run_record


def evaluate_arm(root, task_id, arm):
    task_meta = TASKS[str(task_id)]
    task_dir = root / f'task_{task_id}'
    workspace = task_dir / 'runs' / arm

    target_oracle = workspace / task_meta['oracle_target']
    target_oracle.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(task_meta['oracle_source'], target_oracle)

    env = dict(os.environ)
    env['JAVA_HOME'] = JAVA_HOME
    env['ANDROID_HOME'] = ANDROID_HOME
    env['PATH'] = f"{JAVA_HOME}/bin:{env.get('PATH', '')}"

    try:
        oracle_cmd = f"./gradlew {task_meta['gradle_oracle_task']} --console=plain"
        res_oracle = subprocess.run(oracle_cmd, shell=True, cwd=str(workspace), env=env,
                                    capture_output=True, text=True, timeout=300)
        oracle_pass = (res_oracle.returncode == 0)
    finally:
        if target_oracle.exists():
            target_oracle.unlink()

    original_cmd = f"./gradlew {task_meta['gradle_original_task']} --console=plain"
    res_orig = subprocess.run(original_cmd, shell=True, cwd=str(workspace), env=env,
                              capture_output=True, text=True, timeout=300)
    original_pass = (res_orig.returncode == 0)

    res_diff = subprocess.run(['git', 'status', '--porcelain'], cwd=str(workspace),
                              capture_output=True, text=True)
    diff_output = res_diff.stdout

    test_files_added = len(re.findall(r'Test\.kt', diff_output))

    eval_record = {
        'task_id': task_id,
        'arm': arm,
        'oracle_pass': oracle_pass,
        'original_suite_pass': original_pass,
        'functional_acceptance': (oracle_pass and original_pass),
        'new_tests_found': test_files_added,
        'diff_summary': diff_output.splitlines()[:20]
    }
    if not oracle_pass:
        eval_record['oracle_error'] = (res_oracle.stdout + '\n' + res_oracle.stderr)[-1500:]
    if not original_pass:
        eval_record['original_error'] = (res_orig.stdout + '\n' + res_orig.stderr)[-1500:]

    write_json(task_dir / 'evidence' / f'{arm}-eval.json', eval_record)
    return eval_record


def build_summary(root, task_ids):
    results = {}
    for tid in task_ids:
        t_meta = {k: (str(v) if isinstance(v, Path) else v) for k, v in TASKS[str(tid)].items()}
        t_results = {}
        for arm in ARMS:
            run_file = root / f'task_{tid}' / 'evidence' / f'{arm}-run.json'
            eval_file = root / f'task_{tid}' / 'evidence' / f'{arm}-eval.json'
            if run_file.exists() and eval_file.exists():
                r_data = read_json(run_file)
                e_data = read_json(eval_file)
                t_results[arm] = {**r_data, **e_data}
        results[str(tid)] = {
            'metadata': t_meta,
            'arms': t_results
        }
    return results


def main():
    parser = argparse.ArgumentParser(description="Proyecto Real Android CRM — Multi-Model Benchmark Runner")
    parser.add_argument('--model', default='github-copilot/mai-code-1.1-flash', help="Identificador del modelo en OpenCode")
    parser.add_argument('--tasks', nargs='+', default=['1', '2'], help="Tareas a ejecutar (ej: 1 2)")
    parser.add_argument('--arms', nargs='+', default=list(ARMS), help="Brazos a evaluar")
    parser.add_argument('--root', type=Path, default=DEFAULT_ROOT, help="Directorio temporal del laboratorio")
    parser.add_argument('--output-dir', type=Path, default=None, help="Directorio para guardar resultados.json y evidencia")
    parser.add_argument('--prepare-only', action='store_true', help="Solo preparar workspaces sin llamar al modelo")
    parser.add_argument('--eval-only', action='store_true', help="Solo evaluar workspaces existentes")
    args = parser.parse_args()

    task_ids = args.tasks
    arms = args.arms
    root = args.root.resolve()
    model = args.model
    output_dir = args.output_dir.resolve() if args.output_dir else (SPEC_DIR.parent / f'real-android-{model.replace("/", "_")}')

    print(f"=== INICIANDO BENCHMARK MULTI-MODELO REAL ANDROID CRM ===")
    print(f"Modelo: {model} | Tareas: {task_ids} | Brazos: {arms}")
    print(f"Root: {root} | Salida: {output_dir}")

    for tid in task_ids:
        print(f"\n--- Procesando Tarea {tid}: {TASKS[tid]['title']} ---")
        for arm in arms:
            if not args.eval_only:
                print(f"\n> [Tarea {tid}] Preparando workspace para brazo: {arm}")
                prepare_workspace(root, tid, arm)

            if args.prepare_only:
                print(f"  Preparación completa para {arm}. Saltando inferencia.")
                continue

            if not args.eval_only:
                print(f"  Ejecutando inferencia CLI con {model} ({arm})...")
                run_res = execute_arm(root, tid, arm, model)
                print(f"  Inferencia finalizada: {run_res['duration_seconds']}s, {run_res['tokens']['total']} tokens, steps: {run_res['steps']}.")

            print(f"  Evaluando brazo {arm} con oráculo externo...")
            eval_res = evaluate_arm(root, tid, arm)
            print(f"  Resultado evaluación: Oráculo={eval_res['oracle_pass']}, Original={eval_res['original_suite_pass']}, Aceptación={eval_res['functional_acceptance']}")

            # Guardar snapshot acumulado de resultados y evidencia
            summary = build_summary(root, task_ids)
            write_json(output_dir / 'resultados.json', summary)
            
            # Persistir evidencia en output_dir
            ev_src = root / f'task_{tid}' / 'evidence'
            ev_dest = output_dir / f'task_{tid}' / 'evidence'
            if ev_src.exists():
                ev_dest.parent.mkdir(parents=True, exist_ok=True)
                if ev_dest.exists():
                    shutil.rmtree(ev_dest)
                shutil.copytree(ev_src, ev_dest)

    summary = build_summary(root, task_ids)
    summary_path = output_dir / 'resultados.json'
    write_json(summary_path, summary)
    print(f"\nResumen consolidado guardado en: {summary_path}")


if __name__ == '__main__':
    main()
