"""Deterministic retrieval of local governance controls."""

from collections.abc import Iterable
from dataclasses import dataclass

from ai_data_governance_agent.domain.evidence import Evidence
from ai_data_governance_agent.domain.response import GovernanceControl
from ai_data_governance_agent.tools.quality_analyzer import (
    QualityFinding,
    QualityFindingType,
)


class PolicyRetrievalError(ValueError):
    """Raised when policy retrieval cannot preserve traceability."""


@dataclass(frozen=True, slots=True)
class _LocalPolicy:
    """Represent one locally defined governance control."""

    control_id: str
    title: str
    description: str
    source: str
    finding_types: frozenset[QualityFindingType]


_LOCAL_POLICIES: tuple[_LocalPolicy, ...] = (
    _LocalPolicy(
        control_id="DQ-001",
        title="Validação de qualidade de registros",
        description=(
            "Identificar e acompanhar registros inválidos e falhas em validações de qualidade."
        ),
        source="docs/policies/LOCAL_CONTROLS.md#dq-001",
        finding_types=frozenset({"invalid_records", "validation_failures"}),
    ),
    _LocalPolicy(
        control_id="DQ-002",
        title="Reconciliação de volumes",
        description=(
            "Verificar divergências entre contagens esperadas, observadas ou entre camadas."
        ),
        source="docs/policies/LOCAL_CONTROLS.md#dq-002",
        finding_types=frozenset({"reconciliation_divergence", "count_divergence"}),
    ),
    _LocalPolicy(
        control_id="DQ-003",
        title="Integridade e relacionamentos",
        description=("Acompanhar falhas de relacionamento e violações de integridade dos dados."),
        source="docs/policies/LOCAL_CONTROLS.md#dq-003",
        finding_types=frozenset({"missing_relationships", "integrity_inconsistencies"}),
    ),
)


def retrieve_policies(
    evidence_items: Iterable[Evidence],
    findings: Iterable[QualityFinding],
) -> list[GovernanceControl]:
    """Retrieve applicable local controls with evidence traceability."""
    known_ids: set[str] = set()

    for evidence in evidence_items:
        if evidence.evidence_id in known_ids:
            raise PolicyRetrievalError(f"duplicate evidence_id: {evidence.evidence_id}")

        known_ids.add(evidence.evidence_id)

    validated_findings = list(findings)

    for index, finding in enumerate(validated_findings):
        for evidence_id in finding.supporting_evidence:
            if evidence_id not in known_ids:
                raise PolicyRetrievalError(
                    f"unknown evidence_id {evidence_id} in finding at index {index}"
                )

    controls: list[GovernanceControl] = []

    for policy in _LOCAL_POLICIES:
        matches = [
            finding
            for finding in validated_findings
            if finding.finding_type in policy.finding_types
        ]

        if not matches:
            continue

        evidence_ids = list(
            dict.fromkeys(
                evidence_id for finding in matches for evidence_id in finding.supporting_evidence
            )
        )

        matched_types = list(dict.fromkeys(finding.finding_type for finding in matches))

        controls.append(
            GovernanceControl(
                control_id=policy.control_id,
                title=policy.title,
                description=policy.description,
                source=policy.source,
                relevance=("Sinais de qualidade identificados: " + ", ".join(matched_types) + "."),
                supporting_evidence=evidence_ids,
            )
        )

    return controls


__all__ = [
    "PolicyRetrievalError",
    "retrieve_policies",
]
