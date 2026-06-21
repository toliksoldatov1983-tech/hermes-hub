from malyarka_clean_core import build_corel_export_model, build_order_result


def test_clean_order_pipeline_smoke():
    order_result = build_order_result("1000 400 2")
    corel_model = build_corel_export_model(order_result)

    assert order_result["status"] == "clean"
    assert order_result["disputed_rows"] == []
    assert order_result["export_blocked"] is False
    assert order_result["total_area_m2"] == 0.8
    assert corel_model["export_blocked"] is False
    assert corel_model["reason"] == "ready"
    assert corel_model["source_status"] == "clean"
    assert corel_model["corel_rows"] == [
        {
            "height_mm": 1000,
            "width_mm": 400,
            "quantity": 2,
        }
    ]


def test_disputed_order_pipeline_smoke():
    order_result = build_order_result("1000 400\n1000")
    corel_model = build_corel_export_model(order_result)

    assert order_result["status"] == "has_disputes"
    assert order_result["disputed_rows"] != []
    assert order_result["total_area_m2"] == 0.4
    assert order_result["export_blocked"] is True
    assert corel_model["corel_rows"] == []
    assert corel_model["export_blocked"] is True
    assert corel_model["reason"] == "disputed_rows_present"
    assert corel_model["source_status"] == "has_disputes"


def test_empty_order_pipeline_smoke():
    order_result = build_order_result("")
    corel_model = build_corel_export_model(order_result)

    assert order_result["status"] == "empty_or_invalid"
    assert order_result["total_area_m2"] == 0
    assert order_result["export_blocked"] is True
    assert corel_model["corel_rows"] == []
    assert corel_model["export_blocked"] is True
    assert corel_model["source_status"] == "empty_or_invalid"


def test_garbage_order_pipeline_smoke():
    order_result = build_order_result("привет\nничего непонятно")
    corel_model = build_corel_export_model(order_result)

    assert order_result["status"] == "empty_or_invalid"
    assert order_result["confirmed_rows"] == []
    assert order_result["total_area_m2"] == 0
    assert order_result["export_blocked"] is True
    assert corel_model["corel_rows"] == []
    assert corel_model["export_blocked"] is True
    assert corel_model["source_status"] == "empty_or_invalid"
