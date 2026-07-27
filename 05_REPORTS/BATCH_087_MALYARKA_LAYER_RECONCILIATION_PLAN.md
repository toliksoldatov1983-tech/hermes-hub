# BATCH_087_MALYARKA_LAYER_RECONCILIATION_PLAN

Дата: 2026-07-02

Режим: только план. Код, тесты, CLI, dashboard, smoke, project-audit, `NEXT_TASK.md`, `CURRENT_STATE.md`, `DONE.md`, `REPORT_TO_USER.md` не менялись.

## КРАТКИЙ ВЫВОД

Будущий рабочий слой Malyarka должен оставаться в `src\hermes_modules\malyarka`.

`src\hermes_clean` нужно оставить как reference / compatibility / hardening слой. Его нельзя переносить напрямую, потому что он работает с другой моделью данных: dict-based order results, размеры, площадь и локальные RC2-механики.

Переносить нужно не файлы, а идеи и правила: validation, dispute questions, export gate source policy, отдельные fixture cases и часть dry-run dialog поведения. Всё это нужно адаптировать под `MalyarkaOrder`, `MalyarkaOrderRow` и текущий формат `item | quantity | unit`.

## ПРИНЯТОЕ НАПРАВЛЕНИЕ

Выбран вариант A + B из read-only аудита:

1. `src\hermes_modules\malyarka` — будущий основной рабочий Malyarka-модуль.
2. `src\hermes_clean` — временный compatibility/reference/hardening слой.
3. Прямое слияние запрещено.
4. Адаптация только отдельными будущими batch, с тестами и без реальных заказов.

## ЧТО СРАВНИВАЛОСЬ

Слой `src\hermes_clean`:

- `validation.py`
- `fixtures.py`
- `dispute_resolver.py`
- `export_gate.py`
- `state_machine.py`
- `preview_generator.py`
- `telegram_flow.py`
- `task_queue.py`
- `memory_sync.py`
- `secret_guard.py`
- `gdrive_stub.py`

Слой `src\hermes_modules\malyarka`:

- `order_contract.py`
- `parser_contract.py`
- `preview_contract.py`
- `dispute_contract.py`
- `resolution_contract.py`
- `dispute_classifier.py`
- `export_contract.py`
- `export_preview.py`
- `fixtures.py`
- `combined_preview.py`
- `synthetic_pricing.py`
- `schema_contract.py`
- `workflow.py`
- `demo.py`
- `status.py`
- `hardening_adapter.py`

Ключевой факт: `src\hermes_modules\malyarka\hardening_adapter.py` уже импортирует `hermes_clean` и показывает безопасную модель мостика, а не прямого слияния.

## КОНФЛИКТ ФОРМАТОВ

`hermes_clean`:

- формат: dict;
- примерная модель: `confirmed_rows`, `disputed_rows`, `height`, `width`, `quantity`, `total_area_m2`;
- логика ближе к размерному/площадному заказу;
- используется в RC2 tests, preview, state machine, Telegram dialog flow.

`hermes_modules.malyarka`:

- формат: typed dataclasses;
- модель: `MalyarkaOrder`, `MalyarkaOrderRow`, `RowStatus`;
- входной формат: `item | quantity | unit`;
- подключён к CLI, dashboard, daily-report, project-audit, smoke, Telegram router.

Безопасная адаптация:

1. Не копировать файлы из `hermes_clean` в `hermes_modules.malyarka`.
2. Для каждой идеи определить equivalent в `MalyarkaOrder`.
3. Если equivalent нет, сначала добавить контракт/тест, потом реализацию.
4. Не менять существующие CLI-команды до появления совместимых тестов.
5. Оставить `hardening_adapter.py` временным мостом до решения о финальном удалении/заморозке compatibility слоя.

## ТАБЛИЦА КОМПОНЕНТОВ

