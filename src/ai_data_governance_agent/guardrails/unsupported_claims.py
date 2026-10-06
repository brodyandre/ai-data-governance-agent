"""Deterministic guardrails for unsupported analytical claims."""

from collections.abc import Iterable

from ai_data_governance_agent.domain.enums import HypothesisStatus
from ai_data_governance_agent.domain.response import RootCauseHypothesis


def qualify_unsupported_hypotheses(
    hypotheses: Iterable[RootCauseHypothesis],
) -> list[RootCauseHypothesis]:
    """Qualify unsupported root-cause conclusions conservatively.

    A hypothesis without supporting evidence cannot preserve a status that
    implies stronger analytical certainty. Such hypotheses remain explicitly
    hypotheses by being downgraded to ``suspected``.

    Evidence-reference validity is intentionally not checked here. That
    responsibility belongs to the dedicated traceability guardrail.
    """
    qualified: list[RootCauseHypothesis] = []

    for hypothesis in hypotheses:
        guarded = hypothesis.model_copy(deep=True)

        if not guarded.supporting_evidence and guarded.status is not HypothesisStatus.SUSPECTED:
            guarded = guarded.model_copy(
                update={
                    "status": HypothesisStatus.SUSPECTED,
                },
                deep=True,
            )

        qualified.append(guarded)

    return qualified


__all__ = [
    "qualify_unsupported_hypotheses",
]
