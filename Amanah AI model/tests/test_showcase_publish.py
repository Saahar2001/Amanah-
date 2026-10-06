import json
from pathlib import Path


def test_validated_publisher_is_no_training_release_flow():
    path = Path("notebooks/publish_v0_2_from_drive_cpu.ipynb")
    nb = json.loads(path.read_text(encoding="utf-8"))
    text = "\n".join("".join(cell.get("source", [])) for cell in nb["cells"])

    assert "scripts.package_hf_model" in text
    assert "CPU FULL-HANDLER RELEASE GATES: PASS" in text
    assert "HF VALIDATED UPLOAD: PASS" in text
    assert "v0.2-validated" in text
    assert "training.train" not in text
    assert "create_inference_endpoint" not in text


def test_model_card_contains_current_measured_results():
    text = Path("MODEL_CARD.md").read_text(encoding="utf-8")
    assert "95.2615%" in text
    assert "96.9518%" in text
    assert "2.9499%" in text
    assert "3,323" in text
    assert "32,621" in text
    assert "pipeline_tag: text-classification" in text
    assert "endpoints-template" in text
