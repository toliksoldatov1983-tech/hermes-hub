# Server Gate 6 — Backup & Staging Apply Inputs

Date: 2026-06-17 | Approval: RED

## Backup Commands (future)

```bash
cd /opt/malyarka-telegram-bot
cp malyarka_core/adapters/telegram.py malyarka_core/adapters/telegram.py.bak.$(date +%Y%m%d)
```

## Files to Apply

| File | Action | Content |
|------|--------|---------|
| `malyarka_core/adapters/hermes_adapter.py` | CREATE | From Gate 5 draft |
| `malyarka_core/adapters/telegram.py` | MODIFY | Hook from Gate 5 draft |

## Prechecks Before Write

- [ ] Backup created and verified
- [ ] SSH access confirmed
- [ ] Feature flag in draft is False
- [ ] No config.py/token/.env access

## Postchecks After Write

- [ ] `python -c "from malyarka_core.adapters.hermes_adapter import check_hermes_safety"` works
- [ ] Original preview path still works
- [ ] Flag OFF → no Hermes in output
- [ ] No bot restart

## RED Approval Required

- Creating backup on server
- Writing any file to server
- Applying patch
