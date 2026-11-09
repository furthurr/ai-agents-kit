#!/usr/bin/env python3
"""Read-only evidence inventory + portable source snapshot; no model calls."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tarfile

from preserve_real_project_lab import safe

REPO = Path(__file__).resolve().parent.parent
EXPERIMENTS = (
    'ponytail-2026-11-04', 'odd-vs-sdd-2026-11-04', 'continuidad-2026-11-04',
    'developer-sdd-odd-gemini-2026-11-04', 'developer-compacto-gemini-2026-11-04',
    'real-project-gemini-2026-11-05', 'developer-v2-alta-gemini-2026-11-05',
    'developer-v2-dominios-build-gemini-2026-11-05', 'odd-estandares-gemini-2026-11-05',
    'odd-estandares-reintento-gemini-2026-11-05', 'odd-estandares-gpt6-luna-max',
    'odd-estandares-gpt6-luna-max-1800', 'odd-navigator-architecture-luna-max',
    'odd-domain-core-luna-max',
)
SCRIPTS = (
    'gemini_three_way.py', 'gemini_three_way_report.py', 'test_gemini_three_way.py',
    'gemini_benchmark.py', 'odd_vs_sdd_experiment.py', 'odd_vs_sdd_audit.py', 'odd_vs_sdd_supplement.py',
    'developer_compact_benchmark.py', 'developer_compact_report.py', 'test_developer_compact_benchmark.py',
    'developer_v2_high_benchmark.py', 'developer_v2_high_report.py',
    'developer_v2_domains_build.py', 'developer_v2_domains_report.py',
    'test_developer_v2_high_benchmark.py', 'test_developer_v2_high_report.py',
    'test_developer_v2_domains_build.py', 'test_developer_v2_domains_report.py',
    'odd_standards_benchmark.py', 'odd_standards_retry.py', 'odd_standards_luna.py',
    'odd_standards_luna_1800.py', 'odd_standards_report.py',
    'test_odd_standards_benchmark.py', 'test_odd_standards_retry.py', 'test_odd_standards_luna.py',
    'test_odd_standards_luna_1800.py', 'test_odd_standards_report.py',
    'odd_context_routing.py', 'odd_context_routing_report.py',
    'test_odd_context_routing.py', 'test_odd_context_routing_report.py',
    'odd_domain_core.py', 'odd_domain_core_report.py', 'test_odd_domain_core.py', 'test_odd_domain_core_report.py',
    'real_project_gemini_lab.py', 'real_project_report.py', 'preserve_real_project_lab.py',
    'test_real_project_gemini_lab.py', 'test_real_project_report.py',
    'preserve_experiment_context.py', 'preserve_odd_continuity.py',
)
CANONICAL = (
    'canonical/manifest.json', 'canonical/agents/developer.md',
    'canonical/skills/developer/SKILL.md', 'canonical/skills/developer/references/plan.md',
    'canonical/skills/data-api/SKILL.md', 'canonical/skills/data-api/references/templates.md',
    'canonical/skills/ui-design/SKILL.md', 'canonical/skills/ui-design/references/templates.md',
    'canonical/shared/project-context.md', 'canonical/shared/mas-identity.md',
    'adapters/opencode/agents/developer.json',
)
EXPECTED = {
    'canonical/agents/developer.md': '3e6acaf5d3609a660c117eda69eae1a0f72381991211e6089e5414c564e522be',
    'canonical/skills/developer/SKILL.md': '44febbfaf22dd90f8971019cbd133bdde6dd31fc46478813a4f42671984f9608',
    'canonical/skills/data-api/SKILL.md': '007364b6113683239b4538aa9e1515fd6a46abe74c3978c7af7bac2a29cbec68',
    'canonical/skills/ui-design/SKILL.md': 'c86f04f00a180a210c6d87b7eca0de1d2702f0ff8f229553deb147936a8ca016',
}


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b''):
            value.update(chunk)
    return value.hexdigest()


def git(*args):
    return subprocess.run(['git', *args], cwd=REPO, capture_output=True, text=True, check=True).stdout.strip()


def build(destination):
    if not destination.is_dir():
        raise RuntimeError('Existing continuity directory required')
    archive = destination / 'herramientas-y-plan.tar.gz'
    manifest_file = destination / 'manifest.json'
    if archive.exists() or manifest_file.exists():
        raise RuntimeError('Never overwrite a continuity snapshot')
    evidence, verified_archives = {}, []
    for name in EXPERIMENTS:
        folder = REPO / 'docs/experimentos' / name
        if not (folder / 'README.md').is_file():
            raise RuntimeError('Missing report: ' + name)
        inventory = {}
        for path in sorted(folder.rglob('*')):
            relative = path.relative_to(REPO)
            if path.is_file() and not path.is_symlink() and safe(relative) and path.name != '.DS_Store':
                inventory[str(relative)] = digest(path)
        evidence[name] = inventory
        provenance = folder / 'preservacion.json'
        lab = folder / 'laboratorio.tar.gz'
        if provenance.is_file() and lab.is_file():
            expected = json.loads(provenance.read_text()).get('archive_sha256')
            actual = inventory[str(lab.relative_to(REPO))]
            if expected != actual:
                raise RuntimeError('Laboratory archive hash mismatch: ' + name)
            verified_archives.append(name)
    inputs = [(REPO / 'tools' / name, 'tools/' + name) for name in SCRIPTS]
    inputs += [(REPO / name, name) for name in CANONICAL]
    inputs += [(destination / name, 'continuidad/' + name) for name in ('CONTINUAR-AQUI.md', 'PROMPT.md', 'estado.json')]
    desktop = Path('/Users/pedrogomezvasquez/Desktop/PLAN-Developer-v2-como-Developer-2026-11-05.md')
    inputs.append((desktop, 'external/' + desktop.name))
    for path, name in inputs:
        if not path.is_file() or path.is_symlink() or not safe(Path(name)):
            raise RuntimeError('Missing/unsafe selected source: ' + name)
    snapshot = {}
    with tarfile.open(archive, 'x:gz') as tar:
        for path, name in inputs:
            snapshot[name] = digest(path)
            tar.add(path, arcname=name, recursive=False)
    with tarfile.open(archive, 'r:gz') as tar:
        for member in tar.getmembers():
            path = Path(member.name)
            if not member.isfile() or path.is_absolute() or '..' in path.parts or not safe(path):
                raise RuntimeError('Unsafe snapshot member')
            with tar.extractfile(member) as file:
                if hashlib.sha256(file.read()).hexdigest() != snapshot[member.name]:
                    raise RuntimeError('Snapshot member changed: ' + member.name)
    result = {
        'recorded_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'repo': str(REPO), 'head': git('rev-parse', 'HEAD'), 'git_status': git('status', '--short'),
        'snapshot_archive_sha256': digest(archive), 'snapshot_files': snapshot,
        'experiment_files': evidence, 'verified_laboratory_archives': verified_archives,
        'unchanged_canonical_checks': {name: {'expected': expected, 'actual': digest(REPO / name),
                                               'matches': digest(REPO / name) == expected} for name, expected in EXPECTED.items()},
        'desktop_plan': {'source': str(desktop), 'sha256': digest(desktop),
                         'matches_previous_session': digest(desktop) == 'fd62d8aa65605549f3d0321522751b3f35fb5b02af8435fcc2acad9edda97f5b'},
        'transport': 'Copy docs/experimentos plus this source snapshot, or the same complete local checkout; no claim remote contains untracked files',
        'new_model_calls': 0, 'canonical_or_index_updates': False,
        'archive_verification_scope': 'Archive hashes checked against prior preservation manifests; source snapshot members checked individually, not every historical archive re-audited semantically',
    }
    with manifest_file.open('x') as file:
        json.dump(result, file, ensure_ascii=False, indent=2)
    print(json.dumps({'experiment_packages': len(evidence), 'verified_laboratory_archives': len(verified_archives),
                      'snapshot_files': len(snapshot), 'snapshot_archive_sha256': result['snapshot_archive_sha256'],
                      'canonical_checks_match': all(value['matches'] for value in result['unchanged_canonical_checks'].values()),
                      'desktop_plan_matches': result['desktop_plan']['matches_previous_session'], 'new_model_calls': 0}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('destination', type=Path)
    build(parser.parse_args().destination.resolve())
