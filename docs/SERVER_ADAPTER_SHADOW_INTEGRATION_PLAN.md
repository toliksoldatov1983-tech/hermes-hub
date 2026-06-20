# Server Adapter Shadow Integration Plan

Date: 2026-06-17 | No code, no patch

## Local → Server Mapping

| Local (E:\Hermes-Hub) | Server (/opt/...) |
|-----------------------|-------------------|
| `fake_telegram_adapter.py` | Server adapter module |
| Fake event dict | aiogram Message object |
| `process_telegram_event` | Router middleware/handler |
| `adapter_mode="fake"` | `adapter_mode="dry_run"` |

## How Telegram Event Becomes Adapter Event

```text
aiogram Message.text → adapter.process(text) → adapter_result
                                             → if blocked: return
                                             → if allowed: continue to Sales/Malyarka
```

## Key Principles

1. **Off-by-default**: feature flag `HERMES_ADAPTER_ENABLED=false`
2. **Dry-run first**: even when enabled, `dry_run=true`
3. **No side effects**: adapter returns result, doesn't call Telegram API
4. **Fallback safe**: if adapter fails → original handler path
5. **Production blocked**: `production_ready=false` always
