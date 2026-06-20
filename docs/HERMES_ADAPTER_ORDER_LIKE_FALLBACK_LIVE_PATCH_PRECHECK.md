# HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LIVE_PATCH_PRECHECK

Дата: 2026-06-20

## Approval phrase required

Future live patch requires:

```text
APPROVE_ORDER_LIKE_FALLBACK_LIVE_PATCH_ONCE
```

## Precheck checklist

Do not patch unless all are true:

- [ ] SSH access verified read-only.
- [ ] Live service state recorded.
- [ ] Autostart state recorded.
- [ ] Feature flag confirmed OFF.
- [ ] Production confirmed OFF.
- [ ] Phase 2 confirmed OFF.
- [ ] Local fix-candidate tests passed.
- [ ] Live `hermes_adapter.py` backup plan ready.
- [ ] Rollback plan ready.
- [ ] Patch scope limited to `hermes_adapter.py`.
- [ ] No `.env`, `config.py`, token, `os.environ` reads required.
- [ ] No DB/log/order reads required.

## Stop conditions

Stop before patch if:

- SSH is blocked;
- live file differs unexpectedly from snapshot and cannot be reviewed safely;
- backup cannot be created;
- feature flag is not OFF;
- production status is unclear;
- syntax check command would require secrets;
- rollback path is unclear.

