# BATCH_063A_LOCATION_VERIFY_REPORT

Дата: 2026-07-01
Цель: Проверить, где фактически выполнен BATCH_063_SAFE_LOCAL_MALYARKA_FULL_HARDENING_PACK.

---

## ГДЕ ВЫПОЛНЕН BATCH_063

**BATCH_063 выполнен в: `[удалённый архив]`**

**BATCH_063 НЕ выполнен в: `C:\Users\user\Desktop\Hermes-Clean`**

Рабочим каталогом при выполнении был `E:\«Гермес Клин»`. Команды запускались с `PYTHONPATH=projects/malyarka-clean/src;projects/malyarka-clean/tools`.

---

## ПРОВЕРКА СУЩЕСТВОВАНИЯ ДИРЕКТОРИЙ

| Путь | Существует? |
|------|-------------|
| `C:\Users\user\Desktop\Hermes-Clean\src\hermes_modules\malyarka` | ✅ ДА — 16 файлов, СВОЯ архитектура |
| `C:\Users\user\Desktop\Hermes-Clean\src\malyarka_clean_core` | ❌ НЕТ |
| `[удалённый архив]` | ✅ ДА — 11 файлов, архитектура BATCH_063 |

---

## ГДЕ РЕАЛЬНО НАХОДЯТСЯ ФАЙЛЫ BATCH_063

| Файл | Desktop Hermes-Clean | E:\«Гермес Клин» | Примечание |
|------|---------------------|---------------|------------|
| `validation.py` | ❌ НЕТ | ✅ `malyarka_clean_core/validation.py` | 170 строк |
| `fixtures.py` | ✅ СВОЯ версия | ✅ `malyarka_clean_core/fixtures.py` | **Абсолютно разное содержимое!** |
| `dispute_resolver.py` | ❌ НЕТ | ✅ `malyarka_clean_core/dispute_resolver.py` | 210 строк |
| `corel_export_model.py` | ❌ НЕТ | ✅ `malyarka_clean_core/corel_export_model.py` | С ExportBlockedError |
| `scenarios.py` | ✅ СВОЯ версия | ✅ `malyarka_clean_telegram/scenarios.py` | **Абсолютно разное содержимое!** |
| `scripts/hermes.cmd` | ✅ СВОЯ версия | ✅ `scripts/hermes.cmd` | **Разный dispatcher** |
| `tools/run_fixtures.py` | ❌ НЕТ | ✅ `tools/run_fixtures.py` | |
| `tools/run_disputes.py` | ❌ НЕТ | ✅ `tools/run_disputes.py` | |
| `tools/run_combined.py` | ❌ НЕТ | ✅ `tools/run_combined.py` | |
| `tools/run_telegram_scenarios.py` | ❌ НЕТ | ✅ `tools/run_telegram_scenarios.py` | |
| `tools/run_project_audit.py` | ❌ НЕТ | ✅ `tools/run_project_audit.py` | |
| `tests/test_validation.py` | ❌ НЕТ | ✅ | 14 тестов |
| `tests/test_fixtures.py` | ❌ НЕТ | ✅ | 11 тестов |
| `tests/test_dispute_resolver.py` | ❌ НЕТ | ✅ | 8 тестов |
| `tests/test_export_gate.py` | ❌ НЕТ | ✅ | 7 тестов |
| `tests/test_telegram_scenarios.py` | ❌ НЕТ | ✅ | 14 тестов |

---

## ПРЕДУПРЕЖДЕНИЕ ПО fixtures.py

**Файл `fixtures.py` существует в ОБОИХ проектах, но с принципиально разным содержимым.**

### Desktop Hermes-Clean (`src/hermes_modules/malyarka/fixtures.py`):
- Архитектура: `MalyarkaFixture` dataclass с полями `name`, `source_text`, `expected_final_ready`, `purpose`
- Формат: `"wall paint | 2 | bucket"` (item | quantity | unit)
- Импортирует: `dispute_contract`, `export_contract`, `parser_contract`, `preview_contract`
- 9 синтетических фикстур
- Является частью СВОЕЙ архитектуры Desktop Hermes-Clean

