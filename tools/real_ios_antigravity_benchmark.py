#!/usr/bin/env python3
"""Benchmark arnés para Proyecto Real iOS CRM con Gemini 3.8 Flash (Antigravity Nativo).

Utiliza la herramienta oficial y nativa de Google Antigravity:
  ~/.gemini/antigravity/bin/agentapi (Google DeepMind Language Server)
para ejecutar los 5 perfiles metodológicos sobre las 3 tareas iOS sin terceros:
  1. build_sin_mas: Main agent sin documentación MAS (control)
  2. build_mas: Main agent con documentación MAS
  3. developer_actual: Agente Developer v1 canónico instalado
  4. v2: Developer v2 candidato2 (modular con dominios)
  5. v2_reforzado: Agente Developer evolucionado con los 2 refuerzos ODD
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
BASE_ZIP = Path(os.environ.get("MOBILE_BENCHMARK_IOS_ARCHIVE",
    str(Path.home() / ".local/share/ai-agents-kit/fixtures/mobile-ios.zip")))
EXP_DIR = REPO / 'docs/experimentos/real-ios-gemini-antigravity-2026-11-09'
DEFAULT_ROOT = Path('/tmp/real-ios-benchmark')

AGENTAPI = Path.home() / '.gemini/antigravity/bin/agentapi'
BRAIN_DIR = Path.home() / '.gemini/antigravity/brain'

TIMEOUT = 1800
ARMS = ('v2_reforzado', 'developer_actual', 'v2', 'build_mas', 'build_sin_mas')

DELTA_A = ('Vincula los criterios afectados con pruebas o checks observables, sin casos de relleno. '
           'Cuando modifiques código compartido, contrasta con el baseline disponible el comportamiento '
           'existente que no se pidió cambiar y añade regresión para protegerlo.')
DELTA_B = ('Al reanudar, contrasta el registro con el código y las verificaciones disponibles antes de '
           'continuar; los estados guardados no sustituyen evidencia vigente. Si cambia un requisito, '
           'actualiza su literal y reabre solo el trabajo afectado.')

SECRETS = ('*.env*', '*.pem', '*.key', '*.p12', '*.pfx', '*.mobileprovision', '*credential*',
           '*.secret*', '*/.ssh/*', '*/.aws/*', '*/.config/gh/*', '*/auth.json')

TASKS = {
    '1': {
        'id': 'GIOS-SEARCH-PROSPECTS',
        'title': 'Media-Baja — Búsqueda, Filtrado y Normalización de Prospectos',
        'complexity': 'media-baja',
        'file': EXP_DIR / 'tarea-1-media-baja.md',
        'oracle_source': EXP_DIR / 'oraculos/OracleSearchProspectsTests.swift',
        'oracle_target': 'FixtureProject/FixtureProject Tests/Domain/OracleSearchProspectsTests.swift',
        'xcode_oracle_test': 'FixtureProject Tests/OracleSearchProspectsTests',
        'xcode_original_test': 'FixtureProject Tests/FixtureComponent1Tests',
    },
    '2': {
        'id': 'GIOS-BUZON-RETRY-UI',
        'title': 'Media-Alta — Remediación QLT-0017 y Gestión de Altas en Conflicto',
        'complexity': 'media-alta',
        'file': EXP_DIR / 'tarea-2-media-alta.md',
        'oracle_source': EXP_DIR / 'oraculos/OracleBuzonRetryUiTests.swift',
        'oracle_target': 'FixtureProject/FixtureProject Tests/Presentacion/OracleBuzonRetryUiTests.swift',
        'xcode_oracle_test': 'FixtureProject Tests/OracleBuzonRetryUiTests',
        'xcode_original_test': 'FixtureProject Tests/FixtureComponent1Tests',
    },
    '3': {
        'id': 'GIOS-QUEUE-CONCURRENCY-CIPHER',
        'title': 'Alta — Deduplicación Atómica, Concurrencia y Cifrado en Cola Offline',
        'complexity': 'alta',
        'file': EXP_DIR / 'tarea-3-alta.md',
        'oracle_source': EXP_DIR / 'oraculos/OracleQueueConcurrencyCipherTests.swift',
        'oracle_target': 'FixtureProject/FixtureProject Tests/App/ViewModels/OracleQueueConcurrencyCipherTests.swift',
        'xcode_oracle_test': 'FixtureProject Tests/OracleQueueConcurrencyCipherTests',
        'xcode_original_test': 'FixtureProject Tests/FixtureComponent1Tests',
    }
}


def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def write_json(path, data, exclusive=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x' if exclusive else 'w', encoding='utf-8') as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write('\n')


def read_json(path):
    with path.open('r', encoding='utf-8') as handle:
        return json.load(handle)


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
    unzipped = temp_dir / 'app-crm-ios-enterprise'
    shutil.move(str(unzipped), str(target_dir))
    shutil.rmtree(temp_dir)


def fix_deployment_target(workspace):
    pbxproj = workspace / 'FixtureProject/FixtureProject.xcodeproj/project.pbxproj'
    if pbxproj.exists():
        content = pbxproj.read_text(encoding='utf-8')
        # Ajustar deployment target a 26.1 para compatibilidad exacta con el simulador instalado
        updated = re.sub(r'IPHONEOS_DEPLOYMENT_TARGET = 26\.2;', 'IPHONEOS_DEPLOYMENT_TARGET = 26.1;', content)
        pbxproj.write_text(updated, encoding='utf-8')


def prepare_workspace(root, task_id, arm):
    task_dir = root / f'task_{task_id}'
    workspace = task_dir / 'runs' / arm

    if workspace.exists():
        shutil.rmtree(workspace)

    extract_base_project(workspace)
    fix_deployment_target(workspace)

    mas_folders = ['.architecture', '.data', '.design', '.quality', '.security', '.navigator', '.sdd']
    if arm == 'build_sin_mas':
        agents_md = workspace / 'AGENTS.md'
        if agents_md.exists():
            agents_md.unlink()
        for folder in mas_folders:
            p = workspace / folder
            if p.exists():
                shutil.rmtree(p)

    # Inicializar commit base limpio para aislar con precisión el diff del agente
    subprocess.run(['git', 'config', 'user.name', 'Benchmark Runner'], cwd=str(workspace), capture_output=True)
    subprocess.run(['git', 'config', 'user.email', 'benchmark@test.local'], cwd=str(workspace), capture_output=True)
    subprocess.run(['git', 'add', '-A'], cwd=str(workspace), capture_output=True)
    subprocess.run(['git', 'commit', '-m', 'chore: baseline benchmark setup', '--allow-empty'], cwd=str(workspace), capture_output=True)


def build_system_instructions(arm, workspace):
    if arm == 'build_sin_mas':
        return (
            "Eres un agente general de desarrollo de software trabajando en un proyecto iOS con Swift y SwiftUI. "
            "Implementa el código y pruebas requeridas directamente en el workspace. No tienes acceso a documentación MAS."
        )
    elif arm == 'build_mas':
        return (
            "Eres un agente de desarrollo de software con acceso completo a la documentación del repositorio "
            f"({workspace}/.architecture, .data, .quality, .navigator). Consulta los índices y contratos del proyecto "
            "antes de implementar para respetar la arquitectura Clean + MVVM existente."
        )
    elif arm == 'developer_actual':
        return (
            "Eres el agente Developer canónico de Proyecto Real iOS CRM. Especializado en features completas de producto "
            "(UI SwiftUI, datos/APIs y lógica de negocio). Sigue arquitectura Clean + MVVM. "
            "PLAN TÉCNICO PRE-APROBADO: El usuario ya ha aprobado el plan técnico de implementación. "
            "Estás en modo IMPLEMENTACIÓN directa: escribe los archivos de código y pruebas inmediatamente sin pausas interactivas."
        )
    elif arm == 'v2':
        return (
            "Eres el agente Developer v2 (modular con dominios) de Proyecto Real iOS CRM. "
            "Aplica Clean Architecture + MVVM + Coordinator. "
            "Fase 1: Inspecciona contratos en Domain y Data. "
            "Fase 2: Implementa la lógica de negocio y UI respetando estrictamente los patrones del proyecto. "
            "Fase 3: Crea pruebas unitarias rigurosas en Swift Testing / XCTest y verifica que compilen limpiamente."
        )
    elif arm == 'v2_reforzado':
        return (
            "Eres el agente Developer v2 reforzado de Proyecto Real iOS CRM. "
            f"REGLA ODD DELTA A: {DELTA_A} "
            f"REGLA ODD DELTA B: {DELTA_B} "
            "Aplica Clean Architecture + MVVM + Coordinator con máxima disciplina DRY. "
            "Reutiliza la infraestructura existente sin sobre-ingeniería ni queries redundantes. "
            "Implementa el código en producción y añade suites exhaustivas de pruebas unitarias y de regresión."
        )
    return "Eres un agente de software para iOS."


def execute_arm_antigravity(root, task_id, arm):
    task_meta = TASKS[str(task_id)]
    task_dir = root / f'task_{task_id}'
    workspace = task_dir / 'runs' / arm

    task_spec = task_meta['file'].read_text(encoding='utf-8')
    sys_inst = build_system_instructions(arm, workspace)

    prompt = (
        f"<SYSTEM_INSTRUCTIONS>\n{sys_inst}\n</SYSTEM_INSTRUCTIONS>\n\n"
        f"<WORKSPACE_LOCATION>\nEl proyecto iOS está ubicado en: {workspace}\n"
        f"El archivo de proyecto Xcode es: {workspace}/FixtureProject/FixtureProject.xcodeproj\n"
        f"</WORKSPACE_LOCATION>\n\n"
        f"<TASK_SPECIFICATION>\n{task_spec}\n</TASK_SPECIFICATION>\n\n"
        "INSTRUCCIÓN DE EJECUCIÓN DIRECTA:\n"
        "1. Lee los archivos relevantes en el workspace usando read_file.\n"
        "2. Crea o edita los archivos de código y pruebas necesarios usando write_file o edit_file.\n"
        "3. Asegúrate de compilar y probar tus cambios usando run_command ejecutando xcodebuild.\n"
        "4. Al concluir, emite un resumen claro de los archivos modificados y da por finalizada la tarea."
    )

    started = time.monotonic()
    title = f"GIOS-{task_id}-{arm}"
    cmd = [
        str(AGENTAPI), 'new-conversation',
        '--model=flash',
        f'--title={title}',
        prompt
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"agentapi failed: {res.stderr}")

    api_resp = json.loads(res.stdout)
    conv_id = api_resp.get('response', {}).get('newConversation', {}).get('conversationId')
    if not conv_id:
        raise RuntimeError(f"No conversationId returned by agentapi: {res.stdout}")

    print(f"    Conversación Antigravity iniciada (ID: {conv_id}). Monitoreando ejecución...")

    # Monitorear finalización de la conversación en brain/
    log_file = BRAIN_DIR / conv_id / '.system_generated/logs/transcript.jsonl'
    tokens = {'total': 0, 'input': 0, 'output': 0, 'cache_read': 0}
    steps = 0
    tools_called = 0
    soft_stop_reason = 'unknown'

    wait_start = time.monotonic()
    idle_count = 0
    prev_line_count = 0

    while time.monotonic() - wait_start < TIMEOUT:
        time.sleep(5)
        if not log_file.exists():
            continue

        lines = log_file.read_text(encoding='utf-8').strip().splitlines()
        if not lines:
            continue

        cur_tokens = {'total': 0, 'input': 0, 'output': 0, 'cache_read': 0}
        cur_steps = 0
        cur_tools = 0
        last_ev = None

        for line in lines:
            try:
                ev = json.loads(line)
            except Exception:
                continue
            last_ev = ev
            if ev.get('type') == 'PLANNER_RESPONSE':
                cur_steps += 1
                inp = ev.get('input_tokens', 0)
                out = ev.get('output_tokens', 0)
                cache = ev.get('cache_read_tokens', 0)
                cur_tokens['input'] += inp
                cur_tokens['output'] += out
                cur_tokens['cache_read'] += cache
                cur_tokens['total'] += (inp + out)
                if ev.get('tool_calls'):
                    cur_tools += len(ev.get('tool_calls', []))

        tokens = cur_tokens
        steps = cur_steps
        tools_called = cur_tools

        # Verificar si el último evento fue una respuesta sin tool_calls y el proceso se ha estabilizado
        if last_ev and last_ev.get('type') == 'PLANNER_RESPONSE' and not last_ev.get('tool_calls') and cur_steps >= 1:
            if len(lines) == prev_line_count:
                idle_count += 1
                if idle_count >= 2:
                    soft_stop_reason = 'stop'
                    break
            else:
                idle_count = 1
        else:
            idle_count = 0

        prev_line_count = len(lines)

    elapsed = round(time.monotonic() - started, 3)

    run_record = {
        'task_id': task_id,
        'task_name': task_meta['id'],
        'arm': arm,
        'model': 'google/gemini-3.8-flash (Antigravity Native)',
        'conversation_id': conv_id,
        'steps': steps,
        'tools_called': tools_called,
        'tokens': tokens,
        'duration_seconds': elapsed,
        'soft_stop_reason': soft_stop_reason,
        'exit_code': 0,
        'completed_at': stamp()
    }

    write_json(task_dir / 'evidence' / f'{arm}-run.json', run_record)
    return run_record


def evaluate_arm_ios(root, task_id, arm):
    task_meta = TASKS[str(task_id)]
    task_dir = root / f'task_{task_id}'
    workspace = task_dir / 'runs' / arm
    project_dir = workspace / 'FixtureProject'

    target_oracle = workspace / task_meta['oracle_target']
    target_oracle.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(task_meta['oracle_source'], target_oracle)

    # 1. Ejecutar Oráculo Externo
    oracle_cmd = [
        'xcodebuild', 'test',
        '-scheme', 'FixtureProject',
        '-destination', 'platform=iOS Simulator,name=iPhone 17',
        f"-only-testing:{task_meta['xcode_oracle_test']}",
        'IPHONEOS_DEPLOYMENT_TARGET=26.1'
    ]

    try:
        res_oracle = subprocess.run(oracle_cmd, cwd=str(project_dir),
                                    capture_output=True, text=True, timeout=300)
        oracle_pass = (res_oracle.returncode == 0)
    except subprocess.TimeoutExpired:
        oracle_pass = False
        res_oracle = None
    finally:
        if target_oracle.exists():
            target_oracle.unlink()

    # 2. Ejecutar Suite Original para Verificar No-Regresión
    original_cmd = [
        'xcodebuild', 'test',
        '-scheme', 'FixtureProject',
        '-destination', 'platform=iOS Simulator,name=iPhone 17',
        f"-only-testing:{task_meta['xcode_original_test']}",
        'IPHONEOS_DEPLOYMENT_TARGET=26.1'
    ]

    try:
        res_orig = subprocess.run(original_cmd, cwd=str(project_dir),
                                  capture_output=True, text=True, timeout=300)
        original_pass = (res_orig.returncode == 0)
    except subprocess.TimeoutExpired:
        original_pass = False
        res_orig = None

    # 3. Comprobar archivos nuevos y conteo de LOC
    res_diff = subprocess.run(['git', 'status', '--porcelain'], cwd=str(workspace),
                              capture_output=True, text=True)
    diff_output = res_diff.stdout
    test_files_added = len(re.findall(r'Tests\.swift', diff_output))

    # LOC de producción vs tests
    prod_loc = 0
    test_loc = 0
    res_numstat = subprocess.run(['git', 'diff', '--numstat', 'HEAD'], cwd=str(workspace),
                                 capture_output=True, text=True)
    for line in res_numstat.stdout.splitlines():
        parts = line.strip().split('\t')
        if len(parts) >= 3:
            add = int(parts[0]) if parts[0].isdigit() else 0
            fname = parts[2]
            if 'Test' in fname:
                test_loc += add
            else:
                prod_loc += add

    # Sumar archivos no trackeados si los hubiera
    for line in diff_output.splitlines():
        if line.startswith('??'):
            fname = line[3:].strip()
            fpath = workspace / fname
            if fpath.is_file() and fname.endswith('.swift'):
                try:
                    c = len(fpath.read_text(encoding='utf-8').splitlines())
                    if 'Test' in fname:
                        test_loc += c
                    else:
                        prod_loc += c
                except Exception:
                    pass

    eval_record = {
        'task_id': task_id,
        'arm': arm,
        'oracle_pass': oracle_pass,
        'original_suite_pass': original_pass,
        'functional_acceptance': (oracle_pass and original_pass),
        'new_tests_found': test_files_added,
        'loc_added_prod': prod_loc,
        'loc_added_test': test_loc,
        'diff_summary': diff_output.splitlines()[:20]
    }

    if not oracle_pass and res_oracle:
        eval_record['oracle_error'] = (res_oracle.stdout + '\n' + res_oracle.stderr)[-1500:]
    if not original_pass and res_orig:
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
    parser = argparse.ArgumentParser(description="Proyecto Real iOS CRM — Gemini 3.8 Flash (Antigravity Native) Benchmark Runner")
    parser.add_argument('--tasks', nargs='+', default=['1', '2', '3'], help="Tareas a ejecutar (1: Media-Baja, 2: Media-Alta, 3: Alta)")
    parser.add_argument('--arms', nargs='+', default=list(ARMS), help="Brazos a evaluar")
    parser.add_argument('--root', type=Path, default=DEFAULT_ROOT, help="Directorio temporal del laboratorio")
    parser.add_argument('--prepare-only', action='store_true', help="Solo preparar workspaces sin inferencia")
    parser.add_argument('--eval-only', action='store_true', help="Solo evaluar con oráculos")
    args = parser.parse_args()

    task_ids = args.tasks
    arms = args.arms
    root = args.root.resolve()
    output_dir = EXP_DIR

    print("==================================================================")
    print(" INICIANDO BENCHMARK REAL IOS CRM")
    print(" Modelo: Gemini 3.8 Flash (Google Antigravity Nativo — Sin Copilot)")
    print(f" Tareas: {task_ids} | Brazos: {arms}")
    print(f" Root: {root} | Salida: {output_dir}")
    print("==================================================================")

    for tid in task_ids:
        print(f"\n--- Procesando Tarea {tid}: {TASKS[tid]['title']} ---")
        for arm in arms:
            if not args.eval_only:
                print(f"\n> [Tarea {tid}] Preparando workspace para brazo: {arm}...")
                prepare_workspace(root, tid, arm)

            if args.prepare_only:
                print(f"  Preparación completa para {arm}. Saltando inferencia.")
                continue

            if not args.eval_only:
                print(f"  Ejecutando inferencia con Gemini 3.8 Flash (Antigravity Nativo) [{arm}]...")
                try:
                    run_res = execute_arm_antigravity(root, tid, arm)
                    print(f"  Inferencia finalizada: {run_res['duration_seconds']}s, {run_res['tokens']['total']} tokens, steps: {run_res['steps']}.")
                except Exception as ex:
                    print(f"  ERROR en inferencia {arm}: {ex}")
                    evidence_dir = root / f'task_{tid}' / 'evidence'
                    evidence_dir.mkdir(parents=True, exist_ok=True)
                    write_json(evidence_dir / f'{arm}-run.json', {
                        'task_id': tid, 'arm': arm, 'error': str(ex), 'completed_at': stamp()
                    })

            print(f"  Evaluando brazo {arm} con oráculo externo Xcode...")
            try:
                eval_res = evaluate_arm_ios(root, tid, arm)
                print(f"  Resultado evaluación: Oráculo={eval_res['oracle_pass']}, Original={eval_res['original_suite_pass']}, Aceptación={eval_res['functional_acceptance']}")
            except Exception as ex:
                print(f"  ERROR en evaluación {arm}: {ex}")
                evidence_dir = root / f'task_{tid}' / 'evidence'
                evidence_dir.mkdir(parents=True, exist_ok=True)
                write_json(evidence_dir / f'{arm}-eval.json', {
                    'task_id': tid, 'arm': arm, 'oracle_pass': False, 'original_suite_pass': False,
                    'functional_acceptance': False, 'error': str(ex)
                })
            print(f"  Resultado evaluación: Oráculo={eval_res['oracle_pass']}, Original={eval_res['original_suite_pass']}, Aceptación={eval_res['functional_acceptance']}")

            # Guardar snapshot progresivo
            summary = build_summary(root, task_ids)
            write_json(output_dir / 'resultados.json', summary)

    summary = build_summary(root, task_ids)
    summary_path = output_dir / 'resultados.json'
    write_json(summary_path, summary)
    print(f"\nResumen consolidado guardado en: {summary_path}")


if __name__ == '__main__':
    main()
