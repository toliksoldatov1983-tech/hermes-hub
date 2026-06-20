# Server Read-Only Gate Preplan

Date: 2026-06-17 | Gate: RED

## Preplan Only

NO SSH. NO server file read. NO secrets.

## What We Know

- Server: `/opt/malyarka-telegram-bot`
- Files: presence-only inventory exists
- config.py: EXISTS but NEVER read
- Token: NEVER read

## What We Need (if approved)

1. Safe read-only inventory update
2. No config.py/token/.env/os.environ
3. Explicit user approval for each file read
