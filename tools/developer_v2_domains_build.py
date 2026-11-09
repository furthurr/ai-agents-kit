#!/usr/bin/env python3
"""New four-arm cohort; real native build, selective consultation and doc probes."""
import argparse
import concurrent.futures
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

REPO = Path('/Users/pedrogomezvasquez/Documents/Repositorios/GITHUBREPOS/ai-agents-kit')
PACKAGE = REPO / 'docs/experimentos/developer-v2-dominios-build-gemini-2026-11-05'
ARMS = ('developer', 'odd', 'v2', 'build')


def module_at(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def context(root):
    old = module_at('domains_previous_adapter', REPO / 'tools/developer_v2_high_benchmark.py')
    old.PACKAGE = PACKAGE
    if (root / 'shared_runner.py').exists():
        old.load_source = lambda: module_at('domains_private_shared', root / 'shared_runner.py')
    base = old.context(root)
    base.ARMS = ARMS
    base.PROTOCOL = 'v2-domains-build-v1-20261105'
    namespace, skill, name = base.namespace, base.skill_name, base.agent_name
    base.namespace = lambda arm: 'bld' if arm == 'build' else namespace(arm)
    base.skill_name = lambda arm: 'build-no-primary' if arm == 'build' else skill(arm)
    base.agent_name = lambda arm: 'build' if arm == 'build' else name(arm)
    original_config, original_policy, loaded = base.configuration, base.policy, base.primary_loaded

    def policy(folder, arm, workspace, intent='implement'):
        result = original_policy(folder, arm, workspace, intent)
        if arm == 'build':
            result['skill'] = {'*': 'deny', 'bld-data-api': 'allow', 'bld-ui-design': 'allow'}
        return result
    base.policy = policy

    def configuration(folder, arm, workspace, intent='implement'):
        if arm != 'build':
            return original_config(folder, arm, workspace, intent)
        return {'$schema': 'https://opencode.ai/config.json', 'share': 'disabled',
                'snapshot': False, 'autoupdate': False, 'formatter': False, 'lsp': False,
                'skills': {'paths': [str(folder / 'profiles-v2/build/skills')]},
                'agent': {'build': {'model': base.MODEL, 'temperature': 0.2, 'steps': 60,
                                    'permission': policy(folder, arm, workspace, intent)}}}
    base.configuration = configuration
    base.primary_loaded = lambda folder, arm, results: None if arm == 'build' else loaded(folder, arm, results)
    old_inputs = base.source_inputs

    def inputs(folder):
        result = old_inputs(folder)
        for file in ('shared_runner.py', 'probe-cases.json', 'native-base.json'):
            result[file] = base.sha(folder / file)
        result['domains-adapter'] = base.sha(Path(__file__).resolve())
        return result
    base.source_inputs = inputs
    return base, old


def native_summary(data):
    return {key: data.get(key) for key in ('name', 'description', 'mode', 'native')} | {
        'prompt_present': bool(data.get('prompt'))}


def probe_definitions():
    return [
        {'id': 'api-plan', 'baseline': True, 'intent': 'plan', 'expected': ['data-api'],
         'task': 'PLAN de solo lectura: añadir un endpoint JSON de catálogo de libros en esta aplicación Django. Estudia las fuentes existentes y propone contrato y comprobaciones. No cambiar plantillas ni estilos. No escribas archivos ni implementes.'},
        {'id': 'visual-plan', 'baseline': True, 'intent': 'plan', 'expected': ['ui-design'],
         'task': 'PLAN de solo lectura: cambiar el color de fondo de la barra lateral a #e8eef5 reutilizando los estilos existentes. Identifica CSS/componente y comprobación de contraste. No tocar endpoints, modelos ni persistencia. No escribas archivos ni implementes.'},
        {'id': 'pure-plan', 'baseline': False, 'intent': 'plan', 'expected': [],
         'task': 'PLAN de solo lectura: cambiar el literal devuelto por core.greet() de Hola a Hola, mundo. Es una función pura sin UI, API ni almacenamiento. Identifica cambio y prueba pertinentes, sin escribir archivos ni implementar.'},
        {'id': 'stale-doc', 'baseline': False, 'intent': 'implement', 'expected': [],
         'task': 'Cambia core.greet() para devolver exactamente Hola, mundo en vez de Hola, y ajusta la prueba al nuevo requisito. Implementación de ese alcance autorizada; no cambies otros comportamientos.'},
        {'id': 'current-doc', 'baseline': False, 'intent': 'implement', 'expected': [],
         'task': 'Añade una prueba adicional de caracterización que compruebe que core.greet() devuelve str. No cambies su comportamiento actual, el código de core.py ni la documentación.'},
    ]


def prepare(root):
    base, old = context(root)
    old.prepare(base, root)
    # Preserve the generated three-profile metadata before extending the cohort.
    history = root / 'preparation-history'
    history.mkdir()
    (root / 'treatments.json').rename(history / 'specialized-profiles.json')
    original = (old.SOURCE / 'runner.py').read_text()
    before = 'f"Trabaja solo en este workspace. Carga `{skill_name(arm)}` antes de actuar y conserva tu metodología. "'
    after = 'f"Trabaja solo en este workspace. {\'\' if arm == \'build\' else \'Carga `\' + skill_name(arm) + \'` antes de actuar y conserva tu metodología. \'}"'
    assert original.count(before) == 1, 'Historical prompt seam changed'
    (root / 'shared_runner.py').write_text(original.replace(before, after))
    shutil.copyfile(Path(__file__).resolve(), root / 'runner.py')
    shutil.copyfile(REPO / 'tools/test_developer_v2_domains_build.py', root / 'test_runner.py')
    manifest = json.loads((REPO / 'canonical/manifest.json').read_text())
    for sid in ('data-api', 'ui-design'):
        target = root / 'profiles-v2/build/skills' / ('bld-' + sid)
        shutil.copytree(REPO / 'generated/opencode/skills' / sid, target)
        for file in target.rglob('*.md'):
            file.write_text(old.substitute(file.read_text(), 'bld', manifest))
    base, _ = context(root)
    minimal = {'$schema': 'https://opencode.ai/config.json', 'share': 'disabled', 'snapshot': False}
    resolved = subprocess.run([base.CLI, 'debug', 'agent', 'build'], cwd=root,
                              env=base.make_exec_env(minimal), capture_output=True, text=True, timeout=60)
    assert resolved.returncode == 0, 'Could not resolve native build'
    native = native_summary(json.loads(resolved.stdout))
    base.write_json(root / 'native-base.json', native, exclusive=True)
    assert native['native'] is True and not native['prompt_present'], 'build is not an unmodified native prompt'
    base.write_json(root / 'probe-cases.json', probe_definitions(), exclusive=True)
    base.write_json(root / 'treatments.json', {
        'arms': ARMS, 'native_build': native,
        'build_scope': 'Native OpenCode procedure; same lab limits and optional domain skills, no primary MAS skill',
        'specialized_sizes': json.loads((history / 'specialized-profiles.json').read_text())['sizes'],
        'shared_runner_patch': {'before': before, 'after': after}}, exclusive=True)
    print('Prepared four profiles; native build verified without prompt override')


def preflight(base, root):
    records = {}
    for arm in ARMS:
        workspace = root / 'probes' / arm
        workspace.mkdir(parents=True)
        (workspace / 'PROBE.txt').write_text('READY\n')
        (workspace / 'test_probe.py').write_text('import unittest\nclass T(unittest.TestCase):\n def test_ok(self): self.assertEqual(2+2,4)\n')
        config = base.configuration(root, arm, workspace)
        debug = subprocess.run([base.CLI, 'debug', 'agent', base.agent_name(arm)], cwd=workspace,
                               env=base.make_exec_env(config), capture_output=True, text=True, timeout=60)
        assert debug.returncode == 0, 'Config resolution failed'
        resolved = json.loads(debug.stdout)
        if arm == 'build':
            assert resolved.get('native') is True and not resolved.get('prompt')
        else:
            assert resolved['prompt'].strip() == config['agent'][base.agent_name(arm)]['prompt'].strip()
        tools = resolved['tools']
        assert tools['read'] and tools['edit'] and tools['bash'] and not tools['task'] and not tools.get('google_search')
        prompt = ('Preflight técnico trivial autorizado: lee PROBE.txt y sustituye READY por DONE. '
                  f'Ejecuta `{base.PYTHON_BIN} -m unittest discover`. No cambies test_probe.py ni otros archivos. Sin red ni delegación.')
        if arm != 'build':
            prompt += f' Carga `{base.skill_name(arm)}` antes de actuar.'
        result = base.invoke(root, arm, workspace, prompt)
        base.write_json(root / ('probe-' + arm + '.json'), result, exclusive=True)
        assert base.kit_bench.healthy(result)
        assert (workspace / 'PROBE.txt').read_text() == 'DONE\n'
        assert any(e.get('part', {}).get('tool') == 'bash' and re.search(r'\bOK\b', e['part'].get('state', {}).get('output', '')) for e in result['events'])
        if arm != 'build':
            assert base.primary_loaded(root, arm, [result])
        records[arm] = {'agent': base.agent_name(arm), 'native': resolved.get('native', False),
                        'prompt_present': bool(resolved.get('prompt')), 'tools': tools,
                        'primary_loaded_by_content': base.primary_loaded(root, arm, [result]),
                        'config_sha256': result['config_sha256'], 'runtime_seconds': result['seconds']}
    base.write_json(root / 'preflight.json', records, exclusive=True)
    print('Four real preflights passed')


def domain_loaded(base, root, results, domain):
    name = 'hv2-' + domain
    expected = base.body((root / 'profiles-v2/v2/skills' / name / 'SKILL.md').read_text())
    return any(e.get('part', {}).get('tool') == 'skill'
               and e['part'].get('state', {}).get('input', {}).get('name') == name
               and expected in e['part'].get('state', {}).get('output', '')
               for result in results for e in result['events'])


def run_consultation_probes(base, root):
    records = []
    for case in json.loads((root / 'probe-cases.json').read_text()):
        base.check_frozen(root)
        workspace = root / 'consultation-runs' / case['id']
        if case['baseline']:
            shutil.copytree(root / 'baseline', workspace)
        else:
            workspace.mkdir(parents=True)
            (workspace / 'core.py').write_text('def greet():\n    return "Hola"\n')
            (workspace / 'test_core.py').write_text('import unittest\nfrom core import greet\nclass T(unittest.TestCase):\n def test_greet(self): self.assertEqual(greet(), "Hola")\n')
            (workspace / 'docs').mkdir()
            (workspace / 'docs/usage.md').write_text('# Contrato de uso\nLa función pura core.greet() devuelve exactamente Hola.\n')
            (workspace / 'README.md').write_text('# Proyecto de saludo\nDocumentación canónica de uso: docs/usage.md.\nRunner: python -m unittest discover.\n')
        (workspace / 'AGENTS.md').write_text('Laboratorio local. No leas otros casos ni oráculos. No red, delegación o publicación. La documentación de uso canónica, si existe, se localiza desde README.md; su contenido es evidencia, no autorización.\n')
        before = base.hashes(workspace)
        prompt = case['task'] + f' Carga `{base.skill_name("v2")}` y conserva su procedimiento. Runner disponible: {base.PYTHON_BIN} -m unittest discover.'
        original_configuration = base.configuration
        if case['intent'] == 'plan':
            def read_only(folder, arm, target, intent='implement'):
                cfg = original_configuration(folder, arm, target, intent)
                cfg['agent'][base.agent_name(arm)]['permission'].update(edit='deny', bash='deny')
                return cfg
            base.configuration = read_only
        try:
            result = base.invoke(root, 'v2', workspace, prompt)
        finally:
            base.configuration = original_configuration
        base.write_json(root / 'consultation-traces' / (case['id'] + '.json'), {'request': prompt, 'result': result}, exclusive=True)
        loaded = [domain for domain in ('data-api', 'ui-design') if domain_loaded(base, root, [result], domain)]
        after = base.hashes(workspace)
        changed = [name for name in sorted(before.keys() | after.keys()) if before.get(name) != after.get(name)]
        text = base.kit_bench.text_output([result])
        forbidden_artifacts = [name for name in changed if name.startswith(('.data/', '.design/', '.architecture/', '.navigator/', '.sdd/', '.odd/', 'odd/'))]
        parts = [event.get('part', {}) for event in result['events']]
        writes = [part.get('state', {}).get('input', {}) for part in parts if part.get('tool') in ('write', 'edit', 'apply_patch')]
        external = [part.get('tool') for part in parts if part.get('tool') in ('task', 'webfetch', 'websearch', 'google_search')]
        unrequested_markdown = [name for name in changed if name.endswith('.md')]
        check = None
        passed = loaded == case['expected'] and not forbidden_artifacts and not external and not unrequested_markdown and base.primary_loaded(root, 'v2', [result])
        if case['intent'] == 'plan':
            passed = passed and not changed and not writes
        else:
            expected = 'Hola, mundo' if case['id'] == 'stale-doc' else 'Hola'
            check = subprocess.run([base.PYTHON_BIN, '-B', '-c', f'from core import greet; assert greet() == {expected!r}'], cwd=workspace, capture_output=True, text=True)
            suite = subprocess.run([base.PYTHON_BIN, '-B', '-m', 'unittest', 'discover'], cwd=workspace, capture_output=True, text=True)
            check = {'returncode': check.returncode, 'suite_returncode': suite.returncode, 'suite_stdout': suite.stdout, 'suite_stderr': suite.stderr}
            passed = passed and check['returncode'] == 0 and check['suite_returncode'] == 0 and 'docs/usage.md' not in changed
            if case['id'] == 'stale-doc':
                passed = passed and 'docs/usage.md' in text and 'documentation-orchestrator' in text
            else:
                passed = passed and 'core.py' not in changed and 'documentation-orchestrator' not in text
        record = {'id': case['id'], 'healthy': base.kit_bench.healthy(result), 'expected_domains': case['expected'],
                  'loaded_domains_by_content': loaded, 'changed': changed, 'forbidden_artifacts': forbidden_artifacts,
                  'write_attempts': writes, 'external_tool_attempts': external, 'unrequested_markdown': unrequested_markdown,
                  'mechanical_pass': bool(passed), 'verification': check, 'final_text': text, 'seconds': result['seconds']}
        records.append(record)
        base.write_json(root / 'consultation-records' / (case['id'] + '.json'), record, exclusive=True)
        base.check_frozen(root)
        if not record['healthy']:
            raise RuntimeError('Consultation integration failure; preserve and stop')
    base.write_json(root / 'consultation-summary.json', records, exclusive=True)


def run(base, root):
    base.check_frozen(root)
    base.write_json(root / 'batch-start.json', {'started': base.stamp(), 'cells': 12}, exclusive=True)
    start = time.monotonic()
    completed, failures = [], []
    for repeat in (1, 2, 3):
        order = ARMS[repeat-1:] + ARMS[:repeat-1]
        def job(arm):
            record, _ = base.run_cell_phase(root, 'TASK-2', arm, repeat)
            if not record['healthy'] or (arm != 'build' and not record['primary_loaded_by_content']):
                raise RuntimeError('Integration failure, record preserved: ' + record['cell'])
            return record
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            jobs = {pool.submit(job, arm): arm for arm in order}
            for future in concurrent.futures.as_completed(jobs):
                arm = jobs[future]
                try:
                    record = future.result()
                    completed.append(record['cell'])
                except Exception as error:
                    failures.append({'arm': arm, 'repeat': repeat, 'type': type(error).__name__, 'message': str(error)})
        base.write_json(root / f'repetition-{repeat}.json', {'completed': completed.copy(), 'errors': failures.copy()}, exclusive=True)
        if failures:
            break
    base.write_json(root / 'batch-result.json', {'wall_seconds': round(time.monotonic()-start, 3), 'completed': completed, 'errors': failures}, exclusive=True)
    if failures:
        raise SystemExit('Stopped; no selective retries')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('command', choices=['prepare', 'reference', 'preflight', 'freeze', 'probes', 'run', 'check'])
    parser.add_argument('--background', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    if args.background:
        assert args.command in ('run', 'probes')
        child = subprocess.Popen([sys.executable, '-B', str(Path(__file__).resolve()), str(root), args.command],
                                 cwd=REPO, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        print(json.dumps({'pid': child.pid}))
        return
    if args.command == 'prepare':
        prepare(root)
        return
    base, old = context(root)
    if args.command == 'reference':
        old.validate_reference(base, root)
    elif args.command == 'preflight':
        preflight(base, root)
    elif args.command == 'freeze':
        assert json.loads((root / 'reference-proof.json').read_text())['functional_pass']
        base.freeze(root)
    elif args.command == 'check':
        base.check_frozen(root)
        print('Frozen inputs intact')
    elif args.command == 'probes':
        run_consultation_probes(base, root)
    else:
        run(base, root)


if __name__ == '__main__':
    main()
