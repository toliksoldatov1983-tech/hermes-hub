# Server Adapter Gate 5 — Staging Patch Plan (No Apply)

Date: 2026-06-17 | Status: PLAN ONLY

## Purpose

Prepare staging patch plan and markdown-only code drafts. No real files created.

## Affected Files (future)

| File | Action |
|------|--------|
| `hermes_adapter.py` | CREATE (draft in markdown) |
| `adapters/telegram.py` | MODIFY hook (draft in markdown) |

## Apply Sequence (future)

1. Create backup of `adapters/telegram.py`
2. Write `hermes_adapter.py` to server
3. Add hook to `adapters/telegram.py`
4. Verify: feature flag OFF, dry_run only
5. Postcheck all 12 items
6. Do NOT restart bot

## Mandatory Approvals

| Step | Approval |
|------|----------|
| Draft code locally | GREEN ✅ (this gate) |
| Create backup on server | YELLOW |
| Write files to server | RED |
| Apply patch | RED |
| Restart bot | RED (separate) |
