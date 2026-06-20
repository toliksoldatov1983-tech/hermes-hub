# Server Read-Only Stop Conditions

Date: 2026-06-17 | RED gate

Hermes MUST stop if:

| # | Condition |
|---|-----------|
| 1 | SSH needed but no RED approval |
| 2 | Need to read token/.env/config.py contents |
| 3 | Need to start/stop/restart live bot |
| 4 | Need to modify files |
| 5 | Need to read database/log/order contents |
| 6 | Need to launch polling/webhook |
| 7 | Need to do git operation |
| 8 | Need to execute patch |
| 9 | Need to read real orders |
| 10 | Doubt whether a file is safe to read |
| 11 | Encounter unknown file in secrets path |
| 12 | `config.py` found — STOP, DO NOT READ |

## Rule

When in doubt → STOP and ask. Better to stop early than read secrets.
