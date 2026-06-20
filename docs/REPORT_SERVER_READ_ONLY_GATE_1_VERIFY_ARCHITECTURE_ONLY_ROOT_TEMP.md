# REPORT — Server Read-Only Gate 1: Architecture Verified

Date: 2026-06-17 | Status: ✅ COMPLETE

## SSH: Confirmed ✅

```text
root@178.104.95.187 via temp key
```

## Path: `/opt/malyarka-telegram-bot` ✅

## Architecture Map

```
/opt/malyarka-telegram-bot/
├── malyarka_telegram/          # Telegram bot layer
│   ├── app.py                  # Bot scaffold (no aiogram import)
│   ├── router.py               # Mode router (state machine)
│   ├── handlers.py             # Message handlers (pure, no API)
│   ├── intent.py               # Intent classification (regex, local)
│   ├── modes.py                # Mode constants
│   ├── keyboards.py            # Telegram keyboards
│   ├── messages.py             # Russian message formatters
│   ├── session.py              # Session management
│   ├── access.py               # Owner access control
│   ├── voice.py                # Voice processing
│   ├── obsidian_inbox.py       # Note-taking bridge
│   ├── config.py               # ⛔ FORBIDDEN
│   └── engineer_tasks.py       # Engineer task definitions
│
├── malyarka_core/              # Core business logic
│   ├── calculations.py         # Area/quantity calculations
│   ├── parsing.py              # Text dimension parser
│   ├── validation.py           # Order finalization rules
│   ├── models.py               # Data models
│   ├── services/
│   │   ├── orders.py           # Service layer (pass-through)
│   │   └── archive.py          # Archive service
│   ├── exports/
│   │   ├── corel.py            # Corel export
│   │   ├── malyarka.py         # Painting workshop export
│   │   └── malyarka_file.py    # File export
│   ├── adapters/
│   │   ├── cli.py              # CLI adapter
│   │   └── telegram.py         # Telegram adapter ⚡ KEY FILE
│   ├── security/               # Access control
│   │   └── permissions.py
│   └── storage/                # Data persistence
│       ├── repository.py
│       ├── schema.py
│       └── reference_data.py
│
├── malyarka_ai/                # AI layer
│   ├── deepseek.py             # DeepSeek client
│   ├── pipeline.py             # Processing pipeline
│   ├── prompts.py              # AI prompts
│   ├── bridge.py               # AI bridge
│   ├── diagnostics.py          # AI diagnostics
│   ├── contracts.py            # AI contracts
│   ├── config.py               # ⛔ FORBIDDEN
│   └── __init__.py
│
├── malyarka_vision/            # Vision layer
│   ├── gemini.py               # Gemini client
│   ├── config.py               # ⛔ FORBIDDEN
│   └── __init__.py
│
└── requirements.txt            # aiogram>=3, openai>=1
```

## Adapter Insertion Point ⚡

**File:** `malyarka_core/adapters/telegram.py` (already exists!)

The server already has an adapter structure at `malyarka_core/adapters/`. The Telegram adapter at `adapters/telegram.py` is the natural insertion point for Hermes adapter logic.

### Existing Flow
```
Telegram → app.py → router.py → handlers.py → intent.py
```

### Target Flow
```
Telegram → app.py → router.py → handlers.py
→ malyarka_core/adapters/telegram.py (Hermes adapter)
→ malyarka_core/services/orders.py
```

## Safe Files for Review (Gate 2)

| File | Reason |
|------|--------|
| `malyarka_core/adapters/telegram.py` | ⚡ KEY — existing adapter |
| `malyarka_telegram/handlers.py` | Message processing |
| `malyarka_telegram/router.py` | Mode routing |
| `malyarka_telegram/intent.py` | Intent classification |
| `malyarka_core/services/orders.py` | Order service |
| `malyarka_core/exports/corel.py` | Corel export |

## Forbidden Files

| File | Reason |
|------|--------|
| `malyarka_telegram/config.py` | Secrets |
| `malyarka_ai/config.py` | Secrets |
| `malyarka_vision/config.py` | Secrets |
| Any `.env` | Secrets |

## Safety

```
server writes: 0 | token/.env/config: NOT read
DB/logs/orders: NOT read | live bot: NOT touched
polling/webhook: NOT started | git/patch: NOT executed
```

## Next Gate

`SERVER_READ_ONLY_GATE_2_SAFE_FILE_REVIEW_WHITELIST` (RED/YELLOW)
