"""Tests for the deterministic offline FakeProvider."""

import socket

import pytest
from pydantic import BaseModel, ConfigDict, ValidationError

from ai_data_governance_agent.providers import (
    FakeProvider,
    FakeProviderResponseNotConfiguredError,
    ModelProvider,
    ProviderError,
)


class ExampleResponse(BaseModel):
    """Primary structured response used by FakeProvider tests."""

    model_config = ConfigDict(extra="forbid")

    message: str
    confidence: float


class AlternateResponse(BaseModel):
    """Secondary response proving support for multiple models."""

    model_config = ConfigDict(extra="forbid")

    category: str
    approved: bool


class ListResponse(BaseModel):
    """Response containing mutable structured data."""

    model_config = ConfigDict(extra="forbid")

    items: list[str]


def test_provider_name_is_fake() -> None:
    provider = FakeProvider()

    assert provider.provider_name == "fake"


def test_fake_provider_satisfies_model_provider_protocol() -> None:
    provider = FakeProvider()

    assert isinstance(provider, ModelProvider)


def test_mapping_configuration_returns_requested_model() -> None:
    provider = FakeProvider(
        responses={
            ExampleResponse: {
                "message": "deterministic",
                "confidence": 0.95,
            }
        }
    )

    result = provider.generate_structured(
        system_prompt="System.",
        user_prompt="User.",
        response_model=ExampleResponse,
    )

    assert isinstance(result, ExampleResponse)
    assert result.message == "deterministic"
    assert result.confidence == 0.95


def test_basemodel_configuration_returns_requested_model() -> None:
    configured = ExampleResponse(
        message="configured model",
        confidence=0.90,
    )
    provider = FakeProvider(
        responses={
            ExampleResponse: configured,
        }
    )

    result = provider.generate_structured(
        system_prompt="System.",
        user_prompt="User.",
        response_model=ExampleResponse,
    )

    assert isinstance(result, ExampleResponse)
    assert result == configured


def test_basemodel_configuration_returns_new_instance() -> None:
    configured = ExampleResponse(
        message="configured model",
        confidence=0.90,
    )
    provider = FakeProvider(
        responses={
            ExampleResponse: configured,
        }
    )

    result = provider.generate_structured(
        system_prompt="System.",
        user_prompt="User.",
        response_model=ExampleResponse,
    )

    assert result is not configured


def test_repeated_calls_are_reproducible() -> None:
    provider = FakeProvider(
        responses={
            ExampleResponse: {
                "message": "same response",
                "confidence": 0.88,
            }
        }
    )

    first = provider.generate_structured(
        system_prompt="System.",
        user_prompt="User.",
        response_model=ExampleResponse,
    )
    second = provider.generate_structured(
        system_prompt="System.",
        user_prompt="User.",
        response_model=ExampleResponse,
    )

    assert first == second
    assert first.model_dump() == second.model_dump()


def test_repeated_calls_return_independent_mutable_data() -> None:
    provider = FakeProvider(
        responses={
            ListResponse: {
                "items": ["one", "two"],
            }
        }
    )

    first = provider.generate_structured(
        system_prompt="System.",
        user_prompt="User.",
        response_model=ListResponse,
    )
    first.items.append("three")

    second = provider.generate_structured(
        system_prompt="System.",
        user_prompt="User.",
        response_model=ListResponse,
    )

    assert first.items == ["one", "two", "three"]
    assert second.items == ["one", "two"]


def test_prompts_do_not_change_preconfigured_response() -> None:
    provider = FakeProvider(
        responses={
            ExampleResponse: {
                "message": "fixed",
                "confidence": 1.0,
            }
        }
    )

    first = provider.generate_structured(
        system_prompt="First system prompt.",
        user_prompt="First user prompt.",
        response_model=ExampleResponse,
    )
    second = provider.generate_structured(
        system_prompt="Completely different system prompt.",
        user_prompt="Completely different user prompt.",
        response_model=ExampleResponse,
    )

    assert first == second


