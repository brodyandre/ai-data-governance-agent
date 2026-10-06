"""Incident input domain model for the AI Data Governance Agent."""

from datetime import datetime
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ai_data_governance_agent.domain.enums import Severity
from ai_data_governance_agent.domain.evidence import Evidence


class IncidentInput(BaseModel):
    """Represent a validated data incident submitted for analysis."""

    model_config = ConfigDict(extra="forbid")

    incident_id: str
    title: str
    description: str
    source_system: str
    detected_at: datetime
    evidence: list[Evidence]

    affected_datasets: list[str] = Field(default_factory=list)
    reported_by: str | None = None
    business_context: str | None = None
    expected_behavior: str | None = None
    observed_behavior: str | None = None
    initial_severity: Severity | None = None
    tags: list[str] = Field(default_factory=list)

    @field_validator(
        "incident_id",
        "title",
        "description",
        "source_system",
    )
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        """Trim required text fields and reject blank values."""
        normalized = value.strip()

        if not normalized:
            raise ValueError("value must contain non-whitespace characters")

        return normalized

    @model_validator(mode="after")
    def validate_unique_evidence_ids(self) -> Self:
        """Reject duplicated evidence identifiers within the incident."""
        seen: set[str] = set()
        duplicates: list[str] = []

        for evidence in self.evidence:
            evidence_id = evidence.evidence_id

            if evidence_id in seen and evidence_id not in duplicates:
                duplicates.append(evidence_id)

            seen.add(evidence_id)

        if duplicates:
            duplicate_values = ", ".join(duplicates)
            raise ValueError(f"duplicate evidence_id values are not allowed: {duplicate_values}")

        return self


__all__ = ["IncidentInput"]
