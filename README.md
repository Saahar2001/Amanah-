# AMANAH | أمانة

[![AMANAH Model CI](https://github.com/Saahar2001/Amanah-/actions/workflows/model-ci.yml/badge.svg)](https://github.com/Saahar2001/Amanah-/actions/workflows/model-ci.yml)

**Semantic Integrity Engine for Islamic Content**

AMANAH is a research-oriented semantic integrity system for detecting meaning drift in translated Islamic content. The current measured release focuses on **Qur'anic Arabic → English translation integrity** and combines a fine-tuned multilingual classifier, trusted-reference retrieval, high-precision semantic rules, and fail-closed human-review behavior.

**ملخص عربي:** أمانة هو نظام للتحقق من سلامة المعنى في ترجمة المحتوى الإسلامي. النسخة المقاسة حاليًا تختص بترجمة القرآن من العربية إلى الإنجليزية، وتجمع بين نموذج متعدد اللغات تم تخصيصه للمهمة، ومراجع موثوقة، وقواعد دلالية عالية الدقة، وآلية امتناع آمنة عند عدم كفاية الدليل.

## Repository layout

The challenge repository is intentionally split into two auditable components:

| Component | Purpose |
|---|---|
| **[Amanah AI model](./Amanah%20AI%20model/README.md)** | Model architecture, data pipeline, training/evaluation code, tests, notebooks, metrics, release evidence, API contract, source governance, security, and presentation figures |
| **[Amanah Website](./Amanah%20Website/README.md)** | Web-application area and secret-safe server-side model integration contract |

## Measured release snapshot

| Item | Value |
|---|---:|
| Model version | `amanah-semantic-integrity-v0.2` |
| Base encoder | `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli` |
| Canonical ayat represented | 6,236 |
| Total dataset samples | 32,621 |
| Held-out test rows | 3,323 |
| Macro F1 | **95.26%** |
| Severity Macro F1 | **96.94%** |
| Critical Drift Recall | **96.95%** |
| Coverage | **98.53%** |
| Critical Coverage | **97.98%** |
| False Safe Rate | **2.95%** |
| Final black-box acceptance | **PASS** |
| Live release gates | **PASS** |

> **Evaluation note:** All reported metrics are measured on the frozen held-out Qur'anic Arabic → English semantic-integrity benchmark.

## Implemented pipeline

1. Fine-tuned multilingual semantic-drift classifier.
2. Trusted-reference retrieval by Qur'an verse identifier.
3. Canonical Arabic source verification with fail-closed behavior on mismatch.
4. High-precision semantic guards for known critical failure modes.
5. Decision fusion into `PASS`, `REVIEW`, `CRITICAL`, or `ABSTAIN`.
6. Reproducible training, calibration, evaluation, packaging, and deployment notebooks.
7. Protected Hugging Face Inference Endpoint integration.
8. Automated unit, regression, data-quality, and CI tests.
9. Scientific-source governance documentation for Qur'an, Hadith, Tafsir, and terminology expansion.

## Review paths for judges

For a fast technical review:

1. **[Model README](./Amanah%20AI%20model/README.md)** — complete technical overview and run instructions.
2. **[Model Card](./Amanah%20AI%20model/MODEL_CARD.md)** — intended use, metrics, architecture, and safety design.
3. **[Measured metrics](./Amanah%20AI%20model/results/metrics.json)** — machine-readable benchmark values.
4. **[Architecture](./Amanah%20AI%20model/docs/ARCHITECTURE.md)** — system components and decision flow.
5. **[Reproducibility](./Amanah%20AI%20model/docs/REPRODUCIBILITY.md)** — setup, training, evaluation, packaging, and deployment procedure.
6. **[Baseline protocol](./Amanah%20AI%20model/docs/BASELINE_COMPARISON.md)** — fair comparison methodology without fabricated external scores.
7. **[Retrieval/RAG strategy](./Amanah%20AI%20model/docs/RAG_AND_RETRIEVAL_STRATEGY.md)** — why exact retrieval is used for Qur'an and where RAG fits future Hadith/Tafsir expansion.
8. **[API reference](./Amanah%20AI%20model/docs/API_REFERENCE.md)** — request/response contract without credentials.
9. **[Security](./Amanah%20AI%20model/docs/SECURITY.md)** — secret-management and fail-closed requirements.
10. **[Tests](./Amanah%20AI%20model/tests/)** — unit and regression evidence.

## Security

No production access tokens, API keys, passwords, or secret values are committed to this repository. Example environment files contain placeholders only. Runtime credentials must be supplied through environment variables or a platform secret store.

## Reproducibility

Start with **[Amanah AI model/README.md](./Amanah%20AI%20model/README.md)**. It documents the model design, data pipeline, training configuration, exact evaluation metrics, release gates, API request/response contract, local execution, deployment flow, source provenance, and validation evidence.

---

**Challenge release:** AMANAH v0.2  
**Repository:** https://github.com/Saahar2001/Amanah-
