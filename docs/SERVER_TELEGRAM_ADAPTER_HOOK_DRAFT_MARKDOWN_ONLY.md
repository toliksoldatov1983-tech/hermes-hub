# Server Telegram Adapter Hook — Draft (Markdown Only)

Date: 2026-06-17 | DO NOT modify telegram.py

## Proposed change in `malyarka_core/adapters/telegram.py`

### Add after imports, before functions:

```python
# === Hermes Adapter Feature Flag ===
_HERMES_ADAPTER_ENABLED = False  # off by default, no impact on existing flow
```

### Modify `build_order_preview_from_text`:

```python
def build_order_preview_from_text(text: str) -> dict[str, Any]:
    """Build a user-facing order preview from plain text."""

    # === HERMES ADAPTER HOOK ===
    if _HERMES_ADAPTER_ENABLED:
        try:
            from malyarka_core.adapters.hermes_adapter import check_hermes_safety
            hermes = check_hermes_safety(text)
            if hermes["fallback_required"]:
                pass  # fall through to original logic
            elif hermes["blocked"]:
                return {
                    "blocked": True,
                    "block_reason": hermes["block_reason"],
                    "confirmed_items": [],
                    "disputed_items": [],
                    "confirmed_count": 0,
                    "disputed_count": 0,
                    "total_quantity": 0,
                    "total_area_m2": 0.0,
                    "can_export": False,
                    "export_blocked_reason": hermes["block_reason"],
                }
        except Exception:
            pass  # safe failure: fall through to original logic

    # === EXISTING LOGIC (unchanged) ===
    order = build_order_from_text(text)
    confirmed_items = [_confirmed_item_to_preview(item) for item in order.items]
    disputed_items = [_disputed_item_to_preview(item) for item in order.disputed_items]
    export_blocked_reason = _get_export_blocked_reason(order)

    return {
        "confirmed_items": confirmed_items,
        "disputed_items": disputed_items,
        "confirmed_count": len(confirmed_items),
        "disputed_count": len(disputed_items),
        "total_quantity": calculate_total_quantity(order.items),
        "total_area_m2": calculate_total_area_m2(order.items),
        "can_export": export_blocked_reason == "",
        "export_blocked_reason": export_blocked_reason,
    }
```

## Safety

- Flag OFF → original path, zero impact
- Exception → fallback to original path
- Hook is try/except wrapped
- No side effects in hook call
- Handlers/router/orders unchanged
