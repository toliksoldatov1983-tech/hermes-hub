# HERMES_ADAPTER_PHASE2_PRECHECK_CHECKLIST

Дата: 2026-06-20

## Required precheck before future Phase 2 dry-run

- [ ] Sync layer is current.
- [ ] Service is running.
- [ ] Autostart is disabled.
- [ ] Feature flag is OFF before the dry-run.
- [ ] Adapter file is present.
- [ ] Telegram hook is present.
- [ ] SSH access is verified.
- [ ] Rollback plan is ready.
- [ ] Production is OFF.
- [ ] No real orders are used.
- [ ] No photos are used.
- [ ] No Vision/API is used.

## Current known values

```text
service running: yes
autostart disabled: yes
feature flag OFF: yes
adapter file present: yes
telegram hook present: yes
SSH access verified: yes
production OFF: yes
Phase 2 OFF: yes
```

## Stop conditions

Stop before any Phase 2 action if:

- SSH is not verified;
- feature flag cannot be confirmed OFF;
- service state is not understood;
- production is not confirmed OFF;
- rollback plan is not ready;
- any step requires reading secrets, DB, logs, or real orders.

