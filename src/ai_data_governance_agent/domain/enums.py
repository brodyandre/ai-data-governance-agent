"""Normalized domain enums for the AI Data Governance Agent."""

from enum import StrEnum


class Severity(StrEnum):
    """Normalized incident severity."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentClassification(StrEnum):
    """Normalized incident classification."""

    DATA_QUALITY = "data_quality"
    SCHEMA = "schema"
    INTEGRITY = "integrity"
    RECONCILIATION = "reconciliation"
    FRESHNESS = "freshness"
    PIPELINE_FAILURE = "pipeline_failure"
    GOVERNANCE = "governance"
    UNKNOWN = "unknown"


class EvidenceType(StrEnum):
    """Normalized evidence type."""

    DATA_QUALITY_CHECK = "data_quality_check"
    PIPELINE_REPORT = "pipeline_report"
    VALIDATION_RESULT = "validation_result"
    RECONCILIATION_RESULT = "reconciliation_result"
    LOG = "log"
    BUSINESS_RULE = "business_rule"
    GOVERNANCE_POLICY = "governance_policy"
    ANALYST_OBSERVATION = "analyst_observation"
    METRIC = "metric"
    DATASET_SAMPLE = "dataset_sample"


class EvidenceReliability(StrEnum):
    """Normalized evidence reliability."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class BusinessImpactStatus(StrEnum):
    """Normalized business impact status."""

    CONFIRMED = "confirmed"
    POTENTIAL = "potential"
    UNKNOWN = "unknown"


class ActionPriority(StrEnum):
    """Normalized recommended-action priority."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


__all__ = [
    "ActionPriority",
    "BusinessImpactStatus",
    "EvidenceReliability",
    "EvidenceType",
    "IncidentClassification",
    "Severity",
]
