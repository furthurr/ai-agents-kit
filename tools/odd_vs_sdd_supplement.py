#!/usr/bin/env python3
"""Run six separately frozen supplementary ODD-vs-SDD cells."""
import concurrent.futures
import importlib.util
import json
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
runner = Path(__file__).resolve().parent / 'odd_vs_sdd_experiment.py'
spec = importlib.util.spec_from_file_location('odd_experiment', runner)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
assert module.ROOT == root
frozen = json.loads((root / 'freeze.json').read_text())
assert frozen['inputs'] == module.frozen_inputs()
jobs = [('S08', 'A', 4), ('S08', 'B', 4), ('S09', 'B', 4),
        ('S09', 'A', 4), ('S10', 'A', 4), ('S10', 'B', 4)]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    for result in pool.map(lambda job: module.cell(*job), jobs):
        print(result['cell'], 'pass=', result['functional_pass'],
              'returncodes=', result['returncodes'], 'seconds=', result['seconds'], flush=True)
