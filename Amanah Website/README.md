# Amanah Website

This directory is reserved for the challenge web application.

The model repository and website are intentionally separated at the top level so judges can inspect the ML implementation independently from the user interface.

## Model integration contract

The website should call AMANAH from a **server-side** route or worker.

Required runtime environment variables:

```env
AMANAH_ML_URL=<inference endpoint URL>
AMANAH_ML_TOKEN=<server-side authorization token>
```

Do not expose `AMANAH_ML_TOKEN` in browser JavaScript.

Request:

```json
{
  "inputs": {
    "source_type": "quran",
    "source_ar": "canonical Arabic ayah text",
    "candidate_en": "candidate English translation",
    "ayah_id": "35:28"
  }
}
```

Authoritative response fields:
- `decision`
- `integrity_score`
- `severity`
- `confidence`
- `drifts`
- `needs_human_review`
- `model_version`
- `reference_status`

If an LLM is used to generate an explanation, it must not overwrite these fields.

See `model-integration.example.ts` for a secret-safe server-side example.

> The website implementation can be added by the frontend team inside this directory without modifying the model package.
