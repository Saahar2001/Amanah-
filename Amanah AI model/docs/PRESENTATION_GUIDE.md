# Presentation Guide for the Judging Team

## Recommended technical story

### Slide 1 — Problem
Translations of sensitive Islamic content can preserve fluent language while reversing agency, dropping conditions, changing modality, or altering negation.

### Slide 2 — Why generic similarity is insufficient
A semantically dangerous change may have high lexical overlap. AMANAH uses a drift taxonomy instead of a single similarity score.

### Slide 3 — Architecture
Use `figures/architecture.svg`.
Key message:
> Fine-tuned classifier + trusted references + high-precision semantic guards + fail-closed review.

### Slide 4 — Dataset and reproducibility
Use `figures/dataset_split.svg`.
Show:
- 6,236 ayat
- 32,621 examples
- ayah-grouped splits
- no split leakage
- deterministic seed

### Slide 5 — Results
Use `figures/metrics_overview.svg`.
Say exactly:
- Macro F1: 95.26%
- Critical Drift Recall: 96.95%
- Coverage: 98.53%
- False Safe Rate: 2.95%

Do not call Macro F1 “accuracy.”

### Slide 6 — Per-class behavior
Use `figures/per_label_f1.svg`.
Point out that CONDITION_LOSS is the weakest measured class (88.89% F1), which makes the evaluation more credible than showing only the best metric.

### Slide 7 — Safety engineering
Demo the 35:28 agency reversal:
- wrong direction → CRITICAL + AGENCY_SHIFT;
- correct direction → no AGENCY_SHIFT.

Then show 2:2:
- “beyond doubt” → no false negation alarm;
- “This is not the Book” → critical negation change.

### Slide 8 — Fail closed
Send mismatched Arabic with a valid ayah ID.
Expected:
`ABSTAIN / source_mismatch / human review`.

### Slide 9 — Comparison
Use `docs/BASELINE_COMPARISON.md`.
Compare architecture honestly. If another model has not been run on the same test split, do not invent a numeric score.

### Slide 10 — Expansion
Explain that Hadith/Tafsir are ideal for retrieval/RAG because source, grading, and traceability matter. They remain outside the current measured classifier benchmark until separately validated.

## Suggested 60-second live demo

1. Open the analysis form.
2. Submit a faithful translation → PASS.
3. Submit the 35:28 agency-reversed translation → CRITICAL.
4. Expand the drift evidence.
5. Show source/reference provenance.
6. End with the measured-results slide.

## Claims that are defensible

- “The classifier was trained and evaluated on a frozen held-out split.”
- “Macro F1 is 95.26%.”
- “Critical drift recall is 96.95%.”
- “The runtime fails closed on canonical-source mismatch.”
- “High-risk cases are protected by regression gates.”
- “The decision is structured and does not depend on an LLM explanation layer.”

## Claims to avoid

- “95% accuracy for all Islamic content.”
- “The model validates religious correctness.”
- “Hadith and Tafsir have the same measured performance.”
- “AMANAH is better than model X” without a same-split benchmark.
