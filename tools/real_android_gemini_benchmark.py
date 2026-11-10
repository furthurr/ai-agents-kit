#!/usr/bin/env python3
"""Android CRM benchmark v2: frozen agents, audited requests and verified tests.

Examples (no model calls):
  python3 tools/real_android_gemini_benchmark.py --preflight-only
  python3 tools/real_android_gemini_benchmark.py --prepare-only --base-zip /path/app.zip

Use --baseline-only before a paid run. Results go to --root/resultados.json,
never to the historical experiment. Profiles come only from this repository;
installed agents are not substituted implicitly. Agent content is unchanged.
"""
from pathlib import Path
import os

import mobile_benchmark_common as common
from mobile_benchmark_common import (ARMS, DELTA_A, DELTA_B, SECRETS, agent_name,
                                     primary_skill, reinforce, sha)

REPO = common.REPO
BASE_ZIP = Path(os.environ.get("MOBILE_BENCHMARK_ANDROID_ARCHIVE",
    str(Path.home() / ".local/share/ai-agents-kit/fixtures/mobile-android.zip")))
PACKAGE = REPO / 'docs/experimentos/real-android-gemini-2026-11-08'
CLI = Path.home() / '.opencode/bin/opencode'
MODEL = common.DEFAULT_MODEL
JAVA_HOME = '/opt/homebrew/opt/openjdk@21'
ANDROID_HOME = str(Path.home() / 'Developer/android')
TIMEOUT, STEP_LIMIT, TOKEN_LIMIT = 1800, 60, 5_000_000

TASKS = {
    '1': {
        'id': 'GBA-SEARCH-PROSPECTS', 'complexity': 'media-baja',
        'file': PACKAGE / 'tarea-1-media-baja.md',
        'oracle_source': PACKAGE / 'oraculos/OracleSearchProspectsTest.kt',
        'oracle_target': 'core/domain/src/test/java/com/example/mobilefixture/domain/use_case/prospect/OracleSearchProspectsTest.kt',
        'gradle_oracle_task': ':core:domain:testReleaseUnitTest --tests "com.example.mobilefixture.domain.use_case.prospect.OracleSearchProspectsTest"',
        'gradle_original_task': ':core:domain:testReleaseUnitTest',
    },
    '2': {
        'id': 'GBA-BUZON-RETRY-UI', 'complexity': 'media-alta',
        'file': PACKAGE / 'tarea-2-media-alta.md',
        'oracle_source': PACKAGE / 'oraculos/OracleBuzonRetryUiTest.kt',
        'oracle_target': 'app/src/test/java/com/example/mobilefixture/tests1/features/offline/buzon/OracleBuzonRetryUiTest.kt',
        'gradle_oracle_task': ':app:testDebugUnitTest --tests "com.example.mobilefixture.tests1.features.offline.buzon.OracleBuzonRetryUiTest"',
        'gradle_original_task': ':app:testDebugUnitTest',
    },
    '3': {
        'id': 'GBA-QUEUE-CONCURRENCY-CIPHER', 'complexity': 'alta',
        'file': PACKAGE / 'tarea-3-alta.md',
        'oracle_source': PACKAGE / 'oraculos/OracleQueueConcurrencyCipherTest.kt',
        'oracle_target': 'core/data/src/test/java/com/example/mobilefixture/data/local/offline/OracleQueueConcurrencyCipherTest.kt',
        'gradle_oracle_task': ':core:data:testReleaseUnitTest --tests "com.example.mobilefixture.data.local.offline.OracleQueueConcurrencyCipherTest"',
        'gradle_original_task': ':core:data:testReleaseUnitTest',
    },
}


def prepare_local_properties(workspace):
    # Do not read pre-existing local.properties: it can contain credentials.
    (workspace / 'local.properties').write_text(f'sdk.dir={ANDROID_HOME}\n')


def prepare_workspace(root, task_id, arm):
    return common.prepare_cell(root, task_id, arm, 'android', BASE_ZIP, TASKS[task_id], ANDROID_HOME)


def configuration(root, task_id, arm):
    return common.opencode_configuration(root, task_id, arm, MODEL)


def main(argv=None):
    return common.main_for('android', TASKS, BASE_ZIP, CLI, argv)


if __name__ == '__main__':
    raise SystemExit(main())
