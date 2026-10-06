"""Tests for the shared LangGraph workflow state contract."""

from datetime import UTC, datetime

import pytest
from langgraph.graph import END, START, StateGraph
from pydantic import ValidationError

from ai_data_governance_agent.domain.incident import IncidentInput
from ai_data_governance_agent.domain.response import (
    AgentResponse,
    BusinessImpact,
    GovernanceControl,
)
from ai_data_governance_agent.tools.quality_analyzer import QualityFinding
from ai_data_governance_agent.workflow import (
    AgentState,
    ToolResults,
    WorkflowError,
    create_initial_state,
)


def make_incident() -> IncidentInput:
    """Create a representative validated incident."""
    return IncidentInput.model_validate(
        {
            "incident_id": "INC-001",
            "title": "Orders quality incident",
            "description": "Invalid rows were detected.",
            "source_system": "orders-lakehouse",
            "detected_at": datetime(2026, 10, 6, 12, 0, tzinfo=UTC),
            "evidence": [
                {
                    "evidence_id": "EV-001",
                    "evidence_type": "data_quality_check",
                    "source": "quality-report",
                    "value": {
                        "invalid_rows": 30,
                    },
                    "metadata": {
                        "environment": "test",
                    },
                }
            ],
        }
    )


def test_initial_state_represents_all_required_workflow_sections() -> None:
    state = create_initial_state(make_incident())

    assert set(state) == {
        "incident",
        "evidence",
        "tool_results",
        "classification",
        "severity",
        "executive_summary",
        "confidence",
        "root_cause_hypotheses",
        "recommended_actions",
        "human_review_decision",
        "errors",
        "completed_steps",
        "current_step",
        "final_response",
    }


def test_initial_state_copies_incident_and_evidence() -> None:
    incident = make_incident()

    state = create_initial_state(incident)

    assert state["incident"] == incident
    assert state["incident"] is not incident
    assert state["evidence"] == incident.evidence
    assert state["evidence"][0] is not incident.evidence[0]


def test_source_incident_mutation_does_not_change_state() -> None:
    incident = make_incident()
    state = create_initial_state(incident)

    incident.evidence[0].metadata["environment"] = "changed"

    assert state["incident"].evidence[0].metadata == {"environment": "test"}
    assert state["evidence"][0].metadata == {"environment": "test"}


def test_state_incident_and_evidence_views_are_independent() -> None:
    state = create_initial_state(make_incident())

    state["evidence"][0].metadata["environment"] = "workflow"

    assert state["evidence"][0].metadata == {"environment": "workflow"}
    assert state["incident"].evidence[0].metadata == {"environment": "test"}


def test_separate_initial_states_do_not_share_mutable_data() -> None:
    incident = make_incident()

    first = create_initial_state(incident)
    second = create_initial_state(incident)

    first["completed_steps"].append("validated")
    first["evidence"][0].metadata["environment"] = "first"

    assert second["completed_steps"] == []
    assert second["evidence"][0].metadata == {"environment": "test"}


def test_workflow_error_is_structured() -> None:
    error = WorkflowError(
        step="quality_analyzed",
        error_type="QualityAnalysisError",
        message="Unable to analyze quality.",
        recoverable=True,
    )

    assert error.step == "quality_analyzed"
    assert error.error_type == "QualityAnalysisError"
    assert error.message == "Unable to analyze quality."
    assert error.recoverable is True


def test_workflow_error_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        WorkflowError.model_validate(
            {
                "step": "failed",
                "error_type": "UnexpectedError",
                "message": "Failure.",
                "recoverable": False,
                "unexpected": True,
            }
        )


def test_tool_results_start_empty() -> None:
    results = ToolResults()

    assert results.quality_findings == []
    assert results.business_impact is None
    assert results.governance_controls == []


def test_tool_results_store_deterministic_tool_outputs() -> None:
    finding = QualityFinding(
        finding_type="invalid_records",
        description="Evidence reports 30 invalid rows.",
        supporting_evidence=["EV-001"],
        details={"invalid_rows": 30},
    )
    impact = BusinessImpact(
        status="potential",
        description="Potential impact on order analytics.",
        affected_processes=["order reporting"],
        affected_consumers=["analytics team"],
        materiality="medium",
        supporting_evidence=["EV-001"],
    )
    control = GovernanceControl(
        control_id="DQ-001",
        title="Record quality validation",
        description="Validate invalid records.",
        source="docs/policies/LOCAL_CONTROLS.md#dq-001",
        relevance="invalid_records",
        supporting_evidence=["EV-001"],
    )

    results = ToolResults(
        quality_findings=[finding],
        business_impact=impact,
        governance_controls=[control],
    )

    assert results.quality_findings == [finding]
    assert results.business_impact == impact
    assert results.governance_controls == [control]


