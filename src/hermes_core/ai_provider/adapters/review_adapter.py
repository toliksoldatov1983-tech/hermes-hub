"""Review provider adapter — universal review through BaseProviderAdapter.

This adapter gives the old review_provider_factory a path into the new
universal AI Provider architecture without rewriting the factory immediately.
"""

from __future__ import annotations

from hermes_core.ai_provider.adapters.base import BaseProviderAdapter
from hermes_core.ai_provider.contract import (
    AIProviderMetadata,
    AIProviderRequest,
    AIProviderResponse,
    ProviderCapability,
    SecretPolicy,
)


class MockReviewAdapter(BaseProviderAdapter):
    """Mock review adapter — local-only review, no external API."""

    @property
    def metadata(self) -> AIProviderMetadata:
        return AIProviderMetadata(
            provider_id="mock-review",
            provider_name="Mock Review Provider",
            model_id="mock-review-default",
            mode="mock-review",
            capabilities=(
                ProviderCapability.REVIEW,
                ProviderCapability.TEXT_GENERATION,
            ),
            secret_policy=SecretPolicy.NO_SECRET_REQUIRED,
            requires_secret=False,
            requires_network=False,
            approval_required="",
            is_enabled=True,
        )

    def generate(self, request: AIProviderRequest) -> AIProviderResponse:
        return AIProviderResponse(
            text=f"MOCK_REVIEW: {request.truncated_prompt()}",
            provider_id="mock-review",
            provider_name="Mock Review Provider",
            model_id="mock-review-default",
            is_mock=True,
            safety={
                "real_api_called": False,
                "env_read": False,
                "token_used": False,
                "network_called": False,
            },
        )

    def generate_review(self, code: str) -> AIProviderResponse:
        """Mock code review — local only, pattern-based."""
        return AIProviderResponse(
            text=_detect_review_pattern(code),
            provider_id="mock-review",
            provider_name="Mock Review Provider",
            model_id="mock-review-default",
            is_mock=True,
            safety={
                "real_api_called": False,
                "env_read": False,
                "token_used": False,
                "network_called": False,
            },
        )


class DeepSeekReviewDisabledAdapter(BaseProviderAdapter):
    """DeepSeek review adapter — always disabled in safe-local mode."""

    @property
    def metadata(self) -> AIProviderMetadata:
        return AIProviderMetadata(
            provider_id="deepseek-review-disabled",
            provider_name="DeepSeek Review",
            model_id="deepseek-chat",
            mode="deepseek-review-disabled",
            capabilities=(
                ProviderCapability.REVIEW,
                ProviderCapability.TEXT_GENERATION,
                ProviderCapability.NETWORK_REQUIRED,
            ),
            secret_policy=SecretPolicy.BLOCKED_UNTIL_APPROVE_SECRET_SETUP,
            requires_secret=True,
            requires_network=True,
            approval_required="APPROVE_SECRET_SETUP",
            is_enabled=False,
            blocked_reason="DeepSeek review is disabled until APPROVE_SECRET_SETUP is granted.",
        )

    def generate(self, request: AIProviderRequest) -> AIProviderResponse:
        return AIProviderResponse.blocked(
            self.metadata.blocked_reason,
            provider_id="deepseek-review-disabled",
        )

    def generate_review(self, code: str) -> AIProviderResponse:
        return AIProviderResponse.blocked(
            self.metadata.blocked_reason,
            provider_id="deepseek-review-disabled",
        )


# ── Mock review pattern detection ──

_MOCK_PATTERNS = {
    "safety": "MOCK_REVIEW [safety]: Code passes local safety checks. No secrets, no external calls detected.",
    "structure": "MOCK_REVIEW [structure]: Code follows Hermes-Clean conventions. Module boundaries respected.",
    "malyarka": "MOCK_REVIEW [malyarka]: Malyarka module uses synthetic data only. Export gate enforced.",
    "telegram": "MOCK_REVIEW [telegram]: Telegram module is dry-run only. No live polling/webhook.",
    "general": "MOCK_REVIEW [general]: Local mock review completed. No external review provider configured.",
}


def _detect_review_pattern(code: str) -> str:
    lowered = code.lower()
    if "token" in lowered or "secret" in lowered or "api_key" in lowered:
        return _MOCK_PATTERNS["safety"]
    if "malyarka" in lowered or "order" in lowered:
        return _MOCK_PATTERNS["malyarka"]
    if "telegram" in lowered or "polling" in lowered:
        return _MOCK_PATTERNS["telegram"]
    if "class " in lowered or "def " in lowered:
        return _MOCK_PATTERNS["structure"]
    return _MOCK_PATTERNS["general"]
