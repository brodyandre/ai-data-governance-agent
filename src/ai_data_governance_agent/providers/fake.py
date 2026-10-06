"""Deterministic offline provider used by tests and local development."""

from collections.abc import Mapping

from pydantic import BaseModel

from ai_data_governance_agent.providers.base import ProviderError


class FakeProviderResponseNotConfiguredError(ProviderError):
    """Raised when no fake response exists for the requested model."""


class FakeProvider:
    """Return preconfigured structured responses without network access."""

    def __init__(
        self,
        *,
        responses: Mapping[
            type[BaseModel],
            BaseModel | Mapping[str, object],
        ]
        | None = None,
        error: ProviderError | None = None,
    ) -> None:
        self._responses = dict(responses or {})
        self._error = error

    @property
    def provider_name(self) -> str:
        """Return the stable identifier used by this provider."""
        return "fake"

    def generate_structured[T: BaseModel](
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[T],
    ) -> T:
        """Return the configured response for the requested model."""
        del system_prompt
        del user_prompt

        if self._error is not None:
            raise self._error

        configured_response = self._responses.get(response_model)

        if configured_response is None:
            raise FakeProviderResponseNotConfiguredError(
                f"no fake response configured for {response_model.__name__}"
            )

        if isinstance(configured_response, BaseModel):
            payload = configured_response.model_dump()
        else:
            payload = dict(configured_response)

        return response_model.model_validate(payload)


__all__ = [
    "FakeProvider",
    "FakeProviderResponseNotConfiguredError",
]
