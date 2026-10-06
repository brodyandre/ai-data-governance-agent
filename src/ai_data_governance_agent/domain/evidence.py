"""Evidence domain model for the AI Data Governance Agent."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, JsonValue, field_validator

from ai_data_governance_agent.domain.enums import EvidenceReliability, EvidenceType


class Evidence(BaseModel):
    """Represent one traceable piece of evidence associated with an incident."""

    model_config = ConfigDict(extra="forbid")

    evidence_id: str
    evidence_type: EvidenceType
    source: str
    description: str | None = None
    value: JsonValue = None
    collected_at: datetime | None = None
    reliability: EvidenceReliability | None = None
    metadata: dict[str, JsonValue] = Field(default_factory=dict)

    @field_validator("evidence_id", "source")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        """Trim required text fields and reject empty values."""
        normalized = value.strip()

        if not normalized:
            raise ValueError("value must contain non-whitespace characters")

        return normalized

    @field_validator("description")
    @classmethod
    def validate_optional_description(cls, value: str | None) -> str | None:
        """Trim an optional description and reject whitespace-only content."""
        if value is None:
            return None

        normalized = value.strip()

        if not normalized:
            raise ValueError("description must contain non-whitespace characters")

        return normalized


__all__ = ["Evidence"]
