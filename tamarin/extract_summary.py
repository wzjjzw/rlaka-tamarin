#!/usr/bin/env python3
import csv
import re
from pathlib import Path
root = Path(__file__).resolve().parent
text = (root / 'tamarin_output.txt').read_text()
summary = text.split('summary of summaries:')[-1]
rows = re.findall(r'^\s+(\w+) \((all-traces|exists-trace)\): ([^\n]+?) \((\d+) steps\)', summary, re.M)
if not rows:
    raise RuntimeError('No lemma summary found in the actual output.')
with (root / 'lemma_results.csv').open('w', newline='') as f:
    w=csv.writer(f);w.writerow(['lemma','trace_quantifier','result','proof_steps']);w.writerows(rows)
print(f'Extracted {len(rows)} lemma results from the actual Tamarin log.')
