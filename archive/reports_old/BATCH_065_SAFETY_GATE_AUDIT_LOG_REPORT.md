# BATCH_065 — RUNTIME SAFETY GATE И AUDIT LOG

Дата: 2026-07-01
Статус: ✅ ВЫПОЛНЕНО

---

## ЧТО СДЕЛАНО

### Новые файлы

| Файл | Описание |
|------|----------|
| `src/hermes_core/safety/audit_log.py` | Локальный аудит-лог (JSONL). Логирует SAFE/CONFIRM/BLOCKED. Запрещает секреты. |
| `src/hermes_core/safety/__init__.py` | Расширен: экспорт SafetyGate, AuditLog, классификаций |
| `tests/test_safety_gate.py` | 24 теста: SAFE, CONFIRM_REQUIRED, BLOCKED, audit log, секреты |

### Изменённые файлы

| Файл | Изменение |
|------|-----------|
| `src/hermes_core/cli.py` | `safety` команда теперь логирует в аудит; добавлена `safety-audit` команда |

---

## ПРОВЕРКИ

### Безопасность (safety delete)

```
decision=BLOCKED
reason=Action is blocked by Hermes-Clean policy.
audit_logged=BLOCKED
```

### Аудит-лог (safety-audit)

```
safety_audit=local
total_entries=4
safe=1
confirm_required=1
blocked=2
log_path=.../05_REPORTS/AUDIT_LOG.jsonl
```

### Полные проверки

| Команда | Результат |
|---------|-----------|
| `hermes.cmd safety delete` | BLOCKED ✅ |
| `hermes.cmd safety create_local_report` | SAFE ✅ |
| `hermes.cmd safety connect_telegram` | CONFIRM_REQUIRED ✅ |
| `hermes.cmd safety-audit` | 4 entries logged ✅ |
| `hermes.cmd project-audit` | 14/14 OK ✅ |
| `hermes.cmd smoke` | 20/20 OK ✅ |
| `run_tests.cmd` | **128 passed + 6 subtests** ✅ |

---

## АРХИТЕКТУРА SAFETY GATE

```
hermes_core/safety/
├── __init__.py          — exports: SafetyGate, LocalAuditLog, classify_action, SAFE/CONFIRM/BLOCKED
├── action_policy.py     — SAFE/CONFIRM_REQUIRED/BLOCKED действия + classify_action()
├── safety_gate.py       — SafetyGate.evaluate(), .block_if_needed()
└── audit_log.py         — LocalAuditLog: запись, чтение, проверка секретов, лимиты
```

### Классификация действий

| Категория | Примеры |
|-----------|---------|
| **SAFE** (5) | answer_text, create_local_report, update_local_state, dry_run, local_test |
| **CONFIRM_REQUIRED** (6) | read_external_folder, read_old_archive, read_google_drive_document, run_external_api, work_with_tokens, connect_telegram |
| **BLOCKED** (8) | delete, modify_old_project, modify_real_order, telegram_live, drive_move_without_approval, read_secret, change_permissions, send_external_file |

### Аудит-лог

- Формат: JSONL в `05_REPORTS/AUDIT_LOG.jsonl`
- Лимит: 500 KB / 200 записей
- Запрещены: token, api_key, secret, password, orders_db, real_order, client_name, env_value
- Очистка старых записей при превышении лимита

---

## НОВЫЕ ТЕСТЫ (24)

| Тест | Проверка |
|------|----------|
| test_classify_safe_action | SAFE для create_local_report |
| test_classify_dry_run_is_safe | SAFE для dry_run |
| test_classify_confirm_required | CONFIRM_REQUIRED для connect_telegram |
| test_classify_confirm_with_approval | SAFE при approved=True |
| test_classify_blocked | BLOCKED для delete |
| test_classify_delete_stays_blocked | BLOCKED даже с approved=True |
| test_classify_modify_real_order_blocked | BLOCKED |
| test_classify_telegram_live_blocked | BLOCKED |
| test_classify_read_secret_blocked | BLOCKED |
| test_classify_unknown_action_confirm | CONFIRM_REQUIRED для неизвестного |
| test_safety_gate_single_safe | SafetyGate.evaluate() → SAFE |
| test_safety_gate_single_blocked | SafetyGate.evaluate() → BLOCKED |
| test_safety_gate_block_if_needed_* | batch проверки |
| test_audit_log_writes_entry | Запись + чтение |
| test_audit_log_multiple_entries | 3 записи: SAFE, BLOCKED, CONFIRM |
| test_audit_log_forbids_secrets_* | ValueError при token/api_key/real_order |
| test_audit_log_clear | Очистка лога |
| test_drive_move_* | gate для Google Drive |

---

## ЧТО НЕ ТРОГАЛОСЬ

- E:\«Гермес Клин»
- Архивы, [удалён]
- Google Drive (кроме классификации действий)
- .env, токены, ключи
- Live Telegram
- Внешние API
- Реальные заказы

---

## СЛЕДУЮЩИЙ ШАГ

BATCH_063B_PLAN_SAFE_PORT_MALYARKA_HARDENING_TO_HERMES_CLEAN:
подготовить план безопасного переноса результатов BATCH_063 в Desktop Hermes-Clean.
