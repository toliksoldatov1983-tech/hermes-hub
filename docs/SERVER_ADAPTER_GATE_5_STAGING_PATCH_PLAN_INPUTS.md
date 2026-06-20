# Server Adapter Gate 5 — Staging Patch Plan Inputs

Date: 2026-06-17 | No apply

## What Gate 5 May Produce

- Python code for `hermes_adapter.py` (locally drafted)
- Exact hook diff for `adapters/telegram.py` (locally drafted)
- Dry-run test scenarios

## What Gate 5 Must NOT Do

- Apply any patch to server
- Write files to server
- Restart bot
- Enable feature flag to True
- Touch config.py, .env, DB

## Approval Needed Before Any Server Write

| Action | Approval |
|--------|----------|
| Draft Python code locally | GREEN |
| Create backup on server | YELLOW |
| Apply patch to server | RED |
| Restart bot | RED |

## Temp Root Key

Keep until all read-only gates complete. Remove only after separate approval.
