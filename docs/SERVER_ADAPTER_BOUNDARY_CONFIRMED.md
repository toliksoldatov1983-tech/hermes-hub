# Server Adapter Boundary Confirmed

Date: 2026-06-17

## Boundary

```
INPUT: Telegram message text (str)
    → handlers.py: validate, classify intent, check dangerous words
    → adapters/telegram.py: build preview, calculate, validate export
    → services/orders.py: coordinate parsing + exports
OUTPUT: Order preview dict + Corel/Malyarka rows
```

## Hermes Hook Point

`adapters/telegram.py::build_order_preview_from_text(text)`

This is the natural hook for:
1. Safety validation (Hermes adapter checks)
2. Dry-run mode (feature flag gated)
3. Block dangerous/production actions
4. Route to Sales→Malyarka→Corel pipeline

## Already Protected

| Protection | Where |
|-----------|-------|
| Dangerous words block | handlers.py (git, token, .env, delete, etc.) |
| Owner-only modes | router.py (engineer, ideas, admin) |
| Intent blocking | intent.py (blocked pattern detection) |
| Export validation | validation.py (order export checks) |
| No aiogram import | handlers.py, router.py (pure Python) |
| No API calls | adapters/telegram.py (no network) |
