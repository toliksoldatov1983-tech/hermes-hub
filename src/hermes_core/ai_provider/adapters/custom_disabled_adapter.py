"""Custom disabled provider adapter — placeholder for future custom providers."""

from __future__ import annotations

from hermes_core.ai_provider.adapters.base import BaseProviderAdapter
from hermes_core.ai_provider.contract import (
    AIProviderMetadata,
    AIProviderRequest,
    AIProviderResponse,
    ProviderCapability,
    SecretPolicy,
)


class CustomDisabledProviderAdapter(BaseProviderAdapter):
    """Placeholder for future custom providers.

    When someone wants to add a custom provider:
      1. Create a new adapter extending BaseProviderAdapter
      2. Register it in ai_provider/registry.py
      3. Define its capabilities, secret_policy and safety metadata
    """

    @property
    def metadata(self) -> AIProviderMetadata:
        return AIProviderMetadata(
            provider_id="custom-disabled",
            provider_name="Custom Provider (placeholder)",
            model_id="custom-default",
            mode="custom-disabled",
            capabilities=(
                ProviderCapability.TEXT_GENERATION,
                ProviderCapability.NETWORK_REQUIRED,
            ),
            secret_policy=SecretPolicy.SECRET_REQUIRED,
            requires_secret=True,
            requires_network=True,
            approval_required="APPROVE_SECRET_SETUP",
            is_enabled=False,
            blocked_reason=(
                "Custom provider requires a registered adapter, "
                "APPROVE_SECRET_SETUP, and explicit user approval."
            ),
        )

    def generate(self, request: AIProviderRequest) -> AIProviderResponse:
        return AIProviderResponse.blocked(
            self.metadata.blocked_reason,
            provider_id="custom-disabled",
        )
