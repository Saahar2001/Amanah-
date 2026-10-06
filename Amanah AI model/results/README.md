# Results

This directory contains the machine-readable values used in the AMANAH v0.2 challenge documentation.

## Files

- `metrics.json` — frozen held-out evaluation summary.
- `per_label_f1.csv` — per-class F1 values.
- `training_config.json` — measured run configuration.
- `release_gates.md` — high-impact regression and live-release cases.

## Provenance

The metrics correspond to training signature:
```text
74751fc19ce83158
```

The completed run reported:
- 3,323 test rows;
- 3,274 scored rows;
- 49 fail-closed overlength abstentions;
- 98.5254% coverage;
- 95.2615% Macro F1;
- 96.9518% Critical Drift Recall.

The values are also documented in `../docs/VALIDATION_RESULTS_V02.md`.

## Evaluation context

These values are the official measured results for the frozen AMANAH Qur'anic Arabic → English semantic-integrity benchmark associated with training signature `74751fc19ce83158`.
