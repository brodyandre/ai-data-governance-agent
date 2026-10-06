"""Tests for deterministic evidence collection."""

from collections.abc import Iterator

import pytest
from pydantic import ValidationError

from ai_data_governance_agent.domain import Evidence
from ai_data_governance_agent.tools import (
    EvidenceCollectionError,
    collect_evidence,
)


def valid_payload(
    evidence_id: str = "EV-001",
    *,
    evidence_type: str = "reconciliation_result",
    source: str = "pipeline-report",
) -> dict[str, object]:
    """Create a valid raw evidence payload."""
    return {
        "evidence_id": evidence_id,
        "evidence_type": evidence_type,
        "source": source,
        "description": "Evidence description.",
        "value": {
            "raw_count": 400,
            "silver_count": 388,
        },
        "reliability": "high",
        "metadata": {
            "dataset": "orders",
        },
    }


def test_collects_empty_iterable() -> None:
    assert collect_evidence([]) == []


def test_normalizes_mapping_into_evidence() -> None:
    result = collect_evidence(
        [
            valid_payload(
                evidence_id=" EV-001 ",
                source=" pipeline-report ",
            )
        ]
    )

    assert len(result) == 1
    assert isinstance(result[0], Evidence)
    assert result[0].evidence_id == "EV-001"
    assert result[0].source == "pipeline-report"


def test_preserves_evidence_order() -> None:
    result = collect_evidence(
        [
            valid_payload("EV-003"),
            valid_payload("EV-001"),
            valid_payload("EV-002"),
        ]
    )

    assert [item.evidence_id for item in result] == [
        "EV-003",
        "EV-001",
        "EV-002",
    ]


def test_preserves_evidence_id_casing() -> None:
    result = collect_evidence(
        [
            valid_payload("Ev-ABC-001"),
        ]
    )

    assert result[0].evidence_id == "Ev-ABC-001"


def test_ids_are_case_sensitive_for_duplicate_detection() -> None:
    result = collect_evidence(
        [
            valid_payload("EV-001"),
            valid_payload("ev-001"),
        ]
    )

    assert [item.evidence_id for item in result] == [
        "EV-001",
        "ev-001",
    ]


def test_duplicate_ids_are_detected_after_normalization() -> None:
    with pytest.raises(
        EvidenceCollectionError,
        match=(
            r"duplicate evidence_id detected: EV-001 "
            r"\(first index 0, duplicate index 1\)"
        ),
    ):
        collect_evidence(
            [
                valid_payload(" EV-001 "),
                valid_payload("EV-001"),
            ]
        )


def test_duplicate_error_reports_first_and_duplicate_indexes() -> None:
    with pytest.raises(EvidenceCollectionError) as exc_info:
        collect_evidence(
            [
                valid_payload("EV-001"),
                valid_payload("EV-002"),
                valid_payload("EV-001"),
            ]
        )

    assert str(exc_info.value) == (
        "duplicate evidence_id detected: EV-001 (first index 0, duplicate index 2)"
    )


def test_invalid_mapping_raises_collection_error() -> None:
    invalid = valid_payload()
    invalid["evidence_type"] = "not-supported"

    with pytest.raises(
        EvidenceCollectionError,
        match="invalid evidence at index 0",
    ) as exc_info:
        collect_evidence([invalid])

    assert isinstance(exc_info.value.__cause__, ValidationError)


def test_invalid_mapping_error_reports_correct_index() -> None:
    invalid = valid_payload("EV-002")
    invalid["source"] = "   "

    with pytest.raises(
        EvidenceCollectionError,
        match="invalid evidence at index 1",
    ):
        collect_evidence(
            [
                valid_payload("EV-001"),
                invalid,
            ]
        )


@pytest.mark.parametrize(
    "candidate",
    [
        "plain-text",
        42,
        3.14,
        ["not", "a", "mapping"],
        ("not", "a", "mapping"),
    ],
)
def test_unsupported_structure_is_rejected(candidate: object) -> None:
    with pytest.raises(
        EvidenceCollectionError,
        match="unsupported evidence structure at index 0",
    ):
        collect_evidence([candidate])  # type: ignore[list-item]


def test_existing_evidence_instance_is_accepted() -> None:
    evidence = Evidence.model_validate(valid_payload())

    result = collect_evidence([evidence])

    assert result == [evidence]


def test_existing_evidence_instance_is_deep_copied() -> None:
    evidence = Evidence.model_validate(valid_payload())

    result = collect_evidence([evidence])

    assert result[0] is not evidence
    assert result[0].metadata is not evidence.metadata


def test_collector_does_not_mutate_existing_evidence() -> None:
    evidence = Evidence.model_validate(valid_payload())
    original_dump = evidence.model_dump()

    collect_evidence([evidence])

    assert evidence.model_dump() == original_dump


def test_collector_does_not_mutate_raw_mapping() -> None:
    payload = valid_payload(
        evidence_id=" EV-001 ",
        source=" pipeline-report ",
    )
    original = {
        **payload,
        "value": dict(payload["value"]),  # type: ignore[arg-type]
        "metadata": dict(payload["metadata"]),  # type: ignore[arg-type]
    }

    collect_evidence([payload])

    assert payload == original


def test_traceability_fields_are_preserved() -> None:
    payload = valid_payload()
    payload["value"] = {
        "raw_count": 400,
        "silver_count": 388,
    }
    payload["metadata"] = {
        "dataset": "orders",
        "run_id": "RUN-001",
    }

    result = collect_evidence([payload])

    evidence = result[0]

    assert evidence.evidence_id == "EV-001"
    assert evidence.source == "pipeline-report"
    assert evidence.value == {
        "raw_count": 400,
        "silver_count": 388,
    }
    assert evidence.metadata == {
        "dataset": "orders",
        "run_id": "RUN-001",
    }


def test_generator_input_is_supported() -> None:
    def candidates() -> Iterator[dict[str, object]]:
        yield valid_payload("EV-001")
        yield valid_payload("EV-002")

    result = collect_evidence(candidates())

    assert [item.evidence_id for item in result] == [
        "EV-001",
        "EV-002",
    ]


def test_same_input_produces_same_output() -> None:
    payloads = [
        valid_payload("EV-001"),
        valid_payload(
            "EV-002",
            evidence_type="metric",
            source="quality-metric",
        ),
    ]

    first = collect_evidence(payloads)
    second = collect_evidence(payloads)

    assert first == second


def test_extra_fields_are_rejected_through_evidence_contract() -> None:
    payload = valid_payload()
    payload["unexpected"] = "not-allowed"

    with pytest.raises(
        EvidenceCollectionError,
        match="invalid evidence at index 0",
    ):
        collect_evidence([payload])
