# RLAKA research artifacts

Reproducibility files for **A Robust Lightweight Authentication and Key Agreement Protocol for Smart Home Environments**.

This package contains newly executed diagnostic-latency simulations and a fresh Tamarin run of the unchanged public RLAKA theory. It does not represent historical output files from the original manuscript preparation.

## Simulation data

The script `simulation/reproduce.py` implements the model and settings reported in Supplementary Section S6.3. It uses NumPy 2.3.5 and independently initializes `Generator(PCG64(SeedSequence([20261014, N])))` for N = 2, 3, 4.

Each N has 100000 trials. In each trial, one retry interval is drawn from a normal distribution with mean 10 ms and standard deviation 1 ms and reused for all N failures. The probe duration is drawn independently with mean 2 ms and standard deviation 0.1 ms. All retry samples are drawn before all probe samples. Normal draws are not truncated.

`detect_latency_ms = N * retry_interval_ms + probe_duration_ms`

The sample standard deviation uses `ddof=1`; the 95th percentile uses linear interpolation. This is a synthetic timing model, not measured hardware or network latency.

### Files

- `simulation/reproduce.py`: executable reproduction script constructed from the manuscript specification.
- `simulation/requirements.txt`: pinned NumPy dependency.
- `simulation/run_stdout.txt`: actual console output from this execution.
- `simulation/results/diagnostic_latency_samples_N2.csv`, `...N3.csv`, `...N4.csv`: all 300000 generated trials, exported with 17 significant digits.
- `simulation/results/diagnostic_latency_summary.csv`: unrounded simulated statistics and nominal means.
- `simulation/results/table_S4_analytical_probabilities.csv`: formula-derived values for Table S4, not Monte Carlo output.
- `simulation/results/run_metadata.json`: environment, generation time, parameters, and comparison against Table S5.

Sample CSV columns: `trial_id` is a 1-based index within N; `N` is the failure threshold; `retry_interval_ms` and `probe_duration_ms` are sampled inputs; `detect_latency_ms` is the computed output. All timing columns are in milliseconds.

The reproduced mean, sample standard deviation, and 95th percentile, rounded to two decimal places, match all nine corresponding Table S5 entries:

| N | Simulated mean (ms) | Sample standard deviation (ms) | 95th percentile (ms) |
|---|---:|---:|---:|
| 2 | 21.99 | 2.00 | 25.28 |
| 3 | 32.00 | 3.00 | 36.94 |
| 4 | 42.01 | 4.00 | 48.60 |

### Reproduce

From the package directory:

```bash
python -m pip install -r simulation/requirements.txt
python simulation/reproduce.py
```

The script overwrites its generated simulation results and updates the run metadata. Table S4 is computed with N = 3 as p^4, and its expected count is 100000*p^4.

## Tamarin output

Source repository: https://github.com/wzjjzw/rlaka-tamarin

The exact source commit and SHA-256 hash are recorded in `tamarin/run_metadata.json`. `tamarin/rlaka.spthy` is copied byte-for-byte from that commit. The upstream README and MIT license are retained as provenance files; the actual outcome of this execution is in `tamarin_output.txt`.

Execution used Tamarin 1.12.0 and Maude 3.5.1:

```bash
tamarin-prover rlaka.spthy --prove --bound=9 --derivcheck-timeout=0
```

This execution set `GHCRTS=-N2`. The command completed with exit code 0. Tamarin reported successful wellformedness checks and `verified` for all 13 lemmas. These results apply to the supplied symbolic theory and its stated lemmas; they are not an independent validation of the computational IU proofs or a new audit of correspondence between the model and the complete protocol.

### Files

- `tamarin/rlaka.spthy`: unchanged source theory.
- `tamarin/tamarin_output.txt`: complete actual output, including proof derivations and the final summary.
- `tamarin/lemma_results.csv`: machine-readable extraction of that final summary.
- `tamarin/run_metadata.json`: source commit, model checksum, tool versions, command, execution environment, timing, and exit status.
- `tamarin/run_tamarin.py`: reruns the theory using installed tools and saves new output under `tamarin/rerun/` without replacing the packaged log.
- `tamarin/extract_summary.py`: extracts the result CSV from the full packaged log.
- `tamarin/upstream_README.md` and `tamarin/LICENSE`: source repository documentation and license.

Install Tamarin 1.12.0 and Maude 3.5.1 and ensure both executables are on PATH. Then run:

```bash
python tamarin/run_tamarin.py
```

The 36-second processing time in this log is a tool runtime on the reproduction machine, not the protocol latency evaluated in the paper. Source and result integrity can be checked with `SHA256SUMS.txt`.
