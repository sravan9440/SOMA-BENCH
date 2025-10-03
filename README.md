# SOMA-Bench (Paper 2)
An open, synthetic **benchmark and evaluation harness** for IAM **sign-in**, **account recovery**, and **machine-credential rotation** with **PQC-aware overlays**.

- Code: Apache-2.0 • Docs/schemas: CC BY 4.0  
- Reproduces **Table 1/1B**, **Figs. 2–4**, and rotation SLO table.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/run_e1.py  # Baseline trade-offs (Table 1 + Fig. 2)
python scripts/run_e2.py  # PQC overlay effects (Fig. 3 + Table 1B)
python scripts/run_e3.py  # Drift & signal dropout (Figs. 4a/4b)
python scripts/run_e4.py  # Rotation rollout SLOs (Table 2)
```
Outputs go to `results/` (CSVs) and `figs/` (PNGs).

## What’s here
- **configs/** YAMLs for E1–E4 (seeds, fraud %, drift, dropout, overlay profile).
- **soma_bench/generator.py**: synthetic event generator (seeded).
- **soma_bench/baselines.py**: Static MFA + Trivial Risk baselines.
- **soma_bench/overlay.py**: classical/hybrid/PQC size & latency adders.
- **soma_bench/metrics.py**: fraud blocked, legit friction, p95, TTI, SLOs.
- **soma_bench/plotting.py**: clean Matplotlib charts.
- **scripts/**: one script per experiment.

## Cite
If you use this repository, please cite:
- Nidamanooru, **Identity Refined at the Quantum Gate: Framing the AI + Post-Quantum Challenge for IAM**, Zenodo, 2025. doi:10.5281/zenodo.16989599.
- This repository: *SOMA-Bench: An Open Synthetic Benchmark for Risk-Aware Recovery & Machine Identities in PQC-era IAM* (Apache-2.0).
