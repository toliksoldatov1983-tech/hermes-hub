"""Minimal dispute result builder for the first local parser."""


def build_parse_result(input_data, parsed_data):
    """Build the first order parse result from prepared input and parsed rows."""
    if input_data["preliminary_status"] == "empty_or_invalid":
        status = "empty_or_invalid"
    elif parsed_data["disputed_rows"]:
        status = "has_disputes"
    else:
        status = "clean"

    return {
        "source": input_data["source"],
        "status": status,
        "raw_text": input_data["raw_text"],
        "confirmed_rows": _confirmed_rows(parsed_data["candidate_rows"]),
        "disputed_rows": _disputed_rows(parsed_data["disputed_rows"]),
        "summary": _summary(status, parsed_data),
    }


def _confirmed_rows(candidate_rows):
    rows = []
    for index, row in enumerate(candidate_rows, start=1):
        rows.append({
            "row_id": f"row-{index}",
            **row,
        })
    return rows


def _disputed_rows(disputed_rows):
    rows = []
    for index, row in enumerate(disputed_rows, start=1):
        rows.append({
            "dispute_id": f"dispute-{index}",
            "missing_fields": _missing_fields(row["reason"]),
            "suggested_question": _suggested_question(row["reason"]),
            "severity": "needs_user_review",
            **row,
        })
    return rows


def _missing_fields(reason):
    if reason == "missing_width":
        return ["width"]
    if reason == "missing_height":
        return ["height"]
    return []


def _suggested_question(reason):
    questions = {
        "missing_width": "Уточнить ширину строки.",
        "missing_height": "Уточнить высоту строки.",
        "too_many_numbers": "Уточнить, какие числа являются высотой, шириной и количеством.",
        "unclear_quantity": "Уточнить количество.",
        "unparsed_order_text": "Уточнить, влияет ли текст на заказ.",
        "empty_or_garbage": "Проверить строку или удалить ее.",
        "unsupported_format": "Уточнить размер в формате высота ширина количество.",
    }
    return questions.get(reason, "Уточнить строку.")


def _summary(status, parsed_data):
    return {
        "confirmed_count": len(parsed_data["candidate_rows"]),
        "disputed_count": len(parsed_data["disputed_rows"]),
        "next_action": "review_disputes" if status != "clean" else "ready_for_area_later",
    }
