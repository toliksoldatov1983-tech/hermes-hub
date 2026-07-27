# QUARANTINE_MOVE_REPORT

## Блок

BATCH_004_MOVE_APPROVED_ITEMS_TO_QUARANTINE

## Подтверждение

Пользователь явно разрешил карантин старых объектов командой: "разрешаю карантин".

## Карантин

Создана папка:

`C:\Users\user\Desktop\[удалён]`

Внутри создан файл:

`C:\Users\user\Desktop\[удалён]\README_DO_NOT_USE_AS_SOURCE.md`

## Перенесено в карантин

- `C:\Users\user\Desktop\Hermes Пульт` -> `C:\Users\user\Desktop\[удалён]\Hermes Пульт`
- `C:\Users\user\Desktop\hermes_codex_package` -> `C:\Users\user\Desktop\[удалён]\hermes_codex_package`
- `C:\Users\user\Desktop\гермес мысли` -> `C:\Users\user\Desktop\[удалён]\гермес мысли`
- `C:\Users\user\Desktop\Hermes Agent OS.lnk` -> `C:\Users\user\Desktop\[удалён]\Hermes Agent OS.lnk`
- `C:\Users\user\Desktop\«Гермес Клин».lnk` -> `C:\Users\user\Desktop\[удалён]\«Гермес Клин».lnk`
- `C:\Users\user\Desktop\Hermes Пульт.lnk` -> `C:\Users\user\Desktop\[удалён]\Hermes Пульт.lnk`
- `C:\Users\user\Desktop\Hermes рабочие файлы.lnk` -> `C:\Users\user\Desktop\[удалён]\Hermes рабочие файлы.lnk`
- `C:\Users\user\Desktop\Hermes.lnk` -> `C:\Users\user\Desktop\[удалён]\Hermes.lnk`
- `C:\Users\user\Desktop\Проверить «Гермес Клин».lnk` -> `C:\Users\user\Desktop\[удалён]\Проверить «Гермес Клин».lnk`
- `C:\Users\user\Desktop\Малярка - Ход проекта Гермес.pdf` -> `C:\Users\user\Desktop\[удалён]\Малярка - Ход проекта Гермес.pdf`

## Не найдено

Не найденных объектов из разрешённого списка нет.

## Не удалось перенести

- `C:\Users\user\Desktop\malyarka_codex_work`
  - Причина: Windows сообщил, что объект используется другим процессом.
  - Действие: принудительный перенос не выполнялся, доступ не ломался, объект оставлен на рабочем столе.

## Осталось на рабочем столе

Обязательные объекты, которые должны остаться:

- `C:\Users\user\Desktop\Hermes-Clean`
- `[удалён] C:\Users\user\Desktop\«Гермес Клин».zip [архив]`
- `C:\Users\user\Desktop\[архив] архивный zip-файл`

Также остался объект, который не удалось перенести:

- `C:\Users\user\Desktop\malyarka_codex_work`

## Соблюдённые запреты

- Ничего не удалялось.
- Архивы не распаковывались.
- `.env`, токены, ключи и базы не читались.
- Google Drive не изменялся.
- Реальные заказы не трогались.
- Старый Hermes и Telegram-бот не запускались.
- `Hermes-Clean`, `«Гермес Клин».zip [архив]` и `[архив] архивный zip-файл` не переносились.
- Файлы вне явно разрешённого списка не переносились.

## Итог

Карантин создан. Подтверждённые доступные объекты перенесены.

Один объект, `malyarka_codex_work`, остался на рабочем столе из-за блокировки другим процессом.

Следующий крупный блок: BATCH_005_PREPARE_GOOGLE_DRIVE_CLEANUP_PLAN.

## BATCH_004B_RETRY_LOCKED_QUARANTINE_ITEM

### Цель

Повторно попробовать перенести `C:\Users\user\Desktop\malyarka_codex_work` в `C:\Users\user\Desktop\[удалён]`.

### Результат

Перенос не выполнен.

### Причина

Windows повторно сообщил: "The process cannot access the file because it is being used by another process."

### Статус объекта

- Исходный объект существует: `C:\Users\user\Desktop\malyarka_codex_work`
- Назначение не создано: `C:\Users\user\Desktop\[удалён]\malyarka_codex_work`
- Принудительные действия не выполнялись.
- Процессы не закрывались.
- Содержимое папки не читалось.

### Следующий крупный блок

BATCH_004C_USER_CLOSE_LOCKING_PROCESS: пользователь закрывает процесс, который держит доступ к `malyarka_codex_work`, затем можно повторить перенос отдельной командой.

## BATCH_004D_RETRY_AFTER_USER_CLOSED_PROCESS

### Подтверждение

Пользователь сообщил, что закрыл возможные блокирующие программы / перезагрузил компьютер.

### Цель

Повторно перенести `C:\Users\user\Desktop\malyarka_codex_work` в `C:\Users\user\Desktop\[удалён]`.

### Результат

Перенос не выполнен.

### Причина

Windows снова сообщил: "The process cannot access the file because it is being used by another process."

### Статус объекта

- Исходный объект существует: `C:\Users\user\Desktop\malyarka_codex_work`
- Назначение не создано: `C:\Users\user\Desktop\[удалён]\malyarka_codex_work`
- Принудительные действия не выполнялись.
- Процессы не закрывались и не убивались.
- Содержимое папки не читалось.

### Следующий крупный блок

BATCH_004E_MANUAL_FIND_LOCKING_PROCESS: вручную определить, какой процесс держит `malyarka_codex_work`, без удаления и без принудительного завершения процессов Codex.

## BATCH_004F_CLOSE_OLD_HERMES_PROCESSES_AND_RETRY_QUARANTINE

### Подтверждение

Пользователь разрешил закрыть только PID 11680, 18920 и 11236.

### Закрытые процессы

- `cmd.exe` PID 11680 — старый [архив] [удалённый архив] memory-gateway.
- `node.exe` PID 18920 — дочерний процесс старого memory-gateway.
- `chrome.exe` PID 11236 — старый Hermes dashboard.

### Перенос

`C:\Users\user\Desktop\malyarka_codex_work` успешно перенесён в `C:\Users\user\Desktop\[удалён]\malyarka_codex_work`.

### Итог

Все подтверждённые старые объекты Hermes / Malyarka теперь находятся в карантине.

Удалений, распаковки архивов, чтения `.env`, поиска токенов, запуска старого Hermes, запуска Telegram-бота и изменений Google Drive не было.
