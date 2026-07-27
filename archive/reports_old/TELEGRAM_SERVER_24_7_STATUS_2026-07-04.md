# TELEGRAM_SERVER_24_7_STATUS_2026-07-04

Дата: 2026-07-04 13:27 +05:00
Исполнитель: Codex

## Цель

Проверить Telegram/Hermes bot gateway и готовность работы 24/7 с сервера, чтобы пользователь мог продолжать работу с телефона при выключенном ПК.

## Проверено

- Локальная папка `C:\Users\user\Documents\«Гермес Клин».` содержит только инструкции и отчеты, без кода бота.
- Локальная legacy-обертка `C:\Users\user\Documents\Codex\Malyarka_Bot_Service` указывает на отсутствующую папку `C:\Users\user\Desktop\malyarka_codex_work`.
- Windows Scheduled Task `Malyarka Telegram Bot` существует, но отключен.
- Батник `C:\Users\user\Desktop\Перезапустить_бота.bat` перезапускает серверный `hermes-gateway` через SSH.
- Сервер `hermes-server` доступен по SSH.
- `hermes-gateway.service` на сервере:
  - `active`;
  - `enabled`;
  - `Restart=always`;
  - `Linger=yes`;
  - Main PID: `10807`;
  - команда запуска: `/usr/local/lib/hermes-agent/venv/bin/python -m hermes_cli.main gateway run --replace`.
- Локальный `scripts\hermes.cmd telegram-status` показывает dry-run статус Hermes-Clean, не live polling.

## Найдено

- На сервере нет второго видимого `telegram`/`gateway`/`polling` процесса, кроме `hermes-gateway`.
- В логах сервера после рестарта были `Telegram polling conflict` до `2026-07-04 08:20:11 UTC`.
- После `08:20:11 UTC` новых conflict-строк в проверенном окне не появилось.
- Ранее в логах был `InvalidToken` из-за ошибочного формата токена, но текущий процесс после `08:04:04 UTC` запущен и не падал.
- Owner phone `/status` reached the server at `2026-07-04 08:29:42 UTC`.
- Server log showed `Unauthorized user: 784990082 (Soldatov Anatoliy) on telegram`.
- Telegram returned pairing flow, so transport works but access is not approved yet.

## Статус

`PHONE_LIVE_TEST_PASSED`

Серверная 24/7-часть поднята и работает независимо от включенного ПК. Входящий Telegram update с телефона дошел до сервера, pairing approval выполнен после отдельного подтверждения пользователя, повторный `/status` с телефона вернул `Hermes Gateway Status`.

## Pairing Approval

- Пользователь подтвердил: `разрешаю привязать Telegram 5MUQKKUT`.
- Выполнено на сервере: `hermes pairing approve telegram 5MUQKKUT`.
- Сервер подтвердил: `Soldatov Anatoliy (784990082)` теперь может пользоваться ботом.
- `hermes-gateway` после approval: `active`, `enabled`.

## Phone Live Test

- Повторный `/status` после pairing approval вернул `Hermes Gateway Status`.
- Сервер после теста: `hermes-gateway` `active`, `enabled`.
- Свежий journal window: новых ошибок нет.

## Безопасность

- `.env` не читался.
- Токены и ключи не читались и не выводились.
- Live bot не перезапускался.
- Второй polling не запускался.
- Реальные заказы не открывались и не менялись.
- Google Drive не менялся.
- Файлы не удалялись.

## Следующий крупный шаг

Вернуться к рабочему сценарию: ждать реальный заказ или безопасную команду в Telegram. Реальный export и работа с заказами выполняются только после отдельного подтверждения.
