"""Universal AI Provider module — provider-neutral architecture.

This is the NEW provider layer. Old files in hermes_core/ai/ are preserved
for backward compatibility with existing CLI commands.
"""

from hermes_core.ai_provider.contract import (
    AIProviderMetadata,
    AIProviderRequest,
    AIProviderResponse,
    ProviderCapability,
    SecretPolicy,
)
from hermes_core.ai_provider.registry import (
    ProviderRegistry,
    get_default_registry,
    reset_default_registry,
)
from hermes_core.ai_provider.router import AIProviderRouter, RouterDecision

__all__ = [
    "AIProviderMetadata",
    "AIProviderRequest",
    "AIProviderResponse",
    "AIProviderRouter",
    "ProviderCapability",
    "ProviderRegistry",
    "RouterDecision",
    "SecretPolicy",
    "get_default_registry",
    "reset_default_registry",
]
