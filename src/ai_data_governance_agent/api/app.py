"""FastAPI application bootstrap."""

from typing import Literal

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict

from ai_data_governance_agent import __version__
from ai_data_governance_agent.api.errors import (
    ErrorResponse,
    build_error_response,
    request_validation_exception_handler,
)
from ai_data_governance_agent.domain.incident import IncidentInput
from ai_data_governance_agent.domain.response import AgentResponse
from ai_data_governance_agent.providers import (
    ModelProvider,
    ProviderError,
)
from ai_data_governance_agent.workflow import (
    WorkflowExecutionError,
    run_agent,
)

SERVICE_NAME = "ai-data-governance-agent"

_PROVIDER_WORKFLOW_STEPS = frozenset(
    {
        "hypotheses_generated",
        "recommendations_generated",
    }
)


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

    application.add_exception_handler(
        RequestValidationError,
        request_validation_exception_handler,
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
        responses={
            422: {
                "model": ErrorResponse,
                "description": "Request validation failed.",
            },
            500: {
                "model": ErrorResponse,
                "description": "Internal analysis failure.",
            },
            502: {
                "model": ErrorResponse,
                "description": "Model provider failure.",
            },
            503: {
                "model": ErrorResponse,
                "description": "Model provider is not configured.",
            },
        },
        tags=["incidents"],
    )
    def analyze_incident(
        incident: IncidentInput,
    ) -> AgentResponse | JSONResponse:
        """Analyze a validated data incident through the agent workflow."""
        if provider is None:
            return build_error_response(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                code="provider_not_configured",
                message="model provider is not configured",
            )

        try:
            return run_agent(
                incident,
                provider,
            )
        except ProviderError:
            return _provider_error_response()
        except WorkflowExecutionError as exc:
            if _is_provider_workflow_failure(exc):
                return _provider_error_response()

            return _internal_error_response()
        except Exception:
            return _internal_error_response()

    return application


def _is_provider_workflow_failure(
    exc: WorkflowExecutionError,
) -> bool:
    """Identify workflow failures originating from provider-backed nodes."""
    return any(error.step in _PROVIDER_WORKFLOW_STEPS for error in exc.errors)


def _provider_error_response() -> JSONResponse:
    """Return a safe error without exposing provider details."""
    return build_error_response(
        status_code=status.HTTP_502_BAD_GATEWAY,
        code="provider_error",
        message="model provider failed to complete the analysis",
    )


def _internal_error_response() -> JSONResponse:
    """Return a safe error without exposing internal details."""
    return build_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        code="internal_error",
        message="analysis could not be completed safely",
    )


app = create_app()


__all__ = [
    "HealthResponse",
    "SERVICE_NAME",
    "app",
    "create_app",
]
