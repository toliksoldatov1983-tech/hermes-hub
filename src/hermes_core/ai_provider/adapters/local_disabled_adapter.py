"""Local disabled provider adapter — placeholder for future local providers."""

from __future__ import annotations

from hermes_core.ai_provider.adapters.base import BaseProviderAdapter
from hermes_core.ai_provider.contract import (
    AIProviderMetadata,
    AIProviderRequest,
    AIProviderResponse,
    ProviderCapability,
    SecretPolicy,
)


class LocalDisabledProviderAdapter(BaseProviderAdapter):
    """Placeholder for future local-only providers (e.g. local LLM)."""

    @property
    def metadata(self) -> AIProviderMetadata:
        return AIProviderMetadata(
            provider_id="local-disabled",
            provider_name="Local LLM (placeholder)",
            model_id="local-default",
            mode="local-disabled",
            capabilities=(
                ProviderCapability.TEXT_GENERATION,
                ProviderCapability.LOCAL_ONLY,
            ),
            secret_policy=SecretPolicy.NO_SECRET_REQUIRED,
            requires_secret=False,
            requires_network=False,
            approval_required="",
            is_enabled=False,
            blocked_reason="Local LLM provider is not implemented yet.",
        )

    def generate(self, request: AIProviderRequest) -> AIProviderResponse:
        return AIProviderResponse.blocked(
            self.metadata.blocked_reason,
            provider_id="local-disabled",
        )
