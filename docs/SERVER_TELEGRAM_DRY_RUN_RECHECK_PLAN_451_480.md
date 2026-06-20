# Server Patch Dry-Run Recheck Plan (PLAN ONLY)

Technical name: `BUNDLE_451_480_SERVER_PATCH_DRY_RUN_RECHECK_PLAN`
Date: 2026-06-17
Type: PLAN_ONLY / AUTO_MARKDOWN
Based on: BUNDLE_361_390 (Patch Plan), BUNDLE_391_420 (Diff Prep Plan)
Note: BUNDLE_421_450 SKIPPED — BLOCKED (missing handlers.py)

## Status

Markdown-only plan. Без server touch. Без кода. Без запуска.

---

## 1. Что такое Dry-Run Recheck

**Dry-run** — применить patch на сервере, но с **всеми feature flags в false**. Бот продолжает работать как раньше, call-site всегда возвращает `fallback_required=true`. Проверяется: patch не ломает существующее поведение.

**Recheck** — перепроверить все safety-условия ДО и ПОСЛЕ dry-run.

**План (этот документ)** — описать как, когда и при каких условиях делать dry-run recheck. Сам dry-run НЕ выполняется.

---

## 2. Учёт BUNDLE_421_450 (SKIPPED)

```text
BUNDLE_421_450: SERVER_PATCH_DIFF_DRAFT_ONLY
Статус: SKIPPED_BLOCKED_MISSING_SERVER_FILE_CONTENTS
Причина: нужна read-only копия handlers.py для meaningful diff draft
```

**Влияние на dry-run recheck:**
- Без draft diff нет точного представления о том, какие строки меняются в handlers.py
- Dry-run невозможен без diff → diff draft — обязательный prerequisite
- Recheck должен включать проверку: «получен ли draft diff (BUNDLE_421_450)?»

---

## 3. Pre-Requisites для Dry-Run

### Уже готово ✅

| # | Prerequisite | Bundle | Статус |
|---|-------------|--------|--------|
| 1 | Server inventory (presence-only) | 231C-234C | ✅ |
| 2 | Adapter insertion design | 235-238 | ✅ |
| 3 | Contract interface + examples | 243-250 | ✅ |
| 4 | Adapter skeleton + tests (17/17) | 271-300 | ✅ |
| 5 | Call-site plan | 301-330 | ✅ |
| 6 | Readiness gate (PARTIALLY READY) | 331-360 | ✅ |
| 7 | Server patch plan | 361-390 | ✅ |
| 8 | Diff preparation plan | 391-420 | ✅ |
| 9 | Dry-run recheck plan | 451-480 | ✅ (этот) |

### Отсутствует ❌

| # | Prerequisite | Почему | Кто решает |
|---|-------------|--------|------------|
| 1 | **Read-only копия handlers.py** | Запрещено читать server files | Пользователь |
| 2 | **Draft diff (BUNDLE_421_450)** | SKIPPED — нет handlers.py | После получения копии |
| 3 | SSH write-доступ | Не подтверждён | Пользователь |
| 4 | `hermes_flags.py` инфраструктура | `config.py` нельзя читать | Архитектурное решение |
| 5 | Backup процедура | Не документирована | Пользователь |
| 6 | Bot runtime state | Неизвестен | Пользователь |

---

## 4. Dry-Run Recheck — Пошаговый план

### Phase A: Pre-Dry-Run Checks

```
[ ] A1. BUNDLE_421_450 выполнен — draft diff готов
[ ] A2. Read-only копия handlers.py получена и проверена
[ ] A3. Diff проверен локально на safe копии handlers.py
[ ] A4. Diff НЕ содержит: config.py, token, .env, secrets
[ ] A5. Diff НЕ меняет: app.py, router.py, services/orders.py
[ ] A6. SSH write-доступ подтверждён
[ ] A7. Backup создан (копия /opt/malyarka-telegram-bot/)
[ ] A8. Rollback diff готов (обратный patch)
[ ] A9. Пользователь дал STOP_APPROVAL (bundle 481-510)
```

