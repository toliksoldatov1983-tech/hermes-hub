# BATCH_101 — E2E Dry-Run Scenarios + UX

Дата: 2026-07-02 · Статус: **COMPLETED** · 733 passed

---

## E2E SCENARIO CONTRACT

`E2EScenario`: steps + expected modes/draft statuses + final state + audit.
`E2EStep`: user_message, expected_intent, expected_mode, expected_draft_status, expected_blocked.
`E2EScenarioRunner`: run_scenario, run_all, run_all_and_report.

## CORE USER SCENARIOS (8)

| ID | Сценарий | Шаги | Статус |
|----|---------|------|--------|
| e2e-001 | Happy path (заказ) | 2 | ✅ |
| e2e-002 | Сомнительный заказ | 2 | ✅ |
| e2e-003 | Исправление + confirm | 3 | ✅ |
| e2e-004 | Отмена черновика | 2 | ✅ |
| e2e-005 | Обычный чат | 2 | ✅ |
| e2e-006 | Статус проекта | 1 | ✅ |
| e2e-007 | Safety blocked | 2 | ✅ |
| e2e-008 | Многошаговое исправление | 3 | ✅ |

## MULTI-TURN TRANSCRIPTS

Runner прогоняет сценарии с сохранением состояния между шагами.

## TELEGRAM UX RESPONSE

`RoutedResponse`: text + buttons + session_state + draft_state + warnings.

## CLI (9 новых)

telegram-e2e-status, telegram-e2e-scenario-list, telegram-e2e-run-all, telegram-e2e-order-happy-path, telegram-e2e-ambiguous-order, telegram-e2e-correction-flow, telegram-e2e-safety-check, telegram-e2e-ux-preview.

## ТЕСТЫ: 42. 733 passed total.

## БЕЗОПАСНОСТЬ

Все: Telegram token, live, .env — не трогались. Dry-run only.

## СЛЕДУЮЩИЙ ШАГ

`BATCH_102_TELEGRAM_LIVE_GATEWAY_READINESS_AND_APPROVAL_GATES`
