# MALYARKA_TWO_LAYERS_READONLY_AUDIT

Дата: 2026-07-02

Режим: read-only аудит. Старые проекты, архивы, Google Drive, `.env`, токены, ключи, реальные заказы и live Telegram не трогались. State-файлы `NEXT_TASK.md`, `CURRENT_STATE.md`, `DONE.md`, `REPORT_TO_USER.md` не редактировались.

## КРАТКИЙ ВЫВОД

В Hermes-Clean сейчас есть два Malyarka-связанных слоя:

1. `src\hermes_clean` — изолированный hardening/reference слой, появившийся после BATCH_063C и последующих RC2-задач. Он содержит dict-based обработку заказов, валидацию, фикстуры, dispute resolver, export gate, state machine, preview, Telegram flow, task queue, memory sync, secret guard и GDrive freeze stub.
2. `src\hermes_modules\malyarka` — основной модуль Malyarka в архитектуре Hermes-Clean. Он подключён к CLI-командам, dashboard, daily-report, smoke и project-audit как рабочий модуль `hermes_modules.malyarka`.

Фактическая связка между ними уже есть: `src\hermes_modules\malyarka\hardening_adapter.py` импортирует `hermes_clean` и даёт совместимость для validation/export hardening.

Рекомендация: вариант A + B. Оставить `src\hermes_modules\malyarka` будущим рабочим слоем, а `src\hermes_clean` считать reference/compatibility слоем. Полезное переносить только отдельным будущим batch, через адаптацию форматов, без прямого слияния папок.

## СЛОЙ 1: src\hermes_clean

- назначение:
  Изолированная локальная safe/dry-run песочница и hardening/reference слой после BATCH_063C/RC2. Работает в основном с dict-based order results и размерами.

- ключевые файлы:
  - `validation.py` — валидация dict-заказов, confirmed/disputed rows, дубликаты, площадь.
  - `fixtures.py` — синтетические фикстуры BATCH_063C.
  - `dispute_resolver.py` — resolver и suggested questions.
  - `export_gate.py` — безопасная модель экспорта и `ExportBlockedError`.
  - `state_machine.py` — локальная машина состояний заказа.
  - `preview_generator.py` — markdown preview и синтетическое ценообразование по размерам.
  - `telegram_flow.py` и `telegram_flow_runner.py` — локальный Telegram dialog flow.
  - `malyarka_dialog_commands.py` — operator-style dry-run команды Malyarka.
  - `malyarka_transcript_report.py` — markdown transcript reports.
  - `memory_sync.py`, `secret_guard.py`, `gdrive_stub.py`, `task_queue.py` — общая RC2 safety/queue/memory/freeze инфраструктура.

- тесты:
  Прямо импортируют `hermes_clean`:
  - `test_validation.py`
  - `test_fixtures.py`
  - `test_dispute_resolver.py`
  - `test_export_gate.py`
  - `test_corel_export_model.py`
  - `test_state_machine.py`
  - `test_preview_report.py`
  - `test_telegram_flow.py`
  - `test_telegram_flow_runner.py`
  - `test_task_queue.py`
  - `test_memory_sync.py`
  - `test_secret_guard.py`
  - `test_gdrive_freeze.py`
  - `test_malyarka_dialog_commands.py`
  - `test_malyarka_transcript_report.py`

- команды:
  Прямо используются в CLI:
  - `scripts\hermes.cmd telegram-flow` -> `hermes_clean.telegram_flow_runner`
  - `scripts\hermes.cmd malyarka-dialog` -> `hermes_clean.malyarka_dialog_commands`
  - `scripts\hermes.cmd malyarka-transcript` -> `hermes_clean.malyarka_transcript_report`

- что содержит из Malyarka:
  - BATCH_063C hardening: validation, fixtures, dispute resolver, export gate.
  - локальный диалоговый слой по размерам/строкам;
  - preview/export safety для dict order results;
  - synthetic-only тестовую механику.

## СЛОЙ 2: src\hermes_modules\malyarka

- назначение:
  Основной бизнес-модуль Malyarka внутри архитектуры Hermes-Clean. Работает с контрактами `MalyarkaOrder`, `MalyarkaOrderRow`, `ParserContract` и форматом `item | quantity | unit`.

- ключевые файлы:
  - `order_contract.py` — `MalyarkaOrder`, `MalyarkaOrderRow`, `RowStatus`.
  - `parser_contract.py` — parser для `item | quantity | unit`.
  - `preview_contract.py` — preview по order contract.
  - `dispute_contract.py` — blocking disputes.
  - `resolution_contract.py` — dry-run замена первой disputed row.
  - `export_contract.py` — export blocked until confirmed/approved.
  - `fixtures.py` — 9 synthetic fixtures для основного модуля.
  - `dispute_classifier.py` — классификация спорных строк.
  - `combined_preview.py` — parse + disputes + pricing + export gate.
  - `schema_contract.py`, `export_preview.py`, `synthetic_pricing.py`.
  - `workflow.py`, `demo.py`, `status.py`.
  - `hardening_adapter.py` — мост к `hermes_clean`.

