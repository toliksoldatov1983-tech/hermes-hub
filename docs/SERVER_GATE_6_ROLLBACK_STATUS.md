# Gate 6 — Rollback Status

Date: 2026-06-18 | Status: NOT ROLLED BACK (postcheck passed)

## Rollback Available

Backup path: `_hermes_backups/20260618_200023/telegram.py`

## Rollback Command

```bash
cd /opt/malyarka-telegram-bot
cp _hermes_backups/20260618_200023/telegram.py malyarka_core/adapters/telegram.py
rm malyarka_core/adapters/hermes_adapter.py
```

## Status

Postcheck passed → rollback NOT executed. Backup retained for safety.