| Компонент | Где сейчас | Есть ли аналог | Решение | Приоритет | Риски |
|---|---|---|---|---|---|
| validation | `src\hermes_clean\validation.py` | Частично: `parser_contract.py`, `dispute_contract.py`, `export_contract.py`, `hardening_adapter.py` | Адаптировать правила в новый `malyarka/validation_contract.py` или расширить parser/dispute/export contracts | HIGH | Разные модели данных; нельзя переносить проверки height/width без решения о размерном формате |
| fixtures | `src\hermes_clean\fixtures.py` | Да: `src\hermes_modules\malyarka\fixtures.py` | Перенести идеи кейсов, не сами dict fixtures; добавить synthetic cases в формат `item | quantity | unit` | MEDIUM | Можно смешать размерные фикстуры с item/unit форматом |
| dispute_resolver | `src\hermes_clean\dispute_resolver.py` | Частично: `dispute_classifier.py`, `resolution_contract.py`, `dispute_contract.py` | Адаптировать suggested questions и причины споров под `MalyarkaOrderRow.dispute_reason` | HIGH | Нельзя потерять блокировку final action при спорных строках |
| export_gate | `src\hermes_clean\export_gate.py` | Да: `export_contract.py`, `export_preview.py`, `hardening_adapter.py` | Усилить source policy в основном модуле: synthetic/manual allowed, real/archive/drive blocked | HIGH | Экспорт может стать слишком permissive, если забыть source_type и approval gate |
| state_machine | `src\hermes_clean\state_machine.py` | Частично: `workflow.py` | Не переносить как файл; взять идеи статусов для будущего Malyarka workflow/state contract | MEDIUM | Может усложнить простой Malyarka workflow |
| preview | `src\hermes_clean\preview_generator.py` | Да: `preview_contract.py`, `combined_preview.py`, `synthetic_pricing.py`, `export_preview.py` | Сравнить полезные поля отчёта и адаптировать только недостающие summary/recommendation поля | MEDIUM | Размерное ценообразование не совместимо с item/unit pricing |
| telegram_flow | `src\hermes_clean\telegram_flow.py`, `telegram_flow_runner.py` | Частично: `hermes_core\telegram\command_router.py`, `scenarios.py` | Сделать bridge-план: будущий Malyarka dialog flow должен вызывать основной модуль, не reference слой | MEDIUM | Можно сломать текущие `telegram-flow`, `malyarka-dialog`, `malyarka-transcript` |
| task_queue | `src\hermes_clean\task_queue.py` | В основном Malyarka-модуле аналога нет; это общий project/runtime слой | Не переносить в Malyarka; оставить вне модуля или позже вынести в core | DO_NOT_MOVE | Malyarka не должна управлять всем Hermes |
| memory_sync | `src\hermes_clean\memory_sync.py` | В Malyarka аналога нет; это общая память/решения проекта | Не переносить в Malyarka; оставить как project/reference или позже вынести в core memory | DO_NOT_MOVE | Malyarka станет слишком большой и начнёт управлять проектом |
| secret_guard | `src\hermes_clean\secret_guard.py` | В Malyarka аналога нет; безопасность должна быть в core/safety/ai | Не переносить в Malyarka | DO_NOT_MOVE | Секреты не должны быть бизнес-логикой Malyarka |
| gdrive_stub | `src\hermes_clean\gdrive_stub.py` | В Malyarka аналога нет | Не переносить в Malyarka; Drive остаётся disabled/pending | DO_NOT_MOVE | Google Drive write заблокирован 403 и не относится к Malyarka core |

## ПЛАН БУДУЩИХ BATCH

1. `BATCH_087A_PLAN_AND_TEST_MALYARKA_VALIDATION_CONTRACT`
   - Только спроектировать и затем отдельным шагом реализовать validation contract для `MalyarkaOrder`.
   - Цель: единые правила для пустого item, пустого unit, bad quantity, negative/zero quantity, malformed row, disputed rows block final.
   - Без реальных заказов.

2. `BATCH_087B_ADAPT_DISPUTE_QUESTIONS_TO_MALYARKA_ORDER`
   - Адаптировать идеи `SUGGESTED_QUESTIONS` из `hermes_clean.dispute_resolver`.
   - Цель: question layer над `MalyarkaOrderRow.dispute_reason`.
   - Не менять live Telegram; только local dry-run.

3. `BATCH_087C_HARDEN_MALYARKA_EXPORT_SOURCE_POLICY`
   - Усилить `export_contract.py` / `export_preview.py`.
   - Добавить явную source policy: `synthetic`, `manual` allowed for preview; `real_order`, `archive`, `imported`, `google_drive`, `unknown` blocked.
   - Сохранить блокировку спорных строк.

4. `BATCH_087D_EXPAND_MALYARKA_FIXTURES_WITH_ADAPTED_CASES`
   - Перенести только идеи fixture cases, не dict-формат.
   - Добавить synthetic cases в `item | quantity | unit`: zero, malformed, missing unit, empty item, mixed valid/disputed, unknown price.

5. `BATCH_087E_PLAN_TELEGRAM_DIALOG_BRIDGE_TO_MAIN_MALYARKA`
   - Спланировать, как `telegram-flow`, `malyarka-dialog`, `malyarka-transcript` смогут использовать основной `hermes_modules.malyarka`.
   - Пока не ломать существующие команды.
   - Проверить, какие сценарии должны остаться compatibility-only.

6. `BATCH_087F_REVIEW_HARDENING_ADAPTER_AND_COMPATIBILITY_DECISION`
   - Проверить `hardening_adapter.py`.
   - Решить: оставить мост, расширить мост, или постепенно заменить его прямыми контрактами в основном модуле.
   - Не удалять `hermes_clean` без отдельного будущего решения.

7. `BATCH_087G_FINAL_LAYER_RECONCILIATION_STATUS`
   - После предыдущих шагов создать итоговый статус:
     - что адаптировано;
     - что осталось reference-only;
     - что запрещено переносить;
     - какие команды используют какой слой;
     - какие тесты закрывают основной модуль.

## ЧТО НЕ ПЕРЕНОСИТЬ

Не переносить в `src\hermes_modules\malyarka`:

