# BATCH_035_SAFE_LOCAL_MALYARKA_NEXT_LAYER

## Статус

Выполнено.

## Что добавлено

- `src\hermes_modules\malyarka\dispute_classifier.py`
- `tests\test_malyarka_dispute_classifier.py`
- `docs\MALYARKA_DISPUTE_CLASSIFICATION.md`
- CLI-команда `scripts\hermes.cmd malyarka-disputes`
- `05_REPORTS\MALYARKA_DISPUTE_CLASSIFICATION_REPORT.md`

## Что делает слой

Классифицирует спорные строки Malyarka на синтетических fixtures:

- `FORMAT_ERROR`
- `MISSING_ITEM`
- `INVALID_QUANTITY`
- `MISSING_UNIT`
- `UNKNOWN_DISPUTE`

Любая спорная строка блокирует финальное действие до ручного подтверждения или исправления.

## Проверки

- `scripts\hermes.cmd malyarka-disputes` — OK.
- `scripts\hermes.cmd smoke` — OK, 16 проверок.
- `scripts\run_tests.cmd` — OK, 92 теста.

## Что не трогалось

- Реальные заказы.
- Клиентские документы.
- Старые архивы.
- Google Drive.
- Секреты.
- `.env`.
- Токены и ключи.
- Live Telegram.

## Следующий крупный блок

BATCH_036_SAFE_LOCAL_COMMAND_HELP_REFRESH.
