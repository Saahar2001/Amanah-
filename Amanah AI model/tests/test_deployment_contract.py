from pathlib import Path


def test_docker_runtime_contract_exists():
    docker = Path("deployment/Dockerfile").read_text(encoding="utf-8")
    assert "uvicorn api.main:app" in docker
    assert "8000" in docker


def test_hf_handler_exposes_analyze_contract():
    from deployment.hf_handler import EndpointHandler
    assert hasattr(EndpointHandler, "__call__")


def test_generated_reference_and_model_artifacts_are_gitignored():
    text = Path(".gitignore").read_text(encoding="utf-8")
    for required in [
        "data/private/",
        "data/reference_store.json",
        "checkpoints/",
        "artifacts/",
        "*.pt",
        "*.safetensors",
    ]:
        assert required in text


def test_env_example_points_to_runtime_reference_store_without_secrets():
    text = Path(".env.example").read_text(encoding="utf-8")
    assert "SOURCE_REGISTRY_PATH=data/reference_store.json" in text
    assert "HF_TOKEN=" in text
    assert "AMANAH_ML_TOKEN=" in text
    assert "hf_" not in text


def test_service_fails_closed_for_source_mismatch_and_missing_reference():
    text = Path("amanah_engine/service.py").read_text(encoding="utf-8")
    assert "source_mismatch" in text
    assert "Trusted reference not found" in text
    assert "needs_human_review=True" in text
    assert "Decision.ABSTAIN" in text
