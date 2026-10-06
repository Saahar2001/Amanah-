# AMANAH Challenge Submission Checklist

## Repository
- [x] Root README explains the project and repository layout.
- [x] `Amanah AI model/` contains model code, training, evaluation, tests, notebooks, metrics, figures, and documentation.
- [x] `Amanah Website/` is separated from the ML implementation.
- [x] No production token or secret is committed.
- [x] Reproducibility and security instructions are documented.

## Model evidence
- [x] Frozen held-out metrics are stored in machine-readable form.
- [x] Per-label F1 is included.
- [x] Dataset split and leakage policy are documented.
- [x] Training configuration is included.
- [x] 35:28 and 2:2 regression gates are documented.
- [x] Canonical source mismatch is fail-closed.
- [x] Unit/regression tests are included.

## Presentation
- [x] Architecture figure.
- [x] Overall metrics figure.
- [x] Per-label F1 figure.
- [x] Dataset split figure.
- [x] Fair baseline-comparison protocol.
- [x] Claim boundaries and limitations.

## Before final submission
- [ ] Add the final website source under `Amanah Website/`.
- [ ] Verify the public demo URL.
- [ ] Run GitHub Actions successfully on the final commit.
- [ ] Run a final secret scan.
- [ ] Confirm presentation numbers match `Amanah AI model/results/metrics.json`.
- [ ] Keep production tokens only in the deployment platform secret manager.
