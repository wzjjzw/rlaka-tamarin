#!/usr/bin/env python3
"""Run the unchanged repository theory and retain actual stdout/stderr."""
import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parent
out = root / 'rerun'
out.mkdir(exist_ok=True)
cmd = ['tamarin-prover', str(root / 'rlaka.spthy'), '--prove', '--bound=9', '--derivcheck-timeout=0']
meta = {'command': cmd, 'started_utc': datetime.now(timezone.utc).isoformat(),
        'platform': platform.platform(), 'GHCRTS': os.environ.get('GHCRTS', ''),
        'model_sha256': hashlib.sha256((root / 'rlaka.spthy').read_bytes()).hexdigest()}
for name, command in [('tamarin_version', ['tamarin-prover', '--version']), ('maude_version', ['maude', '--version'])]:
    r = subprocess.run(command, capture_output=True, text=True)
    meta[name] = r.stdout + r.stderr
with (out / 'tamarin_output.txt').open('wb') as log:
    result = subprocess.run(cmd, cwd=root, stdout=log, stderr=subprocess.STDOUT)
meta['exit_code'] = result.returncode
meta['finished_utc'] = datetime.now(timezone.utc).isoformat()
(out / 'run_metadata.json').write_text(json.dumps(meta, indent=2) + '\n')
print(f'Output saved in {out}; exit code {result.returncode}')
sys.exit(result.returncode)
