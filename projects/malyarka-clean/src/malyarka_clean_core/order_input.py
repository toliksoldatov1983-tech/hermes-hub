"""Input boundary for raw order text."""


def prepare_order_input(raw_text, source="manual", received_at=None):
    """Normalize raw text enough for the first local parser."""
    text = "" if raw_text is None else str(raw_text)
    normalized_text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    original_lines = normalized_text.split("\n") if normalized_text else []
    status = "empty_or_invalid" if not normalized_text else "clean"

    return {
        "source": source,
        "received_at": received_at,
        "raw_text": text,
        "normalized_text": normalized_text,
        "original_lines": original_lines,
        "preliminary_status": status,
    }