- тесты:
  Прямо импортирует основной модуль:
  - `test_malyarka_hardening_adapter.py`

  Косвенно основной модуль проверяется через `hermes_core` smoke/dashboard/CLI тесты и команды, потому что `hermes_core.cli`, `hermes_core.smoke`, `hermes_core.dashboard`, `hermes_core.daily_report`, `hermes_core.telegram.command_router` импортируют `hermes_modules.malyarka`.

- команды:
  Прямо используются в CLI:
  - `scripts\hermes.cmd malyarka-preview`
  - `scripts\hermes.cmd malyarka-fixtures`
  - `scripts\hermes.cmd malyarka-resolve`
  - `scripts\hermes.cmd malyarka-workflow`
  - `scripts\hermes.cmd malyarka-status`
  - `scripts\hermes.cmd malyarka-schema`
  - `scripts\hermes.cmd malyarka-demo`
  - `scripts\hermes.cmd malyarka-pricing`
  - `scripts\hermes.cmd malyarka-disputes`
  - `scripts\hermes.cmd malyarka-combined`

- что содержит из Malyarka:
  - основной parser/preview/disputes/export workflow;
  - synthetic fixtures;
  - модульный status report;
  - schema/export preview;
  - synthetic pricing;
  - combined preview;
  - bridge к hardening через `hardening_adapter.py`.

## ДУБЛИ

- validation:
  - `src\hermes_clean\validation.py` — полноценная dict-based валидация.
  - `src\hermes_modules\malyarka` отдельного `validation.py` не имеет; часть проверок встроена в `parser_contract.py`, `dispute_contract.py`, `export_contract.py`.
  - Дублирование не прямое, но смысловое: оба слоя решают валидность строк/заказа разными моделями данных.

- fixtures:
  - `src\hermes_clean\fixtures.py` — BATCH_063C dict-based fixtures.
  - `src\hermes_modules\malyarka\fixtures.py` — 9 fixtures для `item | quantity | unit`.
  - Дублирование прямое по назначению, но форматы разные.

- dispute resolver:
  - `src\hermes_clean\dispute_resolver.py` — отдельный resolver + suggested questions.
  - `src\hermes_modules\malyarka\dispute_classifier.py`, `dispute_contract.py`, `resolution_contract.py` — классификация, блокировка, dry-run replacement.
  - Дублирование смысловое, не API-совместимое.

- export gate:
  - `src\hermes_clean\export_gate.py` — `build_export_model`, `ExportBlockedError`.
  - `src\hermes_modules\malyarka\export_contract.py`, `export_preview.py` — export blocked until confirmed, preview schema.
  - `hardening_adapter.py` уже соединяет export hardening из `hermes_clean` с модулем Malyarka.

- telegram dry-run scenarios:
  - `src\hermes_clean\telegram_flow.py`, `telegram_flow_runner.py`, `malyarka_dialog_commands.py` — локальный Malyarka диалог.
  - `src\hermes_core\telegram\command_router.py`, `scenarios.py` — общий Telegram dry-run роутер, который использует `hermes_modules.malyarka`.
  - Дублирование частичное: один слой моделирует Malyarka dialog flow, другой общий Telegram command router.

## РАЗЛИЧИЯ

- `hermes_clean`:
  - dict-based данные;
  - размеры и расчёты площади;
  - RC2 safety/reference layer;
  - больше общих подсистем: queue, memory, secret guard, gdrive stub;
  - много прямых unit-тестов;
  - не является основным модулем в архитектурных docs.

- `hermes_modules.malyarka`:
  - typed contracts: `MalyarkaOrder`, `MalyarkaOrderRow`;
  - формат `item | quantity | unit`;
  - подключён к Hermes core как бизнес-модуль;
  - используется dashboard/daily/smoke/CLI/Telegram router;
  - имеет меньше прямых unit-тестов, но больше runtime-подключений;
  - содержит adapter к `hermes_clean`.

## ЧТО ПОДКЛЮЧЕНО К КОМАНДАМ

- `scripts\hermes.cmd` запускает `python -m hermes_core ...`; основная маршрутизация в `src\hermes_core\cli.py`.

