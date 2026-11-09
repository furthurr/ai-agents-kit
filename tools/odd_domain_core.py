#!/usr/bin/env python3
"""Experimental domain skill partition; same standards ODD procedure in both arms."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

import odd_context_routing as pair
import odd_standards_luna_1800 as previous

REPO = previous.REPO
PACKAGE = REPO / 'docs/experimentos/odd-domain-core-luna-max'
PRIOR = pair.PRIOR  # Standards baseline, before the discarded navigation experiment.

IMPLEMENTATION = {
    'data-api': {'Identidad del MAS', 'Cuándo usar esta skill', 'Elegir el flujo según la intención',
                 'Estándares que reconoce', 'Detección de tecnología (dónde vive la capa de datos)',
                 'Uso durante implementación de producto', 'Índice de contexto para otros agentes', 'Reglas'},
    'ui-design': {'Identidad del MAS', 'Cuándo usar esta skill', 'Elegir el flujo según la intención',
                  'Detección de tecnología (dónde viven los tokens)', 'Uso durante implementación de producto',
                  'Qué documentar (checklist visual)', 'Índice de contexto para otros agentes', 'Reglas'},
}


def sections(text):
    """Lossless frontmatter/body and top-level section partition (not inside fences)."""
    end = text.index('---', 4) + 3
    header, body = text[:end], text[end:]
    lines = body.splitlines(keepends=True)
    pieces, current, heading, fence = [], [], '__preamble__', False
    for line in lines:
        if line.startswith('```'):
            fence = not fence
        if not fence and line.startswith('## '):
            pieces.append({'heading': heading, 'text': ''.join(current)})
            heading, current = line[3:].strip(), []
        current.append(line)
    pieces.append({'heading': heading, 'text': ''.join(current)})
    assert header + ''.join(part['text'] for part in pieces) == text
    return header, pieces


def partition(text, domain):
    header, pieces = sections(text)
    missing = IMPLEMENTATION[domain] - {part['heading'] for part in pieces}
    assert not missing, ('Source headings changed', missing)
    implementation, documentation, ledger = [], [], []
    for part in pieces:
        target = 'implementation.md' if part['heading'] == '__preamble__' or part['heading'] in IMPLEMENTATION[domain] else 'documentation.md'
        (implementation if target == 'implementation.md' else documentation).append(part['text'])
        ledger.append({'heading': part['heading'], 'target': target,
                       'sha256': hashlib.sha256(part['text'].encode()).hexdigest(), 'bytes': len(part['text'].encode())})
    core = header + '\n\n' + (PACKAGE / 'nucleo.md').read_text()
    return core, ''.join(implementation), ''.join(documentation), ledger


def context(root):
    base, old = previous.context(root)
    base.PROTOCOL = 'odd-domain-core-luna-max-v1'
    old_inputs = base.source_inputs

    def inputs(folder):
        result = old_inputs(folder)
        for path in (Path(__file__).resolve(), PACKAGE / 'nucleo.md', PACKAGE / 'protocolo.md',
                     REPO / 'tools/test_odd_domain_core.py', REPO / 'tools/odd_context_routing.py', PRIOR / 'freeze.json'):
            result[str(path)] = base.sha(path)
        result['partition-manifest.json'] = base.sha(folder / 'partition-manifest.json')
        result['treatments.json'] = base.sha(folder / 'treatments.json')
        return result
    base.source_inputs = inputs
    return base, old


def prepare(root):
    prior, _ = previous.context(PRIOR)
    prior.check_frozen(PRIOR)
    previous.prepare(root)
    # Both primary ODD procedures are the prior standards-adjusted treatment.
    source = (PRIOR / 'profiles-v2/adjusted/skills/ob-odd-workflow/SKILL.md').read_text()
    control = source.replace('name: ob-odd-workflow\n', 'name: oa-odd-workflow\n').replace('`ob-data-api`', '`oa-data-api`').replace('`ob-ui-design`', '`oa-ui-design`')
    (root / 'profiles-v2/odd/skills/oa-odd-workflow/SKILL.md').write_text(control)
    (root / 'profiles-v2/adjusted/skills/ob-odd-workflow/SKILL.md').write_text(source)
    (root / 'adjusted-SKILL.md').write_text(source)
    manifest = {}
    for domain in ('data-api', 'ui-design'):
        directory = root / 'profiles-v2/adjusted/skills' / ('ob-' + domain)
        original = (directory / 'SKILL.md').read_text()
        core, impl, docs, ledger = partition(original, domain)
        (directory / 'original-contract.md').write_text(original)
        (directory / 'implementation.md').write_text(impl)
        (directory / 'documentation.md').write_text(docs)
        (directory / 'SKILL.md').write_text(core)
        manifest[domain] = {'source_sha256': hashlib.sha256(original.encode()).hexdigest(),
                            'original_bytes': len(original.encode()), 'core_bytes': len(core.encode()),
                            'implementation_bytes': len(impl.encode()), 'documentation_bytes': len(docs.encode()),
                            'sections_in_original_order': ledger}
    shutil.copyfile(PACKAGE / 'protocolo.md', root / 'protocol.md')
    shutil.copyfile(Path(__file__).resolve(), root / 'runner.py')
    shutil.copyfile(REPO / 'tools/test_odd_domain_core.py', root / 'test_runner.py')
    base, _ = context(root)
    base.write_json(root / 'budget.json', {'timeout_per_invocation_seconds': 1800, 'model': 'openai/gpt-6-luna',
                                         'variant': 'max', 'cohort': base.PROTOCOL})
    base.write_json(root / 'partition-manifest.json', manifest, exclusive=True)
    base.write_json(root / 'treatments.json', {
        'labels': {'odd': 'Standards ODD + full domain skills', 'adjusted': 'Same standards ODD + core/reference domain skills'},
        'delta': 'Only the delivery of data-api and ui-design context is changed',
        'no_navigation_maps_added': True, 'same_primary_odd_normalized': True,
        'full_original_contract_preserved': True, 'original_references_unchanged': True,
        'prior_freeze_sha256': base.sha(PRIOR / 'freeze.json')})
    print(json.dumps({domain: {key: value for key, value in values.items() if key != 'sections_in_original_order'}
                      for domain, values in manifest.items()}, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('command', choices=['prepare', 'reference', 'preflight', 'freeze', 'run', 'check'])
    parser.add_argument('--background', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    if args.background:
        assert args.command == 'run'
        child = subprocess.Popen([sys.executable, '-B', str(Path(__file__).resolve()), str(root), 'run'],
                                 cwd=REPO, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL, start_new_session=True)
        print(json.dumps({'pid': child.pid}))
        return
    if args.command == 'prepare':
        prepare(root)
        return
    base, old = context(root)
    if args.command == 'reference':
        old.validate_reference(base, root)
    elif args.command == 'preflight':
        previous.preflight(base, root)
    elif args.command == 'freeze':
        assert json.loads((root / 'reference-proof.json').read_text())['functional_pass']
        base.freeze(root)
    elif args.command == 'check':
        base.check_frozen(root)
        print('Domain-core inputs intact')
    else:
        pair.run(base, root)


if __name__ == '__main__':
    main()
