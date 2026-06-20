# Server Gate 7 — Focused Tests Inputs

Date: 2026-06-18 | No live restart

## Goal

Run focused tests on server to verify Hermes adapter integration without restarting bot.

## Tests

| # | Test | Status |
|---|------|--------|
| 1 | `hermes_adapter.py` imports OK | To verify |
| 2 | `check_hermes_safety("")` → blocked | To verify |
| 3 | `check_hermes_safety("фасады МДФ")` → not blocked | To verify |
| 4 | `check_hermes_safety("production")` → blocked | To verify |
| 5 | `check_hermes_safety("BOT_TOKEN=***")` → blocked | To verify |
| 6 | Feature flag OFF → original path | To verify |

## Restrictions

- No live bot restart
- No systemctl
- No git
- No config.py/token/.env reads
