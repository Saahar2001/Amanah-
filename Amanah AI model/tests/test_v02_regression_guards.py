from amanah_engine.semantic_rules import run_rules
from data.models import DriftLabel


def labels(findings):
    return {f.label for f in findings}


def test_fatir_35_28_agency_reversal_is_caught():
    reference = "Only those of His servants who have knowledge fear Allāh."
    wrong = "Only Allah fears the knowledgeable among His servants."
    assert DriftLabel.AGENCY_SHIFT in labels(run_rules(reference, wrong))


def test_fatir_35_28_correct_direction_is_not_flagged_as_agency_shift():
    reference = "Only those of His servants who have knowledge fear Allāh."
    correct = "Only those fear Allah, from among His servants, who have knowledge."
    assert DriftLabel.AGENCY_SHIFT not in labels(run_rules(reference, correct))


def test_semantic_negation_equivalence_does_not_false_alarm():
    reference = "This is the Book about which there is no doubt."
    candidate = "This is the Book, beyond doubt."
    assert DriftLabel.NEGATION_FLIP not in labels(run_rules(reference, candidate))
