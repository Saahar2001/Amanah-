# Security and Secret Management

## Policy

No production secret is stored in this repository.

Do not commit:
- Hugging Face access tokens;
- endpoint authorization tokens;
- API provider keys;
- private URLs that embed credentials;
- service-account JSON;
- private keys;
- copied Colab secret values.

## Environment variables

Only variable names and placeholders are documented:

```env
HF_TOKEN=<set in secret manager when publishing/deploying>
AMANAH_ML_URL=<server-side inference endpoint URL>
AMANAH_ML_TOKEN=<server-side endpoint authorization token>
```

## Browser boundary

`AMANAH_ML_TOKEN` must never be included in:
- client-side JavaScript bundles;
- public environment variables;
- browser localStorage;
- HTML source;
- screenshots or demo recordings;
- public logs.

The website must call the model from a server/worker layer.

## Repository review

Before challenge submission:
1. search the full repository history for `hf_`, `sk-`, `Bearer `, and private-key blocks;
2. confirm `.env` files are ignored;
3. keep only `.env.example`;
4. revoke any credential that was ever accidentally exposed.

## Endpoint behavior

Endpoint failure must not be replaced by an ungrounded LLM answer. The safe fallback is `ABSTAIN` with human review.
