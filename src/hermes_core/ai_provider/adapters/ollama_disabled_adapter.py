"""Ollama disabled provider adapter — placeholder for future Ollama provider."""

from __future__ import annotations

from hermes_core.ai_provider.adapters.base import BaseProviderAdapter
from hermes_core.ai_provider.contract import (
    AIProviderMetadata,
    AIProviderRequest,
    AIProviderResponse,
    ProviderCapability,
    SecretPolicy,
)


class OllamaDisabledProviderAdapter(BaseProviderAdapter):
    """Placeholder for future Ollama integration."""

    @property
    def metadata(self) -> AIProviderMetadata:
        return AIProviderMetadata(
            provider_id="ollama-disabled",
            provider_name="Ollama (placeholder)",
            model_id="ollama-default",
            mode="ollama-disabled",
            capabilities=(
                ProviderCapability.TEXT_GENERATION,
                ProviderCapability.REVIEW,
                ProviderCapability.LOCAL_ONLY,
            ),
            secret_policy=SecretPolicy.NO_SECRET_REQUIRED,
            requires_secret=False,
            requires_network=False,
            approval_required="",
            is_enabled=False,
            blocked_reason="Ollama provider is not implemented yet.",
        )

    def generate(self, request: AIProviderRequest) -> AIProviderResponse:
        return AIProviderResponse.blocked(
            self.metadata.blocked_reason,
            provider_id="ollama-disabled",
        )
