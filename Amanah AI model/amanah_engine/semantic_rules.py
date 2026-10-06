from __future__ import annotations

import re
from amanah_engine.schemas import DriftFinding
from data.models import DriftLabel, Severity

NEGATION = re.compile(r"\b(no|not|never|cannot|can't|does not|do not|did not)\b", re.I)
SEMANTIC_NEGATION = re.compile(r"\b(beyond doubt|without doubt|free from doubt|free of doubt)\b", re.I)
DOUBT_FREE = re.compile(r"\b(no doubt|beyond doubt|without doubt|free from doubt|free of doubt)\b", re.I)
ALLAH_FEARS = re.compile(r"\b(?:all[aā]h|god)\s+fears?\b", re.I)
FEAR_ALLAH = re.compile(r"\bfear(?:s|ed|ing)?\s+(?:all[aā]h|god)\b", re.I)
MODALITY = re.compile(r"\b(may|might|can|could|should|must|shall)\b", re.I)
QUANTIFIER = re.compile(r"\b(some|all|every|each|none|many|few)\b", re.I)
CONDITION = re.compile(r"\b(if|unless|provided that|when)\b", re.I)
BOOK_ASSERTION = re.compile(r"\b(?:this|that)\s+is\s+(?:the\s+)?book\b", re.I)
BOOK_ASSERTION_NEGATED = re.compile(r"\b(?:this|that)\s+is\s+not\s+(?:the\s+)?book\b", re.I)


def _first(pattern: re.Pattern, text: str) -> str | None:
    m=pattern.search(text)
    return m.group(0) if m else None


def _has_negative_meaning(text: str) -> bool:
    return bool(NEGATION.search(text) or SEMANTIC_NEGATION.search(text))


def is_high_precision_negation_equivalent(reference_en: str, candidate_en: str) -> bool:
    """Return True only for a narrow, reviewed equivalence class.

    This intentionally covers the Qur'an 2:2 style "no doubt" ↔ "beyond/without
    doubt" construction. It is not a general negation rewriter and must not be
    used to suppress unrelated polarity changes.
    """
    return bool(DOUBT_FREE.search(reference_en) and DOUBT_FREE.search(candidate_en))


def is_high_precision_assertion_negated(reference_en: str, candidate_en: str) -> bool:
    """Detect explicit negation of an affirmed Book identity relation.

    This is deliberately narrow: a trusted reference affirms "this/that is
    [the] Book" while the candidate explicitly says "this/that is not [the]
    Book". It covers the live 2:2 false-safe case without introducing a broad
    semantic-negation heuristic.
    """
    return bool(
        BOOK_ASSERTION.search(reference_en)
        and BOOK_ASSERTION_NEGATED.search(candidate_en)
        and not BOOK_ASSERTION_NEGATED.search(reference_en)
    )


def run_rules(reference_en: str, candidate_en: str) -> list[DriftFinding]:
    findings: list[DriftFinding] = []
    ref_neg, cand_neg = _first(NEGATION, reference_en), _first(NEGATION, candidate_en)
    if _has_negative_meaning(reference_en) != _has_negative_meaning(candidate_en):
        findings.append(DriftFinding(label=DriftLabel.NEGATION_FLIP,severity=Severity.S3,confidence=0.97,source_span=ref_neg,target_span=cand_neg,evidence="Negation meaning differs between trusted reference and candidate.",origin="rule"))

    if is_high_precision_assertion_negated(reference_en, candidate_en):
        findings.append(DriftFinding(
            label=DriftLabel.NEGATION_FLIP,
            severity=Severity.S3,
            confidence=0.995,
            source_span=_first(BOOK_ASSERTION, reference_en),
            target_span=_first(BOOK_ASSERTION_NEGATED, candidate_en),
            evidence="Candidate explicitly negates an identity relation affirmed by the trusted reference.",
            origin="rule",
        ))

    # High-precision semantic-role guard for the live-audit failure class exemplified by Qur'an 35:28.
    # If trusted references express people/servants fearing Allah while the candidate makes Allah the
    # grammatical agent of "fear", the relation has been reversed.
    if FEAR_ALLAH.search(reference_en) and ALLAH_FEARS.search(candidate_en) and not ALLAH_FEARS.search(reference_en):
        findings.append(DriftFinding(
            label=DriftLabel.AGENCY_SHIFT,
            severity=Severity.S3,
            confidence=0.995,
            source_span=_first(FEAR_ALLAH, reference_en),
            target_span=_first(ALLAH_FEARS, candidate_en),
            evidence="Agent and patient of the fear relation appear reversed relative to the trusted reference.",
            origin="rule",
        ))

    ref_modal, cand_modal = _first(MODALITY, reference_en), _first(MODALITY, candidate_en)
    if ref_modal and cand_modal and ref_modal.lower() != cand_modal.lower():
        findings.append(DriftFinding(label=DriftLabel.MODALITY_SHIFT,severity=Severity.S3,confidence=0.98,source_span=ref_modal,target_span=cand_modal,evidence="Modal force changed.",origin="rule"))

    ref_quant, cand_quant = _first(QUANTIFIER, reference_en), _first(QUANTIFIER, candidate_en)
    if ref_quant and cand_quant and ref_quant.lower() != cand_quant.lower():
        findings.append(DriftFinding(label=DriftLabel.QUANTIFIER_CHANGE,severity=Severity.S3,confidence=0.98,source_span=ref_quant,target_span=cand_quant,evidence="Quantifier changed.",origin="rule"))

    ref_cond, cand_cond = _first(CONDITION, reference_en), _first(CONDITION, candidate_en)
    if ref_cond and not cand_cond:
        findings.append(DriftFinding(label=DriftLabel.CONDITION_LOSS,severity=Severity.S3,confidence=0.98,source_span=ref_cond,target_span=None,evidence="Conditional marker from trusted reference is absent.",origin="rule"))

    ref_tokens=reference_en.split(); cand_tokens=candidate_en.split()
    if len(ref_tokens) >= 8 and len(cand_tokens) / max(1,len(ref_tokens)) < 0.45:
        findings.append(DriftFinding(label=DriftLabel.OMISSION,severity=Severity.S2,confidence=0.85,evidence="Candidate is substantially shorter than trusted reference; review for omitted meaning.",origin="rule"))
    return findings
