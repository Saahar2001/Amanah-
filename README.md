# AMANAH | أمانة

**Semantic Integrity Engine for Islamic Content**

AMANAH is a research-oriented system for detecting semantic drift in translated Islamic content. The current measured release focuses on **Qur'anic Arabic → English translation integrity** and combines a fine-tuned multilingual classifier, trusted-reference retrieval, high-precision semantic rules, and fail-closed human-review behavior.

This repository is the challenge submission repository and is intentionally organized into two top-level components:

- **[Amanah AI model](./Amanah%20AI%20model/README.md)** — model architecture, training/evaluation code, notebooks, tests, metrics, release evidence, API contract, source-governance documentation, deployment notes, and presentation-ready figures.
- **[Amanah Website](./Amanah%20Website/README.md)** — the web-application area and server-side model integration contract.

## Measured release snapshot

| Item | Value |
|---|---:|
| Model version | `amanah-semantic-integrity-v0.2` |
| Base encoder | `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli` |
| Held-out test rows | 3,323 |
| Macro F1 | **95.26%** |
| Severity Macro F1 | **96.94%** |
| Critical Drift Recall | **96.95%** |
| Coverage | **98.53%** |
| Critical Coverage | **97.98%** |
| False Safe Rate | **2.95%** |
| Final black-box acceptance | **PASS** |
| Live release gates | **PASS** |

> **Metric note:** 95.26% is **Macro F1 on the frozen held-out test split**. It is not presented as universal “accuracy” for all Islamic content, all languages, Hadith, or Tafsir.

## Implemented pipeline

1. Fine-tuned multilingual semantic-drift classifier.
2. Trusted-reference retrieval by Qur'an verse identifier.
3. Canonical Arabic source verification with fail-closed behavior on mismatch.
4. High-precision semantic guards for known critical failure modes.
5. Decision fusion into `PASS`, `REVIEW`, `CRITICAL`, or `ABSTAIN`.
6. Reproducible training, calibration, evaluation, packaging, and deployment notebooks.
7. Protected Hugging Face Inference Endpoint integration.
8. Automated regression and CI tests.
9. Scientific-source governance documentation for Qur'an, Hadith, Tafsir, and terminology expansion.

## Security

No access tokens, API keys, passwords, or secret values are committed to this repository. Example environment files contain placeholders only. Runtime credentials must be supplied through environment variables or platform secret stores.

## Reproducibility

Start with **[Amanah AI model/README.md](./Amanah%20AI%20model/README.md)**. It documents the model design, data pipeline, training configuration, exact evaluation metrics, release gates, API request/response contract, local execution, deployment flow, and current limitations.

---

**Challenge release:** AMANAH v0.2  
**Repository:** https://github.com/Saahar2001/Amanah-
