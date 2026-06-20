# Malyarka Agent — INTAKE CONTRACT

Date: 2026-06-17
Agent: Malyarka Agent (#2, `accepted_as_spec`)
Source: Sales + Client Intake Agent (#1)

## Контракт приёма

Malyarka Agent принимает структурированную Intake Card от Sales Intake Agent.

### Формат

```yaml
handoff_package:
  from: "sales_client_intake_agent"
  to: "malyarka_agent"
  intake_id: "INT-2026-XXXX"
  timestamp: "2026-06-17T..."

  client:
    name: "Иван"
    location: "Москва"

  items:
    - height_mm: 1000
      width_mm: 400
      quantity: 2
      material: "МДФ"
      material_confirmed: true
      color: "RAL 9010"
      color_raw: "белый"
      color_structured: "RAL 9010"
      finish: "матовый"
      surface_finish_raw: "матовый"
      surface_ready: false
      needs_primer: true

  material:
    raw: "МДФ"
    confirmed: true

  color:
    raw: "белый"
    structured: "RAL 9010"

  urgency:
    requested: "обычный"

  flags:
    discount_request: false
    technical_advice_requested: false
    material_question: false
    manager_review_required: false

  ready_for_malyarka_agent: true
```

### Обязательные поля

| Поле | Тип | Описание |
|------|-----|---------|
| `items[].height_mm` | int | Высота в мм, > 0 |
| `items[].width_mm` | int | Ширина в мм, > 0 |
| `items[].quantity` | int | Количество, ≥ 1 |
| `items[].material` | str | Материал |
| `items[].material_confirmed` | bool | false = нужна проверка |
| `items[].color` | str | Цвет (raw или structured) |
| `ready_for_malyarka_agent` | bool | Должен быть true |

### Блокирующие флаги

Handoff **не выполняется**, если любой из флагов = true:
- `discount_request`
- `technical_advice_requested`
- `manager_review_required`
- `material_confirmed: false` для любой позиции

### Обработка

1. Принять Intake Card
2. Проверить `ready_for_malyarka_agent: true`
3. Проверить отсутствие blocking flags
4. Распарсить размеры каждой позиции
5. Разделить на confirmed / disputed
6. Рассчитать площадь
7. Вернуть Order Result

### Статус

`accepted_as_spec` — спецификация утверждена. Код не писать.
