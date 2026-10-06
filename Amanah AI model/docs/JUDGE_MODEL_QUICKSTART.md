# AMANAH Model — Judge Quick Start

This document gives reviewers a direct, independent way to inspect and test the exact validated AMANAH model release without receiving any AMANAH team secret.

## Official review links

- **Challenge repository:** https://github.com/Saahar2001/Amanah-
- **AI model source folder:** https://github.com/Saahar2001/Amanah-/tree/main/Amanah%20AI%20model
- **Hugging Face model:** https://huggingface.co/SaharIsmail/semantic-integrity-v0-1
- **Validated model revision:** https://huggingface.co/SaharIsmail/semantic-integrity-v0-1/tree/v0.2-validated
- **Revision:** `v0.2-validated`
- **API reference:** ./API_REFERENCE.md
- **Measured metrics:** ../results/metrics.json
- **Validation evidence:** ./VALIDATION_RESULTS_V02.md

## Credential rule

For Hugging Face API / Endpoint testing, the reviewer uses a **personal Hugging Face token from their own account**.

AMANAH does not place production tokens, endpoint credentials, secret keys, or passwords in GitHub. Reviewers never need an AMANAH team token to inspect the code or published model package.

## Fastest independent test

### A. Clone source

```bash
git clone https://github.com/Saahar2001/Amanah-.git
cd "Amanah-/Amanah AI model"
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Windows PowerShell activation:

```powershell
.venv\Scripts\Activate.ps1
```

### B. Create the reviewer's Hugging Face token

Create it in the reviewer's own Hugging Face account under **Settings → Access Tokens**, then keep it only in an environment variable or secret manager:

```bash
export HF_TOKEN="<reviewer-personal-token>"
```

### C. Download the validated package

```bash
hf download SaharIsmail/semantic-integrity-v0-1 \
  --revision v0.2-validated \
  --local-dir ./artifacts/model \
  --token "$HF_TOKEN"
```

### D. Run the local API

```bash
export MODEL_DIR="./artifacts/model"
export SOURCE_REGISTRY_PATH="./artifacts/model/reference_store.json"
uvicorn api.main:app --host 127.0.0.1 --port 8000
```

Readiness:

```bash
curl http://127.0.0.1:8000/ready
```

### E. Analyze a translation

Local FastAPI request:

```bash
curl -X POST "http://127.0.0.1:8000/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "quran",
    "source_ar": "لَا إِكْرَاهَ فِي الدِّينِ",
    "candidate_en": "There is no compulsion in religion.",
    "ayah_id": "2:256"
  }'
```

Expected response fields include:

```text
decision
integrity_score
severity
confidence
drifts
needs_human_review
model_version
reference_status
notes
```

## Hugging Face Inference Endpoint test

A reviewer can also deploy the same published package on their own Hugging Face account:

1. Open https://huggingface.co/SaharIsmail/semantic-integrity-v0-1/tree/v0.2-validated
2. Create an Inference Endpoint from revision `v0.2-validated`.
3. Use the reviewer's own Hugging Face authentication/endpoint token.
4. Save the reviewer's endpoint URL and token as local environment variables:

```bash
export AMANAH_ML_URL="https://<reviewer-endpoint>.endpoints.huggingface.cloud"
export AMANAH_ML_TOKEN="<reviewer-personal-token>"
```

5. Call the endpoint:

```bash
curl -X POST "$AMANAH_ML_URL" \
  -H "Authorization: Bearer $AMANAH_ML_TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-Scale-Up-Timeout: 600" \
  -d '{
    "inputs": {
      "source_type": "quran",
      "source_ar": "لَا إِكْرَاهَ فِي الدِّينِ",
      "candidate_en": "There is no compulsion in religion.",
      "ayah_id": "2:256"
    }
  }'
```

## Security

- No real token is committed to this repository.
- No AMANAH production secret is required for review.
- The reviewer owns and controls their Hugging Face token.
- Tokens should be stored only in environment variables, Colab Secrets, or the reviewer's secret manager.
- The website calls protected inference only from the server side; tokens are never sent to browser code.

## Validation evidence

The model release is accompanied by:

- frozen held-out metrics;
- per-label F1;
- release gates;
- source verification tests;
- regression tests for 35:28 and 2:2;
- canonical-source mismatch handling;
- CI tests under `tests/`.

This allows the model to be reviewed both as a published artifact and as a reproducible software pipeline.
