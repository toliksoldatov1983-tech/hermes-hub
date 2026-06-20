# Gate 6 — Applied Files Report

Date: 2026-06-18

## New File

```
malyarka_core/adapters/hermes_adapter.py
```
- 1804 bytes
- `check_hermes_safety(text)` function
- No API calls, no secrets, no DB

## Modified File

```
malyarka_core/adapters/telegram.py
```
- Added: `_HERMES_ADAPTER_ENABLED = False` (line 22)
- Added: Hermes adapter hook (lines 28-48) in `build_order_preview_from_text`
- Feature flag OFF → existing behavior unchanged
- Exception → safe fallback to original path

## Source

Code from `SERVER_HERMES_ADAPTER_DRAFT_CODE_MARKDOWN_ONLY.md` and `SERVER_TELEGRAM_ADAPTER_HOOK_DRAFT_MARKDOWN_ONLY.md` (Gate 5).
