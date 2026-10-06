import json
import re
from pathlib import Path


def test_training_notebook_contains_reproducible_v02_pipeline():
    path = Path("notebooks/model_training_v0_2.ipynb")
    nb = json.loads(path.read_text(encoding="utf-8"))
    text = "\n".join("".join(cell.get("source", [])) for cell in nb["cells"])

    assert "MODEL_PIPELINE_VERSION" in text
    assert "training.train" in text
    assert "training.calibrate_thresholds" in text
    assert "training.evaluate" in text
    assert "scripts.package_hf_model" in text
    assert "torch.cuda.is_available()" in text
    assert "training_complete.json" in text
    assert "FINAL_ACCEPTANCE_REPORT.json" in text
    assert "TRAINING_SIGNATURE" in text
    assert "semantic_integrity_model_cache" in text
    assert "REPOSITORY_ID = 1407563428" in text
    assert 'default_branch = "main"' in text
    assert 'project_root = workspace / "Amanah AI model"' in text
    assert "os.chdir(project_root)" in text
    assert "YOUR_REPO_URL" not in text


def test_shared_submission_docs_do_not_embed_secret_values():
    paths = [
        Path("README.md"),
        Path("MODEL_CARD.md"),
        Path("docs/REPRODUCIBILITY.md"),
        Path("docs/SECURITY.md"),
        Path("notebooks/model_training_v0_2.ipynb"),
    ]
    combined = "\n".join(p.read_text(encoding="utf-8") for p in paths)
    assert re.search(r"hf_[A-Za-z0-9]{20,}", combined) is None
    assert re.search(r"sk-[A-Za-z0-9_-]{20,}", combined) is None
    assert "BEGIN PRIVATE KEY" not in combined
