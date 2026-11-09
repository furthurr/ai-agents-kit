#!/usr/bin/env python3
"""Observable counters for the bounded batching cohort; no historical pooling."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

import odd_batching as experiment


def inspect_events(events):
    counts, output_bytes, reads, steps = Counter(), Counter(), Counter(), []
    pending, ledger = [], []
    first_product, first_red, final_text = None, None, ''
    for index, event in enumerate(events):
        part = event.get('part', {})
        tool, state = part.get('tool'), part.get('state', {})
        data = state.get('input', {})
        output = state.get('output', '')
        tags = []
        paths = [data.get('filePath', '')] + re.findall(r'^\*\*\* (?:Add|Update|Delete) File: (.+)$', data.get('patchText', ''), re.M)
        if tool:
            if tool == 'skill':
                tags = ['criteria' if any(d in data.get('name','') for d in ('data-api','ui-design')) else 'workflow']
            elif tool == 'read':
                path = data.get('filePath','')
                tags = ['read']
                reads[(path,data.get('offset'),data.get('limit'))] += 1
            elif tool in ('glob','grep','list'):
                tags = ['search']
            elif tool in ('write','edit','apply_patch'):
                tags = sorted({'note-write' if 'odd/tasks/' in p else 'test-write' if '/tests/' in p or Path(p).name.startswith('test_') else 'product-write' for p in paths if p}) or ['write-unknown']
                if len(tags)>1: counts['mixed-patch'] += 1
                if 'product-write' in tags and state.get('status')=='completed' and first_product is None:
                    first_product=index
            elif tool=='bash':
                command=data.get('command','')
                tags=['test-run' if 'manage.py test' in command else 'migration' if 'makemigrations' in command else 'check-shell']
                if 'makemigrations' in command and '--dry-run' not in command and first_product is None:
                    first_product=index
                if tags==['test-run'] and re.search(r'FAILED|FAIL:|ERROR:',output):
                    counts['red-test-outputs']+=1
                    if first_red is None: first_red=index
            elif tool=='todowrite': tags=['tracking']
            else: tags=[tool]
            counts.update(tags)
            if state.get('status')=='error': counts['tool-errors']+=1
            size=len(output.encode()) if isinstance(output,str) else 0
            output_bytes[tool]+=size
            pending.append({'tool':tool,'tags':tags,'event':index})
            # Inputs/outputs remain in sanitized transport; the ledger needs no private text.
            ledger.append({'event':index,'tool':tool,'tags':tags,'status':state.get('status'),
                           'paths':[p for p in paths if p], 'pattern':data.get('pattern'),
                           'command':data.get('command'), 'name':data.get('name'), 'output_bytes':size})
        if event.get('type')=='step_finish':
            steps.append({'event':index,'tools':pending,'metrics':experiment.metric(part),'reason':part.get('reason')})
            pending=[]
        if event.get('type')=='text': final_text=part.get('text','')
    return {'operation_counts':dict(counts),'tool_output_bytes':dict(output_bytes),
            'exact_read_repeats':[{'path':p,'offset':o,'limit':l,'count':n} for (p,o,l),n in reads.items() if n>1],
            'rounds':len(steps),'rounds_with_multiple_tools':sum(len(s['tools'])>1 for s in steps),
            'tool_calls':sum(len(s['tools']) for s in steps)+len(pending),
            'first_product_event':first_product,'first_red_event':first_red,
            'red_before_product_mechanical':first_red is not None and first_product is not None and first_red<first_product,
            'final_text':final_text,'steps':steps,'ledger':ledger}


def fidelity(root, arm, events, observed):
    base=experiment.context(root)
    loaded={}
    for domain in ('data-api','ui-design','odd-workflow'):
        name=base.namespace(arm)+'-'+domain
        expected=base.body((root/'profiles-v2'/arm/'skills'/name/'SKILL.md').read_text())
        loaded[domain]=[i for i,e in enumerate(events) if e.get('part',{}).get('tool')=='skill'
                        and e['part'].get('state',{}).get('input',{}).get('name')==name
                        and expected in e['part'].get('state',{}).get('output','')]
    first=observed['first_product_event']
    texts='\n'.join(e.get('part',{}).get('text','') for e in events if e.get('type')=='text')
    return {'loaded_by_full_content':{k:bool(v) for k,v in loaded.items()},
            'domain_events':{k:v for k,v in loaded.items() if k!='odd-workflow'},
            'both_domains_before_product':first is not None and all(loaded[d] and min(loaded[d])<first for d in ('data-api','ui-design')),
            'explicit_documentation_orchestrator':'documentation-orchestrator' in texts,
            'project_markdown_reads':[p['paths'][0] for p in observed['ledger'] if p['tool']=='read' and p['status']=='completed' and p['paths'] and p['paths'][0].endswith('.md')],
            'application_audit':'pending_manual_source_and_test_review'}


def analyze(root):
    arms=[]
    for path in sorted((root/'transport').glob('*.json')):
        result=json.loads(path.read_text())
        cell=path.stem
        arm='adjusted' if '-ADJUSTED-' in cell else 'odd'
        events=result['events']
        observed=inspect_events(events)
        record_path=root/'records'/(cell+'.json')
        record=json.loads(record_path.read_text()) if record_path.exists() else None
        measurement=experiment.totals(events)
        arms.append({'cell':cell,'arm':arm,'repeat':int(cell.rsplit('r',1)[1]),
                     'model':result['model_requested'],'variant':result['variant_requested'],
                     'seconds':result['seconds'],'measurement':measurement,
                     'healthy':bool(record and record['healthy'] and result.get('stop_reason') is None),
                     'stop_reason':result.get('stop_reason'),
                     'functional_pass':record['functional_pass'] if record else None,
                     'evaluation':record['evaluation'] if record else None,
                     'changed_files':record['changed_files'] if record else None,
                     'fidelity':fidelity(root,arm,events,observed),'observed':observed})
    batch_path=root/'batch-result.json'
    batch=json.loads(batch_path.read_text()) if batch_path.exists() else None
    comparison=None
    if len(arms)==4 and all(row['measurement']['complete'] for row in arms):
        aggregate={}
        for arm in ('odd','adjusted'):
            selected=[r for r in arms if r['arm']==arm]
            aggregate[arm]={'tokens':sum(r['measurement']['observed']['comparable_tokens'] for r in selected),
                            'seconds':sum(r['seconds'] for r in selected),
                            'rounds':sum(r['observed']['rounds'] for r in selected)}
        control,treated=aggregate['odd'],aggregate['adjusted']
        pairs=[]
        for repeat in (1,2):
            a=next(r for r in arms if r['arm']=='odd' and r['repeat']==repeat)
            b=next(r for r in arms if r['arm']=='adjusted' and r['repeat']==repeat)
            pairs.append({'repeat':repeat,'token_delta_pct':100*(b['measurement']['observed']['comparable_tokens']/a['measurement']['observed']['comparable_tokens']-1)})
        comparison={'aggregate':aggregate,'pairs':pairs,'token_delta_pct':100*(treated['tokens']/control['tokens']-1),
                    'time_delta_pct':100*(treated['seconds']/control['seconds']-1),
                    'acceptance_requires_manual_fidelity_audit':True,'production_approved':False}
    return {'protocol':experiment.PROTOCOL,'expected_conversations':4,'observed_conversations':len(arms),
            'batch':batch,'arms':arms,'comparison':comparison,
            'limits':'No absent counters treated as zero; observed partial sums are not complete totals; no production conclusion'}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('root',type=Path)
    parser.add_argument('destination',type=Path)
    args=parser.parse_args()
    result=analyze(args.root.resolve())
    with args.destination.open('x') as output:
        json.dump(result,output,ensure_ascii=False,indent=2)
    print(json.dumps({'observed_conversations':result['observed_conversations'],'batch':result['batch'],
                      'comparison':result['comparison']},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
