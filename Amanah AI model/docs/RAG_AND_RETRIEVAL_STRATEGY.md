# Retrieval and RAG Strategy

## Current v0.2 design

The Qur'an v0.2 pipeline uses **deterministic exact retrieval** as its primary grounding mechanism.

For Qur'anic translation integrity, AMANAH normally receives an `ayah_id`. Because the verse identifier is known, exact keyed retrieval provides direct, auditable access to the trusted reference record.

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

## Hybrid architecture rationale

Each layer has a distinct role:
- retrieval supplies trusted evidence and context;
- the fine-tuned classifier identifies the semantic-drift category;
- deterministic rules protect high-impact semantic cases;
- the service layer produces the final structured decision.

This separation keeps the pipeline grounded, reproducible, and auditable.

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

## Cost and scalability

RAG reduces the need to retrain the classifier when the knowledge base expands, while the trained classifier preserves a stable semantic-drift taxonomy.

AMANAH therefore uses a hybrid strategy:
- trained model for measured semantic-drift classification;
- exact retrieval for Qur'an v0.2;
- high-precision rules for critical failure classes;
- RAG as the planned scalable retrieval layer for source-heavy Hadith/Tafsir expansion.

## Evaluation plan

RAG-based Hadith/Tafsir expansion is designed with its own labeled benchmark so each capability can be reported with dedicated, traceable metrics.
