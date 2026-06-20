# HERMES_ADAPTER_PHASE2_COMMAND_PLAN_ONLY

Дата: 2026-06-20

This document is documentation only. Commands are not executed by this plan.

## Future controlled sequence

1. Read-only precheck.
2. Verify service is running.
3. Verify autostart is disabled.
4. Verify Hermes adapter feature flag is OFF.
5. Verify production is OFF.
6. Verify rollback plan is ready.
7. After exact approval, controlled enable flag only for Phase 2 dry-run.
8. Controlled service restart only if technically required by the approved plan.
9. Run safe Telegram test.
10. Forced rollback: feature flag OFF.
11. Final status check.
12. Final report.

## Commands are not authorized now

Not authorized in this packet:

- changing the feature flag;
- `systemctl start`;
- `systemctl restart`;
- `systemctl stop`;
- `systemctl enable`;
- `systemctl disable`;
- production enable;
- Phase 2 launch.

## Approval phrase for future execution

```text
APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE
```

