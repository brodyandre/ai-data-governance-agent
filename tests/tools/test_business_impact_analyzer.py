"""Tests for deterministic business-impact analysis."""

import pytest
from pydantic import ValidationError

from ai_data_governance_agent.domain import BusinessImpact, Evidence
from ai_data_governance_agent.tools import (
    BusinessImpactAnalysisError,
    analyze_business_impact,
    collect_evidence,
)


def make_evidence(
    evidence_id: str = "EV-BIZ-001",
    *,
    evidence_type: str = "analyst_observation",
    status: str = "confirmed",
    description: str = "Revenue reporting is affected.",
    affected_processes: list[str] | None = None,
    affected_consumers: list[str] | None = None,
    materiality: str | None = None,
) -> Evidence:
    """Create evidence containing one structured business-impact signal."""
    impact: dict[str, object] = {
        "status": status,
        "description": description,
    }

    if affected_processes is not None:
        impact["affected_processes"] = affected_processes

    if affected_consumers is not None:
        impact["affected_consumers"] = affected_consumers

    if materiality is not None:
        impact["materiality"] = materiality

    return Evidence.model_validate(
        {
            "evidence_id": evidence_id,
            "evidence_type": evidence_type,
            "source": "test-source",
            "value": {
                "business_impact": impact,
            },
        }
    )


def test_empty_evidence_returns_unknown() -> None:
    impact = analyze_business_impact([])

    assert impact.status.value == "unknown"
    assert impact.supporting_evidence == []
    assert impact.affected_processes == []
    assert impact.affected_consumers == []
    assert impact.materiality is None


def test_technical_evidence_without_business_signal_returns_unknown() -> None:
    evidence = Evidence.model_validate(
        {
            "evidence_id": "EV-DQ-001",
            "evidence_type": "data_quality_check",
            "source": "quality-check",
            "value": {
                "invalid_rows": 30,
            },
        }
    )

    impact = analyze_business_impact([evidence])

    assert impact.status.value == "unknown"
    assert impact.supporting_evidence == []


def test_confirmed_impact_from_analyst_observation() -> None:
    evidence = make_evidence(
        affected_processes=["revenue reporting"],
        affected_consumers=["finance"],
        materiality="high",
    )

    impact = analyze_business_impact([evidence])

    assert impact.status.value == "confirmed"
    assert impact.description == "Revenue reporting is affected."
    assert impact.affected_processes == ["revenue reporting"]
    assert impact.affected_consumers == ["finance"]
    assert impact.materiality == "high"
    assert impact.supporting_evidence == ["EV-BIZ-001"]


def test_potential_impact_from_business_rule() -> None:
    evidence = make_evidence(
        evidence_type="business_rule",
        status="potential",
        description="Missing records may affect revenue analytics.",
        affected_processes=["sales analytics"],
    )

    impact = analyze_business_impact([evidence])

    assert impact.status.value == "potential"
    assert impact.description == ("Missing records may affect revenue analytics.")
    assert impact.affected_processes == ["sales analytics"]
    assert impact.supporting_evidence == ["EV-BIZ-001"]


def test_explicit_unknown_is_representable() -> None:
    evidence = make_evidence(
        evidence_type="business_rule",
        status="unknown",
        description="Business consequence is not yet known.",
    )

    impact = analyze_business_impact([evidence])

    assert impact.status.value == "unknown"
    assert impact.description == "Business consequence is not yet known."
    assert impact.supporting_evidence == ["EV-BIZ-001"]


def test_confirmed_has_precedence_over_potential() -> None:
    evidence = [
        make_evidence(
            "EV-POTENTIAL",
            evidence_type="business_rule",
            status="potential",
            description="Revenue analytics may be affected.",
        ),
        make_evidence(
            "EV-CONFIRMED",
            status="confirmed",
            description="Revenue reporting is affected.",
        ),
    ]

    impact = analyze_business_impact(evidence)

    assert impact.status.value == "confirmed"
    assert impact.description == "Revenue reporting is affected."
    assert impact.supporting_evidence == ["EV-CONFIRMED"]


def test_potential_has_precedence_over_unknown() -> None:
    evidence = [
        make_evidence(
            "EV-UNKNOWN",
            evidence_type="business_rule",
            status="unknown",
            description="Impact is unknown.",
        ),
        make_evidence(
            "EV-POTENTIAL",
            evidence_type="business_rule",
            status="potential",
            description="Revenue analytics may be affected.",
        ),
    ]

    impact = analyze_business_impact(evidence)

    assert impact.status.value == "potential"
    assert impact.supporting_evidence == ["EV-POTENTIAL"]


