#!/usr/bin/env python3
"""Offline harness regression tests: no providers, credentials or app ZIPs needed."""
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
import unicodedata
import zipfile

import mobile_benchmark_common as common
import mobile_benchmark_readonly as readonly
import subprocess
import shutil
import real_android_gemini_benchmark as android
import real_ios_antigravity_benchmark as ios

TMP = Path(tempfile.gettempdir()) / 'opencode'
TMP.mkdir(exist_ok=True)


class HarnessTests(unittest.TestCase):
    def test_failed_native_probe_prevents_model_call(self):
        ws, _, inputs, evidence = self.cell()
        (ws / 'Source.kt').write_text('class Source')
        manifest = common.read_json(inputs / 'manifest.json')
        manifest['workspace_baseline'] = common.snapshot(ws)
        common.write_json(inputs / 'manifest.json', manifest)
        fake = self.root / 'fake-cli'
        fake.write_text('#!/usr/bin/env python3\nimport sys\nfrom pathlib import Path\n'
                        'if "run" in sys.argv: Path("unexpected-inference").touch()\n'
                        'print("native tool unavailable")\n')
        fake.chmod(0o755)
        result = common.run_opencode(self.root, '1', 'v2_reforzado', 'android', fake,
                                     common.DEFAULT_MODEL, 30, 10, 1000)
        self.assertEqual(result['run_status'], 'tooling_error')
        self.assertFalse(result['attribution_ready'])
        self.assertEqual(result['model_calls'], 0)
        self.assertFalse((ws / 'unexpected-inference').exists())
        self.assertFalse((evidence / 'inference.stdout.log').exists())

    def test_observed_inspection_chains_with_restricted_entry_points(self):
        ws = self.root / 'workspace'
        source = ws / 'core/domain/src/FilterProspects.kt'
        source.parent.mkdir(parents=True)
        source.write_text('baseline')
        env = {**os.environ, 'GIT_CONFIG_GLOBAL': os.devnull, 'GIT_CONFIG_NOSYSTEM': '1',
               'BENCHMARK_GIT': shutil.which('git'), 'BENCHMARK_RG': str(common.readonly_rg())}
        for command in (['git', 'init', '--quiet'], ['git', 'add', '--all']):
            subprocess.run(command, cwd=ws, env=env, check=True, capture_output=True)
        bindir = self.root / 'bin'
        bindir.mkdir()
        for tool in ('git', 'ls', 'rg', 'head'):
            wrapper = bindir / tool
            wrapper.write_text('#!/bin/sh\nexec ' + __import__('shlex').join([
                sys.executable, str(Path(readonly.__file__).resolve()), str(ws), tool]) + ' "$@"\n')
            wrapper.chmod(0o755)
        env['PATH'] = str(bindir) + os.pathsep + env.get('PATH', '')
        for command in ('git status --short && git ls-files core/domain/src', 'pwd && ls',
                        'pwd && git status --short && ls',
                        "rg --files core/domain/src | rg 'kt$' | head -10"):
            result = subprocess.run(command, shell=True, cwd=ws, env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        result = subprocess.run('git status --short', shell=True, cwd=ws, env=env, capture_output=True, text=True)
        self.assertEqual(result.stdout, '')
        source.write_text('changed')
        result = subprocess.run("git status --short --untracked-files=all | rg 'FilterProspects|FixtureSource3|^\\?\\?'",
                                shell=True, cwd=ws, env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('FilterProspects.kt', result.stdout)
        for args in (['ls-files', '--exclude-from=/etc/passwd'], ['diff', '--output=/outside'],
                     ['diff', '--ext-diff'], ['ls-files', '../outside']):
            with patch('os.getcwd', return_value=str(ws)), self.assertRaises(ValueError):
                readonly.main(ws, 'git', args)

    def test_readonly_commands_reject_escape_secrets_and_execution(self):
        root = self.root.resolve()
        with patch('os.getcwd', return_value=str(root)):
            for value in ('../escape', '.env', 'test.key', 'local.properties'):
                with self.assertRaises(ValueError):
                    readonly.checked(root, value)
            for args in (['--pre', 'sh', 'pattern'], ['--pre=sh', 'pattern'], ['--files-from', '/etc/passwd']):
                with self.assertRaises(ValueError):
                    readonly.main(root, 'rg', args)

    def test_readonly_bare_ls_and_pipeline_rg(self):
        rg = str(common.readonly_rg())
        script = Path(readonly.__file__).resolve()
        (self.root / 'FilterProspects.kt').write_text('fixture')
        for command in ([sys.executable, str(script), str(self.root), 'ls'],
                        [sys.executable, str(script), str(self.root), 'rg', 'FilterProspects|FixtureSource3|^\\?\\?']):
            result = subprocess.run(command, cwd=self.root, input='?? FilterProspects.kt\n',
                                    capture_output=True, text=True, env={**os.environ, 'BENCHMARK_RG': rg})
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('FilterProspects.kt', result.stdout)

    def test_authorized_migration_preserves_every_other_statement(self):
        path = self.root / 'app/src/test/example/AccesoBuzonViewModelTest.kt'
        path.parent.mkdir(parents=True)
        old_name = 'un fallo de la cola deja el contador en cero'
        identity = 'example.AccesoBuzonViewModelTest/' + old_name
        old = '@Test\nfun `' + old_name + '`() = runTest {\nsetup()\nassertEquals(0, vm.porEnviar.value)\nassertFalse(vm.hayAltas.value)\n}'
        new = old.replace(old_name, 'nuevo contrato').replace('assertFalse', 'assertTrue').replace('\n}', '\nassertTrue(vm.estadoAcceso.value is EstadoAccesoBuzon.Error)\n}')
        path.write_text(new)
        with patch.object(common.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, old)):
            self.assertEqual(common.authorized_test_migrations(self.root, [identity], 'android', '2'),
                             {identity: 'example.AccesoBuzonViewModelTest/nuevo contrato'})
            path.write_text(new.replace('assertEquals(0, vm.porEnviar.value)', ''))
            self.assertEqual(common.authorized_test_migrations(self.root, [identity], 'android', '2'), {})
            path.write_text('')
            self.assertEqual(common.authorized_test_migrations(self.root, [identity], 'android', '2'), {})

    def test_readonly_search_excludes_secret_paths_and_external_symlinks(self):
        script = Path(readonly.__file__).resolve()
        (self.root / 'visible.kt').write_text('needle')
        # Names only: never create or inspect actual credential fixtures.
        (self.root / 'external.kt').symlink_to('/etc/passwd')
        result = subprocess.run([sys.executable, str(script), str(self.root), 'rg', '-l', 'needle', '.'],
                                cwd=self.root, capture_output=True, text=True,
                                env={**os.environ, 'BENCHMARK_RG': str(common.readonly_rg())})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('visible.kt', result.stdout)
        self.assertNotIn('external.kt', result.stdout)
        with self.assertRaises(ValueError):
            readonly.checked(self.root.resolve(), str(self.root / 'external.kt'))

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=TMP)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def cell(self, arm='v2_reforzado', platform='android'):
        ws, profile, inputs, evidence = common.cell_paths(self.root, '1', arm)
        ws.mkdir(parents=True)
        common.freeze_profile(profile, arm)
        inputs.mkdir(parents=True)
        (inputs / 'task.md').write_text('Implementa el contrato explícito.')
        oracle = inputs / ('oracle.kt' if platform == 'android' else 'oracle.swift')
        oracle.write_text('@Test fun testUno() {}' if platform == 'android' else 'func testUno() {}')
        common.write_json(inputs / 'manifest.json', {
            'task_sha256': common.sha(inputs / 'task.md'), 'oracle_sha256': common.sha(oracle),
            'workspace_baseline': common.snapshot(ws)})
        return ws, profile, inputs, evidence

    def test_candidate_content_is_unchanged_except_existing_deltas_and_names(self):
        source = common.REPO / 'docs/experimentos/continuidad-developer-v2-refuerzos-2026-11-06/fuentes'
        raw = (source / 'SKILL-candidato2.md').read_text()
        for arm in ('v2', 'v2_reforzado'):
            expected = common.reinforce(raw) if arm == 'v2_reforzado' else raw
            for old, new in [('__SKILL__', 'developer-v2'), ('__DATA_API__', 'data-api'),
                             ('__UI_DESIGN__', 'ui-design')]:
                expected = expected.replace(old, new)
            files = common.source_profile(arm)['files']
            self.assertEqual(files['skills/developer-v2/SKILL.md'], expected)
            self.assertEqual(files['agent.md'], (source / 'agent-candidato2.md').read_text()
                             .replace('__SKILL__', 'developer-v2'))

    def test_profiles_identical_between_platforms(self):
        for arm in common.ARMS:
            a = common.freeze_profile(self.root / 'android' / arm, arm)
            b = common.freeze_profile(self.root / 'ios' / arm, arm)
            self.assertEqual(a, b)
            for text in common.source_profile(arm)['files'].values():
                self.assertNotRegex(text, r'\{\{\w+\}\}|__(SKILL|DATA_API|UI_DESIGN)__')

    def test_ios_uses_actual_sources_not_rewritten_role(self):
        text = ios.build_system_instructions('v2_reforzado', self.root)
        self.assertIn(common.DELTA_A, text)
        self.assertIn('Consulta de dominio selectiva', text)
        self.assertNotIn('máxima disciplina DRY', text)
        # "actual" follows the current canonical implementation, not an old heading.
        # Historical reports/frozen profiles remain unchanged by this assertion.
        agent = (common.REPO / 'generated/opencode/agents/developer.md').read_text().split('---', 2)[2].lstrip('\n')
        skill = (common.REPO / 'generated/opencode/skills/developer/SKILL.md').read_text()
        self.assertEqual(ios.build_system_instructions('developer_actual', self.root), agent + '\n\n' + skill)

    def test_frozen_profile_changes_are_detected(self):
        profile = self.root / 'profile'
        common.freeze_profile(profile, 'v2')
        (profile / 'agent.md').write_text('Wrong instructions')
        with self.assertRaisesRegex(ValueError, 'alterado'):
            common.verify_profile(profile)

    def test_missing_delta_anchor_is_not_silently_ignored(self):
        with self.assertRaises(ValueError):
            common.reinforce('- **Comprobar.**\n')

    def test_safe_zip_and_existing_workspace(self):
        archive = self.root / 'app.zip'
        with zipfile.ZipFile(archive, 'w') as zf:
            for name in ['app.kt', '.env', 'cert.pem', 'credentials.json', '.git/config',
                         'app/build/stale.xml', 'local.properties']:
                zf.writestr('app-crm-android-enterprise/' + name, 'synthetic fixture')
        ws = self.root / 'ws'
        common.extract_project(archive, ws, 'android', 'v2')
        self.assertEqual(list(ws.iterdir()), [ws / 'app.kt'])
        with self.assertRaises(FileExistsError):
            common.extract_project(archive, ws, 'android', 'v2')

    def test_zip_traversal_is_rejected(self):
        archive = self.root / 'bad.zip'
        with zipfile.ZipFile(archive, 'w') as zf:
            zf.writestr('app-crm-android-enterprise/../escape', 'not extracted')
        with self.assertRaises(ValueError):
            common.extract_project(archive, self.root / 'ws', 'android', 'v2')
        self.assertFalse((self.root / 'escape').exists())

    def test_signed_framework_internal_symlinks_are_preserved(self):
        archive = self.root / 'framework.zip'
        with zipfile.ZipFile(archive, 'w') as zf:
            zf.writestr('App/Vendor.xcframework/macos/Vendor.framework/Versions/A/Vendor', 'binary fixture')
            for name, target in [('Versions/Current', 'A'), ('Vendor', 'Versions/Current/Vendor')]:
                item = zipfile.ZipInfo('App/Vendor.xcframework/macos/Vendor.framework/' + name)
                item.external_attr = (stat.S_IFLNK | 0o777) << 16
                zf.writestr(item, target)
        ws = self.root / 'ws'
        common.extract_project(archive, ws, 'ios', 'v2_reforzado')
        binary = ws / 'Vendor.xcframework/macos/Vendor.framework/Vendor'
        self.assertTrue(binary.is_symlink())
        self.assertEqual(binary.read_text(), 'binary fixture')

    def test_framework_symlink_escape_is_rejected(self):
        archive = self.root / 'framework.zip'
        with zipfile.ZipFile(archive, 'w') as zf:
            item = zipfile.ZipInfo('App/Vendor.framework/Headers')
            item.external_attr = (stat.S_IFLNK | 0o777) << 16
            zf.writestr(item, '../../outside')
        with self.assertRaises(ValueError):
            common.extract_project(archive, self.root / 'ws', 'ios', 'v2_reforzado')

    def test_task_prompt_is_same_across_arms_except_workspace(self):
        prompts = []
        for arm in common.ARMS:
            ws, _, _, _ = self.cell(arm)
            text, _ = common.task_prompt(self.root, '1', arm, 'android')
            prompts.append(text.replace(str(ws), '<workspace>'))
        self.assertEqual(len(set(prompts)), 1)

    def test_no_oracle_access_in_model_permissions(self):
        ws, profile, inputs, _ = self.cell()
        config = common.opencode_configuration(self.root, '1', 'v2_reforzado', 'provider/model')
        perm = config['agent']['pilot-v2_reforzado']['permission']
        self.assertEqual(perm['read']['*'], 'deny')
        self.assertNotIn(str(inputs), perm['read'])
        self.assertNotIn(str(profile / 'agent.md'), perm['write'])
        self.assertEqual(perm['edit']['AGENTS.md'], 'deny')

    def test_openai_provider_and_all_default_model_selection_are_pinned(self):
        self.cell()
        model = 'openai/gpt-6-luna'
        config = common.opencode_configuration(self.root, '1', 'v2_reforzado', model)
        self.assertEqual(common.DEFAULT_MODEL, model)
        self.assertEqual(config['enabled_providers'], ['openai'])
        self.assertEqual(config['model'], model)
        self.assertEqual(config['small_model'], model)
        self.assertEqual(config['agent']['pilot-v2_reforzado']['model'], model)

    def test_real_android_archive_name_and_namespaces_are_bound_in_inputs_only(self):
        archive = self.root / 'app.zip'
        with zipfile.ZipFile(archive, 'w') as zf:
            zf.writestr('ActualAndroid/gradlew', '#!/bin/sh\nexit 0\n')
            zf.writestr('ActualAndroid/core/domain/src/main/java/example/crm/domain/model/prospect/Prospect.kt',
                        'package example.crm.domain.model.prospect\nclass Prospect')
            zf.writestr('ActualAndroid/app/src/main/java/example/crm/mobile/features/offline/buzon/AccesoBuzon.kt',
                        'package example.crm.mobile.features.offline.buzon\n')
        lab = self.root / 'lab'
        common.prepare_cell(lab, '1', 'v2_reforzado', 'android', archive, android.TASKS['1'], '/sdk')
        ws, profile, inputs, _ = common.cell_paths(lab, '1', 'v2_reforzado')
        manifest = common.read_json(inputs / 'manifest.json')
        self.assertEqual(manifest['archive_prefix'], 'ActualAndroid')
        self.assertEqual(manifest['bindings']['com.example.mobilefixture'], 'example.crm')
        self.assertIn('example.crm.domain', (inputs / 'oracle.kt').read_text())
        self.assertIn('example/crm/domain', (inputs / 'task.md').read_text())
        for name, text in common.source_profile('v2_reforzado')['files'].items():
            self.assertEqual((profile / name).read_text(), text)
        self.assertTrue((ws / 'core/domain/src/main/java/example/crm/domain/model/prospect/Prospect.kt').is_file())

    def test_ios_project_and_queue_binding_does_not_double_prefix_types(self):
        ws = self.root / 'ws'
        project = ws / 'Actual App/Actual App.xcodeproj/project.pbxproj'
        project.parent.mkdir(parents=True)
        project.write_text('fixture')
        queue = ws / 'Actual App/Actual App/CompanyFixtureComponent1.swift'
        queue.parent.mkdir()
        queue.write_text('''class CompanyFixtureComponent1 {}
struct CompanyFixtureComponent2 {}
enum CompanyFixtureComponent3 {}
let key = "company.chat.pending.actions.v1"
''')
        bindings, runtime = common.project_bindings(ws, 'ios')
        bound = common.bind_text('FixtureComponent1 FixtureComponent2 FixtureModule FixtureProject/FixtureProject Tests', bindings)
        self.assertEqual(bound, 'CompanyFixtureComponent1 CompanyFixtureComponent2 Actual_App Actual App/Actual App Tests')
        self.assertEqual(runtime['xcode_scheme'], 'Actual App')
        self.assertEqual(bindings['benchmark.fixture.queue'], 'company.chat.pending.actions.v1')

    def test_wall_clock_timeout_preserves_both_logs(self):
        before = time.monotonic()
        result = common.run_logged([sys.executable, '-u', '-c',
                                   'import sys,time; print("out"); print("err",file=sys.stderr); time.sleep(10)'],
                                  self.root, self.root / 'evidence', 'timeout', 0.2)
        self.assertLess(time.monotonic() - before, 3)
        self.assertTrue(result['timed_out'])
        self.assertNotEqual(result['exit_code'], 0)
        self.assertIn('out', Path(result['stdout']).read_text())
        self.assertIn('err', Path(result['stderr']).read_text())

    def test_zero_and_skipped_tests_never_pass(self):
        path = self.root / 'TEST.xml'
        path.write_text('<testsuite><testcase classname="C" name="t"><skipped/></testcase></testsuite>')
        report = common.junit_report([path], 'C')
        self.assertEqual(report['executed'], 0)
        self.assertEqual(common.suite_status({'exit_code': 0}, report), 'no_tests_executed')
        self.assertEqual(common.junit_report([path], 'Other')['cases'], {})
        self.assertEqual(common.suite_status({'exit_code': 0}, {'executed': 1}, 2),
                         'incomplete_test_execution')

    def test_recent_stale_gradle_report_is_not_counted(self):
        ws, _, _, evidence = self.cell()
        stale = ws / 'core/domain/build/test-results/testReleaseUnitTest/TEST-stale.xml'
        stale.parent.mkdir(parents=True)
        stale.write_text('<testsuite><testcase classname="C" name="t"/></testsuite>')

        def no_tests(command, cwd, evidence, name, timeout, env=None):
            evidence.mkdir(parents=True, exist_ok=True)
            out, err = evidence / 'out.log', evidence / 'err.log'
            out.touch()
            err.touch()
            return {'exit_code': 0, 'stdout': str(out), 'stderr': str(err)}

        with patch.object(common, 'run_logged', side_effect=no_tests):
            result = common.run_suite(self.root, '1', 'v2_reforzado', 'android', android.TASKS['1'], 'original')
        self.assertEqual(result['status'], 'no_tests_executed')
        self.assertTrue((evidence / 'original-previous-test-results/testReleaseUnitTest/TEST-stale.xml').exists())

    def test_infrastructure_and_compilation_are_distinguished(self):
        out, err = self.root / 'out.log', self.root / 'err.log'
        err.touch()
        cmd = {'exit_code': 65, 'stdout': str(out), 'stderr': str(err)}
        for message, expected in [
            ('database is locked', 'infrastructure_error'),
            ('file.swift:5:9: error: cannot find type', 'build_failed'),
            ('Unknown external failure', 'runner_error_unclassified')]:
            out.write_text(message)
            self.assertEqual(common.suite_status(cmd, {'executed': 0}), expected)

    def test_ios_uses_isolated_derived_data_and_actual_test_results(self):
        _, _, _, evidence = self.cell(platform='ios')
        commands = []

        def fake_xcode(command, cwd, evidence, name, timeout, env=None):
            commands.append(command)
            evidence.mkdir(parents=True, exist_ok=True)
            out, err = evidence / f'{name}.out', evidence / f'{name}.err'
            err.touch()
            if command[0] == 'xcodebuild':
                Path(command[command.index('-resultBundlePath') + 1]).mkdir()
                out.write_text('Tests executed')
            else:
                common.write_json(out, {'testNodes': [{'nodeType': 'Test Suite',
                    'name': 'OracleSearchProspectsTests', 'children': [
                        {'nodeType': 'Test Case', 'name': 'testUno()', 'result': 'Passed'}]}]})
            return {'exit_code': 0, 'stdout': str(out), 'stderr': str(err), 'timed_out': False}

        with patch.object(common, 'run_logged', side_effect=fake_xcode):
            result = common.run_suite(self.root, '1', 'v2_reforzado', 'ios', ios.TASKS['1'], 'oracle')
        self.assertEqual(result['status'], 'passed')
        self.assertEqual(result['report']['executed'], 1)
        self.assertIn(str(evidence / 'derived-oracle'), commands[0])
        self.assertIn('-parallel-testing-enabled', commands[0])
        self.assertEqual(commands[1][:5], ['xcrun', 'xcresulttool', 'get', 'test-results', 'tests'])

    def test_xcode_report_filters_actual_oracle_class(self):
        data = {'testNodes': [{'nodeType': 'Test Suite', 'name': 'Oracle', 'children': [
            {'nodeType': 'Test Case', 'name': 'testOne()', 'result': 'Passed'}]},
            {'nodeType': 'Test Suite', 'name': 'Unrelated', 'children': [
                {'nodeType': 'Test Case', 'name': 'testTwo()', 'result': 'Passed'}]}]}
        report = common.xcresult_report(data, 'Oracle')
        self.assertEqual(report['executed'], 1)
        self.assertEqual(common.xcresult_report(data, 'Missing')['executed'], 0)

    def test_oracle_is_removed_on_failure_and_never_overwrites_participant(self):
        oracle = self.root / 'oracle.swift'
        oracle.write_text('fixture')
        target = self.root / 'ws' / 'oracle.swift'
        with self.assertRaises(TimeoutError):
            with common.oracle_injection(oracle, target, common.sha(oracle)):
                raise TimeoutError()
        self.assertFalse(target.exists())
        target.write_text('participant')
        with self.assertRaises(FileExistsError):
            with common.oracle_injection(oracle, target, common.sha(oracle)):
                pass
        self.assertEqual(target.read_text(), 'participant')

    def test_metrics_include_cache_and_missing_measurements_are_not_zero(self):
        metrics = common.event_metrics([{'type': 'step_start'}, {'type': 'step_finish', 'part': {
            'reason': 'stop', 'tokens': {'input': 2, 'output': 3, 'reasoning': 4,
                                       'cache': {'read': 5, 'write': 6}, 'total': 20}}}])
        self.assertEqual(metrics['tokens']['total'], 20)
        self.assertIsNone(common.event_metrics([])['tokens']['total'])
        self.assertIsNone(common.event_metrics([{'type': 'step_finish', 'part': {}}])['tokens']['total'])
        native = common.event_metrics([{'type': 'PLANNER_RESPONSE', 'input_tokens': 2,
                                       'output_tokens': 3, 'cache_read_tokens': 5}], native=True)
        self.assertEqual(native['tokens']['total'], 10)
        self.assertFalse(native['tokens']['cross_runtime_comparable'])

    def test_skill_name_alone_does_not_prove_correct_content(self):
        _, profile, _, _ = self.cell()
        event = {'type': 'tool_use', 'part': {'tool': 'skill', 'state': {
            'status': 'completed', 'input': {'name': 'developer-v2'}, 'output': 'another version'}}}
        self.assertFalse(common.profile_observation(profile, 'v2_reforzado', [event])['primary_loaded_by_content'])
        expected = (profile / 'skills/developer-v2/SKILL.md').read_text().split('---', 2)[-1].strip()
        event['part']['state']['output'] = expected
        self.assertTrue(common.profile_observation(profile, 'v2_reforzado', [event])['primary_loaded_by_content'])

    def test_required_tool_permission_failures_are_recorded(self):
        _, profile, _, _ = self.cell()
        event = {'part': {'tool': 'write', 'callID': 'blocked', 'state': {
            'status': 'error', 'error': 'Permission denied by host'}}}
        observed = common.profile_observation(profile, 'v2_reforzado', [event])
        self.assertEqual(observed['permission_errors'][0]['tool'], 'write')

    def test_provider_failure_cannot_count_as_agent_success(self):
        _, _, _, evidence = self.cell()
        common.write_json(evidence / 'run.json', {'attribution_ready': False, 'exit_code': 1})
        passed = {'status': 'passed', 'report': {'cases': {'C/t': 'passed'}}}
        result = common.evaluation_record(self.root, '1', 'v2_reforzado', passed, passed, passed)
        self.assertTrue(result['artifact_acceptance'])
        self.assertIsNone(result['functional_acceptance'])
        self.assertFalse(result['valid_for_agent_comparison'])

    def test_removed_original_tests_fail_regression(self):
        _, _, _, evidence = self.cell()
        common.write_json(evidence / 'run.json', {'attribution_ready': True})
        baseline = {'status': 'passed', 'report': {'cases': {'C/old': 'passed'}}}
        passed = {'status': 'passed', 'report': {'cases': {'C/new': 'passed'}}}
        result = common.evaluation_record(self.root, '1', 'v2_reforzado', baseline, passed, dict(passed))
        self.assertFalse(result['original_suite_pass'])
        self.assertEqual(result['original']['status'], 'baseline_tests_missing')

    def test_native_is_fail_closed_not_idle_transcript_heuristic(self):
        result = common.preflight('ios', ios.TASKS, self.root / 'absent.zip', 'antigravity',
                                  self.root / 'absent-runtime')
        self.assertFalse(result['ready'])
        self.assertTrue(any('cancelación' in e for e in result['errors']))

    def test_preflight_does_not_launch_inference(self):
        with patch.object(common, 'run_opencode') as model:
            status = android.main(['--preflight-only', '--base-zip', str(self.root / 'absent.zip')])
        self.assertEqual(status, 2)
        model.assert_not_called()

    def test_failed_baseline_skips_paid_inference_and_is_not_scored(self):
        def prepare(*args):
            return self.cell()[0]

        def baseline(*args):
            record = {'status': 'infrastructure_error', 'report': {'cases': {}, 'executed': 0}}
            evidence = common.cell_paths(self.root, '1', 'v2_reforzado')[-1]
            common.write_json(evidence / 'baseline.suite.json', record)
            return record

        with patch.object(common, 'preflight', return_value={'ready': True, 'runtime_version': '1.18.34'}), \
                patch.object(common, 'prepare_cell', side_effect=prepare), \
                patch.object(common, 'run_suite', side_effect=baseline), \
                patch.object(common, 'run_opencode') as model:
            result = android.main(['--root', str(self.root), '--tasks', '1', '--arms', 'v2_reforzado'])
        self.assertEqual(result, 1)
        model.assert_not_called()
        record = common.read_json(self.root / 'resultados.json')['tasks']['1']['arms']['v2_reforzado']
        self.assertEqual(record['run_status'], 'not_started')
        self.assertIsNone(record['functional_acceptance'])

    def test_original_historical_results_not_overwritten(self):
        before = {p: common.sha(p / 'resultados.json') for p in (android.PACKAGE, ios.EXP_DIR)}
        common.write_json(self.root / 'resultados.json', common.summary(self.root, ['1'], ['v2_reforzado']))
        self.assertEqual(before, {p: common.sha(p / 'resultados.json') for p in before})

    def test_android_search_oracle_matches_published_business_rules(self):
        text = android.TASKS['1']['oracle_source'].read_text()
        fields = re.findall(r'Prospect\(id = "([^"]+)", razonSocial = (null|"[^"]*"), '
                            r'rfc = "([^"]+)", nombreEmpleado = "([^"]+)"', text)
        def norm(value):
            return ''.join(c for c in unicodedata.normalize('NFD', value.casefold())
                           if unicodedata.category(c) != 'Mn')
        query = re.search(r'fun oraculo03.*?query = "([^"]+)"', text, re.S).group(1)
        matches = [row[0] for row in fields if any(norm(query) in norm(v) for v in row[1:])]
        self.assertEqual(matches, ['3'])
        expected = sorted(fields, key=lambda r: (r[1] == 'null', norm(r[1]), r[2]))
        block = re.search(r'fun oraculo08.*?\n    }', text, re.S).group()
        asserted = re.findall(r'assertEquals\("([^"]+)", res.items\[\d\].id\)', block)
        self.assertEqual(asserted, [r[0] for r in expected])