- Google Drive write / move / cleanup;
- `gdrive_stub.py` как Malyarka-логику;
- работу с `.env`, токенами, ключами;
- `secret_guard.py` как часть Malyarka;
- live Telegram, polling, webhook, send message;
- внешние API;
- реальные заказы и клиентские документы;
- реальные export-файлы;
- удаление файлов;
- project-level task queue как управление всем Hermes;
- project memory / global decisions как Malyarka-логику;
- любые файлы, которые дублируют рабочую архитектуру без пользы;
- прямой dict-based код без адаптации под `MalyarkaOrder`.

## КАКИЕ ТЕСТЫ НУЖНЫ

Минимальный набор будущих тестов:

- `tests/test_malyarka_validation_contract.py`
  - valid order;
  - malformed row;
  - missing item;
  - missing unit;
  - non-numeric quantity;
  - zero/negative quantity;
  - disputed rows block final.

- `tests/test_malyarka_dispute_questions.py`
  - suggested question по missing separator;
  - suggested question по quantity;
  - suggested question по missing item/unit;
  - unknown dispute reason fallback.

- `tests/test_malyarka_export_source_policy.py`
  - synthetic/manual preview allowed;
  - real_order blocked;
  - archive/imported blocked;
  - google_drive blocked;
  - unknown blocked;
  - disputed rows blocked;
  - approval does not override forbidden sources unless explicit future gate exists.

- `tests/test_malyarka_fixture_expansion.py`
  - новые synthetic fixtures в формате `item | quantity | unit`;
  - no real orders;
  - no archive imports;
  - no external files.

- `tests/test_malyarka_dialog_bridge_plan.py` или будущий runtime test после реализации
  - dialog bridge использует `hermes_modules.malyarka`;
  - старые compatibility-команды не сломаны;
  - live Telegram не запускается.

- Обновить существующие smoke/project-audit тесты только после реализации, не в этом плановом batch.

## РИСКИ

- Прямой перенос кода из `hermes_clean` сломает форматы данных.
- Размерная логика `height/width/area` может быть неуместна в текущем item/unit Malyarka-модуле.
- Если сделать `hermes_clean` главным, придётся переписывать CLI, dashboard, smoke и Telegram router.
- Если удалить `hermes_clean`, сломаются текущие tests, `hardening_adapter`, `telegram-flow`, `malyarka-dialog`, `malyarka-transcript`.
- Если оставить оба слоя без плана, будет путаница: где настоящая Malyarka.
- Source policy для экспорта должна быть строгой, иначе можно случайно приблизиться к real order/export режиму.
- Любой будущий Telegram bridge должен оставаться dry-run до отдельного `APPROVE_TELEGRAM_LIVE`.

## RECOMMENDED FINAL ARCHITECTURE

```text
Hermes-Clean
└── src
    ├── hermes_core
    │   ├── safety
    │   ├── telegram
    │   ├── memory
    │   └── reports / CLI / smoke / dashboard
    ├── hermes_modules
    │   └── malyarka
    │       ├── order_contract.py
    │       ├── parser_contract.py
    │       ├── validation_contract.py        # future, after BATCH_087A
    │       ├── dispute_contract.py
    │       ├── dispute_questions.py          # future, after BATCH_087B
    │       ├── export_contract.py
    │       ├── export_source_policy.py       # future, after BATCH_087C
    │       ├── fixtures.py
    │       ├── combined_preview.py
    │       └── hardening_adapter.py          # temporary bridge
    └── hermes_clean
        └── reference / compatibility / RC2 hardening layer
```

Правила:

- `hermes_core` — ядро, безопасность, CLI, reports, Telegram dry-run.
- `hermes_modules\malyarka` — рабочий Malyarka-модуль.
- `hermes_clean` — временный compatibility/reference слой до отдельного решения.

## РЕКОМЕНДАЦИЯ

Начинать с `BATCH_087A_PLAN_AND_TEST_MALYARKA_VALIDATION_CONTRACT`.

Причина: validation — самый полезный и безопасный первый перенос идей. Он не требует live Telegram, Google Drive, секретов, реальных заказов и внешних API. После validation можно безопасно двигаться к dispute questions и export source policy.

## ЧТО ПЕРЕДАТЬ CHATGPT

```text
BATCH_087 выполнен как план, без изменений кода.

Решение:
- src/hermes_modules/malyarka остаётся будущим рабочим Malyarka-модулем.
- src/hermes_clean остаётся reference / compatibility / hardening слоем.
- Прямое слияние запрещено, потому что форматы разные:
  hermes_clean = dict / dimensions / area;
  hermes_modules.malyarka = MalyarkaOrder / MalyarkaOrderRow / item | quantity | unit.

Что адаптировать в будущем:
1. validation rules — HIGH;
2. dispute suggested questions — HIGH;
3. export source policy — HIGH;
4. selected fixture ideas — MEDIUM;
5. dialog bridge — MEDIUM;
6. state machine / preview ideas — MEDIUM;
7. task_queue, memory_sync, secret_guard, gdrive_stub — DO_NOT_MOVE в Malyarka.

Следующий безопасный batch:
BATCH_087A_PLAN_AND_TEST_MALYARKA_VALIDATION_CONTRACT

Он должен спланировать/подготовить validation contract для MalyarkaOrder без реальных заказов, без live Telegram, без Google Drive, без секретов и без изменения старых проектов.
```
