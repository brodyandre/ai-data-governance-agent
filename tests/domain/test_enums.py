"""Tests for normalized domain enums."""

import json
import re
from enum import StrEnum

import pytest

from ai_data_governance_agent.domain import (
    ActionPriority,
    BusinessImpactStatus,
    EvidenceReliability,
    EvidenceType,
    IncidentClassification,
    Severity,
)

ALL_ENUMS = (
    Severity,
    IncidentClassification,
    EvidenceType,
    EvidenceReliability,
    BusinessImpactStatus,
    ActionPriority,
)

EXPECTED_MEMBERS: dict[type[StrEnum], dict[str, str]] = {
    Severity: {
        "LOW": "low",
        "MEDIUM": "medium",
        "HIGH": "high",
        "CRITICAL": "critical",
    },
    IncidentClassification: {
        "DATA_QUALITY": "data_quality",
        "SCHEMA": "schema",
        "INTEGRITY": "integrity",
        "RECONCILIATION": "reconciliation",
        "FRESHNESS": "freshness",
        "PIPELINE_FAILURE": "pipeline_failure",
        "GOVERNANCE": "governance",
        "UNKNOWN": "unknown",
    },
    EvidenceType: {
        "DATA_QUALITY_CHECK": "data_quality_check",
        "PIPELINE_REPORT": "pipeline_report",
        "VALIDATION_RESULT": "validation_result",
        "RECONCILIATION_RESULT": "reconciliation_result",
        "LOG": "log",
        "BUSINESS_RULE": "business_rule",
        "GOVERNANCE_POLICY": "governance_policy",
        "ANALYST_OBSERVATION": "analyst_observation",
        "METRIC": "metric",
        "DATASET_SAMPLE": "dataset_sample",
    },
    EvidenceReliability: {
        "LOW": "low",
        "MEDIUM": "medium",
        "HIGH": "high",
    },
    BusinessImpactStatus: {
        "CONFIRMED": "confirmed",
        "POTENTIAL": "potential",
        "UNKNOWN": "unknown",
    },
    ActionPriority: {
        "LOW": "low",
        "MEDIUM": "medium",
        "HIGH": "high",
        "URGENT": "urgent",
    },
}


@pytest.mark.parametrize("enum_cls", ALL_ENUMS)
def test_enum_uses_str_enum(enum_cls: type[StrEnum]) -> None:
    """Every domain enum must use Python StrEnum."""
    assert issubclass(enum_cls, StrEnum)


@pytest.mark.parametrize("enum_cls", ALL_ENUMS)
def test_enum_members_match_contract(enum_cls: type[StrEnum]) -> None:
    """Enum names and serialized values must match the documented contract."""
    actual = {member.name: member.value for member in enum_cls}

    assert actual == EXPECTED_MEMBERS[enum_cls]


@pytest.mark.parametrize("enum_cls", ALL_ENUMS)
def test_all_documented_values_are_accepted(enum_cls: type[StrEnum]) -> None:
    """Every documented serialized value must create the expected enum member."""
    for member_name, serialized_value in EXPECTED_MEMBERS[enum_cls].items():
        member = enum_cls(serialized_value)

        assert member.name == member_name
        assert member.value == serialized_value


@pytest.mark.parametrize("enum_cls", ALL_ENUMS)
def test_serialized_values_use_lowercase_snake_case(
    enum_cls: type[StrEnum],
) -> None:
    """Serialized values must remain lowercase snake_case."""
    pattern = re.compile(r"^[a-z]+(?:_[a-z]+)*$")

    for member in enum_cls:
        assert pattern.fullmatch(member.value)


@pytest.mark.parametrize("enum_cls", ALL_ENUMS)
def test_enum_does_not_define_aliases(enum_cls: type[StrEnum]) -> None:
    """Domain enums must not contain duplicate-value aliases."""
    assert len(enum_cls.__members__) == len(list(enum_cls))


@pytest.mark.parametrize("enum_cls", ALL_ENUMS)
def test_string_representation_is_serialized_value(
    enum_cls: type[StrEnum],
) -> None:
    """String conversion must expose the stable serialized value."""
    for member in enum_cls:
        assert str(member) == member.value


@pytest.mark.parametrize(
    ("member", "expected_json"),
    [
        (Severity.HIGH, '"high"'),
        (IncidentClassification.DATA_QUALITY, '"data_quality"'),
        (EvidenceType.PIPELINE_REPORT, '"pipeline_report"'),
        (EvidenceReliability.MEDIUM, '"medium"'),
        (BusinessImpactStatus.POTENTIAL, '"potential"'),
        (ActionPriority.URGENT, '"urgent"'),
    ],
)
def test_enum_serializes_as_json_string(
    member: StrEnum,
    expected_json: str,
) -> None:
    """StrEnum values must serialize predictably as JSON strings."""
    assert json.dumps(member) == expected_json


@pytest.mark.parametrize(
    ("enum_cls", "invalid_value"),
    [
        (Severity, "HIGH"),
        (Severity, "High"),
        (Severity, "med"),
        (Severity, " high "),
        (IncidentClassification, "DATA_QUALITY"),
        (IncidentClassification, "data-quality"),
        (IncidentClassification, "dq"),
        (IncidentClassification, "security_problem"),
        (EvidenceType, "PIPELINE_REPORT"),
        (EvidenceType, "pipeline-report"),
        (EvidenceType, "validation"),
        (EvidenceReliability, "unknown"),
        (EvidenceReliability, "MEDIUM"),
        (BusinessImpactStatus, "CONFIRMED"),
        (BusinessImpactStatus, "possible"),
        (ActionPriority, "URGENT"),
        (ActionPriority, "critical"),
    ],
)
def test_invalid_values_are_rejected(
    enum_cls: type[StrEnum],
    invalid_value: str,
) -> None:
    """Unsupported values, aliases, casing, and normalization must be rejected."""
    with pytest.raises(ValueError):
        enum_cls(invalid_value)


def test_unknown_classification_is_explicit_not_fallback() -> None:
    """UNKNOWN must be explicit and must not absorb unsupported classifications."""
    assert IncidentClassification("unknown") is IncidentClassification.UNKNOWN

    with pytest.raises(ValueError):
        IncidentClassification("unsupported_incident_type")


def test_evidence_reliability_has_no_unknown_member() -> None:
    """Missing reliability is represented outside the enum rather than as UNKNOWN."""
    assert "UNKNOWN" not in EvidenceReliability.__members__

    with pytest.raises(ValueError):
        EvidenceReliability("unknown")
