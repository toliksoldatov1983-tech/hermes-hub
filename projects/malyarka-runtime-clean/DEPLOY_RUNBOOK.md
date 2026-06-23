# Malyarka Runtime Clean Deploy Runbook

Дата: 2026-06-23

## Главное правило

Deploy запрещен, пока серверный бот ловит:

```text
TelegramUnauthorizedError
```

Сначала нужен актуальный токен из BotFather.

## 1. Health-check без изменений

```powershell
.\ops\server_health_check.ps1
```

Скрипт не читает значения секретов. Он показывает только имена env-переменных и последние ошибки журнала с редактированием токенов.

## 2. Упаковка clean-кандидата

```powershell
.\ops\package_runtime_clean.ps1
```

Создает zip в:

```text
dist/
```

В пакет не попадают:

```text
.env
orders.db
.venv
.git
__pycache__
.pytest_cache
*.log
*.lock
```

## 3. Dry-run deploy

```powershell
.\ops\deploy_runtime_clean.ps1
```

Без `-Apply` скрипт:

- запускает локальные тесты;
- пакует clean runtime;
- отправляет zip на сервер в `/tmp`;
- распаковывает в `/opt/malyarka-telegram-bot.next`;
- запускает `compileall`;
- не трогает live `/opt/malyarka-telegram-bot`;
- не перезапускает сервис.

## 4. Ротация Telegram token

Только после получения нового токена у BotFather:

```powershell
.\ops\rotate_telegram_token.ps1 -NewToken "123456789:..." -Apply
```

Скрипт:

- делает backup `/etc/malyarka-telegram-bot.env`;
- меняет только `MALYARKA_TELEGRAM_BOT_TOKEN`;
- перезапускает сервис;
- показывает журнал без печати токена.

## 5. Apply deploy

Только после зеленого health-check:

```powershell
.\ops\deploy_runtime_clean.ps1 -Apply
```

Скрипт:

- запускает тесты;
- делает backup live-кода;
- останавливает сервис;
- синхронизирует clean runtime в `/opt/malyarka-telegram-bot`;
- стартует сервис;
- показывает статус и последние логи.

## Что пока не деплоить

Экспериментальные серверные файлы:

```text
malyarka_core/hermes_chat.py
malyarka_vision/openai_vision.py
```

Их нужно разбирать отдельным этапом.
