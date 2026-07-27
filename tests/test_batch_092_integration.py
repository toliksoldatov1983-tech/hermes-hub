"""Tests for BATCH_092: AI Provider Integration, Review Unification, Daily Assistant.

Covers:
  - Review provider through universal router
  - Malyarka uses AI Provider Router
  - No direct Gemini/DeepSeek usage in Malyarka
  - Daily Assistant commands
  - Daily Brief / What Next / Local Health
  - No .env read, no secret logging, no network call
  - Disabled provider blocking
  - Regression for BATCH_088–091
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Ensure project root is importable
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))


# ── 1. Review provider through universal router ──


class TestReviewProviderUnification:
    """Review provider now delegates to AIProviderRouter."""

    def test_mock_review_adapter_registered(self):
        from hermes_core.ai_provider import get_default_registry, reset_default_registry
        reset_default_registry()
        registry = get_default_registry()
        adapter = registry.get("mock-review")
        assert adapter is not None, "mock-review adapter should be registered"
        assert adapter.metadata.provider_id == "mock-review"
        assert adapter.metadata.can_use_now is True

    def test_mock_review_adapter_generates(self):
        from hermes_core.ai_provider import get_default_registry, reset_default_registry
        from hermes_core.ai_provider.contract import AIProviderRequest
        reset_default_registry()
        registry = get_default_registry()
        adapter = registry.get("mock-review")
        response = adapter.generate(AIProviderRequest(prompt="test"))
        assert response.is_mock is True
        assert "MOCK" in response.text

    def test_mock_review_adapter_generate_review(self):
        from hermes_core.ai_provider import get_default_registry, reset_default_registry
        reset_default_registry()
        registry = get_default_registry()
        adapter = registry.get("mock-review")
        response = adapter.generate_review("print('hello')")
        assert response.is_mock is True
        assert response.text, "Review should return non-empty text"

    def test_deepseek_review_disabled_adapter_blocked(self):
        from hermes_core.ai_provider import get_default_registry, reset_default_registry
        reset_default_registry()
        registry = get_default_registry()
        adapter = registry.get("deepseek-review-disabled")
        assert adapter is not None, "deepseek-review-disabled should be registered"
        assert adapter.metadata.is_blocked is True
        assert adapter.metadata.can_use_now is False

    def test_review_factory_still_works(self):
        """Old ReviewProviderFactory API works after bridging to router."""
        from hermes_core.review.review_provider_factory import (
            ReviewProviderConfig,
            ReviewProviderFactory,
        )
        factory = ReviewProviderFactory()
        selection = factory.select(ReviewProviderConfig(mode="mock-review"))
        assert selection.is_blocked is False
        result = selection.review("test code")
        assert result.provider == "mock-review"

    def test_review_factory_deepseek_disabled(self):
        from hermes_core.review.review_provider_factory import (
            ReviewProviderConfig,
            ReviewProviderFactory,
        )
        factory = ReviewProviderFactory()
        selection = factory.select(ReviewProviderConfig(mode="deepseek-disabled"))
        assert selection.is_blocked is True
        assert selection.blocked_reason is not None

    def test_router_selects_mock_review(self):
        from hermes_core.ai_provider import AIProviderRouter, reset_default_registry
        from hermes_core.ai_provider.registry import get_default_registry
        reset_default_registry()
        get_default_registry()  # ensure populated
        router = AIProviderRouter()
        decision = router.select("mock-review")
        assert decision.is_blocked is False
        assert decision.provider_id == "mock-review"


# ── 2. Malyarka uses AI Provider Router ──


class TestMalyarkaAIRouter:
    """Malyarka AI calls go through AIProviderRouter."""

    def test_review_disputed_row_returns_valid_result(self):
        from hermes_modules.malyarka.ai_review import review_disputed_row
        result = review_disputed_row("broken row without pipe")
        assert result.raw_text == "broken row without pipe"
        assert result.explanation, "Should have explanation"
        assert result.recommended_action in ("delete", "clarify")
        assert result.provider_id == "mock"

    def test_review_disputed_row_is_mock(self):
        from hermes_modules.malyarka.ai_review import review_disputed_row
        result = review_disputed_row("test")
        assert result.is_mock is True

    def test_no_direct_gemini_in_malyarka_ai(self):
        """Verify malyarka/ai_review.py has no direct Gemini imports."""
        import ast
        ai_review_path = PROJECT_ROOT / "src" / "hermes_modules" / "malyarka" / "ai_review.py"
        source = ai_review_path.read_text()
        tree = ast.parse(source)
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        gemini_imports = [i for i in imports if "gemini" in i.lower()]
        assert not gemini_imports, f"ai_review.py should not import Gemini: {gemini_imports}"

    def test_no_direct_deepseek_in_malyarka_ai(self):
        """Verify malyarka/ai_review.py has no direct DeepSeek imports."""
        import ast
        ai_review_path = PROJECT_ROOT / "src" / "hermes_modules" / "malyarka" / "ai_review.py"
        source = ai_review_path.read_text()
        tree = ast.parse(source)
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        deepseek_imports = [i for i in imports if "deepseek" in i.lower()]
        assert not deepseek_imports, f"ai_review.py should not import DeepSeek: {deepseek_imports}"

    def test_safety_metadata_no_network_called(self):
        from hermes_modules.malyarka.ai_review import review_disputed_row
        result = review_disputed_row("test")
        assert result.safety["real_api_called"] is False
        assert result.safety["network_called"] is False
        assert result.safety["direct_gemini_call"] is False
        assert result.safety["direct_deepseek_call"] is False

    def test_review_disputed_rows_batch(self):
        from hermes_modules.malyarka.ai_review import review_disputed_rows
        results = review_disputed_rows(["row1", "row2", "row3"])
        assert len(results) == 3
        for r in results:
            assert r.is_mock is True

    def test_ai_explain_dispute_category(self):
        from hermes_modules.malyarka.ai_review import ai_explain_dispute_category
        result = ai_explain_dispute_category("missing_separator", "broken|row")
        assert result.explanation
        assert result.provider_id == "mock"


# ── 3. Daily Assistant ──


class TestDailyAssistant:
    """Daily assistant commands work and produce correct output."""

    def test_build_daily_assistant(self):
        from hermes_core.daily_assistant import build_daily_assistant
        report = build_daily_assistant()
        assert report.health_status == "OK"
        assert report.ai_providers_total > 0
        assert report.ai_providers_safe > 0
        assert report.ai_providers_blocked > 0
        assert len(report.gates) == 6
        assert len(report.recommended_commands) > 0
        assert len(report.blocked_without_approval) > 0

    def test_build_daily_brief(self):
        from hermes_core.daily_assistant import build_daily_brief
        brief = build_daily_brief()
        assert brief.project == "Hermes-Clean"
        assert brief.health
        assert brief.malyarka
        assert brief.ai_provider
        assert len(brief.warnings) > 0

    def test_build_what_next(self):
        from hermes_core.daily_assistant import build_what_next
        report = build_what_next()
        assert report.next_task_id
        assert len(report.safe_commands) > 0
        assert len(report.blocked_actions) > 0

    def test_daily_assistant_has_malyarka_status(self):
        from hermes_core.daily_assistant import build_daily_assistant
        report = build_daily_assistant()
        assert report.malyarka_fixtures == 12
        assert "dry-run" in report.malyarka_status

    def test_daily_assistant_has_ai_provider_details(self):
        from hermes_core.daily_assistant import build_daily_assistant
        report = build_daily_assistant()
        assert len(report.provider_details) >= 2  # mock + mock-review at minimum


# ── 4. No .env read, no secret logging, no network ──


class TestSafetyConstraints:
    """Safety constraints are enforced."""

    def test_ai_provider_response_safety_defaults(self):
        from hermes_core.ai_provider import AIProviderResponse
        resp = AIProviderResponse(text="test")
        assert resp.safety["real_api_called"] is False
        assert resp.safety["env_read"] is False
        assert resp.safety["token_used"] is False
        assert resp.safety["network_called"] is False

    def test_blocked_response_has_safety(self):
        from hermes_core.ai_provider import AIProviderResponse
        resp = AIProviderResponse.blocked("test reason")
        assert resp.is_blocked is True
        assert resp.safety["real_api_called"] is False

    def test_malyarka_ai_review_no_network(self):
        from hermes_modules.malyarka.ai_review import review_disputed_row
        result = review_disputed_row("test")
        assert result.safety["network_called"] is False

    def test_mock_adapter_no_secret(self):
        from hermes_core.ai_provider import get_default_registry, reset_default_registry
        reset_default_registry()
        registry = get_default_registry()
        for adapter in registry.list_all():
            meta = adapter.metadata
            if meta.provider_id in ("mock", "mock-review"):
                assert meta.requires_secret is False, f"{meta.provider_id} should not require secret"


# ── 5. Disabled provider blocking ──


class TestDisabledProviderBlocking:
    """Disabled and blocked providers are enforced."""

    def test_deepseek_provider_blocked(self):
        from hermes_core.ai_provider import AIProviderRouter, reset_default_registry
        from hermes_core.ai_provider.registry import get_default_registry
        reset_default_registry()
        get_default_registry()
        router = AIProviderRouter()
        decision = router.select("deepseek-disabled")
        assert decision.is_blocked is True

    def test_deepseek_review_blocked(self):
        from hermes_core.ai_provider import AIProviderRouter, reset_default_registry
        from hermes_core.ai_provider.registry import get_default_registry
        reset_default_registry()
        get_default_registry()
        router = AIProviderRouter()
        decision = router.select("deepseek-review-disabled")
        assert decision.is_blocked is True

    def test_gemini_blocked_without_approval(self):
        from hermes_core.ai_provider import AIProviderRouter, reset_default_registry
        from hermes_core.ai_provider.registry import get_default_registry
        reset_default_registry()
        get_default_registry()
        router = AIProviderRouter()
        decision = router.select("gemini-disabled", approved=False)
        assert decision.is_blocked is True

    def test_mock_provider_always_safe(self):
        from hermes_core.ai_provider import AIProviderRouter, reset_default_registry
        from hermes_core.ai_provider.registry import get_default_registry
        reset_default_registry()
        get_default_registry()
        router = AIProviderRouter()
        decision = router.select("mock")
        assert decision.is_blocked is False

    def test_disabled_providers_cannot_generate(self):
        from hermes_core.ai_provider import AIProviderRouter, reset_default_registry
        from hermes_core.ai_provider.registry import get_default_registry
        reset_default_registry()
        get_default_registry()
        router = AIProviderRouter()
        response = router.generate("deepseek-disabled")
        assert response.is_blocked is True


# ── 6. Registry integrity ──


class TestRegistryIntegrity:
    """Registry has all expected providers after BATCH_092."""

    def test_expected_providers_registered(self):
        from hermes_core.ai_provider import get_default_registry, reset_default_registry
        reset_default_registry()
        registry = get_default_registry()
        expected = {
            "mock", "gemini-disabled", "deepseek-disabled",
            "local-disabled", "ollama-disabled", "custom-disabled",
            "mock-review", "deepseek-review-disabled",
        }
        registered = set(registry.list_ids())
        for pid in expected:
            assert pid in registered, f"{pid} should be registered"

    def test_registry_count(self):
        from hermes_core.ai_provider import get_default_registry, reset_default_registry
        reset_default_registry()
        registry = get_default_registry()
        assert registry.count() >= 8, f"Expected at least 8 providers, got {registry.count()}"

    def test_safe_providers_count(self):
        from hermes_core.ai_provider import get_default_registry, reset_default_registry
        reset_default_registry()
        registry = get_default_registry()
        enabled = registry.list_enabled()
        safe_ids = {a.metadata.provider_id for a in enabled}
        assert "mock" in safe_ids, "mock must be enabled"
        assert "mock-review" in safe_ids, "mock-review must be enabled"
        # Real providers should be disabled
        assert "gemini-disabled" not in safe_ids


# ── 7. CLI integration ──


class TestCLIIntegration:
    """New CLI commands are registered and functional."""

    def test_daily_assistant_cli_registered(self):
        from hermes_core.cli import build_parser
        parser = build_parser()
        # Parse should not crash with the new subcommands
        args = parser.parse_args(["daily-assistant"])
        assert args.command == "daily-assistant"

    def test_daily_assistant_cli_runs(self):
        from hermes_core.cli import daily_assistant_command
        import argparse
        ns = argparse.Namespace()
        rc = daily_assistant_command(ns)
        assert rc == 0

    def test_daily_brief_cli_runs(self):
        from hermes_core.cli import daily_brief_command
        import argparse
        ns = argparse.Namespace()
        rc = daily_brief_command(ns)
        assert rc == 0

    def test_what_next_cli_runs(self):
        from hermes_core.cli import what_next_command
        import argparse
        ns = argparse.Namespace()
        rc = what_next_command(ns)
        assert rc == 0

    def test_local_health_cli_runs(self):
        from hermes_core.cli import local_health_command
        import argparse
        ns = argparse.Namespace()
        rc = local_health_command(ns)
        assert rc == 0

    def test_project_status_cli_runs(self):
        from hermes_core.cli import project_status_command
        import argparse
        ns = argparse.Namespace()
        rc = project_status_command(ns)
        assert rc == 0

    def test_malyarka_mode_status_cli_runs(self):
        from hermes_core.cli import malyarka_mode_status_command
        import argparse
        ns = argparse.Namespace()
        rc = malyarka_mode_status_command(ns)
        assert rc == 0

    def test_new_providers_in_list(self):
        from hermes_core.ai_provider import AIProviderRouter, reset_default_registry
        from hermes_core.ai_provider.registry import get_default_registry
        reset_default_registry()
        get_default_registry()
        router = AIProviderRouter()
        providers = router.list_providers()
        provider_ids = {d.provider_id for d in providers}
        assert "mock-review" in provider_ids
        assert "deepseek-review-disabled" in provider_ids


# ── 8. Regression — BATCH_088–091 smoke ──


class TestRegression:
    """Ensure BATCH_092 doesn't break BATCH_088–091 functionality."""

    def test_ai_provider_router_still_works(self):
        from hermes_core.ai_provider import AIProviderRouter, reset_default_registry
        from hermes_core.ai_provider.registry import get_default_registry
        reset_default_registry()
        get_default_registry()
        router = AIProviderRouter()
        decision = router.select("mock")
        assert decision.is_blocked is False
        providers = router.list_providers()
        assert len(providers) > 0

    def test_ai_provider_registry_still_works(self):
        from hermes_core.ai_provider import get_default_registry, reset_default_registry
        reset_default_registry()
        registry = get_default_registry()
        assert registry.count() >= 6  # original six + review adapters

    def test_provider_factory_compatibility(self):
        """Old provider_factory still works."""
        from hermes_core.ai.provider_factory import ProviderConfig, ProviderFactory
        selection = ProviderFactory().select(ProviderConfig(mode="mock"))
        assert selection.is_blocked is False

    def test_malyarka_fixtures_still_load(self):
        from hermes_modules.malyarka.fixtures import run_all_fixtures
        results = run_all_fixtures()
        assert len(results) == 12, f"Expected 12 fixtures, got {len(results)}"

    def test_malyarka_parser_still_works(self):
        from hermes_modules.malyarka.parser_contract import ParserContract
        order = ParserContract().parse("paint | 2 | bucket")
        assert order is not None
