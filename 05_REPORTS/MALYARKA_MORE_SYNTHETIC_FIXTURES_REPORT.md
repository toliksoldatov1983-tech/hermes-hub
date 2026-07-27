# MALYARKA_MORE_SYNTHETIC_FIXTURES_REPORT

## Блок

BATCH_027H_MALYARKA_MORE_SYNTHETIC_FIXTURES

## Что создано

Расширены synthetic fixtures Malyarka.

Добавлены cases:

- unknown synthetic price;
- empty item;
- empty unit;
- mixed valid/disputed rows.

## Ограничения

Fixtures остаются полностью synthetic. Реальные заказы, цены, клиенты, Excel, Google Drive, старые архивы и секреты не читались.

## Проверки

- `scripts\hermes.cmd malyarka-fixtures` — OK;
- `scripts\run_tests.cmd` — OK.

## Следующий крупный блок

BATCH_027I_INCLUDE_MALYARKA_IN_SMOKE
