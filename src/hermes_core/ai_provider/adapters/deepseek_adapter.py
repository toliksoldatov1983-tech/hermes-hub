"""DeepSeek provider adapter — second real provider adapter, disabled in safe mode."""

from __future__ import annotations

from hermes_core.ai_provider.adapters.base import BaseProviderAdapter
from hermes_core.ai_provider.contract import (
    AIProviderMetadata,
    AIProviderRequest,
    AIProviderResponse,
    ProviderCapability,
    SecretPolicy,
)


class DeepSeekProviderAdapter(BaseProviderAdapter):
    """DeepSeek adapter — always disabled in local-safe mode.

    Future capabilities (documented but never activated without approval):
      - text_generation, review, embeddings, tool_calling, json_mode, long_context
    """

    @property
    def metadata(self) -> AIProviderMetadata:
        return AIProviderMetadata(
            provider_id="deepseek-disabled",
            provider_name="DeepSeek",
            model_id="deepseek-chat",
            mode="deepseek-disabled",
            capabilities=(
                ProviderCapability.TEXT_GENERATION,
                ProviderCapability.REVIEW,
                ProviderCapability.EMBEDDINGS,
                ProviderCapability.TOOL_CALLING,
                ProviderCapability.JSON_MODE,
                ProviderCapability.LONG_CONTEXT,
                ProviderCapability.NETWORK_REQUIRED,
            ),
            secret_policy=SecretPolicy.BLOCKED_UNTIL_APPROVE_SECRET_SETUP,
            requires_secret=True,
            requires_network=True,
            approval_required="APPROVE_SECRET_SETUP",
            is_enabled=False,
            blocked_reason="DeepSeek is disabled until APPROVE_SECRET_SETUP is granted.",
        )

    def generate(self, request: AIProviderRequest) -> AIProviderResponse:
        return AIProviderResponse.blocked(
            self.metadata.blocked_reason,
            provider_id="deepseek-disabled",
        )
