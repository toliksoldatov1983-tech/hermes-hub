# Dispute Questions — Маппинг шаблонов к ошибкам

**Файл:** `src/hermes_clean/dispute_resolver.py`
**Константа:** `SUGGESTED_QUESTIONS`
**Функция:** `get_suggested_question(reason) -> str`

---

## 1. Полный список шаблонов

| reason (код ошибки) | Шаблон вопроса (русский) | Когда возникает |
|---------------------|--------------------------|-----------------|
| `missing_width` | *Уточнить ширину строки.* | В строке только одно число вместо двух (например, `1000`) |
| `missing_height` | *Уточнить высоту строки.* | В строке есть ширина, но нет высоты |
| `too_many_numbers` | *Уточнить, какие числа являются высотой, шириной и количеством.* | 4+ чисел в строке (например, `1000 400 2 5`) |
| `unclear_quantity` | *Уточнить количество.* | Количество не определено или сомнительно |
| `unparsed_order_text` | *Уточнить, влияет ли текст на заказ.* | Строка содержит текст, а не размеры (например, `срочно`) |
| `empty_or_garbage` | *Проверить строку или удалить ее.* | Строка пустая или нечитаемый мусор |
| `unsupported_format` | *Уточнить размер в формате высота ширина количество.* | Неподдерживаемый формат (например, `1000 мм`) |
| *(любой другой)* | *Уточнить строку.* | Запасной вариант для неизвестных причин |

---

## 2. Маппинг reason → действие Resolver'а

| reason | Действие по умолчанию | Можно ли accept? | Можно ли delete? | Можно ли clarify? |
|--------|----------------------|:----------------:|:----------------:|:------------------:|
| `missing_width` | clarify | ✅ (нужно ввести width) | ✅ | ✅ |
| `missing_height` | clarify | ✅ | ✅ | ✅ |
| `too_many_numbers` | clarify | ✅ | ✅ | ✅ split |
| `unclear_quantity` | clarify | ✅ | ✅ | ✅ |
| `unparsed_order_text` | clarify | ❌ (нет размеров) | ✅ | ✅ |
| `empty_or_garbage` | clarify | ❌ | ✅ | ✅ |
| `unsupported_format` | clarify | ❌ | ✅ | ✅ |

---

## 3. Маппинг reason → severity

| reason | severity | Автоматическое разрешение? |
|--------|----------|---------------------------|
| `missing_width` | `needs_user_review` | Нет (нужно число) |
| `missing_height` | `needs_user_review` | Нет |
| `too_many_numbers` | `needs_user_review` | Можно split |
| `unclear_quantity` | `needs_user_review` | Нет |
| `unparsed_order_text` | `needs_user_review` | Нет (текст) |
| `empty_or_garbage` | `needs_user_review` | Можно delete |
| `unsupported_format` | `needs_user_review` | Нет |

---

## 4. Маппинг: фикстура → проверяемый вопрос

| Фикстура | reason | Какой вопрос проверяет |
|----------|--------|----------------------|
| `dispute_missing_width` | `missing_width` | *Уточнить ширину строки.* |
| `dispute_too_many_numbers` | `too_many_numbers` | *Уточнить, какие числа...* |
| `dispute_mixed` | `unparsed_order_text` | *Уточнить, влияет ли текст...* |
| `dispute_garbage` | `unparsed_order_text` | *Уточнить, влияет ли текст...* |
| `edge_negative` | `unparsed_order_text` | *Уточнить, влияет ли текст...* |

---

## 5. Маппинг: validation violation → dispute question

Некоторые ошибки валидации могут быть разрешены через DisputeResolver:

| Validation reason | Соответствующий dispute reason | Вопрос |
|-------------------|-------------------------------|--------|
| `out_of_range` (height=0) | `missing_height` или `clarify` | *Уточнить высоту строки.* |
| `out_of_range` (height > 20000) | `clarify` | *Уточнить строку.* |
| `out_of_range` (width=0) | `missing_width` | *Уточнить ширину строки.* |
| `invalid_quantity` | `unclear_quantity` | *Уточнить количество.* |
| `area_too_large` | `split` | Техническое разделение строки |
| `unparsed_order_text` | `unparsed_order_text` | *Уточнить, влияет ли текст...* |
| `empty_or_garbage` | `empty_or_garbage` | *Проверить строку или удалить ее.* |

> **Важно:** Не все validation violations имеют прямой dispute question. `out_of_range` с height=30000 — техническое нарушение, которое не решается уточнением у пользователя. Resolver корректно вернёт "Уточнить строку." как fallback.