def test_agent_state_is_accepted_by_langgraph_stategraph() -> None:
    def validate_node(
        state: AgentState,
    ) -> dict[str, object]:
        assert state["incident"].incident_id == "INC-001"

        return {
            "current_step": "validated",
            "completed_steps": ["validated"],
        }

    builder = StateGraph(AgentState)
    builder.add_node("validate", validate_node)
    builder.add_edge(START, "validate")
    builder.add_edge("validate", END)

    graph = builder.compile()
    result = graph.invoke(create_initial_state(make_incident()))

    assert result["current_step"] == "validated"
    assert result["completed_steps"] == ["validated"]


def test_completed_steps_reducer_accumulates_graph_progress() -> None:
    def validate_node(
        state: AgentState,
    ) -> dict[str, object]:
        del state
        return {
            "current_step": "validated",
            "completed_steps": ["validated"],
        }

    def quality_node(
        state: AgentState,
    ) -> dict[str, object]:
        assert state["completed_steps"] == ["validated"]

        return {
            "current_step": "quality_analyzed",
            "completed_steps": ["quality_analyzed"],
        }

    builder = StateGraph(AgentState)
    builder.add_node("validate", validate_node)
    builder.add_node("quality", quality_node)
    builder.add_edge(START, "validate")
    builder.add_edge("validate", "quality")
    builder.add_edge("quality", END)

    graph = builder.compile()
    result = graph.invoke(create_initial_state(make_incident()))

    assert result["completed_steps"] == [
        "validated",
        "quality_analyzed",
    ]
    assert result["current_step"] == "quality_analyzed"


def test_errors_reducer_accumulates_structured_errors() -> None:
    first_error = WorkflowError(
        step="quality_analyzed",
        error_type="QualityAnalysisError",
        message="Quality analysis failed.",
        recoverable=True,
    )
    second_error = WorkflowError(
        step="policies_retrieved",
        error_type="PolicyRetrievalError",
        message="Policy retrieval failed.",
        recoverable=False,
    )

    def first_node(
        state: AgentState,
    ) -> dict[str, object]:
        del state
        return {"errors": [first_error]}

    def second_node(
        state: AgentState,
    ) -> dict[str, object]:
        assert state["errors"] == [first_error]
        return {"errors": [second_error]}

    builder = StateGraph(AgentState)
    builder.add_node("first", first_node)
    builder.add_node("second", second_node)
    builder.add_edge(START, "first")
    builder.add_edge("first", "second")
    builder.add_edge("second", END)

    graph = builder.compile()
    result = graph.invoke(create_initial_state(make_incident()))

    assert result["errors"] == [
        first_error,
        second_error,
    ]


def test_current_step_uses_latest_scalar_update() -> None:
    def first_node(
        state: AgentState,
    ) -> dict[str, object]:
        del state
        return {"current_step": "validated"}

    def second_node(
        state: AgentState,
    ) -> dict[str, object]:
        assert state["current_step"] == "validated"
        return {"current_step": "quality_analyzed"}

    builder = StateGraph(AgentState)
    builder.add_node("first", first_node)
    builder.add_node("second", second_node)
    builder.add_edge(START, "first")
    builder.add_edge("first", "second")
    builder.add_edge("second", END)

    graph = builder.compile()
    result = graph.invoke(create_initial_state(make_incident()))

    assert result["current_step"] == "quality_analyzed"


def test_final_response_can_be_stored_in_graph_state() -> None:
    incident = make_incident()

    response = AgentResponse(
        incident_id=incident.incident_id,
        classification="data_quality",
        severity="medium",
        executive_summary="Structured incident analysis completed.",
        evidence=incident.evidence,
        business_impact=BusinessImpact(
            status="potential",
            description="Potential impact on order analytics.",
            supporting_evidence=["EV-001"],
        ),
        confidence=0.80,
        human_review_required=False,
    )

    def response_node(
        state: AgentState,
    ) -> dict[str, object]:
        del state
        return {
            "final_response": response,
            "current_step": "response_built",
            "completed_steps": ["response_built"],
        }

    builder = StateGraph(AgentState)
    builder.add_node("response", response_node)
    builder.add_edge(START, "response")
    builder.add_edge("response", END)

    graph = builder.compile()
    result = graph.invoke(create_initial_state(incident))

    assert result["final_response"] == response
    assert result["current_step"] == "response_built"
    assert result["completed_steps"] == ["response_built"]
