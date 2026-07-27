# Validation Rules — Hermes Clean

**Файл:** `src/hermes_clean/validation.py`
**Назначение:** Локальная валидация структуры и значений заказа без API/БД/секретов.

---

## 1. Проверка одной строки — `validate_single_row(row) -> dict`

Принимает словарь одной строки `{height, width, quantity}`.

### Правило 1.1 — Диапазон высоты (height)

| Поле | Условие | Результат |
|------|---------|-----------|
| `height` | `< 1` или `> 20 000` | ❌ violation `out_of_range` |
| `height` | не `int` и не `float` | ❌ violation `out_of_range` |
| `height` | 1..20 000 и числовой | ✅ OK |

Константа: `MIN_SIZE_MM = 1`, `MAX_SIZE_MM = 20_000`

Поддерживаемые ключи: `"height"` или `"height_mm"`.

### Правило 1.2 — Диапазон ширины (width)

Аналогично высоте. Те же константы.

Поддерживаемые ключи: `"width"` или `"width_mm"`.

### Правило 1.3 — Количество (quantity)

| Поле | Условие | Результат |
|------|---------|-----------|
| `quantity` | не `int` | ❌ violation `invalid_quantity` |
| `quantity` | `< 1` | ❌ violation `invalid_quantity` |
| `quantity` | целое и >= 1 | ✅ OK |

Float (`2.5`) — НЕ принимается.

### Правило 1.4 — Площадь строки (area)

Вычисляется автоматически если height и width — числа:

```
area_m2 = height * width * max(1, int(quantity)) / 1_000_000
```

| Условие | Результат |
|---------|-----------|
| `area_m2 <= 200.0` | ✅ OK |
| `area_m2 > 200.0` | ❌ violation `area_too_large` |

Константа: `MAX_AREA_M2_PER_ROW = 200.0`

---

## 2. Проверка полного заказа — `validate_order_result(order_result) -> dict`

Принимает словарь с ключами `confirmed_rows`, `disputed_rows`, `total_area_m2`.

### Правило 2.1 — Валидация каждой подтверждённой строки

Для каждой строки из `confirmed_rows` вызывается `validate_single_row()`.
Если хотя бы одна строка невалидна → violation с привязкой `row_id` и `source_line`.

### Правило 2.2 — Спорные строки-мусор

Для каждой строки из `disputed_rows` с причиной `empty_or_garbage` или `unparsed_order_text` → violation.

Структурные споры (`missing_width`, `too_many_numbers`) НЕ дают violation валидации — они обрабатываются `DisputeResolver`.

### Правило 2.3 — Дубликаты строк

Сравнивается кортеж `(height, width, quantity)`.
Если такой же кортеж уже встречался среди confirmed_rows → violation `duplicate_row`.

### Правило 2.4 — Отрицательная общая площадь

Если `total_area_m2 < 0` → violation `negative_area`.

---

## 3. Формат результата

```python
{
    "valid": bool,          # True если violations пуст
    "violations": [...],    # список словарей-нарушений
    "blocked": bool,        # True если violations не пуст
    "block_reason": str | None,  # "validation_failed" или None
    "summary": str,         # человекочитаемая сводка
}
```

### Структура одного violation:

```python
{
    "row_id": "row-1",              # привязка к строке
    "source_line": "?",             # исходная строка в заказе
    "field": "height",              # поле-нарушитель
    "value": 0,                     # значение-нарушитель
    "reason": "out_of_range",       # код причины
    "message": "Высота 0 вне диапазона (1-20000 мм).",  # текст на русском
}
```

---

## 4. Полный список reasons

| Код | Когда срабатывает |
|-----|-------------------|
| `out_of_range` | height или width вне [1, 20000] |
| `invalid_quantity` | quantity не int или < 1 |
| `area_too_large` | площадь строки > 200 м² |
| `empty_or_garbage` | disputed row с неразбираемым текстом |
| `unparsed_order_text` | disputed row = нераспознанный текст |
| `duplicate_row` | точный дубликат (h,w,q) в confirmed |
| `negative_area` | total_area_m2 < 0 |