def test_same_status_candidates_are_merged() -> None:
    evidence = [
        make_evidence(
            "EV-001",
            description="Revenue reporting is affected.",
            affected_processes=["revenue reporting"],
            affected_consumers=["finance"],
            materiality="high",
        ),
        make_evidence(
            "EV-002",
            description="Sales analytics is affected.",
            affected_processes=["sales analytics"],
            affected_consumers=["commercial"],
            materiality="high",
        ),
    ]

    impact = analyze_business_impact(evidence)

    assert impact.status.value == "confirmed"
    assert impact.description == ("Revenue reporting is affected. | Sales analytics is affected.")
    assert impact.affected_processes == [
        "revenue reporting",
        "sales analytics",
    ]
    assert impact.affected_consumers == [
        "finance",
        "commercial",
    ]
    assert impact.materiality == "high"
    assert impact.supporting_evidence == [
        "EV-001",
        "EV-002",
    ]


def test_duplicate_processes_and_consumers_are_removed() -> None:
    evidence = [
        make_evidence(
            "EV-001",
            affected_processes=["revenue reporting"],
            affected_consumers=["finance"],
        ),
        make_evidence(
            "EV-002",
            description="Second confirmed observation.",
            affected_processes=["revenue reporting"],
            affected_consumers=["finance"],
        ),
    ]

    impact = analyze_business_impact(evidence)

    assert impact.affected_processes == ["revenue reporting"]
    assert impact.affected_consumers == ["finance"]


def test_duplicate_descriptions_are_removed() -> None:
    evidence = [
        make_evidence("EV-001"),
        make_evidence("EV-002"),
    ]

    impact = analyze_business_impact(evidence)

    assert impact.description == "Revenue reporting is affected."


def test_conflicting_materiality_returns_none() -> None:
    evidence = [
        make_evidence(
            "EV-001",
            materiality="high",
        ),
        make_evidence(
            "EV-002",
            description="Second confirmed observation.",
            materiality="medium",
        ),
    ]

    impact = analyze_business_impact(evidence)

    assert impact.materiality is None


def test_single_materiality_is_preserved_when_other_is_missing() -> None:
    evidence = [
        make_evidence(
            "EV-001",
            materiality="high",
        ),
        make_evidence(
            "EV-002",
            description="Second confirmed observation.",
        ),
    ]

    impact = analyze_business_impact(evidence)

    assert impact.materiality == "high"


def test_confirmed_business_rule_is_rejected() -> None:
    evidence = make_evidence(
        evidence_type="business_rule",
        status="confirmed",
    )

    with pytest.raises(
        BusinessImpactAnalysisError,
        match="confirmed business impact requires analyst_observation",
    ):
        analyze_business_impact([evidence])


def test_unsupported_evidence_type_is_ignored() -> None:
    evidence = Evidence.model_validate(
        {
            "evidence_id": "EV-LOG",
            "evidence_type": "log",
            "source": "application-log",
            "value": {
                "business_impact": {
                    "status": "confirmed",
                    "description": "Revenue reporting is affected.",
                }
            },
        }
    )

    impact = analyze_business_impact([evidence])

    assert impact.status.value == "unknown"
    assert impact.supporting_evidence == []


def test_non_mapping_value_is_ignored() -> None:
    evidence = Evidence.model_validate(
        {
            "evidence_id": "EV-001",
            "evidence_type": "analyst_observation",
            "source": "analyst",
            "value": "Revenue reporting is affected.",
        }
    )

    impact = analyze_business_impact([evidence])

    assert impact.status.value == "unknown"


def test_missing_business_impact_key_is_ignored() -> None:
    evidence = Evidence.model_validate(
        {
            "evidence_id": "EV-001",
            "evidence_type": "analyst_observation",
            "source": "analyst",
            "value": {
                "comment": "Revenue reporting is affected.",
            },
        }
    )

    impact = analyze_business_impact([evidence])

    assert impact.status.value == "unknown"


def test_business_impact_must_be_object() -> None:
    evidence = Evidence.model_validate(
        {
            "evidence_id": "EV-001",
            "evidence_type": "analyst_observation",
            "source": "analyst",
            "value": {
                "business_impact": "confirmed",
            },
        }
    )

    with pytest.raises(
        BusinessImpactAnalysisError,
        match="business_impact must be an object",
    ):
        analyze_business_impact([evidence])


def test_invalid_status_is_rejected() -> None:
    evidence = Evidence.model_validate(
        {
            "evidence_id": "EV-001",
            "evidence_type": "analyst_observation",
            "source": "analyst",
            "value": {
                "business_impact": {
                    "status": "certain",
                    "description": "Revenue reporting is affected.",
                }
            },
        }
    )

    with pytest.raises(
        BusinessImpactAnalysisError,
        match="invalid business_impact",
    ) as exc_info:
        analyze_business_impact([evidence])

    assert isinstance(exc_info.value.__cause__, ValidationError)


