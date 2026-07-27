"""Tests для validation layer Hermes-Clean."""

from hermes_clean import validate_order_result, validate_single_row


# ── Валидация одной строки ──

def test_single_row_valid():
    result = validate_single_row({"height": 1000, "width": 400, "quantity": 2})
    assert result["valid"] is True
    assert result["violations"] == []


def test_single_row_height_out_of_range():
    result = validate_single_row({"height": 0, "width": 400, "quantity": 1})
    assert result["valid"] is False
    assert any(v["field"] == "height" for v in result["violations"])


def test_single_row_height_too_large():
    result = validate_single_row({"height": 30000, "width": 400, "quantity": 1})
    assert result["valid"] is False
    assert any(v["field"] == "height" for v in result["violations"])


def test_single_row_width_out_of_range():
    result = validate_single_row({"height": 1000, "width": 0, "quantity": 1})
    assert result["valid"] is False
    assert any(v["field"] == "width" for v in result["violations"])


def test_single_row_negative_quantity():
    result = validate_single_row({"height": 1000, "width": 400, "quantity": -1})
    assert result["valid"] is False
    assert any(v["field"] == "quantity" for v in result["violations"])


def test_single_row_zero_quantity():
    result = validate_single_row({"height": 1000, "width": 400, "quantity": 0})
    assert result["valid"] is False


def test_single_row_area_too_large():
    result = validate_single_row({"height": 20000, "width": 20000, "quantity": 1})
    assert result["valid"] is False
    assert any(v["reason"] == "area_too_large" for v in result["violations"])


def test_single_row_float_quantity():
    result = validate_single_row({"height": 1000, "width": 400, "quantity": 2.5})
    assert result["valid"] is False
    assert any(v["field"] == "quantity" for v in result["violations"])


# ── Валидация полного заказа ──

def test_clean_order_passes_validation():
    order = {
        "status": "clean",
        "confirmed_rows": [
            {"row_id": "row-1", "height": 1000, "width": 400, "quantity": 2},
            {"row_id": "row-2", "height": 700, "width": 300, "quantity": 1},
        ],
        "disputed_rows": [],
        "total_area_m2": 1.01,
    }
    v = validate_order_result(order)
    assert v["valid"] is True
    assert v["violations"] == []
    assert v["blocked"] is False


def test_disputed_order_has_validation_violations():
    order = {
        "status": "has_disputes",
        "confirmed_rows": [{"row_id": "row-1", "height": 1000, "width": 400, "quantity": 1}],
        "disputed_rows": [
            {"dispute_id": "d1", "raw_text": "мусор", "reason": "unparsed_order_text", "source_line": 2},
        ],
        "total_area_m2": 0.4,
    }
    v = validate_order_result(order)
    assert v["valid"] is False
    assert len(v["violations"]) >= 1
    assert v["blocked"] is True


def test_empty_order_passes_validation():
    order = {"status": "empty_or_invalid", "confirmed_rows": [], "disputed_rows": [], "total_area_m2": 0}
    v = validate_order_result(order)
    assert v["valid"] is True
    assert v["blocked"] is False


def test_zero_size_row_detected():
    order = {
        "status": "clean",
        "confirmed_rows": [{"row_id": "row-1", "height": 0, "width": 400, "quantity": 1}],
        "disputed_rows": [],
        "total_area_m2": 0,
    }
    v = validate_order_result(order)
    assert v["valid"] is False
    assert any(v["field"] == "height" for v in v["violations"])


def test_duplicate_rows_detected():
    order = {
        "status": "clean",
        "confirmed_rows": [
            {"row_id": "row-1", "height": 1000, "width": 400, "quantity": 2},
            {"row_id": "row-2", "height": 1000, "width": 400, "quantity": 2},
        ],
        "disputed_rows": [],
        "total_area_m2": 0.8,
    }
    v = validate_order_result(order)
    assert v["valid"] is False
    assert any(v["reason"] == "duplicate_row" for v in v["violations"])


def test_non_duplicate_rows_passes():
    order = {
        "status": "clean",
        "confirmed_rows": [
            {"row_id": "row-1", "height": 1000, "width": 400, "quantity": 2},
            {"row_id": "row-2", "height": 700, "width": 300, "quantity": 1},
        ],
        "disputed_rows": [],
        "total_area_m2": 1.01,
    }
    v = validate_order_result(order)
    assert v["valid"] is True


def test_negative_total_area():
    order = {
        "status": "clean",
        "confirmed_rows": [{"row_id": "row-1", "height": 1000, "width": 400, "quantity": 2}],
        "disputed_rows": [],
        "total_area_m2": -1.0,
    }
    v = validate_order_result(order)
    assert v["valid"] is False
    assert any(v["reason"] == "negative_area" for v in v["violations"])
