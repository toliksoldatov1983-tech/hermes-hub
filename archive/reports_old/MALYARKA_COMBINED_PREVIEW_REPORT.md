# BATCH_039_SAFE_LOCAL_MALYARKA_COMBINED_PREVIEW

## Статус

Выполнено.

## Что добавлено

- `src\hermes_modules\malyarka\combined_preview.py`
- CLI-команда `scripts\hermes.cmd malyarka-combined`
- `tests\test_malyarka_combined_preview.py`
- `docs\MALYARKA_COMBINED_PREVIEW.md`

## Безопасность

Команда использует только:

- встроенный synthetic пример по умолчанию;
- или текст, явно переданный пользователем в CLI.

Команда не читает реальные заказы, клиентские документы, старые архивы, Google Drive, `.env`, токены или ключи.

## Проверки

- `scripts\hermes.cmd malyarka-combined` — OK.
- `scripts\hermes.cmd malyarka-combined "paint | 2 | bucket"` — OK.
- `scripts\hermes.cmd help-local` — OK.
- `scripts\hermes.cmd smoke` — OK, 17 проверок.
- `scripts\run_tests.cmd` — OK, 95 тестов.
