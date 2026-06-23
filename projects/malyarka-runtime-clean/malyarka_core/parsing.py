"""Simple text parser for Malyarka order dimensions without Vision."""

from __future__ import annotations

import re

from .models import DisputedItem, OrderDraft, OrderItem

_POSITION_PREFIX_RE = re.compile(r"^\s*(?:№\s*)?\d+\s*[\)\.\:]\s*")
_SIZE_SEPARATOR_RE = re.compile(r"\s*[\*xхXХ×]\s*")
_NUMBER_RE = re.compile(r"-?\d+")


def remove_leading_position_number(line: str) -> str:
    """Remove a leading position number like '1. ' before parsing dimensions."""

    return _POSITION_PREFIX_RE.sub("", line.strip(), count=1)


def normalize_size_separators(line: str) -> str:
    """Convert common size separators to spaces before extracting numbers."""

    return _SIZE_SEPARATOR_RE.sub(" ", line)


def parse_size_line(line: str) -> tuple[OrderItem | None, DisputedItem | None]:
    """Parse one text line into either a confirmed item or a disputed item."""

    raw_line = line.strip()
    if not raw_line:
        return None, None

    cleaned = normalize_size_separators(remove_leading_position_number(raw_line))
    numbers = [int(value) for value in _NUMBER_RE.findall(cleaned)]

    if len(numbers) < 2:
        return None, DisputedItem(
            raw=raw_line,
            reason="Найдено меньше двух чисел: нужны высота и ширина.",
        )

    height = numbers[0]
    width = numbers[1]
    quantity = numbers[2] if len(numbers) >= 3 else 1

    if height <= 0 or width <= 0 or quantity <= 0:
        return None, DisputedItem(
            raw=raw_line,
            reason="Высота, ширина и количество должны быть больше нуля.",
        )

    return OrderItem(
        height=height,
        width=width,
        quantity=quantity,
        source=raw_line,
    ), None


def parse_sizes_text(text: str) -> OrderDraft:
    """Parse multiline text into confirmed and disputed order items."""

    draft = OrderDraft()

    for line in text.splitlines():
        item, disputed_item = parse_size_line(line)

        if item is not None:
            draft.items.append(item)

        if disputed_item is not None:
            draft.disputed_items.append(disputed_item)

    return draft
