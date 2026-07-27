"""Provider Registry — centrally registers all AI provider adapters.

Adding a new provider:
  1. Create a new adapter in adapters/ extending BaseProviderAdapter
  2. Register it in this file via registry.register()
  3. The core router, CLI, and tests work without changes.
"""

from __future__ import annotations

from hermes_core.ai_provider.adapters.base import BaseProviderAdapter
from hermes_core.ai_provider.adapters.mock_adapter import MockProviderAdapter
from hermes_core.ai_provider.adapters.gemini_adapter import GeminiProviderAdapter
from hermes_core.ai_provider.adapters.deepseek_adapter import DeepSeekProviderAdapter
from hermes_core.ai_provider.adapters.local_disabled_adapter import LocalDisabledProviderAdapter
from hermes_core.ai_provider.adapters.ollama_disabled_adapter import OllamaDisabledProviderAdapter
from hermes_core.ai_provider.adapters.custom_disabled_adapter import CustomDisabledProviderAdapter
from hermes_core.ai_provider.adapters.review_adapter import (
    DeepSeekReviewDisabledAdapter,
    MockReviewAdapter,
)


class ProviderRegistry:
    """Registry of all available AI provider adapters.

    Providers register themselves with a unique provider_id.
    The registry is the single source of truth for available providers.
    """

    def __init__(self) -> None:
        self._providers: dict[str, BaseProviderAdapter] = {}

    def register(self, adapter: BaseProviderAdapter) -> None:
        """Register a provider adapter by its provider_id."""
        pid = adapter.metadata.provider_id
        self._providers[pid] = adapter

    def get(self, provider_id: str) -> BaseProviderAdapter | None:
        """Get a provider adapter by ID, or None if not found."""
        return self._providers.get(provider_id)

    def list_all(self) -> list[BaseProviderAdapter]:
        """List all registered provider adapters."""
        return list(self._providers.values())

    def list_enabled(self) -> list[BaseProviderAdapter]:
        """List only providers that are enabled and can_use_now."""
        return [p for p in self._providers.values() if p.metadata.can_use_now]

    def list_disabled(self) -> list[BaseProviderAdapter]:
        """List providers that are disabled or blocked."""
        return [p for p in self._providers.values() if not p.metadata.can_use_now]

    def list_ids(self) -> list[str]:
        return list(self._providers.keys())

    def count(self) -> int:
        return len(self._providers)


# ── Global default registry ──

_default_registry = ProviderRegistry()


def get_default_registry() -> ProviderRegistry:
    """Get or create the default global registry with all built-in adapters."""
    if not _default_registry.list_all():
        _default_registry.register(MockProviderAdapter())
        _default_registry.register(GeminiProviderAdapter())
        _default_registry.register(DeepSeekProviderAdapter())
        _default_registry.register(LocalDisabledProviderAdapter())
        _default_registry.register(OllamaDisabledProviderAdapter())
        _default_registry.register(CustomDisabledProviderAdapter())
        _default_registry.register(MockReviewAdapter())
        _default_registry.register(DeepSeekReviewDisabledAdapter())
    return _default_registry


def reset_default_registry() -> None:
    """Reset the default registry (for testing)."""
    global _default_registry
    _default_registry = ProviderRegistry()
