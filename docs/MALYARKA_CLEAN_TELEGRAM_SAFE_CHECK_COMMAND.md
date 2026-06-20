# Malyarka Clean - безопасная Telegram check-команда

Дата: 2026-06-14

Серия:

```text
Серия 083-086 - Безопасная Telegram check-команда без live-запуска
BATCH_SERIES_083_086_TELEGRAM_SAFE_CHECK_COMMAND
```

## Зачем нужна check-команда

Check-команда нужна, чтобы локально проверить безопасный Telegram-каркас Malyarka Clean до любого реального подключения Telegram.

Команда проверяет:

- импорт `malyarka_clean_telegram`;
- безопасные diagnostics-флаги;
- работу `build_telegram_order_reply()` на трех типах текста заказа;
- что adapter формирует текстовый ответ в dry-check режиме.

Файл команды:

```text
E:\Hermes-Hub\projects\malyarka-clean\tools\check_telegram_skeleton.py
```

## Как она отличается от live Telegram

Это не live Telegram.

Команда не:

- запускает Telegram;
- запускает polling;
- подключает token;
- читает `.env`;
- отправляет сообщения;
- отправляет файлы;
- создает Excel;
- использует старый `bot.py`;
- использует старый Telegram-код;
- подключает API;
- работает с базой данных.

## Что проверяется

Diagnostics должны оставаться безопасными:

```text
live_telegram=false
polling=false
token_required=false
reads_env_file=false
uses_old_bot_py=false
sends_files=false
creates_excel=false
```

Adapter проверяется на трех примерах:

```text
clean
has_disputes
empty_or_invalid
```

## Как запускать вручную

Из PowerShell:

```powershell
$env:PYTHONPATH='E:\Hermes-Hub\projects\malyarka-clean\src'
python E:\Hermes-Hub\projects\malyarka-clean\tools\check_telegram_skeleton.py
```

Ожидаемый результат:

```text
Итог: OK. Telegram-каркас импортируется и работает в безопасном dry-check режиме.
```

## Tests

Focused tests:

```powershell
$env:PYTHONPATH='E:\Hermes-Hub\projects\malyarka-clean\src'
python -m pytest E:\Hermes-Hub\projects\malyarka-clean\tests\test_telegram_skeleton_check_command.py -q
```

Результат текущей серии:

```text
6 passed
```

## Важная граница

Check-команда является подготовительным шагом перед будущим Telegram-подключением.

Она не дает разрешения:

- читать `.env`;
- использовать token;
- запускать polling;
- запускать Telegram live;
- отправлять сообщения пользователям;
- создавать файлы Excel из Telegram adapter.

Реальное Telegram-подключение должно быть отдельной серией и только после отдельного разрешения пользователя.
