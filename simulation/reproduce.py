#!/usr/bin/env python3
"""Regenerate Supplementary Tables S4-S5 using the manuscript's synthetic model."""
import csv
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parent / 'results'
OUT.mkdir(exist_ok=True)
if np.__version__ != '2.3.5':
    raise RuntimeError('Install numpy==2.3.5 for the recorded reproduction environment.')
expected = {2: ['21.99', '2.00', '25.28'], 3: ['32.00', '3.00', '36.94'], 4: ['42.01', '4.00', '48.60']}
summary = []
checks = []
for n in (2, 3, 4):
    rng = np.random.Generator(np.random.PCG64(np.random.SeedSequence([20261014, n])))
    # One interval per trial reused for all N failures, then an independent probe draw.
    retry = rng.normal(10.0, 1.0, 100000)
    probe = rng.normal(2.0, 0.1, 100000)
    delay = n * retry + probe
    samples = np.column_stack((np.arange(1, 100001), np.full(100000, n), retry, probe, delay))
    np.savetxt(OUT / f'diagnostic_latency_samples_N{n}.csv', samples,
               delimiter=',', header='trial_id,N,retry_interval_ms,probe_duration_ms,detect_latency_ms',
               comments='', fmt=['%d', '%d', '%.17g', '%.17g', '%.17g'])
    values = [float(delay.mean()), float(delay.std(ddof=1)), float(np.quantile(delay, .95, method='linear'))]
    row = dict(N=n, trials=100000, nominal_mean_ms=n * 10 + 2,
               simulated_mean_ms=values[0], sample_std_ms=values[1], percentile95_ms=values[2])
    summary.append(row)
    rounded = [f'{v:.2f}' for v in values]
    checks.append(dict(N=n, expected=expected[n], reproduced=rounded, matches=rounded == expected[n]))
    print(f'N={n}: mean={values[0]:.8f}, std={values[1]:.8f}, p95={values[2]:.8f}; Table S5 match={checks[-1]["matches"]}')
with (OUT / 'diagnostic_latency_summary.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(summary[0])); w.writeheader(); w.writerows(summary)
with (OUT / 'table_S4_analytical_probabilities.csv').open('w', newline='') as f:
    w = csv.writer(f); w.writerow(['N','p','analytical_alert_probability','expected_count_per_100000_windows'])
    for p in (.05,.10,.20,.30,.50):
        w.writerow([3,p,format(p**4,'.12g'),format(100000*p**4,'.12g')])
metadata = dict(generated_utc=datetime.now(timezone.utc).isoformat(), python=sys.version,
                numpy=np.__version__, platform=platform.platform(),
                result_origin='New execution of a reproduction script constructed from Supplementary Section S6.3; not original author-run files.',
                generator='PCG64', seed_sequence='[20261014, N]', trials_per_N=100000,
                retry_normal_ms=dict(mean=10.0,std=1.0), probe_normal_ms=dict(mean=2.0,std=.1),
                draw_order='All 100000 retry samples, then all 100000 probe samples for each N.',
                formula='detect_latency_ms = N * retry_interval_ms + probe_duration_ms',
                truncation='None', std_ddof=1, quantile_method='linear', table_S5_checks=checks)
(OUT / 'run_metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
assert all(c['matches'] for c in checks), 'Mismatch with Table S5'
