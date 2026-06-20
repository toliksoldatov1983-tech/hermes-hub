# Server Patch Diff Preparation Plan (PLAN ONLY)

Technical name: `BUNDLE_391_420_SERVER_PATCH_PREPARE_DIFF_ONLY`
Date: 2026-06-17
Type: DIFF_PREP_ONLY / STOP_REVIEW (processed as soft-review in TRUST_TEST_7)
Based on: BUNDLE_361_390 Server Patch Plan

## Status

Markdown-only plan. Не реальный diff. Не применяется. Сервер не трогается.

## Что такое «подготовка diff» в этом контексте

Это **план** того, как будет выглядеть будущий unified diff для серверного patch.

Не сам diff. Не применение. Только описание структуры diff.

---

## 1. Целевые файлы для diff

По server patch plan (361-390):

### Файл A: `hermes_call_site.py` — НОВЫЙ

```text
Путь: /opt/malyarka-telegram-bot/malyarka_telegram/hermes_call_site.py
Действие: создать новый файл
Тип diff: добавление целого файла
```

### Файл B: `handlers.py` — ИЗМЕНЕНИЕ

```text
Путь: /opt/malyarka-telegram-bot/malyarka_telegram/handlers.py
Действие: изменить существующий файл (добавить 3 строки)
Тип diff: unified diff с контекстом
```

### Файл C: `hermes_flags.py` — НОВЫЙ

```text
Путь: /opt/malyarka-telegram-bot/malyarka_telegram/hermes_flags.py
Действие: создать новый файл (feature flags, без secrets)
Тип diff: добавление целого файла
```

---

## 2. Структура Diff A — hermes_call_site.py (новый файл)

```diff
--- /dev/null
+++ b/malyarka_telegram/hermes_call_site.py
@@ -0,0 +1,35 @@
+"""
+Tiny guarded call-site for Hermes adapter.
+
+OFF BY DEFAULT. Feature-flag gated. Dry-run only.
+Never sends Telegram messages directly.
+Fallback to existing flow on any block.
+"""
+
+from __future__ import annotations
+from typing import Any, Dict
+
+from malyarka_telegram.hermes_flags import HERMES_FLAGS
+
+
+async def hermes_call_site(message_text: str, safe_context: Dict[str, Any]):
+    """Tiny guarded call-site. Returns AdapterResult."""
+
+    if not HERMES_FLAGS.get("HERMES_TELEGRAM_INSERTION_ENABLED", False):
+        return {"fallback_required": True, "reason": "insertion disabled"}
+
+    if not HERMES_FLAGS.get("HERMES_SAFE_MODE", True):
+        return {"fallback_required": True, "reason": "safe mode required"}
+
+    request = {
+        "action": "answer_text",
+        "payload": {
+            "text": message_text,
+            "safe_context_summary": str(safe_context)[:500],
+        },
+        "dry_run": True,
+        "feature_flags": dict(HERMES_FLAGS),
+        "safe_mode": True,
+        "diagnostics": False,
+    }
+    # Adapter call would go here — local skeleton for now
+    return {"fallback_required": True, "reason": "adapter not connected"}
```

> **Примечание:** это ПРОЕКТ diff, не реальный код. Содержимое основано на call-site plan (301-330) и adapter skeleton (271-300). Финальный код должен быть адаптирован под реальную структуру серверного бота.

---

## 3. Структура Diff B — handlers.py (изменение)

```diff
--- a/malyarka_telegram/handlers.py
+++ b/malyarka_telegram/handlers.py
@@ -X,Y +X,Y+3 @@
+# === HERMES CALL-SITE (off by default) ===
+from malyarka_telegram.hermes_call_site import hermes_call_site
+
 async def handle_message(message, ...):
+    cs = await hermes_call_site(message.text, _build_safe_context(message))
+    if cs.get("fallback_required"):
+        pass  # continue existing flow
     # === existing handler logic below ===
```

> **Примечание:** X,Y — номера строк НЕИЗВЕСТНЫ (handlers.py contents не читались).
> Контекстные строки (async def handle_message...) — предположительные.
> Точный diff невозможен без read-only копии handlers.py.

---

## 4. Структура Diff C — hermes_flags.py (новый файл)

```diff
--- /dev/null
+++ b/malyarka_telegram/hermes_flags.py
@@ -0,0 +1,20 @@
+"""
+Hermes adapter feature flags.
+
+ALL FLAGS ARE SAFE BY DEFAULT.
+No secrets, tokens, or private data.
+"""
+
+HERMES_FLAGS = {
+    "HERMES_ADAPTER_ENABLED": False,
+    "HERMES_SERVER_ADAPTER_ENABLED": False,
+    "HERMES_TELEGRAM_INSERTION_ENABLED": False,
+    "HERMES_SAFE_MODE": True,
+    "HERMES_DRY_RUN_ONLY": True,
+    "HERMES_EXPORT_CALLBACKS_ENABLED": False,
+    "HERMES_ADMIN_CHANGES_ENABLED": False,
+    "HERMES_ENGINEER_MODE_ENABLED": False,
+    "HERMES_ASSISTANT_MODE_ENABLED": False,
+}
+```
+

---

## 5. Порядок применения diff (будущее)

```
1. Создать hermes_flags.py (все флаги false)
2. Создать hermes_call_site.py
3. Изменить handlers.py (добавить import + вызов)
4. Проверить: бот запускается без ошибок
5. Проверить: call-site возвращает fallback (флаги false)
6. Только после проверки: включать флаги поэтапно
```

---

## 6. Pre-requisites для реального diff

Перед созданием реального diff необходимо:

| # | Requirement | Статус |
|---|------------|--------|
| 1 | Read-only копия handlers.py | ❌ Не получена |
| 2 | Точная handler-функция идентифицирована | ❌ Неизвестна |
| 3 | Номера строк для вставки определены | ❌ Неизвестны |
| 4 | Импорты в handlers.py проверены | ❌ Не проверены |
| 5 | Структура проекта на сервере подтверждена | ⚠️ Только presence-only |

---

## 7. Что этот план НЕ делает

- ❌ Не является реальным diff-файлом
- ❌ Не содержит реальных строк из handlers.py
- ❌ Не может быть применён через `patch` или `git apply`
- ❌ Не требует чтения server files
- ❌ Не требует server connection
- ❌ Не меняет production код

---

## 8. Следующий шаг

```text
BUNDLE_421_450_SERVER_PATCH_DIFF_DRAFT_ONLY
```

Требуется read-only копия handlers.py для создания meaningful draft diff.

---

## Источники

- `SERVER_TELEGRAM_SERVER_PATCH_PLAN_361_390.md`
- `SERVER_TELEGRAM_TINY_GUARDED_CALLSITE_PLAN_301_330.md`
- `server_adapter_skeleton.py` (BUNDLE_271_300)
- `SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_REPORT_231C_234C.md`
