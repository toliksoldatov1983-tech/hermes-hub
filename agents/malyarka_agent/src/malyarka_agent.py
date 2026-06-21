"""
Malyarka Agent — offline Python module.

BUNDLE: MALYARKA_AGENT_OFFLINE_PYTHON_MODULE
Status: accepted (not active)

Accepts structured Intake Cards from Sales Intake Agent
and produces preliminary order results.
Never: counts final price, invents sizes/materials/colors,
       touches server/secrets/real orders.
"""

from __future__ import annotations

from typing import Any, Dict, List

# ---------------------------------------------------------------------------
# 1. analyze_intake_card(card) -> dict
# ---------------------------------------------------------------------------


def analyze_intake_card(card: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze a structured intake card and return analysis."""
    items = card.get("items", [])
    material_info = card.get("material", {})
    flags = card.get("flags", {})

    return {
        "item_count": len(items),
        "has_sizes": bool(items),
        "has_material": material_info.get("raw") is not None,
        "material_confirmed": material_info.get("confirmed", True),
        "missing_fields": detect_missing_fields(card),
        "blocking_flags": detect_blocking_flags(card),
    }


# ---------------------------------------------------------------------------
# 2. build_preliminary_result(card) -> dict
# ---------------------------------------------------------------------------


def build_preliminary_result(card: Dict[str, Any]) -> Dict[str, Any]:
    """Build a preliminary order result from an intake card."""
    items = card.get("items", [])
    flags = card.get("flags", {})

    # Split confirmed / disputed
    split = split_confirmed_and_disputed(card)
    confirmed = split["confirmed_rows"]
    disputed = split["disputed_rows"]

    # Calculate area (confirmed only)
    total_area = sum(
        (r.get("height_mm", 0) * r.get("width_mm", 0) * r.get("quantity", 1))
        / 1_000_000
        for r in confirmed
    )

    # Detect missing fields
    missing = detect_missing_fields(card)
    blocking = detect_blocking_flags(card)

    # Determine status
    status_info = determine_order_status(card)

    # Build dispute reasons
    dispute_reasons = []
    for row in disputed:
        reason = row.get("dispute_reason", "unconfirmed_data")
        dispute_reasons.append(f"{reason}: {row.get('material', '?')} {row.get('color', '?')}")

    result = {
        "intake_id": card.get("intake_id", ""),
        "status": status_info["status"],
        "confirmed_rows": [
            {
                "height_mm": r.get("height_mm"),
                "width_mm": r.get("width_mm"),
                "quantity": r.get("quantity", 1),
                "material": r.get("material", ""),
                "color": r.get("color", ""),
                "finish": r.get("finish", ""),
                "area_m2": round(
                    (r.get("height_mm", 0) * r.get("width_mm", 0) * r.get("quantity", 1))
                    / 1_000_000,
                    4,
                ),
            }
            for r in confirmed
        ],
        "disputed_rows": [
            {
                "height_mm": r.get("height_mm"),
                "width_mm": r.get("width_mm"),
                "quantity": r.get("quantity", 1),
                "material": r.get("material", ""),
                "color": r.get("color", ""),
                "dispute_reason": r.get("dispute_reason", "unconfirmed_data"),
            }
            for r in disputed
        ],
        "total_area_m2": round(total_area, 4),
        "export_blocked": len(disputed) > 0 or len(blocking) > 0,
        "dispute_reasons": dispute_reasons,
        "missing_fields": missing,
        "manager_review_required": flags.get("manager_review_required", False)
        or flags.get("discount_request", False)
        or flags.get("technical_advice_requested", False),
        "flags": {
            "discount_request": flags.get("discount_request", False),
            "technical_advice_requested": flags.get("technical_advice_requested", False),
            "material_question": flags.get("material_question", False),
            "manager_review_required": flags.get("manager_review_required", False),
        },
        "ready_for_human_review": (
            status_info["status"] == "ready_for_human_review"
        ),
        "short_summary": _build_summary(confirmed, disputed, total_area),
        "not_final_order": True,
    }

    return result


# ---------------------------------------------------------------------------
# 3. split_confirmed_and_disputed(card) -> dict
# ---------------------------------------------------------------------------


def split_confirmed_and_disputed(card: Dict[str, Any]) -> Dict[str, Any]:
    """Split items into confirmed_rows and disputed_rows."""
    items = card.get("items", [])
    flags = card.get("flags", {})

    confirmed: List[Dict[str, Any]] = []
    disputed: List[Dict[str, Any]] = []

    for item in items:
        reasons: List[str] = []

        # Check material confirmation
        if not item.get("material"):
            reasons.append("missing_material")
        elif not item.get("material_confirmed", True):
            reasons.append("material_ambiguous")

        # Check blocking flags
        if flags.get("discount_request"):
            reasons.append("discount_request_pending")
        if flags.get("technical_advice_requested"):
            reasons.append("technical_advice_pending")
        if flags.get("manager_review_required") and not reasons:
            reasons.append("manager_review_required")

        # Check sizes
        if not item.get("height_mm") or not item.get("width_mm"):
            reasons.append("incomplete_sizes")

        # Check color
        if not item.get("color"):
            reasons.append("missing_color")

        if reasons:
            disputed.append({
                **item,
                "dispute_reason": reasons[0],
                "all_reasons": reasons,
            })
        else:
            confirmed.append(dict(item))

    return {
        "confirmed_rows": confirmed,
        "disputed_rows": disputed,
    }


# ---------------------------------------------------------------------------
# 4. detect_missing_fields(card) -> list[str]
# ---------------------------------------------------------------------------


def detect_missing_fields(card: Dict[str, Any]) -> List[str]:
    """Detect missing fields in intake card."""
    missing: List[str] = []
    items = card.get("items", [])
    material_info = card.get("material", {})

    if not items:
        missing.append("items")
        return missing

    for i, item in enumerate(items):
        if not item.get("height_mm"):
            missing.append(f"item_{i}_height_mm")
        if not item.get("width_mm"):
            missing.append(f"item_{i}_width_mm")
        if not item.get("material"):
            missing.append(f"item_{i}_material")
        if not item.get("color"):
            missing.append(f"item_{i}_color")

    if not material_info.get("raw"):
        missing.append("material_raw")
    if not material_info.get("confirmed", True):
        missing.append("material_confirmation")

    return missing


# ---------------------------------------------------------------------------
# 5. detect_blocking_flags(card) -> list[str]
# ---------------------------------------------------------------------------


def detect_blocking_flags(card: Dict[str, Any]) -> List[str]:
    """Detect blocking flags that prevent finalization."""
    flags = card.get("flags", {})
    blocking: List[str] = []

    if flags.get("discount_request"):
        blocking.append("discount_request")
    if flags.get("technical_advice_requested"):
        blocking.append("technical_advice_requested")
    if flags.get("manager_review_required"):
        blocking.append("manager_review_required")
    if flags.get("material_question"):
        blocking.append("material_question")

    return blocking


# ---------------------------------------------------------------------------
# 6. determine_order_status(result) -> dict
# ---------------------------------------------------------------------------


def determine_order_status(card: Dict[str, Any]) -> Dict[str, Any]:
    """Determine the status of an order based on its intake card."""
    items = card.get("items", [])
    flags = card.get("flags", {})
    material_info = card.get("material", {})

    # No items → needs clarification
    if not items:
        return {"status": "needs_clarification", "reason": "no_items"}

    # Check each item for completeness
    for item in items:
        if not item.get("height_mm") or not item.get("width_mm"):
            return {"status": "needs_clarification", "reason": "incomplete_sizes"}
        if not item.get("material"):
            return {"status": "needs_clarification", "reason": "missing_material"}
        if not item.get("color"):
            return {"status": "needs_clarification", "reason": "missing_color"}

    # Check material confirmation
    if not material_info.get("confirmed", True):
        return {"status": "blocked_disputed_data", "reason": "material_not_confirmed"}

    for item in items:
        if not item.get("material_confirmed", True):
            return {"status": "blocked_disputed_data", "reason": "material_not_confirmed"}

    # Check blocking flags
    if flags.get("discount_request"):
        return {"status": "blocked_disputed_data", "reason": "discount_request"}
    if flags.get("technical_advice_requested"):
        return {"status": "blocked_disputed_data", "reason": "technical_advice"}
    if flags.get("manager_review_required"):
        return {"status": "blocked_disputed_data", "reason": "manager_review"}

    # All clear → preliminary result, ready for human review
    return {"status": "ready_for_human_review", "reason": "all_checks_passed"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _build_summary(confirmed: list, disputed: list, area: float) -> str:
    """Build a short human-readable summary."""
    parts = []
    if confirmed:
        parts.append(f"{len(confirmed)} confirmed ({area} м²)")
    if disputed:
        parts.append(f"{len(disputed)} disputed")
    if not parts:
        return "нет данных"
    return ", ".join(parts)
