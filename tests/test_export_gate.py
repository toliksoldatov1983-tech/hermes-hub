"""Tests для ExportBlockedError gate hardening Hermes-Clean."""

import pytest
from hermes_clean import ExportBlockedError, build_export_model


def test_clean_order_no_exception():
    order = {"status": "clean", "confirmed_rows": [{"height": 1000, "width": 400, "quantity": 2}], "disputed_rows": []}
    model = build_export_model(order, strict=True)
    assert model["export_blocked"] is False
    assert model["reason"] == "ready"


def test_disputed_order_raises_in_strict_mode():
    order = {"status": "has_disputes", "confirmed_rows": [{"height": 1000, "width": 400, "quantity": 2}],
             "disputed_rows": [{"dispute_id": "d1", "raw_text": "мусор", "reason": "unparsed_order_text"}]}
    with pytest.raises(ExportBlockedError) as exc:
        build_export_model(order, strict=True)
    assert "disputed_rows_present" in str(exc.value)
    assert exc.value.reason == "disputed_rows_present"
    assert exc.value.source_status == "has_disputes"


def test_empty_order_raises_in_strict_mode():
    order = {"status": "empty_or_invalid", "confirmed_rows": [], "disputed_rows": []}
    with pytest.raises(ExportBlockedError):
        build_export_model(order, strict=True)


def test_garbage_order_raises_in_strict_mode():
    order = {"status": "has_disputes", "confirmed_rows": [],
             "disputed_rows": [{"dispute_id": "d1", "raw_text": "привет", "reason": "unparsed_order_text"}]}
    with pytest.raises(ExportBlockedError):
        build_export_model(order, strict=True)


def test_disputed_order_blocked_dict_in_non_strict():
    order = {"status": "has_disputes", "confirmed_rows": [{"height": 1000, "width": 400, "quantity": 1}],
             "disputed_rows": [{"dispute_id": "d1", "raw_text": "мусор", "reason": "unparsed_order_text"}]}
    model = build_export_model(order)
    assert model["export_blocked"] is True
    assert model["export_rows"] == []


def test_manually_blocked_order_raises_in_strict_mode():
    order = {"status": "clean", "confirmed_rows": [{"height": 1000, "width": 400, "quantity": 2}],
             "disputed_rows": [], "export_blocked": True}
    with pytest.raises(ExportBlockedError):
        build_export_model(order, strict=True)


def test_export_blocked_error_is_value_error():
    assert issubclass(ExportBlockedError, ValueError)
