"""Safe and structured HTTP error responses."""

from collections.abc import Iterable

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field


class ErrorDetail(BaseModel):
    """Represent one safe request-validation error."""

    model_config = ConfigDict(extra="forbid")

    field: str
    message: str
    type: str


class ErrorResponse(BaseModel):
    """Represent the public API error contract."""

    model_config = ConfigDict(extra="forbid")

    code: str
    message: str
    details: list[ErrorDetail] = Field(default_factory=list)


def build_error_response(
    *,
    status_code: int,
    code: str,
    message: str,
    details: Iterable[ErrorDetail] = (),
) -> JSONResponse:
    """Build a safe JSON error response."""
    payload = ErrorResponse(
        code=code,
        message=message,
        details=list(details),
    )

    return JSONResponse(
        status_code=status_code,
        content=payload.model_dump(mode="json"),
    )


async def request_validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Return request-validation errors without echoing input values."""
    del request

    details: list[ErrorDetail] = []

    for error in exc.errors():
        location = [str(part) for part in error["loc"] if part != "body"]

        details.append(
            ErrorDetail(
                field=".".join(location) or "request",
                message=error["msg"],
                type=error["type"],
            )
        )

    return build_error_response(
        status_code=422,
        code="request_validation_error",
        message="request validation failed",
        details=details,
    )


__all__ = [
    "ErrorDetail",
    "ErrorResponse",
    "build_error_response",
    "request_validation_exception_handler",
]
