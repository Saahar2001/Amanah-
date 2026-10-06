# Technical Architecture

## Overview

AMANAH is a hybrid semantic-integrity pipeline. It does not delegate the final safety decision to a general-purpose LLM.

```text
Ayah ID + Arabic source + candidate English
                 |
                 v
       Trusted Reference Store
                 |
       +---------+----------+
       |                    |
 canonical source      trusted English
    verification          references
       |                    |
       +---------+----------+
                 |
                 v
     Fine-tuned mDeBERTa classifier
                 |
                 +-------------------+
                 |                   |
                 v                   v
       model drift findings   high-precision rules
                 |                   |
                 +---------+---------+
                           |
                           v
                     decision fusion
                           |
        +------------------+------------------+
        |                  |                  |
      PASS              REVIEW/CRITICAL    ABSTAIN
                                             |
                                      human review required
```

## Classifier layer

`amanah_engine/classifier.py` loads the packaged checkpoint, calibrated thresholds, model metadata, tokenizer, and severity head. It supports both single-item and batched inference.

At runtime, the adapter pre-checks token length and routes inputs beyond the model context to the safe review path, preventing silent truncation.

## Reference layer

`amanah_engine/references.py` loads `reference_store.json` and resolves by ayah ID. Arabic normalization is used only for safe canonical matching. Duplicate normalized Arabic values are not auto-resolved.

## Semantic rules

`amanah_engine/semantic_rules.py` implements narrowly scoped, reviewable rules. Examples include:
- high-impact agency reversal;
- explicit negation contradiction;
- semantic equivalence for the reviewed “no doubt / beyond doubt” class;
- modality and quantifier changes;
- condition loss;
- strong omission heuristic.

Rules complement the trained model; they do not replace it.

## Service layer

`amanah_engine/service.py`:
1. resolves the trusted record;
2. validates provenance;
3. checks canonical Arabic;
4. obtains model findings;
5. applies reference-aware semantic rules;
6. applies narrow contradiction/equivalence resolvers;
7. calls decision fusion.

## Decision fusion

`amanah_engine/scoring.py` combines model and rule findings. High-precision S3 rule findings force `CRITICAL`; low model confidence can force `ABSTAIN`; any remaining findings require review.

## Deployment

`deployment/hf_handler.py` provides the Hugging Face custom inference handler. The same service can be wrapped with FastAPI using `api/`.

No production token is embedded in either implementation.
