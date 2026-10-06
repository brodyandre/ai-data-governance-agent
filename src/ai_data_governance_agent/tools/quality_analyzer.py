"""Deterministic data-quality analysis from structured evidence."""

from collections.abc import Iterable
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from ai_data_governance_agent.domain.enums import EvidenceType
from ai_data_governance_agent.domain.evidence import Evidence

type QualityFindingType = Literal[
    "invalid_records",
    "reconciliation_divergence",
    "missing_relationships",
    "validation_failures",
    "count_divergence",
    "integrity_inconsistencies",
]


class QualityFinding(BaseModel):
    """Represent a deterministic quality finding supported by evidence."""

    model_config = ConfigDict(extra="forbid")

    finding_type: QualityFindingType
    description: str
    supporting_evidence: list[str] = Field(min_length=1)
    details: dict[str, JsonValue] = Field(default_factory=dict)


def analyze_quality(
    evidence_items: Iterable[Evidence],
) -> list[QualityFinding]:
    """Analyze supported structured quality signals in deterministic order."""
    findings: list[QualityFinding] = []

    for evidence in evidence_items:
        value = evidence.value

        if not isinstance(value, dict):
            continue

        if evidence.evidence_type in {
            EvidenceType.DATA_QUALITY_CHECK,
            EvidenceType.VALIDATION_RESULT,
        }:
            _append_positive_count_finding(
                findings,
                evidence,
                value,
                key="invalid_rows",
                finding_type="invalid_records",
                label="invalid rows",
            )
            _append_positive_count_finding(
                findings,
                evidence,
                value,
                key="missing_relationships",
                finding_type="missing_relationships",
                label="missing relationships",
            )
            _append_positive_count_finding(
                findings,
                evidence,
                value,
                key="validation_failures",
                finding_type="validation_failures",
                label="validation failures",
            )
            _append_positive_count_finding(
                findings,
                evidence,
                value,
                key="integrity_violations",
                finding_type="integrity_inconsistencies",
                label="integrity violations",
            )

        if evidence.evidence_type is EvidenceType.RECONCILIATION_RESULT:
            _append_count_divergence(
                findings,
                evidence,
                value,
                left_key="expected_count",
                right_key="actual_count",
                finding_type="reconciliation_divergence",
            )
            _append_count_divergence(
                findings,
                evidence,
                value,
                left_key="source_count",
                right_key="target_count",
                finding_type="count_divergence",
            )
            _append_count_divergence(
                findings,
                evidence,
                value,
                left_key="raw_count",
                right_key="silver_count",
                finding_type="count_divergence",
            )

    return findings


def _append_positive_count_finding(
    findings: list[QualityFinding],
    evidence: Evidence,
    value: dict[str, JsonValue],
    *,
    key: str,
    finding_type: QualityFindingType,
    label: str,
) -> None:
    count = value.get(key)

    if not _is_positive_int(count):
        return

    findings.append(
        QualityFinding(
            finding_type=finding_type,
            description=f"Evidence reports {count} {label}.",
            supporting_evidence=[evidence.evidence_id],
            details={key: count},
        )
    )


def _append_count_divergence(
    findings: list[QualityFinding],
    evidence: Evidence,
    value: dict[str, JsonValue],
    *,
    left_key: str,
    right_key: str,
    finding_type: QualityFindingType,
) -> None:
    left_value = value.get(left_key)
    right_value = value.get(right_key)

    if not _is_non_negative_int(left_value):
        return

    if not _is_non_negative_int(right_value):
        return

    if left_value == right_value:
        return

    findings.append(
        QualityFinding(
            finding_type=finding_type,
            description=(f"{left_key}={left_value} differs from {right_key}={right_value}."),
            supporting_evidence=[evidence.evidence_id],
            details={
                left_key: left_value,
                right_key: right_value,
                "absolute_difference": abs(left_value - right_value),
            },
        )
    )


def _is_positive_int(value: JsonValue | None) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _is_non_negative_int(value: JsonValue | None) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


__all__ = [
    "QualityFinding",
    "QualityFindingType",
    "analyze_quality",
]
