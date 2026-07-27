# GOOGLE_DRIVE_LOW_MOVE_REPORT

## Блок

BATCH_009_MOVE_LOW_GOOGLE_DRIVE_HERMES_DOCS_TO_ARCHIVE

## Цель

Перенести только 12 найденных LOW-документов Hermes в `HERMES_OLD_ARCHIVE`.

## Целевая папка

`HERMES_OLD_ARCHIVE`

ID: `1gPcOVORzP3zrFP0R07RVnxz3An2oJYP0`

Статус: папка существует, проверена по метаданным Google Drive.

## Предварительная проверка

Все 12 LOW-документов из манифеста были проверены по метаданным:

- имена совпадают с разрешённым списком;
- MIME/type: `application/vnd.google-apps.document`;
- это не Google Sheets;
- это не Apps Script;
- это не Malyarka-документы;
- это не дубликаты из MEDIUM-группы;
- исходный родитель на момент проверки: My Drive root, ID `0AFVq6WDHzvNUUk9PVA`.

## Результат переноса

Перенос не выполнен.

Первая попытка переместить `HERMES_NEXT_TASK_BLOCKS.md` завершилась ошибкой Google Drive:

`403 appNotAuthorizedToFile`

Текст причины:

`The user has not granted the app 77377267392 write access to the file 1wYMfC9NhkGT8m1KRDjnBfmLOaFqtCzLB2DcHPRUgC2E.`

После этой ошибки остальные 11 файлов не переносились, чтобы не выполнять повторные write-операции без устранения причины доступа.

## Перенесено

0 файлов.

## Пропущено

| Имя | ID | Причина |
|---|---|---|
| HERMES_NEXT_TASK_BLOCKS.md | 1wYMfC9NhkGT8m1KRDjnBfmLOaFqtCzLB2DcHPRUgC2E | Google Drive отказал в write-доступе для приложения Codex |
| TELEGRAM_SETUP_RU.md | 1e8KmsX3eExDCMemIVLUGxpRZbV2tNB8EGXvhlys5Xl8 | перенос не выполнялся после отказа на первом файле |
| HERMES_SEVEN_BLOCK_EXECUTION_PLAN.md | 1dKn5-xd5Wt2uR7nP4nzQaDAyy1hCJvB7ey7PymI9xbg | перенос не выполнялся после отказа на первом файле |
| QUICK_START_RU.md | 19zow6t4hBMSShYPqfBWEWBMDAI5eXauX1wg4hmd89B0 | перенос не выполнялся после отказа на первом файле |
| daily_agent_log.md | 1ZFR6zQdWXDUOJtI8fsc5UiFpymEIuIHJmcyUdLRXQ70 | перенос не выполнялся после отказа на первом файле |
| 2026-06-29.md | 1MHqQIuFO_YAxgRRHMEU9hKMJsU52y2mxVKqCqYpEqx0 | перенос не выполнялся после отказа на первом файле |
| HERMES_DAILY_AGENT_SAFETY_RULES.md | 1E_rr9eTnKRrtVqC6VWXW1ahCfUTP0L1dkbJD61zsQ_4 | перенос не выполнялся после отказа на первом файле |
| BACKUP_AND_RESTORE_RU.md | 115NVv0INKfDjJ4H3-sNj2eKZHIu68rTEavohliynGew | перенос не выполнялся после отказа на первом файле |
| AI_AGENT_RESTORE_INSTRUCTION_RU.md | 1YEFzkvPGj_aMqVRbbWLHfB3DUhHfIz_-N0BPBhrCNZ8 | перенос не выполнялся после отказа на первом файле |
| HERMES_DAILY_AGENT_PLAN.md | 1JwMz5L7emvPyIr5uU8bEIQr5TXMHcCOCETJkvLvrsDQ | перенос не выполнялся после отказа на первом файле |
| HERMES_PRICE_RULES.md | 16qqyHBqN2yPGEF_V2QlrW4217v-uBG_Rtd5PRCykD5Y | перенос не выполнялся после отказа на первом файле |
| proposal-izmenit-cenu-moderna-500000.md | 1e8Br_2R3ATDML8YhbxTdOuj-Y0dFtg8JJDfqxyjaYsI | перенос не выполнялся после отказа на первом файле |

## Проверка после отказа

`HERMES_NEXT_TASK_BLOCKS.md` после отказа всё ещё имеет родителя My Drive root `0AFVq6WDHzvNUUk9PVA`.

Это означает, что первая попытка не переместила файл.

## Что не трогалось

- Malyarka-документы;
- Google Sheets;
- Apps Script;
- неизвестные файлы;
- реальные заказы;
- клиентские документы;
- токены;
- ключи;
- доступы;
- права доступа.

## Запреты соблюдены

- Файлы не удалялись.
- Файлы не переименовывались.
- Права доступа не менялись.
- Содержимое документов не открывалось.
- Malyarka / Sheets / Apps Script не трогались.

## Следующий шаг

Нужно отдельно решить вопрос write-доступа приложения Codex к этим файлам Google Drive или выполнить перенос вручную в интерфейсе Google Drive.

## BATCH_009B — диагностика write-доступа

Перенос повторно не выполнялся.

Подтверждена причина блокировки: `403 appNotAuthorizedToFile`.

Вероятная причина: Google Drive connector Codex может читать метаданные и создавать собственные объекты, но не имеет write-доступа к старым существующим файлам, которые не были явно авторизованы для изменения этим приложением.

Созданы:

- `05_REPORTS/GOOGLE_DRIVE_WRITE_ACCESS_DIAGNOSTIC.md`;
- `05_REPORTS/GOOGLE_DRIVE_MANUAL_MOVE_LIST_LOW.md`.

Требуется решение пользователя: переподключить Google Drive с нужными правами, вручную перенести 12 LOW-документов или оставить Google Drive как есть.