### E:\«Гермес Клин» (`malyarka_clean_core/fixtures.py`):
- Архитектура: `FIXTURE_REGISTRY` dict с полями `id`, `label`, `raw_text`, `expected_status`, `tags`
- Формат: `"1000 400 2"` (height width quantity в мм)
- Независимый модуль (не импортирует другие контракты)
- 16 синтетических фикстур
- Является частью архитектуры BATCH_063

**Вердикт: fixtures.py НЕ был изменён — в каждом проекте своя независимая версия.**

---

## ТЕСТЫ

### Тесты, реально запускавшиеся при BATCH_063:

```text
Рабочий каталог: E:\«Гермес Клин»
Команда: PYTHONPATH="projects/malyarka-clean/src;projects/malyarka-clean/tools" python -m pytest projects/malyarka-clean/tests/ -q
Результат: 121 passed
```

### Какие тесты были запущены (все в `[удалённый архив]`):

| Файл | Тестов |
|------|--------|
| test_first_local_parser.py | 8 |
| test_area_calculator.py | 5 |
| test_order_result.py | 5 |
| test_corel_export_model.py | 6 |
| test_excel_corel_export.py | 6 |
| test_order_pipeline_smoke.py | 4 |
| test_telegram_adapter.py | 6 |
| test_telegram_pre_token_readiness.py | 8 |
| test_telegram_config_check.py | 7 |
| test_telegram_skeleton_check_command.py | 6 |
| test_single_local_runner.py | 4 |
| **test_validation.py** | **14** (Новый BATCH_063) |
| **test_fixtures.py** | **11** (Новый BATCH_063) |
| **test_dispute_resolver.py** | **8** (Новый BATCH_063) |
| **test_export_gate.py** | **7** (Новый BATCH_063) |
| **test_telegram_scenarios.py** | **14** (Новый BATCH_063) |
| **ВСЕГО** | **121** |

### Тесты в Desktop Hermes-Clean (`C:\Users\user\Desktop\Hermes-Clean\tests\`):
- Своя экосистема тестов (50+ файлов)
- НЕ содержат test_validation.py, test_export_gate.py
- Имеют свои test_malyarka_fixtures.py, test_malyarka_resolution.py и т.д.

---

## ВЕРДИКТ

**BATCH_063 НЕЛЬЗЯ считать частью Hermes-Clean (`C:\Users\user\Desktop\Hermes-Clean`).**

Причины:
1. Все новые файлы (validation.py, dispute_resolver.py, ExportBlockedError, run_fixtures.py и др.) созданы только в `[удалённый архив]`, но отсутствуют в Desktop Hermes-Clean.
2. Desktop Hermes-Clean имеет свою параллельную архитектуру Malyarka (другие имена модулей, другие контракты, другой формат данных).
3. `fixtures.py` и `scenarios.py` существуют в обоих проектах, но с принципиально разным содержимым — это не «изменённые» файлы, а независимые реализации.
4. Тесты BATCH_063 запускались из `E:\«Гермес Клин»`, а не из Desktop.
5. CLI-команды (`hermes.cmd malyarka-fixtures` и др.) в Desktop используют другой dispatcher и не найдут модули BATCH_063.

---

## РИСКИ

1. **Двойная кодовая база**: Desktop Hermes-Clean и E:\«Гермес Клин» — два независимых проекта Malyarka. Риск рассинхрона и путаницы.
2. **Разные форматы данных**: Desktop — `"item | quantity | unit"`, E-drive — `"height width quantity mm"`. Прямой перенос кода невозможен без адаптации.
3. **Разные контракты**: Desktop использует `ParserContract`, `ExportContract`, `DisputeContract`; E-drive — `build_order_result`, `build_corel_export_model`, `DisputeResolver`.
4. **E:\«Гермес Клин» содержит server staging и архивные данные** — частично пересекается с запретными зонами (хотя BATCH_063 их не трогал).

---

## ЧТО НУЖНО СДЕЛАТЬ ДАЛЬШЕ

BATCH_063B_PLAN_SAFE_PORT_MALYARKA_HARDENING_TO_HERMES_CLEAN:

Подготовить план безопасного переноса полезных результатов BATCH_063
из `[удалённый архив]` в `C:\Users\user\Desktop\Hermes-Clean`,
учитывая различия в архитектуре и контрактах.

Без автоматического копирования, без импорта старого проекта и без реальных заказов.
