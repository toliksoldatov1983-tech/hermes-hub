# Codex Handoff Prompt — Ready

Date: 2026-06-17 | DO NOT execute

```text
CODEX TASK: SERVER_READ_ONLY_GATE_1_VERIFY_ARCHITECTURE_ONLY

Context: Hermes Hub project, local MVP complete (145/145 tests).
Server: /opt/malyarka-telegram-bot, SSH to ubuntu@49.13.76.163

GOAL: Read-only architecture verification. NO changes.

ALLOWED: pwd, ls, find (maxdepth 3), tree, head (whitelist)
FORBIDDEN: .env, config.py, token, orders.db, logs, systemctl, git, patch

CHECK:
- app.py, router.py, handlers.py exist?
- malyarka_core/services/orders.py exist?
- Where is Dispatcher created?
- Where is likely adapter insertion point?

STOP if file may contain secrets/token/config.
```
