"""Deterministic evidence collection and normalization."""

from collections.abc import Iterable, Mapping

from pydantic import ValidationError

from ai_data_governance_agent.domain.evidence import Evidence


class EvidenceCollectionError(ValueError):
    """Raised when evidence collection cannot be completed safely."""


EvidenceCandidate = Evidence | Mapping[str, object]


def collect_evidence(
    candidates: Iterable[EvidenceCandidate],
) -> list[Evidence]:
    """Normalize, validate, and organize evidence in deterministic order."""
    collected: list[Evidence] = []
    first_index_by_id: dict[str, int] = {}

    for index, candidate in enumerate(candidates):
        evidence = _normalize_candidate(candidate, index)

        first_index = first_index_by_id.get(evidence.evidence_id)

        if first_index is not None:
            raise EvidenceCollectionError(
                "duplicate evidence_id detected: "
                f"{evidence.evidence_id} "
                f"(first index {first_index}, duplicate index {index})"
            )

        first_index_by_id[evidence.evidence_id] = index
        collected.append(evidence)

    return collected


def _normalize_candidate(
    candidate: EvidenceCandidate,
    index: int,
) -> Evidence:
    """Convert one supported candidate into a validated Evidence model."""
    if isinstance(candidate, Evidence):
        return candidate.model_copy(deep=True)

    if isinstance(candidate, Mapping):
        try:
            return Evidence.model_validate(candidate)
        except ValidationError as exc:
            raise EvidenceCollectionError(f"invalid evidence at index {index}") from exc

    raise EvidenceCollectionError(
        f"unsupported evidence structure at index {index}: {type(candidate).__name__}"
    )


__all__ = [
    "EvidenceCandidate",
    "EvidenceCollectionError",
    "collect_evidence",
]
