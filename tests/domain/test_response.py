"""Tests for structured AgentResponse domain models."""

import pytest
from pydantic import ValidationError

from ai_data_governance_agent.domain import (
    ActionPriority,
    AgentResponse,
    BusinessImpact,
    BusinessImpactStatus,
    Evidence,
    GovernanceControl,
    HypothesisStatus,
    IncidentClassification,
    RecommendedAction,
    RootCauseHypothesis,
    Severity,
)


def evidence_payload(
    evidence_id: str = "EV-001",
) -> dict[str, object]:
    """Return one valid evidence payload."""
    return {
        "evidence_id": evidence_id,
        "evidence_type": "reconciliation_result",
        "source": "pipeline-report",
        "description": "Raw and silver record counts differ.",
        "value": {
            "raw_count": 400,
            "silver_count": 388,
        },
        "reliability": "high",
    }


def business_impact_payload() -> dict[str, object]:
    """Return a valid potential business impact payload."""
    return {
        "status": "potential",
        "description": "Downstream sales metrics may be incomplete.",
        "affected_processes": ["sales analytics"],
        "affected_consumers": ["commercial reporting"],
        "materiality": "medium",
        "supporting_evidence": ["EV-001"],
    }


def minimal_agent_response_payload() -> dict[str, object]:
    """Return the smallest representative AgentResponse payload."""
    return {
        "incident_id": "DE-101",
        "classification": "data_quality",
        "severity": "high",
        "executive_summary": ("Data Quality validation removed records from the silver layer."),
        "evidence": [evidence_payload()],
        "business_impact": business_impact_payload(),
        "confidence": 0.9,
        "human_review_required": False,
    }


def test_hypothesis_status_contains_expected_values() -> None:
    """DG-104 must formalize the documented hypothesis states."""
    assert [member.value for member in HypothesisStatus] == [
        "suspected",
        "probable",
        "confirmed",
        "rejected",
    ]


@pytest.mark.parametrize(
    "value",
    [
        "SUSPECTED",
        "Probable",
        "unknown",
        "likely",
    ],
)
def test_invalid_hypothesis_status_is_rejected(value: str) -> None:
    """Hypothesis status must remain case-sensitive and explicit."""
    with pytest.raises(ValueError):
        HypothesisStatus(value)


def test_business_impact_is_valid() -> None:
    """A documented business impact structure must be accepted."""
    impact = BusinessImpact(**business_impact_payload())

    assert impact.status is BusinessImpactStatus.POTENTIAL
    assert impact.description == "Downstream sales metrics may be incomplete."
    assert impact.materiality == "medium"
    assert impact.supporting_evidence == ["EV-001"]


def test_unknown_business_impact_can_have_no_supporting_evidence() -> None:
    """Unknown impact must remain representable without fabricated evidence."""
    impact = BusinessImpact(
        status="unknown",
        description="Business impact has not been established.",
    )

    assert impact.status is BusinessImpactStatus.UNKNOWN
    assert impact.supporting_evidence == []


def test_confirmed_business_impact_requires_supporting_evidence() -> None:
    """Confirmed business impact must have structural evidence support."""
    with pytest.raises(
        ValidationError,
        match="confirmed business impact requires supporting evidence",
    ):
        BusinessImpact(
            status="confirmed",
            description="Revenue reporting is incomplete.",
        )


def test_confirmed_business_impact_with_evidence_is_valid() -> None:
    """Confirmed business impact may be represented when evidence is referenced."""
    impact = BusinessImpact(
        status="confirmed",
        description="Revenue reporting is incomplete.",
        supporting_evidence=["EV-001"],
    )

    assert impact.status is BusinessImpactStatus.CONFIRMED


def test_business_impact_rejects_invalid_status() -> None:
    """Unsupported business impact states must fail validation."""
    with pytest.raises(ValidationError):
        BusinessImpact(
            status="likely",
            description="Potential downstream impact.",
        )


