from malyarka_clean_core import calculate_area


def test_single_confirmed_row_quantity_one():
    result = calculate_area([
        {"row_id": "row-1", "height": 1000, "width": 400, "quantity": 1}
    ])

    assert result["total_area_m2"] == 0.4
    assert result["calculated_rows"][0]["area_m2"] == 0.4
    assert result["export_blocked"] is False


def test_single_confirmed_row_quantity_two():
    result = calculate_area([
        {"row_id": "row-1", "height": 1000, "width": 400, "quantity": 2}
    ])

    assert result["total_area_m2"] == 0.8
    assert result["calculated_rows"][0]["area_m2"] == 0.8
    assert result["export_blocked"] is False


def test_multiple_confirmed_rows_sum_total_area():
    result = calculate_area([
        {"row_id": "row-1", "height": 1000, "width": 400, "quantity": 1},
        {"row_id": "row-2", "height": 500, "width": 300, "quantity": 2},
    ])

    assert result["total_area_m2"] == 0.7
    assert [row["area_m2"] for row in result["calculated_rows"]] == [0.4, 0.3]
    assert result["export_blocked"] is False


def test_disputed_rows_are_excluded_and_block_export():
    disputed = [{"dispute_id": "dispute-1", "raw_text": "1000", "reason": "missing_width"}]

    result = calculate_area([
        {"row_id": "row-1", "height": 1000, "width": 400, "quantity": 1}
    ], disputed_rows=disputed)

    assert result["total_area_m2"] == 0.4
    assert result["excluded_disputed_rows"] == disputed
    assert result["export_blocked"] is True
    assert result["export_block_reason"] == "unresolved_disputes"


def test_empty_confirmed_rows_return_zero_area():
    result = calculate_area([])

    assert result["total_area_m2"] == 0
    assert result["calculated_rows"] == []
    assert result["export_blocked"] is False
