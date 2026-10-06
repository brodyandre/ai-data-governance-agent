"""FastAPI application bootstrap."""

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict

from ai_data_governance_agent import __version__

SERVICE_NAME = "ai-data-governance-agent"


class HealthResponse(BaseModel):
    """Represent the public health-check response."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["ok"]
    service: str
    version: str


def create_app() -> FastAPI:
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

    return application


app = create_app()


__all__ = [
    "HealthResponse",
    "SERVICE_NAME",
    "app",
    "create_app",
]
