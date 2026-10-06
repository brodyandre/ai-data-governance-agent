"""Tests for deterministic insufficient-evidence behavior."""

from ai_data_governance_agent.guardrails import (
    INSUFFICIENT_EVIDENCE_CONFIDENCE_CEILING,
    INSUFFICIENT_EVIDENCE_EXECUTIVE_SUMMARY,
    build_additional_investigation_recommendation,
    cap_insufficient_evidence_confidence,
)


def test_confidence_ceiling_is_conservative() -> None:
    assert INSUFFICIENT_EVIDENCE_CONFIDENCE_CEILING == 0.50


def test_high_confidence_is_capped_without_evidence() -> None:
    assert cap_insufficient_evidence_confidence(0.95) == 0.50


def test_confidence_at_ceiling_is_preserved() -> None:
    assert cap_insufficient_evidence_confidence(0.50) == 0.50


def test_lower_confidence_is_not_artificially_increased() -> None:
    assert cap_insufficient_evidence_confidence(0.30) == 0.30


def test_executive_summary_explicitly_reports_insufficient_evidence() -> None:
    assert INSUFFICIENT_EVIDENCE_EXECUTIVE_SUMMARY == (
        "Evidence is insufficient to establish a reliable root cause. "
        "Additional investigation is required."
    )


def test_additional_investigation_recommendation_is_safe() -> None:
    action = build_additional_investigation_recommendation()

    assert action.priority == "high"
    assert action.requires_human_approval is False
    assert action.supporting_evidence == []

    assert action.description == (
        "Collect and validate additional evidence before "
        "drawing root-cause conclusions or planning remediation."
    )

    assert action.rationale == (
        "The incident does not contain evidence sufficient "
        "to support a reliable analytical conclusion."
    )


def test_recommendation_builder_returns_independent_objects() -> None:
    first = build_additional_investigation_recommendation()
    second = build_additional_investigation_recommendation()

    first.description = "Changed."

    assert first is not second
    assert second.description == (
        "Collect and validate additional evidence before "
        "drawing root-cause conclusions or planning remediation."
    )
