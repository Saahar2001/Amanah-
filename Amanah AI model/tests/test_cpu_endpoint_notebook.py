import json
from pathlib import Path


def test_existing_endpoint_updater_is_control_only_and_no_training():
    path = Path("notebooks/update_existing_endpoint_v0_2_validated_cpu.ipynb")
    nb = json.loads(path.read_text(encoding="utf-8"))
    text = "\n".join("".join(cell.get("source", [])) for cell in nb["cells"])

    assert "semantic-integrity-v0-1-cpu" in text
    assert "v0.2-validated" in text
    assert "Existing endpoint" in text
    assert "LIVE 35:28 WRONG-AGENCY GATE: PASS" in text
    assert "LIVE 2:2 TRUE-NEGATION GATE: PASS" in text
    assert "LIVE SOURCE-MISMATCH FAIL-CLOSED GATE: PASS" in text
    assert "scale_to_zero" in text
    assert "create_inference_endpoint" not in text
    assert "training.train" not in text
