from malyarka_clean_core import build_order_result


def test_clean_order_result():
    result = build_order_result("1000 400 2")

    assert result["status"] == "clean"
    assert len(result["confirmed_rows"]) == 1
    assert result["disputed_rows"] == []
    assert result["total_area_m2"] == 0.8
    assert result["export_blocked"] is False
    assert result["dispute_reasons"] == []
    assert result["next_action"] == "ready_for_export_later"


def test_order_result_with_dispute_blocks_export():
    result = build_order_result("1000 400\n1000")

    assert result["status"] == "has_disputes"
    assert len(result["confirmed_rows"]) == 1
    assert len(result["disputed_rows"]) == 1
    assert result["total_area_m2"] == 0.4
    assert result["export_blocked"] is True
    assert result["dispute_reasons"] == ["missing_width"]
    assert result["next_action"] == "review_disputes"


def test_empty_order_result():
    result = build_order_result("")

    assert result["status"] == "empty_or_invalid"
    assert result["confirmed_rows"] == []
    assert result["disputed_rows"] == []
    assert result["total_area_m2"] == 0
    assert result["export_blocked"] is True
    assert result["dispute_reasons"] == []
    assert result["next_action"] == "provide_valid_order_text"


def test_garbage_order_result_is_empty_or_invalid():
    result = build_order_result("привет\nничего непонятно")

    assert result["status"] == "empty_or_invalid"
    assert result["confirmed_rows"] == []
    assert len(result["disputed_rows"]) == 2
    assert result["total_area_m2"] == 0
    assert result["export_blocked"] is True
    assert result["next_action"] == "provide_valid_order_text"


def test_partial_size_without_width_stays_disputed():
    result = build_order_result("1000")

    assert result["status"] == "has_disputes"
    assert result["confirmed_rows"] == []
    assert len(result["disputed_rows"]) == 1
    assert result["dispute_reasons"] == ["missing_width"]
    assert result["export_blocked"] is True
