# Server Adapter Future Backup Plan

Date: 2026-06-17 | No backup created

## Files to Backup (future)

| File | Reason |
|------|--------|
| `malyarka_core/adapters/telegram.py` | Will be modified (hook) |

## Backup Convention

```
adapters/telegram.py.bak.20260617
```

## Verification

```bash
diff adapters/telegram.py adapters/telegram.py.bak.20260617
md5sum adapters/telegram.py adapters/telegram.py.bak.20260617
```

## Storage

Same directory as original, or `/opt/malyarka-telegram-bot/backups/`.

## Status

Backups NOT created. Requires separate YELLOW approval.
