"""Tests for provider-independent model generation contracts."""

from pydantic import BaseModel, ConfigDict

from ai_data_governance_agent.providers import (
    ModelProvider,
    ProviderError,
)


class ExampleResponse(BaseModel):
    """Simple structured response used by provider contract tests."""

    model_config = ConfigDict(extra="forbid")

    answer: str
    confidence: float


class CompatibleProvider:
    """Minimal implementation satisfying the provider protocol."""

    @property
    def provider_name(self) -> str:
        return "compatible-test-provider"

    def generate_structured[T: BaseModel](
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[T],
    ) -> T:
        assert system_prompt
        assert user_prompt

        return response_model.model_validate(
            {
                "answer": "structured result",
                "confidence": 0.95,
            }
        )


class IncompatibleProvider:
    """Object intentionally missing structured generation."""

    @property
    def provider_name(self) -> str:
        return "incompatible"


def test_compatible_provider_satisfies_runtime_protocol() -> None:
    provider = CompatibleProvider()

    assert isinstance(provider, ModelProvider)


def test_incompatible_provider_does_not_satisfy_runtime_protocol() -> None:
    provider = IncompatibleProvider()

    assert not isinstance(provider, ModelProvider)


def test_provider_name_is_stable_string() -> None:
    provider: ModelProvider = CompatibleProvider()

    assert provider.provider_name == "compatible-test-provider"


def test_generate_structured_returns_requested_pydantic_model() -> None:
    provider: ModelProvider = CompatibleProvider()

    result = provider.generate_structured(
        system_prompt="Return a structured response.",
        user_prompt="Analyze the incident.",
        response_model=ExampleResponse,
    )

    assert isinstance(result, ExampleResponse)
    assert result.answer == "structured result"
    assert result.confidence == 0.95


def test_generate_structured_result_is_serializable() -> None:
    provider: ModelProvider = CompatibleProvider()

    result = provider.generate_structured(
        system_prompt="Return a structured response.",
        user_prompt="Analyze the incident.",
        response_model=ExampleResponse,
    )

    assert result.model_dump() == {
        "answer": "structured result",
        "confidence": 0.95,
    }


def test_protocol_does_not_require_inheritance() -> None:
    provider = CompatibleProvider()

    assert ModelProvider not in CompatibleProvider.__bases__
    assert isinstance(provider, ModelProvider)


def test_provider_error_is_runtime_error() -> None:
    error = ProviderError("provider failure")

    assert isinstance(error, RuntimeError)
    assert str(error) == "provider failure"


def test_provider_error_can_be_raised_and_caught() -> None:
    try:
        raise ProviderError("structured generation failed")
    except ProviderError as exc:
        assert str(exc) == "structured generation failed"
    else:
        raise AssertionError("ProviderError was not raised")


def test_multiple_response_models_are_supported() -> None:
    class AlternateResponse(BaseModel):
        answer: str
        confidence: float

    provider: ModelProvider = CompatibleProvider()

    result = provider.generate_structured(
        system_prompt="Return a structured response.",
        user_prompt="Analyze the incident.",
        response_model=AlternateResponse,
    )

    assert isinstance(result, AlternateResponse)


def test_provider_contract_operates_without_network_or_credentials() -> None:
    provider: ModelProvider = CompatibleProvider()

    result = provider.generate_structured(
        system_prompt="System instructions.",
        user_prompt="User instructions.",
        response_model=ExampleResponse,
    )

    assert result.answer == "structured result"