def test_business_impact_rejects_extra_fields() -> None:
    """Undocumented business impact fields must be rejected."""
    payload = business_impact_payload()
    payload["confidence"] = 0.9

    with pytest.raises(ValidationError):
        BusinessImpact(**payload)


def test_root_cause_hypothesis_is_valid() -> None:
    """A documented root-cause hypothesis must be accepted."""
    hypothesis = RootCauseHypothesis(
        description="Invalid quantities caused validation failures.",
        supporting_evidence=["EV-001"],
        confidence=0.95,
        status="probable",
    )

    assert hypothesis.status is HypothesisStatus.PROBABLE
    assert hypothesis.confidence == 0.95


@pytest.mark.parametrize("confidence", [0.0, 1.0])
def test_hypothesis_confidence_accepts_boundaries(
    confidence: float,
) -> None:
    """Hypothesis confidence must accept both documented boundaries."""
    hypothesis = RootCauseHypothesis(
        description="Possible root cause.",
        confidence=confidence,
        status="suspected",
    )

    assert hypothesis.confidence == confidence


@pytest.mark.parametrize("confidence", [-0.01, 1.01, -1.0, 2.0])
def test_hypothesis_confidence_rejects_out_of_range_values(
    confidence: float,
) -> None:
    """Hypothesis confidence must remain between zero and one."""
    with pytest.raises(ValidationError):
        RootCauseHypothesis(
            description="Possible root cause.",
            confidence=confidence,
            status="suspected",
        )


def test_confirmed_hypothesis_requires_supporting_evidence() -> None:
    """A confirmed root cause cannot be structurally unsupported."""
    with pytest.raises(
        ValidationError,
        match="confirmed root-cause hypothesis requires supporting evidence",
    ):
        RootCauseHypothesis(
            description="The upstream quantity rule caused the incident.",
            confidence=1.0,
            status="confirmed",
        )


def test_confirmed_hypothesis_with_evidence_is_valid() -> None:
    """A confirmed hypothesis may reference one or more evidence IDs."""
    hypothesis = RootCauseHypothesis(
        description="The upstream quantity rule caused the incident.",
        supporting_evidence=["EV-001"],
        confidence=1.0,
        status="confirmed",
    )

    assert hypothesis.status is HypothesisStatus.CONFIRMED


def test_recommended_action_is_valid() -> None:
    """A consultative recommended action must be representable."""
    action = RecommendedAction(
        description="Review rejected records.",
        priority="high",
        rationale="Rejected records may affect downstream analytics.",
        requires_human_approval=False,
        supporting_evidence=["EV-001"],
    )

    assert action.priority is ActionPriority.HIGH
    assert action.requires_human_approval is False


@pytest.mark.parametrize(
    "priority",
    ["low", "medium", "high", "urgent"],
)
def test_recommended_action_accepts_valid_priorities(
    priority: str,
) -> None:
    """All documented action priorities must be accepted."""
    action = RecommendedAction(
        description="Investigate the incident.",
        priority=priority,
        rationale="Further analysis is required.",
        requires_human_approval=True,
    )

    assert action.priority is ActionPriority(priority)


@pytest.mark.parametrize(
    "priority",
    ["critical", "immediate", "HIGH", "Urgent"],
)
def test_recommended_action_rejects_invalid_priorities(
    priority: str,
) -> None:
    """Unsupported or incorrectly cased priorities must fail."""
    with pytest.raises(ValidationError):
        RecommendedAction(
            description="Investigate the incident.",
            priority=priority,
            rationale="Further analysis is required.",
            requires_human_approval=True,
        )


def test_governance_control_is_valid() -> None:
    """A governance control must preserve its traceability fields."""
    control = GovernanceControl(
        control_id="GOV-001",
        title="Data Quality Review",
        description="Critical data quality incidents require review.",
        source="governance-policy-catalog",
        relevance="The incident affects a governed analytical dataset.",
        supporting_evidence=["EV-001"],
    )

    assert control.control_id == "GOV-001"
    assert control.supporting_evidence == ["EV-001"]


