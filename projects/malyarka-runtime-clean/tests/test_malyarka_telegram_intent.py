"""Tests for malyarka_telegram.intent — local intent recognition.

Covers:
- dimension patterns → order
- order keywords → order
- engineer keywords → engineer
- ideas keywords → ideas
- admin keywords → admin (with clarification)
- ambiguous phrases → unknown + clarify_question
- dangerous content → blocked
- stop/greeting phrases → unknown + clarify_question
- empty text → unknown + clarify_question
- no external API calls, no .env reads, no orders.db access
"""

from __future__ import annotations

import importlib
import re
import sys

import pytest

from malyarka_telegram.intent import (
    INTENT_ADMIN,
    INTENT_ENGINEER,
    INTENT_IDEAS,
    INTENT_ORDER,
    INTENT_UNKNOWN,
    DEFAULT_CONFIDENCE_THRESHOLD,
    IntentResult,
    classify_intent,
)


# ======================================================================
# Helper
# ======================================================================

def _check(
    text: str,
    *,
    intent: str | None = None,
    not_intent: str | None = None,
    min_confidence: float = 0.0,
    max_confidence: float = 1.0,
    blocked: bool = False,
    has_clarify: bool = False,
    reason_contains: str | None = None,
) -> None:
    """Run classify_intent and assert expectations."""
    result = classify_intent(text)
    assert isinstance(result, IntentResult), f"Expected IntentResult, got {type(result)}"
    if intent is not None:
        assert result.intent == intent, (
            f"Text={text!r}: expected intent={intent!r}, got {result.intent!r}"
        )
    if not_intent is not None:
        assert result.intent != not_intent, (
            f"Text={text!r}: expected not intent={not_intent!r}, got {result.intent!r}"
        )
    if min_confidence > 0:
        assert result.confidence >= min_confidence, (
            f"Text={text!r}: confidence {result.confidence:.2f} < {min_confidence:.2f}"
        )
    if max_confidence < 1.0:
        assert result.confidence <= max_confidence, (
            f"Text={text!r}: confidence {result.confidence:.2f} > {max_confidence:.2f}"
        )
    assert result.blocked == blocked, (
        f"Text={text!r}: expected blocked={blocked}, got blocked={result.blocked}"
    )
    if has_clarify:
        assert result.clarify_question is not None, (
            f"Text={text!r}: expected clarify_question but got None"
        )
        assert len(result.clarify_question) > 10, (
            f"Text={text!r}: clarify_question too short"
        )
    else:
        assert result.clarify_question is None, (
            f"Text={text!r}: expected no clarify_question but got {result.clarify_question!r}"
        )
    if reason_contains:
        assert reason_contains in result.reason, (
            f"Text={text!r}: expected reason to contain {reason_contains!r}, "
            f"got {result.reason!r}"
        )


# ======================================================================
# Dimension patterns → order
# ======================================================================

class TestDimensionPatterns:
    def test_asterisk_dimensions(self):
        _check("1000*400", intent=INTENT_ORDER, min_confidence=0.85, reason_contains="размеры")

    def test_asterisk_with_quantity(self):
        _check("1000*400*2", intent=INTENT_ORDER, min_confidence=0.85, reason_contains="размеры")

    def test_x_latin_dimensions(self):
        _check("1000 x 400", intent=INTENT_ORDER, min_confidence=0.85, reason_contains="размеры")

    def test_x_latin_tight(self):
        _check("500x300", intent=INTENT_ORDER, min_confidence=0.85, reason_contains="размеры")

    def test_x_cyrillic_dimensions(self):
        _check("1000х400", intent=INTENT_ORDER, min_confidence=0.85, reason_contains="размеры")

    def test_cyrillic_uppercase(self):
        _check("1000Х400", intent=INTENT_ORDER, min_confidence=0.85, reason_contains="размеры")

    def test_multiplication_sign(self):
        _check("1000×400", intent=INTENT_ORDER, min_confidence=0.85, reason_contains="размеры")

    def test_x_with_quantity(self):
        _check("1000 x 400 x 2", intent=INTENT_ORDER, min_confidence=0.85, reason_contains="размеры")

    def test_space_separated_two_numbers(self):
        _check("1000 400", intent=INTENT_ORDER, min_confidence=0.85, reason_contains="размеры")

    def test_space_separated_three_numbers(self):
        _check("1000 400 2", intent=INTENT_ORDER, min_confidence=0.85, reason_contains="размеры")

    def test_multiline_dimensions(self):
        text = "1000*400\n500 x 300\n200 100 2"
        _check(text, intent=INTENT_ORDER, min_confidence=0.85, reason_contains="размеры")

    def test_dimensions_with_order_keyword(self):
        _check("Прими заказ 1000*400", intent=INTENT_ORDER, min_confidence=0.85)

    def test_large_numbers(self):
        _check("2000 800 3", intent=INTENT_ORDER, min_confidence=0.85, reason_contains="размеры")


