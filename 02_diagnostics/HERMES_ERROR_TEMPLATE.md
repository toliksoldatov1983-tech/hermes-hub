# Шаблон разбора ошибки Hermes

Используй для каждого сбоя Hermes Desktop, CLI или обновления.

## Кратко

- Дата:
- Где ошибка: Desktop / CLI / update / config / model / tools / другое
- Что делали перед ошибкой:
- Что ожидалось:
- Что произошло:

## Симптомы

- Текст ошибки:
- Скриншот:
- Команда, если запускалось из терминала:
- Повторяется стабильно: да / нет / неизвестно

## Логи

- `C:\Users\user\AppData\Local\hermes\logs\bootstrap-installer.log`
- `C:\Users\user\AppData\Local\hermes\logs\desktop.log`
- `C:\Users\user\AppData\Local\hermes\logs\gui.log`
- `C:\Users\user\AppData\Local\hermes\logs\backend.log`

## Диагностика

- Проверить `hermes logs errors`.
- Проверить `hermes doctor` без `--fix`.
- Проверить `hermes status`.
- Проверить свежие строки логов после времени ошибки.
- Проверить, запускался ли свежий `Hermes.exe`.
- Проверить, нет ли TypeScript/build ошибок после обновления.

## Решение

- Найденная причина:
- Что изменено:
- Какие файлы изменены:
- Нужен ли backup:
- Нужен ли перезапуск Hermes:

## Проверки после исправления

- Команда проверки:
- Результат:
- Hermes Desktop запускается:
- Логи без новой ошибки:

## Риски и следующий шаг

- Риски:
- Следующий крупный блок:
