"""Tests for the Evidence domain model."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from ai_data_governance_agent.domain import (
    Evidence,
    EvidenceReliability,
    EvidenceType,
)


def minimal_evidence_payload() -> dict[str, object]:
    """Return the smallest valid Evidence payload."""
    return {
        "evidence_id": "EV-001",
        "evidence_type": "pipeline_report",
        "source": "sales-pipeline",
    }


def test_minimal_evidence_is_valid() -> None:
    """Only the three required fields must be necessary."""
    evidence = Evidence(**minimal_evidence_payload())

    assert evidence.evidence_id == "EV-001"
    assert evidence.evidence_type is EvidenceType.PIPELINE_REPORT
    assert evidence.source == "sales-pipeline"
    assert evidence.description is None
    assert evidence.value is None
    assert evidence.collected_at is None
    assert evidence.reliability is None
    assert evidence.metadata == {}


def test_complete_evidence_is_valid() -> None:
    """All documented fields must be accepted together."""
    evidence = Evidence(
        evidence_id="EV-001",
        evidence_type="reconciliation_result",
        source="pipeline-report",
        description="Raw and silver record counts differ.",
        value={
            "raw_count": 400,
            "silver_count": 388,
            "difference": 12,
        },
        collected_at="2026-10-05T20:00:00Z",
        reliability="high",
        metadata={
            "dataset": "orders",
            "layer": "silver",
        },
    )

    assert evidence.evidence_type is EvidenceType.RECONCILIATION_RESULT
    assert evidence.reliability is EvidenceReliability.HIGH
    assert isinstance(evidence.collected_at, datetime)


def test_evidence_id_is_required() -> None:
    """Evidence without evidence_id must be rejected."""
    payload = minimal_evidence_payload()
    payload.pop("evidence_id")

    with pytest.raises(ValidationError):
        Evidence(**payload)


@pytest.mark.parametrize("evidence_id", ["", " ", "   ", "\t", "\n"])
def test_evidence_id_rejects_blank_values(evidence_id: str) -> None:
    """Blank evidence identifiers must be rejected."""
    payload = minimal_evidence_payload()
    payload["evidence_id"] = evidence_id

    with pytest.raises(ValidationError):
        Evidence(**payload)


def test_evidence_id_is_trimmed_without_semantic_rewrite() -> None:
    """Only surrounding whitespace may be normalized."""
    evidence = Evidence(
        evidence_id="  ev-001  ",
        evidence_type="metric",
        source="monitoring",
    )

    assert evidence.evidence_id == "ev-001"


def test_source_is_required() -> None:
    """Evidence without source must be rejected."""
    payload = minimal_evidence_payload()
    payload.pop("source")

    with pytest.raises(ValidationError):
        Evidence(**payload)


@pytest.mark.parametrize("source", ["", " ", "   ", "\t", "\n"])
def test_source_rejects_blank_values(source: str) -> None:
    """Blank evidence sources must be rejected."""
    payload = minimal_evidence_payload()
    payload["source"] = source

    with pytest.raises(ValidationError):
        Evidence(**payload)


def test_source_is_trimmed_without_semantic_rewrite() -> None:
    """Source normalization must only remove surrounding whitespace."""
    evidence = Evidence(
        evidence_id="EV-001",
        evidence_type="metric",
        source="  Pipeline Report  ",
    )

    assert evidence.source == "Pipeline Report"


@pytest.mark.parametrize(
    "evidence_type",
    [
        "data_quality_check",
        "pipeline_report",
        "validation_result",
        "reconciliation_result",
        "log",
        "business_rule",
        "governance_policy",
        "analyst_observation",
        "metric",
        "dataset_sample",
    ],
)
def test_valid_evidence_types_are_accepted(evidence_type: str) -> None:
    """Every documented EvidenceType value must be accepted."""
    evidence = Evidence(
        evidence_id="EV-001",
        evidence_type=evidence_type,
        source="test-source",
    )

    assert evidence.evidence_type.value == evidence_type


@pytest.mark.parametrize(
    "evidence_type",
    [
        "report",
        "DataQuality",
        "RECONCILIATION_RESULT",
        "unknown_type",
        "pipeline-report",
    ],
)
def test_invalid_evidence_types_are_rejected(evidence_type: str) -> None:
    """Unsupported or incorrectly cased EvidenceType values must fail."""
    with pytest.raises(ValidationError):
        Evidence(
            evidence_id="EV-001",
            evidence_type=evidence_type,
            source="test-source",
        )


@pytest.mark.parametrize("reliability", ["low", "medium", "high"])
def test_valid_reliability_values_are_accepted(reliability: str) -> None:
    """Every documented reliability value must be accepted."""
    evidence = Evidence(
        evidence_id="EV-001",
        evidence_type="metric",
        source="monitoring",
        reliability=reliability,
    )

    assert evidence.reliability is EvidenceReliability(reliability)


@pytest.mark.parametrize(
    "reliability",
    ["trusted", "unknown", "HIGH", "Medium"],
)
def test_invalid_reliability_values_are_rejected(reliability: str) -> None:
    """Unsupported reliability values must be rejected."""
    with pytest.raises(ValidationError):
        Evidence(
            evidence_id="EV-001",
            evidence_type="metric",
            source="monitoring",
            reliability=reliability,
        )


def test_reliability_may_be_omitted() -> None:
    """Reliability may remain unevaluated."""
    evidence = Evidence(**minimal_evidence_payload())

    assert evidence.reliability is None


def test_description_may_be_omitted() -> None:
    """Description must remain optional."""
    evidence = Evidence(**minimal_evidence_payload())

    assert evidence.description is None


def test_description_is_trimmed() -> None:
    """Description must remove only surrounding whitespace."""
    evidence = Evidence(
        **minimal_evidence_payload(),
        description="  Record counts differ.  ",
    )

    assert evidence.description == "Record counts differ."


@pytest.mark.parametrize("description", ["", " ", "   ", "\t", "\n"])
def test_blank_description_is_rejected(description: str) -> None:
    """Whitespace-only descriptions must be rejected."""
    with pytest.raises(ValidationError):
        Evidence(
            **minimal_evidence_payload(),
            description=description,
        )


@pytest.mark.parametrize(
    "value",
    [
        "orders SOURCE=400 TARGET=388",
        30,
        0.075,
        True,
        ["ORD-000038", "ORD-000144"],
        {"raw_count": 400, "silver_count": 388},
        None,
    ],
)
def test_value_accepts_json_compatible_values(value: object) -> None:
    """Evidence value must support representative JSON-compatible values."""
    evidence = Evidence(
        **minimal_evidence_payload(),
        value=value,
    )

    assert evidence.value == value


@pytest.mark.parametrize(
    "value",
    [
        {"nested": {"count": 12}},
        {"items": [1, 2, 3]},
        [True, None, "value", 12],
    ],
)
def test_value_accepts_nested_json_structures(value: object) -> None:
    """Nested JSON-compatible structures must remain supported."""
    evidence = Evidence(
        **minimal_evidence_payload(),
        value=value,
    )

    assert evidence.value == value


def test_valid_iso_datetime_is_parsed() -> None:
    """Valid ISO 8601 datetime strings must be parsed."""
    evidence = Evidence(
        **minimal_evidence_payload(),
        collected_at="2026-10-05T20:00:00Z",
    )

    assert isinstance(evidence.collected_at, datetime)
    assert evidence.collected_at.isoformat() == "2026-10-05T20:00:00+00:00"


def test_valid_datetime_with_offset_is_parsed() -> None:
    """Valid ISO datetimes with explicit offsets must be accepted."""
    evidence = Evidence(
        **minimal_evidence_payload(),
        collected_at="2026-10-05T17:00:00-03:00",
    )

    assert evidence.collected_at is not None
    assert evidence.collected_at.utcoffset() is not None


@pytest.mark.parametrize(
    "collected_at",
    [
        "yesterday",
        "yesterday evening",
        "not-a-datetime",
    ],
)
def test_invalid_datetime_is_rejected(collected_at: str) -> None:
    """Malformed datetime strings must be rejected."""
    with pytest.raises(ValidationError):
        Evidence(
            **minimal_evidence_payload(),
            collected_at=collected_at,
        )


def test_metadata_defaults_to_empty_dict() -> None:
    """Omitted metadata must produce an empty dictionary."""
    evidence = Evidence(**minimal_evidence_payload())

    assert evidence.metadata == {}


def test_metadata_default_is_not_shared() -> None:
    """Evidence instances must not share mutable metadata."""
    evidence_a = Evidence(**minimal_evidence_payload())
    evidence_b = Evidence(
        evidence_id="EV-002",
        evidence_type="metric",
        source="monitoring",
    )

    evidence_a.metadata["dataset"] = "orders"

    assert evidence_a.metadata == {"dataset": "orders"}
    assert evidence_b.metadata == {}
    assert evidence_a.metadata is not evidence_b.metadata


def test_metadata_accepts_json_compatible_object() -> None:
    """Metadata must support nested JSON-compatible objects."""
    metadata = {
        "pipeline_run_id": "run-20261005-001",
        "failed_records": 30,
        "details": {
            "dataset": "orders",
            "layers": ["raw", "silver"],
        },
    }

    evidence = Evidence(
        **minimal_evidence_payload(),
        metadata=metadata,
    )

    assert evidence.metadata == metadata


def test_extra_top_level_fields_are_rejected() -> None:
    """Undocumented top-level fields must fail validation."""
    payload = minimal_evidence_payload()
    payload["confidence"] = 0.95

    with pytest.raises(ValidationError):
        Evidence(**payload)


def test_enum_values_serialize_as_strings() -> None:
    """Enum fields must serialize using their documented string values."""
    evidence = Evidence(
        evidence_id="EV-001",
        evidence_type=EvidenceType.RECONCILIATION_RESULT,
        source="pipeline-report",
        reliability=EvidenceReliability.HIGH,
    )

    serialized = evidence.model_dump(mode="json")

    assert serialized["evidence_type"] == "reconciliation_result"
    assert serialized["reliability"] == "high"


def test_serialization_is_json_compatible_and_predictable() -> None:
    """JSON-mode serialization must preserve the documented structure."""
    evidence = Evidence(
        evidence_id="  EV-001  ",
        evidence_type="reconciliation_result",
        source="  pipeline-report  ",
        description="  Raw and silver record counts differ.  ",
        value={
            "raw_count": 400,
            "silver_count": 388,
            "difference": 12,
        },
        collected_at="2026-10-05T20:00:00Z",
        reliability="high",
        metadata={"dataset": "orders"},
    )

    assert evidence.model_dump(mode="json") == {
        "evidence_id": "EV-001",
        "evidence_type": "reconciliation_result",
        "source": "pipeline-report",
        "description": "Raw and silver record counts differ.",
        "value": {
            "raw_count": 400,
            "silver_count": 388,
            "difference": 12,
        },
        "collected_at": "2026-10-05T20:00:00Z",
        "reliability": "high",
        "metadata": {"dataset": "orders"},
    }


def test_duplicate_ids_are_not_checked_by_individual_model() -> None:
    """Duplicate evidence IDs remain a collection-level responsibility."""
    evidence_a = Evidence(**minimal_evidence_payload())
    evidence_b = Evidence(**minimal_evidence_payload())

    assert evidence_a.evidence_id == evidence_b.evidence_id == "EV-001"
