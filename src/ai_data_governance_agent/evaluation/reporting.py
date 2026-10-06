"""Human-readable reporting for deterministic evaluation results."""

from ai_data_governance_agent.evaluation.metrics import (
    EvaluationReport,
    ScenarioEvaluationResult,
)

_METRIC_LABELS = (
    ("schema_valid_rate", "Schema valid rate"),
    ("severity_accuracy", "Severity accuracy"),
    (
        "evidence_traceability_rate",
        "Evidence traceability rate",
    ),
    (
        "unsupported_rejection_rate",
        "Unsupported rejection rate",
    ),
    (
        "human_review_accuracy",
        "Human review accuracy",
    ),
    (
        "tool_execution_success_rate",
        "Tool execution success rate",
    ),
    ("test_pass_rate", "Test pass rate"),
)


def render_summary(
    report: EvaluationReport,
) -> str:
    """Render a concise terminal-friendly evaluation summary."""
    passed_scenarios = sum(scenario.passed for scenario in report.scenarios)

    lines = [
        "AI Data Governance Agent - Evaluation Summary",
        "=" * 45,
        f"Scenarios: {report.scenario_count}",
        (f"Scenario results: {passed_scenarios}/{report.scenario_count} passed"),
        "",
        "Metrics",
        "-------",
    ]

    for field_name, label in _METRIC_LABELS:
        value = getattr(
            report.metrics,
            field_name,
        )

        lines.append(f"{label}: {_percentage(value)}")

    lines.extend(
        [
            (f"Response latency: {report.metrics.response_latency:.3f} ms"),
            "",
            "Scenarios",
            "---------",
        ]
    )

    for scenario in report.scenarios:
        lines.append(_scenario_summary_line(scenario))

    lines.extend(
        [
            "",
            ("Latency is environment-dependent and is not part of the functional pass criteria."),
        ]
    )

    return "\n".join(lines)


def render_markdown(
    report: EvaluationReport,
) -> str:
    """Render a Markdown report reusable in documentation."""
    passed_scenarios = sum(scenario.passed for scenario in report.scenarios)

    lines = [
        "# Deterministic Evaluation Report",
        "",
        "## Executive summary",
        "",
        (f"- Scenarios evaluated: **{report.scenario_count}**"),
        (f"- Scenarios passed: **{passed_scenarios}/{report.scenario_count}**"),
        (
            "- Overall functional status: "
            f"**{'PASS' if passed_scenarios == report.scenario_count else 'FAIL'}**"
        ),
        (f"- Average local response latency: **{report.metrics.response_latency:.3f} ms**"),
        "",
        "## Metrics",
        "",
        "| Metric | Result |",
        "| --- | ---: |",
    ]

    for field_name, _label in _METRIC_LABELS:
        value = getattr(
            report.metrics,
            field_name,
        )

        lines.append(f"| `{field_name}` | {_percentage(value)} |")

    lines.extend(
        [
            (f"| `response_latency` | {report.metrics.response_latency:.3f} ms |"),
            "",
            "## Scenario results",
            "",
            (
                "| Scenario | Status | Schema | Classification | "
                "Severity | Human review | Traceability | Tools |"
            ),
            ("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |"),
        ]
    )

    for scenario in report.scenarios:
        lines.append(_scenario_markdown_row(scenario))

    lines.extend(
        [
            "",
            "## Challenge-ready highlights",
            "",
            (f"- **{passed_scenarios}/{report.scenario_count}** deterministic scenarios passed."),
            (
                "- **"
                f"{_percentage(report.metrics.evidence_traceability_rate)}"
                "** evidence traceability for claims requiring support."
            ),
            (
                "- **"
                f"{_percentage(report.metrics.unsupported_rejection_rate)}"
                "** rejection or conservative qualification of "
                "unsupported claims."
            ),
            (
                "- **"
                f"{_percentage(report.metrics.human_review_accuracy)}"
                "** human-review decision accuracy."
            ),
            (
                "- **"
                f"{_percentage(report.metrics.tool_execution_success_rate)}"
                "** deterministic tool execution success."
            ),
            "",
            "> Response latency is measured locally and varies by environment. "
            "It is not part of the functional pass criteria.",
            "",
        ]
    )

    return "\n".join(lines)


def _scenario_summary_line(
    scenario: ScenarioEvaluationResult,
) -> str:
    status = "PASS" if scenario.passed else "FAIL"

    return (
        f"[{status}] {scenario.scenario_id} "
        f"(traceability="
        f"{_percentage(scenario.evidence_traceability_rate)}, "
        f"tools="
        f"{_percentage(scenario.tool_execution_success_rate)})"
    )


def _scenario_markdown_row(
    scenario: ScenarioEvaluationResult,
) -> str:
    return (
        f"| `{scenario.scenario_id}` "
        f"| {'PASS' if scenario.passed else 'FAIL'} "
        f"| {_boolean_mark(scenario.schema_valid)} "
        f"| {_boolean_mark(scenario.classification_match)} "
        f"| {_boolean_mark(scenario.severity_match)} "
        f"| {_boolean_mark(scenario.human_review_match)} "
        f"| {_percentage(scenario.evidence_traceability_rate)} "
        f"| {_percentage(scenario.tool_execution_success_rate)} |"
    )


def _percentage(
    value: float,
) -> str:
    """Render a normalized rate as a percentage."""
    return f"{value * 100:.1f}%"


def _boolean_mark(
    value: bool,
) -> str:
    """Render booleans without terminal-dependent symbols."""
    return "PASS" if value else "FAIL"


__all__ = [
    "render_markdown",
    "render_summary",
]
