"""Tests for safe and structured API error handling."""

import importlib
from unittest.mock import patch

from fastapi.testclient import TestClient

from ai_data_governance_agent.api import (
    ErrorResponse,
    create_app,
)
from ai_data_governance_agent.providers import (
    FakeProvider,
    ProviderError,
)

ANALYZE_PATH = "/api/v1/incidents/analyze"


def make_incident_payload() -> dict[str, object]:
    """Return a structurally valid incident payload."""
    return {
        "incident_id": "INC-603",
        "title": "Incident for API error tests",
        "description": ("A data-quality anomaly requires investigation."),
        "source_system": "orders-lakehouse",
        "detected_at": "2026-10-06T22:45:00Z",
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


def test_validation_error_uses_structured_contract() -> None:
    client = TestClient(
        create_app(
            provider=FakeProvider(),
        )
    )

    response = client.post(
        ANALYZE_PATH,
        json={
            "incident_id": "INC-INVALID",
        },
    )

    assert response.status_code == 422

    error = ErrorResponse.model_validate(response.json())

    assert error.code == "request_validation_error"
    assert error.message == "request validation failed"
    assert error.details

    fields = {detail.field for detail in error.details}

    assert {
        "title",
        "description",
        "source_system",
        "detected_at",
        "evidence",
    }.issubset(fields)


def test_validation_error_does_not_echo_rejected_input() -> None:
    secret = "SECRET-REQUEST-VALUE-603"

    payload = make_incident_payload()
    payload["unexpected_field"] = secret

    client = TestClient(
        create_app(
            provider=FakeProvider(),
        )
    )

    response = client.post(
        ANALYZE_PATH,
        json=payload,
    )

    assert response.status_code == 422
    assert secret not in response.text

    error = ErrorResponse.model_validate(response.json())

    assert error.code == "request_validation_error"

    assert any(detail.field == "unexpected_field" for detail in error.details)


def test_provider_failure_returns_safe_502() -> None:
    secret = "SECRET-PROVIDER-TOKEN-603"

    provider = FakeProvider(error=ProviderError(f"provider failed with token {secret}"))

    client = TestClient(
        create_app(
            provider=provider,
        )
    )

    response = client.post(
        ANALYZE_PATH,
        json=make_incident_payload(),
    )

    assert response.status_code == 502
    assert secret not in response.text

    assert response.json() == {
        "code": "provider_error",
        "message": ("model provider failed to complete the analysis"),
        "details": [],
    }


def test_unexpected_internal_failure_returns_safe_500() -> None:
    secret = "SECRET-INTERNAL-DATABASE-PASSWORD-603"

    api_app_module = importlib.import_module("ai_data_governance_agent.api.app")

    client = TestClient(
        create_app(
            provider=FakeProvider(),
        )
    )

    with patch.object(
        api_app_module,
        "run_agent",
        side_effect=RuntimeError(f"database password is {secret}"),
    ):
        response = client.post(
            ANALYZE_PATH,
            json=make_incident_payload(),
        )

    assert response.status_code == 500
    assert secret not in response.text

    assert response.json() == {
        "code": "internal_error",
        "message": "analysis could not be completed safely",
        "details": [],
    }


def test_provider_not_configured_uses_error_contract() -> None:
    client = TestClient(create_app())

    response = client.post(
        ANALYZE_PATH,
        json=make_incident_payload(),
    )

    assert response.status_code == 503

    error = ErrorResponse.model_validate(response.json())

    assert error.code == "provider_not_configured"
    assert error.details == []


def test_openapi_documents_analysis_error_contracts() -> None:
    application = create_app()

    schema = application.openapi()

    responses = schema["paths"][ANALYZE_PATH]["post"]["responses"]

    assert {
        "422",
        "500",
        "502",
        "503",
    }.issubset(responses)

    for status_code in (
        "422",
        "500",
        "502",
        "503",
    ):
        response_schema = responses[status_code]["content"]["application/json"]["schema"]

        assert response_schema["$ref"] == "#/components/schemas/ErrorResponse"
