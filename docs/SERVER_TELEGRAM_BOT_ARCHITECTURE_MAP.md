# Architecture map серверного Telegram-бота

Дата: 2026-06-15

Источник анализа:

`E:\Hermes-Hub\inputs\server_bot_read_only_copy\SERVER_BOT_READ_ONLY_REPORT.md`

Это карта по локальному read-only collector-отчёту. Сервер, live-бот, polling, token, `.env`, `config.py`, Vision и API не трогались.

## Граница безопасности

Collector-отчёт показывает безопасный режим анализа:

* `read_only: true`;
* `whitelist_only: true`;
* `bot_code_executed: false`;
* `bot_modules_imported: false`;
* `processes_started: false`;
* `environment_read: false`;
* `env_file_read: false`;
* `token_read: false`;
* `files_changed: false`.

Collector читал только локальную staging-копию:

`E:\Hermes-Hub\inputs\server_bot_read_only_copy`

Не читались `.env`, token-like files, secret files, переменные окружения, базы, логи и приватные ключи.

## Общая архитектура

Общая цепочка существующего серверного Telegram-бота по collector-отчёту:

```text
Telegram
-> malyarka_telegram/app.py
-> aiogram Bot / Dispatcher
-> router.py
-> handlers.py
-> malyarka_core/services/orders.py
-> parsing.py / validation.py / calculations.py
-> exports / files
```

`app.py` является live-точкой входа Telegram-слоя. В нём создаётся `Dispatcher`, регистрируются обработчики сообщений и callback-действий, а запуск выполняется через polling.

## Точка входа и polling

В отчёте найдена точка входа:

* `malyarka_telegram/app.py`;
* функция `run_polling(config: TelegramConfig | None = None) -> int`;
* создание `Dispatcher()`;
* регистрация `@dispatcher.message()`;
* регистрация callback handlers;
* запуск `await dispatcher.start_polling(bot)`;
* CLI-точка `main()`;
* запуск через `--run-polling`.

Из предыдущей инвентаризации серверного процесса известно, что live-команда была:

```text
/opt/malyarka-telegram-bot/.venv/bin/python -m malyarka_telegram.app --run-polling
```

Это подтверждает режим: Telegram live работает через polling. В рамках этого анализа polling не запускался и не останавливался.

## Основные режимы

Режимы определяются в Telegram-слое через `malyarka_telegram/router.py`, `malyarka_telegram/modes.py`, `malyarka_telegram/session.py` и `malyarka_telegram/intent.py`.

По collector-отчёту видны режимы:

* neutral;
* order;
* chat;
* engineer;
* ideas;
* admin;
* summary;
* rules.

Логика маршрутизации:

* текущий режим хранится через session store;
* команды переключают режимы;
* neutral mode может уточнять намерение пользователя;
* order mode отправляет текст в заказную обработку;
* admin mode защищён owner/access checks;
* engineer mode связан с инженерным workflow.

## Обработчики сообщений

Основная обработка сообщений проходит через `@dispatcher.message()` в `app.py`.

Дальше текст проходит через:

* `router.py` — выбор режима и действия;
* `handlers.py` — безопасная текстовая обвязка без прямого импорта aiogram;
* `malyarka_core.adapters.telegram` — построение preview заказа;
* `malyarka_core/services/orders.py` — сервисный слой заказа.

Collector-отчёт показывает, что `handlers.py` специально отделяет Telegram runtime от логики обработки текста. Это важная будущая точка для безопасного adapter layer.

## Callback actions

В `app.py` зарегистрированы callback-действия:

* `COREL_EXCEL_ACTION`;
* `MALYARKA_FILE_ACTION`;
* `ENGINEER_TASK_ACTIONS`;
* `CLARIFY_INTENT_ACTIONS`.

Найденные обработчики:

* `handle_corel_excel_callback(...)`;
* `handle_malyarka_file_callback(...)`;
* `handle_engineer_task_callback(...)`;
* `handle_clarify_intent_callback(...)`.

Corel callback готовит и отправляет Excel-файл для Corel. Malyarka file callback готовит и отправляет файл малярки. Engineer callback отвечает на инженерные task-card actions без запуска Hermes и без изменения файлов. Clarify callback переключает пользователя в нужный режим: заказ, идеи, инженер или отмена.

## Кнопки

В `keyboards.py` и `messages.py` обнаружены inline/reply keyboard flows:

* основная reply-клавиатура;
* copy keyboard для preview заказа;
* кнопки спорных строк;
* кнопка скачивания Excel для Corel;
* copy-кнопка для Corel;
* engineer task keyboard;
* clarify intent keyboard.

Ключевые действия:

* `download_corel_excel`;
* `download_malyarka_file`;
* `engineer_task_allow_read_only`;
* clarify actions для order / ideas / engineer / cancel.

## Связь Telegram -> core

Связь Telegram-слоя с core проходит через несколько уровней:

* `app.py` импортирует export-функции из `malyarka_core.exports`;
* `handlers.py` использует `build_order_preview_from_text`;
* `orders.py` координирует parsing, validation, calculations и exports;
* `parsing.py` разбирает размеры;
* `validation.py` проверяет возможность export;
* `calculations.py` считает площадь и количество;
* export-слой готовит файлы.

