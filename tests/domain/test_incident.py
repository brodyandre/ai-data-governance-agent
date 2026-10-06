"""Tests for the IncidentInput domain model."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from ai_data_governance_agent.domain import (
    Evidence,
    IncidentInput,
    Severity,
)


def minimal_incident_payload() -> dict[str, object]:
    """Return the smallest valid IncidentInput payload."""
    return {
        "incident_id": "DE-101",
        "title": "Silver layer record divergence",
        "description": "Raw and silver record counts do not reconcile.",
        "source_system": "lakehouse-pipeline",
        "detected_at": "2026-10-05T20:00:00Z",
        "evidence": [],
    }


def evidence_payload(
    evidence_id: str = "EV-001",
) -> dict[str, object]:
    """Return a valid evidence payload."""
    return {
        "evidence_id": evidence_id,
        "evidence_type": "reconciliation_result",
        "source": "pipeline-report",
        "value": {
            "raw_count": 400,
            "silver_count": 388,
        },
        "reliability": "high",
    }


def test_minimal_incident_is_valid() -> None:
    """An incident with only required fields must be accepted."""
    incident = IncidentInput(**minimal_incident_payload())

    assert incident.incident_id == "DE-101"
    assert incident.title == "Silver layer record divergence"
    assert incident.source_system == "lakehouse-pipeline"
    assert isinstance(incident.detected_at, datetime)
    assert incident.evidence == []
    assert incident.affected_datasets == []
    assert incident.tags == []
    assert incident.initial_severity is None


def test_empty_evidence_collection_is_structurally_valid() -> None:
    """Evidence may be empty even though the field itself is required."""
    incident = IncidentInput(**minimal_incident_payload())

    assert incident.evidence == []


def test_complete_incident_is_valid() -> None:
    """All documented fields must be accepted together."""
    incident = IncidentInput(
        incident_id="DE-101",
        title="Silver layer record divergence",
        description="Record counts between raw and silver layers do not reconcile.",
        source_system="lakehouse-pipeline",
        detected_at="2026-10-05T20:00:00Z",
        evidence=[evidence_payload()],
        affected_datasets=["orders", "order_items"],
        reported_by="data-quality-monitor",
        business_context="Sales analytics pipeline",
        expected_behavior=("Valid raw records should be represented in the silver layer."),
        observed_behavior=("Some records were rejected during data quality validation."),
        initial_severity="high",
        tags=["data-quality", "reconciliation", "silver-layer"],
    )

    assert incident.initial_severity is Severity.HIGH
    assert incident.affected_datasets == ["orders", "order_items"]
    assert incident.reported_by == "data-quality-monitor"
    assert incident.business_context == "Sales analytics pipeline"
    assert incident.tags == [
        "data-quality",
        "reconciliation",
        "silver-layer",
    ]

    assert len(incident.evidence) == 1
    assert isinstance(incident.evidence[0], Evidence)
    assert incident.evidence[0].evidence_id == "EV-001"


@pytest.mark.parametrize(
    "required_field",
    [
        "incident_id",
        "title",
        "description",
        "source_system",
        "detected_at",
        "evidence",
    ],
)
def test_required_fields_cannot_be_omitted(required_field: str) -> None:
    """Every documented required field must be present."""
    payload = minimal_incident_payload()
    payload.pop(required_field)

    with pytest.raises(ValidationError):
        IncidentInput(**payload)


@pytest.mark.parametrize(
    "field_name",
    [
        "incident_id",
        "title",
        "description",
        "source_system",
    ],
)
@pytest.mark.parametrize(
    "blank_value",
    ["", " ", "   ", "\t", "\n"],
)
def test_required_text_fields_reject_blank_values(
    field_name: str,
    blank_value: str,
) -> None:
    """Required textual fields must reject whitespace-only values."""
    payload = minimal_incident_payload()
    payload[field_name] = blank_value

    with pytest.raises(ValidationError):
        IncidentInput(**payload)


def test_required_text_fields_are_trimmed() -> None:
    """Required textual fields must remove surrounding whitespace."""
    incident = IncidentInput(
        incident_id="  DE-101  ",
        title="  Silver layer record divergence  ",
        description="  Raw and silver counts differ.  ",
        source_system="  lakehouse-pipeline  ",
        detected_at="2026-10-05T20:00:00Z",
        evidence=[],
    )

    assert incident.incident_id == "DE-101"
    assert incident.title == "Silver layer record divergence"
    assert incident.description == "Raw and silver counts differ."
    assert incident.source_system == "lakehouse-pipeline"


def test_incident_id_casing_is_preserved() -> None:
    """Incident identifiers must not be semantically rewritten."""
    incident = IncidentInput(
        incident_id="de-101",
        title="Test incident",
        description="Test description",
        source_system="test-system",
        detected_at="2026-10-05T20:00:00Z",
        evidence=[],
    )

    assert incident.incident_id == "de-101"


def test_valid_iso_datetime_is_parsed() -> None:
    """A valid ISO 8601 detection timestamp must be parsed."""
    incident = IncidentInput(**minimal_incident_payload())

    assert isinstance(incident.detected_at, datetime)
    assert incident.detected_at.isoformat() == "2026-10-05T20:00:00+00:00"


@pytest.mark.parametrize(
    "detected_at",
    [
        "yesterday",
        "yesterday evening",
        "not-a-datetime",
    ],
)
def test_invalid_detection_timestamp_is_rejected(
    detected_at: str,
) -> None:
    """Malformed detection timestamps must be rejected."""
    payload = minimal_incident_payload()
    payload["detected_at"] = detected_at

    with pytest.raises(ValidationError):
        IncidentInput(**payload)


def test_evidence_payloads_are_converted_to_evidence_models() -> None:
    """Nested evidence dictionaries must become Evidence models."""
    payload = minimal_incident_payload()
    payload["evidence"] = [evidence_payload()]

    incident = IncidentInput(**payload)

    assert len(incident.evidence) == 1
    assert isinstance(incident.evidence[0], Evidence)
    assert incident.evidence[0].evidence_id == "EV-001"


def test_existing_evidence_model_is_accepted() -> None:
    """Already validated Evidence objects must be accepted."""
    evidence = Evidence(**evidence_payload())

    payload = minimal_incident_payload()
    payload["evidence"] = [evidence]

    incident = IncidentInput(**payload)

    assert incident.evidence == [evidence]


def test_invalid_nested_evidence_is_rejected() -> None:
    """Invalid Evidence structures must fail IncidentInput validation."""
    payload = minimal_incident_payload()
    payload["evidence"] = [
        {
            "evidence_id": "EV-001",
            "evidence_type": "unsupported_type",
            "source": "pipeline-report",
        }
    ]

    with pytest.raises(ValidationError):
        IncidentInput(**payload)


def test_duplicate_evidence_ids_are_rejected() -> None:
    """Evidence identifiers must be unique inside one incident."""
    payload = minimal_incident_payload()
    payload["evidence"] = [
        evidence_payload("EV-001"),
        evidence_payload("EV-001"),
    ]

    with pytest.raises(
        ValidationError,
        match="duplicate evidence_id values are not allowed: EV-001",
    ):
        IncidentInput(**payload)


def test_duplicates_are_detected_after_evidence_id_trimming() -> None:
    """Normalized Evidence IDs must participate in duplicate detection."""
    payload = minimal_incident_payload()
    payload["evidence"] = [
        evidence_payload("EV-001"),
        evidence_payload("  EV-001  "),
    ]

    with pytest.raises(
        ValidationError,
        match="duplicate evidence_id values are not allowed: EV-001",
    ):
        IncidentInput(**payload)


def test_evidence_ids_remain_case_sensitive() -> None:
    """Evidence identifiers differing only by case remain distinct."""
    payload = minimal_incident_payload()
    payload["evidence"] = [
        evidence_payload("EV-001"),
        evidence_payload("ev-001"),
    ]

    incident = IncidentInput(**payload)

    assert [item.evidence_id for item in incident.evidence] == [
        "EV-001",
        "ev-001",
    ]


def test_multiple_duplicate_ids_are_reported_deterministically() -> None:
    """Duplicate IDs must be reported in encounter order."""
    payload = minimal_incident_payload()
    payload["evidence"] = [
        evidence_payload("EV-001"),
        evidence_payload("EV-002"),
        evidence_payload("EV-001"),
        evidence_payload("EV-003"),
        evidence_payload("EV-002"),
    ]

    with pytest.raises(
        ValidationError,
        match=("duplicate evidence_id values are not allowed: EV-001, EV-002"),
    ):
        IncidentInput(**payload)


@pytest.mark.parametrize(
    "severity",
    [
        "low",
        "medium",
        "high",
        "critical",
    ],
)
def test_valid_initial_severity_is_accepted(severity: str) -> None:
    """Every documented Severity value must be accepted."""
    payload = minimal_incident_payload()
    payload["initial_severity"] = severity

    incident = IncidentInput(**payload)

    assert incident.initial_severity is Severity(severity)


@pytest.mark.parametrize(
    "severity",
    [
        "HIGH",
        "Critical",
        "urgent",
        "unknown",
    ],
)
def test_invalid_initial_severity_is_rejected(severity: str) -> None:
    """Unsupported initial severity values must fail validation."""
    payload = minimal_incident_payload()
    payload["initial_severity"] = severity

    with pytest.raises(ValidationError):
        IncidentInput(**payload)


def test_optional_fields_may_be_omitted() -> None:
    """All documented optional fields must have safe defaults."""
    incident = IncidentInput(**minimal_incident_payload())

    assert incident.affected_datasets == []
    assert incident.reported_by is None
    assert incident.business_context is None
    assert incident.expected_behavior is None
    assert incident.observed_behavior is None
    assert incident.initial_severity is None
    assert incident.tags == []


def test_mutable_list_defaults_are_not_shared() -> None:
    """Incident instances must not share mutable list defaults."""
    incident_a = IncidentInput(**minimal_incident_payload())

    payload_b = minimal_incident_payload()
    payload_b["incident_id"] = "DE-102"
    incident_b = IncidentInput(**payload_b)

    incident_a.affected_datasets.append("orders")
    incident_a.tags.append("data-quality")

    assert incident_a.affected_datasets == ["orders"]
    assert incident_a.tags == ["data-quality"]
    assert incident_b.affected_datasets == []
    assert incident_b.tags == []

    assert incident_a.affected_datasets is not incident_b.affected_datasets
    assert incident_a.tags is not incident_b.tags


def test_extra_top_level_fields_are_rejected() -> None:
    """Undocumented top-level fields must be rejected."""
    payload = minimal_incident_payload()
    payload["confidence"] = 0.95

    with pytest.raises(ValidationError):
        IncidentInput(**payload)


def test_serialization_is_predictable() -> None:
    """JSON-mode serialization must preserve the public contract."""
    incident = IncidentInput(
        incident_id="DE-101",
        title="Silver layer record divergence",
        description="Raw and silver record counts do not reconcile.",
        source_system="lakehouse-pipeline",
        detected_at="2026-10-05T20:00:00Z",
        evidence=[evidence_payload()],
        affected_datasets=["orders", "order_items"],
        initial_severity="high",
        tags=["data-quality", "reconciliation"],
    )

    serialized = incident.model_dump(mode="json")

    assert serialized["incident_id"] == "DE-101"
    assert serialized["detected_at"] == "2026-10-05T20:00:00Z"
    assert serialized["initial_severity"] == "high"
    assert serialized["affected_datasets"] == ["orders", "order_items"]
    assert serialized["tags"] == ["data-quality", "reconciliation"]

    assert serialized["evidence"][0]["evidence_id"] == "EV-001"
    assert serialized["evidence"][0]["evidence_type"] == "reconciliation_result"
    assert serialized["evidence"][0]["reliability"] == "high"
