# Malyarka Agent — OUTPUT CONTRACT

Date: 2026-06-17
Agent: Malyarka Agent (#2, `accepted_as_spec`)
Target: Human Review → будущий Corel Export Agent

## Preliminary Order Result

Malyarka Agent возвращает **предварительный** результат. Это НЕ финальный заказ.

### Формат

```yaml
order_result:
  intake_id: "INT-2026-XXXX"
  status: "preliminary_result"
  confirmed_rows:
    - height_mm: 1000
      width_mm: 400
      quantity: 2
      material: "МДФ"
      color: "RAL 9010"
      finish: "матовый"
      area_m2: 0.8
  disputed_rows:
    - height_mm: 600
      width_mm: 300
      quantity: 1
      material: "дерево"
      material_confirmed: false
      reason: "material_ambiguous"
  total_area_m2: 0.8
  export_blocked: true
  dispute_reasons:
    - "material_ambiguous: дерево — уточнить массив/шпон/МДФ"
  missing_fields: []
  manager_review_required: false
  flags:
    discount_request: false
    technical_advice_requested: false
  short_summary: "2 позиции: 1 confirmed (0.8 м²), 1 disputed (дерево)"
  not_final_order: true
```

### Статусы результата

| Статус | Условие |
|--------|--------|
| `needs_clarification` | Не хватает данных — вернуть Sales Intake |
| `preliminary_result` | Расчёт выполнен — ждать human review |
| `ready_for_human_review` | Все проверки пройдены — можно подтверждать |
| `blocked_disputed_data` | Спорные строки — экспорт заблокирован |

### Что НЕ содержит результат

- ❌ Финальную стоимость
- ❌ Цены материалов
- ❌ Сроки выполнения
- ❌ LKM / расход материалов
- ❌ Подтверждение производства
- ❌ Secrets / token / .env

### Подтверждение

```text
not_final_order: true
```

Результат становится финальным только после human review и явного подтверждения.
