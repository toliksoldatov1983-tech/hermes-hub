"""Tests for BATCH_100: Telegram Conversation Memory + Order Draft State."""

from __future__ import annotations
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))


class TestConversationMemory:
    def test_create_session(self):
        from hermes_core.telegram_memory import ConversationSession
        s = ConversationSession()
        assert s.session_id == "dry-run-session-001"
        assert s.safe_local is True

    def test_session_audit(self):
        from hermes_core.telegram_memory import ConversationSession
        s = ConversationSession()
        assert s.audit_metadata["real_user"] is False
        assert s.audit_metadata["in_memory_only"] is True

    def test_add_turn(self):
        from hermes_core.telegram_memory import ConversationSession
        s = ConversationSession()
        s.add_turn("user", "привет", "general_chat")
        assert s.turn_count == 1

    def test_set_mode(self):
        from hermes_core.telegram_memory import ConversationSession, ConversationMode
        s = ConversationSession()
        s.set_mode(ConversationMode.MALYARKA_ORDER)
        assert s.mode == ConversationMode.MALYARKA_ORDER

    def test_pending_question(self):
        from hermes_core.telegram_memory import ConversationSession, ReplyExpectation
        s = ConversationSession()
        s.set_pending_question("Подтвердить?", ReplyExpectation.CONFIRMATION)
        assert s.is_awaiting_reply is True
        s.clear_pending_question()
        assert s.is_awaiting_reply is False

    def test_attach_draft(self):
        from hermes_core.telegram_memory import ConversationSession
        s = ConversationSession()
        s.attach_draft("draft-001")
        assert s.has_active_draft is True


class TestMemoryStore:
    def test_create_session(self):
        from hermes_core.telegram_memory import get_memory_store
        store = get_memory_store()
        s = store.create_session("test-1")
        assert s.session_id == "test-1"

    def test_in_memory_only(self):
        from hermes_core.telegram_memory import get_memory_store
        store = get_memory_store()
        assert store.is_persistent is False
        assert store.is_in_memory is True

    def test_reset_session(self):
        from hermes_core.telegram_memory import get_memory_store
        store = get_memory_store()
        s1 = store.create_session("test-reset")
        s1.add_turn("user", "hello")
        s2 = store.reset_session("test-reset")
        assert s2.turn_count == 0


class TestOrderDraft:
    def test_create_draft(self):
        from hermes_core.telegram_memory import OrderDraft
        d = OrderDraft(source_text="720х300 краска белая")
        assert d.status.value == "new"

    def test_add_confirmed(self):
        from hermes_core.telegram_memory import OrderDraft, OrderDraftLine
        d = OrderDraft()
        d.add_confirmed(OrderDraftLine(raw_text="paint|2|bucket", item="paint", quantity="2", unit="bucket"))
        assert len(d.confirmed_rows) == 1

    def test_disputes_block_export(self):
        from hermes_core.telegram_memory import OrderDraft, OrderDraftLine
        d = OrderDraft()
        d.add_disputed(OrderDraftLine(raw_text="broken", is_disputed=True, dispute_reason="bad"))
        assert d.has_disputes is True
        d.confirm()
        assert d.status.value == "has_disputes"

    def test_confirm_no_disputes(self):
        from hermes_core.telegram_memory import OrderDraft, OrderDraftLine
        d = OrderDraft()
        d.add_confirmed(OrderDraftLine(raw_text="ok|1|pc", item="ok", quantity="1", unit="pc"))
        d.confirm()
        assert d.status.value == "confirmed"

    def test_cancel(self):
        from hermes_core.telegram_memory import OrderDraft
        d = OrderDraft()
        d.cancel()
        assert d.status.value == "cancelled"

    def test_audit_no_export(self):
        from hermes_core.telegram_memory import OrderDraft
        d = OrderDraft()
        assert d.audit_metadata["export_created"] is False


class TestDraftLifecycle:
    def test_create_and_parse(self):
        from hermes_core.telegram_memory import DraftLifecycle
        lc = DraftLifecycle()
        d = lc.parse_from_text("d1", "paint|2|bucket\nroller|3|piece")
        assert len(d.confirmed_rows) == 2
        assert d.has_disputes is False

    def test_detect_disputes(self):
        from hermes_core.telegram_memory import DraftLifecycle
        lc = DraftLifecycle()
        d = lc.parse_from_text("d2", "broken row\nroller|3|piece")
        assert d.has_disputes is True

    def test_confirm_lifecycle(self):
        from hermes_core.telegram_memory import DraftLifecycle
        lc = DraftLifecycle()
        lc.parse_from_text("d3", "paint|2|bucket")
        lc.confirm("d3")
        d = lc.get("d3")
        assert d.is_confirmed is True


class TestContextAwareRouter:
    def test_route_general_chat(self):
        from hermes_core.telegram_memory import ContextAwareRouter
        router = ContextAwareRouter()
        r = router.route("привет")
        assert "Mock assistant" in r.text

    def test_route_order(self):
        from hermes_core.telegram_memory import ContextAwareRouter
        router = ContextAwareRouter()
        r = router.route("paint|2|bucket\nroller|3|piece")
        assert "Черновик" in r.text or "черновик" in r.text.lower()
        assert r.draft_state is not None

    def test_route_blocked(self):
        from hermes_core.telegram_memory import ContextAwareRouter
        router = ContextAwareRouter()
        r = router.route(".env")
        assert r.blocked_reason != ""

    def test_route_confirmation_without_draft(self):
        from hermes_core.telegram_memory import ContextAwareRouter
        router = ContextAwareRouter()
        r = router.route("да, подтверждаю")
        assert "нет активного черновика" in r.text.lower() or "Mock assistant" in r.text


class TestCLIMemoryCommands:
    def test_memory_status(self):
        from hermes_core.cli import telegram_memory_status_command
        import argparse
        assert telegram_memory_status_command(argparse.Namespace()) == 0

    def test_session_dry_run(self):
        from hermes_core.cli import telegram_session_dry_run_command
        import argparse
        assert telegram_session_dry_run_command(argparse.Namespace()) == 0

    def test_order_draft_create(self):
        from hermes_core.cli import telegram_order_draft_create_dry_run_command
        import argparse
        assert telegram_order_draft_create_dry_run_command(argparse.Namespace()) == 0

    def test_conversation_flow(self):
        from hermes_core.cli import telegram_conversation_flow_dry_run_command
        import argparse
        assert telegram_conversation_flow_dry_run_command(argparse.Namespace()) == 0

    def test_memory_safety(self):
        from hermes_core.cli import telegram_memory_safety_check_command
        import argparse
        assert telegram_memory_safety_check_command(argparse.Namespace()) == 0


class TestRegression:
    def test_malyarka(self):
        from hermes_modules.malyarka.fixtures import run_all_fixtures
        assert len(run_all_fixtures()) == 12

    def test_intent_router(self):
        from hermes_core.telegram_intent import TelegramIntentRouter
        assert TelegramIntentRouter().detect("привет").intent.value == "general_chat"

    def test_bridge(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        assert BridgeRouter().handle(BridgeRequest(action=BridgeActionType.STATUS)).is_ok
