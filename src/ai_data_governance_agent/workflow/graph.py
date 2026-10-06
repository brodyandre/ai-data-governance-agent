"""LangGraph orchestration for the single-agent workflow."""

from typing import Literal, cast

from langgraph.graph import END, START, StateGraph

from ai_data_governance_agent.domain.incident import IncidentInput
from ai_data_governance_agent.domain.response import AgentResponse
from ai_data_governance_agent.providers import ModelProvider
from ai_data_governance_agent.workflow.nodes import (
    analyze_business_impact_node,
    analyze_quality_node,
    build_final_response_node,
    collect_evidence_node,
    determine_human_review_node,
    make_generate_hypotheses_node,
    make_generate_recommendations_node,
    retrieve_policies_node,
    validate_incident_node,
)
from ai_data_governance_agent.workflow.state import (
    AgentState,
    WorkflowError,
    create_initial_state,
)

type WorkflowRoute = Literal["continue", "end"]


class WorkflowExecutionError(RuntimeError):
    """Raised when an orchestrated workflow finishes without a final response."""

    def __init__(self, errors: list[WorkflowError]) -> None:
        self.errors = [error.model_copy(deep=True) for error in errors]

        message = "workflow execution failed"

        if self.errors:
            details = "; ".join(
                (f"{error.step}: {error.error_type}: {error.message}") for error in self.errors
            )
            message = f"{message}: {details}"

        super().__init__(message)


def build_agent_graph(provider: ModelProvider):
    """Build and compile the single-agent LangGraph workflow."""
    builder = StateGraph(AgentState)

    builder.add_node(
        "validate_incident",
        validate_incident_node,
    )
    builder.add_node(
        "collect_evidence",
        collect_evidence_node,
    )
    builder.add_node(
        "analyze_quality",
        analyze_quality_node,
    )
    builder.add_node(
        "analyze_business_impact",
        analyze_business_impact_node,
    )
    builder.add_node(
        "retrieve_policies",
        retrieve_policies_node,
    )
    builder.add_node(
        "generate_hypotheses",
        make_generate_hypotheses_node(provider),
    )
    builder.add_node(
        "generate_recommendations",
        make_generate_recommendations_node(provider),
    )
    builder.add_node(
        "determine_human_review",
        determine_human_review_node,
    )
    builder.add_node(
        "build_final_response",
        build_final_response_node,
    )

    builder.add_edge(
        START,
        "validate_incident",
    )

    _add_guarded_edge(
        builder,
        "validate_incident",
        "collect_evidence",
    )
    _add_guarded_edge(
        builder,
        "collect_evidence",
        "analyze_quality",
    )
    _add_guarded_edge(
        builder,
        "analyze_quality",
        "analyze_business_impact",
    )
    _add_guarded_edge(
        builder,
        "analyze_business_impact",
        "retrieve_policies",
    )
    _add_guarded_edge(
        builder,
        "retrieve_policies",
        "generate_hypotheses",
    )
    _add_guarded_edge(
        builder,
        "generate_hypotheses",
        "generate_recommendations",
    )
    _add_guarded_edge(
        builder,
        "generate_recommendations",
        "determine_human_review",
    )
    _add_guarded_edge(
        builder,
        "determine_human_review",
        "build_final_response",
    )

    builder.add_edge(
        "build_final_response",
        END,
    )

    return builder.compile()


def run_agent_state(
    incident: IncidentInput,
    provider: ModelProvider,
) -> AgentState:
    """Execute the workflow and return its complete final state."""
    graph = build_agent_graph(provider)

    result = graph.invoke(create_initial_state(incident))

    return cast(AgentState, result)


def run_agent(
    incident: IncidentInput,
    provider: ModelProvider,
) -> AgentResponse:
    """Execute the workflow and return its validated final response."""
    state = run_agent_state(
        incident,
        provider,
    )

    response = state["final_response"]

    if response is None:
        raise WorkflowExecutionError(state["errors"])

    return response


def _route_after_node(
    state: AgentState,
) -> WorkflowRoute:
    """Stop graph execution immediately after an explicit node failure."""
    if state["current_step"] == "failed":
        return "end"

    return "continue"


def _add_guarded_edge(
    builder: StateGraph,
    source: str,
    target: str,
) -> None:
    """Connect nodes while terminating the workflow on explicit failure."""
    builder.add_conditional_edges(
        source,
        _route_after_node,
        {
            "continue": target,
            "end": END,
        },
    )


__all__ = [
    "WorkflowExecutionError",
    "build_agent_graph",
    "run_agent",
    "run_agent_state",
]