class OfflineEndToEndTests(unittest.TestCase):
    def test_prepare_run_and_evaluate_with_fake_cli_and_gradle(self):
        with tempfile.TemporaryDirectory(dir=TMP) as temp:
            base = Path(temp)
            archive = base / 'app.zip'
            gradle = '''#!/usr/bin/env python3
import sys
from pathlib import Path
cls = sys.argv[sys.argv.index('--tests')+1] if '--tests' in sys.argv else 'OriginalSuite'
count = 10 if '--tests' in sys.argv else 1
p = Path('core/domain/build/test-results/testReleaseUnitTest/TEST-fixture.xml')
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<testsuite>' + ''.join('<testcase classname="'+cls+'" name="test'+str(i)+'"/>' for i in range(count)) + '</testsuite>')
'''
            with zipfile.ZipFile(archive, 'w') as zf:
                info = zipfile.ZipInfo('app-crm-android-enterprise/gradlew')
                info.external_attr = 0o100755 << 16
                zf.writestr(info, gradle)
                zf.writestr('app-crm-android-enterprise/AGENTS.md', 'Synthetic project instructions')
            fake_cli = base / 'fake-opencode'
            fake_cli.write_text('''#!/usr/bin/env python3
import json,os,sys,shutil,subprocess
from pathlib import Path
if '--version' in sys.argv:
 print('1.18.34')
 sys.exit(0)
if 'debug' in sys.argv:
 if 'files' in sys.argv: print('gradlew')
 else:
  import base64
  print(json.dumps({'content':base64.b64encode(Path(sys.argv[-1]).read_bytes()).decode(),'encoding':'base64'}))
 sys.exit(0)
cfg=json.loads(os.environ['OPENCODE_CONFIG_CONTENT'])
assert 'readonly-bin' not in os.environ['PATH']
assert shutil.which('git') == os.environ['BENCHMARK_GIT']
assert subprocess.run([os.environ['BENCHMARK_GIT'],'rev-parse','--show-toplevel'],capture_output=True).returncode == 0
assert subprocess.run([os.environ['BENCHMARK_RG'],'--files','--hidden'],capture_output=True).returncode == 0
participant_git=subprocess.check_output([os.environ['SHELL'],'-c','command -v git'],text=True).strip()
assert 'readonly-bin' in participant_git
assert subprocess.run([os.environ['SHELL'],'-c','pwd && git status --short && ls'],capture_output=True).returncode == 0
skill=Path(cfg['skills']['paths'][0])/'developer-v2/SKILL.md'
output=skill.read_text().split('---',2)[-1].strip()
for ev in [{'type':'step_start'}, {'type':'tool_use','part':{'tool':'skill','state':{'status':'completed','input':{'name':'developer-v2'},'output':output}}}, {'type':'step_finish','part':{'reason':'stop','tokens':{'input':2,'output':3,'cache':{'read':5,'write':0}}}}]:
 print(json.dumps(ev),flush=True)
''')
            fake_cli.chmod(0o755)
            java = base / 'jdk/bin'
            java.mkdir(parents=True)
            (java / 'java').touch()
            sdk = base / 'sdk'
            sdk.mkdir()
            root = base / 'lab'
            args = ['--root', str(root), '--base-zip', str(archive), '--tasks', '1',
                    '--arms', 'v2_reforzado', '--cli', str(fake_cli), '--java-home', str(java.parent),
                    '--android-home', str(sdk)]
            self.assertEqual(android.main([*args, '--prepare-only']), 0)
            self.assertEqual(android.main([*args, '--run-prepared']), 0)
            result = common.read_json(root / 'resultados.json')['tasks']['1']['arms']['v2_reforzado']
            self.assertTrue(result['functional_acceptance'])
            self.assertTrue(result['primary_loaded_by_content'])
            self.assertEqual(result['tokens']['total'], 10)
            self.assertGreaterEqual(result['oracle']['report']['executed'], 10)
            ws, _, _, evidence = common.cell_paths(root, '1', 'v2_reforzado')
            self.assertFalse((ws / android.TASKS['1']['oracle_target']).exists())
            self.assertTrue((evidence / 'request.json').is_file())
            self.assertTrue((evidence / 'inference.stdout.log').is_file())
            self.assertIn('--pure', common.read_json(evidence / 'inference.command.json')['command'])
            self.assertIn('--title', common.read_json(evidence / 'inference.command.json')['command'])
            with self.assertRaises(FileExistsError):
                android.main(args)
            # A fast process can finish between budget polls: the final counters
            # still invalidate an over-budget run instead of silently accepting it.
            limited_args = list(args)
            limited_args[limited_args.index('--root') + 1] = str(base / 'limited')
            self.assertEqual(android.main([*limited_args, '--token-limit', '5']), 1)
            limited = common.read_json(base / 'limited/resultados.json')['tasks']['1']['arms']['v2_reforzado']
            self.assertEqual(limited['stop_reason'], 'token_limit')
            self.assertFalse(limited['attribution_ready'])
            self.assertIsNone(limited['functional_acceptance'])


if __name__ == '__main__':
    unittest.main()