# ======================================================================
# Order keywords → order
# ======================================================================

class TestOrderKeywords:
    def test_order_keyword(self):
        _check("заказ", intent=INTENT_ORDER, min_confidence=0.5, max_confidence=0.85)

    def test_new_order(self):
        _check("новый заказ", intent=INTENT_ORDER, min_confidence=0.80)

    def test_accept_order(self):
        _check("прими заказ", intent=INTENT_ORDER, min_confidence=0.5)

    def test_facade_keyword(self):
        _check("фасад", intent=INTENT_ORDER, min_confidence=0.45)

    def test_detail_keyword(self):
        _check("деталь", intent=INTENT_ORDER, min_confidence=0.40)

    def test_size_keyword(self):
        _check("размеры", intent=INTENT_ORDER, min_confidence=0.40)

    def test_excel_keyword(self):
        _check("Excel для Corel", intent=INTENT_ORDER, min_confidence=0.25)

    def test_corel_keyword(self):
        _check("корел", intent=INTENT_ORDER, min_confidence=0.25)


# ======================================================================
# Engineer keywords → engineer
# ======================================================================

class TestEngineerKeywords:
    def test_status_keyword(self):
        _check("какой статус проекта", intent=INTENT_ENGINEER, min_confidence=0.55)

    def test_next_step(self):
        _check("следующий шаг", intent=INTENT_ENGINEER, min_confidence=0.55)

    def test_check_keyword(self):
        _check("проверь отчёт", intent=INTENT_ENGINEER, min_confidence=0.5)

    def test_task_keyword(self):
        _check("задача для Hermes", intent=INTENT_ENGINEER, min_confidence=0.5,
               reason_contains="инженер")

    def test_report_keyword(self):
        _check("покажи отчёт", intent=INTENT_ENGINEER, min_confidence=0.5)

    def test_engineer_keyword(self):
        _check("инженер проекта", intent=INTENT_ENGINEER, min_confidence=0.5)

    def test_technical_task(self):
        _check("техническое задание", intent=INTENT_ENGINEER, min_confidence=0.55)

    def test_hermes_keyword(self):
        _check("запусти задачу для Hermes", intent=INTENT_ENGINEER, min_confidence=0.5)


# ======================================================================
# Ideas keywords → ideas
# ======================================================================

class TestIdeasKeywords:
    def test_idea_keyword(self):
        _check("у меня есть идея", intent=INTENT_IDEAS, min_confidence=0.55)

    def test_let_us_discuss(self):
        _check("давай обсудим новую идею", intent=INTENT_IDEAS, min_confidence=0.5,
               reason_contains="идеи")

    def test_what_if(self):
        _check("а что если добавить кнопку", intent=INTENT_IDEAS, min_confidence=0.5)

    def test_suggest(self):
        _check("предлагаю сделать так", intent=INTENT_IDEAS, min_confidence=0.45)

    def test_think_about(self):
        _check("подумать над улучшением", intent=INTENT_IDEAS, min_confidence=0.35)

    def test_optimization(self):
        _check("оптимизация производства", intent=INTENT_IDEAS, min_confidence=0.35)

    def test_interview(self):
        _check("интервью для опроса", intent=INTENT_IDEAS, min_confidence=0.40)


# ======================================================================
# Admin keywords → admin (with caution)
# ======================================================================

