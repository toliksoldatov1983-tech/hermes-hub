"""Universal AI Provider Contract — provider-neutral interface.

This module defines the core types for any AI provider adapter.
No provider-specific logic. No secrets. No network calls.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class ProviderCapability(Enum):
    """Capabilities an AI provider may support."""

    TEXT_GENERATION = auto()
    REVIEW = auto()
    VISION = auto()
    EMBEDDINGS = auto()
    TOOL_CALLING = auto()
    JSON_MODE = auto()
    LONG_CONTEXT = auto()
    LOCAL_ONLY = auto()
    NETWORK_REQUIRED = auto()


class SecretPolicy(Enum):
    """How a provider handles secrets."""

    NO_SECRET_REQUIRED = auto()
    SECRET_REQUIRED = auto()
    SECRET_NOT_LOADED = auto()
    APPROVAL_REQUIRED = auto()
    BLOCKED_UNTIL_APPROVE_SECRET_SETUP = auto()


@dataclass(frozen=True)
class AIProviderRequest:
    """Request object sent to any provider."""

    prompt: str = ""
    system_prompt: str = ""
    temperature: float = 0.7
    max_tokens: int = 1024
    capabilities: tuple[ProviderCapability, ...] = ()

    def truncated_prompt(self, max_len: int = 500) -> str:
        if len(self.prompt) <= max_len:
            return self.prompt
        return self.prompt[:max_len] + "..."


@dataclass(frozen=True)
class AIProviderResponse:
    """Response object from any provider."""

    text: str
    provider_id: str = ""
    provider_name: str = ""
    model_id: str = ""
    is_mock: bool = True
    is_blocked: bool = False
    blocked_reason: str = ""
    safety: dict[str, Any] = field(default_factory=lambda: {
        "real_api_called": False,
        "env_read": False,
        "token_used": False,
        "network_called": False,
    })

    @staticmethod
    def blocked(reason: str, provider_id: str = "unknown") -> "AIProviderResponse":
        return AIProviderResponse(
            text=f"BLOCKED: {reason}",
            provider_id=provider_id,
            provider_name=provider_id,
            is_mock=True,
            is_blocked=True,
            blocked_reason=reason,
        )

    @staticmethod
    def error(message: str, provider_id: str = "unknown") -> "AIProviderResponse":
        return AIProviderResponse(
            text=f"ERROR: {message}",
            provider_id=provider_id,
            provider_name=provider_id,
            is_mock=True,
            is_blocked=True,
            blocked_reason=message,
        )


@dataclass(frozen=True)
class AIProviderMetadata:
    """Metadata describing a registered provider adapter."""

    provider_id: str
    provider_name: str
    model_id: str
    mode: str
    capabilities: tuple[ProviderCapability, ...]
    secret_policy: SecretPolicy
    requires_secret: bool = False
    requires_network: bool = False
    approval_required: str = ""
    is_enabled: bool = True
    blocked_reason: str = ""

    @property
    def is_blocked(self) -> bool:
        return bool(self.blocked_reason) or not self.is_enabled

    @property
    def can_use_now(self) -> bool:
        return (
            self.is_enabled
            and not self.requires_secret
            and not self.requires_network
            and not self.blocked_reason
        )
