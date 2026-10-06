# AMANAH v0.2 Release Gates

The final release pipeline includes local packaged-handler gates and live endpoint gates.

## Validated safety cases

### 35:28 — wrong agency
Input meaning reverses the fear relation:
```text
Only Allah fears the knowledgeable among His servants.
```

Expected and observed release behavior:
- decision: `CRITICAL`
- severity: `S3`
- drift: `AGENCY_SHIFT`
- human review: true
- reference status: verified

### 35:28 — correct direction
Expected:
- no `AGENCY_SHIFT`;
- valid candidate is not marked critical for agency reversal.

### 2:2 — reviewed semantic equivalence
Candidate uses “beyond doubt” where the trusted reference uses “no doubt.”

Expected:
- no `NEGATION_FLIP` solely because of that equivalence.

### 2:2 — true negation contradiction
Candidate explicitly negates the Book identity.

Expected:
- `NEGATION_FLIP`
- `REVIEW` or `CRITICAL`
- human review required

### Canonical Arabic mismatch
Expected:
- `ABSTAIN`
- integrity score 0
- `reference_status = source_mismatch`
- human review required

## Release principle

A checkpoint is not considered deployment-ready merely because the aggregate benchmark is strong. Known high-impact failure classes must also pass explicit regression gates through the full packaged handler and live endpoint.
