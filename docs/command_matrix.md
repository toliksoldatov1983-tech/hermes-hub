# Command Matrix — Hermes-Clean CLI Map

Все команды выполняются из корня проекта `C:\Users\user\Desktop\Hermes-Clean`.

---

## Тестирование

| Команда | Описание |
|---------|----------|
| `python -m pytest tests/ -v` | Запустить все 278 тестов (verbose) |
| `python -m pytest tests/ -q` | Запустить все тесты (quiet) |
| `python -m pytest tests/<file> -v` | Запустить конкретный тестовый файл |
| `python -m pytest tests/ -k "test_name"` | Запустить тест по имени |
| `python -m pytest tests/ --co` | Собрать только коллекцию (без запуска) |

---

## Сухие прогоны (Dry-run tools)

| Команда | Описание |
|---------|----------|
| `python tools/run_fixtures.py` | Прогнать все 11 фикстур через валидацию |
| `python tools/run_disputes.py` | Проверить разрешение споров (6 сценариев) |

---

## State Machine

| Команда | Описание |
|---------|----------|
| `python -c "from hermes_clean import OrderStateMachine; sm = OrderStateMachine(); print(sm.state_label)"` | Создать state machine |
| `python -c "from hermes_clean.state_machine import _ALLOWED_TRANSITIONS; print({k.name: [s.name for s in v] for k,v in _ALLOWED_TRANSITIONS.items()})"` | Показать карту переходов |

---

## Task Queue

| Команда | Описание |
|---------|----------|
| `python -c "from hermes_clean import create_default_queue; q=create_default_queue(); print(q.render_dashboard())"` | Дашборд очереди |
| `python -c "from hermes_clean import create_default_queue; q=create_default_queue(); print(q.audit_report())"` | Отчёт аудита |
| `python -c "from hermes_clean import create_default_queue; q=create_default_queue(); q.activate_next(); q.complete_current('OK'); print(q.progress)"` | Пройти 1 шаг |

---

## Telegram Dialog Flow

| Команда | Описание |
|---------|----------|
| `python -c "from hermes_clean import TelegramDialogFlow; f=TelegramDialogFlow(); f.receive_order('1000 400 2'); print(f.get_last_message())"` | Чистый заказ |
| `python -c "from hermes_clean import TelegramDialogFlow; f=TelegramDialogFlow(); f.receive_order('1000 400 2\nмусор'); f.ask_questions(); print(f.get_last_message())"` | Заказ со спорами → вопросы |
| `python -c "from hermes_clean import TelegramDialogFlow; f=TelegramDialogFlow(); f.receive_order('1000 400 2\nмусор'); f.ask_questions(); f.resolve_dispute('dispute-2',{'action':'delete'}); f.show_final_report(); print(f.get_last_message())"` | Полный цикл disputed |
| `python -c "from hermes_clean import TelegramDialogFlow; f=TelegramDialogFlow(); f.receive_order('1000 400 2'); f.show_preview(); print(f.get_last_message())"` | Preview report |

---

## Preview Report

| Команда | Описание |
|---------|----------|
| `python -c "from hermes_clean import generate_preview, preview_to_markdown; r=generate_preview({'status':'clean','confirmed_rows':[{'height':1000,'width':400,'quantity':2}],'disputed_rows':[],'total_area_m2':0.8}); print(preview_to_markdown(r))"` | Сгенерировать preview (markdown) |

---

## Memory Sync

| Команда | Описание |
|---------|----------|
| `python -c "from hermes_clean import MemorySync, Subsystem; ms=MemorySync(); ms.add_decision('arch','clean',Subsystem.MALYARKA); print(ms.render_dashboard())"` | Дашборд реестра |
| `python -c "from hermes_clean import MemorySync; ms=MemorySync(); print(ms.check_integrity().is_consistent)"` | Проверка целостности |

---

## Secret Guard

| Команда | Описание |
|---------|----------|
| `python -c "from hermes_clean import SecretGuard; g=SecretGuard(); print(g.report())"` | Отчёт о защите секретов |
| `python -c "from hermes_clean import sanitize_text; print(sanitize_text('api_key=sk-testABC...WXYZ'))"` | Зачистка текста |
| `python -c "from hermes_clean import SecretGuard; g=SecretGuard(); print(g.run_full_check())"` | Полная проверка контура |

---

## GDrive Stub

| Команда | Описание |
|---------|----------|
| `python -c "from hermes_clean import GDriveStub; s=GDriveStub(); print(GDriveStub.get_manual_instructions())"` | Инструкция по ручному размещению |
| `python -c "from hermes_clean import GDriveStub; s=GDriveStub(); s.set_manual_path('.'); print(s.check_manual_files())"` | Проверить ручную папку |

---

## Validation

| Команда | Описание |
|---------|----------|
| `python -c "from hermes_clean import validate_single_row; print(validate_single_row({'height':1000,'width':400,'quantity':2}))"` | Валидация одной строки |
| `python -c "from hermes_clean import validate_order_result; print(validate_order_result({'confirmed_rows':[{'height':1000,'width':400,'quantity':2}],'disputed_rows':[],'total_area_m2':0.8}))"` | Валидация заказа |

---

## Export Gate

| Команда | Описание |
|---------|----------|
| `python -c "from hermes_clean import build_export_model; r=build_export_model({'status':'clean','confirmed_rows':[{'height':1000,'width':400,'quantity':2}],'disputed_rows':[]}, strict=True); print(r)"` | Проверка экспорта (strict) |

---

## Фикстуры

| Команда | Описание |
|---------|----------|
| `python -c "from hermes_clean import list_fixtures; print(list_fixtures())"` | Список всех фикстур |
| `python -c "from hermes_clean import get_fixture; print(get_fixture('clean_single'))"` | Показать конкретную фикстуру |
