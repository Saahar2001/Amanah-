from __future__ import annotations

from amanah_engine.references import normalize_arabic
from amanah_engine.schemas import AnalyzeRequest, AnalyzeResponse, DriftFinding
from amanah_engine.semantic_rules import is_high_precision_assertion_negated, is_high_precision_negation_equivalent, run_rules
from amanah_engine.scoring import fuse_decision
from data.models import Decision, DriftLabel, Severity


def _consensus_rule_findings(references_en: list[str], candidate_en: str) -> list[DriftFinding]:
    if not references_en:
        return []

    per_reference = [run_rules(str(ref), candidate_en) for ref in references_en]

    # Most lexical rules remain strict consensus: every trusted reference must support
    # the same warning before it can override a model decision.
    common_labels = set(f.label for f in per_reference[0])
    for findings in per_reference[1:]:
        common_labels &= {f.label for f in findings}
    selected = [f for f in per_reference[0] if f.label in common_labels]

    # AGENCY_SHIFT is different: trusted translations may paraphrase the same relation
    # ("fear Allah", "are in awe of Allah", etc.), so requiring every translation to
    # match the same English regex can erase a real subject/object reversal.
    # The underlying rule is deliberately high precision; one trusted reference that
    # explicitly establishes the relation is sufficient evidence for REVIEW/CRITICAL.
    if not any(f.label == DriftLabel.AGENCY_SHIFT for f in selected):
        agency_candidates = [
            f
            for findings in per_reference
            for f in findings
            if f.label == DriftLabel.AGENCY_SHIFT
        ]
        if agency_candidates:
            selected.append(max(agency_candidates, key=lambda f: f.confidence))

    # A trusted reference that explicitly affirms "this/that is the Book" is
    # sufficient to reject a candidate that says "this/that is not the Book".
    # Requiring every translation to use the same copular wording would erase
    # this high-precision contradiction when other references paraphrase it.
    if not any(f.label == DriftLabel.NEGATION_FLIP for f in selected):
        explicit_negation_candidates = [
            f
            for ref, findings in zip(references_en, per_reference)
            for f in findings
            if f.label == DriftLabel.NEGATION_FLIP
            and is_high_precision_assertion_negated(str(ref), candidate_en)
        ]
        if explicit_negation_candidates:
            selected.append(max(explicit_negation_candidates, key=lambda f: f.confidence))

    return selected


class AmanahAnalysisService:
    def __init__(self, classifier, reference_store):
        self.classifier=classifier; self.reference_store=reference_store

    def readiness(self) -> dict:
        model_available = bool(getattr(self.classifier, "available", False))
        try:
            reference_count = len(self.reference_store)
        except (TypeError, AttributeError):
            reference_count = 0
        return {
            "ready": model_available and reference_count > 0,
            "model_available": model_available,
            "reference_count": reference_count,
        }

    def _abstain(self, model_version: str, note: str, reference_status: str) -> AnalyzeResponse:
        return AnalyzeResponse(decision=Decision.ABSTAIN,integrity_score=0,severity=Severity.S0,confidence=0.0,drifts=[],needs_human_review=True,model_version=model_version,reference_status=reference_status,notes=[note])

    def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        ayah_id = request.ayah_id or (f'{request.surah}:{request.ayah}' if request.surah and request.ayah else None)
        reference=self.reference_store.lookup(ayah_id)
        if reference is None and hasattr(self.reference_store, 'match_source_ar'):
            reference=self.reference_store.match_source_ar(request.source_ar)
        if reference is None:
            return self._abstain(getattr(self.classifier,'model_version','unknown'),"Trusted reference not found; provenance cannot be verified.","missing")
        if reference.get('provenance_verified') is not True:
            return self._abstain(getattr(self.classifier,'model_version','unknown'),"Trusted reference provenance is not verified.","unverified_provenance")
        canonical_ar = reference.get('source_ar')
        if canonical_ar and normalize_arabic(request.source_ar) != normalize_arabic(str(canonical_ar)):
            return self._abstain(getattr(self.classifier,'model_version','unknown'),"Submitted Arabic source does not match the trusted canonical source for this ayah.","source_mismatch")
        prediction=self.classifier.predict(request.source_ar,request.candidate_en)
        if not prediction.get('available'):
            return self._abstain(prediction.get('model_version','unavailable'),prediction.get('error','Model unavailable.'),"verified")
        refs=reference.get('references_en') or []
        if not refs:
            return self._abstain(prediction.get('model_version','unknown'),"Trusted English reference missing.","missing")
        # Reference-envelope rule findings must survive all approved references before they are treated as high-precision.
        rule_findings=_consensus_rule_findings([str(ref) for ref in refs],request.candidate_en)
        raw_findings=prediction.get('findings',[])
        model_findings=[x if isinstance(x,DriftFinding) else DriftFinding.model_validate(x) for x in raw_findings]

        # High-precision contradiction resolver for a known false-positive class:
        # the model can label "no doubt" -> "beyond doubt" as NEGATION_FLIP even
        # though both constructions preserve the same proposition. Suppress only
        # this narrow reviewed equivalence when it is supported by a trusted
        # reference; unrelated model negation findings remain untouched.
        if any(is_high_precision_negation_equivalent(str(ref), request.candidate_en) for ref in refs):
            model_findings=[
                finding for finding in model_findings
                if finding.label != DriftLabel.NEGATION_FLIP
            ]

        fused=fuse_decision(model_findings=model_findings,rule_findings=rule_findings,model_available=True,model_confidence=float(prediction.get('confidence',0.0)))
        return AnalyzeResponse(decision=fused.decision,integrity_score=fused.integrity_score,severity=fused.severity,confidence=fused.confidence,drifts=fused.findings,needs_human_review=fused.needs_human_review,model_version=prediction.get('model_version','unknown'),reference_status='verified',notes=fused.notes)
