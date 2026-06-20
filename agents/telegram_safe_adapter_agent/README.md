# Telegram Safe Adapter Agent

Status: `accepted` (not active)
GATE: TELEGRAM_SAFE_ADAPTER_GATE_1

## What

Fake Telegram adapter for local offline testing.
Accepts fake Telegram-style events, validates safety, routes to agent chain.

## Files

- `src/fake_telegram_adapter.py` — fake adapter module
- `tests/test_fake_telegram_adapter.py` — 12 tests
- `ADAPTER_CONTRACT.md` — input/output contract
- `SCENARIOS.md` — test scenarios

## Safety

- No Telegram/aiogram import
- No token/env/config access
- dry_run=true, production_ready=false
- No server/network/API calls
