# Краткое резюме плана fake adapter / test double

Дата: 2026-06-15

## Суть

Fake adapter нужен только как будущий локальный test double для contract tests Hermes adapter.

Он не является live Hermes adapter и не подключается к Telegram.

## Что fake adapter не делает

Fake adapter не должен:

* читать token;
* читать `.env`;
* читать `config.py`;
* импортировать live bot modules;
* запускать polling / webhook / subprocess / API;
* менять существующий серверный бот;
* создавать файлы;
* менять цены, правила или базу;
* трогать реальные заказы.

## Fake scenarios

Нужны сценарии:

* safe allowed action;
* forbidden action;
* unknown action;
* empty output;
* missing required fields;
* wrong field types;
* unsafe diagnostics;
* `fallback_required=true`;
* adapter off by default;
* feature flags blocking export/admin/write actions.

## Fake outputs

Нужны формы:

* valid output;
* blocked output;
* unsafe output;
* malformed output;
* fallback output.

## Главное правило

Fake adapter помогает проверить contract tests без live-бота и без side effects.

Любое реальное действие должно быть заблокировано или превращено в dry-run draft / explanation / suggested next step.

## Следующий безопасный шаг

Серия 187-190 — Реализация локального fake adapter и focused contract tests

Техническое имя:

`BATCH_SERIES_187_190_HERMES_ADAPTER_FAKE_ADAPTER_TEST_DOUBLE_IMPLEMENTATION`

Только после отдельного разрешения пользователя.
