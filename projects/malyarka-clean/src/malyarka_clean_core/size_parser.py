"""First local size parser for approved simple formats."""

import re


_PLAIN_NUMBER_LINE = re.compile(r"^\s*(\d+)(?:\s+(\d+))?(?:\s+(\d+))?\s*$")
_SEPARATED_SIZE_LINE = re.compile(r"^\s*(\d+)\s*[xX*\u00d7]\s*(\d+)\s*$")
_HAS_LETTERS = re.compile(r"[A-Za-zА-Яа-яЁё]")


def parse_size_lines(original_lines):
    """Parse approved size-only lines into candidates and disputed rows."""
    candidate_rows = []
    disputed_rows = []

    for index, raw_line in enumerate(original_lines, start=1):
        line = raw_line.strip()
        if not line:
            disputed_rows.append(_dispute(index, raw_line, "empty_or_garbage"))
            continue

        separated_match = _SEPARATED_SIZE_LINE.match(line)
        if separated_match:
            height, width = separated_match.groups()
            candidate_rows.append(_candidate(index, raw_line, height, width, "1"))
            continue

        if _HAS_LETTERS.search(line):
            disputed_rows.append(_dispute(index, raw_line, "unparsed_order_text"))
            continue

        plain_match = _PLAIN_NUMBER_LINE.match(line)
        if plain_match:
            height, width, quantity = plain_match.groups()
            if width is None:
                disputed_rows.append(_dispute(index, raw_line, "missing_width"))
                continue
            candidate_rows.append(_candidate(index, raw_line, height, width, quantity or "1"))
            continue

        numbers = re.findall(r"\d+", line)
        if len(numbers) > 3:
            disputed_rows.append(_dispute(index, raw_line, "too_many_numbers"))
        elif len(numbers) == 1:
            disputed_rows.append(_dispute(index, raw_line, "missing_width"))
        elif len(numbers) == 0:
            disputed_rows.append(_dispute(index, raw_line, "empty_or_garbage"))
        else:
            disputed_rows.append(_dispute(index, raw_line, "unsupported_format"))

    return {
        "candidate_rows": candidate_rows,
        "disputed_rows": disputed_rows,
        "parsing_notes": [],
    }


def _candidate(source_line, raw_text, height, width, quantity):
    return {
        "source_line": source_line,
        "raw_text": raw_text,
        "height": int(height),
        "width": int(width),
        "quantity": int(quantity),
        "unit": "mm",
        "notes": [],
    }


def _dispute(source_line, raw_text, reason):
    return {
        "source_line": source_line,
        "raw_text": raw_text,
        "reason": reason,
    }
