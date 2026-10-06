# Reproducibility Guide

This guide describes how a reviewer can inspect, test, retrain, evaluate, and package AMANAH without access to production secrets.

## 1. Environment

Recommended:
- Python 3.11+
- Git
- 16 GB RAM recommended for development
- CUDA-capable GPU recommended for retraining
- CPU is sufficient for unit tests and most packaging/control steps

```bash
cd "Amanah AI model"
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
# source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Run tests

```bash
pytest -q
```

The suite covers source contracts, dataset generation, split leakage checks, classifier loading, scoring, semantic rules, service behavior, packaging, training metrics, v0.2 regression guards, and API behavior.

## 3. Build the reference dataset

The measured pipeline is implemented in:
```text
scripts/fetch_verified_sources.py
scripts/prepare_amanah_sd.py
scripts/qa_dataset.py
```

Source metadata, versions, and checksums are preserved in the reference bundle.

## 4. Train

Primary notebook:
```text
notebooks/model_training_v0_2.ipynb
```

Equivalent training entry point:
```bash
python -m training.train --help
```

The notebook records a deterministic training signature and supports persistent checkpoint caching.

## 5. Calibrate and evaluate

```bash
python -m training.calibrate_thresholds --help
python -m training.evaluate --help
```

Evaluation reports coverage and abstention explicitly. Overlength rows are not silently removed from the report.

Measured release values are in `results/metrics.json` and `docs/VALIDATION_RESULTS_V02.md`.

## 6. Package for Hugging Face

```bash
python -m scripts.package_hf_model \
  --checkpoint /path/to/checkpoint \
  --reference-store /path/to/reference_store.json \
  --output /path/to/hf_package
```

The package includes the model artifacts plus the current runtime code required by the custom handler.

## 7. Secret handling

The code expects secret values at runtime only. Never place them in source code.

Example secret names:
```text
HF_TOKEN
AMANAH_ML_URL
AMANAH_ML_TOKEN
```

For Colab, store `HF_TOKEN` in Colab Secrets. For production, use the hosting platform's secret manager.

## 8. Validated publishing flow

- `notebooks/publish_v0_2_from_drive_cpu.ipynb`
  - reuses the completed checkpoint;
  - rebuilds the runtime package from current source;
  - runs packaged-handler regression gates;
  - uploads only after gates pass.

- `notebooks/update_existing_endpoint_v0_2_validated_cpu.ipynb`
  - updates an existing endpoint revision only;
  - refuses to create a new endpoint;
  - runs live 35:28, 2:2, and source-mismatch gates;
  - can scale the endpoint to zero after validation.

## 9. Model weights

Large trained weights are intentionally not committed to Git. This keeps the repository auditable and avoids mixing source control with large binary artifacts. Reviewers can inspect the complete training/evaluation process and reproduce a checkpoint from the notebook.

## 10. Reproducibility boundary

The reported 95.2615% Macro F1 belongs to training signature `74751fc19ce83158` and the frozen held-out split produced by that run. If the source corpus, labels, data generation, split, or preprocessing changes, metrics must be re-measured rather than carried over.
