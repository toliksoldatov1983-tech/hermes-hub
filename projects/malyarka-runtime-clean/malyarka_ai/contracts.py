"""Safe JSON contract helpers for future DeepSeek order analysis."""

from __future__ import annotations

import json
from typing import Any


ALLOWED_DEEPSEEK_ITEM_TYPES = frozenset({"row", "disputed", "info", "scheme"})
REQUIRED_ROW_SIZE_FIELDS = ("height", "width", "quantity")

DEEPSEEK_ORDER_RESPONSE_CONTRACT: dict[str, Any] = {
    "items": [
        {
            "type": "row|disputed|info|scheme",
            "source": "text",
            "raw": "original input row",
            "size": {"height": 1000, "width": 400, "quantity": 1},
            "note": "",
            "reason": "",
        }
    ]
}


def validate_deepseek_order_response(data: Any) -> dict[str, Any]:
    """Validate a parsed DeepSeek JSON response against the safe order contract."""

    errors: list[str] = []

    if not isinstance(data, dict):
        return {"valid": False, "errors": ["response must be a JSON object"]}

    items = data.get("items")
    if not isinstance(items, list):
        return {"valid": False, "errors": ["items must be a list"]}

    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"items[{index}] must be an object")
            continue

        item_type = item.get("type")
        if item_type not in ALLOWED_DEEPSEEK_ITEM_TYPES:
            errors.append(f"items[{index}].type is not allowed")
            continue

        size = item.get("size", {})
        if size is None:
            size = {}
        if not isinstance(size, dict):
            errors.append(f"items[{index}].size must be an object")
            continue

        if item_type == "row":
            _validate_confirmed_row_size(size, index, errors)
        elif item_type == "disputed":
            reason = item.get("reason")
            if not isinstance(reason, str) or not reason.strip():
                errors.append(f"items[{index}].reason is required for disputed")
            _validate_optional_size(size, index, errors)
        else:
            _validate_optional_size(size, index, errors)

    return {"valid": not errors, "errors": errors}


def parse_deepseek_json_response(text: str | bytes | None) -> dict[str, Any]:
    """Parse and validate a future DeepSeek JSON response without raising."""

    if text is None:
        return {
            "valid": False,
            "data": None,
            "errors": ["response text is empty"],
        }

    try:
        decoded = text.decode("utf-8") if isinstance(text, bytes) else text
        data = json.loads(decoded)
    except (UnicodeDecodeError, TypeError, json.JSONDecodeError) as exc:
        return {"valid": False, "data": None, "errors": [f"invalid JSON: {exc}"]}

    validation = validate_deepseek_order_response(data)
    return {
        "valid": validation["valid"],
        "data": data if validation["valid"] else None,
        "errors": validation["errors"],
    }


def _validate_confirmed_row_size(
    size: dict[str, Any],
    index: int,
    errors: list[str],
) -> None:
    for field in REQUIRED_ROW_SIZE_FIELDS:
        if field not in size:
            errors.append(f"items[{index}].size.{field} is required for row")
            continue
        if not _is_positive_number(size[field]):
            errors.append(f"items[{index}].size.{field} must be positive")


def _validate_optional_size(
    size: dict[str, Any],
    index: int,
    errors: list[str],
) -> None:
    for field, value in size.items():
        if field in REQUIRED_ROW_SIZE_FIELDS and not _is_positive_number(value):
            errors.append(f"items[{index}].size.{field} must be positive")


def _is_positive_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0
