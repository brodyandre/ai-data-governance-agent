"""Integration tests for incidents without supporting evidence."""

from datetime import UTC, datetime

from ai_data_governance_agent.domain.incident import IncidentInput
from ai_data_governance_agent.providers import FakeProvider
from ai_data_governance_agent.workflow import (
    HypothesisGenerationResult,
    RecommendationGenerationResult,
    run_agent,
)


def make_incident(
    *,
    with_evidence: bool = False,
) -> IncidentInput:
    """Create a structurally valid incident for DG-502 tests."""
    evidence: list[dict[str, object]] = []

    if with_evidence:
        evidence.append(
            {
                "evidence_id": "EV-001",
                "evidence_type": "data_quality_check",
                "source": "quality-report",
                "value": {
                    "invalid_rows": 30,
                },
            }
        )

    return IncidentInput.model_validate(
        {
            "incident_id": "INC-502",
            "title": "Incident under investigation",
            "description": ("An anomaly was reported and requires investigation."),
            "source_system": "orders-lakehouse",
            "detected_at": datetime(
                2026,
                10,
                6,
                21,
                0,
                tzinfo=UTC,
            ),
            "evidence": evidence,
        }
    )


def make_hypothesis_only_provider(
    *,
    confidence: float = 0.95,
) -> FakeProvider:
    """Return an adversarial hypothesis without recommendation config."""
    return FakeProvider(
        responses={
            HypothesisGenerationResult: {
                "classification": "unknown",
                "severity": "medium",
                "executive_summary": ("The upstream process caused the incident."),
                "confidence": confidence,
                "root_cause_hypotheses": [
                    {
                        "description": ("The upstream process caused the incident."),
                        "supporting_evidence": ["EV-FAKE"],
                        "confidence": 0.95,
                        "status": "confirmed",
                    }
                ],
            }
        }
    )


def test_structurally_valid_incident_without_evidence_is_accepted() -> None:
    incident = make_incident()

    response = run_agent(
        incident,
        make_hypothesis_only_provider(),
    )

    assert response.incident_id == "INC-502"
    assert response.evidence == []


def test_missing_evidence_caps_confidence_and_overrides_summary() -> None:
    response = run_agent(
        make_incident(),
        make_hypothesis_only_provider(
            confidence=0.95,
        ),
    )

    assert response.confidence == 0.50

    assert response.executive_summary == (
        "Evidence is insufficient to establish a reliable root cause. "
        "Additional investigation is required."
    )


def test_missing_evidence_discards_provider_hypotheses() -> None:
    response = run_agent(
        make_incident(),
        make_hypothesis_only_provider(),
    )

    assert response.root_cause_hypotheses == []


def test_missing_evidence_does_not_fabricate_supporting_evidence() -> None:
    response = run_agent(
        make_incident(),
        make_hypothesis_only_provider(),
    )

    assert response.evidence == []
    assert response.root_cause_hypotheses == []

    assert len(response.recommended_actions) == 1
    assert response.recommended_actions[0].supporting_evidence == []


def test_missing_evidence_generates_additional_investigation_action() -> None:
    response = run_agent(
        make_incident(),
        make_hypothesis_only_provider(),
    )

    assert len(response.recommended_actions) == 1

    action = response.recommended_actions[0]

    assert action.priority == "high"

    assert action.description == (
        "Collect and validate additional evidence before "
        "drawing root-cause conclusions or planning remediation."
    )


def test_missing_evidence_activates_expected_human_review_rules() -> None:
    response = run_agent(
        make_incident(),
        make_hypothesis_only_provider(),
    )

    assert response.human_review_required is True

    assert response.human_review_reasons == [
        "low confidence",
        "insufficient evidence",
        "high root-cause uncertainty",
    ]


def test_low_provider_confidence_is_not_increased_without_evidence() -> None:
    response = run_agent(
        make_incident(),
        make_hypothesis_only_provider(
            confidence=0.30,
        ),
    )

    assert response.confidence == 0.30


def test_recommendation_provider_is_not_required_without_evidence() -> None:
    provider = make_hypothesis_only_provider()

    response = run_agent(
        make_incident(),
        provider,
    )

    assert len(response.recommended_actions) == 1


def test_evidence_present_preserves_normal_provider_path() -> None:
    provider = FakeProvider(
        responses={
            HypothesisGenerationResult: {
                "classification": "data_quality",
                "severity": "medium",
                "executive_summary": ("Invalid records require investigation."),
                "confidence": 0.85,
                "root_cause_hypotheses": [
                    {
                        "description": ("Validation may have rejected invalid records."),
                        "supporting_evidence": ["EV-001"],
                        "confidence": 0.80,
                        "status": "probable",
                    }
                ],
            },
            RecommendationGenerationResult: {
                "recommended_actions": [
                    {
                        "description": ("Review the invalid records."),
                        "priority": "medium",
                        "rationale": ("The quality evidence identified invalid rows."),
                        "requires_human_approval": False,
                        "supporting_evidence": ["EV-001"],
                    }
                ]
            },
        }
    )

    response = run_agent(
        make_incident(with_evidence=True),
        provider,
    )

    assert response.confidence == 0.85

    assert response.executive_summary == "Invalid records require investigation."

    assert len(response.root_cause_hypotheses) == 1
    assert len(response.recommended_actions) == 1

    assert response.recommended_actions[0].supporting_evidence == ["EV-001"]
