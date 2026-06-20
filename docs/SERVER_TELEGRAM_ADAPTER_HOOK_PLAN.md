# Server Telegram Adapter Hook Plan

Date: 2026-06-17 | No code

## Target File

```
/opt/malyarka-telegram-bot/malyarka_core/adapters/telegram.py
```

## Hook Location

Function: `build_order_preview_from_text(text: str)`

## Before/After

```python
def build_order_preview_from_text(text: str):
    # === HERMES ADAPTER HOOK ===
    if _HERMES_ADAPTER_ENABLED:
        from malyarka_core.adapters.hermes_adapter import check_hermes_safety
        hermes = check_hermes_safety(text)
        if hermes["blocked"]:
            return {"blocked": True, "reason": hermes["block_reason"]}
    
    # === EXISTING LOGIC (unchanged) ===
    order = build_order_from_text(text)
    ...
```

## Safety

- Feature flag off by default → no impact on existing flow
- Existing functions NOT modified
- `build_order_preview_from_text` remains the main path
- One flag disables Hermes: `_HERMES_ADAPTER_ENABLED = False`

## Feature Flag

```python
_HERMES_ADAPTER_ENABLED = False  # off by default
```