def test_governance_control_rejects_extra_fields() -> None:
    """Undocumented governance fields must be rejected."""
    with pytest.raises(ValidationError):
        GovernanceControl(
            control_id="GOV-001",
            title="Data Quality Review",
            description="Review requirement.",
            source="policy-catalog",
            relevance="Relevant to the incident.",
            supporting_evidence=[],
            unsupported=True,
        )


def test_minimal_agent_response_is_valid() -> None:
    """The required AgentResponse structure must be accepted."""
    response = AgentResponse(**minimal_agent_response_payload())

    assert response.incident_id == "DE-101"
    assert response.classification is IncidentClassification.DATA_QUALITY
    assert response.severity is Severity.HIGH
    assert response.confidence == 0.9
    assert response.human_review_required is False
    assert response.human_review_reasons == []
    assert response.root_cause_hypotheses == []
    assert response.recommended_actions == []
    assert response.governance_controls == []


def test_nested_evidence_is_parsed_as_evidence_model() -> None:
    """AgentResponse evidence payloads must become Evidence models."""
    response = AgentResponse(**minimal_agent_response_payload())

    assert isinstance(response.evidence[0], Evidence)
    assert response.evidence[0].evidence_id == "EV-001"


@pytest.mark.parametrize(
    "classification",
    [
        "data_quality",
        "schema",
        "integrity",
        "reconciliation",
        "freshness",
        "pipeline_failure",
        "governance",
        "unknown",
    ],
)
def test_agent_response_accepts_valid_classifications(
    classification: str,
) -> None:
    """All documented incident classifications must be accepted."""
    payload = minimal_agent_response_payload()
    payload["classification"] = classification

    response = AgentResponse(**payload)

    assert response.classification is IncidentClassification(classification)


@pytest.mark.parametrize(
    "classification",
    [
        "DATA_QUALITY",
        "data-quality",
        "security",
    ],
)
def test_agent_response_rejects_invalid_classifications(
    classification: str,
) -> None:
    """Unsupported classifications must fail validation."""
    payload = minimal_agent_response_payload()
    payload["classification"] = classification

    with pytest.raises(ValidationError):
        AgentResponse(**payload)


@pytest.mark.parametrize(
    "severity",
    ["low", "medium", "high", "critical"],
)
def test_agent_response_accepts_valid_severity(
    severity: str,
) -> None:
    """All documented severity values must be accepted."""
    payload = minimal_agent_response_payload()
    payload["severity"] = severity

    response = AgentResponse(**payload)

    assert response.severity is Severity(severity)


@pytest.mark.parametrize(
    "severity",
    ["HIGH", "Critical", "urgent", "unknown"],
)
def test_agent_response_rejects_invalid_severity(
    severity: str,
) -> None:
    """Unsupported severity values must fail validation."""
    payload = minimal_agent_response_payload()
    payload["severity"] = severity

    with pytest.raises(ValidationError):
        AgentResponse(**payload)


@pytest.mark.parametrize("confidence", [0.0, 0.5, 1.0])
def test_agent_response_confidence_accepts_valid_values(
    confidence: float,
) -> None:
    """Overall confidence must accept values inside the closed interval."""
    payload = minimal_agent_response_payload()
    payload["confidence"] = confidence

    response = AgentResponse(**payload)

    assert response.confidence == confidence


@pytest.mark.parametrize("confidence", [-0.01, 1.01, -1.0, 2.0])
def test_agent_response_confidence_rejects_invalid_values(
    confidence: float,
) -> None:
    """Overall confidence must remain between zero and one."""
    payload = minimal_agent_response_payload()
    payload["confidence"] = confidence

    with pytest.raises(ValidationError):
        AgentResponse(**payload)


def test_human_review_true_requires_reasons() -> None:
    """Mandatory review must include auditable reasons."""
    payload = minimal_agent_response_payload()
    payload["human_review_required"] = True
    payload["human_review_reasons"] = []

    with pytest.raises(
        ValidationError,
        match=("human_review_reasons are required when human_review_required is true"),
    ):
        AgentResponse(**payload)


