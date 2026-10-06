"""Integration tests for unsupported claims in the workflow."""

from datetime import UTC, datetime

from ai_data_governance_agent.domain.incident import IncidentInput
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
            "incident_id": "INC-501",
            "title": "Unsupported hypothesis test",
            "description": "Validate unsupported analytical claims.",
            "source_system": "orders-lakehouse",
            "detected_at": datetime(
                2026,
                10,
                6,
                20,
                30,
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
    status: str,
    supporting_evidence: list[str],
) -> FakeProvider:
    return FakeProvider(
        responses={
            HypothesisGenerationResult: {
                "classification": "data_quality",
                "severity": "medium",
                "executive_summary": ("The incident requires investigation."),
                "confidence": 0.90,
                "root_cause_hypotheses": [
                    {
                        "description": (
                            "An upstream transformation may have caused the invalid records."
                        ),
                        "supporting_evidence": supporting_evidence,
                        "confidence": 0.90,
                        "status": status,
                    }
                ],
            },
            RecommendationGenerationResult: {
                "recommended_actions": [
                    {
                        "description": ("Investigate the invalid records."),
                        "priority": "medium",
                        "rationale": ("The quality check identified invalid rows."),
                        "requires_human_approval": False,
                        "supporting_evidence": ["EV-001"],
                    }
                ]
            },
        }
    )


def test_final_response_qualifies_unsupported_probable_claim() -> None:
    response = run_agent(
        make_incident(),
        make_provider(
            status="probable",
            supporting_evidence=[],
        ),
    )

    hypothesis = response.root_cause_hypotheses[0]

    assert hypothesis.status == "suspected"
    assert hypothesis.supporting_evidence == []


def test_final_response_qualifies_unsupported_rejected_claim() -> None:
    response = run_agent(
        make_incident(),
        make_provider(
            status="rejected",
            supporting_evidence=[],
        ),
    )

    hypothesis = response.root_cause_hypotheses[0]

    assert hypothesis.status == "suspected"


def test_supported_probable_claim_remains_probable() -> None:
    response = run_agent(
        make_incident(),
        make_provider(
            status="probable",
            supporting_evidence=["EV-001"],
        ),
    )

    hypothesis = response.root_cause_hypotheses[0]

    assert hypothesis.status == "probable"
    assert hypothesis.supporting_evidence == ["EV-001"]


def test_supported_confirmed_claim_remains_confirmed() -> None:
    response = run_agent(
        make_incident(),
        make_provider(
            status="confirmed",
            supporting_evidence=["EV-001"],
        ),
    )

    hypothesis = response.root_cause_hypotheses[0]

    assert hypothesis.status == "confirmed"


def test_confirmed_without_evidence_fails_before_final_response() -> None:
    state = run_agent_state(
        make_incident(),
        make_provider(
            status="confirmed",
            supporting_evidence=[],
        ),
    )

    assert state["current_step"] == "failed"
    assert state["final_response"] is None
    assert len(state["errors"]) == 1

    error = state["errors"][0]

    assert error.step == "hypotheses_generated"
    assert error.error_type == "ValidationError"
    assert "confirmed root-cause hypothesis requires supporting evidence" in error.message
