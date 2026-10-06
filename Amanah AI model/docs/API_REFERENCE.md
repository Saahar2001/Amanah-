# API Reference

## Published model for independent review

**Hugging Face model repository**  
https://huggingface.co/SaharIsmail/semantic-integrity-v0-1

**Validated AMANAH v0.2 revision**  
https://huggingface.co/SaharIsmail/semantic-integrity-v0-1/tree/v0.2-validated

Revision: `v0.2-validated`

### Reviewer credential policy

For authenticated Hugging Face API or Inference Endpoint testing, reviewers should use a **personal Hugging Face access token from their own Hugging Face account**.

- The AMANAH team does **not** publish or share its production token.
- No token, endpoint secret, API key, or password is committed to this repository.
- Reviewers should grant only the Hugging Face permissions required for the action they perform.
- Keep tokens in environment variables, Colab Secrets, or the reviewer's own secret manager.
- Never paste a real token into source code, screenshots, issues, or commits.

A reviewer can inspect the public model repository directly. A personal Hugging Face token is used when the chosen Hugging Face workflow requires authenticated download, API access, or deployment of an Inference Endpoint.

## Quick test path A — run locally

### 1. Clone the challenge repository

```bash
git clone https://github.com/Saahar2001/Amanah-.git
cd "Amanah-/Amanah AI model"
```

### 2. Create the Python environment

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Create a personal Hugging Face token

From the reviewer's own Hugging Face account, create an access token in **Settings → Access Tokens**. Use the minimum permissions needed for the intended action.

Store it only in the current environment:

```bash
export HF_TOKEN="<reviewer-personal-hugging-face-token>"
# PowerShell: $env:HF_TOKEN="<reviewer-personal-hugging-face-token>"
```

### 4. Download the validated model package

```bash
hf download SaharIsmail/semantic-integrity-v0-1 \\
  --revision v0.2-validated \\
  --local-dir ./artifacts/model \\
  --token "$HF_TOKEN"
```

The published package contains the trained checkpoint, tokenizer/configuration files, calibrated thresholds, `reference_store.json`, and the custom Hugging Face handler/runtime files required by the validated release.

### 5. Point the local API to the downloaded package

```bash
export MODEL_DIR="./artifacts/model"
export SOURCE_REGISTRY_PATH="./artifacts/model/reference_store.json"
# PowerShell:
# $env:MODEL_DIR="./artifacts/model"
# $env:SOURCE_REGISTRY_PATH="./artifacts/model/reference_store.json"
```

### 6. Start AMANAH locally

```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000
```

Check readiness:

```bash
curl http://127.0.0.1:8000/ready
```

Then call:

```text
POST http://127.0.0.1:8000/v1/analyze
```

The local API is unauthenticated unless the reviewer explicitly sets `AMANAH_API_TOKEN`.

## Quick test path B — deploy on the reviewer's Hugging Face account

1. Open the validated model revision: https://huggingface.co/SaharIsmail/semantic-integrity-v0-1/tree/v0.2-validated
2. Sign in to the reviewer's own Hugging Face account.
3. Create an **Inference Endpoint** from the published AMANAH model package and select revision `v0.2-validated`.
4. Use the reviewer's own Hugging Face token/endpoint authorization; do not request or reuse the AMANAH team's production credential.
5. After the endpoint is ready, set:

```bash
export AMANAH_ML_URL="https://<reviewer-endpoint>.endpoints.huggingface.cloud"
export AMANAH_ML_TOKEN="<reviewer-personal-endpoint-token>"
```

6. Send the request shown below directly to `$AMANAH_ML_URL`.

---

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
