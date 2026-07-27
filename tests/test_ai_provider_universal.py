"""Tests for the universal AI provider layer.

Tests verify:
  - Provider registry works correctly
  - Router enforces safety policy
  - Unknown providers are blocked
  - Mock provider works
  - Gemini/DeepSeek are disabled by default
  - New provider can be registered without changing core
  - No secrets, no API calls, no env reading
"""

from __future__ import annotations

from hermes_core.ai_provider import (
    AIProviderRequest,
    AIProviderResponse,
    AIProviderRouter,
    ProviderCapability,
    SecretPolicy,
    get_default_registry,
    reset_default_registry,
)
from hermes_core.ai_provider.adapters.base import BaseProviderAdapter
from hermes_core.ai_provider.contract import AIProviderMetadata


# ── Registry tests ──
def test_registry_has_providers():
    """Registry has expected providers (original + review adapters)."""
    from hermes_core.ai_provider import get_default_registry, reset_default_registry
    reset_default_registry()
    reg = get_default_registry()
    assert reg.count() >= 8  # 6 original + 2 review adapters
    ids = reg.list_ids()
    assert "mock" in ids
    assert "gemini-disabled" in ids
    assert "deepseek-disabled" in ids
    assert "local-disabled" in ids
    assert "ollama-disabled" in ids
    assert "custom-disabled" in ids


def test_registry_get_mock():
    reset_default_registry()
    reg = get_default_registry()
    adapter = reg.get("mock")
    assert adapter is not None
    assert adapter.metadata.provider_id == "mock"
    assert adapter.metadata.is_enabled
    assert not adapter.metadata.is_blocked


def test_registry_get_unknown():
    reset_default_registry()
    reg = get_default_registry()
    assert reg.get("nonexistent") is None


def test_registry_new_provider_can_be_added_without_core_change():
    """Verify adding a new provider = create adapter + register.
    No core changes needed."""
    reset_default_registry()
    reg = get_default_registry()

    # Simulate adding a new provider
    class TestAdapter(BaseProviderAdapter):
        @property
        def metadata(self) -> AIProviderMetadata:
            return AIProviderMetadata(
                provider_id="test-new",
                provider_name="Test New Provider",
                model_id="test-model",
                mode="test-mode",
                capabilities=(ProviderCapability.TEXT_GENERATION,),
                secret_policy=SecretPolicy.NO_SECRET_REQUIRED,
                requires_secret=False,
                requires_network=False,
            )

        def generate(self, request: AIProviderRequest) -> AIProviderResponse:
            return AIProviderResponse(text="TEST")

    reg.register(TestAdapter())
    assert reg.count() == 9  # 8 default + 1 custom
    assert reg.get("test-new") is not None

    # Router can select it
    router = AIProviderRouter(reg)
    decision = router.select("test-new")
    assert not decision.is_blocked
    assert decision.metadata is not None

    # Clean up
    reset_default_registry()


def test_registry_list_enabled():
    reset_default_registry()
    reg = get_default_registry()
    enabled = reg.list_enabled()
    ids = [p.metadata.provider_id for p in enabled]
    assert "mock" in ids
    assert "gemini-disabled" not in ids
    assert "deepseek-disabled" not in ids


def test_registry_list_disabled():
    reset_default_registry()
    reg = get_default_registry()
    disabled = reg.list_disabled()
    ids = [p.metadata.provider_id for p in disabled]
    assert "mock" not in ids
    assert "gemini-disabled" in ids


# ── Router tests ──


def test_router_mock_works():
    reset_default_registry()
    router = AIProviderRouter()
    decision = router.select("mock")
    assert not decision.is_blocked
    assert decision.metadata is not None
    assert decision.metadata.can_use_now


def test_router_unknown_blocked():
    reset_default_registry()
    router = AIProviderRouter()
    decision = router.select("nonexistent")
    assert decision.is_blocked
    assert "Unknown" in decision.blocked_reason


def test_router_gemini_disabled_by_default():
    reset_default_registry()
    router = AIProviderRouter()
    decision = router.select("gemini-disabled")
    assert decision.is_blocked
    assert "disabled" in decision.blocked_reason.lower()


def test_router_deepseek_disabled_by_default():
    reset_default_registry()
    router = AIProviderRouter()
    decision = router.select("deepseek-disabled")
    assert decision.is_blocked
    assert "disabled" in decision.blocked_reason.lower()


def test_router_local_disabled_by_default():
    reset_default_registry()
    router = AIProviderRouter()
    decision = router.select("local-disabled")
    assert decision.is_blocked


def test_router_gemini_requires_approval():
    """Even with approved=True, gemini is still blocked because
    it's hard-disabled in the adapter metadata."""
    reset_default_registry()
    router = AIProviderRouter()
    decision = router.select("gemini-disabled", approved=True)
    assert decision.is_blocked


