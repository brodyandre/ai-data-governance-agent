"""Shared state contract used by the LangGraph workflow."""

from operator import add
from typing import Annotated, Literal, TypedDict

from pydantic import BaseModel, ConfigDict, Field

from ai_data_governance_agent.domain.evidence import Evidence
from ai_data_governance_agent.domain.incident import IncidentInput
from ai_data_governance_agent.domain.response import (
    AgentResponse,
    BusinessImpact,
    GovernanceControl,
)
from ai_data_governance_agent.tools.quality_analyzer import QualityFinding

type WorkflowStep = Literal[
    "received",
    "validated",
    "evidence_collected",
    "quality_analyzed",
    "business_impact_analyzed",
    "policies_retrieved",
    "hypotheses_generated",
    "recommendations_generated",
    "human_review_evaluated",
    "response_built",
    "failed",
]


class WorkflowError(BaseModel):
    """Represent one explicit error recorded during graph execution."""

    model_config = ConfigDict(extra="forbid")

    step: WorkflowStep
    error_type: str
    message: str
    recoverable: bool


class ToolResults(BaseModel):
    """Store deterministic tool outputs produced during analysis."""

    model_config = ConfigDict(extra="forbid")

    quality_findings: list[QualityFinding] = Field(default_factory=list)
    business_impact: BusinessImpact | None = None
    governance_controls: list[GovernanceControl] = Field(default_factory=list)


class AgentState(TypedDict):
    """Represent the complete shared state of the agent workflow."""

    incident: IncidentInput
    evidence: list[Evidence]
    tool_results: ToolResults
    errors: Annotated[list[WorkflowError], add]
    completed_steps: Annotated[list[WorkflowStep], add]
    current_step: WorkflowStep
    final_response: AgentResponse | None


def create_initial_state(incident: IncidentInput) -> AgentState:
    """Create an isolated initial workflow state from a validated incident."""
    return AgentState(
        incident=incident.model_copy(deep=True),
        evidence=[evidence.model_copy(deep=True) for evidence in incident.evidence],
        tool_results=ToolResults(),
        errors=[],
        completed_steps=[],
        current_step="received",
        final_response=None,
    )


__all__ = [
    "AgentState",
    "ToolResults",
    "WorkflowError",
    "WorkflowStep",
    "create_initial_state",
]
