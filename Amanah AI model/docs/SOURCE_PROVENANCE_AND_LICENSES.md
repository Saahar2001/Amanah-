# Source Provenance and License Notes

## Canonical Qur'anic Arabic

The submission source-governance policy prioritizes the **King Fahd Glorious Qur'an Printing Complex (KFGQPC)** developer resources for challenge-aligned canonical Qur'anic data.

Developer resources: https://qurancomplex.gov.sa/en/techquran/dev/

Canonical Qur'anic Arabic is treated as immutable source data. Synthetic mutations are applied only to separate candidate records and never to the canonical text.

## English reference translations

**QuranEnc.com**  
API documentation: https://quranenc.com/en/home/api

Validated English reference keys include:

- `english_rwwad` — Rowwad Translation Center
- `english_saheeh` — Noor International Center
- `english_hilali_khan` — Hilali & Khan

Published reference translations are stored unchanged. Synthetic mutations are written only to separate candidate records and are never represented as published QuranEnc translations.

The retrieval pipeline preserves source key, version, retrieval timestamp, source URL, and checksums so every reference remains traceable and auditable.

## Base model

Training base: `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`.

Required model attribution and license metadata are retained with the deployed model package.

## Repository code

Repository licensing is governed by the LICENSE file when included in the challenge submission.
