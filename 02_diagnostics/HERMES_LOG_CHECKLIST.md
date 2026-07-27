# Чеклист проверки логов Hermes

Используй при сбоях обновления, запуска Desktop, модели, инструментов или конфигурации.

## Быстрые команды

```powershell
hermes logs errors
hermes logs desktop
hermes logs gui
hermes logs --since 1h
hermes doctor
hermes status
```

`hermes doctor --fix` запускать только после отдельного подтверждения.

## Основные логи Windows

- `C:\Users\user\AppData\Local\hermes\logs\bootstrap-installer.log` - обновление и rebuild Desktop.
- `C:\Users\user\AppData\Local\hermes\logs\desktop.log` - запуск Desktop и backend ready.
- `C:\Users\user\AppData\Local\hermes\logs\gui.log` - GUI, frontend, предупреждения конфигурации.
- `C:\Users\user\AppData\Local\hermes\logs\backend.log` - backend и сервисы.

## Что искать

- `error`
- `failed`
- `exception`
- `traceback`
- `TypeScript`
- `typecheck`
- `npm`
- `exit code`
- `config`
- `backend ready`
- `HERMES_DASHBOARD_READY`

## Безопасный порядок диагностики

1. Зафиксировать время ошибки.
2. Прочитать последние строки логов.
3. Выполнить `hermes logs errors`.
4. Выполнить `hermes doctor` без `--fix`.
5. Проверить `hermes status`.
6. Если ошибка после обновления, проверить `bootstrap-installer.log`.
7. Если ошибка Desktop, проверить `desktop.log` и `gui.log`.
8. Если ошибка сборки, проверить `npm run typecheck` и `npm run pack` в папке Desktop.
9. Перед изменениями сделать backup файла, который будет правиться.
10. После исправления перезапустить Hermes и проверить свежие логи.

## Что не делать без подтверждения

- Не запускать автоматический `--fix`.
- Не удалять логи.
- Не чистить sessions, checkpoints или memory.
- Не менять `.env`, ключи и токены.
- Не переустанавливать Hermes без отдельной команды пользователя.
