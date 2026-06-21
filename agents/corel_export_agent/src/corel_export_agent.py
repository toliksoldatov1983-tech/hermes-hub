"""
Corel Export Agent — offline Python module.

BUNDLE: COREL_EXPORT_AGENT_OFFLINE_PYTHON_MODULE
Status: accepted (not active)

Accepts preliminary order results from Malyarka Agent
and produces export contracts for future Corel/Excel layer.
Never: launches Corel, creates real files, counts prices,
       touches server/secrets/real orders.
"""

from __future__ import annotations

from typing import Any, Dict, List


# ---------------------------------------------------------------------------
# 1. validate_preliminary_result(result) -> dict
# ---------------------------------------------------------------------------


def validate_preliminary_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Validate that the input is a proper preliminary result."""
    issues: List[str] = []

    if not isinstance(result, dict):
        return {"valid": False, "issues": ["not_a_dict"]}

    if not result.get("confirmed_rows") and not result.get("disputed_rows"):
        if not result.get("items"):
            issues.append("no_data")

    if result.get("not_final_order") is not True:
        issues.append("not_final_order_missing_or_false")

    return {"valid": len(issues) == 0, "issues": issues}


# ---------------------------------------------------------------------------
# 2. build_export_contract(result) -> dict
# ---------------------------------------------------------------------------


def build_export_contract(result: Dict[str, Any]) -> Dict[str, Any]:
    """Build an export contract from a preliminary result."""
    confirmed = result.get("confirmed_rows", [])
    disputed = result.get("disputed_rows", [])
    export_blocked = result.get("export_blocked", False)
    flags = result.get("flags", {})
    manager_review = result.get("manager_review_required", False)

    # Detect blockers
    blockers = detect_export_blockers(result)

    # Extract Corel rows (only confirmed)
    corel_rows = extract_corel_rows(result) if not blockers else []

    # Determine export status
    status_info = determine_export_status(result)

    contract = {
        "source": "malyarka_agent",
        "target": "corel_export_agent",
        "status": status_info["status"],
        "ready_for_corel": len(blockers) == 0 and len(corel_rows) > 0,
        "confirmed_count": len(confirmed),
        "disputed_count": len(disputed),
        "export_blocked": export_blocked,
        "export_blockers": blockers,
        "corel_rows": corel_rows,
        "total_area_m2": result.get("total_area_m2", 0),
        "manager_review_required": manager_review,
        "flags": {
            "discount_request": flags.get("discount_request", False),
            "technical_advice_requested": flags.get("technical_advice_requested", False),
            "manager_review_required": flags.get("manager_review_required", False),
        },
        "not_final_export": True,
        "preview": build_corel_preview({"corel_rows": corel_rows, "status": status_info["status"]}),
    }

    return contract


# ---------------------------------------------------------------------------
# 3. extract_corel_rows(result) -> list[dict]
# ---------------------------------------------------------------------------


def extract_corel_rows(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract Corel-ready rows from confirmed rows only.

    Export order: height_mm, width_mm, quantity.
    """
    confirmed = result.get("confirmed_rows", [])
    rows: List[Dict[str, Any]] = []

    for i, row in enumerate(confirmed):
        h = row.get("height_mm")
        w = row.get("width_mm")
        q = row.get("quantity", 1)

        if not h or not w or not q:
            continue

        rows.append({
            "index": i + 1,
            "height_mm": h,
            "width_mm": w,
            "quantity": q,
            "area_m2": round((h * w * q) / 1_000_000, 4),
            "material": row.get("material", ""),
            "color": row.get("color", ""),
            "finish": row.get("finish", ""),
        })

    return rows


# ---------------------------------------------------------------------------
# 4. detect_export_blockers(result) -> list[str]
# ---------------------------------------------------------------------------


def detect_export_blockers(result: Dict[str, Any]) -> List[str]:
    """Detect conditions that block export."""
    blockers: List[str] = []

    if result.get("export_blocked", False):
        blockers.append("export_blocked_flag")

    if result.get("disputed_rows"):
        blockers.append("disputed_rows_present")

    if result.get("manager_review_required", False):
        blockers.append("manager_review_required")

    flags = result.get("flags", {})
    if flags.get("discount_request"):
        blockers.append("discount_request")
    if flags.get("technical_advice_requested"):
        blockers.append("technical_advice_requested")

    confirmed = result.get("confirmed_rows", [])
    if not confirmed:
        blockers.append("no_confirmed_rows")

    for row in confirmed:
        if not row.get("height_mm") or not row.get("width_mm"):
            blockers.append("incomplete_dimensions")
            break
        if not row.get("quantity"):
            blockers.append("missing_quantity")
            break

    if result.get("not_final_order") is not True:
        blockers.append("not_final_order_invalid")

    return blockers


# ---------------------------------------------------------------------------
# 5. determine_export_status(contract) -> dict
# ---------------------------------------------------------------------------


def determine_export_status(result: Dict[str, Any]) -> Dict[str, Any]:
    """Determine export readiness."""
    blockers = detect_export_blockers(result)
    confirmed = result.get("confirmed_rows", [])

    if not confirmed:
        return {"status": "blocked", "reason": "no_confirmed_rows", "can_export": False}

    if blockers:
        return {"status": "blocked", "reason": blockers[0], "can_export": False, "all_blockers": blockers}

    return {"status": "ready", "reason": "all_checks_passed", "can_export": True}


# ---------------------------------------------------------------------------
# 6. build_corel_preview(contract) -> str
# ---------------------------------------------------------------------------


def build_corel_preview(contract: Dict[str, Any]) -> str:
    """Build a text preview of the export contract."""
    rows = contract.get("corel_rows", [])
    status = contract.get("status", "blocked")

    if not rows:
        return "[export blocked — no confirmed rows]"

    lines = [f"Corel Export Preview ({len(rows)} rows)"]
    lines.append("-" * 40)

    for row in rows:
        h = row.get("height_mm", "?")
        w = row.get("width_mm", "?")
        q = row.get("quantity", 1)
        mat = row.get("material", "")
        col = row.get("color", "")
        fin = row.get("finish", "")
        area = row.get("area_m2", 0)

        line = f"  {row['index']}. {h}×{w} mm, ×{q}"
        if mat:
            line += f", {mat}"
        if col:
            line += f", {col}"
        if fin:
            line += f", {fin}"
        line += f" ({area} m²)"
        lines.append(line)

    lines.append("-" * 40)
    lines.append(f"Status: {status}")
    lines.append("not_final_export: true")

    return "\n".join(lines)