def test_router_unknown_provider_no_api_call():
    """Router must never call external API for unknown providers."""
    reset_default_registry()
    router = AIProviderRouter()
    decision = router.select("foobar")
    assert decision.is_blocked
    # generate should also be safe
    resp = router.generate("foobar", AIProviderRequest(prompt="test"))
    assert resp.is_blocked
    assert resp.safety["real_api_called"] is False
    assert resp.safety["env_read"] is False
    assert resp.safety["token_used"] is False


def test_router_generate_mock():
    reset_default_registry()
    router = AIProviderRouter()
    resp = router.generate("mock", AIProviderRequest(prompt="hello"))
    assert not resp.is_blocked
    assert resp.text.startswith("MOCK:")
    assert resp.safety["real_api_called"] is False
    assert resp.safety["env_read"] is False
    assert resp.safety["token_used"] is False


def test_router_generate_gemini_blocked_no_api():
    reset_default_registry()
    router = AIProviderRouter()
    resp = router.generate("gemini-disabled", AIProviderRequest(prompt="hello"))
    assert resp.is_blocked
    assert resp.safety["real_api_called"] is False
    assert resp.safety["env_read"] is False
    assert resp.safety["token_used"] is False


def test_router_generate_deepseek_blocked_no_api():
    reset_default_registry()
    router = AIProviderRouter()
    resp = router.generate("deepseek-disabled", AIProviderRequest(prompt="hello"))
    assert resp.is_blocked
    assert resp.safety["real_api_called"] is False


# ── Secret policy tests ──


def test_mock_has_no_secret_required():
    reset_default_registry()
    reg = get_default_registry()
    adapter = reg.get("mock")
    assert adapter is not None
    assert adapter.metadata.secret_policy == SecretPolicy.NO_SECRET_REQUIRED
    assert not adapter.metadata.requires_secret


def test_gemini_has_secret_required():
    reset_default_registry()
    reg = get_default_registry()
    adapter = reg.get("gemini-disabled")
    assert adapter is not None
    assert adapter.metadata.requires_secret
    assert adapter.metadata.approval_required == "APPROVE_SECRET_SETUP"


def test_deepseek_has_secret_required():
    reset_default_registry()
    reg = get_default_registry()
    adapter = reg.get("deepseek-disabled")
    assert adapter is not None
    assert adapter.metadata.requires_secret
    assert adapter.metadata.approval_required == "APPROVE_SECRET_SETUP"


# ── Capabilities tests ──


def test_mock_capabilities():
    reset_default_registry()
    reg = get_default_registry()
    adapter = reg.get("mock")
    caps = adapter.metadata.capabilities
    names = [c.name for c in caps]
    assert "TEXT_GENERATION" in names
    assert "REVIEW" in names
    assert "JSON_MODE" in names


def test_gemini_capabilities():
    reset_default_registry()
    reg = get_default_registry()
    adapter = reg.get("gemini-disabled")
    caps = adapter.metadata.capabilities
    names = [c.name for c in caps]
    assert "TEXT_GENERATION" in names
    assert "VISION" in names
    assert "EMBEDDINGS" in names
    assert "NETWORK_REQUIRED" in names


# ── Safety tests ──


def test_no_env_read_in_registry():
    """Registry never reads .env files."""
    reset_default_registry()
    reg = get_default_registry()
    for adapter in reg.list_all():
        resp = adapter.generate(AIProviderRequest(prompt="test"))
        assert resp.safety.get("env_read") is False


def test_no_token_used_in_registry():
    """Registry never uses tokens."""
    reset_default_registry()
    reg = get_default_registry()
    for adapter in reg.list_all():
        resp = adapter.generate(AIProviderRequest(prompt="test"))
        assert resp.safety.get("token_used") is False


def test_no_real_api_called():
    """No provider adapter calls real API."""
    reset_default_registry()
    reg = get_default_registry()
    for adapter in reg.list_all():
        resp = adapter.generate(AIProviderRequest(prompt="test"))
        assert resp.safety.get("real_api_called") is False


def test_registry_no_secrets_in_metadata():
    """Registry metadata must never contain real keys."""
    reset_default_registry()
    reg = get_default_registry()
    for adapter in reg.list_all():
        m = adapter.metadata
        text = str(m)
        assert "sk-" not in text  # OpenAI-style
        assert "AIza" not in text  # Gemini-style
        assert "key" not in text.lower() or "requires_secret" in text or "secret_policy" in text


# ── AIProviderResponse tests ──


def test_blocked_response_factory():
    resp = AIProviderResponse.blocked("test reason", provider_id="test")
    assert resp.is_blocked
    assert resp.blocked_reason == "test reason"
    assert resp.provider_id == "test"
    assert resp.is_mock


def test_error_response_factory():
    resp = AIProviderResponse.error("test error", provider_id="test")
    assert resp.is_blocked
    assert "ERROR" in resp.text
    assert resp.provider_id == "test"