### Phase B: Dry-Run Execution

```
[ ] B1. Применить patch на сервере
        - hermes_call_site.py → создан
        - hermes_flags.py → создан (все флаги false)
        - handlers.py → изменён (+3 строки)
[ ] B2. Проверить: бот запускается без ошибок
[ ] B3. Проверить логи: нет traceback, нет ошибок импорта
[ ] B4. Проверить: call-site всегда возвращает fallback_required=true
[ ] B5. Проверить: существующее поведение бота не изменилось
[ ] B6. Проверить: Telegram-сообщения не отправляются из adapter
[ ] B7. Проверить: side_effects=[] (логи, файлы — без изменений)
[ ] B8. Мониторить логи ≥ 1 час
```

### Phase C: Post-Dry-Run

```
[ ] C1. Если все проверки пройдены → откатить patch (rollback diff)
[ ] C2. Проверить: после отката бот работает как раньше
[ ] C3. Задокументировать результаты dry-run
[ ] C4. Подготовить activation plan (будущие bundle)
[ ] C5. Не включать feature flags без отдельного STOP_APPROVAL
```

---

## 5. Что именно проверяется в Dry-Run

| Проверка | Как | Критерий |
|----------|-----|----------|
| Бот запускается | Проверить процесс/логи | Нет crash, нет traceback |
| Импорты работают | Логи импорта | `import hermes_call_site` — OK |
| Call-site возвращает fallback | Флаги false → fallback | `fallback_required=true` |
| Существующая логика цела | Ручной тест: отправить сообщение боту | Ответ как раньше |
| Нет side effects | Логи, файлы, БД | Без изменений |
| Нет Telegram send из adapter | Логи adapter | 0 отправок |
| Rollback работает | Применить обратный diff | Бот работает как раньше |

---

## 6. Почему Server/Live/Runtime/Secrets запрещены

| Зона | Причина запрета |
|------|----------------|
| **Server files** | `config.py` содержит token — утечка = компрометация бота |
| **Live Telegram** | Бот обрабатывает реальных пользователей — сбой = простой |
| **Runtime** | Polling/webhook — изменение может нарушить доставку сообщений |
| **Secrets** | Token, .env, os.environ — компрометация безопасности |
| **Real orders** | Обработка заказов через непроверенный adapter — риск ошибок |

**Принцип:** все опасные зоны остаются под защитой feature flags (false) и dry-run (true). Ни одно действие не выполняется без явного STOP_APPROVAL.

---

## 7. Blocker'ы (текущее состояние)

```text
BLOCKERS (6 из 6):
❌ handlers.py read-only копия
❌ Draft diff (BUNDLE_421_450)
❌ SSH write-доступ
❌ hermes_flags.py инфраструктура
❌ Backup процедура
❌ Bot runtime state

READY (9 из 9):
✅ Inventory, design, contracts, skeleton, tests, call-site plan,
   readiness gate, patch plan, diff prep plan, dry-run plan
```

**Вывод:** dry-run НЕВОЗМОЖЕН без решения blocker'ов. План готов — ждать выполнения prerequisites.

---

## 8. Следующий bundle

```text
#9: BUNDLE_481_510_SERVER_PATCH_FINAL_APPROVAL_GATE
Type: GATE_ONLY
Autonomy: STOP_APPROVAL
```

**HARD STOP.** STOP_APPROVAL — требуется явное разрешение пользователя перед любыми server patch действиями (включая dry-run).

---

## Источники

- `SERVER_TELEGRAM_SERVER_PATCH_PLAN_361_390.md`
- `SERVER_TELEGRAM_DIFF_PREPARATION_PLAN_391_420.md`
- `REPORT_BUNDLE_331_360_SERVER_PATCH_READINESS_GATE.md`
- `SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_REPORT_231C_234C.md`
- `SAFETY_RULES.md`
- `MANIFEST.md`