class TestAdminKeywords:
    def test_admin_keyword_low_conf(self):
        # "админ" alone is 0.55, below 0.85 → should clarify (unknown)
        _check("админ", intent=INTENT_UNKNOWN, has_clarify=True)

    def test_admin_diagnostics_more_clear(self):
        # "диагностика" alone is 0.55, below 0.85 → clarify
        _check("диагностика", intent=INTENT_UNKNOWN, has_clarify=True)

    def test_admin_combined_high_conf(self):
        # Multiple admin keywords combined still need to check
        # "админ диагностика" = 0.55 + 0.55 = 1.0 (capped) → should be admin
        result = classify_intent("админ диагностика сброс")
        assert result.intent == INTENT_ADMIN, f"Expected admin, got {result.intent}"

    def test_exact_admin_command_not_handled_here(self):
        # "/админ" is a command — this module handles free text, not commands
        # The text "/админ" doesn't contain "админ" as a word boundary
        pass

    def test_admin_reset(self):
        _check("сброс режима", intent=INTENT_UNKNOWN, has_clarify=True)


# ======================================================================
# Ambiguous / unclear phrases → unknown + clarify_question
# ======================================================================

class TestAmbiguousPhrases:
    def test_unclear_instruction(self):
        _check("разберись с файлом малярки", intent=INTENT_UNKNOWN, has_clarify=True)

    def test_vague_request(self):
        _check("сделай это нормально", intent=INTENT_UNKNOWN, has_clarify=True)

    def test_continue_phrase(self):
        _check("давай продолжим", intent=INTENT_UNKNOWN, has_clarify=True)

    def test_weather(self):
        _check("погода сегодня хорошая", intent=INTENT_UNKNOWN, has_clarify=True)

    def test_nonsense(self):
        _check("трамвай парабола крокодил", intent=INTENT_UNKNOWN, has_clarify=True)

    def test_single_word_unknown(self):
        _check("что-то", intent=INTENT_UNKNOWN, has_clarify=True)

    def test_numbers_only_no_dimensions(self):
        # Single number without space-separated dimension pattern
        _check("123", intent=INTENT_UNKNOWN, has_clarify=True)

    def test_simple_ok(self):
        _check("ок", intent=INTENT_UNKNOWN, has_clarify=True)

    def test_thanks(self):
        _check("спасибо", intent=INTENT_UNKNOWN, has_clarify=True)

    def test_hi(self):
        _check("привет", intent=INTENT_UNKNOWN, has_clarify=True)

    def test_order_request_with_make(self):
        # "сделай заказ" = 0.15 + 0.75 = 0.90 → order
        _check("сделай заказ", intent=INTENT_ORDER, min_confidence=0.70)

    def test_clear_order_request(self):
        # Multiple strong order keywords: "прими новый заказ" = 0.35 + 0.60 = 0.95
        _check("прими новый заказ", intent=INTENT_ORDER, min_confidence=0.7)


# ======================================================================
# Clarification question content
# ======================================================================

class TestClarificationContent:
    def test_clarification_has_options(self):
        result = classify_intent("разберись с файлом малярки")
        assert result.clarify_question is not None
        assert "Новый заказ" in result.clarify_question
        assert "Идея" in result.clarify_question
        assert "Инженер" in result.clarify_question
        assert "Отмена" in result.clarify_question


# ======================================================================
# Dangerous content → blocked
# ======================================================================

class TestDangerousContent:
    def test_dot_env_blocked(self):
        _check("дай .env", blocked=True, intent=INTENT_UNKNOWN)

    def test_token_blocked(self):
        _check("где token", blocked=True, intent=INTENT_UNKNOWN)

    def test_orders_db_blocked(self):
        _check("orders.db", blocked=True, intent=INTENT_UNKNOWN)

    def test_bot_py_blocked(self):
        _check("bot.py", blocked=True, intent=INTENT_UNKNOWN)

    def test_git_add_blocked(self):
        _check("git add все файлы", blocked=True, intent=INTENT_UNKNOWN)

    def test_git_commit_blocked(self):
        _check("сделай git commit", blocked=True, intent=INTENT_UNKNOWN)

    def test_git_push_blocked(self):
        _check("git push в репозиторий", blocked=True, intent=INTENT_UNKNOWN)

    def test_blocked_has_message(self):
        result = classify_intent("где .env")
        assert result.blocked is True
        assert result.block_message is not None
        assert "заблокирован" in result.block_message.lower()

    def normal_text_not_blocked(self):
        result = classify_intent("прими заказ 1000*400")
        assert result.blocked is False
        assert result.block_message is None


