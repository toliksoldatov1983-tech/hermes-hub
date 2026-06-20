# REPORT — Server Adapter Gate 6: Backup & Staging Apply

Date: 2026-06-18 | Status: ✅ COMPLETE

## SSH: yes (root@178.104.95.187)

## Backup

| Item | Detail |
|------|--------|
| Directory | `/opt/malyarka-telegram-bot/_hermes_backups/20260618_200023/` |
| File backed up | `telegram.py` (original) |

## Files Written

| File | Action |
|------|--------|
| `malyarka_core/adapters/hermes_adapter.py` | ✅ CREATED (1804 bytes) |
| `malyarka_core/adapters/telegram.py` | ✅ MODIFIED (hook + flag) |

## Feature Flag

```python
_HERMES_ADAPTER_ENABLED = False  # off by default
```

## Postcheck

| Check | Result |
|-------|--------|
| hermes_adapter.py syntax | ✅ OK |
| telegram.py syntax | ✅ OK |
| Feature flag | ✅ OFF |
| Backup exists | ✅ yes |

## Rollback Available

```bash
cp _hermes_backups/20260618_200023/telegram.py malyarka_core/adapters/telegram.py
```

## Safety

```
live bot: NOT restarted | systemctl: NOT used | git: NOT used
token/.env/config: NOT read | DB/logs/orders: NOT read
handlers/router/orders: NOT touched
```