def test_blank_description_is_rejected() -> None:
    evidence = Evidence.model_validate(
        {
            "evidence_id": "EV-001",
            "evidence_type": "analyst_observation",
            "source": "analyst",
            "value": {
                "business_impact": {
                    "status": "confirmed",
                    "description": "   ",
                }
            },
        }
    )

    with pytest.raises(
        BusinessImpactAnalysisError,
        match="invalid business_impact",
    ):
        analyze_business_impact([evidence])


def test_description_is_trimmed() -> None:
    evidence = make_evidence(
        description="  Revenue reporting is affected.  ",
    )

    impact = analyze_business_impact([evidence])

    assert impact.description == "Revenue reporting is affected."


def test_materiality_is_trimmed() -> None:
    evidence = make_evidence(
        materiality="  high  ",
    )

    impact = analyze_business_impact([evidence])

    assert impact.materiality == "high"


def test_blank_materiality_is_rejected() -> None:
    evidence = Evidence.model_validate(
        {
            "evidence_id": "EV-001",
            "evidence_type": "analyst_observation",
            "source": "analyst",
            "value": {
                "business_impact": {
                    "status": "confirmed",
                    "description": "Revenue reporting is affected.",
                    "materiality": "   ",
                }
            },
        }
    )

    with pytest.raises(
        BusinessImpactAnalysisError,
        match="invalid business_impact",
    ):
        analyze_business_impact([evidence])


def test_processes_and_consumers_are_trimmed() -> None:
    evidence = make_evidence(
        affected_processes=["  revenue reporting  "],
        affected_consumers=["  finance  "],
    )

    impact = analyze_business_impact([evidence])

    assert impact.affected_processes == ["revenue reporting"]
    assert impact.affected_consumers == ["finance"]


@pytest.mark.parametrize(
    "field_name",
    [
        "affected_processes",
        "affected_consumers",
    ],
)
def test_blank_affected_values_are_rejected(
    field_name: str,
) -> None:
    impact = {
        "status": "confirmed",
        "description": "Revenue reporting is affected.",
        field_name: ["   "],
    }

    evidence = Evidence.model_validate(
        {
            "evidence_id": "EV-001",
            "evidence_type": "analyst_observation",
            "source": "analyst",
            "value": {
                "business_impact": impact,
            },
        }
    )

    with pytest.raises(
        BusinessImpactAnalysisError,
        match="invalid business_impact",
    ):
        analyze_business_impact([evidence])


def test_extra_business_impact_fields_are_rejected() -> None:
    evidence = Evidence.model_validate(
        {
            "evidence_id": "EV-001",
            "evidence_type": "analyst_observation",
            "source": "analyst",
            "value": {
                "business_impact": {
                    "status": "confirmed",
                    "description": "Revenue reporting is affected.",
                    "unexpected": True,
                }
            },
        }
    )

    with pytest.raises(
        BusinessImpactAnalysisError,
        match="invalid business_impact",
    ):
        analyze_business_impact([evidence])


def test_result_preserves_supporting_evidence_order() -> None:
    evidence = [
        make_evidence(
            "EV-003",
            status="potential",
            evidence_type="business_rule",
            description="First potential impact.",
        ),
        make_evidence(
            "EV-001",
            status="potential",
            evidence_type="business_rule",
            description="Second potential impact.",
        ),
        make_evidence(
            "EV-002",
            status="potential",
            evidence_type="business_rule",
            description="Third potential impact.",
        ),
    ]

    impact = analyze_business_impact(evidence)

    assert impact.supporting_evidence == [
        "EV-003",
        "EV-001",
        "EV-002",
    ]


def test_same_input_produces_same_result() -> None:
    evidence = [
        make_evidence(
            "EV-001",
            affected_processes=["revenue reporting"],
        ),
        make_evidence(
            "EV-002",
            description="Sales analytics is affected.",
            affected_processes=["sales analytics"],
        ),
    ]

    first = analyze_business_impact(evidence)
    second = analyze_business_impact(evidence)

    assert first == second


def test_business_impact_domain_contract_is_used() -> None:
    evidence = make_evidence()

    impact = analyze_business_impact([evidence])

    assert isinstance(impact, BusinessImpact)


def test_collector_and_business_impact_integration() -> None:
    evidence = collect_evidence(
        [
            {
                "evidence_id": " EV-BIZ-001 ",
                "evidence_type": "analyst_observation",
                "source": " business-analyst ",
                "value": {
                    "business_impact": {
                        "status": "confirmed",
                        "description": ("Revenue reporting is affected."),
                        "affected_processes": [
                            "revenue reporting",
                        ],
                    }
                },
            }
        ]
    )

    impact = analyze_business_impact(evidence)

    assert impact.status.value == "confirmed"
    assert impact.supporting_evidence == ["EV-BIZ-001"]
    assert impact.affected_processes == ["revenue reporting"]
