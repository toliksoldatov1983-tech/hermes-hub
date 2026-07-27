# BATCH_051_SAFE_LOCAL_PROJECT_AUDIT_COMMAND

## Статус

Выполнено.

## Что добавлено

- `src\hermes_core\project_audit.py`
- CLI-команда `scripts\hermes.cmd project-audit`
- `tests\test_project_audit.py`
- `docs\LOCAL_PROJECT_AUDIT.md`

## Безопасность

Project audit проверяет только локальные paths и runtime flags.

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

- `scripts\hermes.cmd project-audit` — OK, 12 checks, 0 failed.
- `scripts\hermes.cmd help-local` — OK.
- `scripts\hermes.cmd smoke` — OK, 20 проверок.
- `scripts\run_tests.cmd` — OK, 103 теста.
