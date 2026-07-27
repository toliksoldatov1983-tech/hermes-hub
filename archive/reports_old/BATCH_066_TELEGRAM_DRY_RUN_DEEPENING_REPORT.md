# BATCH_066 — TELEGRAM DRY-RUN DEEPENING

Дата: 2026-07-01
Статус: ✅ ВЫПОЛНЕНО

---

## ЧТО СДЕЛАНО

### Новые файлы

| Файл | Описание |
|------|----------|
| `telegram/blocked_actions.py` | Центральный реестр 18 заблокированных действий (5 категорий) |
| `tests/test_telegram_dry_run_deep.py` | 22 теста: команды, безопасность, запрет токенов/сети |

### Изменённые файлы

| Файл | Изменение |
|------|-----------|
| `telegram/command_router.py` | +7 новых команд (/order, /disputes, /fix, /export-blocked, /audit, /safety, /blocked) + русские алиасы |
| `telegram/scenarios.py` | 13 новых сценариев (было 5 → стало 18) |
| `telegram/status_report.py` | Детальные категории blocked actions, расширенные safety limits |
| `cli.py` | telegram-status показывает blocked_actions и категории |

---

## НОВЫЕ DRY-RUN КОМАНДЫ

| Команда | Алиас | Описание |
|---------|-------|----------|
| `/order` | `/заказ` | Парсинг синтетического заказа |
| `/disputes` | `/споры` | Классификация спорных строк |
| `/fix` | `/исправить` | Подсказка по исправлению |
| `/export-blocked` | `/экспорт-заблокирован` | Причины блокировки экспорта |
| `/audit` | `/аудит` | Сводка аудит-лога |
| `/safety` | — | Классификация действия через safety gate |
| `/blocked` | — | Полный список заблокированных действий |

## BLOCKED ACTIONS (18)

| Категория | Кол-во | Примеры |
|-----------|--------|---------|
| telegram | 4 | live_polling, live_webhook, send_message, live_bot_start |
| secrets | 4 | token_read, env_read, key_access, secret_storage |
| orders | 3 | real_order_read, real_order_modify, client_data_access |
| export | 3 | file_export, real_excel_create, external_send |
| external | 4 | external_api, google_drive_write/move, archives_access |

---

## ПРОВЕРКИ

| Команда | Результат |
|---------|-----------|
| `message /status` | OK |
| `telegram-scenarios` | 18 сценариев ✅ |
| `telegram-status` | 26 aliases, 10 safety limits, 18 blocked ✅ |
| `smoke` | 20/20 OK ✅ |
| `run_tests.cmd` | **150 passed + 6 subtests** ✅ (+22 новых) |

## ТЕСТЫ БЕЗОПАСНОСТИ

- `test_command_router_does_not_read_env` — ✅
- `test_command_router_does_not_read_token_env` — ✅
- `test_no_polling_import` — ✅ (нет импорта polling)
- `test_no_telegram_send_import` — ✅ (нет aiogram/telethon)
- `test_no_network_call` — ✅

---

## ЧТО НЕ ТРОГАЛОСЬ

- TELEGRAM_TOKEN, .env
- Polling / webhook / отправка сообщений
- Внешние API
- Реальные заказы

## СЛЕДУЮЩИЙ ШАГ

BATCH_063B_PLAN_SAFE_PORT_MALYARKA_HARDENING_TO_HERMES_CLEAN
