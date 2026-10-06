"""Individually testable nodes used by the LangGraph workflow."""

import json
from collections.abc import Callable

from pydantic import BaseModel, ConfigDict, Field

from ai_data_governance_agent.domain.enums import (
    IncidentClassification,
    Severity,
)
from ai_data_governance_agent.domain.human_review import (
    HumanReviewDecision,
    HumanReviewSignals,
    evaluate_human_review,
)
from ai_data_governance_agent.domain.incident import IncidentInput
from ai_data_governance_agent.domain.response import (
    AgentResponse,
    BusinessImpact,
    RecommendedAction,
    RootCauseHypothesis,
)
from ai_data_governance_agent.guardrails import qualify_unsupported_hypotheses
from ai_data_governance_agent.providers import ModelProvider
from ai_data_governance_agent.tools.business_impact_analyzer import (
    analyze_business_impact,
)
from ai_data_governance_agent.tools.evidence_collector import collect_evidence
from ai_data_governance_agent.tools.policy_retriever import retrieve_policies
from ai_data_governance_agent.tools.quality_analyzer import analyze_quality
from ai_data_governance_agent.workflow.state import (
    AgentState,
    WorkflowError,
    WorkflowStep,
)


class WorkflowNodeStateError(ValueError):
    """Raised when a node requires workflow state that is not available."""


class HypothesisGenerationResult(BaseModel):
    """Represent provider output produced by the hypothesis node."""

    model_config = ConfigDict(extra="forbid")

    classification: IncidentClassification
    severity: Severity
    executive_summary: str
    confidence: float = Field(ge=0.0, le=1.0)
    root_cause_hypotheses: list[RootCauseHypothesis] = Field(default_factory=list)


class RecommendationGenerationResult(BaseModel):
    """Represent provider output produced by the recommendation node."""

    model_config = ConfigDict(extra="forbid")

    recommended_actions: list[RecommendedAction] = Field(default_factory=list)


def validate_incident_node(
    state: AgentState,
) -> dict[str, object]:
    """Revalidate the incident contract at the workflow boundary."""
    try:
        incident = IncidentInput.model_validate(state["incident"].model_dump(mode="python"))
    except Exception as exc:
        return _failure_update("validated", exc)

    return _success_update(
        "validated",
        incident=incident,
    )


def collect_evidence_node(
    state: AgentState,
) -> dict[str, object]:
    """Collect and normalize incident evidence."""
    try:
        evidence = collect_evidence(state["incident"].evidence)
    except Exception as exc:
        return _failure_update(
            "evidence_collected",
            exc,
        )

    return _success_update(
        "evidence_collected",
        evidence=evidence,
    )


def analyze_quality_node(
    state: AgentState,
) -> dict[str, object]:
    """Run deterministic data-quality analysis."""
    try:
        findings = analyze_quality(state["evidence"])
    except Exception as exc:
        return _failure_update(
            "quality_analyzed",
            exc,
        )

    tool_results = state["tool_results"].model_copy(
        update={
            "quality_findings": findings,
        },
        deep=True,
    )

    return _success_update(
        "quality_analyzed",
        tool_results=tool_results,
    )


def analyze_business_impact_node(
    state: AgentState,
) -> dict[str, object]:
    """Run deterministic business-impact analysis."""
    try:
        business_impact = analyze_business_impact(state["evidence"])
    except Exception as exc:
        return _failure_update(
            "business_impact_analyzed",
            exc,
        )

    tool_results = state["tool_results"].model_copy(
        update={
            "business_impact": business_impact,
        },
        deep=True,
    )

    return _success_update(
        "business_impact_analyzed",
        tool_results=tool_results,
    )