# ======================================================================
# Empty / short text
# ======================================================================

class TestEmptyText:
    def test_empty_string(self):
        _check("", intent=INTENT_UNKNOWN, has_clarify=True)

    def test_whitespace_only(self):
        _check("   ", intent=INTENT_UNKNOWN, has_clarify=True)

    def test_newline_only(self):
        _check("\n\n", intent=INTENT_UNKNOWN, has_clarify=True)


# ======================================================================
# Edge cases
# ======================================================================

class TestEdgeCases:
    def test_numbers_with_order_keyword(self):
        _check("заказ 800 600 2", intent=INTENT_ORDER, min_confidence=0.85,
               reason_contains="размеры")

    def test_numbers_similar_to_dimensions(self):
        # These could be dimensions if they have specific patterns
        _check("800 600", intent=INTENT_ORDER, min_confidence=0.85)

    def test_combined_order_and_ideas(self):
        # "давай обсудим заказ" — both order and ideas keywords
        # ideas: давай(0.25) + обсудим(0.70) = 0.95
        # order: заказ(0.75)
        # diff = 0.20 >= 0.15 → ideas wins (stronger ideas signal)
        _check("давай обсудим заказ", intent=INTENT_IDEAS, min_confidence=0.70)

    def test_one_number_only(self):
        # Single number is not a dimension pattern
        _check("1000", intent=INTENT_UNKNOWN, has_clarify=True)

    def test_excel_corel_sizes(self):
        # Mix of order keywords and dimensions
        _check("Excel для Corel 1000*400", intent=INTENT_ORDER, min_confidence=0.85)

    def test_mixed_intents_close(self):
        # "проверь идею" — engineer(0.35) vs ideas(0.55)
        # diff = 0.20 > 0.15 → ideas wins
        _check("проверь идею", intent=INTENT_IDEAS, min_confidence=0.35)

    def test_result_is_dataclass(self):
        result = classify_intent("1000*400")
        assert hasattr(result, "intent")
        assert hasattr(result, "confidence")
        assert hasattr(result, "reason")
        assert hasattr(result, "target_mode")
        assert hasattr(result, "clarify_question")
        assert hasattr(result, "blocked")
        assert hasattr(result, "block_message")

    def test_confidence_range(self):
        result = classify_intent("1000*400")
        assert 0.0 <= result.confidence <= 1.0

        result = classify_intent("привет")
        assert result.confidence == 0.0

        result = classify_intent("")
        assert result.confidence == 0.0


# ======================================================================
# No external calls
# ======================================================================

class TestNoExternalCalls:
    """Verify the module does not import or call external AI/API modules."""

    def test_no_openai_import(self):
        """Check no openai import."""
        import malyarka_telegram.intent as mod
        source = open(mod.__file__, encoding="utf-8").read()
        assert "openai" not in source.lower(), (
            "intent.py should not import or reference openai"
        )

    def test_no_http_libs(self):
        """Check no HTTP library imports."""
        import malyarka_telegram.intent as mod
        source = open(mod.__file__, encoding="utf-8").read().lower()
        for lib in ("requests", "httpx", "urllib"):
            assert lib not in source, f"intent.py should not import {lib}"

    def test_no_dotenv_import(self):
        """Check for python-dotenv import."""
        import malyarka_telegram.intent as mod
        source = open(mod.__file__, encoding="utf-8").read().lower()
        assert "dotenv" not in source, (
            "intent.py should not import python-dotenv"
        )

    def test_no_orders_db_access(self):
        """Check code does not reference external DB."""
        import malyarka_telegram.intent as mod
        source = open(mod.__file__, encoding="utf-8").read()
        assert "orders.db" not in source

    def test_no_bot_token(self):
        """Check no BOT_TOKEN reference."""
        import malyarka_telegram.intent as mod
        source = open(mod.__file__, encoding="utf-8").read()
        assert "BOT_TOKEN" not in source

    def test_no_deepseek_api_key(self):
        """Check no DEEPSEEK_API_KEY reference."""
        import malyarka_telegram.intent as mod
        source = open(mod.__file__, encoding="utf-8").read()
        assert "DEEPSEEK" not in source

    def test_no_os_environ_access(self):
        """Check no os.environ or os.getenv calls."""
        import malyarka_telegram.intent as mod
        source = open(mod.__file__, encoding="utf-8").read()
        assert "environ" not in source, (
            "intent.py should not access os.environ"
        )


