from pathlib import Path


def test_github_ci_runs_model_tests_from_submission_root():
    path = Path("..") / ".github" / "workflows" / "model-ci.yml"
    text = path.read_text(encoding="utf-8")
    assert 'working-directory: "Amanah AI model"' in text
    assert "pytest -q" in text
    assert 'python-version: "3.11"' in text
    assert "pip install -r requirements.txt" in text
