from amanah_engine.schemas import AnalyzeRequest, DriftFinding
from amanah_engine.service import AmanahAnalysisService
from data.models import Decision, DriftLabel, Severity


class FakeNegationClassifier:
    available = True
    model_version = "test-v0.2"

    def predict(self, source_ar, candidate_en):
        return {
            "available": True,
            "confidence": 0.998,
            "severity": "S3",
            "findings": [
                DriftFinding(
                    label=DriftLabel.NEGATION_FLIP,
                    severity=Severity.S3,
                    confidence=0.998,
                    origin="model",
                )
            ],
            "model_version": self.model_version,
        }


class FakeFaithfulClassifier:
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


class TwoTwoStore:
    def __len__(self):
        return 1

    def lookup(self, ayah_id):
        if ayah_id != "2:2":
            return None
        return {
            "ayah_id": "2:2",
            "source_ar": "canonical-source",
            "provenance_verified": True,
            "references_en": [
                "This is the Book about which there is no doubt, a guidance for the mindful.",
                "This is the Book in which there is no doubt, a guidance for those conscious of Allah.",
            ],
        }


def test_service_suppresses_model_false_negation_for_beyond_doubt_equivalence():
    service=AmanahAnalysisService(FakeNegationClassifier(),TwoTwoStore())
    result=service.analyze(AnalyzeRequest(
        source_type="quran",
        source_ar="canonical-source",
        candidate_en="This is the Book, beyond doubt, a guidance for the mindful.",
        ayah_id="2:2",
    ))
    assert result.decision == Decision.PASS
    assert not any(x.label == DriftLabel.NEGATION_FLIP for x in result.drifts)


def test_service_does_not_suppress_unrelated_real_negation_change():
    service=AmanahAnalysisService(FakeNegationClassifier(),TwoTwoStore())
    result=service.analyze(AnalyzeRequest(
        source_type="quran",
        source_ar="canonical-source",
        candidate_en="This is not the Book, a guidance for the mindful.",
        ayah_id="2:2",
    ))
    assert any(x.label == DriftLabel.NEGATION_FLIP for x in result.drifts)
    assert result.decision == Decision.CRITICAL


def test_rules_catch_true_book_assertion_negation_even_when_model_says_faithful():
    service=AmanahAnalysisService(FakeFaithfulClassifier(),TwoTwoStore())
    result=service.analyze(AnalyzeRequest(
        source_type="quran",
        source_ar="canonical-source",
        candidate_en="This is not the Book, a guidance for the mindful.",
        ayah_id="2:2",
    ))
    assert any(
        x.label == DriftLabel.NEGATION_FLIP and x.origin == "rule"
        for x in result.drifts
    )
    assert result.decision == Decision.CRITICAL
