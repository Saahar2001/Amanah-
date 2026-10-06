---
pipeline_tag: text-classification
library_name: transformers
language:
- ar
- en
tags:
- semantic-integrity
- quran-translation
- multilingual
endpoints-template:
- task: custom
---

# Model Card — AMANAH Semantic Integrity v0.2

## Model identifier
`amanah-semantic-integrity-v0.2`

## Intended use
Structured detection of semantic drift in **English candidate translations of Qur'anic Arabic**, conditioned on a trusted source record and integrated with runtime semantic safety rules.

## Base model
`MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`

## Output
The deployed service returns:
- decision: `PASS | REVIEW | CRITICAL | ABSTAIN`
- integrity score
- severity: `S0–S3`
- confidence
- structured drift findings
- human-review flag
- model version
- reference status
- notes

## Measured training labels
- FAITHFUL
- NEGATION_FLIP
- OMISSION
- MODALITY_SHIFT
- QUANTIFIER_CHANGE
- CONDITION_LOSS

Runtime-only high-precision guards extend protection to known critical failure modes such as AGENCY_SHIFT. Runtime guards are not represented as additional trained checkpoint labels in the reported classifier benchmark.

## Dataset
- 6,236 ayat represented
- 32,621 total samples
- 25,986 train
- 3,312 validation
- 3,323 test
- group split by ayah
- no ayah leakage reported
- no canonical mismatch reported
- no unknown ayah reported

## Measured evaluation
- Macro F1: 95.2615%
- Severity Macro F1: 96.9372%
- Critical Drift Recall: 96.9518%
- Coverage: 98.5254%
- Critical Coverage: 97.9769%
- False Safe Rate: 2.9499%
- Abstention Rate: 1.4746%

Per-label F1:
- FAITHFUL: 97.2373%
- NEGATION_FLIP: 95.4689%
- OMISSION: 97.2569%
- MODALITY_SHIFT: 96.3351%
- QUANTIFIER_CHANGE: 96.3821%
- CONDITION_LOSS: 88.8889%

## Training
- seed: 42
- target epochs: 5
- last completed epoch: 4
- early stopping: enabled
- batch size: 4
- gradient accumulation: 4
- learning rate: 2e-5
- max sequence length: 512
- best validation loss: 0.1448546965718427

## Safety design
1. canonical source verification;
2. trusted reference requirement;
3. fail-closed ABSTAIN behavior;
4. no silent runtime truncation beyond model context;
5. model + rule fusion;
6. explicit human-review state;
7. regression gates for known semantic failures.

## Known limitations
The measured results do not cover:
- Hadith verification;
- Tafsir correctness;
- Arabic → languages other than English;
- universal theological correctness;
- arbitrary long documents beyond model context.

The model must not be presented as a religious authority or fatwa system.

## Provenance note
The measured source-building script records Tanzil Uthmani Arabic and QuranEnc English references. Challenge-aligned source governance and the KFGQPC migration path are documented separately. The benchmark results should not be relabeled as originating from a source that was not used in the measured run.

## Reproducibility
See `README.md`, `docs/REPRODUCIBILITY.md`, `notebooks/model_training_v0_2.ipynb`, and `docs/VALIDATION_RESULTS_V02.md`.
