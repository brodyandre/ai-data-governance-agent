"""Structured agent response domain models."""

from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ai_data_governance_agent.domain.enums import (
    ActionPriority,
    BusinessImpactStatus,
    HypothesisStatus,
    IncidentClassification,
    Severity,
)
from ai_data_governance_agent.domain.evidence import Evidence


class BusinessImpact(BaseModel):
    """Represent confirmed, potential, or unknown business impact."""

    model_config = ConfigDict(extra="forbid")

    status: BusinessImpactStatus
    description: str
    affected_processes: list[str] = Field(default_factory=list)
    affected_consumers: list[str] = Field(default_factory=list)
    materiality: str | None = None
    supporting_evidence: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_confirmed_impact_has_evidence(self) -> Self:
        """Require supporting evidence for a confirmed business impact."""
        if self.status is BusinessImpactStatus.CONFIRMED and not self.supporting_evidence:
            raise ValueError("confirmed business impact requires supporting evidence")

        return self


class RootCauseHypothesis(BaseModel):
    """Represent a possible explanation for an incident."""

    model_config = ConfigDict(extra="forbid")

    description: str
    supporting_evidence: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    status: HypothesisStatus

    @model_validator(mode="after")
    def validate_confirmed_hypothesis_has_evidence(self) -> Self:
        """Require evidence before a hypothesis can be structurally confirmed."""
        if self.status is HypothesisStatus.CONFIRMED and not self.supporting_evidence:
            raise ValueError("confirmed root-cause hypothesis requires supporting evidence")

        return self


class RecommendedAction(BaseModel):
    """Represent a consultative action recommended by the agent."""

    model_config = ConfigDict(extra="forbid")

    description: str
    priority: ActionPriority
    rationale: str
    requires_human_approval: bool
    supporting_evidence: list[str] = Field(default_factory=list)


class GovernanceControl(BaseModel):
    """Represent a governance rule, policy, or control relevant to an incident."""

    model_config = ConfigDict(extra="forbid")

    control_id: str
    title: str
    description: str
    source: str
    relevance: str
    supporting_evidence: list[str] = Field(default_factory=list)


class AgentResponse(BaseModel):
    """Represent the structured final response for an analyzed incident."""

    model_config = ConfigDict(extra="forbid")

    incident_id: str
    classification: IncidentClassification
    severity: Severity
    executive_summary: str
    evidence: list[Evidence]
    business_impact: BusinessImpact
    root_cause_hypotheses: list[RootCauseHypothesis] = Field(default_factory=list)
    recommended_actions: list[RecommendedAction] = Field(default_factory=list)
    governance_controls: list[GovernanceControl] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    human_review_required: bool
    human_review_reasons: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_human_review_reasons(self) -> Self:
        """Require auditable reasons whenever human review is mandatory."""
        if self.human_review_required and not self.human_review_reasons:
            raise ValueError("human_review_reasons are required when human_review_required is true")

        return self


__all__ = [
    "AgentResponse",
    "BusinessImpact",
    "GovernanceControl",
    "RecommendedAction",
    "RootCauseHypothesis",
]
