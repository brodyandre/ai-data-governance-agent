"""Deterministic evaluation metrics for the agent workflow."""

from collections.abc import Callable, Iterable
from time import perf_counter

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from ai_data_governance_agent.domain.response import AgentResponse
from ai_data_governance_agent.evaluation.dataset import (
    EvaluationScenario,
    load_evaluation_dataset,
)
from ai_data_governance_agent.guardrails import evaluate_traceability
from ai_data_governance_agent.providers import FakeProvider
from ai_data_governance_agent.workflow import (
    HypothesisGenerationResult,
    RecommendationGenerationResult,
    run_agent_state,
)

_TOOL_STEPS = frozenset(
    {
        "evidence_collected",
        "quality_analyzed",
        "business_impact_analyzed",
        "policies_retrieved",
    }
)


class ScenarioEvaluationResult(BaseModel):
    """Represent evaluation measurements for one scenario."""

    model_config = ConfigDict(extra="forbid")

    scenario_id: str

    schema_valid: bool
    classification_match: bool
    severity_match: bool
    human_review_match: bool

    evidence_traceability_rate: float = Field(
        ge=0.0,
        le=1.0,
    )
    traceable_claims: int = Field(ge=0)
    total_traceable_claims: int = Field(ge=0)

    unsupported_rejection_applicable: bool
    unsupported_rejection_passed: bool | None

    tool_execution_success_rate: float = Field(
        ge=0.0,
        le=1.0,
    )
    successful_tool_executions: int = Field(ge=0)
    expected_tool_executions: int = Field(ge=0)

    response_latency: float = Field(ge=0.0)

    passed: bool


class EvaluationMetrics(BaseModel):
    """Represent aggregate DG-702 evaluation metrics."""

    model_config = ConfigDict(extra="forbid")

    schema_valid_rate: float = Field(
        ge=0.0,
        le=1.0,
    )
    severity_accuracy: float = Field(
        ge=0.0,
        le=1.0,
    )
    evidence_traceability_rate: float = Field(
        ge=0.0,
        le=1.0,
    )
    unsupported_rejection_rate: float = Field(
        ge=0.0,
        le=1.0,
    )
    human_review_accuracy: float = Field(
        ge=0.0,
        le=1.0,
    )
    tool_execution_success_rate: float = Field(
        ge=0.0,
        le=1.0,
    )

    response_latency: float = Field(ge=0.0)

    test_pass_rate: float = Field(
        ge=0.0,
        le=1.0,
    )


class EvaluationReport(BaseModel):
    """Represent the complete deterministic evaluation report."""

    model_config = ConfigDict(extra="forbid")

    scenario_count: int = Field(gt=0)
    metrics: EvaluationMetrics
    scenarios: list[ScenarioEvaluationResult]


def evaluate_scenario(
    scenario: EvaluationScenario,
    *,
    clock: Callable[[], float] | None = None,
) -> ScenarioEvaluationResult:
    """Execute and measure one deterministic evaluation scenario."""
    timer = clock or perf_counter

    responses: dict[type[BaseModel], BaseModel] = {
        HypothesisGenerationResult: (scenario.hypothesis_response),
    }

    if scenario.recommendation_response is not None:
        responses[RecommendationGenerationResult] = scenario.recommendation_response

    provider = FakeProvider(
        responses=responses,
    )

    started_at = timer()

    try:
        state = run_agent_state(
            scenario.incident,
            provider,
        )
    except Exception:
        elapsed_ms = _elapsed_ms(
            started_at,
            timer(),
        )

        return _failed_scenario_result(
            scenario,
            response_latency=elapsed_ms,
        )

    elapsed_ms = _elapsed_ms(
        started_at,
        timer(),
    )

    response = state["final_response"]

    schema_valid = _is_schema_valid(response)

    classification_match = bool(
        response is not None and response.classification is scenario.expected.classification
    )

    severity_match = bool(response is not None and response.severity is scenario.expected.severity)

    human_review_match = bool(
        response is not None
        and response.human_review_required is scenario.expected.human_review_required
    )

    traceability_rate = 0.0
    traceable_claims = 0
    total_traceable_claims = 0

    if response is not None:
        traceability = evaluate_traceability(
            evidence=response.evidence,
            business_impact=response.business_impact,
            hypotheses=response.root_cause_hypotheses,
            recommendations=response.recommended_actions,
            governance_controls=response.governance_controls,
        )

        traceability_rate = traceability.traceability_rate
        traceable_claims = traceability.traceable_claims
        total_traceable_claims = traceability.total_claims

    unsupported_applicable = scenario.expected.unsupported_claim_rejection_expected

    unsupported_passed: bool | None = None

    if unsupported_applicable:
        actual_statuses = (
            [hypothesis.status for hypothesis in response.root_cause_hypotheses]
            if response is not None
            else None
        )

        unsupported_passed = actual_statuses == scenario.expected.final_hypothesis_statuses

    completed_steps = set(state["completed_steps"])

    successful_tools = len(_TOOL_STEPS.intersection(completed_steps))

    expected_tools = len(_TOOL_STEPS)

    tool_success_rate = successful_tools / expected_tools

    passed = all(
        (
            schema_valid,
            classification_match,
            severity_match,
            human_review_match,
            traceability_rate == 1.0,
            tool_success_rate == 1.0,
            (unsupported_passed is True if unsupported_applicable else True),
        )
    )

    return ScenarioEvaluationResult(
        scenario_id=scenario.scenario_id,
        schema_valid=schema_valid,
        classification_match=classification_match,
        severity_match=severity_match,
        human_review_match=human_review_match,
        evidence_traceability_rate=traceability_rate,
        traceable_claims=traceable_claims,
        total_traceable_claims=total_traceable_claims,
        unsupported_rejection_applicable=(unsupported_applicable),
        unsupported_rejection_passed=(unsupported_passed),
        tool_execution_success_rate=(tool_success_rate),
        successful_tool_executions=(successful_tools),
        expected_tool_executions=(expected_tools),
        response_latency=elapsed_ms,
        passed=passed,
    )


