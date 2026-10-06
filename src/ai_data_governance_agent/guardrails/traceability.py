"""Deterministic validation and measurement of evidence traceability."""

from collections.abc import Iterable

from pydantic import BaseModel, ConfigDict, Field

from ai_data_governance_agent.domain.enums import (
    BusinessImpactStatus,
    HypothesisStatus,
)
from ai_data_governance_agent.domain.evidence import Evidence
from ai_data_governance_agent.domain.response import (
    BusinessImpact,
    GovernanceControl,
    RecommendedAction,
    RootCauseHypothesis,
)


class TraceabilityValidationError(ValueError):
    """Raised when analytical conclusions cannot be traced to evidence."""


class TraceabilityReport(BaseModel):
    """Represent deterministic traceability measurements."""

    model_config = ConfigDict(extra="forbid")

    available_evidence_ids: list[str] = Field(default_factory=list)
    referenced_evidence_ids: list[str] = Field(default_factory=list)
    invalid_evidence_ids: list[str] = Field(default_factory=list)
    missing_support: list[str] = Field(default_factory=list)

    total_claims: int = Field(ge=0)
    traceable_claims: int = Field(ge=0)
    traceability_rate: float = Field(ge=0.0, le=1.0)


def evaluate_traceability(
    *,
    evidence: Iterable[Evidence],
    business_impact: BusinessImpact,
    hypotheses: Iterable[RootCauseHypothesis],
    recommendations: Iterable[RecommendedAction],
    governance_controls: Iterable[GovernanceControl],
) -> TraceabilityReport:
    """Measure evidence traceability without raising validation errors."""
    evidence_items = list(evidence)
    hypothesis_items = list(hypotheses)
    recommendation_items = list(recommendations)
    control_items = list(governance_controls)

    available_ids = list(dict.fromkeys(item.evidence_id for item in evidence_items))
    known_ids = set(available_ids)

    referenced_ids: list[str] = []
    invalid_ids: list[str] = []
    missing_support: list[str] = []

    total_claims = 0
    traceable_claims = 0

    claims: list[
        tuple[
            str,
            list[str],
            bool,
        ]
    ] = []

    claims.append(
        (
            "business_impact",
            list(business_impact.supporting_evidence),
            business_impact.status
            in {
                BusinessImpactStatus.POTENTIAL,
                BusinessImpactStatus.CONFIRMED,
            },
        )
    )

    for index, hypothesis in enumerate(hypothesis_items):
        claims.append(
            (
                f"root_cause_hypothesis[{index}]",
                list(hypothesis.supporting_evidence),
                hypothesis.status
                in {
                    HypothesisStatus.PROBABLE,
                    HypothesisStatus.CONFIRMED,
                    HypothesisStatus.REJECTED,
                },
            )
        )

    for index, recommendation in enumerate(recommendation_items):
        claims.append(
            (
                f"recommended_action[{index}]",
                list(recommendation.supporting_evidence),
                bool(known_ids),
            )
        )

    for index, control in enumerate(control_items):
        claims.append(
            (
                f"governance_control[{index}]",
                list(control.supporting_evidence),
                True,
            )
        )

    for label, references, requires_support in claims:
        unique_references = list(dict.fromkeys(references))

        for evidence_id in unique_references:
            if evidence_id not in referenced_ids:
                referenced_ids.append(evidence_id)

            if evidence_id not in known_ids and evidence_id not in invalid_ids:
                invalid_ids.append(evidence_id)

        if not requires_support:
            continue

        total_claims += 1

        if not unique_references:
            missing_support.append(label)
            continue

        if all(evidence_id in known_ids for evidence_id in unique_references):
            traceable_claims += 1

    traceability_rate = traceable_claims / total_claims if total_claims else 1.0

    return TraceabilityReport(
        available_evidence_ids=available_ids,
        referenced_evidence_ids=referenced_ids,
        invalid_evidence_ids=invalid_ids,
        missing_support=missing_support,
        total_claims=total_claims,
        traceable_claims=traceable_claims,
        traceability_rate=traceability_rate,
    )


def validate_traceability(
    *,
    evidence: Iterable[Evidence],
    business_impact: BusinessImpact,
    hypotheses: Iterable[RootCauseHypothesis],
    recommendations: Iterable[RecommendedAction],
    governance_controls: Iterable[GovernanceControl],
) -> TraceabilityReport:
    """Validate traceability and return its deterministic report."""
    report = evaluate_traceability(
        evidence=evidence,
        business_impact=business_impact,
        hypotheses=hypotheses,
        recommendations=recommendations,
        governance_controls=governance_controls,
    )

    failures: list[str] = []

    if report.missing_support:
        failures.append("missing supporting evidence for: " + ", ".join(report.missing_support))

    if report.invalid_evidence_ids:
        failures.append("unknown evidence_id values: " + ", ".join(report.invalid_evidence_ids))

    if failures:
        raise TraceabilityValidationError("; ".join(failures))

    return report


__all__ = [
    "TraceabilityReport",
    "TraceabilityValidationError",
    "evaluate_traceability",
    "validate_traceability",
]
