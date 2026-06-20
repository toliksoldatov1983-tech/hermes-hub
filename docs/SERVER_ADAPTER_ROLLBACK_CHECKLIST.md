# Server Adapter Rollback Checklist

Date: 2026-06-17 | No patch

## Files to Backup (future)

| File | Purpose |
|------|---------|
| `handlers.py` | Message processing logic |
| `router.py` | Routing rules |
| `app.py` | Bot entry point |

## Before Adapter Insertion

- [ ] Backup all target files
- [ ] Verify backups are restorable
- [ ] Document current handler flow
- [ ] Note original imports

## Feature Flag

```python
HERMES_ADAPTER_ENABLED = False  # off by default
```

To disable: set to `False` → adapter bypassed → original path.

## Rollback Steps

1. Set `HERMES_ADAPTER_ENABLED = False`
2. Restart bot (only if needed)
3. Verify original behavior restored
4. If fails: restore from backup

## NOT Included

- No patch applied yet
- No code written
- No server changes
