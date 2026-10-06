# API Reference

## Transport

AMANAH exposes a JSON inference contract. In production, the web application calls the model from a server-side environment.

### Endpoint configuration

The repository intentionally contains no endpoint credential.

Required environment names:
```env
AMANAH_ML_URL=<configured by deployment owner>
AMANAH_ML_TOKEN=<configured in server-side secret manager>
```

## Request

Method: `POST`

Headers:
```http
Content-Type: application/json
Authorization: Bearer <server-side token>
X-Scale-Up-Timeout: 600
```

Body:
```json
{
  "inputs": {
    "source_type": "quran",
    "source_ar": "canonical Arabic ayah text",
    "candidate_en": "candidate English translation",
    "ayah_id": "2:256"
  }
}
```

`ayah_id` is strongly recommended because it permits deterministic trusted-reference lookup.

## Response schema

```json
{
  "decision": "PASS",
  "integrity_score": 100,
  "severity": "S0",
  "confidence": 0.998,
  "drifts": [],
  "needs_human_review": false,
  "model_version": "amanah-semantic-integrity-v0.2",
  "reference_status": "verified",
  "notes": []
}
```

### Decision semantics

- `PASS`: no material drift detected by the current pipeline.
- `REVIEW`: potential semantic drift; human review recommended.
- `CRITICAL`: high-impact semantic drift detected; human review required.
- `ABSTAIN`: the system cannot verify safely; human review required.

### Reference status

Typical values:
- `verified`
- `missing`
- `unverified_provenance`
- `source_mismatch`

## Failure policy

If the inference service is unavailable, the application should not substitute an ungrounded LLM verdict. The correct safety behavior is an unavailable/abstain state and human review.

## Local API

After installing dependencies and providing a compatible local packaged checkpoint/reference store:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Inspect `api/main.py`, `api/routes.py`, and `deployment/hf_handler.py` for the concrete runtime wrappers.