def retrieve_policies_node(
    state: AgentState,
) -> dict[str, object]:
    """Retrieve applicable deterministic governance controls."""
    try:
        controls = retrieve_policies(
            state["evidence"],
            state["tool_results"].quality_findings,
        )
    except Exception as exc:
        return _failure_update(
            "policies_retrieved",
            exc,
        )

    tool_results = state["tool_results"].model_copy(
        update={
            "governance_controls": controls,
        },
        deep=True,
    )

    return _success_update(
        "policies_retrieved",
        tool_results=tool_results,
    )


def make_generate_hypotheses_node(
    provider: ModelProvider,
) -> Callable[[AgentState], dict[str, object]]:
    """Create the provider-backed root-cause hypothesis node."""

    def generate_hypotheses_node(
        state: AgentState,
    ) -> dict[str, object]:
        try:
            result = provider.generate_structured(
                system_prompt=(
                    "Analyze the data incident conservatively. "
                    "Distinguish observed evidence from hypotheses. "
                    "Do not present unsupported claims as facts. "
                    "Return only the requested structured response."
                ),
                user_prompt=_build_hypothesis_context(state),
                response_model=HypothesisGenerationResult,
            )
        except Exception as exc:
            return _failure_update(
                "hypotheses_generated",
                exc,
            )

        hypotheses = qualify_unsupported_hypotheses(result.root_cause_hypotheses)

        return _success_update(
            "hypotheses_generated",
            classification=result.classification,
            severity=result.severity,
            executive_summary=result.executive_summary,
            confidence=result.confidence,
            root_cause_hypotheses=hypotheses,
        )

    return generate_hypotheses_node


def make_generate_recommendations_node(
    provider: ModelProvider,
) -> Callable[[AgentState], dict[str, object]]:
    """Create the provider-backed recommendation node."""

    def generate_recommendations_node(
        state: AgentState,
    ) -> dict[str, object]:
        try:
            result = provider.generate_structured(
                system_prompt=(
                    "Generate safe, consultative recommendations for "
                    "the data incident. Do not execute remediation. "
                    "Recommendations must remain traceable to available "
                    "evidence and explicitly require approval when needed. "
                    "Return only the requested structured response."
                ),
                user_prompt=_build_recommendation_context(state),
                response_model=RecommendationGenerationResult,
            )
        except Exception as exc:
            return _failure_update(
                "recommendations_generated",
                exc,
            )

        return _success_update(
            "recommendations_generated",
            recommended_actions=result.recommended_actions,
        )

    return generate_recommendations_node


def determine_human_review_node(
    state: AgentState,
) -> dict[str, object]:
    """Apply deterministic human-review rules to explicit state signals."""
    try:
        severity = _require_value(
            state["severity"],
            "severity",
        )
        confidence = _require_value(
            state["confidence"],
            "confidence",
        )

        hypotheses = state["root_cause_hypotheses"]
        recommendations = state["recommended_actions"]

        recommendation_requires_approval = any(
            action.requires_human_approval for action in recommendations
        )

        signals = HumanReviewSignals(
            severity=severity,
            confidence=confidence,
            material_business_impact=_has_material_business_impact(
                state["tool_results"].business_impact
            ),
            insufficient_evidence=not state["evidence"],
            conflicting_evidence=False,
            regulatory_exposure=False,
            governance_exposure=False,
            privacy_impact=False,
            destructive_action=False,
            irreversible_action=False,
            high_root_cause_uncertainty=(
                not hypotheses or max(hypothesis.confidence for hypothesis in hypotheses) < 0.70
            ),
            unsafe_recommendation=not recommendations,
            critical_process_affected=False,
        )

        decision = evaluate_human_review(signals)

        if recommendation_requires_approval:
            reason = "recommended action requires human approval"
            reasons = list(decision.human_review_reasons)

            if reason not in reasons:
                reasons.append(reason)

            decision = HumanReviewDecision(
                human_review_required=True,
                human_review_reasons=reasons,
            )
    except Exception as exc:
        return _failure_update(
            "human_review_evaluated",
            exc,
        )

    return _success_update(
        "human_review_evaluated",
        human_review_decision=decision,
    )


