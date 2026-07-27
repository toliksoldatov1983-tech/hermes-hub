from hermes_modules.malyarka.export_contract import export_blocked_until_confirmed
from hermes_modules.malyarka.export_preview import build_export_preview
from hermes_modules.malyarka.export_source_policy import classify_export_source
from hermes_modules.malyarka.parser_contract import ParserContract


def test_synthetic_source_allows_preview_but_not_file_write():
    decision = classify_export_source("synthetic")

    assert decision.allowed_for_preview is True
    assert decision.allowed_for_file_write is False
    assert decision.blocked is False


def test_manual_source_allows_preview_but_not_file_write():
    decision = classify_export_source("manual")

    assert decision.allowed_for_preview is True
    assert decision.allowed_for_file_write is False


def test_real_order_source_is_blocked():
    decision = classify_export_source("real_order")

    assert decision.blocked is True
    assert decision.reason == "source_type_blocked:real_order"


def test_google_drive_source_is_blocked():
    decision = classify_export_source("google_drive")

    assert decision.blocked is True
    assert decision.reason == "source_type_blocked:google_drive"


def test_export_contract_blocks_forbidden_source_even_with_approval():
    order = ParserContract().parse("paint | 2 | bucket")

    status = export_blocked_until_confirmed(order, approved=True, source_type="archive")

    assert status == "BLOCKED: source_type_blocked:archive."


def test_export_contract_keeps_dispute_block():
    order = ParserContract().parse("broken row")

    status = export_blocked_until_confirmed(order, approved=True, source_type="synthetic")

    assert status == "BLOCKED: disputed rows must be resolved before export."


def test_export_preview_reports_blocked_source():
    order = ParserContract().parse("paint | 2 | bucket")

    preview = build_export_preview(order, source_type="real_order")

    assert preview.can_write_file is False
    assert preview.source_type == "real_order"
    assert preview.blocked_reason == "source_type_blocked:real_order"
