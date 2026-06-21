from malyarka_clean_core import build_corel_export_model, build_order_result


def test_clean_order_prepares_corel_rows():
    order_result = build_order_result("1000 400 2")

    result = build_corel_export_model(order_result)

    assert result["export_blocked"] is False
    assert result["reason"] == "ready"
    assert result["source_status"] == "clean"
    assert result["corel_rows"] == [
        {
            "height_mm": 1000,
            "width_mm": 400,
            "quantity": 2,
        }
    ]


def test_corel_row_contains_only_required_fields():
    order_result = build_order_result("1000 400 2")

    result = build_corel_export_model(order_result)

    assert set(result["corel_rows"][0]) == {"height_mm", "width_mm", "quantity"}


def test_order_with_disputes_blocks_corel_rows():
    order_result = build_order_result("1000 400\n1000")

    result = build_corel_export_model(order_result)

    assert result["corel_rows"] == []
    assert result["export_blocked"] is True
    assert result["reason"] == "disputed_rows_present"
    assert result["source_status"] == "has_disputes"


def test_empty_order_blocks_corel_rows():
    order_result = build_order_result("")

    result = build_corel_export_model(order_result)

    assert result["corel_rows"] == []
    assert result["export_blocked"] is True
    assert result["reason"] == "empty_or_invalid"
    assert result["source_status"] == "empty_or_invalid"


def test_garbage_order_blocks_corel_rows_as_empty_or_invalid():
    order_result = build_order_result("привет\nничего непонятно")

    result = build_corel_export_model(order_result)

    assert result["corel_rows"] == []
    assert result["export_blocked"] is True
    assert result["source_status"] == "empty_or_invalid"


def test_export_blocked_reason_is_reported():
    order_result = build_order_result("1000 400")
    order_result["export_blocked"] = True

    result = build_corel_export_model(order_result)

    assert result["corel_rows"] == []
    assert result["export_blocked"] is True
    assert result["reason"] == "export_blocked"
