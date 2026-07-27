"""Tests для export model Hermes-Clean (политика экспорта)."""

from hermes_clean import build_export_model


def test_clean_order_prepares_export_rows():
    order = {"status": "clean", "confirmed_rows": [{"height": 1000, "width": 400, "quantity": 2}], "disputed_rows": []}
    result = build_export_model(order)
    assert result["export_blocked"] is False
    assert result["reason"] == "ready"
    assert result["source_status"] == "clean"
    assert result["export_rows"] == [{"height_mm": 1000, "width_mm": 400, "quantity": 2}]


def test_export_row_contains_only_required_fields():
    order = {"status": "clean", "confirmed_rows": [{"height": 1000, "width": 400, "quantity": 2}], "disputed_rows": []}
    result = build_export_model(order)
    assert set(result["export_rows"][0]) == {"height_mm", "width_mm", "quantity"}


def test_order_with_disputes_blocks_export():
    order = {"status": "has_disputes", "confirmed_rows": [{"height": 1000, "width": 400, "quantity": 2}],
             "disputed_rows": [{"dispute_id": "d1", "raw_text": "1000", "reason": "missing_width"}]}
    result = build_export_model(order)
    assert result["export_rows"] == []
    assert result["export_blocked"] is True
    assert result["reason"] == "disputed_rows_present"
    assert result["source_status"] == "has_disputes"


def test_empty_order_blocks_export():
    order = {"status": "empty_or_invalid", "confirmed_rows": [], "disputed_rows": []}
    result = build_export_model(order)
    assert result["export_rows"] == []
    assert result["export_blocked"] is True
    assert result["reason"] == "empty_or_invalid"
    assert result["source_status"] == "empty_or_invalid"


def test_garbage_order_blocks_export():
    order = {"status": "has_disputes", "confirmed_rows": [],
             "disputed_rows": [{"dispute_id": "d1", "raw_text": "привет", "reason": "unparsed_order_text"}]}
    result = build_export_model(order)
    assert result["export_rows"] == []
    assert result["export_blocked"] is True


def test_export_blocked_reason_is_reported():
    order = {"status": "clean", "confirmed_rows": [{"height": 1000, "width": 400, "quantity": 2}],
             "disputed_rows": [], "export_blocked": True}
    result = build_export_model(order)
    assert result["export_rows"] == []
    assert result["export_blocked"] is True
    assert result["reason"] == "export_blocked"
