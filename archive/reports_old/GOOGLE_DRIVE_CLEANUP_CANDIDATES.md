# GOOGLE_DRIVE_CLEANUP_CANDIDATES

## Блок

BATCH_006_COLLECT_GOOGLE_DRIVE_INVENTORY

## А. КАНДИДАТЫ НА HERMES_OLD_ARCHIVE

Эти элементы считаются кандидатами на будущий перенос только после отдельного разрешения пользователя.

### Старые Hermes-документы

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

### Старые Python-файлы

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

### Старые тесты

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

### Старые PowerShell-скрипты

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

### Старые JSON-файлы

- `memory_sources.json`
- `proposals.json`
- `price_rules.json`
- `recurring_tasks.json`
- `tasks.json`

### Старые документы Малярки

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

## Б. НЕ ТРОГАТЬ БЕЗ РАЗРЕШЕНИЯ

- `Заказы`
- `Список дел`
- `MalyarkaMasterBot_2`
- `Проект без названия`
- любые Google Sheets;
- любые Apps Script;
- документы клиентов;
- реальные заказы;
- файлы с токенами, ключами, доступами;
- неизвестные документы.

## В. ТРЕБУЕТ РУЧНОЙ ПРОВЕРКИ

- `Малярка — сводная рабочая выжимка`
- `Правила Малярка`
- `Реестр цен на услуги Малярка`
- `Реестр цен на материалы Малярка`
- любые документы, которые могут содержать полезные правила, но не считаются актуальными автоматически.

## Запреты

- Не удалять Google Drive файлы.
- Не перемещать Google Drive файлы.
- Не создавать папки на Google Drive.
- Не менять права доступа.
- Не открывать содержимое старых документов.
- Не читать токены, ключи, `.env`.
- Не трогать реальные заказы.
- Не считать старые Google Drive файлы актуальной правдой проекта.

## Следующий крупный блок

BATCH_007_WAIT_USER_APPROVAL_FOR_GOOGLE_DRIVE_STRUCTURE.
