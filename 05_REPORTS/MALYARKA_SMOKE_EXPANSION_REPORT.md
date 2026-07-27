# MALYARKA_SMOKE_EXPANSION_REPORT

## Блок

BATCH_027I_INCLUDE_MALYARKA_IN_SMOKE

## Что создано

Расширен общий локальный smoke-test Hermes-Clean.

Добавлены проверки:

- `malyarka-fixtures`;
- `malyarka-schema`;
- `malyarka-pricing`;
- `malyarka-demo`.

## Ограничения

Smoke остаётся локальным и synthetic. Реальные заказы, цены, клиенты, Excel, Google Drive, старые архивы и секреты не читались.

## Проверки

- `scripts\hermes.cmd smoke` — OK;
- `scripts\run_tests.cmd` — OK.

## Следующий крупный блок

BATCH_027J_MALYARKA_LOCAL_ONLY_SUMMARY
