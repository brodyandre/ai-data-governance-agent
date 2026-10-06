"""Tests for the FastAPI application bootstrap and health endpoint."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from ai_data_governance_agent import __version__
from ai_data_governance_agent.api import (
    SERVICE_NAME,
    app,
    create_app,
)


def test_application_is_fastapi_instance() -> None:
    assert isinstance(app, FastAPI)
    assert app.title == "AI Data Governance Agent"
    assert app.version == __version__


def test_health_endpoint_returns_service_status() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok",
        "service": SERVICE_NAME,
        "version": __version__,
    }


def test_health_endpoint_returns_json() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.headers["content-type"].startswith("application/json")


def test_application_factory_creates_independent_apps() -> None:
    first = create_app()
    second = create_app()

    assert isinstance(first, FastAPI)
    assert isinstance(second, FastAPI)
    assert first is not second

    response = TestClient(first).get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
