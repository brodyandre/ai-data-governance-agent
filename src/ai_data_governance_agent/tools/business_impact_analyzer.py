"""Deterministic business-impact analysis from structured evidence."""

from collections.abc import Iterable

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
)

from ai_data_governance_agent.domain.enums import (
    BusinessImpactStatus,
    EvidenceType,
)
from ai_data_governance_agent.domain.evidence import Evidence
from ai_data_governance_agent.domain.response import BusinessImpact


class BusinessImpactAnalysisError(ValueError):
    """Raised when explicit business-impact evidence is malformed or unsafe."""


class _BusinessImpactSignal(BaseModel):
    """Represent one explicit business-impact signal carried by evidence."""

    model_config = ConfigDict(extra="forbid")

    status: BusinessImpactStatus
    description: str
    affected_processes: list[str] = Field(default_factory=list)
    affected_consumers: list[str] = Field(default_factory=list)
    materiality: str | None = None

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str) -> str:
        normalized = value.strip()

        if not normalized:
            raise ValueError("description must contain non-whitespace characters")

        return normalized

    @field_validator("materiality")
    @classmethod
    def validate_materiality(cls, value: str | None) -> str | None:
        if value is None:
            return None

        normalized = value.strip()

        if not normalized:
            raise ValueError("materiality must contain non-whitespace characters")

        return normalized

    @field_validator(
        "affected_processes",
        "affected_consumers",
    )
    @classmethod
    def validate_text_lists(cls, values: list[str]) -> list[str]:
        normalized: list[str] = []

        for value in values:
            item = value.strip()

            if not item:
                raise ValueError("affected values must contain non-whitespace characters")

            normalized.append(item)

        return normalized


_SUPPORTED_EVIDENCE_TYPES = {
    EvidenceType.ANALYST_OBSERVATION,
    EvidenceType.BUSINESS_RULE,
}

_UNKNOWN_DESCRIPTION = "Business impact cannot be determined from available structured evidence."


def analyze_business_impact(
    evidence_items: Iterable[Evidence],
) -> BusinessImpact:
    """Determine business impact from explicit structured evidence."""
    candidates: list[BusinessImpact] = []

    for evidence in evidence_items:
        candidate = _extract_candidate(evidence)

        if candidate is not None:
            candidates.append(candidate)

    if not candidates:
        return _unknown_business_impact()

    return _merge_candidates(candidates)


def _extract_candidate(
    evidence: Evidence,
) -> BusinessImpact | None:
    if evidence.evidence_type not in _SUPPORTED_EVIDENCE_TYPES:
        return None

    value = evidence.value

    if not isinstance(value, dict):
        return None

    raw_signal = value.get("business_impact")

    if raw_signal is None:
        return None

    if not isinstance(raw_signal, dict):
        raise BusinessImpactAnalysisError(
            f"business_impact must be an object for evidence {evidence.evidence_id}"
        )

    try:
        signal = _BusinessImpactSignal.model_validate(raw_signal)
    except ValidationError as exc:
        raise BusinessImpactAnalysisError(
            f"invalid business_impact in evidence {evidence.evidence_id}"
        ) from exc

    if (
        signal.status is BusinessImpactStatus.CONFIRMED
        and evidence.evidence_type is not EvidenceType.ANALYST_OBSERVATION
    ):
        raise BusinessImpactAnalysisError(
            "confirmed business impact requires analyst_observation "
            f"evidence: {evidence.evidence_id}"
        )

    return BusinessImpact(
        status=signal.status,
        description=signal.description,
        affected_processes=signal.affected_processes,
        affected_consumers=signal.affected_consumers,
        materiality=signal.materiality,
        supporting_evidence=[evidence.evidence_id],
    )


def _merge_candidates(
    candidates: list[BusinessImpact],
) -> BusinessImpact:
    for status in (
        BusinessImpactStatus.CONFIRMED,
        BusinessImpactStatus.POTENTIAL,
        BusinessImpactStatus.UNKNOWN,
    ):
        selected = [candidate for candidate in candidates if candidate.status is status]

        if selected:
            return _merge_same_status(selected, status)

    return _unknown_business_impact()


def _merge_same_status(
    candidates: list[BusinessImpact],
    status: BusinessImpactStatus,
) -> BusinessImpact:
    descriptions = _unique(candidate.description for candidate in candidates)
    affected_processes = _unique(
        process for candidate in candidates for process in candidate.affected_processes
    )
    affected_consumers = _unique(
        consumer for candidate in candidates for consumer in candidate.affected_consumers
    )
    supporting_evidence = _unique(
        evidence_id for candidate in candidates for evidence_id in candidate.supporting_evidence
    )

    materiality = _resolve_materiality(candidates)

    return BusinessImpact(
        status=status,
        description=" | ".join(descriptions),
        affected_processes=affected_processes,
        affected_consumers=affected_consumers,
        materiality=materiality,
        supporting_evidence=supporting_evidence,
    )


def _resolve_materiality(
    candidates: list[BusinessImpact],
) -> str | None:
    values = _unique(
        candidate.materiality for candidate in candidates if candidate.materiality is not None
    )

    if len(values) == 1:
        return values[0]

    return None


def _unique(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _unknown_business_impact() -> BusinessImpact:
    return BusinessImpact(
        status=BusinessImpactStatus.UNKNOWN,
        description=_UNKNOWN_DESCRIPTION,
        affected_processes=[],
        affected_consumers=[],
        materiality=None,
        supporting_evidence=[],
    )


__all__ = [
    "BusinessImpactAnalysisError",
    "analyze_business_impact",
]
