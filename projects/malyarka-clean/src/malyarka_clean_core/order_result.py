"""Final order result integration for the first Malyarka Clean slice."""

from .area_calculator import calculate_area
from .dispute_detector import build_parse_result
from .order_input import prepare_order_input
from .size_parser import parse_size_lines


def build_order_result(raw_text, source="manual", received_at=None):
    """Parse raw text, calculate confirmed area and return one order result."""
    input_data = prepare_order_input(raw_text, source=source, received_at=received_at)
    parsed_data = parse_size_lines(input_data["original_lines"])
    parse_result = build_parse_result(input_data, parsed_data)
    area_result = calculate_area(
        parse_result["confirmed_rows"],
        disputed_rows=parse_result["disputed_rows"],
    )

    return combine_order_result(input_data, parse_result, area_result)


def combine_order_result(input_data, parse_result, area_result):
    """Combine parser, dispute and area outputs into the final result shape."""
    confirmed_rows = parse_result["confirmed_rows"]
    disputed_rows = parse_result["disputed_rows"]

    if not confirmed_rows and _is_empty_or_garbage_only(disputed_rows):
        status = "empty_or_invalid"
    elif disputed_rows:
        status = "has_disputes"
    else:
        status = "clean"

    export_blocked = status != "clean" or area_result["export_blocked"]
    dispute_reasons = [row["reason"] for row in disputed_rows]

    return {
        "source": input_data["source"],
        "raw_text": input_data["raw_text"],
        "status": status,
        "confirmed_rows": confirmed_rows,
        "disputed_rows": disputed_rows,
        "total_area_m2": area_result["total_area_m2"],
        "export_blocked": export_blocked,
        "short_summary": _short_summary(status, confirmed_rows, disputed_rows, area_result),
        "dispute_reasons": dispute_reasons,
        "warnings": area_result["warnings"],
        "next_action": _next_action(status),
    }


def _short_summary(status, confirmed_rows, disputed_rows, area_result):
    confirmed_count = len(confirmed_rows)
    disputed_count = len(disputed_rows)
    total_area_m2 = area_result["total_area_m2"]

    if status == "empty_or_invalid":
        return "no valid order rows found"
    if status == "has_disputes":
        return (
            f"{confirmed_count} confirmed row(s), "
            f"{disputed_count} disputed row(s), export blocked"
        )
    return f"{confirmed_count} confirmed row(s), {total_area_m2} m2 total"


def _next_action(status):
    if status == "clean":
        return "ready_for_export_later"
    if status == "has_disputes":
        return "review_disputes"
    return "provide_valid_order_text"


def _is_empty_or_garbage_only(disputed_rows):
    if not disputed_rows:
        return True

    garbage_reasons = {
        "empty_or_garbage",
        "unparsed_order_text",
    }
    return all(row.get("reason") in garbage_reasons for row in disputed_rows)
