# Malyarka Agent — TEST SCENARIOS

Date: 2026-06-17
Agent: Malyarka Agent (#2, `accepted`, not active)
Purpose: 15 сценариев для будущей проверки (без кода, markdown-only)

---

## Формат

| Поле | Описание |
|------|---------|
| Входная Intake Card | Что получает агент |
| Ожидаемый результат | Что должен вернуть |
| Статус | preliminary_result / needs_clarification / blocked_disputed_data |

---

### Сценарий 1 — Intake card без размеров

```yaml
intake_card:
  items: []
  material: {raw: "МДФ", confirmed: true}
  flags: {}
```
**Ожидаемый результат:** `needs_clarification` — нет размеров.

---

### Сценарий 2 — Intake card без материала

```yaml
intake_card:
  items:
    - height_mm: 1000, width_mm: 400, quantity: 2, material: ""
  material: {raw: null, confirmed: false}
  flags: {}
```
**Ожидаемый результат:** `needs_clarification` — нет материала.

---

### Сценарий 3 — Ambiguous material (дерево)

```yaml
intake_card:
  items:
    - height_mm: 1000, width_mm: 400, quantity: 2, material: "дерево", material_confirmed: false, color: "белый"
  material: {raw: "дерево", confirmed: false}
  color: {raw: "белый"}
  flags: {material_question: true}
```
**Ожидаемый результат:** `blocked_disputed_data` — материал не подтверждён → спорная строка.

---

### Сценарий 4 — Raw color (без RAL)

```yaml
intake_card:
  items:
    - height_mm: 1000, width_mm: 400, quantity: 1, material: "МДФ", material_confirmed: true, color: "белый"
  material: {raw: "МДФ", confirmed: true}
  color: {raw: "белый", structured: null}
  flags: {}
```
**Ожидаемый результат:** `preliminary_result` — цвет допустим без RAL.

---

### Сценарий 5 — Structured RAL/NCS

```yaml
intake_card:
  items:
    - height_mm: 800, width_mm: 500, quantity: 3, material: "МДФ", material_confirmed: true, color: "RAL 9010"
  material: {raw: "МДФ", confirmed: true}
  color: {raw: "RAL 9010", structured: "RAL 9010"}
  flags: {}
```
**Ожидаемый результат:** `preliminary_result` — area = 800×500×3/1M = 1.2 м².

---

### Сценарий 6 — Только покраска

```yaml
intake_card:
  items:
    - height_mm: 1000, width_mm: 400, quantity: 4, material: "МДФ", material_confirmed: true, color: "белый", finish: "матовый"
  material: {raw: "МДФ", confirmed: true}
  color: {raw: "белый"}
  flags: {}
```
**Ожидаемый результат:** `preliminary_result` — 4 шт, 1.6 м².

---

### Сценарий 7 — Фрезеровка + покраска

```yaml
intake_card:
  items:
    - height_mm: 800, width_mm: 500, quantity: 4, material: "МДФ", material_confirmed: true, color: "белый"
  flags: {technical_advice_requested: true, manager_review_required: true}
```
**Ожидаемый результат:** `blocked_disputed_data` — technical_advice блокирует.

---

### Сценарий 8 — Фасады под ключ (нет размеров)

```yaml
intake_card:
  items: []
  flags: {manager_review_required: true}
```
**Ожидаемый результат:** `needs_clarification` — нет размеров + manager review.

---

### Сценарий 9 — Переделка старых фасадов

```yaml
intake_card:
  items:
    - height_mm: 600, width_mm: 400, quantity: 5, material: "дерево", material_confirmed: false, color: "белый"
  material: {raw: "дерево", confirmed: false}
  flags: {material_question: true}
```
**Ожидаемый результат:** `blocked_disputed_data` — материал не подтверждён.

---

### Сценарий 10 — Discount request

```yaml
intake_card:
  items:
    - height_mm: 1000, width_mm: 400, quantity: 10, material: "МДФ", material_confirmed: true, color: "RAL 9010"
  flags: {discount_request: true}
```
**Ожидаемый результат:** `blocked_disputed_data` — discount блокирует, менеджер нужен.

---

### Сценарий 11 — Technical advice requested

```yaml
intake_card:
  items:
    - height_mm: 1000, width_mm: 400, quantity: 2, material: "МДФ", material_confirmed: true, color: "белый"
  flags: {technical_advice_requested: true, manager_review_required: true}
```
**Ожидаемый результат:** `blocked_disputed_data` — техсовет блокирует.

---

### Сценарий 12 — Manager review required

```yaml
intake_card:
  items:
    - height_mm: 1000, width_mm: 400, quantity: 1, material: "МДФ", material_confirmed: true, color: "RAL 9010"
  flags: {manager_review_required: true}
```
**Ожидаемый результат:** `blocked_disputed_data` — manager review требуется.

---

### Сценарий 13 — Disputed line (неподтверждённый материал)

```yaml
intake_card:
  items:
    - height_mm: 1000, width_mm: 400, quantity: 2, material: "МДФ", material_confirmed: true, color: "RAL 9010"
    - height_mm: 600, width_mm: 300, quantity: 1, material: "дерево", material_confirmed: false, color: "коричневый"
  material: {raw: "МДФ", confirmed: true}
  flags: {material_question: true}
```
**Ожидаемый результат:** `blocked_disputed_data` — 1 confirmed (0.8 м²) + 1 disputed.

---

### Сценарий 14 — Достаточно данных

```yaml
intake_card:
  items:
    - height_mm: 1000, width_mm: 400, quantity: 4, material: "МДФ", material_confirmed: true, color: "RAL 9010", finish: "матовый"
    - height_mm: 600, width_mm: 300, quantity: 2, material: "МДФ", material_confirmed: true, color: "RAL 8017", finish: "глянцевый"
  material: {raw: "МДФ", confirmed: true}
  color: {raw: "RAL 9010", structured: "RAL 9010"}
  flags: {}
```
**Ожидаемый результат:** `preliminary_result` — 2 confirmed, 1.96 м².

---

### Сценарий 15 — Заблокировано: данных недостаточно

```yaml
intake_card:
  items:
    - height_mm: 1000, width_mm: 400, quantity: 1, material: "", material_confirmed: false, color: ""
  material: {raw: null, confirmed: false}
  flags: {}
```
**Ожидаемый результат:** `needs_clarification` — нет материала и цвета.
