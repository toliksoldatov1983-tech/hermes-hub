from hermes_modules.malyarka.hardening_adapter import (
    build_safe_export_preview,
    get_hardening_status,
    validate_synthetic_order_result,
)


def test_hardening_status_exposes_compatibility_layer():
    status = get_hardening_status()

    assert status.compatibility_layer == "hermes_clean"
    assert status.fixture_count >= 10
    assert status.validation_available is True
    assert status.export_gate_available is True
    assert "synthetic" in status.allowed_preview_sources
    assert "real_order" in status.blocked_sources


def test_validate_synthetic_order_result_uses_hardening_layer():
    result = validate_synthetic_order_result(
        {
            "status": "clean",
            "confirmed_rows": [{"height": 1000, "width": 400, "quantity": 1}],
            "disputed_rows": [],
            "total_area_m2": 0.4,
        }
    )

    assert result["valid"] is True
    assert result["blocked"] is False


def test_export_preview_blocks_real_order_source():
    preview = build_safe_export_preview(
        {
            "status": "clean",
            "confirmed_rows": [{"height": 1000, "width": 400, "quantity": 1}],
            "disputed_rows": [],
            "total_area_m2": 0.4,
        },
        source_type="real_order",
    )

    assert preview["export_blocked"] is True
    assert preview["reason"] == "source_type_blocked:real_order"
    assert preview["source_type"] == "real_order"


def test_export_preview_allows_synthetic_clean_order():
    preview = build_safe_export_preview(
        {
            "status": "clean",
            "confirmed_rows": [{"height": 1000, "width": 400, "quantity": 1}],
            "disputed_rows": [],
            "total_area_m2": 0.4,
        },
        source_type="synthetic",
    )

    assert preview["export_blocked"] is False
    assert preview["source_type"] == "synthetic"
    assert preview["validation"]["valid"] is True


def test_export_preview_blocks_validation_failure():
    preview = build_safe_export_preview(
        {
            "status": "clean",
            "confirmed_rows": [{"height": 0, "width": 400, "quantity": 1}],
            "disputed_rows": [],
            "total_area_m2": 0,
        },
        source_type="synthetic",
    )

    assert preview["export_blocked"] is True
    assert preview["reason"] == "validation_failed"
