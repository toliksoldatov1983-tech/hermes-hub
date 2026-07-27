"""Base provider adapter — all adapters must extend this."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from hermes_core.ai_provider.contract import (
    AIProviderMetadata,
    AIProviderRequest,
    AIProviderResponse,
)


class BaseProviderAdapter(ABC):
    """Abstract base for all AI provider adapters.

    Subclasses must provide:
      - metadata: static AIProviderMetadata describing the provider
      - generate(): produce a response for a given request
      - generate_review(): optional review method (default returns blocked)
    """

    @property
    @abstractmethod
    def metadata(self) -> AIProviderMetadata:
        ...

    @abstractmethod
    def generate(self, request: AIProviderRequest) -> AIProviderResponse:
        ...

    def generate_review(self, code: str) -> AIProviderResponse:
        """Optional review method. Default returns blocked."""
        return AIProviderResponse.blocked(
            f"{self.metadata.provider_id} does not support code review.",
            provider_id=self.metadata.provider_id,
        )

    def __repr__(self) -> str:
        m = self.metadata
        return f"{type(self).__name__}(id={m.provider_id}, enabled={m.is_enabled})"
