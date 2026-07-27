# BATCH_063B_PORT_PLAN

## Статус

BATCH_063B_PLAN_SAFE_PORT_MALYARKA_HARDENING_TO_HERMES_CLEAN выполнен.

## Цель

Закрыть главный незакрытый хвост после работы старого Hermes по BATCH_063-BATCH_072.

Нужно не копировать старый проект, а подготовить безопасный план переноса только полезных Malyarka hardening идей в Desktop Hermes-Clean.

## Источники

### Старый исполнитель

`[удалённый архив]`

Найденные safe-local результаты BATCH_063:

- `src\malyarka_clean_core\validation.py`
- `src\malyarka_clean_core\fixtures.py`
- `src\malyarka_clean_core\dispute_resolver.py`
- `src\malyarka_clean_core\corel_export_model.py`
- `src\malyarka_clean_telegram\scenarios.py`
- тесты `test_validation.py`, `test_fixtures.py`, `test_dispute_resolver.py`, `test_export_gate.py`, `test_telegram_scenarios.py`

### Новый источник правды

`C:\Users\user\Desktop\Hermes-Clean`

Актуальные Desktop-модули:

- `src\hermes_modules\malyarka\fixtures.py`
- `src\hermes_modules\malyarka\resolution_contract.py`
- `src\hermes_modules\malyarka\export_contract.py`
- `src\hermes_modules\malyarka\parser_contract.py`
- `src\hermes_modules\malyarka\combined_preview.py`
- `src\hermes_core\telegram\scenarios.py`
- `src\hermes_core\telegram\command_router.py`
- `src\hermes_core\telegram\blocked_actions.py`

## Вердикт по серии BATCH_063-BATCH_072

Серию принять как полезную safe-local работу старого Hermes.

Но:

- старый Hermes не является новым Hermes-Clean;
- старый Hermes не является источником правды;
- Desktop Hermes-Clean не считать live-ready системой;
- Desktop Hermes-Clean считать local-safe release candidate только после закрытия BATCH_063C.

## Что уже есть в Desktop Hermes-Clean

Проверено локально:

- `scripts\hermes.cmd help-local` - OK, 32 команды;
- `scripts\hermes.cmd telegram-scenarios` - OK, 18 сценариев;
- `scripts\hermes.cmd malyarka-fixtures` - OK, 9 fixtures;
- `scripts\hermes.cmd safety-audit` - OK, audit log читается.

Финальная проверка после записи task-state:

- `scripts\hermes.cmd project-audit` - OK, 25 checks, 0 failed;
- `scripts\hermes.cmd smoke` - OK, 20 checks, 0 failed;
- `scripts\run_tests.cmd` - OK, 158 тестов.

Уже есть:

- Malyarka fixtures;
- dispute classification;
- dispute replacement dry-run;
- export blocking;
- Telegram dry-run scenarios;
- safety audit log;
- AI/review mock/disabled gates.

## Главные gaps для переноса

### Gap 1. Validation module

В Desktop Hermes-Clean нет отдельного `validation.py` для Malyarka.

Нужно добавить адаптированный Desktop-модуль:

`src\hermes_modules\malyarka\validation.py`

Проверки:

- empty item;
- empty unit;
- zero quantity;
- negative quantity;
- non-numeric quantity;
- oversized quantity;
- malformed row;
- disputed rows block final action.

### Gap 2. Fixtures expansion

В Desktop сейчас 9 fixtures.

Нужно добавить минимум:

- `zero_quantity`;
- `oversized_quantity`;
- `malformed_row`;
- возможно `unsupported_format`.

Все fixtures должны оставаться synthetic.

### Gap 3. Dispute resolver questions

В Desktop есть `resolution_contract.py`, но он в основном заменяет первую disputed row.

Нужно добавить слой вопросов:

- какие строки спорные;
- что нужно уточнить;
- какой формат исправления ожидается;
- почему export всё ещё blocked.

Без интерактива, без файловой записи, без реальных заказов.

### Gap 4. Export gate source policy

В Desktop `export_contract.py` блокирует disputes и требует approval.

Нужно усилить:

- `source_type=synthetic/manual` разрешён для preview;
- `source_type=real_order` всегда blocked;
- `source_type=archive/imported` всегда blocked без отдельного future gate;
- validation failed -> blocked;
- disputed rows -> blocked.

Пока не создавать Excel.

### Gap 5. Tests

Добавить focused tests:

- `tests\test_malyarka_validation.py`;
- расширить `tests\test_malyarka_fixtures.py`;
- расширить `tests\test_malyarka_resolution.py`;
- расширить `tests\test_malyarka_contracts.py` или добавить `test_malyarka_export_gate.py`;
- при необходимости расширить Telegram dry-run tests.

## Что нельзя переносить

Не переносить:

- весь `[удалённый архив]`;
- старую структуру как новую архитектуру;
- runtime/live Telegram код;
- Excel export implementation как production path;
- любые `.env`, ключи, токены;
- реальные заказы;
- клиентские документы;
- старые архивы;
- Google Drive integration.

## План BATCH_063C

Следующий пакет:

`BATCH_063C_SAFE_PORT_MISSING_MALYARKA_HARDENING_TO_DESKTOP`

Сделать внутри Desktop Hermes-Clean:

1. Добавить `src\hermes_modules\malyarka\validation.py`.
2. Расширить `fixtures.py` недостающими synthetic cases.
3. Добавить question layer в dispute resolution.
4. Усилить export gate source policy.
5. Добавить/расширить тесты.
6. Обновить docs/reports/task-state.
7. Выполнить проверки:
   - `scripts\hermes.cmd malyarka-fixtures`;
   - `scripts\hermes.cmd malyarka-disputes`;
   - `scripts\hermes.cmd malyarka-combined`;
   - `scripts\hermes.cmd telegram-scenarios`;
   - `scripts\hermes.cmd project-audit`;
   - `scripts\hermes.cmd smoke`;
   - `scripts\run_tests.cmd`.

## Safety

Во время BATCH_063B:

- старый Hermes не изменялся;
- код из старого проекта не копировался автоматически;
- архивы не читались и не распаковывались;
- `[удалён]` не открывался;
- реальные заказы не читались;
- `.env`, токены и ключи не читались;
- Google Drive не менялся;
- live Telegram не запускался;
- внешние API не вызывались.
