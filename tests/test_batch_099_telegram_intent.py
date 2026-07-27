"""Tests for BATCH_099: Telegram Intent Router + Malyarka Chat Dry-Run."""

from __future__ import annotations
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))


class TestIntentContract:
    def test_intent_type_values(self):
        from hermes_core.telegram_intent import IntentType
        assert IntentType.GENERAL_CHAT.value == "general_chat"
        assert IntentType.MALYARKA_ORDER.value == "malyarka_order"

    def test_intent_result_to_dict(self):
        from hermes_core.telegram_intent import IntentResult
        r = IntentResult.general_chat()
        d = r.to_dict()
        assert d["intent"] == "general_chat"
        assert d["safe_local"] is True

    def test_intent_result_audit(self):
        from hermes_core.telegram_intent import IntentResult
        r = IntentResult.general_chat()
        assert r.audit_metadata["real_telegram_api"] is False
        assert r.audit_metadata["token_used"] is False

    def test_blocked_intent(self):
        from hermes_core.telegram_intent import IntentResult, IntentType
        r = IntentResult.blocked(IntentType.SAFETY_SENSITIVE, "blocked")
        assert r.is_blocked is True
        assert r.intent == IntentType.SAFETY_SENSITIVE


class TestOrderDetection:
    def test_dimensions_detected(self):
        from hermes_core.telegram_intent import detect_order
        r = detect_order("720х300 краска белая")
        assert r.dimensions_found is True
        assert r.is_order is True

    def test_dimensions_with_x(self):
        from hermes_core.telegram_intent import detect_order
        r = detect_order("1200 x 800 цвет серый 5 шт")
        assert r.dimensions_found is True
        assert r.quantity_found is True

    def test_no_order_in_chat(self):
        from hermes_core.telegram_intent import detect_order
        r = detect_order("привет, как дела?")
        assert r.is_order is False
        assert r.confidence < 0.3

    def test_material_detected(self):
        from hermes_core.telegram_intent import detect_order
        r = detect_order("фасады мдф 5 штук")
        assert r.material_found is True

    def test_correction_detected(self):
        from hermes_core.telegram_intent import detect_order
        r = detect_order("исправь размер на 800х600")
        assert r.is_correction is True

    def test_confirmation_detected(self):
        from hermes_core.telegram_intent import detect_order
        r = detect_order("да, подтверждаю")
        assert r.is_confirmation is True

    def test_order_name_detection(self):
        from hermes_core.telegram_intent import detect_order
        r = detect_order("заказ №42 клиент Иванов")
        assert r.order_name_found is True


class TestIntentRouter:
    def test_general_chat(self):
        from hermes_core.telegram_intent import TelegramIntentRouter
        r = TelegramIntentRouter().detect("привет, как дела?")
        assert r.intent.value == "general_chat"

    def test_malyarka_order(self):
        from hermes_core.telegram_intent import TelegramIntentRouter
        r = TelegramIntentRouter().detect("720х300 краска белая 3 шт")
        assert r.intent.value == "malyarka_order"
        assert r.confidence > 0.7

    def test_project_status(self):
        from hermes_core.telegram_intent import TelegramIntentRouter
        r = TelegramIntentRouter().detect("/status")
        assert r.intent.value == "project_status"

    def test_help(self):
        from hermes_core.telegram_intent import TelegramIntentRouter
        r = TelegramIntentRouter().detect("помощь")
        assert r.intent.value == "help"

    def test_safety_blocked(self):
        from hermes_core.telegram_intent import TelegramIntentRouter
        r = TelegramIntentRouter().detect("telegram token")
        assert r.intent.value == "safety_sensitive"
        assert r.is_blocked is True

    def test_env_blocked(self):
        from hermes_core.telegram_intent import TelegramIntentRouter
        r = TelegramIntentRouter().detect(".env")
        assert r.is_blocked is True

    def test_correction_with_context(self):
        from hermes_core.telegram_intent import TelegramIntentRouter
        ctx = {"has_draft_order": True, "has_disputed_rows": True}
        r = TelegramIntentRouter().detect("исправь размер", context=ctx)
        assert r.intent.value == "malyarka_order_correction"

    def test_confirmation_with_context(self):
        from hermes_core.telegram_intent import TelegramIntentRouter
        ctx = {"awaiting_confirmation": True}
        r = TelegramIntentRouter().detect("да, подтверждаю", context=ctx)
        assert r.intent.value == "malyarka_order_confirmation"


class TestCLITelegramIntent:
    def test_intent_status(self):
        from hermes_core.cli import telegram_intent_status_command
        import argparse
        assert telegram_intent_status_command(argparse.Namespace()) == 0

    def test_intent_dry_run(self):
        from hermes_core.cli import telegram_intent_dry_run_command
        import argparse
        assert telegram_intent_dry_run_command(argparse.Namespace()) == 0

    def test_order_detect(self):
        from hermes_core.cli import telegram_intent_order_detect_command
        import argparse
        assert telegram_intent_order_detect_command(argparse.Namespace()) == 0

    def test_chat_detect(self):
        from hermes_core.cli import telegram_intent_chat_detect_command
        import argparse
        assert telegram_intent_chat_detect_command(argparse.Namespace()) == 0

    def test_safety_check(self):
        from hermes_core.cli import telegram_safety_check_command
        import argparse
        assert telegram_safety_check_command(argparse.Namespace()) == 0


class TestRegression:
    def test_malyarka(self):
        from hermes_modules.malyarka.fixtures import run_all_fixtures
        assert len(run_all_fixtures()) == 12

    def test_ai_provider(self):
        from hermes_core.ai_provider import AIProviderRouter, reset_default_registry
        from hermes_core.ai_provider.registry import get_default_registry
        reset_default_registry()
        get_default_registry()
        assert not AIProviderRouter().select("mock").is_blocked

    def test_bridge(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        assert BridgeRouter().handle(BridgeRequest(action=BridgeActionType.STATUS)).is_ok
