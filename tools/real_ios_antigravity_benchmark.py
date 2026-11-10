#!/usr/bin/env python3
"""iOS CRM benchmark v2 using caller-supplied, authorized fixtures.

Historical published evidence is anonymized; its metrics are not a new run.

Controlled comparison explicitly uses --runtime opencode, exactly the same
profile renderer, model/provider, budgets and tools as Android, with Xcode as
the build/test adapter. This is a NEW experiment, not a replay of Antigravity.

--runtime antigravity is diagnostic only: the installed agentapi CLI has no
verified isolated completion/cancellation contract. Preflight refuses to launch
it instead of treating an idle transcript as completed work. Native profile
payloads can still be inspected offline with build_system_instructions().

  python3 tools/real_ios_antigravity_benchmark.py --runtime opencode --preflight-only
  python3 tools/real_ios_antigravity_benchmark.py --runtime antigravity --preflight-only
"""
from pathlib import Path
import os

import mobile_benchmark_common as common
from mobile_benchmark_common import ARMS, DELTA_A, DELTA_B, SECRETS

REPO = common.REPO
BASE_ZIP = Path(os.environ.get("MOBILE_BENCHMARK_IOS_ARCHIVE",
    str(Path.home() / ".local/share/ai-agents-kit/fixtures/mobile-ios.zip")))
EXP_DIR = REPO / 'docs/experimentos/real-ios-gemini-antigravity-2026-11-09'
AGENTAPI = Path.home() / '.gemini/antigravity/bin/agentapi'
CLI = Path.home() / '.opencode/bin/opencode'
TIMEOUT = 1800

TASKS = {
    '1': {
        'id': 'GIOS-SEARCH-PROSPECTS', 'complexity': 'media-baja',
        'file': EXP_DIR / 'tarea-1-media-baja.md',
        'oracle_source': EXP_DIR / 'oraculos/OracleSearchProspectsTests.swift',
        'oracle_target': 'FixtureProject/FixtureProject Tests/Domain/OracleSearchProspectsTests.swift',
        'xcode_oracle_test': 'FixtureProject Tests/OracleSearchProspectsTests',
        'xcode_original_test': 'FixtureProject Tests',
    },
    '2': {
        'id': 'GIOS-BUZON-RETRY-UI', 'complexity': 'media-alta',
        'file': EXP_DIR / 'tarea-2-media-alta.md',
        'oracle_source': EXP_DIR / 'oraculos/OracleBuzonRetryUiTests.swift',
        'oracle_target': 'FixtureProject/FixtureProject Tests/Presentacion/OracleBuzonRetryUiTests.swift',
        'xcode_oracle_test': 'FixtureProject Tests/OracleBuzonRetryUiTests',
        'xcode_original_test': 'FixtureProject Tests',
    },
    '3': {
        'id': 'GIOS-QUEUE-CONCURRENCY-CIPHER', 'complexity': 'alta',
        'file': EXP_DIR / 'tarea-3-alta.md',
        'oracle_source': EXP_DIR / 'oraculos/OracleQueueConcurrencyCipherTests.swift',
        'oracle_target': 'FixtureProject/FixtureProject Tests/App/ViewModels/OracleQueueConcurrencyCipherTests.swift',
        'xcode_oracle_test': 'FixtureProject Tests/OracleQueueConcurrencyCipherTests',
        'xcode_original_test': 'FixtureProject Tests',
    },
}


def build_system_instructions(arm, workspace):
    """Exact repository profile for inspection; not a fake native system role."""
    definition = common.source_profile(arm)
    files = definition['files']
    return '\n\n'.join(files[name] for name in ('agent.md', f'skills/{common.primary_skill(arm)}/SKILL.md')
                         if name in files)


def prepare_workspace(root, task_id, arm):
    return common.prepare_cell(root, task_id, arm, 'ios', BASE_ZIP, TASKS[task_id])


def main(argv=None):
    return common.main_for('ios', TASKS, BASE_ZIP, CLI, argv)


if __name__ == '__main__':
    raise SystemExit(main())
