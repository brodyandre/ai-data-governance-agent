"""Tests for deterministic DG-702 evaluation metrics."""

from collections.abc import Iterator

from ai_data_governance_agent.evaluation import (
    evaluate_dataset,
    evaluate_scenario,
    load_evaluation_dataset,
)


def scenario_by_id(scenario_id: str):
    """Return one evaluation scenario by identifier."""
    scenarios = {scenario.scenario_id: scenario for scenario in load_evaluation_dataset()}

    return scenarios[scenario_id]


def make_clock(
    values: list[float],
):
    """Return a deterministic monotonic clock."""
    iterator: Iterator[float] = iter(values)

    return lambda: next(iterator)


def test_evaluation_executes_all_dataset_scenarios() -> None:
    report = evaluate_dataset()

    assert report.scenario_count == 7
    assert len(report.scenarios) == 7


def test_all_responses_are_schema_valid() -> None:
    report = evaluate_dataset()

    assert report.metrics.schema_valid_rate == 1.0

    assert all(result.schema_valid for result in report.scenarios)


def test_severity_accuracy_is_perfect_for_baseline_dataset() -> None:
    report = evaluate_dataset()

    assert report.metrics.severity_accuracy == 1.0

    assert all(result.severity_match for result in report.scenarios)


def test_evidence_traceability_is_complete() -> None:
    report = evaluate_dataset()

    assert report.metrics.evidence_traceability_rate == 1.0

    assert all(result.evidence_traceability_rate == 1.0 for result in report.scenarios)


def test_unsupported_claims_are_rejected() -> None:
    report = evaluate_dataset()

    applicable = [result for result in report.scenarios if result.unsupported_rejection_applicable]

    assert len(applicable) == 2

    assert report.metrics.unsupported_rejection_rate == 1.0

    assert all(result.unsupported_rejection_passed is True for result in applicable)


def test_human_review_accuracy_matches_dataset() -> None:
    report = evaluate_dataset()

    assert report.metrics.human_review_accuracy == 1.0

    assert all(result.human_review_match for result in report.scenarios)


def test_tool_execution_success_rate_is_complete() -> None:
    report = evaluate_dataset()

    assert report.metrics.tool_execution_success_rate == 1.0

    assert all(result.successful_tool_executions == 4 for result in report.scenarios)

    assert all(result.expected_tool_executions == 4 for result in report.scenarios)


def test_response_latency_is_reported_in_milliseconds() -> None:
    scenario = scenario_by_id("low_severity_incident")

    clock = make_clock(
        [
            10.000,
            10.025,
        ]
    )

    result = evaluate_scenario(
        scenario,
        clock=clock,
    )

    assert result.response_latency == 25.0


def test_test_pass_rate_is_perfect_for_baseline_dataset() -> None:
    report = evaluate_dataset()

    assert report.metrics.test_pass_rate == 1.0

    assert all(result.passed for result in report.scenarios)


def test_classification_is_checked_per_scenario() -> None:
    report = evaluate_dataset()

    assert all(result.classification_match for result in report.scenarios)


def test_insufficient_evidence_guardrail_is_measured() -> None:
    result = evaluate_scenario(scenario_by_id("insufficient_evidence"))

    assert result.unsupported_rejection_applicable is True

    assert result.unsupported_rejection_passed is True

    assert result.passed is True


def test_unsupported_claim_downgrade_is_measured() -> None:
    result = evaluate_scenario(scenario_by_id("unsupported_claim"))

    assert result.unsupported_rejection_applicable is True

    assert result.unsupported_rejection_passed is True

    assert result.passed is True
