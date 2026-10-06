"""Tests for deterministic data-quality analysis."""

import pytest
from pydantic import ValidationError

from ai_data_governance_agent.domain import Evidence
from ai_data_governance_agent.tools import (
    QualityFinding,
    analyze_quality,
    collect_evidence,
)


def make_evidence(
    evidence_id: str = "EV-001",
    *,
    evidence_type: str = "data_quality_check",
    value: object = None,
) -> Evidence:
    """Create validated evidence for quality-analysis tests."""
    return Evidence.model_validate(
        {
            "evidence_id": evidence_id,
            "evidence_type": evidence_type,
            "source": "test-source",
            "value": value,
        }
    )


def test_empty_evidence_produces_no_findings() -> None:
    assert analyze_quality([]) == []


def test_invalid_records_are_detected() -> None:
    findings = analyze_quality(
        [
            make_evidence(
                value={"invalid_rows": 30},
            )
        ]
    )

    assert len(findings) == 1
    assert findings[0].finding_type == "invalid_records"
    assert findings[0].supporting_evidence == ["EV-001"]
    assert findings[0].details == {"invalid_rows": 30}


def test_missing_relationships_are_detected() -> None:
    findings = analyze_quality(
        [
            make_evidence(
                value={"missing_relationships": 33},
            )
        ]
    )

    assert len(findings) == 1
    assert findings[0].finding_type == "missing_relationships"
    assert findings[0].supporting_evidence == ["EV-001"]
    assert findings[0].details == {"missing_relationships": 33}


def test_validation_failures_are_detected() -> None:
    findings = analyze_quality(
        [
            make_evidence(
                evidence_type="validation_result",
                value={"validation_failures": 7},
            )
        ]
    )

    assert len(findings) == 1
    assert findings[0].finding_type == "validation_failures"
    assert findings[0].supporting_evidence == ["EV-001"]
    assert findings[0].details == {"validation_failures": 7}


def test_integrity_inconsistencies_are_detected() -> None:
    findings = analyze_quality(
        [
            make_evidence(
                value={"integrity_violations": 4},
            )
        ]
    )

    assert len(findings) == 1
    assert findings[0].finding_type == "integrity_inconsistencies"
    assert findings[0].supporting_evidence == ["EV-001"]
    assert findings[0].details == {"integrity_violations": 4}


def test_expected_actual_reconciliation_divergence_is_detected() -> None:
    findings = analyze_quality(
        [
            make_evidence(
                evidence_type="reconciliation_result",
                value={
                    "expected_count": 400,
                    "actual_count": 388,
                },
            )
        ]
    )

    assert len(findings) == 1
    finding = findings[0]

    assert finding.finding_type == "reconciliation_divergence"
    assert finding.supporting_evidence == ["EV-001"]
    assert finding.details == {
        "expected_count": 400,
        "actual_count": 388,
        "absolute_difference": 12,
    }


def test_source_target_count_divergence_is_detected() -> None:
    findings = analyze_quality(
        [
            make_evidence(
                evidence_type="reconciliation_result",
                value={
                    "source_count": 1000,
                    "target_count": 970,
                },
            )
        ]
    )

    assert len(findings) == 1
    finding = findings[0]

    assert finding.finding_type == "count_divergence"
    assert finding.supporting_evidence == ["EV-001"]
    assert finding.details == {
        "source_count": 1000,
        "target_count": 970,
        "absolute_difference": 30,
    }


def test_raw_silver_count_divergence_is_detected() -> None:
    findings = analyze_quality(
        [
            make_evidence(
                evidence_type="reconciliation_result",
                value={
                    "raw_count": 400,
                    "silver_count": 388,
                },
            )
        ]
    )

    assert len(findings) == 1
    finding = findings[0]

    assert finding.finding_type == "count_divergence"
    assert finding.supporting_evidence == ["EV-001"]
    assert finding.details == {
        "raw_count": 400,
        "silver_count": 388,
        "absolute_difference": 12,
    }


@pytest.mark.parametrize(
    ("key", "finding_type"),
    [
        ("invalid_rows", "invalid_records"),
        ("missing_relationships", "missing_relationships"),
        ("validation_failures", "validation_failures"),
        ("integrity_violations", "integrity_inconsistencies"),
    ],
)
def test_zero_quality_count_does_not_generate_finding(
    key: str,
    finding_type: str,
) -> None:
    findings = analyze_quality(
        [
            make_evidence(
                value={key: 0},
            )
        ]
    )

    assert all(item.finding_type != finding_type for item in findings)


