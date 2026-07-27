# Fixture Count — Полный аудит синтетических фикстур

**Файл:** `src/hermes_clean/fixtures.py`
**Всего фикстур:** 11
**ID префикс:** `syn-*`

---

## Группа 1: Clean orders (4 фикстуры)

Чистые заказы без спорных строк. Проверяют корректный парсинг и валидацию.

| # | ID | Имя | Тег | Суть |
|---|----|-----|-----|------|
| 1 | `syn-clean-single` | **clean_single** | `clean, minimal` | Одиночная строка `1000x400x2`. Площадь 0.8 м². Базовая проверка. |
| 2 | `syn-clean-multi` | **clean_multi** | `clean, multi` | 3 строки: `1000x400x2`, `700x300x1`, `500x500x3`. Сумма 1.76 м². Мульти-строка. |
| 3 | `syn-clean-large` | **clean_large** | `clean, large` | Крупные размеры: `3000x2000x1` (6 м²), `5000x2500x2` (25 м²). Граница допустимого. |
| 4 | `syn-clean-zero` | **clean_zero_rows** | `empty, edge` | Пустой заказ. 0 строк, 0 disputed. Статус `empty_or_invalid`. Граничный случай. |

### Что проверяют:

- ✅ Одна строка → корректный результат
- ✅ Несколько строк → корректная сумма
- ✅ Крупные размеры в пределах лимита
- ✅ Пустой ввод → empty_or_invalid без ошибок

---

## Группа 2: Disputed orders (4 фикстуры)

Заказы со спорными строками. Проверяют логику обнаружения проблем.

| # | ID | Имя | Тег | Суть |
|---|----|-----|-----|------|
| 5 | `syn-disp-width` | **dispute_missing_width** | `disputed, single` | Одно число `1000` — не хватает ширины. Причина `missing_width`. |
| 6 | `syn-disp-numbers` | **dispute_too_many_numbers** | `disputed, format` | `1000 400 2 5` — 4 числа. Причина `too_many_numbers`. |
| 7 | `syn-disp-mixed` | **dispute_mixed** | `disputed, mixed` | 2 чистые строки + 1 мусор. Причина `unparsed_order_text`. |
| 8 | `syn-disp-garbage` | **dispute_garbage** | `disputed, garbage` | Только мусор: `привет`, `ничего непонятно`. 2 disputed. |

### Что проверяют:

- ✅ Structural dispute (missing_width) — НЕ блокирует валидацию, идёт в Resolver
- ✅ Structural dispute (too_many_numbers) — НЕ блокирует валидацию
- ✅ Mixed (clean + disputed) — valid=False для валидации
- ✅ Garbage only — valid=False, blocked=True

---

## Группа 3: Edge / boundary cases (3 фикстуры)

Граничные и аномальные случаи.

| # | ID | Имя | Тег | Суть |
|---|----|-----|-----|------|
| 9 | `syn-edge-neg` | **edge_negative** | `edge, safety` | Отрицательное число `-1000 400`. Статус `has_disputes`. |
| 10 | `syn-edge-zero` | **edge_zero_size** | `edge` | Нулевая высота: `height=0`. valid=False (out_of_range). |
| 11 | `syn-edge-ru-x` | *не вошёл* | — | Русская «х» как разделитель — исключён в адаптации. |

### Что проверяют:

- ✅ Отрицательные числа → disputed (безопасность)
- ✅ Нулевой размер → violation out_of_range (не блокирует export, но предупреждает)

---

## Сводка

| Метрика | Значение |
|---------|----------|
| Всего фикстур | **11** |
| Clean | 4 |
| Disputed | 4 |
| Edge | 3 |
| Все ID уникальны | ✅ |
| Все имеют tags | ✅ |

### Охват reasons через фикстуры:

| reason | Какая фикстура покрывает |
|--------|--------------------------|
| `out_of_range` | `edge_zero_size` |
| `invalid_quantity` | нет (чисто тестовый) |
| `area_too_large` | нет (чисто тестовый) |
| `unparsed_order_text` | `dispute_mixed`, `dispute_garbage`, `edge_negative` |
| `empty_or_garbage` | нет |
| `duplicate_row` | нет (чисто тестовый) |
| `missing_width` | `dispute_missing_width` |
| `too_many_numbers` | `dispute_too_many_numbers` |
| `negative_area` | нет (чисто тестовый) |

> Фикстуры покрывают логику end-to-end. Отдельные причины (`area_too_large`, `negative_area`, `duplicate_row`) покрываются напрямую в `test_validation.py`.
