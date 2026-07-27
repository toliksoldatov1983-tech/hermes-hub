# MALYARKA_SYNTHETIC_PRICING_REPORT

## Блок

BATCH_027G_MALYARKA_SYNTHETIC_PRICING_AND_METADATA

## Что создано

Добавлены synthetic pricing и metadata для Malyarka:

- `src/hermes_modules/malyarka/synthetic_pricing.py`;
- расширена schema в `schema_contract.py`;
- расширен export preview в `export_preview.py`;
- CLI-команда `scripts\hermes.cmd malyarka-pricing`;
- тесты `tests/test_malyarka_synthetic_pricing.py`;
- документация `docs/MALYARKA_SYNTHETIC_PRICING.md`.

## Что важно

Все цены и metadata синтетические. `can_use_as_real_price=False`.

## Ограничения

Реальные цены, реальные клиенты, реальные заказы, Excel, Google Drive, старые архивы, токены, ключи и `.env` не читались.

## Проверки

- `scripts\hermes.cmd malyarka-pricing` — OK;
- `scripts\run_tests.cmd` — OK.

## Следующий крупный блок

BATCH_027H_MALYARKA_MORE_SYNTHETIC_FIXTURES