def evaluate_dataset(
    scenarios: Iterable[EvaluationScenario] | None = None,
    *,
    clock: Callable[[], float] | None = None,
) -> EvaluationReport:
    """Evaluate all scenarios and calculate aggregate metrics."""
    scenario_items = list(load_evaluation_dataset() if scenarios is None else scenarios)

    if not scenario_items:
        raise ValueError("evaluation dataset must contain at least one scenario")

    results = [
        evaluate_scenario(
            scenario,
            clock=clock,
        )
        for scenario in scenario_items
    ]

    scenario_count = len(results)

    schema_valid_rate = _rate(
        sum(result.schema_valid for result in results),
        scenario_count,
    )

    severity_accuracy = _rate(
        sum(result.severity_match for result in results),
        scenario_count,
    )

    total_claims = sum(result.total_traceable_claims for result in results)
    traceable_claims = sum(result.traceable_claims for result in results)

    evidence_traceability_rate = (
        _rate(
            traceable_claims,
            total_claims,
        )
        if total_claims
        else 1.0
    )

    unsupported_results = [result for result in results if result.unsupported_rejection_applicable]

    unsupported_rejection_rate = (
        _rate(
            sum(result.unsupported_rejection_passed is True for result in unsupported_results),
            len(unsupported_results),
        )
        if unsupported_results
        else 1.0
    )

    human_review_accuracy = _rate(
        sum(result.human_review_match for result in results),
        scenario_count,
    )

    successful_tool_executions = sum(result.successful_tool_executions for result in results)
    expected_tool_executions = sum(result.expected_tool_executions for result in results)

    tool_execution_success_rate = _rate(
        successful_tool_executions,
        expected_tool_executions,
    )

    response_latency = sum(result.response_latency for result in results) / scenario_count

    test_pass_rate = _rate(
        sum(result.passed for result in results),
        scenario_count,
    )

    return EvaluationReport(
        scenario_count=scenario_count,
        metrics=EvaluationMetrics(
            schema_valid_rate=schema_valid_rate,
            severity_accuracy=severity_accuracy,
            evidence_traceability_rate=(evidence_traceability_rate),
            unsupported_rejection_rate=(unsupported_rejection_rate),
            human_review_accuracy=(human_review_accuracy),
            tool_execution_success_rate=(tool_execution_success_rate),
            response_latency=round(
                response_latency,
                3,
            ),
            test_pass_rate=test_pass_rate,
        ),
        scenarios=results,
    )


def _is_schema_valid(
    response: AgentResponse | None,
) -> bool:
    if response is None:
        return False

    try:
        AgentResponse.model_validate(response.model_dump(mode="python"))
    except ValidationError:
        return False

    return True


def _failed_scenario_result(
    scenario: EvaluationScenario,
    *,
    response_latency: float,
) -> ScenarioEvaluationResult:
    unsupported_applicable = scenario.expected.unsupported_claim_rejection_expected

    return ScenarioEvaluationResult(
        scenario_id=scenario.scenario_id,
        schema_valid=False,
        classification_match=False,
        severity_match=False,
        human_review_match=False,
        evidence_traceability_rate=0.0,
        traceable_claims=0,
        total_traceable_claims=0,
        unsupported_rejection_applicable=(unsupported_applicable),
        unsupported_rejection_passed=(False if unsupported_applicable else None),
        tool_execution_success_rate=0.0,
        successful_tool_executions=0,
        expected_tool_executions=len(_TOOL_STEPS),
        response_latency=response_latency,
        passed=False,
    )


def _elapsed_ms(
    started_at: float,
    finished_at: float,
) -> float:
    """Convert monotonic elapsed time to non-negative milliseconds."""
    return round(
        max(
            finished_at - started_at,
            0.0,
        )
        * 1000,
        3,
    )


def _rate(
    numerator: int,
    denominator: int,
) -> float:
    """Return a normalized deterministic rate."""
    if denominator <= 0:
        raise ValueError("rate denominator must be greater than zero")

    return numerator / denominator


__all__ = [
    "EvaluationMetrics",
    "EvaluationReport",
    "ScenarioEvaluationResult",
    "evaluate_dataset",
    "evaluate_scenario",
]
