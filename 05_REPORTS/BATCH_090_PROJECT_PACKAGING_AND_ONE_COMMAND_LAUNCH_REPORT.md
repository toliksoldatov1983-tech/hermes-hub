# BATCH_090_PROJECT_PACKAGING_AND_ONE_COMMAND_LAUNCH — Отчёт

Дата: 2026-07-02
Исполнитель: Hermes Agent

## Краткий вывод

BATCH_090 выполнен полностью и успешно. Создана полная packaging-инфраструктура проекта, добавлены однокомандные скрипты запуска и проверки, обновлена документация. Все 309 тестов, 25/25 аудит и 23/23 smoke пройдены. Все gates безопасности сохранены.

---

## Что сделано

### БЛОК 1. PACKAGING

Созданы:
- **pyproject.toml** — полный packaging-файл с метаданными, entry point для CLI (`hermes = "hermes_core.cli:main"`), конфигурацией pytest
- **requirements.txt** — минимальные зависимости (только pytest, проект использует только stdlib)

### БЛОК 2. ONE-COMMAND LOCAL START

Создан:
- **scripts\start_local.cmd** — однокомандный запуск: refresh-all → dashboard → smoke → app-status → malyarka-status → safety-audit, с выводом доступных команд и отключённых функций

### БЛОК 3. ONE-COMMAND LOCAL CHECK

Созданы:
- **scripts\check_local.cmd** — стандартная проверка (10 шагов): audit, smoke, malyarka-status, malyarka-fixtures, malyarka-disputes, malyarka-combined, malyarka-dialog, malyarka-transcript, telegram-flow, run_tests
- **scripts\check_full.cmd** — полная проверка (27 шагов): все CLI команды, все сценарии Malyarka, Telegram, safety, dashboard, тесты

### БЛОК 4. CLI CONSISTENCY

Все 35+ CLI команд проверены и работают:
- help-local, app-status, dashboard, daily-report, project-audit, smoke — OK
- malyarka-status, malyarka-fixtures, malyarka-disputes, malyarka-combined — OK
- malyarka-dialog (clean + disputed), malyarka-transcript (clean + disputed) — OK
- telegram-flow (clean + disputed), telegram-scenarios, telegram-status — OK
- safety, safety-audit, health, status, start-summary, reports, tasks, memory — OK

### БЛОК 5. DOCUMENTATION

Обновлены:
- **START_HERE.md** — расширена информацией о новых скриптах, gates, полной проверке
- **docs\USER_RUNBOOK_RU.md** — полная русская инструкция: однокомандный запуск, все команды, режимы безопасности, что делать после перезагрузки
- Обновление README.md не потребовалось (уже содержит актуальную информацию)

### БЛОК 6. SAFETY GATES

Проверено — все gates сохранены:
- `disabled` подсистемы остаются выключенными (6 disabled)
- `.env` не найден внутри Hermes-Clean
- live Telegram не запущен
- реальные AI-провайдеры заблокированы
- Google Drive write заблокирован
- real order access заблокирован
- archive import заблокирован
- delete заблокирован

### БЛОК 7. REPORT

Создан данный отчёт. Обновлены все статусные файлы.

---

## Результаты проверок

| Проверка | Результат |
|----------|-----------|
| help-local | 35 команд, все gates видны |
| app-status | 6 enabled / 6 disabled |
| dashboard | health=OK, smoke=OK |
| daily-report | OK |
| project-audit | 25/25, 0 failed |
| smoke | 23/23, 0 failed |
| malyarka-status | 5 commands, 10 contracts, 4 gated |
| malyarka-fixtures | 12/12 fixtures OK |
| malyarka-disputes | 8 disputes, 4 categories |
| malyarka-combined | default_synthetic, OK |
| malyarka-dialog (clean) | 4 commands, export_ready=True |
| malyarka-transcript (clean) | export_ready=True |
| telegram-flow (clean) | export_ready=true, 4 steps |
| run_tests | 309 passed |

---

## Изменённые файлы

**Созданные:**
- `pyproject.toml` — packaging, entry point, pytest config
- `requirements.txt` — внешние зависимости
- `scripts\start_local.cmd` — однокомандный запуск
- `scripts\check_local.cmd` — стандартная проверка (10 шагов)
- `scripts\check_full.cmd` — полная проверка (27 шагов)
- `05_REPORTS\BATCH_090_PROJECT_PACKAGING_AND_ONE_COMMAND_LAUNCH_REPORT.md`

**Обновлённые:**
- `START_HERE.md` — информация о новых скриптах
- `docs\USER_RUNBOOK_RU.md` — полная русская инструкция
- `00_START\CURRENT_STATE.md`
- `03_TASKS\ACTIVE_BATCH.md`
- `03_TASKS\DONE.md`
- `03_TASKS\NEXT_TASK.md`
- `05_REPORTS\REPORT_TO_USER.md`

---

## Безопасность

Подтверждаю:
- `.env` не читался — внутри Hermes-Clean их нет
- реальный `.env` не создавался
- токены не читались
- ключи не читались
- Google Drive не трогался
- live Telegram не запускался
- polling/webhook не запускались
- реальные заказы не использовались
- внешние API не вызывались
- удаления не было
- src\hermes_modules\malyarka не сломан
- src\hermes_clean не удалён

---

## Риски / Хвосты

- Один из reports_count показывает 120 отчётов (много). Это не баг, а результат накопления.
- После установки pyproject.toml может потребоваться `pip install -e .` для entry point (но CLI через `python -m hermes_core` уже работает).
- scripts\check_full.cmd выполняет 27 шагов — может быть полезно сократить при ежедневном использовании.

---

## Следующий крупный шаг

```
BATCH_091_AI_PROVIDER_SECRET_GATE_SETUP
```

Настройка безопасного подключения AI-провайдеров (Gemini/DeepSeek) через approval gates. Безопасная интеграция ключей, токенов и провайдеров с сохранением всех gates.

---

## Что передать ChatGPT

BATCH_090 выполнен. Hermes-Clean получил полную packaging-инфраструктуру:
- pyproject.toml + requirements.txt
- start_local.cmd (однокомандный запуск)
- check_local.cmd (стандартная проверка)
- check_full.cmd (полная проверка)
- обновлённая документация на русском

Все 309 тестов, 25/25 audit, 23/23 smoke — OK.
Следующий блок: BATCH_091_AI_PROVIDER_SECRET_GATE_SETUP.
