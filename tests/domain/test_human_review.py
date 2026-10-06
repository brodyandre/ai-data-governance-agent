"""Tests for deterministic human-review rules."""

import pytest
from pydantic import ValidationError

from ai_data_governance_agent.domain import (
    HUMAN_REVIEW_CONFIDENCE_THRESHOLD,
    HumanReviewSignals,
    Severity,
    evaluate_human_review,
)


def make_signals(**overrides: object) -> HumanReviewSignals:
    """Create a low-risk baseline with optional signal overrides."""
    data: dict[str, object] = {
        "severity": Severity.LOW,
        "confidence": 0.95,
        "material_business_impact": False,
        "insufficient_evidence": False,
        "conflicting_evidence": False,
        "regulatory_exposure": False,
        "governance_exposure": False,
        "privacy_impact": False,
        "destructive_action": False,
        "irreversible_action": False,
        "high_root_cause_uncertainty": False,
        "unsafe_recommendation": False,
        "critical_process_affected": False,
    }
    data.update(overrides)
    return HumanReviewSignals(**data)


def test_confidence_threshold_is_point_seven() -> None:
    assert HUMAN_REVIEW_CONFIDENCE_THRESHOLD == 0.70


def test_safe_low_risk_scenario_does_not_require_review() -> None:
    decision = evaluate_human_review(make_signals())

    assert decision.human_review_required is False
    assert decision.human_review_reasons == []


def test_critical_severity_always_requires_review() -> None:
    decision = evaluate_human_review(
        make_signals(
            severity=Severity.CRITICAL,
            confidence=0.99,
        )
    )

    assert decision.human_review_required is True
    assert decision.human_review_reasons == ["critical severity"]


def test_high_severity_with_material_business_impact_requires_review() -> None:
    decision = evaluate_human_review(
        make_signals(
            severity=Severity.HIGH,
            material_business_impact=True,
        )
    )

    assert decision.human_review_required is True
    assert decision.human_review_reasons == ["high severity with material business impact"]


def test_high_severity_without_material_impact_does_not_trigger_that_rule() -> None:
    decision = evaluate_human_review(
        make_signals(
            severity=Severity.HIGH,
            material_business_impact=False,
        )
    )

    assert decision.human_review_required is False
    assert decision.human_review_reasons == []


def test_material_impact_without_high_severity_does_not_trigger_that_rule() -> None:
    decision = evaluate_human_review(
        make_signals(
            severity=Severity.MEDIUM,
            material_business_impact=True,
        )
    )

    assert decision.human_review_required is False
    assert decision.human_review_reasons == []


@pytest.mark.parametrize(
    ("confidence", "expected_required"),
    [
        (0.0, True),
        (0.699, True),
        (0.70, False),
        (0.71, False),
        (1.0, False),
    ],
)
def test_confidence_threshold_is_applied_exactly(
    confidence: float,
    expected_required: bool,
) -> None:
    decision = evaluate_human_review(make_signals(confidence=confidence))

    assert decision.human_review_required is expected_required

    if expected_required:
        assert decision.human_review_reasons == ["low confidence"]
    else:
        assert decision.human_review_reasons == []


@pytest.mark.parametrize(
    ("field_name", "expected_reason"),
    [
        ("insufficient_evidence", "insufficient evidence"),
        ("conflicting_evidence", "conflicting evidence"),
        ("regulatory_exposure", "regulatory exposure"),
        ("governance_exposure", "governance exposure"),
        ("privacy_impact", "privacy impact"),
        ("destructive_action", "destructive action"),
        ("irreversible_action", "irreversible action"),
        (
            "high_root_cause_uncertainty",
            "high root-cause uncertainty",
        ),
        (
            "unsafe_recommendation",
            "safe recommendation cannot be determined",
        ),
        (
            "critical_process_affected",
            "critical business process affected",
        ),
    ],
)
def test_individual_risk_signal_requires_review(
    field_name: str,
    expected_reason: str,
) -> None:
    decision = evaluate_human_review(make_signals(**{field_name: True}))

    assert decision.human_review_required is True
    assert decision.human_review_reasons == [expected_reason]


def test_multiple_rules_return_all_reasons_in_deterministic_order() -> None:
    decision = evaluate_human_review(
        make_signals(
            severity=Severity.CRITICAL,
            confidence=0.50,
            material_business_impact=True,
            insufficient_evidence=True,
            conflicting_evidence=True,
            regulatory_exposure=True,
            governance_exposure=True,
            privacy_impact=True,
            destructive_action=True,
            irreversible_action=True,
            high_root_cause_uncertainty=True,
            unsafe_recommendation=True,
            critical_process_affected=True,
        )
    )

    assert decision.human_review_required is True
    assert decision.human_review_reasons == [
        "critical severity",
        "low confidence",
        "insufficient evidence",
        "conflicting evidence",
        "regulatory exposure",
        "governance exposure",
        "privacy impact",
        "destructive action",
        "irreversible action",
        "high root-cause uncertainty",
        "safe recommendation cannot be determined",
        "critical business process affected",
    ]


@pytest.mark.parametrize("confidence", [-0.01, 1.01, -1.0, 2.0])
def test_signals_reject_out_of_range_confidence(confidence: float) -> None:
    with pytest.raises(ValidationError):
        make_signals(confidence=confidence)


@pytest.mark.parametrize(
    "severity",
    [
        "CRITICAL",
        "Critical",
        "urgent",
        "unknown",
    ],
)
def test_signals_reject_invalid_severity(severity: str) -> None:
    with pytest.raises(ValidationError):
        make_signals(severity=severity)


@pytest.mark.parametrize(
    "value",
    [
        1,
        0,
        "true",
        "false",
        "yes",
        "no",
    ],
)
def test_risk_signals_require_strict_boolean_values(value: object) -> None:
    with pytest.raises(ValidationError):
        make_signals(governance_exposure=value)


def test_signals_reject_extra_fields() -> None:
    data = make_signals().model_dump()
    data["unexpected"] = True

    with pytest.raises(ValidationError):
        HumanReviewSignals(**data)


def test_decision_serialization_is_predictable() -> None:
    decision = evaluate_human_review(
        make_signals(
            regulatory_exposure=True,
            privacy_impact=True,
        )
    )

    assert decision.model_dump() == {
        "human_review_required": True,
        "human_review_reasons": [
            "regulatory exposure",
            "privacy impact",
        ],
    }


def test_same_input_produces_same_decision() -> None:
    signals = make_signals(
        severity=Severity.HIGH,
        material_business_impact=True,
        conflicting_evidence=True,
    )

    first = evaluate_human_review(signals)
    second = evaluate_human_review(signals)

    assert first == second
