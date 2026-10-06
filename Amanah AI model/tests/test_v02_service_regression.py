from amanah_engine.schemas import AnalyzeRequest
from amanah_engine.service import AmanahAnalysisService
from data.models import Decision


class FakeClassifier:
    available = True
    model_version = "test-v0.2"

    def predict(self, source_ar, candidate_en):
        return {
            "available": True,
            "confidence": 0.998,
            "severity": "S0",
            "findings": [],
            "model_version": self.model_version,
        }


class FakeStore:
    def __len__(self):
        return 1

    def lookup(self, ayah_id):
        if ayah_id != "35:28":
            return None
        return {
            "ayah_id": "35:28",
            "source_ar": "إِنَّمَا يَخْشَى اللَّهَ مِنْ عِبَادِهِ الْعُلَمَاءُ",
            "provenance_verified": True,
            "references_en": [
                "Only those of His servants who have knowledge fear Allah.",
                "Of His servants, only the knowledgeable are truly in awe of Allah.",
            ],
        }

    def match_source_ar(self, source_ar):
        return self.lookup("35:28")


def test_service_keeps_agency_shift_if_one_trusted_reference_states_relation_explicitly():
    service=AmanahAnalysisService(FakeClassifier(),FakeStore())
    result=service.analyze(AnalyzeRequest(
        source_type="quran",
        source_ar="إِنَّمَا يَخْشَى اللَّهَ مِنْ عِبَادِهِ الْعُلَمَاءُ",
        candidate_en="Only Allah fears the knowledgeable among His servants.",
        ayah_id="35:28",
    ))
    assert result.decision == Decision.CRITICAL
    assert any(x.label.value == "AGENCY_SHIFT" for x in result.drifts)


def test_service_does_not_raise_agency_shift_for_correct_direction():
    service=AmanahAnalysisService(FakeClassifier(),FakeStore())
    result=service.analyze(AnalyzeRequest(
        source_type="quran",
        source_ar="إِنَّمَا يَخْشَى اللَّهَ مِنْ عِبَادِهِ الْعُلَمَاءُ",
        candidate_en="Only those of His servants who have knowledge fear Allah.",
        ayah_id="35:28",
    ))
    assert not any(x.label.value == "AGENCY_SHIFT" for x in result.drifts)
