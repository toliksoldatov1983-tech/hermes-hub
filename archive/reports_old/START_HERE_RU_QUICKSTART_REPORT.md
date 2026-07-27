# BATCH_043_SAFE_LOCAL_START_HERE_RU_QUICKSTART

## Статус

Выполнено.

## Что обновлено

- `START_HERE.md`

## Что добавлено

- короткий русский утренний порядок запуска;
- список главных безопасных команд;
- ссылка на dashboard;
- текущий safe mode;
- список запретов без отдельного risk-control;
- указание на `NEXT_TASK.md`.

## Безопасность

Изменения только локальные внутри Hermes-Clean.

Не читались и не менялись:

- реальные заказы;
- клиентские документы;
- старые архивы;
- Google Drive;
- `.env`;
- токены;
- ключи;
- live Telegram.

## Проверки

- чтение `START_HERE.md` через PowerShell — OK.
- `scripts\hermes.cmd dashboard` — OK.
- `scripts\hermes.cmd smoke` — OK, 17 проверок.
- `scripts\run_tests.cmd` — OK, 96 тестов.
