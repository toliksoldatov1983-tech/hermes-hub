# Malyarka Agent — PRELIMINARY RESULT TEMPLATE

Date: 2026-06-17
Agent: Malyarka Agent (#2, `accepted`, not active)

## Шаблон результата

```yaml
order_result:
  intake_id: "FAKE-XXX"

  # === Статус ===
  status: "preliminary_result"  # needs_clarification | preliminary_result | blocked_disputed_data | ready_for_human_review

  # === Подтверждённые строки ===
  confirmed_rows:
    - height_mm: 1000
      width_mm: 400
      quantity: 2
      material: "МДФ"
      material_confirmed: true
      color: "RAL 9010"
      color_raw: "RAL 9010"
      color_structured: "RAL 9010"
      finish: "матовый"
      area_m2: 0.8   # h * w * qty / 1_000_000

  # === Спорные строки ===
  disputed_rows:
    - height_mm: 600
      width_mm: 300
      quantity: 1
      material: "дерево"
      material_confirmed: false
      color: "коричневый"
      reason: "material_ambiguous"
      suggested_action: "уточнить массив/шпон/МДФ"

  # === Пропущенные поля ===
  missing_fields: []

  # === Общая площадь (только confirmed) ===
  total_area_m2: 0.8

  # === Блокировка экспорта ===
  export_blocked: true
  export_blocked_reason: "disputed_rows_present"

  # === Флаги ===
  flags:
    discount_request: false
    technical_advice_requested: false
    material_question: true
    manager_review_required: false

  # === Для менеджера ===
  manager_review_required: false

  # === Готовность ===
  ready_for_human_review: false

  # === Критическое ===
  not_final_order: true

  # === Краткое описание ===
  short_summary: "2 позиции: 1 confirmed (0.8 м²), 1 disputed (дерево)"
```

## Статусы

| Статус | Когда |
|--------|-------|
| `needs_clarification` | Нет размеров / материала / цвета |
| `preliminary_result` | Расчёт выполнен, не финальный |
| `blocked_disputed_data` | Спорные строки / blocking flags |
| `ready_for_human_review` | Всё чисто, можно проверять |

## Что НЕ содержит

- ❌ Стоимость / цену
- ❌ Сроки
- ❌ LKM / расход материалов
- ❌ Подтверждение производства
- ❌ Secrets / token / .env
