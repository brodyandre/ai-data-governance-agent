"""Tests for DG-703 evaluation reporting."""

import json
from pathlib import Path

from ai_data_governance_agent.evaluation import (
    evaluate_dataset,
    render_markdown,
    render_summary,
)
from ai_data_governance_agent.evaluation.__main__ import main


def test_summary_is_human_readable() -> None:
    report = evaluate_dataset()

    summary = render_summary(report)

    assert "AI Data Governance Agent - Evaluation Summary" in summary
    assert "Scenarios: 7" in summary
    assert "Scenario results: 7/7 passed" in summary
    assert "Schema valid rate: 100.0%" in summary
    assert "Severity accuracy: 100.0%" in summary
    assert "Test pass rate: 100.0%" in summary


def test_summary_lists_all_evaluation_scenarios() -> None:
    report = evaluate_dataset()

    summary = render_summary(report)

    expected_scenarios = {
        "de_101_raw_silver_divergence",
        "de_102_revenue_semantics",
        "insufficient_evidence",
        "conflicting_evidence",
        "low_severity_incident",
        "critical_incident",
        "unsupported_claim",
    }

    for scenario_id in expected_scenarios:
        assert f"[PASS] {scenario_id}" in summary

    assert "Latency is environment-dependent" in summary


def test_markdown_report_is_reusable_in_documentation() -> None:
    report = evaluate_dataset()

    markdown = render_markdown(report)

    assert "# Deterministic Evaluation Report" in markdown
    assert "## Executive summary" in markdown
    assert "## Metrics" in markdown
    assert "## Scenario results" in markdown
    assert "## Challenge-ready highlights" in markdown

    assert "- Overall functional status: **PASS**" in markdown

    assert "| `schema_valid_rate` | 100.0% |" in markdown

    assert "| `test_pass_rate` | 100.0% |" in markdown


def test_markdown_contains_challenge_ready_metrics() -> None:
    report = evaluate_dataset()

    markdown = render_markdown(report)

    assert "**7/7** deterministic scenarios passed." in markdown

    assert "**100.0%** evidence traceability" in markdown

    assert "**100.0%** rejection or conservative qualification" in markdown

    assert "**100.0%** human-review decision accuracy." in markdown


def test_cli_defaults_to_summary(
    capsys,
) -> None:
    main([])

    captured = capsys.readouterr()

    assert "AI Data Governance Agent - Evaluation Summary" in captured.out
    assert "Scenario results: 7/7 passed" in captured.out


def test_cli_json_output_is_machine_readable(
    capsys,
) -> None:
    main(
        [
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()

    payload = json.loads(captured.out)

    assert payload["scenario_count"] == 7

    assert payload["metrics"]["schema_valid_rate"] == 1.0

    assert payload["metrics"]["test_pass_rate"] == 1.0


def test_cli_writes_markdown_report(
    tmp_path: Path,
    capsys,
) -> None:
    output_path = tmp_path / "reports" / "evaluation" / "latest.md"

    main(
        [
            "--format",
            "markdown",
            "--output",
            str(output_path),
        ]
    )

    captured = capsys.readouterr()

    assert output_path.exists()

    content = output_path.read_text(encoding="utf-8")

    assert "# Deterministic Evaluation Report" in content

    assert "## Challenge-ready highlights" in content

    assert str(output_path) in captured.out
