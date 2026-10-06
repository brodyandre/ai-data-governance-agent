"""Tests for the unsupported-claims guardrail."""

from ai_data_governance_agent.domain.enums import HypothesisStatus
from ai_data_governance_agent.domain.response import RootCauseHypothesis
from ai_data_governance_agent.guardrails import (
    qualify_unsupported_hypotheses,
)


def make_hypothesis(
    *,
    status: HypothesisStatus,
    supporting_evidence: list[str] | None = None,
    confidence: float = 0.90,
) -> RootCauseHypothesis:
    return RootCauseHypothesis(
        description="A transformation may have caused the incident.",
        supporting_evidence=list(supporting_evidence or []),
        confidence=confidence,
        status=status,
    )


def test_empty_collection_remains_empty() -> None:
    assert qualify_unsupported_hypotheses([]) == []


def test_unsupported_suspected_hypothesis_remains_suspected() -> None:
    hypothesis = make_hypothesis(
        status=HypothesisStatus.SUSPECTED,
    )

    result = qualify_unsupported_hypotheses([hypothesis])

    assert result[0].status is HypothesisStatus.SUSPECTED
    assert result[0].supporting_evidence == []


def test_unsupported_probable_hypothesis_is_qualified() -> None:
    hypothesis = make_hypothesis(
        status=HypothesisStatus.PROBABLE,
        confidence=0.95,
    )

    result = qualify_unsupported_hypotheses([hypothesis])

    assert result[0].status is HypothesisStatus.SUSPECTED
    assert result[0].confidence == 0.95
    assert result[0].supporting_evidence == []


def test_unsupported_rejected_hypothesis_is_qualified() -> None:
    hypothesis = make_hypothesis(
        status=HypothesisStatus.REJECTED,
    )

    result = qualify_unsupported_hypotheses([hypothesis])

    assert result[0].status is HypothesisStatus.SUSPECTED


def test_supported_probable_hypothesis_is_preserved() -> None:
    hypothesis = make_hypothesis(
        status=HypothesisStatus.PROBABLE,
        supporting_evidence=["EV-001"],
    )

    result = qualify_unsupported_hypotheses([hypothesis])

    assert result[0].status is HypothesisStatus.PROBABLE
    assert result[0].supporting_evidence == ["EV-001"]


def test_supported_rejected_hypothesis_is_preserved() -> None:
    hypothesis = make_hypothesis(
        status=HypothesisStatus.REJECTED,
        supporting_evidence=["EV-001"],
    )

    result = qualify_unsupported_hypotheses([hypothesis])

    assert result[0].status is HypothesisStatus.REJECTED


def test_supported_confirmed_hypothesis_is_preserved() -> None:
    hypothesis = make_hypothesis(
        status=HypothesisStatus.CONFIRMED,
        supporting_evidence=["EV-001"],
        confidence=1.0,
    )

    result = qualify_unsupported_hypotheses([hypothesis])

    assert result[0].status is HypothesisStatus.CONFIRMED


def test_guardrail_does_not_mutate_input_hypothesis() -> None:
    hypothesis = make_hypothesis(
        status=HypothesisStatus.PROBABLE,
    )

    result = qualify_unsupported_hypotheses([hypothesis])

    assert hypothesis.status is HypothesisStatus.PROBABLE
    assert result[0].status is HypothesisStatus.SUSPECTED
    assert result[0] is not hypothesis


def test_guardrail_accepts_generic_iterables() -> None:
    hypotheses = (
        make_hypothesis(
            status=HypothesisStatus.PROBABLE,
        )
        for _ in range(2)
    )

    result = qualify_unsupported_hypotheses(hypotheses)

    assert len(result) == 2
    assert all(item.status is HypothesisStatus.SUSPECTED for item in result)
