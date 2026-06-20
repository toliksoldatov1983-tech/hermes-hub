# Codex — Start Here When Available

Date: 2026-06-17

## Current Status

- 145/145 tests, 0 violations, 0 active agents
- Local chain: Sales→Malyarka→Corel verified
- Server Read-Only Gate 1: BLOCKED (SSH)
- First gate to run: `SERVER_READ_ONLY_GATE_1_VERIFY_ARCHITECTURE_ONLY_VIA_CODEX`

## Docs to Read First

1. `PROJECT_CURRENT_STATUS_COMPACT.md`
2. `SERVER_BLOCKED_STATUS_FINAL.md`
3. `SERVER_READ_ONLY_GATE_1_FAST_RETRY_PLAN.md`
4. `SERVER_READ_ONLY_APPROVAL_PROMPT.md`

## MUST NOT

- Read .env, config.py, token, orders.db, logs
- Start/stop live bot, polling, webhook
- Run systemctl, git, patch, apply
- Create production files
- Activate agents

## First Gate

```
SERVER_READ_ONLY_GATE_1_VERIFY_ARCHITECTURE_ONLY_VIA_CODEX
Target: /opt/malyarka-telegram-bot
Commands: pwd, ls, find, tree, head (whitelist only)
```
