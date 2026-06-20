# Server Gate 4 — Patch Plan Inputs

Date: 2026-06-17 | No code, no apply

## Candidate Files

| File | Action | New? |
|------|--------|------|
| `malyarka_core/adapters/hermes_adapter.py` | CREATE | ✅ new |
| `malyarka_core/adapters/telegram.py` | MODIFY | ❌ hook only |

## Required Backups (before Gate 4)

| File | Purpose |
|------|---------|
| `adapters/telegram.py` | Restore point |
| `handlers.py` | Verify no regressions |

## Required Prechecks

- [ ] SSH access working
- [ ] Live bot stopped (if needed for backup)
- [ ] `adapters/telegram.py` backed up to safe location
- [ ] feature flag tested as False before changes

## Stop Conditions (Gate 4)

- Need to read config.py / .env / token
- Need to modify handlers.py / router.py / orders.py
- Need to restart live bot without approval
- Need to apply patch without backup

## Expected Changes

1. Create `hermes_adapter.py` — new file, no deps
2. Add 3-line hook to `adapters/telegram.py` — after imports, before logic
3. Add `_HERMES_ADAPTER_ENABLED = False` flag
