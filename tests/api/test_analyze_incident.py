"""Tests for the incident analysis HTTP endpoint."""

from fastapi.testclient import TestClient

from ai_data_governance_agent.api import create_app
from ai_data_governance_agent.providers import FakeProvider
from ai_data_governance_agent.workflow import (
    HypothesisGenerationResult,
    RecommendationGenerationResult,
)

ANALYZE_PATH = "/api/v1/incidents/analyze"


def make_incident_payload() -> dict[str, object]:
    """Return a valid HTTP incident payload."""
    return {
        "incident_id": "INC-602",
        "title": "Invalid records detected",
        "description": ("A data-quality validation identified invalid records."),
        "source_system": "orders-lakehouse",
        "detected_at": "2026-10-06T22:30:00Z",
        "evidence": [
            {
                "evidence_id": "EV-001",
                "evidence_type": "data_quality_check",
                "source": "quality-report",
                "value": {
                    "invalid_rows": 30,
                },
            }
        ],
    }


def make_provider() -> FakeProvider:
    """Return the deterministic provider used by API tests."""
    return FakeProvider(
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


def test_analyze_endpoint_executes_workflow() -> None:
    client = TestClient(
        create_app(
            provider=make_provider(),
        )
    )

    response = client.post(
        ANALYZE_PATH,
        json=make_incident_payload(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["incident_id"] == "INC-602"
    assert body["classification"] == "data_quality"
    assert body["severity"] == "medium"
    assert body["confidence"] == 0.85

    assert body["executive_summary"] == "Invalid records require investigation."


def test_analyze_endpoint_returns_agent_response_contract() -> None:
    client = TestClient(
        create_app(
            provider=make_provider(),
        )
    )

    response = client.post(
        ANALYZE_PATH,
        json=make_incident_payload(),
    )

    body = response.json()

    assert response.status_code == 200

    assert len(body["evidence"]) == 1
    assert body["evidence"][0]["evidence_id"] == "EV-001"

    assert len(body["root_cause_hypotheses"]) == 1

    assert body["root_cause_hypotheses"][0]["supporting_evidence"] == ["EV-001"]

    assert len(body["recommended_actions"]) == 1

    assert body["recommended_actions"][0]["supporting_evidence"] == ["EV-001"]

    assert isinstance(
        body["governance_controls"],
        list,
    )
    assert isinstance(
        body["human_review_required"],
        bool,
    )
    assert isinstance(
        body["human_review_reasons"],
        list,
    )


def test_invalid_incident_request_returns_422() -> None:
    client = TestClient(
        create_app(
            provider=make_provider(),
        )
    )

    response = client.post(
        ANALYZE_PATH,
        json={
            "incident_id": "INC-INVALID",
        },
    )

    assert response.status_code == 422

    body = response.json()

    assert "detail" in body
    assert isinstance(body["detail"], list)


def test_request_with_unknown_field_returns_422() -> None:
    client = TestClient(
        create_app(
            provider=make_provider(),
        )
    )

    payload = make_incident_payload()
    payload["unexpected_field"] = "not-allowed"

    response = client.post(
        ANALYZE_PATH,
        json=payload,
    )

    assert response.status_code == 422


def test_analyze_endpoint_requires_configured_provider() -> None:
    client = TestClient(create_app())

    response = client.post(
        ANALYZE_PATH,
        json=make_incident_payload(),
    )

    assert response.status_code == 503

    assert response.json() == {"detail": "model provider is not configured"}
