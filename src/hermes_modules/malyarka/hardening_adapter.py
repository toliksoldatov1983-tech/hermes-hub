from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from hermes_clean import build_export_model, list_fixtures, validate_order_result


ALLOWED_PREVIEW_SOURCES = {"synthetic", "manual"}
BLOCKED_SOURCES = {"real_order", "archive", "imported", "google_drive", "unknown"}


@dataclass(frozen=True)
class HardeningStatus:
    compatibility_layer: str
    fixture_count: int
    validation_available: bool
    export_gate_available: bool
    allowed_preview_sources: tuple[str, ...]
    blocked_sources: tuple[str, ...]


def get_hardening_status() -> HardeningStatus:
    return HardeningStatus(
        compatibility_layer="hermes_clean",
        fixture_count=len(list_fixtures()),
        validation_available=True,
        export_gate_available=True,
        allowed_preview_sources=tuple(sorted(ALLOWED_PREVIEW_SOURCES)),
        blocked_sources=tuple(sorted(BLOCKED_SOURCES)),
    )


def validate_synthetic_order_result(order_result: dict[str, Any]) -> dict[str, Any]:
    return validate_order_result(order_result)


def build_safe_export_preview(
    order_result: dict[str, Any],
    *,
    source_type: str = "synthetic",
    strict: bool = False,
) -> dict[str, Any]:
    if source_type not in ALLOWED_PREVIEW_SOURCES:
        return {
            "export_rows": [],
            "export_blocked": True,
            "reason": f"source_type_blocked:{source_type}",
            "source_status": order_result.get("status", "unknown"),
            "source_type": source_type,
        }

    validation = validate_order_result(order_result)
    if validation["blocked"]:
        return {
            "export_rows": [],
            "export_blocked": True,
            "reason": validation["block_reason"] or "validation_failed",
            "source_status": order_result.get("status", "unknown"),
            "source_type": source_type,
            "validation": validation,
        }

    model = build_export_model(order_result, strict=strict)
    model["source_type"] = source_type
    model["validation"] = validation
    return model
