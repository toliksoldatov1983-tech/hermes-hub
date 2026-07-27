# BATCH_099 — Telegram Intent Router + Malyarka Chat Dry-Run

Дата: 2026-07-02 · Статус: **COMPLETED** · 641 passed

---

## TEST COUNT RECONCILIATION

614 (BATCH_098) → 641 (BATCH_099: +27). BATCH_097 report: 618 was error (real: 614). BATCH_098 test file was not created.

## TELEGRAM INTENT ROUTER CONTRACT

`IntentType`: general_chat, malyarka_order, malyarka_order_correction, malyarka_order_confirmation, project_status, daily_assistant, what_next, help, safety_sensitive, unknown.

`IntentResult`: intent + confidence + route_target + clarification + audit.

## CONTEXT-AWARE ROUTING

Router учитывает: last_intent, has_draft_order, has_disputed_rows, awaiting_confirmation.

## MALYARKA ORDER DETECTION

Patterns: dimensions (720x300, 720х300, 720*300), quantity, color, material, order name, corrections, confirmations. Confidence: 0.1–0.95.

## GENERAL CHAT DRY-RUN

Обычный чат → mock assistant. Live AI disabled.

## TELEGRAM DRY-RUN FLOW

Fake message → Intent Router → Safety Gate → Runtime Bridge → Malyarka/Assistant → Response.

## CLARIFICATION LOGIC

Low confidence → suggested question: "Похоже на заказ для Малярки. Разобрать?"

## SAFETY GATES

6 blocked phrases: telegram token, .env, google drive, delete, gemini, deepseek.

## CLI COMMANDS (7)

| Команда | Статус |
|---------|--------|
| `telegram-intent-status` | OK |
| `telegram-intent-dry-run` | 7/9 OK (2 need context) |
| `telegram-intent-order-detect` | OK |
| `telegram-intent-chat-detect` | OK |
| `telegram-intent-clarify` | OK |
| `telegram-flow-dry-run` | OK |
| `telegram-safety-check` | 6/6 blocked |

## ТЕСТЫ: 27. 641 passed total.

## БЕЗОПАСНОСТЬ

Telegram token не читался. Live Telegram disabled. Все действия dry-run.

## СЛЕДУЮЩИЙ ШАГ

`BATCH_100_TELEGRAM_CONVERSATION_MEMORY_AND_ORDER_DRAFT_STATE`
