"""Tests для dispute resolver Hermes-Clean."""

from hermes_clean import DisputeResolution, DisputeResolver, ResolverSummary
from hermes_clean.dispute_resolver import get_suggested_question, SUGGESTED_QUESTIONS


# ── Шаблоны вопросов ──

def test_all_dispute_reasons_have_question():
    reasons = ["missing_width", "missing_height", "too_many_numbers",
               "unclear_quantity", "unparsed_order_text", "empty_or_garbage",
               "unsupported_format"]
    for r in reasons:
        q = get_suggested_question(r)
        assert q, f"Reason '{r}' has no question template"
        assert q.endswith("."), f"Question for '{r}' should end with '.'"
        assert len(q) > 5, f"Question for '{r}' is too short"


def test_unknown_reason_returns_default():
    q = get_suggested_question("some_unknown_reason")
    assert q == "Уточнить строку."


def test_suggested_questions_are_non_empty():
    for reason, question in SUGGESTED_QUESTIONS.items():
        assert question, f"Empty question for reason '{reason}'"


# ── Resolver ──

def test_resolver_accept():
    resolver = DisputeResolver()
    disputed = {"dispute_id": "dispute-1", "source_line": 2, "raw_text": "1000", "reason": "missing_width"}
    outcome = resolver.resolve(disputed, {"action": "accept", "height": 1000, "width": 400, "quantity": 2})
    assert isinstance(outcome, DisputeResolution)
    assert outcome.resolved is True
    assert outcome.action == "accept"
    assert outcome.confirmed_row is not None
    assert outcome.confirmed_row["height"] == 1000
    assert outcome.confirmed_row["width"] == 400
    assert outcome.confirmed_row["quantity"] == 2


def test_resolver_accept_missing_fields():
    resolver = DisputeResolver()
    disputed = {"dispute_id": "dispute-1", "raw_text": "1000", "reason": "missing_width"}
    outcome = resolver.resolve(disputed, {"action": "accept", "height": 1000})
    assert outcome.resolved is False
    assert outcome.action == "clarify"


def test_resolver_delete():
    resolver = DisputeResolver()
    disputed = {"dispute_id": "dispute-1", "raw_text": "1000", "reason": "missing_width"}
    outcome = resolver.resolve(disputed, {"action": "delete"})
    assert outcome.resolved is True
    assert outcome.action == "delete"
    assert outcome.confirmed_row is None


def test_resolver_clarify():
    resolver = DisputeResolver()
    disputed = {"dispute_id": "dispute-1", "raw_text": "1000", "reason": "missing_width"}
    outcome = resolver.resolve(disputed, {"action": "clarify"})
    assert outcome.resolved is False
    assert outcome.action == "clarify"


def test_resolver_split():
    resolver = DisputeResolver()
    disputed = {"dispute_id": "dispute-1", "raw_text": "1000 400 5", "reason": "too_many_numbers"}
    outcome = resolver.resolve(disputed, {
        "action": "split",
        "rows": [
            {"height": 1000, "width": 400, "quantity": 2},
            {"height": 1000, "width": 400, "quantity": 3},
        ],
    })
    assert outcome.action == "split"
    assert outcome.confirmed_row is not None
    assert outcome.confirmed_row["height"] == 1000
    assert len(outcome.new_disputes) == 1


def test_resolver_max_attempts():
    resolver = DisputeResolver(max_resolution_attempts=2)
    disputed = {"dispute_id": "dispute-1", "raw_text": "1000", "reason": "missing_width"}
    for _ in range(2):
        outcome = resolver.resolve(disputed, {"action": "clarify"})
        assert outcome.resolved is False
    outcome = resolver.resolve(disputed, {"action": "clarify"})
    assert "Исчерпаны попытки" in outcome.note


def test_resolve_all():
    resolver = DisputeResolver()
    disputed_rows = [
        {"dispute_id": "d1", "raw_text": "1000", "reason": "missing_width", "source_line": 2},
        {"dispute_id": "d2", "raw_text": "мусор", "reason": "unparsed_order_text", "source_line": 3},
    ]
    resolutions = {
        "d1": {"action": "accept", "height": 1000, "width": 400, "quantity": 1},
        "d2": {"action": "delete"},
    }
    summary = resolver.resolve_all(disputed_rows, resolutions)
    assert isinstance(summary, ResolverSummary)
    assert summary.total_disputes == 2
    assert summary.resolved == 2
    assert summary.unresolved == 0
    assert summary.is_fully_resolved is True
    assert summary.export_unblocked is True
    assert len(summary.new_confirmed_rows) == 1


def test_resolve_all_partial():
    resolver = DisputeResolver()
    disputed_rows = [
        {"dispute_id": "d1", "raw_text": "1000", "reason": "missing_width"},
        {"dispute_id": "d2", "raw_text": "мусор", "reason": "unparsed_order_text"},
    ]
    resolutions = {
        "d1": {"action": "accept", "height": 1000, "width": 400, "quantity": 1},
    }
    summary = resolver.resolve_all(disputed_rows, resolutions)
    assert summary.total_disputes == 2
    assert summary.resolved == 1
    assert summary.unresolved == 1
    assert summary.is_fully_resolved is False
    assert summary.export_unblocked is False
