# Server — Next 3 Gates After Access Restored

Date: 2026-06-17

## Gate 1: Architecture Verification (retry)

**Gate:** RED
**Task:** read-only architecture check of `/opt/malyarka-telegram-bot`
**Prerequisite:** SSH restored

## Gate 2: Safe File Review Whitelist

**Gate:** RED/YELLOW
**Task:** read headers of safe files (router.py, handlers.py, app.py)
**Prerequisite:** Gate 1 passed
**Forbidden:** .env, config.py, token, DB, logs

## Gate 3: Dry-Run Patch Plan (no code)

**Gate:** YELLOW
**Task:** markdown-only plan for adapter insertion
**Prerequisite:** Gate 2 passed
**Output:** patch plan, NOT patch file
