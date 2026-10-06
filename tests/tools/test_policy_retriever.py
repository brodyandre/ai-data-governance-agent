"""Tests for deterministic local policy retrieval."""

import pytest

from ai_data_governance_agent.domain import Evidence
from ai_data_governance_agent.tools import (
    PolicyRetrievalError,
    QualityFinding,
    analyze_quality,
    collect_evidence,
    retrieve_policies,
)


def make_evidence(
    evidence_id: str = "EV-001",
    *,
    evidence_type: str = "data_quality_check",
    value: object = None,
) -> Evidence:
    """Create validated evidence for policy-retrieval tests."""
    return Evidence.model_validate(
        {
            "evidence_id": evidence_id,
            "evidence_type": evidence_type,
            "source": "test-source",
            "value": value,
        }
    )


def make_finding(
    finding_type: str,
    evidence_id: str = "EV-001",
) -> QualityFinding:
    """Create one deterministic quality finding."""
    return QualityFinding.model_validate(
        {
            "finding_type": finding_type,
            "description": "Test finding.",
            "supporting_evidence": [evidence_id],
        }
    )


def test_empty_findings_return_no_controls() -> None:
    evidence = [make_evidence()]

    assert retrieve_policies(evidence, []) == []


def test_empty_evidence_and_findings_return_no_controls() -> None:
    assert retrieve_policies([], []) == []


@pytest.mark.parametrize(
    ("finding_type", "expected_control"),
    [
        ("invalid_records", "DQ-001"),
        ("validation_failures", "DQ-001"),
        ("reconciliation_divergence", "DQ-002"),
        ("count_divergence", "DQ-002"),
        ("missing_relationships", "DQ-003"),
        ("integrity_inconsistencies", "DQ-003"),
    ],
)
def test_each_supported_finding_maps_to_expected_control(
    finding_type: str,
    expected_control: str,
) -> None:
    evidence = [make_evidence()]
    findings = [make_finding(finding_type)]

    controls = retrieve_policies(evidence, findings)

    assert len(controls) == 1
    assert controls[0].control_id == expected_control
    assert controls[0].supporting_evidence == ["EV-001"]


def test_control_source_is_preserved() -> None:
    evidence = [make_evidence()]
    findings = [make_finding("invalid_records")]

    controls = retrieve_policies(evidence, findings)

    assert controls[0].source == ("docs/policies/LOCAL_CONTROLS.md#dq-001")


def test_multiple_findings_for_same_control_are_merged() -> None:
    evidence = [
        make_evidence("EV-001"),
        make_evidence("EV-002"),
    ]
    findings = [
        make_finding("invalid_records", "EV-001"),
        make_finding("validation_failures", "EV-002"),
    ]

    controls = retrieve_policies(evidence, findings)

    assert len(controls) == 1
    assert controls[0].control_id == "DQ-001"
    assert controls[0].supporting_evidence == [
        "EV-001",
        "EV-002",
    ]


def test_duplicate_supporting_evidence_is_removed() -> None:
    evidence = [make_evidence("EV-001")]
    findings = [
        make_finding("invalid_records", "EV-001"),
        make_finding("validation_failures", "EV-001"),
    ]

    controls = retrieve_policies(evidence, findings)

    assert controls[0].supporting_evidence == ["EV-001"]


def test_control_order_is_deterministic() -> None:
    evidence = [
        make_evidence("EV-001"),
        make_evidence("EV-002"),
        make_evidence("EV-003"),
    ]
    findings = [
        make_finding("missing_relationships", "EV-003"),
        make_finding("count_divergence", "EV-002"),
        make_finding("invalid_records", "EV-001"),
    ]

    controls = retrieve_policies(evidence, findings)

    assert [control.control_id for control in controls] == [
        "DQ-001",
        "DQ-002",
        "DQ-003",
    ]


def test_relevance_contains_matching_finding_type() -> None:
    evidence = [make_evidence()]
    findings = [make_finding("invalid_records")]

    controls = retrieve_policies(evidence, findings)

    assert "invalid_records" in controls[0].relevance


def test_multiple_finding_types_are_listed_in_relevance() -> None:
    evidence = [
        make_evidence("EV-001"),
        make_evidence("EV-002"),
    ]
    findings = [
        make_finding("invalid_records", "EV-001"),
        make_finding("validation_failures", "EV-002"),
    ]

    controls = retrieve_policies(evidence, findings)

    assert controls[0].relevance == (
        "Sinais de qualidade identificados: invalid_records, validation_failures."
    )


def test_unknown_evidence_reference_is_rejected() -> None:
    evidence = [make_evidence("EV-001")]
    findings = [
        make_finding(
            "invalid_records",
            "EV-NOT-FOUND",
        )
    ]

    with pytest.raises(
        PolicyRetrievalError,
        match="unknown evidence_id EV-NOT-FOUND",
    ):
        retrieve_policies(evidence, findings)