# ======================================================================
# Target mode mapping
# ======================================================================

class TestTargetMode:
    def test_order_has_target(self):
        result = classify_intent("1000*400")
        assert result.target_mode == "order"

    def test_engineer_has_target(self):
        result = classify_intent("статус проекта")
        assert result.target_mode == "engineer"

    def test_ideas_has_target(self):
        result = classify_intent("у меня идея")
        assert result.target_mode == "ideas"

    def test_unknown_has_no_target(self):
        result = classify_intent("привет")
        assert result.target_mode is None


# ======================================================================
# Constants and API surface
# ======================================================================

class TestConstants:
    def test_all_intents_defined(self):
        assert INTENT_ORDER == "order"
        assert INTENT_IDEAS == "ideas"
        assert INTENT_ENGINEER == "engineer"
        assert INTENT_ADMIN == "admin"
        assert INTENT_UNKNOWN == "unknown"

    def test_threshold_is_exposed(self):
        assert isinstance(DEFAULT_CONFIDENCE_THRESHOLD, float)
        assert DEFAULT_CONFIDENCE_THRESHOLD > 0.0

    def test_classify_intent_is_callable(self):
        assert callable(classify_intent)


# ======================================================================
# Clarification response on ambiguous admin
# ======================================================================

class TestAdminClarification:
    def test_admin_clarification(self):
        """Admin-likely but not certain should clarify."""
        result = classify_intent("админ")
        assert result.is_unknown()

    def test_admin_diagnostics_full_phrase(self):
        """Admin diagnostics phrase should clarify."""
        result = classify_intent("проверь режим")
        assert result.is_unknown()

    def test_admin_strong_signal(self):
        """Multiple admin keywords should trigger admin."""
        result = classify_intent("админ диагностика")
        assert result.is_admin()


# ======================================================================
# Module import safety
# ======================================================================

def test_module_import_does_not_start_polling():
    """Just importing the module must not start any polling or servers."""
    import malyarka_telegram.intent
    # Re-import (no-op for cache, but confirms no side effects)
    importlib.reload(malyarka_telegram.intent)


def test_module_independent_of_libs():
    """The intent module should not import python-telegram-bot libs."""
    import malyarka_telegram.intent as mod
    source = open(mod.__file__, encoding="utf-8").read().lower()
    # The word 'telegram' appears in docstrings/comments (intent description).
    # But there should be NO import of 'telegram.ext'.
    lines = source.split('\n')
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('from ') or stripped.startswith('import '):
            assert 'telegram' not in stripped.lower(), (
                f"intent.py should not import telegram libs: {stripped}"
            )


# ======================================================================
# IntentResult convenience methods
# ======================================================================

class TestIntentResultHelpers:
    def test_is_order(self):
        r = IntentResult(intent="order", confidence=0.9, reason="test")
        assert r.is_order() is True
        assert r.is_ideas() is False
        assert r.is_engineer() is False
        assert r.is_admin() is False
        assert r.is_unknown() is False

    def test_is_ideas(self):
        r = IntentResult(intent="ideas", confidence=0.8, reason="test")
        assert r.is_order() is False
        assert r.is_ideas() is True
        assert r.is_unknown() is False

    def test_is_unknown(self):
        r = IntentResult(intent="unknown", confidence=0.0, reason="test")
        assert r.is_order() is False
        assert r.is_unknown() is True

    def test_is_admin(self):
        r = IntentResult(intent="admin", confidence=0.9, reason="test")
        assert r.is_admin() is True
        assert r.is_unknown() is False

    def test_is_engineer(self):
        r = IntentResult(intent="engineer", confidence=0.8, reason="test")
        assert r.is_engineer() is True
        assert r.is_order() is False
