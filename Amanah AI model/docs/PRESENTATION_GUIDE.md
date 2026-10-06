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

Present the result by its scientific metric name: **Macro F1 = 95.26%**.

### Slide 6 — Per-class behavior
Use `figures/per_label_f1.svg`.
Show the complete per-label profile to demonstrate consistent performance across multiple semantic-drift categories.

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
Use the same frozen benchmark protocol for every numerical baseline comparison.

### Slide 10 — Expansion
Explain the expansion architecture for Hadith/Tafsir using retrieval/RAG with source, grading, and traceability metadata.

## Suggested 60-second live demo

1. Open the analysis form.
2. Submit a faithful translation → PASS.
3. Submit the 35:28 agency-reversed translation → CRITICAL.
4. Expand the drift evidence.
5. Show source/reference provenance.
6. End with the measured-results slide.

## Recommended judge-facing claims

- “The classifier was trained and evaluated on a frozen held-out split.”
- “Macro F1 is 95.26%.”
- “Critical Drift Recall is 96.95%.”
- “Coverage is 98.53%.”
- “The runtime verifies canonical-source consistency and routes uncertain cases to human review.”
- “High-impact semantic cases are protected by explicit regression gates.”
- “The final decision is structured, reproducible, and grounded in trusted references.”
- “Numerical baseline comparisons use the same frozen benchmark protocol.”
