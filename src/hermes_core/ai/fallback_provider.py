from __future__ import annotations

from hermes_core.ai.mock_provider import MockProvider


class FallbackProvider(MockProvider):
    """Safe fallback until DeepSeek / DeepSig keys are explicitly configured."""

    pass
