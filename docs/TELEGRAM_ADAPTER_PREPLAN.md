# Telegram Adapter Preplan

Date: 2026-06-17 | Gate: RED/YELLOW

## Preplan Only

This is a markdown preplan. NO Telegram API. NO token. NO live.

## Architecture

```text
Agents → Telegram Safe Adapter (#4) → Telegram API → Client
            ↑ accepted, not active
```

## Requirements

1. Token — NEVER read without user
2. Polling/webhook — NEVER touch
3. Existing bot — NEVER modify
4. Send messages — ONLY after live approval

## Next Step

Yellow approval for adapter planning only (no code, no API).
