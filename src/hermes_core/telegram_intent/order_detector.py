"""Malyarka Order Detector — detects orders in chat messages.

Recognizes patterns: dimensions, quantities, colors, materials.
All dry-run. No real orders.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


# ── Order patterns ──

_DIMENSION_PATTERNS = [
    re.compile(r"(\d{2,4})\s*[xх×*]\s*(\d{2,4})"),   # 720x300, 720х300
    re.compile(r"(\d{2,4})\s*[xх×*]\s*(\d{2,4})\s*[xх×*]\s*(\d{2,4})"),  # 720x300x18
    re.compile(r"(\d{2,4})\s*на\s*(\d{2,4})"),        # 720 на 300
]

_QUANTITY_PATTERNS = [
    re.compile(r"(\d+)\s*(?:шт|штук|штуки|pcs|pieces?)", re.IGNORECASE),
    re.compile(r"количество[:\s]*(\d+)", re.IGNORECASE),
    re.compile(r"кол-во[:\s]*(\d+)", re.IGNORECASE),
]

_COLOR_PATTERNS = [
    re.compile(r"(?:цвет|color)[:\s]*([а-яёa-z\s]+)", re.IGNORECASE),
    re.compile(r"(?:краска|покраска|paint)[:\s]*([а-яёa-z\s]+)", re.IGNORECASE),
]

_MATERIAL_PATTERNS = [
    re.compile(r"(?:материал|material)[:\s]*([а-яёa-z\s]+)", re.IGNORECASE),
    re.compile(r"(?:мдф|мдвп|дсп|лдсп|фанера|mdf|plywood)", re.IGNORECASE),
    re.compile(r"(?:фасад|фасады|fronts?)", re.IGNORECASE),
]

_ORDER_NAME_PATTERNS = [
    re.compile(r"(?:заказ|order)[:\s#]*([а-яёa-z0-9\s\-]+)", re.IGNORECASE),
    re.compile(r"(?:клиент|customer|заказчик)[:\s]*([а-яёa-z\s]+)", re.IGNORECASE),
]

_CORRECTION_PATTERNS = [
    re.compile(r"(?:исправ|поправ|замен|вмест|correct|fix|change|replace)", re.IGNORECASE),
    re.compile(r"(?:не\s+(?:так|то|правильно)|ошиб(?:ка|ся))", re.IGNORECASE),
]

_CONFIRMATION_PATTERNS = [
    re.compile(r"^(?:да|yes|ок|ok|okay|ага|угу|верно|правильно|подтвержд|confirm|соглас)", re.IGNORECASE),
    re.compile(r"^(?:отправ|export|готов|заверш)", re.IGNORECASE),
]


@dataclass
class OrderDetectionResult:
    """Result of order detection in a message."""

    is_order: bool = False
    confidence: float = 0.0
    found_patterns: list[str] = field(default_factory=list)
    dimensions_found: bool = False
    quantity_found: bool = False
    color_found: bool = False
    material_found: bool = False
    order_name_found: bool = False
    is_correction: bool = False
    is_confirmation: bool = False
    reason: str = ""
    extracted: dict[str, Any] = field(default_factory=dict)
    audit: dict[str, Any] = field(default_factory=lambda: {
        "real_order": False,
        "synthetic": True,
        "env_read": False,
    })


def detect_order(text: str) -> OrderDetectionResult:
    """Detect if a message contains a Malyarka order.

    Returns detection result with confidence and extracted data.
    """
    result = OrderDetectionResult()
    text_lower = text.lower()

    # The dry-run order draft format is one or more item|quantity|unit
    # rows. Treat it as an explicit order even when it contains no
    # dimensions, colours or material keywords.
    pipe_rows = [line.strip() for line in text.splitlines() if line.strip()]
    valid_pipe_rows = [
        line for line in pipe_rows
        if len(line.split("|")) >= 3 and all(part.strip() for part in line.split("|")[:3])
    ]
    if valid_pipe_rows:
        result.found_patterns.append("structured_rows")
        result.extracted["structured_rows"] = valid_pipe_rows

    # Check for corrections/confirmations first
    for pat in _CORRECTION_PATTERNS:
        if pat.search(text_lower):
            result.is_correction = True
            result.found_patterns.append("correction")
            break

    for pat in _CONFIRMATION_PATTERNS:
        if pat.search(text_lower):
            result.is_confirmation = True
            result.found_patterns.append("confirmation")
            break

    # Dimension detection
    for pat in _DIMENSION_PATTERNS:
        m = pat.search(text_lower)
        if m:
            result.dimensions_found = True
            result.found_patterns.append("dimensions")
            dims = [g for g in m.groups()]
            result.extracted["dimensions"] = dims
            break

    # Quantity detection
    for pat in _QUANTITY_PATTERNS:
        m = pat.search(text_lower)
        if m:
            result.quantity_found = True
            result.found_patterns.append("quantity")
            result.extracted["quantity"] = m.group(1)
            break

    # Color detection
    for pat in _COLOR_PATTERNS:
        m = pat.search(text_lower)
        if m:
            result.color_found = True
            result.found_patterns.append("color")
            result.extracted["color"] = m.group(1).strip()
            break

    # Material detection
    for pat in _MATERIAL_PATTERNS:
        m = pat.search(text_lower)
        if m:
            result.material_found = True
            result.found_patterns.append("material")
            break

    # Order name detection
    for pat in _ORDER_NAME_PATTERNS:
        if pat.search(text_lower):
            result.order_name_found = True
            result.found_patterns.append("order_name")
            break

    # Calculate confidence
    score = 0
    patterns_count = len(result.found_patterns)
    for key in ["dimensions", "quantity", "color", "material", "order_name"]:
        if key in result.found_patterns:
            score += 1

    if valid_pipe_rows:
        result.confidence = 0.95
        result.is_order = True
        result.reason = "Обнаружен структурированный заказ: название|количество|единица."
    elif result.dimensions_found and score >= 2:
        result.confidence = min(0.95, 0.5 + score * 0.15)
        result.is_order = True
        result.reason = f"Обнаружены признаки заказа: {', '.join(result.found_patterns)}"
    elif result.dimensions_found and score == 1:
        result.confidence = 0.5
        result.is_order = True
        result.reason = "Возможный заказ (только размеры). Нужно уточнить."
    elif score >= 2:
        result.confidence = 0.4
        result.is_order = True
        result.reason = "Слабые признаки заказа. Нужно уточнение."
    elif result.is_correction:
        result.confidence = 0.8
        result.is_order = True
        result.reason = "Похоже на исправление заказа."
    elif result.is_confirmation:
        result.confidence = 0.9
        result.is_order = True
        result.reason = "Похоже на подтверждение."
    else:
        result.confidence = 0.1
        result.is_order = False
        result.reason = "Признаков заказа не обнаружено."

    return result