- Команды, использующие `hermes_modules.malyarka`:
  - `malyarka-preview`
  - `malyarka-fixtures`
  - `malyarka-resolve`
  - `malyarka-workflow`
  - `malyarka-status`
  - `malyarka-schema`
  - `malyarka-demo`
  - `malyarka-pricing`
  - `malyarka-disputes`
  - `malyarka-combined`
  - также Telegram `/malyarka`, `/malyarka-combined`, `/order`, `/disputes`, `/fix` через `hermes_core.telegram.command_router`.

- Команды, использующие `hermes_clean`:
  - `telegram-flow`
  - `malyarka-dialog`
  - `malyarka-transcript`
  - косвенно через `hermes_modules.malyarka.hardening_adapter`.

## ЧТО ПОДКЛЮЧЕНО К DASHBOARD / AUDIT / SMOKE

- dashboard:
  - `src\hermes_core\dashboard.py` использует `hermes_modules.malyarka.demo`, `fixtures`, `parser_contract`, `export_contract`.
  - `hermes_clean` напрямую dashboard не использует.

- daily-report:
  - `src\hermes_core\daily_report.py` использует `hermes_modules.malyarka.combined_preview`, `demo`.

- project-audit:
  - `src\hermes_core\project_audit.py` проверяет существование `src\hermes_modules\malyarka`.
  - `src\hermes_clean` как отдельный обязательный слой в project-audit не проверяется.

- smoke:
  - `src\hermes_core\smoke.py` использует оба слоя.
  - `hermes_modules.malyarka`: preview, fixtures, schema, pricing, disputes, combined, demo.
  - `hermes_clean`: telegram-flow, malyarka-dialog, malyarka-transcript.

- release-checklist:
  - `src\hermes_core\release_checklist.py` описывает Malyarka как synthetic/manual module, но не фиксирует `hermes_clean` как основной Malyarka слой.

## РИСКИ

- Два слоя имеют разные модели данных. Прямой перенос кода может сломать контракты.
- Название `hermes_clean` звучит как главный проект, но фактически в архитектуре Hermes-Clean основным модулем Malyarka является `hermes_modules.malyarka`.
- `hermes_clean` покрыт большим числом тестов, но не весь подключён к CLI/dashboard/audit.
- `hermes_modules.malyarka` подключён к CLI/dashboard/smoke, но часть hardening-функций держит через adapter к `hermes_clean`.
- Фикстуры и dispute/export логика существуют в двух разных форматах; это может путать будущую разработку.
- Если удалить или резко отключить `hermes_clean`, сломаются `hardening_adapter`, `telegram-flow`, `malyarka-dialog`, `malyarka-transcript` и связанные тесты.
- Если сделать `hermes_clean` основным модулем, придётся переписать текущие Hermes core CLI/dashboard/smoke/telegram-router связи.

## РЕКОМЕНДАЦИЯ

Выбрать вариант A + B:

1. Оставить `src\hermes_modules\malyarka` как будущий рабочий Malyarka-слой.
2. Оставить `src\hermes_clean` как reference/compatibility hardening слой, не удалять и не переименовывать сейчас.
3. Подготовить отдельный будущий batch:
   `BATCH_087_PLAN_MALYARKA_LAYER_RECONCILIATION`
4. В этом batch только спланировать перенос полезных идей из `hermes_clean` в `hermes_modules.malyarka`:
   - validation rules;
   - suggested dispute questions;
   - stricter export gate source policy;
   - selected fixture ideas;
   - selected dialog/transcript behavior.
5. Не делать прямой перенос файлов. Делать только адаптацию под `MalyarkaOrder` и текущий CLI/dashboard/smoke.

## ЧТО ПЕРЕДАТЬ CHATGPT

Короткая передача:

```text
В Hermes-Clean есть два Malyarka слоя.

1. src/hermes_clean — hardening/reference слой после BATCH_063C. Он содержит validation, fixtures, dispute_resolver, export_gate, state_machine, preview_generator, telegram_flow, task_queue, memory_sync, secret_guard, gdrive_stub. Он dict-based и размерный.

2. src/hermes_modules/malyarka — основной рабочий модуль Hermes-Clean. Он подключён к CLI, dashboard, daily-report, smoke, project-audit и Telegram router. Он contract-based: MalyarkaOrder, MalyarkaOrderRow, ParserContract, формат item | quantity | unit.

Связь уже есть: src/hermes_modules/malyarka/hardening_adapter.py импортирует hermes_clean.

Риск: прямое слияние опасно, потому что форматы данных разные.

Рекомендация: оставить hermes_modules.malyarka рабочим слоем, hermes_clean держать как reference/compatibility. Следующий безопасный шаг — BATCH_087_PLAN_MALYARKA_LAYER_RECONCILIATION: только план адаптации полезного из hermes_clean в hermes_modules.malyarka, без переноса файлов и без реальных заказов.
```