@pytest.mark.parametrize(
    "value",
    [
        -1,
        -100,
        1.5,
        "10",
        True,
        False,
        None,
    ],
)
def test_unsupported_quality_count_does_not_generate_finding(
    value: object,
) -> None:
    findings = analyze_quality(
        [
            make_evidence(
                value={"invalid_rows": value},
            )
        ]
    )

    assert findings == []


def test_equal_expected_actual_counts_do_not_generate_finding() -> None:
    findings = analyze_quality(
        [
            make_evidence(
                evidence_type="reconciliation_result",
                value={
                    "expected_count": 400,
                    "actual_count": 400,
                },
            )
        ]
    )

    assert findings == []


def test_equal_source_target_counts_do_not_generate_finding() -> None:
    findings = analyze_quality(
        [
            make_evidence(
                evidence_type="reconciliation_result",
                value={
                    "source_count": 1000,
                    "target_count": 1000,
                },
            )
        ]
    )

    assert findings == []


def test_equal_raw_silver_counts_do_not_generate_finding() -> None:
    findings = analyze_quality(
        [
            make_evidence(
                evidence_type="reconciliation_result",
                value={
                    "raw_count": 400,
                    "silver_count": 400,
                },
            )
        ]
    )

    assert findings == []


@pytest.mark.parametrize(
    "value",
    [
        {
            "expected_count": -1,
            "actual_count": 10,
        },
        {
            "expected_count": 10.5,
            "actual_count": 10,
        },
        {
            "expected_count": "10",
            "actual_count": 9,
        },
        {
            "expected_count": True,
            "actual_count": 0,
        },
    ],
)
def test_invalid_reconciliation_counts_do_not_generate_finding(
    value: object,
) -> None:
    findings = analyze_quality(
        [
            make_evidence(
                evidence_type="reconciliation_result",
                value=value,
            )
        ]
    )

    assert findings == []


def test_missing_reconciliation_side_does_not_generate_finding() -> None:
    findings = analyze_quality(
        [
            make_evidence(
                evidence_type="reconciliation_result",
                value={
                    "raw_count": 400,
                },
            )
        ]
    )

    assert findings == []


def test_non_mapping_value_does_not_generate_finding() -> None:
    evidence = [
        make_evidence(
            value=42,
        ),
        make_evidence(
            "EV-002",
            value="invalid rows detected",
        ),
        make_evidence(
            "EV-003",
            value=["invalid_rows", 30],
        ),
    ]

    assert analyze_quality(evidence) == []


def test_free_text_description_does_not_generate_finding() -> None:
    evidence = Evidence.model_validate(
        {
            "evidence_id": "EV-TEXT",
            "evidence_type": "log",
            "source": "application-log",
            "description": ("30 invalid rows and 33 missing relationships were detected."),
        }
    )

    assert analyze_quality([evidence]) == []


def test_log_with_quality_shaped_value_does_not_generate_finding() -> None:
    evidence = make_evidence(
        evidence_type="log",
        value={
            "invalid_rows": 30,
            "missing_relationships": 33,
        },
    )

    assert analyze_quality([evidence]) == []


def test_metric_with_quality_shaped_value_does_not_generate_finding() -> None:
    evidence = make_evidence(
        evidence_type="metric",
        value={
            "invalid_rows": 30,
        },
    )

    assert analyze_quality([evidence]) == []


def test_data_quality_check_does_not_apply_reconciliation_rules() -> None:
    evidence = make_evidence(
        evidence_type="data_quality_check",
        value={
            "raw_count": 400,
            "silver_count": 388,
        },
    )

    assert analyze_quality([evidence]) == []


def test_reconciliation_result_does_not_apply_quality_count_rules() -> None:
    evidence = make_evidence(
        evidence_type="reconciliation_result",
        value={
            "invalid_rows": 30,
        },
    )

    assert analyze_quality([evidence]) == []


