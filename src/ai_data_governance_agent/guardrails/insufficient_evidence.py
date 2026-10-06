"""Deterministic behavior for incidents without available evidence."""

from ai_data_governance_agent.domain.response import RecommendedAction

INSUFFICIENT_EVIDENCE_CONFIDENCE_CEILING = 0.50

INSUFFICIENT_EVIDENCE_EXECUTIVE_SUMMARY = (
    "Evidence is insufficient to establish a reliable root cause. "
    "Additional investigation is required."
)


def cap_insufficient_evidence_confidence(
    confidence: float,
) -> float:
    """Limit confidence when no evidence is available."""
    return min(
        confidence,
        INSUFFICIENT_EVIDENCE_CONFIDENCE_CEILING,
    )


def build_additional_investigation_recommendation() -> RecommendedAction:
    """Return the safe deterministic action used without evidence."""
    return RecommendedAction(
        description=(
            "Collect and validate additional evidence before "
            "drawing root-cause conclusions or planning remediation."
        ),
        priority="high",
        rationale=(
            "The incident does not contain evidence sufficient "
            "to support a reliable analytical conclusion."
        ),
        requires_human_approval=False,
        supporting_evidence=[],
    )


__all__ = [
    "INSUFFICIENT_EVIDENCE_CONFIDENCE_CEILING",
    "INSUFFICIENT_EVIDENCE_EXECUTIVE_SUMMARY",
    "build_additional_investigation_recommendation",
    "cap_insufficient_evidence_confidence",
]
