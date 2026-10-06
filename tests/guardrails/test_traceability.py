"""Tests for deterministic evidence traceability validation."""

import pytest

from ai_data_governance_agent.domain.evidence import Evidence
from ai_data_governance_agent.domain.response import (
    BusinessImpact,
    GovernanceControl,
    RecommendedAction,
    RootCauseHypothesis,
)
from ai_data_governance_agent.guardrails import (
    TraceabilityValidationError,
    evaluate_traceability,
    validate_traceability,
)


def make_evidence(
    evidence_id: str = "EV-001",
) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        evidence_type="data_quality_check",
        source="quality-report",
        value={"invalid_rows": 30},
    )


def unknown_impact() -> BusinessImpact:
    return BusinessImpact(
        status="unknown",
        description="Business impact is not established.",
    )


def probable_hypothesis(
    supporting_evidence: list[str],
) -> RootCauseHypothesis:
    return RootCauseHypothesis(
        description="Validation may have rejected invalid records.",
        supporting_evidence=supporting_evidence,
        confidence=0.80,
        status="probable",
    )


def recommendation(
    supporting_evidence: list[str],
) -> RecommendedAction:
    return RecommendedAction(
        description="Review invalid records.",
        priority="medium",
        rationale="Further investigation is required.",
        requires_human_approval=False,
        supporting_evidence=supporting_evidence,
    )


def governance_control(
    supporting_evidence: list[str],
) -> GovernanceControl:
    return GovernanceControl(
        control_id="DQ-001",
        title="Data Quality Review",
        description="Review detected data-quality failures.",
        source="local-policy-catalog",
        relevance="Invalid records were detected.",
        supporting_evidence=supporting_evidence,
    )


def test_empty_traceability_has_complete_rate() -> None:
    report = evaluate_traceability(
        evidence=[],
        business_impact=unknown_impact(),
        hypotheses=[],
        recommendations=[],
        governance_controls=[],
    )

    assert report.available_evidence_ids == []
    assert report.referenced_evidence_ids == []
    assert report.invalid_evidence_ids == []
    assert report.missing_support == []
    assert report.total_claims == 0
    assert report.traceable_claims == 0
    assert report.traceability_rate == 1.0


def test_fully_traceable_claims_have_rate_one() -> None:
    report = evaluate_traceability(
        evidence=[make_evidence()],
        business_impact=BusinessImpact(
            status="potential",
            description="Reporting may be incomplete.",
            supporting_evidence=["EV-001"],
        ),
        hypotheses=[probable_hypothesis(["EV-001"])],
        recommendations=[recommendation(["EV-001"])],
        governance_controls=[governance_control(["EV-001"])],
    )

    assert report.total_claims == 4
    assert report.traceable_claims == 4
    assert report.traceability_rate == 1.0
    assert report.invalid_evidence_ids == []
    assert report.missing_support == []


def test_partial_traceability_is_measurable() -> None:
    report = evaluate_traceability(
        evidence=[make_evidence()],
        business_impact=unknown_impact(),
        hypotheses=[probable_hypothesis(["EV-001"])],
        recommendations=[recommendation([])],
        governance_controls=[],
    )

    assert report.total_claims == 2
    assert report.traceable_claims == 1
    assert report.traceability_rate == 0.5

    assert report.missing_support == ["recommended_action[0]"]


def test_referenced_evidence_ids_are_deduplicated() -> None:
    report = evaluate_traceability(
        evidence=[make_evidence()],
        business_impact=unknown_impact(),
        hypotheses=[probable_hypothesis(["EV-001", "EV-001"])],
        recommendations=[recommendation(["EV-001"])],
        governance_controls=[],
    )

    assert report.referenced_evidence_ids == ["EV-001"]


def test_invalid_reference_is_reported() -> None:
    report = evaluate_traceability(
        evidence=[make_evidence()],
        business_impact=unknown_impact(),
        hypotheses=[probable_hypothesis(["EV-FAKE"])],
        recommendations=[],
        governance_controls=[],
    )

    assert report.invalid_evidence_ids == ["EV-FAKE"]
    assert report.total_claims == 1
    assert report.traceable_claims == 0
    assert report.traceability_rate == 0.0


def test_invalid_reference_is_detected_for_suspected_hypothesis() -> None:
    hypothesis = RootCauseHypothesis(
        description="A possible cause requires investigation.",
        supporting_evidence=["EV-FAKE"],
        confidence=0.40,
        status="suspected",
    )

    report = evaluate_traceability(
        evidence=[make_evidence()],
        business_impact=unknown_impact(),
        hypotheses=[hypothesis],
        recommendations=[],
        governance_controls=[],
    )

    assert report.total_claims == 0
    assert report.traceability_rate == 1.0
    assert report.invalid_evidence_ids == ["EV-FAKE"]


def test_validate_traceability_returns_report_when_valid() -> None:
    report = validate_traceability(
        evidence=[make_evidence()],
        business_impact=unknown_impact(),
        hypotheses=[probable_hypothesis(["EV-001"])],
        recommendations=[recommendation(["EV-001"])],
        governance_controls=[],
    )

    assert report.traceability_rate == 1.0
    assert report.invalid_evidence_ids == []
    assert report.missing_support == []


def test_potential_business_impact_requires_support() -> None:
    with pytest.raises(
        TraceabilityValidationError,
        match="business_impact",
    ):
        validate_traceability(
            evidence=[make_evidence()],
            business_impact=BusinessImpact(
                status="potential",
                description="Reporting may be incomplete.",
            ),
            hypotheses=[],
            recommendations=[],
            governance_controls=[],
        )


def test_probable_hypothesis_requires_support() -> None:
    with pytest.raises(
        TraceabilityValidationError,
        match=r"root_cause_hypothesis\[0\]",
    ):
        validate_traceability(
            evidence=[make_evidence()],
            business_impact=unknown_impact(),
            hypotheses=[probable_hypothesis([])],
            recommendations=[],
            governance_controls=[],
        )


def test_recommendation_requires_support_when_evidence_exists() -> None:
    with pytest.raises(
        TraceabilityValidationError,
        match=r"recommended_action\[0\]",
    ):
        validate_traceability(
            evidence=[make_evidence()],
            business_impact=unknown_impact(),
            hypotheses=[],
            recommendations=[recommendation([])],
            governance_controls=[],
        )


def test_investigation_recommendation_without_evidence_is_allowed() -> None:
    report = validate_traceability(
        evidence=[],
        business_impact=unknown_impact(),
        hypotheses=[],
        recommendations=[recommendation([])],
        governance_controls=[],
    )

    assert report.total_claims == 0
    assert report.traceability_rate == 1.0


def test_governance_control_requires_support() -> None:
    with pytest.raises(
        TraceabilityValidationError,
        match=r"governance_control\[0\]",
    ):
        validate_traceability(
            evidence=[make_evidence()],
            business_impact=unknown_impact(),
            hypotheses=[],
            recommendations=[],
            governance_controls=[governance_control([])],
        )


def test_validation_reports_missing_and_unknown_support_together() -> None:
    with pytest.raises(
        TraceabilityValidationError,
    ) as exc_info:
        validate_traceability(
            evidence=[make_evidence()],
            business_impact=BusinessImpact(
                status="potential",
                description="Reporting may be incomplete.",
            ),
            hypotheses=[probable_hypothesis(["EV-FAKE"])],
            recommendations=[],
            governance_controls=[],
        )

    message = str(exc_info.value)

    assert "missing supporting evidence for: business_impact" in message
    assert "unknown evidence_id values: EV-FAKE" in message