def test_multiple_supported_signals_from_one_evidence_are_preserved() -> None:
    evidence = make_evidence(
        value={
            "invalid_rows": 30,
            "missing_relationships": 33,
            "validation_failures": 2,
            "integrity_violations": 1,
        },
    )

    findings = analyze_quality([evidence])

    assert [item.finding_type for item in findings] == [
        "invalid_records",
        "missing_relationships",
        "validation_failures",
        "integrity_inconsistencies",
    ]

    assert all(item.supporting_evidence == ["EV-001"] for item in findings)


def test_findings_preserve_input_evidence_order() -> None:
    evidence = [
        make_evidence(
            "EV-002",
            value={"invalid_rows": 2},
        ),
        make_evidence(
            "EV-001",
            value={"missing_relationships": 1},
        ),
    ]

    findings = analyze_quality(evidence)

    assert [item.supporting_evidence[0] for item in findings] == [
        "EV-002",
        "EV-001",
    ]


def test_findings_have_deterministic_order_within_evidence() -> None:
    evidence = make_evidence(
        value={
            "integrity_violations": 1,
            "validation_failures": 2,
            "missing_relationships": 3,
            "invalid_rows": 4,
        },
    )

    findings = analyze_quality([evidence])

    assert [item.finding_type for item in findings] == [
        "invalid_records",
        "missing_relationships",
        "validation_failures",
        "integrity_inconsistencies",
    ]


def test_reconciliation_findings_have_deterministic_order() -> None:
    evidence = make_evidence(
        evidence_type="reconciliation_result",
        value={
            "expected_count": 100,
            "actual_count": 90,
            "source_count": 200,
            "target_count": 180,
            "raw_count": 300,
            "silver_count": 270,
        },
    )

    findings = analyze_quality([evidence])

    assert [item.finding_type for item in findings] == [
        "reconciliation_divergence",
        "count_divergence",
        "count_divergence",
    ]

    assert findings[0].details["absolute_difference"] == 10
    assert findings[1].details["absolute_difference"] == 20
    assert findings[2].details["absolute_difference"] == 30


def test_same_input_produces_same_findings() -> None:
    evidence = [
        make_evidence(
            "EV-001",
            value={
                "invalid_rows": 30,
                "missing_relationships": 33,
            },
        ),
        make_evidence(
            "EV-002",
            evidence_type="reconciliation_result",
            value={
                "raw_count": 400,
                "silver_count": 388,
            },
        ),
    ]

    first = analyze_quality(evidence)
    second = analyze_quality(evidence)

    assert first == second


def test_quality_finding_requires_supporting_evidence() -> None:
    with pytest.raises(ValidationError):
        QualityFinding(
            finding_type="invalid_records",
            description="Invalid rows found.",
            supporting_evidence=[],
        )


def test_quality_finding_rejects_invalid_finding_type() -> None:
    with pytest.raises(ValidationError):
        QualityFinding(
            finding_type="unsupported",  # type: ignore[arg-type]
            description="Unsupported finding.",
            supporting_evidence=["EV-001"],
        )


def test_quality_finding_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        QualityFinding.model_validate(
            {
                "finding_type": "invalid_records",
                "description": "Invalid rows found.",
                "supporting_evidence": ["EV-001"],
                "unexpected": True,
            }
        )


def test_quality_finding_serialization_is_predictable() -> None:
    finding = QualityFinding(
        finding_type="invalid_records",
        description="Evidence reports 30 invalid rows.",
        supporting_evidence=["EV-001"],
        details={
            "invalid_rows": 30,
        },
    )

    assert finding.model_dump() == {
        "finding_type": "invalid_records",
        "description": "Evidence reports 30 invalid rows.",
        "supporting_evidence": ["EV-001"],
        "details": {
            "invalid_rows": 30,
        },
    }


def test_collector_and_analyzer_integration() -> None:
    evidence = collect_evidence(
        [
            {
                "evidence_id": " EV-001 ",
                "evidence_type": "reconciliation_result",
                "source": " pipeline-report ",
                "value": {
                    "raw_count": 400,
                    "silver_count": 388,
                },
            },
            {
                "evidence_id": "EV-002",
                "evidence_type": "data_quality_check",
                "source": "quality-check",
                "value": {
                    "invalid_rows": 30,
                },
            },
        ]
    )

    findings = analyze_quality(evidence)

    assert [
        (
            item.finding_type,
            item.supporting_evidence,
        )
        for item in findings
    ] == [
        (
            "count_divergence",
            ["EV-001"],
        ),
        (
            "invalid_records",
            ["EV-002"],
        ),
    ]