def test_human_review_true_with_reasons_is_valid() -> None:
    """Mandatory human review must be representable with explicit reasons."""
    payload = minimal_agent_response_payload()
    payload["human_review_required"] = True
    payload["human_review_reasons"] = [
        "high severity",
        "potential material business impact",
    ]

    response = AgentResponse(**payload)

    assert response.human_review_required is True
    assert response.human_review_reasons == [
        "high severity",
        "potential material business impact",
    ]


def test_human_review_false_can_have_no_reasons() -> None:
    """No reasons are required when review is not mandatory."""
    response = AgentResponse(**minimal_agent_response_payload())

    assert response.human_review_required is False
    assert response.human_review_reasons == []


def test_agent_response_rejects_extra_top_level_fields() -> None:
    """Undocumented AgentResponse fields must be rejected."""
    payload = minimal_agent_response_payload()
    payload["unsupported_field"] = "value"

    with pytest.raises(ValidationError):
        AgentResponse(**payload)


def test_mutable_defaults_are_not_shared() -> None:
    """Response instances must not share mutable default collections."""
    response_a = AgentResponse(**minimal_agent_response_payload())

    payload_b = minimal_agent_response_payload()
    payload_b["incident_id"] = "DE-102"
    response_b = AgentResponse(**payload_b)

    response_a.human_review_reasons.append("manual review")
    response_a.recommended_actions.append(
        RecommendedAction(
            description="Review records.",
            priority="medium",
            rationale="Validation is required.",
            requires_human_approval=False,
        )
    )

    assert response_b.human_review_reasons == []
    assert response_b.recommended_actions == []

    assert response_a.human_review_reasons is not response_b.human_review_reasons
    assert response_a.recommended_actions is not response_b.recommended_actions


def test_full_agent_response_is_valid() -> None:
    """A complete response following the documented contract must be accepted."""
    response = AgentResponse(
        incident_id="DE-101",
        classification="data_quality",
        severity="high",
        executive_summary=(
            "Data Quality validation removed records from the silver layer "
            "and may affect downstream sales analytics."
        ),
        evidence=[evidence_payload()],
        business_impact=business_impact_payload(),
        root_cause_hypotheses=[
            {
                "description": ("Invalid item quantities caused records to fail validation."),
                "supporting_evidence": ["EV-001"],
                "confidence": 0.95,
                "status": "probable",
            }
        ],
        recommended_actions=[
            {
                "description": ("Review rejected records and validate upstream quantity rules."),
                "priority": "high",
                "rationale": ("Rejected records may cause incomplete downstream analytics."),
                "requires_human_approval": False,
                "supporting_evidence": ["EV-001"],
            }
        ],
        governance_controls=[
            {
                "control_id": "GOV-001",
                "title": "Data Quality Review",
                "description": ("Relevant data quality incidents require review."),
                "source": "governance-policy-catalog",
                "relevance": "The incident affects analytical reporting.",
                "supporting_evidence": ["EV-001"],
            }
        ],
        confidence=0.9,
        human_review_required=True,
        human_review_reasons=[
            "high severity",
            "potential material business impact",
        ],
    )

    assert response.root_cause_hypotheses[0].status is HypothesisStatus.PROBABLE
    assert response.recommended_actions[0].priority is ActionPriority.HIGH
    assert response.governance_controls[0].control_id == "GOV-001"


def test_agent_response_serialization_is_predictable() -> None:
    """JSON-mode serialization must expose stable public values."""
    response = AgentResponse(**minimal_agent_response_payload())

    serialized = response.model_dump(mode="json")

    assert serialized["incident_id"] == "DE-101"
    assert serialized["classification"] == "data_quality"
    assert serialized["severity"] == "high"
    assert serialized["confidence"] == 0.9
    assert serialized["human_review_required"] is False

    assert serialized["business_impact"]["status"] == "potential"
    assert serialized["business_impact"]["materiality"] == "medium"

    assert serialized["evidence"][0]["evidence_id"] == "EV-001"
    assert serialized["evidence"][0]["evidence_type"] == "reconciliation_result"
