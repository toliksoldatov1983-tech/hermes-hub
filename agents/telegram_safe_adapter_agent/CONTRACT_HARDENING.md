# Contract Hardening

Date: 2026-06-17 | Gate 3

## Invariants

| # | Rule | Value |
|---|------|-------|
| 1 | adapter_mode | always "fake" |
| 2 | dry_run | always true |
| 3 | production_ready | always false |
| 4 | telegram_api_called | always false |
| 5 | server_called | always false |
| 6 | side_effects | always [] |

## Forbidden

| # | Action |
|---|--------|
| 1 | Read token / .env / config.py / os.environ |
| 2 | Import aiogram / telegram live modules |
| 3 | Launch polling / webhook / server / API / subprocess |
| 4 | Create production export |
| 5 | Send messages to real clients |

## Allowed

- Process fake Telegram events
- Validate and classify input
- Route safe messages to Sales Agent
- Block unsafe/empty/disputed input
- Return deterministic fake adapter result
