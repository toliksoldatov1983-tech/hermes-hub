"""Mock provider adapter — safe local-only responses."""

from __future__ import annotations

from hermes_core.ai_provider.adapters.base import BaseProviderAdapter
from hermes_core.ai_provider.contract import (
    AIProviderMetadata,
    AIProviderRequest,
    AIProviderResponse,
    ProviderCapability,
    SecretPolicy,
)


class MockProviderAdapter(BaseProviderAdapter):
    """Safe mock adapter — generates local-only synthetic responses."""

    @property
    def metadata(self) -> AIProviderMetadata:
        return AIProviderMetadata(
            provider_id="mock",
            provider_name="Mock Provider",
            model_id="mock-default",
            mode="mock",
            capabilities=(
                ProviderCapability.TEXT_GENERATION,
                ProviderCapability.REVIEW,
                ProviderCapability.JSON_MODE,
            ),
            secret_policy=SecretPolicy.NO_SECRET_REQUIRED,
            requires_secret=False,
            requires_network=False,
            approval_required="",
            is_enabled=True,
        )

    def generate(self, request: AIProviderRequest) -> AIProviderResponse:
        return AIProviderResponse(
            text=f"MOCK: {request.truncated_prompt()}",
            provider_id="mock",
            provider_name="Mock Provider",
            model_id="mock-default",
            is_mock=True,
            safety={
                "real_api_called": False,
                "env_read": False,
                "token_used": False,
                "network_called": False,
            },
        )

    def generate_review(self, code: str) -> AIProviderResponse:
        return AIProviderResponse(
            text="MOCK_REVIEW: Code review completed locally. No external review provider configured.",
            provider_id="mock",
            provider_name="Mock Provider",
            model_id="mock-default",
            is_mock=True,
        )
