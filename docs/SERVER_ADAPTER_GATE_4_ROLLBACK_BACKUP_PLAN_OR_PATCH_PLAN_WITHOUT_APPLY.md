# Server Adapter Gate 4 — Rollback/Backup/Patch Plan (No Apply)

Date: 2026-06-17 | Status: PLAN ONLY

## Purpose

Prepare exact plan for future server dry-run patch without executing anything.

## Affected Files (future)

| File | Action |
|------|--------|
| `malyarka_core/adapters/hermes_adapter.py` | CREATE (new) |
| `malyarka_core/adapters/telegram.py` | MODIFY (hook only) |

## NOT Affected

| File | Reason |
|------|--------|
| `handlers.py` | No changes needed |
| `router.py` | No changes needed |
| `orders.py` | No changes needed |
| `config.py` | ⛔ NEVER touch |
| `.env` | ⛔ NEVER touch |
| DB/logs/orders | ⛔ NEVER touch |

## Backup Strategy

| Original | Backup Name |
|----------|-------------|
| `adapters/telegram.py` | `adapters/telegram.py.bak.YYYYMMDD` |

## Rollback Strategy

1. Restore `adapters/telegram.py` from backup
2. Delete `hermes_adapter.py` if created
3. Set `_HERMES_ADAPTER_ENABLED = False`
4. Verify original preview path works

## Approval Gates

| Gate | Approval |
|------|----------|
| Create backup on server | YELLOW |
| Create hermes_adapter.py | YELLOW |
| Add hook to telegram.py | YELLOW |
| Apply patch | RED |
| Restart bot | RED |
