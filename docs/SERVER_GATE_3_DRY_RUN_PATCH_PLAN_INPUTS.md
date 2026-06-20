# Server Gate 3 — Dry-Run Patch Plan Inputs

Date: 2026-06-17 | No code, no patch

## Target File

`/opt/malyarka-telegram-bot/malyarka_core/adapters/telegram.py`

## Insertion Point

Function: `build_order_preview_from_text(text)`

## What to Add (Hermes Layer)

```python
# BEFORE existing logic:
hermes_result = hermes_adapter.check(text)
if hermes_result.blocked:
    return {"blocked": True, "reason": hermes_result.block_reason}
if hermes_result.review_required:
    preview["review_required"] = True
# CONTINUE with existing logic...
```

## What NOT to Change

- `services/orders.py` — no changes
- `handlers.py` — already connected, no changes needed
- `router.py` — no changes
- `intent.py` — no changes
- Config files — NEVER touch

## Candidate Files

| File | Action |
|------|--------|
| `adapters/telegram.py` | ⚡ ADD Hermes hook |
| `hermes_adapter.py` (new) | ⚡ NEW file: Hermes safety layer |

## Forbidden Files

- config.py (any)
- .env
- orders.db
- Logs
- Token files
