# Server Adapter Gate 3 — Dry-Run Patch Plan (No Code)

Date: 2026-06-17 | Status: PLAN ONLY

## Proposed New File

```
/opt/malyarka-telegram-bot/malyarka_core/adapters/hermes_adapter.py
```

## Proposed Hook

```
malyarka_core/adapters/telegram.py::build_order_preview_from_text
```

## Design

```python
# hermes_adapter.py — NEW file
def check_hermes_safety(text: str) -> dict:
    """Return safety check result. Never calls API, never touches secrets."""
    return {
        "blocked": False,
        "block_reason": None,
        "review_required": False,
        "dry_run": True,
        "production_ready": False,
    }
```

```python
# adapters/telegram.py — HOOK INSERTION
# BEFORE existing logic:
if _HERMES_ADAPTER_ENABLED:
    hermes = check_hermes_safety(text)
    if hermes["blocked"]:
        return {"blocked": True, "reason": hermes["block_reason"]}
```

## Feature Flags

| Flag | Default | Purpose |
|------|---------|---------|
| `_HERMES_ADAPTER_ENABLED` | False | Master switch |
| `_HERMES_DRY_RUN` | True | Always true initially |

## Invariants

| Rule | Value |
|------|-------|
| production_ready | always False |
| dry_run | always True |
| No Telegram API | never |
| No server writes | never |
| No secrets access | never |
