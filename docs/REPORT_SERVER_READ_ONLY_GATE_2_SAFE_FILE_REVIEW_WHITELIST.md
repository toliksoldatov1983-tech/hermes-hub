# REPORT — Server Read-Only Gate 2: Safe File Review

Date: 2026-06-17 | Status: ✅ COMPLETE

## Files Read (6/6)

| # | File | Lines | Role |
|---|------|-------|------|
| 1 | `malyarka_core/adapters/telegram.py` | ~120 | ⚡ MAIN ADAPTER |
| 2 | `malyarka_telegram/handlers.py` | ~200 | Message handlers |
| 3 | `malyarka_telegram/router.py` | ~250 | Mode router |
| 4 | `malyarka_telegram/intent.py` | ~220 | Intent classification |
| 5 | `malyarka_core/services/orders.py` | ~100 | Order service |
| 6 | `malyarka_core/exports/corel.py` | ~80 | Corel export |

## Key Finding: Adapter Already Exists

The server already has a fully functional adapter at `malyarka_core/adapters/telegram.py`:

| Function | Purpose |
|----------|---------|
| `build_order_preview_from_text` | Main entry: text → preview |
| `prepare_export_rows_from_text` | Text → Corel/Malyarka rows |
| `save_order_from_text` | Persist via SQLite connection |
| `build_disputed_lines_message` | Disputed items → Telegram text |
| `build_confirmed_lines_message` | Confirmed items → Telegram text |
| `build_order_summary_message` | Order summary → Telegram text |

## Adapter Boundary Confirmed

```text
Telegram → handlers.py → adapters/telegram.py → services/orders.py → parsing/validation
                ✅ already connected       ✅ service layer         ✅ core logic
```

## Hermes Adapter Hook Point

`malyarka_core/adapters/telegram.py` — `build_order_preview_from_text(text)`

Hermes local fake adapter maps directly to this function. Dry-run hook: wrap/override this function with Hermes safety checks.

## Safety

```
writes: 0 | token/.env/config: NOT read | DB/logs/orders: NOT read
live/polling/webhook: NOT touched | git/patch: NOT executed
```
