"""Deterministic human-review rules for governed incident analysis."""

from pydantic import BaseModel, ConfigDict, Field, StrictBool

from ai_data_governance_agent.domain.enums import Severity

HUMAN_REVIEW_CONFIDENCE_THRESHOLD = 0.70


class HumanReviewSignals(BaseModel):
    """Represent explicit signals used to determine mandatory human review."""

    model_config = ConfigDict(extra="forbid")

    severity: Severity
    confidence: float = Field(ge=0.0, le=1.0)

    material_business_impact: StrictBool
    insufficient_evidence: StrictBool
    conflicting_evidence: StrictBool
    regulatory_exposure: StrictBool
    governance_exposure: StrictBool
    privacy_impact: StrictBool
    destructive_action: StrictBool
    irreversible_action: StrictBool
    high_root_cause_uncertainty: StrictBool
    unsafe_recommendation: StrictBool
    critical_process_affected: StrictBool


class HumanReviewDecision(BaseModel):
    """Represent the deterministic human-review decision and its reasons."""

    model_config = ConfigDict(extra="forbid")

    human_review_required: bool
    human_review_reasons: list[str]


def evaluate_human_review(
    signals: HumanReviewSignals,
) -> HumanReviewDecision:
    """Evaluate all mandatory human-review rules in deterministic order."""
    reasons: list[str] = []

    if signals.severity is Severity.CRITICAL:
        reasons.append("critical severity")

    if signals.severity is Severity.HIGH and signals.material_business_impact:
        reasons.append("high severity with material business impact")

    if signals.confidence < HUMAN_REVIEW_CONFIDENCE_THRESHOLD:
        reasons.append("low confidence")

    if signals.insufficient_evidence:
        reasons.append("insufficient evidence")

    if signals.conflicting_evidence:
        reasons.append("conflicting evidence")

    if signals.regulatory_exposure:
        reasons.append("regulatory exposure")

    if signals.governance_exposure:
        reasons.append("governance exposure")

    if signals.privacy_impact:
        reasons.append("privacy impact")

    if signals.destructive_action:
        reasons.append("destructive action")

    if signals.irreversible_action:
        reasons.append("irreversible action")

    if signals.high_root_cause_uncertainty:
        reasons.append("high root-cause uncertainty")

    if signals.unsafe_recommendation:
        reasons.append("safe recommendation cannot be determined")

    if signals.critical_process_affected:
        reasons.append("critical business process affected")

    return HumanReviewDecision(
        human_review_required=bool(reasons),
        human_review_reasons=reasons,
    )


__all__ = [
    "HUMAN_REVIEW_CONFIDENCE_THRESHOLD",
    "HumanReviewDecision",
    "HumanReviewSignals",
    "evaluate_human_review",
]
