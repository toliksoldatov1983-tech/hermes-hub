# Malyarka Clean — безопасная Telegram config-check проверка

Дата: 2026-06-14

Серия:

```text
Серия 105–108 — Безопасная Telegram config-check проверка
BATCH_SERIES_105_108_TELEGRAM_SAFE_CONFIG_CHECK
```

## Назначение

Config-check нужен, чтобы безопасно проверить подготовительный Telegram-слой без реального подключения Telegram.

Это не live Telegram.

## Созданные файлы

```text
E:\Hermes-Hub\projects\malyarka-clean\src\malyarka_clean_telegram\config_check.py
E:\Hermes-Hub\projects\malyarka-clean\tools\check_telegram_config.py
E:\Hermes-Hub\projects\malyarka-clean\tests\test_telegram_config_check.py
```

## Что возвращает diagnostics

`build_telegram_config_check_report()` возвращает:

```text
live_telegram: false
polling: false
token_required: false
real_token_used: false
reads_env_file: false
uses_old_bot_py: false
safe_to_run_without_token: true
```

## Что config-check НЕ делает

Config-check не:

- запускает Telegram;
- запускает polling;
- требует token;
- использует реальный token;
- читает `.env`;
- читает переменные окружения;
- импортирует старый `bot.py`;
- отправляет сообщения;
- создаёт Excel;
- подключает API;
- работает с базой данных.

## Как запустить вручную

Из PowerShell:

```powershell
$env:PYTHONPATH='E:\Hermes-Hub\projects\malyarka-clean\src'
$env:PYTHONIOENCODING='utf-8'
python E:\Hermes-Hub\projects\malyarka-clean\tools\check_telegram_config.py
```

Ожидаемый результат:

```text
Итог: OK. Config-check безопасен и запускается без Telegram token и без .env.
```

## Tests

Focused tests:

```powershell
$env:PYTHONPATH='E:\Hermes-Hub\projects\malyarka-clean\src'
python -m pytest E:\Hermes-Hub\projects\malyarka-clean\tests\test_telegram_config_check.py -q
```

Результат текущей серии:

```text
7 passed
```

## Важная граница

Реальный token подключать только отдельным будущим разрешением пользователя.

Live Telegram и polling запускать только отдельным будущим разрешением пользователя.

Старый `bot.py` не использовать как активную систему.

