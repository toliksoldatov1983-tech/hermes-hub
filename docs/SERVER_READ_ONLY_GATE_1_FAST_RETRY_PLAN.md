# Server Read-Only Gate 1 — Fast Retry Plan

Date: 2026-06-17 | After SSH restored

## Immediate Commands

```bash
cd /opt/malyarka-telegram-bot
pwd
ls -la
find . -maxdepth 2 -type f | sort
find . -maxdepth 2 -type d | sort
```

## Verify Architecture

```bash
head -5 app.py router.py handlers.py 2>/dev/null
head -5 requirements.txt pyproject.toml 2>/dev/null
ls -la malyarka_core/ malyarka_core/services/ 2>/dev/null
```

## Find Adapter Point

```bash
grep -l "Dispatcher\|router\|handler" *.py 2>/dev/null | head -10
```

## STOP If

- File contains token/env/config → do NOT read
- Need to read .env / config.py contents
- Need to read DB / logs / orders

## NEVER

- .env, config.py contents, token, orders.db, logs
