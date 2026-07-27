"""Provider Router — safe selection of AI provider in local mode.

The router enforces:
  - mock provider is always allowed
  - real providers requiring secret are BLOCKED without APPROVE_SECRET_SETUP
  - real providers requiring network are BLOCKED without explicit approval
  - unknown providers are BLOCKED
"""

from __future__ import annotations

from dataclasses import dataclass

from hermes_core.ai_provider.contract import (
    AIProviderMetadata,
    AIProviderRequest,
    AIProviderResponse,
    ProviderCapability,
    SecretPolicy,
)
from hermes_core.ai_provider.registry import ProviderRegistry, get_default_registry


@dataclass(frozen=True)
class RouterDecision:
    provider_id: str
    provider_name: str
    mode: str
    is_blocked: bool = False
    blocked_reason: str = ""
    metadata: AIProviderMetadata | None = None

    def to_response(self, request: AIProviderRequest) -> AIProviderResponse:
        if self.is_blocked or not self.metadata:
            return AIProviderResponse.blocked(
                self.blocked_reason or "No provider selected.",
                provider_id=self.provider_id,
            )
        adapter = None  # resolved at use time
        return AIProviderResponse(
            text="",
            provider_id=self.provider_id,
            provider_name=self.provider_name,
            is_mock=True,
            is_blocked=self.is_blocked,
            blocked_reason=self.blocked_reason,
        )


class AIProviderRouter:
    """Safe local router that selects a provider with policy enforcement."""

    def __init__(self, registry: ProviderRegistry | None = None) -> None:
        self._registry = registry or get_default_registry()

    def select(
        self,
        provider_id: str = "mock",
        approved: bool = False,
        mode: str = "safe_local",
    ) -> RouterDecision:
        """Select a provider by ID, enforcing safety policy.

        Args:
            provider_id: The registered provider_id to select.
            approved: Whether APPROVE_SECRET_SETUP has been granted.
            mode: Router mode (safe_local, dry_run, etc.)

        Returns:
            RouterDecision with selection result and any blocking reason.
        """
        pid = provider_id.strip().lower()

        # Unknown provider — always blocked
        adapter = self._registry.get(pid)
        if adapter is None:
            return RouterDecision(
                provider_id=pid,
                provider_name=pid,
                mode=mode,
                is_blocked=True,
                blocked_reason=f"Unknown provider: {pid}. Use 'ai-provider-list' to see available providers.",
            )

        meta = adapter.metadata

        # Mock is always allowed
        if pid == "mock":
            return RouterDecision(
                provider_id=pid,
                provider_name=meta.provider_name,
                mode=mode,
                metadata=meta,
            )

        # Blocked provider — hard coded
        if meta.is_blocked:
            return RouterDecision(
                provider_id=pid,
                provider_name=meta.provider_name,
                mode=mode,
                is_blocked=True,
                blocked_reason=meta.blocked_reason or f"{pid} is blocked in this mode.",
                metadata=meta,
            )

        # Provider requiring secret — blocked without approval
        if meta.requires_secret and not approved:
            return RouterDecision(
                provider_id=pid,
                provider_name=meta.provider_name,
                mode=mode,
                is_blocked=True,
                blocked_reason=(
                    f"{pid} requires APPROVE_SECRET_SETUP before it can be enabled. "
                    f"Secret policy: {meta.secret_policy.value}"
                ),
                metadata=meta,
            )

        # Provider requiring network — blocked in safe_local
        if meta.requires_network and mode == "safe_local":
            return RouterDecision(
                provider_id=pid,
                provider_name=meta.provider_name,
                mode=mode,
                is_blocked=True,
                blocked_reason=f"{pid} requires network access, which is blocked in {mode} mode.",
                metadata=meta,
            )

        # Everything checks out (should not happen for real providers in safe_local)
        return RouterDecision(
            provider_id=pid,
            provider_name=meta.provider_name,
            mode=mode,
            is_blocked=not meta.can_use_now,
            blocked_reason=meta.blocked_reason if not meta.can_use_now else "",
            metadata=meta,
        )

    def select_safe(self) -> RouterDecision:
        """Select the default safe provider (mock)."""
        return self.select("mock")

    def list_providers(self) -> list[RouterDecision]:
        """List all registered providers with their status."""
        results: list[RouterDecision] = []
        for adapter in self._registry.list_all():
            meta = adapter.metadata
            results.append(
                RouterDecision(
                    provider_id=meta.provider_id,
                    provider_name=meta.provider_name,
                    mode=meta.mode,
                    is_blocked=meta.is_blocked,
                    blocked_reason=meta.blocked_reason,
                    metadata=meta,
                )
            )
        return results

    def generate(
        self,
        provider_id: str = "mock",
        request: AIProviderRequest | None = None,
        approved: bool = False,
    ) -> AIProviderResponse:
        """Generate a response using the selected provider via the router."""
        decision = self.select(provider_id, approved=approved)
        if decision.is_blocked:
            return AIProviderResponse.blocked(
                decision.blocked_reason,
                provider_id=provider_id,
            )
        adapter = self._registry.get(provider_id)
        if adapter is None:
            return AIProviderResponse.blocked(
                f"Provider '{provider_id}' not found.",
                provider_id=provider_id,
            )
        return adapter.generate(request or AIProviderRequest())
