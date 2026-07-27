# BATCH_057_SAFE_LOCAL_ARCHIVE_IMPORT_PLAN

## Статус

Выполнено.

## Что добавлено

- `docs\ARCHIVE_IMPORT_PLAN.md`

## Главные правила

- `«Гермес Клин».zip [архив]` и `[архив] архивный zip-файл` не являются рабочей правдой.
- Архивы не распаковывались.
- Содержимое архивов не читалось.
- Старые проекты не читались.
- Автоматический импорт в Hermes-Clean запрещён.

## Gates

- `APPROVE_ARCHIVE_UNPACK`
- `APPROVE_MALYARKA_ARCHIVE_IMPORT`
- `APPROVE_REAL_ORDER_ACCESS`
- `APPROVE_SECRET_SETUP`

## Безопасность

Не читались и не менялись:

- архивы;
- старые проекты;
- реальные заказы;
- клиентские документы;
- `.env`;
- токены;
- ключи;
- Google Drive;
- live Telegram.

## Проверки

- `scripts\hermes.cmd project-audit` — OK, 14 checks.
- `scripts\hermes.cmd smoke` — OK, 20 проверок.
- `scripts\run_tests.cmd` — OK, 104 теста.
