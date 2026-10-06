"""Provider-independent contracts for structured model generation."""

from typing import Protocol, runtime_checkable

from pydantic import BaseModel


class ProviderError(RuntimeError):
    """Base error raised by model provider implementations."""


@runtime_checkable
class ModelProvider(Protocol):
    """Contract implemented by model providers used by the agent."""

    @property
    def provider_name(self) -> str:
        """Return a stable provider identifier."""
        ...

    def generate_structured[T: BaseModel](
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[T],
    ) -> T:
        """Generate and validate a structured response."""
        ...


__all__ = [
    "ModelProvider",
    "ProviderError",
]