def test_multiple_response_models_are_supported() -> None:
    provider = FakeProvider(
        responses={
            ExampleResponse: {
                "message": "example",
                "confidence": 0.75,
            },
            AlternateResponse: {
                "category": "governance",
                "approved": True,
            },
        }
    )

    example = provider.generate_structured(
        system_prompt="System.",
        user_prompt="User.",
        response_model=ExampleResponse,
    )
    alternate = provider.generate_structured(
        system_prompt="System.",
        user_prompt="User.",
        response_model=AlternateResponse,
    )

    assert isinstance(example, ExampleResponse)
    assert isinstance(alternate, AlternateResponse)
    assert alternate.category == "governance"
    assert alternate.approved is True


def test_missing_response_raises_specific_error() -> None:
    provider = FakeProvider()

    with pytest.raises(
        FakeProviderResponseNotConfiguredError,
        match="no fake response configured for ExampleResponse",
    ):
        provider.generate_structured(
            system_prompt="System.",
            user_prompt="User.",
            response_model=ExampleResponse,
        )


def test_missing_response_error_is_provider_error() -> None:
    error = FakeProviderResponseNotConfiguredError("missing")

    assert isinstance(error, ProviderError)


def test_configured_error_is_raised() -> None:
    provider = FakeProvider(error=ProviderError("simulated failure"))

    with pytest.raises(
        ProviderError,
        match="simulated failure",
    ):
        provider.generate_structured(
            system_prompt="System.",
            user_prompt="User.",
            response_model=ExampleResponse,
        )


def test_configured_error_has_precedence_over_response() -> None:
    provider = FakeProvider(
        responses={
            ExampleResponse: {
                "message": "would otherwise succeed",
                "confidence": 0.99,
            }
        },
        error=ProviderError("forced failure"),
    )

    with pytest.raises(
        ProviderError,
        match="forced failure",
    ):
        provider.generate_structured(
            system_prompt="System.",
            user_prompt="User.",
            response_model=ExampleResponse,
        )


def test_invalid_configured_payload_is_rejected_by_pydantic() -> None:
    provider = FakeProvider(
        responses={
            ExampleResponse: {
                "message": "missing confidence",
            }
        }
    )

    with pytest.raises(ValidationError):
        provider.generate_structured(
            system_prompt="System.",
            user_prompt="User.",
            response_model=ExampleResponse,
        )


def test_extra_configured_fields_are_rejected_by_response_model() -> None:
    provider = FakeProvider(
        responses={
            ExampleResponse: {
                "message": "invalid",
                "confidence": 0.50,
                "unexpected": True,
            }
        }
    )

    with pytest.raises(ValidationError):
        provider.generate_structured(
            system_prompt="System.",
            user_prompt="User.",
            response_model=ExampleResponse,
        )


def test_external_response_mapping_changes_do_not_replace_configuration() -> None:
    responses = {
        ExampleResponse: {
            "message": "original",
            "confidence": 0.80,
        }
    }

    provider = FakeProvider(responses=responses)
    responses.clear()

    result = provider.generate_structured(
        system_prompt="System.",
        user_prompt="User.",
        response_model=ExampleResponse,
    )

    assert result.message == "original"


def test_provider_operates_without_provider_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for variable in (
        "OPENAI_API_KEY",
        "OCI_CONFIG_FILE",
        "ANTHROPIC_API_KEY",
        "GOOGLE_API_KEY",
    ):
        monkeypatch.delenv(variable, raising=False)

    provider = FakeProvider(
        responses={
            ExampleResponse: {
                "message": "offline",
                "confidence": 1.0,
            }
        }
    )

    result = provider.generate_structured(
        system_prompt="System.",
        user_prompt="User.",
        response_model=ExampleResponse,
    )

    assert result.message == "offline"


def test_provider_does_not_require_network(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_network(*args: object, **kwargs: object) -> None:
        raise AssertionError("FakeProvider attempted to access the network")

    monkeypatch.setattr(
        socket,
        "create_connection",
        fail_network,
    )

    provider = FakeProvider(
        responses={
            ExampleResponse: {
                "message": "offline",
                "confidence": 1.0,
            }
        }
    )

    result = provider.generate_structured(
        system_prompt="System.",
        user_prompt="User.",
        response_model=ExampleResponse,
    )

    assert result.message == "offline"
