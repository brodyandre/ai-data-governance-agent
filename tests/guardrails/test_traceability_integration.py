"""Integration tests for traceability validation in the workflow."""

from datetime import UTC, datetime

from ai_data_governance_agent.domain.incident import IncidentInput
from ai_data_governance_agent.guardrails import evaluate_traceability
from ai_data_governance_agent.providers import FakeProvider
from ai_data_governance_agent.workflow import (
    HypothesisGenerationResult,
    RecommendationGenerationResult,
    run_agent,
    run_agent_state,
)


def make_incident() -> IncidentInput:
    return IncidentInput.model_validate(
        {
            "incident_id": "INC-503",
            "title": "Traceability validation incident",
            "description": "Invalid records were detected.",
            "source_system": "orders-lakehouse",
            "detected_at": datetime(
                2026,
                10,
                6,
                22,
                0,
                tzinfo=UTC,
            ),
            "evidence": [
                {
                    "evidence_id": "EV-001",
                    "evidence_type": "data_quality_check",
                    "source": "quality-report",
                    "value": {
                        "invalid_rows": 30,
                    },
                }
            ],
        }
    )


def make_provider(
    *,
    hypothesis_status: str = "probable",
    hypothesis_evidence: list[str] | None = None,
    recommendation_evidence: list[str] | None = None,
) -> FakeProvider:
    if hypothesis_evidence is None:
        hypothesis_evidence = ["EV-001"]

    if recommendation_evidence is None:
        recommendation_evidence = ["EV-001"]

    return FakeProvider(
        responses={
            HypothesisGenerationResult: {
                "classification": "data_quality",
                "severity": "medium",
                "executive_summary": ("Invalid records require investigation."),
                "confidence": 0.85,
                "root_cause_hypotheses": [
                    {
                        "description": ("Validation may have rejected invalid records."),
                        "supporting_evidence": (hypothesis_evidence),
                        "confidence": 0.80,
                        "status": hypothesis_status,
                    }
                ],
            },
            RecommendationGenerationResult: {
                "recommended_actions": [
                    {
                        "description": ("Review invalid records."),
                        "priority": "medium",
                        "rationale": ("The quality check identified invalid rows."),
                        "requires_human_approval": False,
                        "supporting_evidence": (recommendation_evidence),
                    }
                ]
            },
        }
    )


def test_valid_workflow_response_is_fully_traceable() -> None:
    response = run_agent(
        make_incident(),
        make_provider(),
    )

    report = evaluate_traceability(
        evidence=response.evidence,
        business_impact=response.business_impact,
        hypotheses=response.root_cause_hypotheses,
        recommendations=response.recommended_actions,
        governance_controls=response.governance_controls,
    )

    assert report.invalid_evidence_ids == []
    assert report.missing_support == []
    assert report.total_claims == 3
    assert report.traceable_claims == 3
    assert report.traceability_rate == 1.0


def test_unknown_hypothesis_evidence_blocks_final_response() -> None:
    state = run_agent_state(
        make_incident(),
        make_provider(
            hypothesis_evidence=["EV-FAKE"],
        ),
    )

    assert state["current_step"] == "failed"
    assert state["final_response"] is None
    assert len(state["errors"]) == 1

    error = state["errors"][0]

    assert error.step == "response_built"
    assert error.error_type == "TraceabilityValidationError"
    assert error.message == "unknown evidence_id values: EV-FAKE"


def test_unknown_recommendation_evidence_blocks_final_response() -> None:
    state = run_agent_state(
        make_incident(),
        make_provider(
            recommendation_evidence=["EV-FAKE"],
        ),
    )

    assert state["current_step"] == "failed"
    assert state["final_response"] is None

    error = state["errors"][0]

    assert error.step == "response_built"
    assert error.error_type == "TraceabilityValidationError"
    assert "EV-FAKE" in error.message


def test_recommendation_without_support_is_blocked_when_evidence_exists() -> None:
    state = run_agent_state(
        make_incident(),
        make_provider(
            recommendation_evidence=[],
        ),
    )

    assert state["current_step"] == "failed"
    assert state["final_response"] is None

    error = state["errors"][0]

    assert error.step == "response_built"
    assert error.error_type == "TraceabilityValidationError"

    assert "recommended_action[0]" in error.message


def test_unsupported_probable_hypothesis_is_qualified_before_traceability() -> None:
    response = run_agent(
        make_incident(),
        make_provider(
            hypothesis_evidence=[],
        ),
    )

    hypothesis = response.root_cause_hypotheses[0]

    assert hypothesis.status == "suspected"
    assert hypothesis.supporting_evidence == []

    report = evaluate_traceability(
        evidence=response.evidence,
        business_impact=response.business_impact,
        hypotheses=response.root_cause_hypotheses,
        recommendations=response.recommended_actions,
        governance_controls=response.governance_controls,
    )

    assert report.invalid_evidence_ids == []
    assert report.missing_support == []
    assert report.traceability_rate == 1.0
