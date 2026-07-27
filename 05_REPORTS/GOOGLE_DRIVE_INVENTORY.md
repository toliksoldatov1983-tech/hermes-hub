# GOOGLE_DRIVE_INVENTORY

## Блок

BATCH_006_COLLECT_GOOGLE_DRIVE_INVENTORY

## Назначение

Это локальная инвентаризация верхнего уровня Google Drive по списку, который пользователь вставил в задание.

Google Drive не изменялся. Codex не заходил в Google Drive, не удалял, не перемещал, не переименовывал файлы, не менял права доступа и не создавал папки.

## Главные правила

- Никакой файл Google Drive не считается актуальной правдой Hermes-Clean без проверки.
- Старые Google Drive документы не являются главным источником.
- Главные архивные источники старой информации:
  - `[удалён] C:\Users\user\Desktop\«Гермес Клин».zip [архив]`
  - `C:\Users\user\Desktop\[архив] архивный zip-файл`
- Любой будущий перенос на Google Drive требует отдельного разрешения пользователя.

## ГРУППА 1 — старые Hermes-документы

Предварительная категория: кандидат на `HERMES_OLD_ARCHIVE`.

- `HERMES_NEXT_TASK_BLOCKS.md`
- `TELEGRAM_SETUP_RU.md`
- `HERMES_SEVEN_BLOCK_EXECUTION_PLAN.md`
- `QUICK_START_RU.md`
- `daily_agent_log.md`
- `2026-06-29.md`
- `HERMES_DAILY_AGENT_SAFETY_RULES.md`
- `BACKUP_AND_RESTORE_RU.md`
- `AI_AGENT_RESTORE_INSTRUCTION_RU.md`
- `HERMES_DAILY_AGENT_PLAN.md`
- `HERMES_PRICE_RULES.md`
- `proposal-izmenit-cenu-moderna-500000.md`

## ГРУППА 2 — старые файлы кода Hermes / агента

Предварительная категория: кандидат на `HERMES_OLD_ARCHIVE`.

- `agent.py`
- `planner.py`
- `memory_reader.py`
- `obsidian_reader.py`
- `telegram_dry_run.py`
- `telegram_sender.py`
- `daily_dashboard.py`
- `safety_gate.py`
- `capability_runner.py`
- `project_planner.py`
- `voice_adapter.py`
- `windows_scheduler.py`
- `schedule_runner.py`
- `task_manager.py`
- `price_book.py`
- `order_reader.py`
- `order_renderer.py`
- `talk_handler.py`
- `calendar_reader.py`
- `reminder_planner.py`
- `recurring_task_manager.py`
- `data_health.py`
- `renderers.py`
- `models.py`

## ГРУППА 3 — тесты Hermes

Предварительная категория: кандидат на `HERMES_OLD_ARCHIVE`.

- `test_telegram_block4.py`
- `test_telegram_sender.py`
- `test_self_check.py`
- `test_text_capture.py`
- `test_reminders.py`
- `test_daily_brief.py`
- `test_project_planner.py`
- `test_memory_search.py`
- `test_block5_adapters.py`
- `test_price_book.py`
- `test_cli_tasks.py`
- `test_orders_read_only.py`
- `test_notification_preview.py`
- `test_dry_run_interfaces.py`
- `test_recurring_tasks.py`
- `test_data_health.py`
- `test_models.py`
- `test_safety_gate.py`
- `test_memory_reader.py`
- `test_daily_dashboard.py`

## ГРУППА 4 — PowerShell-скрипты Hermes

Предварительная категория: кандидат на `HERMES_OLD_ARCHIVE`.

- `hermes_prices.ps1`
- `hermes_scheduler_plan.ps1`
- `hermes_check.ps1`
- `hermes_inbox.ps1`
- `hermes_tests.ps1`
- `hermes_telegram_setup_help.ps1`
- `hermes_daily.ps1`
- `hermes_set_telegram_token.ps1`
- `hermes_copy_backup_to_usb.ps1`
- `hermes_telegram_ready.ps1`
- `hermes_orders.ps1`
- `hermes_menu.ps1`
- `hermes_make_portable_backup.ps1`
- `hermes_today.ps1`
- `hermes_daily_save.ps1`
- `hermes_health.ps1`

## ГРУППА 5 — JSON / данные

Предварительная категория: кандидат на `HERMES_OLD_ARCHIVE`.

- `memory_sources.json`
- `proposals.json`
- `price_rules.json`
- `recurring_tasks.json`
- `tasks.json`

## ГРУППА 6 — старые документы Малярки

Предварительная категория: старые Malyarka-документы. Не удалять. Переносить в `HERMES_OLD_ARCHIVE` только после отдельного разрешения пользователя.

- `Малярка — сводная рабочая выжимка`
- `проект малярка`
- `Малярка — настройка Space Agent`
- `Инструкция для агента Малярка`
- `ТЗ агента Малярка`
- `Правила Малярка`
- `Реестр норм расхода Малярка`
- `Реестр цен на материалы Малярка`
- `Реестр цен на услуги Малярка`
- `Шаблон архивной карточки заказа Малярка`
- `Шаблон файла для Малярки и учёта материала`
- `Шаблон файла для учёта финансов Малярка`
- `Шаблон входного заказа Малярка`
- `Шаблон файла для Corel Малярка`
- `Эталонный прогон заказа Малярка — УЧ-003`
- `Эталонный прогон заказа Малярка — УЧ-002`
- `Эталонный прогон заказа Малярка — Юля 001`

## ГРУППА 7 — Google Sheets / Apps Script

Предварительная категория: НЕ ТРОГАТЬ БЕЗ ОТДЕЛЬНОГО РАЗРЕШЕНИЯ.

Причина: эти элементы могут содержать таблицы, скрипты, задачи или рабочие данные.

- `Заказы`
- `Список дел`
- `MalyarkaMasterBot_2`
- `Проект без названия`

## Предварительная классификация

1. Группы 1-5: старые Hermes-файлы, кандидаты на `HERMES_OLD_ARCHIVE`.
2. Группа 6: старые Malyarka-документы, кандидаты на `HERMES_OLD_ARCHIVE` только после отдельного разрешения пользователя.
3. Группа 7: не трогать без отдельного разрешения.
4. Ни один файл из Google Drive не считать актуальной правдой Hermes-Clean без проверки.
5. Главные архивные источники остаются `«Гермес Клин».zip [архив]` и `[архив] архивный zip-файл` на рабочем столе.

## Что требует подтверждения пользователя

- Создавать ли на Google Drive папку `HERMES_CLEAN`.
- Создавать ли на Google Drive папку `HERMES_OLD_ARCHIVE`.
- Какие именно файлы переносить в `HERMES_OLD_ARCHIVE`.
- Что делать с Google Sheets / Apps Script из группы 7.
- Какие Malyarka-документы можно переносить, а какие нужно оставить на месте.

## Следующий крупный блок

BATCH_007_WAIT_USER_APPROVAL_FOR_GOOGLE_DRIVE_STRUCTURE.
