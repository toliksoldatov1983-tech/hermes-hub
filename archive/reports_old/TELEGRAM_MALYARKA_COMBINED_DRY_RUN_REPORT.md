# BATCH_041_TELEGRAM_DRY_RUN_MALYARKA_COMBINED

## Статус

Выполнено.

## Что добавлено

- Telegram dry-run command `/malyarka-combined`.
- Telegram scenario `malyarka_combined_preview`.
- Dashboard section `Malyarka Combined Preview`.
- Documentation `docs\TELEGRAM_MALYARKA_COMBINED_DRY_RUN.md`.

## Безопасность

Блок работает только локально.

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

- `scripts\hermes.cmd message /malyarka-combined` — OK.
- `scripts\hermes.cmd message /malyarka-combined "paint | 2 | bucket"` — OK.
- `scripts\hermes.cmd telegram-scenarios` — OK, 5 сценариев.
- `scripts\hermes.cmd telegram-status` — OK, 8 aliases.
- `scripts\hermes.cmd dashboard` — OK.
- `scripts\hermes.cmd smoke` — OK, 17 проверок.
- `scripts\run_tests.cmd` — OK, 96 тестов.
