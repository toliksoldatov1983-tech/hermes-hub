# Server Adapter Rollback Execution Plan (No Apply)

Date: 2026-06-17 | Plan only

## Steps

1. Set `_HERMES_ADAPTER_ENABLED = False` in `adapters/telegram.py`
2. Restore `adapters/telegram.py` from backup if needed
3. Remove `hermes_adapter.py` if created
4. Verify: `build_order_preview_from_text` works as original
5. STOP if backup missing or corrupted

## Commands (future, NOT now)

```bash
cp adapters/telegram.py.bak.YYYYMMDD adapters/telegram.py
rm adapters/hermes_adapter.py
```

## No Live Restart

Rollback is code-only. Bot restart requires separate RED approval.
