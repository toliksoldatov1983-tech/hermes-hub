# Sales + Client Intake Agent — GOLDEN CASES

Date: 2026-06-17 (updated: edge-case hardened)
Tests: `tests/test_golden_cases.py` (25 тестов)
Demo: `demo/run_demo.py` (15 сценариев)

## Список Golden Cases

| # | Название | Что проверяет |
|---|---------|--------------|
| GC1 | Цена без размеров | discount_request, no price in response |
| GC2 | Размеры без материала | sizes extracted, material missing |
| GC3 | Фасады белые | color detected, sizes missing |
| GC4 | Фрезеровка без типа | technical_advice, manager_review |
| GC5 | Скидка | discount_request, no % in response |
| GC6 | Какой материал лучше | technical_advice, manager_review |
| GC7 | Сроки | manager_review, no deadline words |
| GC8 | Неполное описание | needs_more_info |
| GC9 | Только покраска | FULL DATA → ready_for_malyarka ✅ |
| GC10 | Переделка старых | дерево ambiguous → needs_more_info |
| GC11 | Под ключ | no sizes → needs_more_info |
| GC12 | Цвет без RAL | color detected, ready_for_malyarka |
| GC13 | Примерно 20 | material+color yes, sizes no |
| GC14 | Посчитайте кухню | no data → needs_more_info |
| GC15 | Все данные (дерево) | sizes+color yes, дерево ambiguous → needs_more_info |
| GS1 | Safety price | 4 текста → ни одного "руб" или "₽" |
| GS2 | Safety deadline | 3 текста → ни одного "дня" или "недел" |
| GS3 | Safety discount | 3 текста → ни одного "%" |

## Edge-Case Golden Cases (добавлены 2026-06-17)

| # | Название | Что проверяет |
|---|---------|--------------|
| EC1 | Дерево ambiguous | `дерево` → material_raw="дерево", confirmed=False, material_question=True |
| EC2 | СПб location | `СПб` → detected_location="Санкт-Петербург" |
| EC3 | Алматы location | `Алматы` → detected_location="Алматы" |
| EC4 | Белый не RAL | `белый` → color_raw="белый", color_structured=None |
| EC5 | RAL structured | `RAL 9010` → color_structured="RAL 9010" |
| EC6 | Finish not tech | `матовый` → surface_finish_raw="матовый", technical_advice=False |
| EC7 | Discount blocks | discount_request → ready_for_malyarka=False, manager_review=True |

## Последний результат

```text
48 passed, 0 failed in 0.16s (2026-06-17)
```