def test_unknown_evidence_error_reports_finding_index() -> None:
    evidence = [make_evidence("EV-001")]
    findings = [
        make_finding("invalid_records", "EV-001"),
        make_finding("validation_failures", "EV-NOT-FOUND"),
    ]

    with pytest.raises(
        PolicyRetrievalError,
        match="finding at index 1",
    ):
        retrieve_policies(evidence, findings)


def test_duplicate_evidence_ids_are_rejected() -> None:
    evidence = [
        make_evidence("EV-001"),
        make_evidence("EV-001"),
    ]

    with pytest.raises(
        PolicyRetrievalError,
        match="duplicate evidence_id: EV-001",
    ):
        retrieve_policies(evidence, [])


def test_same_input_produces_same_controls() -> None:
    evidence = [
        make_evidence("EV-001"),
        make_evidence("EV-002"),
    ]
    findings = [
        make_finding("invalid_records", "EV-001"),
        make_finding("count_divergence", "EV-002"),
    ]

    first = retrieve_policies(evidence, findings)
    second = retrieve_policies(evidence, findings)

    assert first == second


def test_control_titles_are_stable() -> None:
    evidence = [
        make_evidence("EV-001"),
        make_evidence("EV-002"),
        make_evidence("EV-003"),
    ]
    findings = [
        make_finding("invalid_records", "EV-001"),
        make_finding("count_divergence", "EV-002"),
        make_finding("missing_relationships", "EV-003"),
    ]

    controls = retrieve_policies(evidence, findings)

    assert [control.title for control in controls] == [
        "Validação de qualidade de registros",
        "Reconciliação de volumes",
        "Integridade e relacionamentos",
    ]


def test_control_descriptions_are_non_empty() -> None:
    evidence = [make_evidence()]
    findings = [make_finding("invalid_records")]

    controls = retrieve_policies(evidence, findings)

    assert controls[0].description


def test_quality_analyzer_and_policy_retriever_integration() -> None:
    evidence = collect_evidence(
        [
            {
                "evidence_id": "EV-001",
                "evidence_type": "data_quality_check",
                "source": "quality-report",
                "value": {
                    "invalid_rows": 30,
                    "missing_relationships": 33,
                },
            },
            {
                "evidence_id": "EV-002",
                "evidence_type": "reconciliation_result",
                "source": "pipeline-report",
                "value": {
                    "raw_count": 400,
                    "silver_count": 388,
                },
            },
        ]
    )

    findings = analyze_quality(evidence)
    controls = retrieve_policies(evidence, findings)

    assert [control.control_id for control in controls] == [
        "DQ-001",
        "DQ-002",
        "DQ-003",
    ]

    assert controls[0].supporting_evidence == ["EV-001"]
    assert controls[1].supporting_evidence == ["EV-002"]
    assert controls[2].supporting_evidence == ["EV-001"]


def test_no_quality_problem_produces_no_control() -> None:
    evidence = collect_evidence(
        [
            {
                "evidence_id": "EV-001",
                "evidence_type": "data_quality_check",
                "source": "quality-report",
                "value": {
                    "invalid_rows": 0,
                },
            },
            {
                "evidence_id": "EV-002",
                "evidence_type": "reconciliation_result",
                "source": "pipeline-report",
                "value": {
                    "raw_count": 400,
                    "silver_count": 400,
                },
            },
        ]
    )

    findings = analyze_quality(evidence)

    assert findings == []
    assert retrieve_policies(evidence, findings) == []


def test_policy_retrieval_is_offline_and_local() -> None:
    evidence = [make_evidence()]
    findings = [make_finding("invalid_records")]

    controls = retrieve_policies(evidence, findings)

    assert controls[0].source.startswith("docs/policies/")


def test_findings_input_order_does_not_change_policy_catalog_order() -> None:
    evidence = [
        make_evidence("EV-001"),
        make_evidence("EV-002"),
        make_evidence("EV-003"),
    ]

    first = retrieve_policies(
        evidence,
        [
            make_finding("invalid_records", "EV-001"),
            make_finding("count_divergence", "EV-002"),
            make_finding("missing_relationships", "EV-003"),
        ],
    )

    second = retrieve_policies(
        evidence,
        [
            make_finding("missing_relationships", "EV-003"),
            make_finding("invalid_records", "EV-001"),
            make_finding("count_divergence", "EV-002"),
        ],
    )

    assert [item.control_id for item in first] == [
        "DQ-001",
        "DQ-002",
        "DQ-003",
    ]
    assert [item.control_id for item in second] == [
        "DQ-001",
        "DQ-002",
        "DQ-003",
    ]
