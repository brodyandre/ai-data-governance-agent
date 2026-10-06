"""Integration tests for the orchestrated LangGraph agent workflow."""

from datetime import UTC, datetime

import pytest

from ai_data_governance_agent.domain.incident import IncidentInput
from ai_data_governance_agent.domain.response import AgentResponse
from ai_data_governance_agent.providers import (
    FakeProvider,
    ProviderError,
)
from ai_data_governance_agent.workflow import (
    HypothesisGenerationResult,
    RecommendationGenerationResult,
    WorkflowExecutionError,
    build_agent_graph,
    run_agent,
    run_agent_state,
)

EXPECTED_STEPS = [
    "validated",
    "evidence_collected",
    "quality_analyzed",
    "business_impact_analyzed",
    "policies_retrieved",
    "hypotheses_generated",
    "recommendations_generated",
    "human_review_evaluated",
    "response_built",
]


def make_incident() -> IncidentInput:
    """Create a representative incident for graph integration tests."""
    return IncidentInput.model_validate(
        {
            "incident_id": "INC-403",
            "title": "Orders quality incident",
            "description": "Invalid order records detected.",
            "source_system": "orders-lakehouse",
            "detected_at": datetime(
                2026,
                10,
                6,
                20,
                0,
                tzinfo=UTC,
            ),
            "evidence": [
                {
                    "evidence_id": "EV-DQ-001",
                    "evidence_type": "data_quality_check",
                    "source": "quality-report",
                    "value": {
                        "invalid_rows": 30,
                    },
                },
                {
                    "evidence_id": "EV-BIZ-001",
                    "evidence_type": "analyst_observation",
                    "source": "analyst",
                    "value": {
                        "business_impact": {
                            "status": "potential",
                            "description": ("Order reporting may be incomplete."),
                            "affected_processes": ["order reporting"],
                            "affected_consumers": ["analytics team"],
                            "materiality": "medium",
                        }
                    },
                },
            ],
        }
    )


def make_provider(
    *,
    confidence: float = 0.82,
    requires_human_approval: bool = False,
) -> FakeProvider:
    """Create deterministic provider outputs for graph tests."""
    return FakeProvider(
        responses={
            HypothesisGenerationResult: {
                "classification": "data_quality",
                "severity": "medium",
                "executive_summary": ("Invalid order records require investigation."),
                "confidence": confidence,
                "root_cause_hypotheses": [
                    {
                        "description": (
                            "A validation failure may have allowed invalid order records."
                        ),
                        "supporting_evidence": ["EV-DQ-001"],
                        "confidence": 0.80,
                        "status": "probable",
                    }
                ],
            },
            RecommendationGenerationResult: {
                "recommended_actions": [
                    {
                        "description": ("Investigate invalid order records before remediation."),
                        "priority": "medium",
                        "rationale": ("The quality check identified invalid rows."),
                        "requires_human_approval": (requires_human_approval),
                        "supporting_evidence": ["EV-DQ-001"],
                    }
                ]
            },
        }
    )


def test_build_agent_graph_compiles() -> None:
    graph = build_agent_graph(make_provider())

    assert callable(graph.invoke)


def test_run_agent_state_executes_expected_sequence() -> None:
    state = run_agent_state(
        make_incident(),
        make_provider(),
    )

    assert state["current_step"] == "response_built"
    assert state["completed_steps"] == EXPECTED_STEPS
    assert state["errors"] == []
    assert state["final_response"] is not None


def test_run_agent_returns_valid_agent_response() -> None:
    response = run_agent(
        make_incident(),
        make_provider(),
    )

    assert isinstance(response, AgentResponse)
    assert response.incident_id == "INC-403"
    assert response.classification == "data_quality"
    assert response.severity == "medium"
    assert response.confidence == 0.82
    assert len(response.root_cause_hypotheses) == 1
    assert len(response.recommended_actions) == 1
    assert [control.control_id for control in response.governance_controls] == ["DQ-001"]


def test_repeated_runs_are_deterministic() -> None:
    incident = make_incident()
    provider = make_provider()

    first = run_agent_state(
        incident,
        provider,
    )
    second = run_agent_state(
        incident,
        provider,
    )

    assert first["completed_steps"] == second["completed_steps"]
    assert first["errors"] == second["errors"]

    assert first["final_response"] is not None
    assert second["final_response"] is not None

    assert first["final_response"].model_dump(mode="json") == second["final_response"].model_dump(
        mode="json"
    )


def test_workflow_does_not_mutate_input_incident() -> None:
    incident = make_incident()
    original = incident.model_copy(deep=True)

    run_agent(
        incident,
        make_provider(),
    )

    assert incident == original
    assert incident.evidence == original.evidence


def test_provider_failure_stops_graph_before_later_nodes() -> None:
    provider = FakeProvider(error=ProviderError("simulated provider failure"))

    state = run_agent_state(
        make_incident(),
        provider,
    )

    assert state["current_step"] == "failed"

    assert state["completed_steps"] == [
        "validated",
        "evidence_collected",
        "quality_analyzed",
        "business_impact_analyzed",
        "policies_retrieved",
    ]

    assert len(state["errors"]) == 1

    error = state["errors"][0]

    assert error.step == "hypotheses_generated"
    assert error.error_type == "ProviderError"
    assert error.message == "simulated provider failure"

    assert state["recommended_actions"] == []
    assert state["human_review_decision"] is None
    assert state["final_response"] is None


def test_run_agent_raises_workflow_execution_error_on_failure() -> None:
    provider = FakeProvider(error=ProviderError("simulated provider failure"))

    with pytest.raises(
        WorkflowExecutionError,
        match="workflow execution failed",
    ) as exc_info:
        run_agent(
            make_incident(),
            provider,
        )

    assert len(exc_info.value.errors) == 1
    assert exc_info.value.errors[0].step == "hypotheses_generated"


def test_workflow_execution_error_contains_structured_details() -> None:
    provider = FakeProvider(error=ProviderError("provider unavailable"))

    with pytest.raises(
        WorkflowExecutionError,
    ) as exc_info:
        run_agent(
            make_incident(),
            provider,
        )

    error = exc_info.value.errors[0]

    assert error.step == "hypotheses_generated"
    assert error.error_type == "ProviderError"
    assert error.message == "provider unavailable"
    assert error.recoverable is False

    assert "hypotheses_generated: ProviderError: provider unavailable" in str(exc_info.value)


def test_low_confidence_activates_human_review_end_to_end() -> None:
    response = run_agent(
        make_incident(),
        make_provider(confidence=0.69),
    )

    assert response.human_review_required is True
    assert "low confidence" in response.human_review_reasons


def test_action_requiring_approval_activates_human_review_end_to_end() -> None:
    response = run_agent(
        make_incident(),
        make_provider(requires_human_approval=True),
    )

    assert response.human_review_required is True

    assert "recommended action requires human approval" in response.human_review_reasons

    assert "destructive action" not in response.human_review_reasons
