"""Tests for the individually testable LangGraph workflow nodes."""

from datetime import UTC, datetime

import pytest

from ai_data_governance_agent.domain.enums import (
    IncidentClassification,
    Severity,
)
from ai_data_governance_agent.domain.human_review import HumanReviewDecision
from ai_data_governance_agent.domain.incident import IncidentInput
from ai_data_governance_agent.domain.response import (
    RecommendedAction,
)
from ai_data_governance_agent.providers import FakeProvider, ProviderError
from ai_data_governance_agent.tools.quality_analyzer import QualityFinding
from ai_data_governance_agent.workflow import (
    AgentState,
    HypothesisGenerationResult,
    RecommendationGenerationResult,
    ToolResults,
    analyze_business_impact_node,
    analyze_quality_node,
    build_final_response_node,
    collect_evidence_node,
    create_initial_state,
    determine_human_review_node,
    make_generate_hypotheses_node,
    make_generate_recommendations_node,
    retrieve_policies_node,
    validate_incident_node,
)


def make_incident() -> IncidentInput:
    """Create a representative incident for workflow node tests."""
    return IncidentInput.model_validate(
        {
            "incident_id": "INC-402",
            "title": "Orders quality incident",
            "description": "Invalid order records detected.",
            "source_system": "orders-lakehouse",
            "detected_at": datetime(
                2026,
                10,
                6,
                16,
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


def make_provider() -> FakeProvider:
    """Create deterministic provider responses for AI-backed nodes."""
    return FakeProvider(
        responses={
            HypothesisGenerationResult: {
                "classification": "data_quality",
                "severity": "medium",
                "executive_summary": ("Invalid order records require investigation."),
                "confidence": 0.82,
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
                        "requires_human_approval": False,
                        "supporting_evidence": ["EV-DQ-001"],
                    }
                ]
            },
        }
    )


def apply_update(
    state: AgentState,
    update: dict[str, object],
) -> None:
    """Apply one node update during direct unit tests."""
    state.update(update)


def prepare_deterministic_state() -> AgentState:
    """Execute deterministic tool nodes and return the resulting state."""
    state = create_initial_state(make_incident())

    for node in (
        validate_incident_node,
        collect_evidence_node,
        analyze_quality_node,
        analyze_business_impact_node,
        retrieve_policies_node,
    ):
        apply_update(state, node(state))

    return state


def prepare_analysis_state() -> AgentState:
    """Create state containing provider-backed analysis outputs."""
    state = prepare_deterministic_state()
    provider = make_provider()

    apply_update(
        state,
        make_generate_hypotheses_node(provider)(state),
    )
    apply_update(
        state,
        make_generate_recommendations_node(provider)(state),
    )

    return state


def test_validate_incident_node_succeeds() -> None:
    state = create_initial_state(make_incident())

    update = validate_incident_node(state)

    assert update["current_step"] == "validated"
    assert update["completed_steps"] == ["validated"]
    assert isinstance(update["incident"], IncidentInput)


def test_validate_incident_node_represents_malformed_state_as_error() -> None:
    state = create_initial_state(make_incident())
    state["incident"] = object()

    update = validate_incident_node(state)

    assert update["current_step"] == "failed"
    assert "completed_steps" not in update

    error = update["errors"][0]

    assert error.step == "validated"
    assert error.error_type == "AttributeError"
    assert error.recoverable is False


def test_collect_evidence_node_succeeds() -> None:
    state = create_initial_state(make_incident())

    update = collect_evidence_node(state)

    assert update["current_step"] == "evidence_collected"
    assert len(update["evidence"]) == 2
    assert update["evidence"][0].evidence_id == "EV-DQ-001"


def test_collect_evidence_node_represents_duplicate_ids_as_error() -> None:
    state = create_initial_state(make_incident())
    duplicate = state["incident"].evidence[0].model_copy(deep=True)

    state["incident"].evidence.append(duplicate)

    update = collect_evidence_node(state)

    assert update["current_step"] == "failed"

    error = update["errors"][0]

    assert error.step == "evidence_collected"
    assert error.error_type == "EvidenceCollectionError"


def test_analyze_quality_node_stores_findings() -> None:
    state = create_initial_state(make_incident())

    update = analyze_quality_node(state)

    results = update["tool_results"]

    assert update["current_step"] == "quality_analyzed"
    assert len(results.quality_findings) == 1
    assert results.quality_findings[0].finding_type == "invalid_records"


def test_analyze_quality_node_represents_tool_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    state = create_initial_state(make_incident())

    def fail_quality(
        evidence_items: object,
    ) -> list[QualityFinding]:
        del evidence_items
        raise RuntimeError("quality tool failure")

    monkeypatch.setattr(
        "ai_data_governance_agent.workflow.nodes.analyze_quality",
        fail_quality,
    )

    update = analyze_quality_node(state)

    assert update["current_step"] == "failed"
    assert update["errors"][0].step == "quality_analyzed"
    assert update["errors"][0].error_type == "RuntimeError"
    assert update["errors"][0].message == "quality tool failure"


def test_analyze_business_impact_node_stores_impact() -> None:
    state = create_initial_state(make_incident())

    update = analyze_business_impact_node(state)

    impact = update["tool_results"].business_impact

    assert update["current_step"] == "business_impact_analyzed"
    assert impact is not None
    assert impact.status == "potential"
    assert impact.supporting_evidence == ["EV-BIZ-001"]


def test_analyze_business_impact_node_represents_invalid_signal() -> None:
    incident = make_incident()
    incident.evidence[1].value = {"business_impact": "invalid"}
    state = create_initial_state(incident)

    update = analyze_business_impact_node(state)

    assert update["current_step"] == "failed"
    assert update["errors"][0].step == "business_impact_analyzed"
    assert update["errors"][0].error_type == "BusinessImpactAnalysisError"


def test_retrieve_policies_node_stores_matching_controls() -> None:
    state = create_initial_state(make_incident())

    apply_update(state, analyze_quality_node(state))

    update = retrieve_policies_node(state)

    controls = update["tool_results"].governance_controls

    assert update["current_step"] == "policies_retrieved"
    assert [item.control_id for item in controls] == ["DQ-001"]


def test_retrieve_policies_node_represents_traceability_failure() -> None:
    state = create_initial_state(make_incident())
    state["tool_results"] = ToolResults(
        quality_findings=[
            QualityFinding(
                finding_type="invalid_records",
                description="Invalid records detected.",
                supporting_evidence=["EV-UNKNOWN"],
                details={"invalid_rows": 1},
            )
        ]
    )

    update = retrieve_policies_node(state)

    assert update["current_step"] == "failed"
    assert update["errors"][0].step == "policies_retrieved"
    assert update["errors"][0].error_type == "PolicyRetrievalError"


def test_generate_hypotheses_node_stores_provider_output() -> None:
    state = prepare_deterministic_state()

    update = make_generate_hypotheses_node(make_provider())(state)

    assert update["current_step"] == "hypotheses_generated"
    assert update["classification"] is IncidentClassification.DATA_QUALITY
    assert update["severity"] is Severity.MEDIUM
    assert update["confidence"] == 0.82
    assert len(update["root_cause_hypotheses"]) == 1


def test_generate_hypotheses_node_represents_provider_failure() -> None:
    state = prepare_deterministic_state()
    provider = FakeProvider(error=ProviderError("simulated hypothesis failure"))

    update = make_generate_hypotheses_node(provider)(state)

    assert update["current_step"] == "failed"
    assert update["errors"][0].step == "hypotheses_generated"
    assert update["errors"][0].error_type == "ProviderError"
    assert update["errors"][0].message == "simulated hypothesis failure"


def test_generate_recommendations_node_stores_provider_output() -> None:
    state = prepare_analysis_state()
    provider = make_provider()

    update = make_generate_recommendations_node(provider)(state)

    assert update["current_step"] == "recommendations_generated"
    assert len(update["recommended_actions"]) == 1
    assert update["recommended_actions"][0].priority == "medium"


def test_generate_recommendations_node_represents_provider_failure() -> None:
    state = prepare_deterministic_state()
    provider = FakeProvider(error=ProviderError("simulated recommendation failure"))

    update = make_generate_recommendations_node(provider)(state)

    assert update["current_step"] == "failed"
    assert update["errors"][0].step == "recommendations_generated"
    assert update["errors"][0].error_type == "ProviderError"


def test_human_review_node_allows_safe_analysis() -> None:
    state = prepare_analysis_state()

    update = determine_human_review_node(state)

    decision = update["human_review_decision"]

    assert update["current_step"] == "human_review_evaluated"
    assert decision.human_review_required is False
    assert decision.human_review_reasons == []


def test_human_review_node_requires_review_for_low_confidence() -> None:
    state = prepare_analysis_state()
    state["confidence"] = 0.69

    update = determine_human_review_node(state)

    decision = update["human_review_decision"]

    assert decision.human_review_required is True
    assert "low confidence" in decision.human_review_reasons


def test_human_review_node_requires_review_when_action_needs_approval() -> None:
    state = prepare_analysis_state()
    action = state["recommended_actions"][0]

    state["recommended_actions"] = [
        action.model_copy(
            update={"requires_human_approval": True},
            deep=True,
        )
    ]

    update = determine_human_review_node(state)

    decision = update["human_review_decision"]

    assert decision.human_review_required is True
    assert "recommended action requires human approval" in decision.human_review_reasons
    assert "destructive action" not in decision.human_review_reasons


def test_human_review_node_requires_review_without_hypotheses() -> None:
    state = prepare_analysis_state()
    state["root_cause_hypotheses"] = []

    update = determine_human_review_node(state)

    decision = update["human_review_decision"]

    assert decision.human_review_required is True
    assert "high root-cause uncertainty" in decision.human_review_reasons


def test_human_review_node_represents_missing_required_state() -> None:
    state = prepare_analysis_state()
    state["severity"] = None

    update = determine_human_review_node(state)

    assert update["current_step"] == "failed"
    assert update["errors"][0].step == "human_review_evaluated"
    assert update["errors"][0].error_type == "WorkflowNodeStateError"


def test_build_final_response_node_creates_valid_response() -> None:
    state = prepare_analysis_state()

    review_update = determine_human_review_node(state)
    apply_update(state, review_update)

    update = build_final_response_node(state)

    response = update["final_response"]

    assert update["current_step"] == "response_built"
    assert response.incident_id == "INC-402"
    assert response.classification is IncidentClassification.DATA_QUALITY
    assert response.severity is Severity.MEDIUM
    assert response.confidence == 0.82
    assert len(response.root_cause_hypotheses) == 1
    assert len(response.recommended_actions) == 1
    assert response.human_review_required is False


def test_build_final_response_node_represents_missing_state() -> None:
    state = prepare_analysis_state()
    state["human_review_decision"] = None

    update = build_final_response_node(state)

    assert update["current_step"] == "failed"
    assert update["errors"][0].step == "response_built"
    assert update["errors"][0].error_type == "WorkflowNodeStateError"


def test_final_response_isolated_from_later_state_mutation() -> None:
    state = prepare_analysis_state()
    state["human_review_decision"] = HumanReviewDecision(
        human_review_required=False,
        human_review_reasons=[],
    )

    update = build_final_response_node(state)
    response = update["final_response"]

    state["recommended_actions"].append(
        RecommendedAction(
            description="Later mutation.",
            priority="low",
            rationale="Test state isolation.",
            requires_human_approval=False,
            supporting_evidence=["EV-DQ-001"],
        )
    )

    assert len(response.recommended_actions) == 1


def test_full_nine_node_sequence_builds_response() -> None:
    state = create_initial_state(make_incident())
    provider = make_provider()

    nodes = (
        validate_incident_node,
        collect_evidence_node,
        analyze_quality_node,
        analyze_business_impact_node,
        retrieve_policies_node,
        make_generate_hypotheses_node(provider),
        make_generate_recommendations_node(provider),
        determine_human_review_node,
        build_final_response_node,
    )

    for node in nodes:
        update = node(state)

        assert update["current_step"] != "failed"

        apply_update(state, update)

    assert state["current_step"] == "response_built"
    assert state["errors"] == []
    assert state["final_response"] is not None
    assert state["final_response"].incident_id == "INC-402"


def test_failure_update_does_not_mark_failed_step_completed() -> None:
    state = prepare_deterministic_state()
    provider = FakeProvider(error=ProviderError("simulated failure"))

    update = make_generate_hypotheses_node(provider)(state)

    assert update["current_step"] == "failed"
    assert "completed_steps" not in update