def build_final_response_node(
    state: AgentState,
) -> dict[str, object]:
    """Build the validated final AgentResponse from workflow state."""
    try:
        classification = _require_value(
            state["classification"],
            "classification",
        )
        severity = _require_value(
            state["severity"],
            "severity",
        )
        executive_summary = _require_value(
            state["executive_summary"],
            "executive_summary",
        )
        confidence = _require_value(
            state["confidence"],
            "confidence",
        )
        business_impact = _require_value(
            state["tool_results"].business_impact,
            "business_impact",
        )
        review = _require_value(
            state["human_review_decision"],
            "human_review_decision",
        )

        response = AgentResponse(
            incident_id=state["incident"].incident_id,
            classification=classification,
            severity=severity,
            executive_summary=executive_summary,
            evidence=[item.model_copy(deep=True) for item in state["evidence"]],
            business_impact=business_impact.model_copy(deep=True),
            root_cause_hypotheses=[
                item.model_copy(deep=True) for item in state["root_cause_hypotheses"]
            ],
            recommended_actions=[
                item.model_copy(deep=True) for item in state["recommended_actions"]
            ],
            governance_controls=[
                item.model_copy(deep=True) for item in state["tool_results"].governance_controls
            ],
            confidence=confidence,
            human_review_required=review.human_review_required,
            human_review_reasons=list(review.human_review_reasons),
        )
    except Exception as exc:
        return _failure_update(
            "response_built",
            exc,
        )

    return _success_update(
        "response_built",
        final_response=response,
    )


def _build_hypothesis_context(
    state: AgentState,
) -> str:
    payload = {
        "incident": state["incident"].model_dump(mode="json"),
        "evidence": [item.model_dump(mode="json") for item in state["evidence"]],
        "tool_results": state["tool_results"].model_dump(mode="json"),
    }

    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
    )


def _build_recommendation_context(
    state: AgentState,
) -> str:
    payload = {
        "incident": state["incident"].model_dump(mode="json"),
        "evidence": [item.model_dump(mode="json") for item in state["evidence"]],
        "tool_results": state["tool_results"].model_dump(mode="json"),
        "classification": (
            state["classification"].value if state["classification"] is not None else None
        ),
        "severity": (state["severity"].value if state["severity"] is not None else None),
        "root_cause_hypotheses": [
            item.model_dump(mode="json") for item in state["root_cause_hypotheses"]
        ],
    }

    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
    )


def _has_material_business_impact(
    impact: BusinessImpact | None,
) -> bool:
    if impact is None or impact.materiality is None:
        return False

    return impact.materiality.strip().lower() in {
        "material",
        "high",
        "significant",
        "critical",
    }


def _require_value[T](
    value: T | None,
    field_name: str,
) -> T:
    if value is None:
        raise WorkflowNodeStateError(f"required workflow field is missing: {field_name}")

    return value


def _success_update(
    step: WorkflowStep,
    **values: object,
) -> dict[str, object]:
    """Build a successful node update."""
    return {
        **values,
        "current_step": step,
        "completed_steps": [step],
    }


def _failure_update(
    step: WorkflowStep,
    exc: Exception,
) -> dict[str, object]:
    """Convert a node failure into explicit workflow state."""
    return {
        "current_step": "failed",
        "errors": [
            WorkflowError(
                step=step,
                error_type=type(exc).__name__,
                message=str(exc),
                recoverable=False,
            )
        ],
    }


__all__ = [
    "HypothesisGenerationResult",
    "RecommendationGenerationResult",
    "WorkflowNodeStateError",
    "analyze_business_impact_node",
    "analyze_quality_node",
    "build_final_response_node",
    "collect_evidence_node",
    "determine_human_review_node",
    "make_generate_hypotheses_node",
    "make_generate_recommendations_node",
    "retrieve_policies_node",
    "validate_incident_node",
]
