# Retrieval and RAG Strategy

## Current v0.2 design

The measured Qur'an pipeline does **not** use generic vector-search RAG as the primary retrieval mechanism.

For Qur'anic translation integrity, AMANAH normally receives an `ayah_id`. Exact keyed retrieval is preferred because the verse identifier is known and deterministic. This avoids approximate-nearest-neighbor retrieval errors in a high-stakes content domain.

Current flow:
```text
ayah_id
  ↓
exact trusted-reference lookup
  ↓
canonical Arabic verification
  ↓
classifier + semantic rules
  ↓
structured decision
```

This is still a grounded retrieval architecture: the runtime decision is evaluated against a trusted reference record rather than relying on model memory.

## Why not replace the classifier with RAG?

RAG answers a different problem:
- retrieval supplies evidence and context;
- the fine-tuned classifier identifies the drift category;
- deterministic rules protect narrow critical cases;
- the service layer decides when to abstain.

Replacing the trained classifier with a general LLM over retrieved text would reduce reproducibility and make the structured drift taxonomy prompt-dependent.

## Where RAG is appropriate

RAG is well suited to future Hadith and Tafsir support because:
- a user query may not include a deterministic record identifier;
- multiple source documents may need to be retrieved;
- Hadith requires source and grading metadata;
- Tafsir requires traceability to named works and passages;
- evidence should be presented to the reviewer.

Recommended future flow:
```text
query / text
   ↓
metadata-aware retrieval
   ↓
approved Hadith / Tafsir evidence
   ↓
verification rules + model analysis
   ↓
grounded explanation
   ↓
human review when evidence is insufficient
```

## Cost perspective

RAG can reduce the need to retrain a model every time the knowledge base changes. It does not eliminate inference cost, and it does not by itself provide a validated semantic-drift classifier.

AMANAH therefore uses a hybrid strategy:
- trained model for measured semantic-drift classification;
- exact retrieval for Qur'an v0.2;
- high-precision rules for critical failure classes;
- RAG as the planned scalable retrieval layer for source-heavy Hadith/Tafsir expansion.

## Evaluation rule

RAG-based expansion must be evaluated separately. The Qur'an v0.2 Macro F1 must not be carried over to a Hadith/Tafsir RAG pipeline without a new labeled benchmark.
