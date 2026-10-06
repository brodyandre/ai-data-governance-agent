"""FastAPI application bootstrap."""

from typing import Literal

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict

from ai_data_governance_agent import __version__
from ai_data_governance_agent.domain.incident import IncidentInput
from ai_data_governance_agent.domain.response import AgentResponse
from ai_data_governance_agent.providers import ModelProvider
from ai_data_governance_agent.workflow import run_agent

SERVICE_NAME = "ai-data-governance-agent"


class HealthResponse(BaseModel):
    """Represent the public health-check response."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["ok"]
    service: str
    version: str


def create_app(
    provider: ModelProvider | None = None,
) -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title="AI Data Governance Agent",
        description=(
            "API for governed analysis of data incidents, evidence and data-quality signals."
        ),
        version=__version__,
    )

    @application.get(
        "/health",
        response_model=HealthResponse,
        tags=["health"],
    )
    def health() -> HealthResponse:
        """Return application health and version information."""
        return HealthResponse(
            status="ok",
            service=SERVICE_NAME,
            version=__version__,
        )

    @application.post(
        "/api/v1/incidents/analyze",
        response_model=AgentResponse,
        tags=["incidents"],
    )
    def analyze_incident(
        incident: IncidentInput,
    ) -> AgentResponse:
        """Analyze a validated data incident through the agent workflow."""
        if provider is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="model provider is not configured",
            )

        return run_agent(
            incident,
            provider,
        )

    return application


app = create_app()


__all__ = [
    "HealthResponse",
    "SERVICE_NAME",
    "app",
    "create_app",
]
