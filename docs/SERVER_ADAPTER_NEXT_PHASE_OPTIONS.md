# Server Adapter — Next Phase Options

Date: 2026-06-18

| Option | Description | Gate |
|--------|-------------|------|
| A | Stop, keep adapter OFF | GREEN |
| B | Controlled enable plan | YELLOW |
| C | Monitoring/logging plan | YELLOW |
| D | Production rollout | RED |
| E | Rollback plan verification | YELLOW |

## A — Safe Stop

Keep flag OFF. Bot runs with existing adapter path. Hermes adapter installed but inactive.

## B — Controlled Enable

Set flag ON, restart bot. Monitor for 1-2 hours. Requires limited RED approval.

## C — Monitoring

Add safe logging to hermes_adapter.py (block count, pass count). No secrets in logs.

## D — Production Rollout

Full enable + monitoring + production orders. RED gate only. Separate approval.

## E — Rollback

Verify backup restoration works. Restore original telegram.py, remove hermes_adapter.py.