Практическая карта:

```text
Telegram message
-> app.py dispatcher
-> router.py mode routing
-> handlers.py text response
-> build_order_preview_from_text
-> services/orders.py
-> parsing / validation / calculations
-> preview / buttons / export callbacks
```

## Excel/Corel поток

Excel/Corel поток найден в `app.py` и `malyarka_core/services/orders.py`.

По отчёту видны элементы:

* `_RUNTIME_COREL_ROWS`;
* `PreparedCorelExcel`;
* `prepare_corel_excel_for_user(...)`;
* `export_corel_xlsx(order, output_path)`;
* временный файл вида `malyarka_corel_{user_id}.xlsx`;
* callback `handle_corel_excel_callback(...)`;
* отправка документа через Telegram.

Важно: этот поток относится к существующему серверному боту. В рамках Hermes Hub анализировалась только локальная копия отчёта, Excel не создавался.

## Файл малярки

Отдельно найден Malyarka file поток:

* `PreparedMalyarkaFile`;
* `prepare_malyarka_file_for_user(...)`;
* `export_malyarka_file_xlsx(order, output_path)`;
* временный файл вида `malyarka_file_{user_id}.xlsx`;
* callback `handle_malyarka_file_callback(...)`;
* отправка документа через Telegram.

Это зона будущего риска: она связана с созданием файлов и отправкой через live Telegram. Менять её напрямую нельзя без отдельного плана и разрешения.

## Инженерный workflow

Engineer workflow связан с:

* `ENGINEER_TASK_ACTIONS`;
* `ENGINEER_TASK_ALLOW_ACTION`;
* engineer task keyboard;
* callback `handle_engineer_task_callback(...)`.

Collector-отчёт явно показывает формулировку, что engineer task-card callbacks должны отвечать без запуска Hermes и без изменения файлов. Это хороший принцип для будущего adapter layer: сначала read-only и диагностика, затем отдельное разрешение на действия.

## Owner/access checks

Access-слой находится в `malyarka_telegram/access.py` и используется в `app.py`, `router.py`, `handlers.py`, `messages.py`.

Найдены функции и проверки:

* `parse_owner_id(...)`;
* `is_owner(...)`;
* `is_owner_id_configured(...)`;
* `format_access_denied_message()`;
* owner-only modes;
* защита admin mode;
* access denied при callback-действиях.

Отчёт не раскрывает значения owner_id. Подозрительные строки были замаскированы redaction-механизмом.

## Obsidian hints

В предыдущей серверной инвентаризации был найден файл `malyarka_telegram/obsidian_inbox.py`.

В whitelist текущего collector он не входил, поэтому архитектурная карта не делает выводов по его содержимому. Это можно изучать только отдельным будущим read-only разрешением, если Obsidian workflow станет важным.

## Missing file

В whitelist был указан файл:

`malyarka_telegram/models.py`

Collector зафиксировал его как missing. По текущей карте архитектуры Telegram-бот работает без этого файла в staging-копии; нужно учитывать это при будущей карте зависимостей.

## Redaction summary

Collector применил redaction к подозрительным строкам.

Зафиксировано: 22 срабатывания redaction.

Маскировались строки с признаками:

* `TOKEN`;
* `SECRET`;
* `API_KEY`;
* `PASSWORD`;
* `PRIVATE_KEY`;
* `bot_token`;
* `.env`.

Секретные значения в отчёт и документы не переносились.

## Зоны риска

Основные зоны риска:

* live polling в `app.py`;
* token и `.env`;
* `config.py`, который специально не копировался;
* owner/access checks;
* callback-отправка файлов;
* Excel/Corel export внутри live Telegram;
* Malyarka file export;
* archive/storage/db-зона;
* admin mode;
* redacted строки;
* отсутствующий `malyarka_telegram/models.py`;
* возможный Obsidian workflow вне текущего whitelist.

Эти зоны нельзя менять напрямую. Сначала нужна карта, adapter layer, diagnostics, feature flags и rollback plan.

## Точки будущего подключения Hermes adapter

Безопасные потенциальные точки подключения Hermes:

1. Между `router.py` / `handlers.py` и core-сервисами.
   Это позволит подключать Hermes как отдельный adapter, не превращая `app.py` в экспериментальную площадку.

2. Вокруг `build_order_preview_from_text`.
   Можно анализировать заказ до live-действий и сохранять совместимость с текущим Telegram UX.

3. Вокруг `services/orders.py`.
   Это слой, где уже сходятся parsing, validation, calculations и exports.

4. Перед callback export-действиями.
   Можно добавить диагностику, feature flags и dry-run проверки до создания или отправки файлов.

5. Отдельный diagnostics / read-only режим.
   Такой слой может показывать состояние без token, без `.env`, без polling и без изменения файлов.

Нельзя начинать с хаотичной правки `app.py` live-бота. Главная стратегия остаётся прежней: сначала карта и защитный слой, потом adapter, потом диагностика и флаги, и только после этого маленькие изменения live-бота.

## Следующий безопасный шаг

Следующий безопасный шаг:

Серия 167-170 — План Hermes adapter layer для серверного Telegram-бота

Техническое имя:

`BATCH_SERIES_167_170_HERMES_ADAPTER_LAYER_PLAN`
