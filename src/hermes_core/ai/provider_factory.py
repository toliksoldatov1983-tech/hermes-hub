from __future__ import annotations

from dataclasses import dataclass

from hermes_core.ai.fallback_provider import FallbackProvider
from hermes_core.ai.gemini_provider import GeminiProvider
from hermes_core.ai.mock_provider import MockProvider
from hermes_core.ai.provider_contract import AIProvider


@dataclass(frozen=True)
class ProviderConfig:
    mode: str = "mock"
    secret_setup_approved: bool = False
    gemini_key_available: bool = False
    deepseek_key_available: bool = False


@dataclass(frozen=True)
class ProviderSelection:
    provider: AIProvider
    provider_name: str
    mode: str
    blocked_reason: str | None = None

    @property
    def is_blocked(self) -> bool:
        return self.blocked_reason is not None


class ProviderFactory:
    def select(self, config: ProviderConfig | None = None) -> ProviderSelection:
        config = config or ProviderConfig()
        mode = config.mode.strip().lower()

        if mode in {"", "mock"}:
            return ProviderSelection(MockProvider(), "mock", "mock")

        if mode in {"fallback", "deepseek-disabled", "deepsig-disabled"}:
            return ProviderSelection(FallbackProvider(), "fallback-mock", mode)

        if mode == "gemini-disabled":
            return ProviderSelection(
                GeminiProvider(enabled=False),
                "gemini",
                mode,
                "Gemini is disabled until APPROVE_SECRET_SETUP.",
            )

        if mode == "gemini":
            if not config.secret_setup_approved:
                return ProviderSelection(
                    GeminiProvider(enabled=False),
                    "gemini",
                    mode,
                    "APPROVE_SECRET_SETUP is required before Gemini can be enabled.",
                )
            if not config.gemini_key_available:
                return ProviderSelection(
                    GeminiProvider(enabled=False),
                    "gemini",
                    mode,
                    "GEMINI_API_KEY availability must be confirmed without storing the key.",
                )
            return ProviderSelection(
                GeminiProvider(enabled=False),
                "gemini",
                mode,
                "Real Gemini client is not implemented in this local-safe block.",
            )

        return ProviderSelection(MockProvider(), "mock", "mock", f"Unknown provider mode: {config.mode}")
