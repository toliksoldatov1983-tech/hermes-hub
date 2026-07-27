# Export Gate Status — Логика блокировки экспорта

**Файл:** `src/hermes_clean/export_gate.py`
**Класс:** `ExportBlockedError(ValueError)`
**Функция:** `build_export_model(order_result, *, strict=False) -> dict`

---

## 1. Входные данные

Функция принимает `order_result` — словарь с ключами:

| Ключ | Тип | Обязателен | Описание |
|------|-----|-----------|----------|
| `status` | str | Да | `"clean"`, `"has_disputes"`, `"empty_or_invalid"` |
| `confirmed_rows` | list[dict] | Да | Уже проверенные строки |
| `disputed_rows` | list[dict] | Да | Спорные строки |
| `export_blocked` | bool | Нет | Ручная блокировка экспорта |

---

## 2. Жёсткие условия блокировки (Gate)

Экспорт блокируется на **100%** если хотя бы ОДНО условие истинно:

### Условие A — Статус empty_or_invalid

```python
if status == "empty_or_invalid":
    return BLOCKED  # reason: "empty_or_invalid"
```

`status` может быть `"empty_or_invalid"` если:
- Нет ни confirmed, ни disputed строк (пустой ввод)
- Только нераспознаваемый мусор

### Условие B — Есть спорные строки

```python
if disputed_rows:
    return BLOCKED  # reason: "disputed_rows_present"
```

Любая непустая `disputed_rows` → блокировка.
Даже одна строка с `missing_width` → блокировка.
Даже resolved, но не удалённая → блокировка.

### Условие C — Ручная блокировка

```python
if order_result.get("export_blocked"):
    return BLOCKED  # reason: "export_blocked"
```

Если внешний код установил `export_blocked=True` → блокировка.

### Условие D — Статус не clean

```python
if status != "clean":
    return BLOCKED  # reason: "source_not_clean"
```

Страховочное условие. Если статус не `"clean"` и не попал в A/B/C → блокировка.

---

## 3. Режимы работы

### Режим strict=False (по умолчанию)

Возвращает словарь-блокировку, **НЕ возбуждает исключение**:

```python
{
    "export_rows": [],
    "export_blocked": True,
    "reason": "disputed_rows_present",  # или empty_or_invalid / export_blocked / source_not_clean
    "source_status": "has_disputes",
}
```

Используется в нестрогих проверках (UI preview, soft checks).

### Режим strict=True

Возбуждает **`ExportBlockedError`** — наследника `ValueError`:

```python
raise ExportBlockedError(
    reason="disputed_rows_present",
    source_status="has_disputes"
)
# message: "Экспорт заблокирован: disputed_rows_present (статус: has_disputes)"
```

Используется в жёстких гейтах (прямой экспорт, API-вызовы).

---

## 4. Успешный экспорт

```python
{
    "export_rows": [
        {"height_mm": 1000, "width_mm": 400, "quantity": 2},
    ],
    "export_blocked": False,
    "reason": "ready",
    "source_status": "clean",
}
```

Только когда **все 4 условия ложны**:
- ✅ status == "clean"
- ✅ disputed_rows == []
- ✅ export_blocked не установлен или False
- ✅ Ничего не прошло через A/B/C/D

---

## 5. Матрица решений

| status | disputed_rows? | export_blocked? | strict=False | strict=True |
|--------|---------------|-----------------|-------------|-------------|
| `clean` | нет | False | ✅ ready | ✅ ready |
| `clean` | нет | True | ⛔ export_blocked | ⛔ ExportBlockedError |
| `has_disputes` | да | любое | ⛔ disputed_rows_present | ⛔ ExportBlockedError |
| `empty_or_invalid` | нет | любое | ⛔ empty_or_invalid | ⛔ ExportBlockedError |
| `empty_or_invalid` | да (мусор) | любое | ⛔ empty_or_invalid | ⛔ ExportBlockedError |

> **Вывод:** Export Gate — жёсткий предохранитель. Экспорт возможен ТОЛЬКО при `status="clean"`, `disputed_rows=[]`, `export_blocked=False`. Любое отклонение — 100% блокировка.
