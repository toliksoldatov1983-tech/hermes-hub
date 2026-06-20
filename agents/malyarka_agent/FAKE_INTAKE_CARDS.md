# Malyarka Agent — FAKE INTAKE CARDS

Date: 2026-06-17
Agent: Malyarka Agent (#2, `accepted`, not active)
Важно: ВСЕ карточки искусственные. Ни одной реальной.

---

### Fake #1 — Простой МДФ

```yaml
intake_id: "FAKE-001"
items:
  - height_mm: 1000, width_mm: 400, quantity: 2, material: "МДФ", material_confirmed: true, color: "белый", finish: "матовый"
material: {raw: "МДФ", confirmed: true}
color: {raw: "белый", structured: null}
flags: {}
```

### Fake #2 — Дерево ambiguous

```yaml
intake_id: "FAKE-002"
items:
  - height_mm: 600, width_mm: 400, quantity: 5, material: "дерево", material_confirmed: false, color: "белый"
material: {raw: "дерево", confirmed: false}
color: {raw: "белый", structured: null}
flags: {material_question: true}
```

### Fake #3 — С RAL

```yaml
intake_id: "FAKE-003"
items:
  - height_mm: 800, width_mm: 500, quantity: 3, material: "МДФ", material_confirmed: true, color: "RAL 9010", finish: "матовый"
material: {raw: "МДФ", confirmed: true}
color: {raw: "RAL 9010", structured: "RAL 9010"}
flags: {}
```

### Fake #4 — Две позиции, одна спорная

```yaml
intake_id: "FAKE-004"
items:
  - height_mm: 1000, width_mm: 400, quantity: 2, material: "МДФ", material_confirmed: true, color: "RAL 9010", finish: "матовый"
  - height_mm: 600, width_mm: 300, quantity: 1, material: "дерево", material_confirmed: false, color: "коричневый", finish: "глянцевый"
material: {raw: "МДФ", confirmed: true}
color: {raw: "RAL 9010", structured: "RAL 9010"}
flags: {material_question: true}
```

### Fake #5 — Discount request

```yaml
intake_id: "FAKE-005"
items:
  - height_mm: 1000, width_mm: 400, quantity: 10, material: "МДФ", material_confirmed: true, color: "RAL 9010", finish: "глянцевый"
material: {raw: "МДФ", confirmed: true}
color: {raw: "RAL 9010", structured: "RAL 9010"}
flags: {discount_request: true}
```

### Fake #6 — Technical advice

```yaml
intake_id: "FAKE-006"
items:
  - height_mm: 800, width_mm: 500, quantity: 4, material: "МДФ", material_confirmed: true, color: "белый", finish: "матовый"
material: {raw: "МДФ", confirmed: true}
color: {raw: "белый", structured: null}
flags: {technical_advice_requested: true, manager_review_required: true}
```

### Fake #7 — Manager review

```yaml
intake_id: "FAKE-007"
items:
  - height_mm: 1200, width_mm: 600, quantity: 1, material: "МДФ", material_confirmed: true, color: "RAL 7016", finish: "матовый"
material: {raw: "МДФ", confirmed: true}
color: {raw: "RAL 7016", structured: "RAL 7016"}
flags: {manager_review_required: true}
```

### Fake #8 — Только покраска

```yaml
intake_id: "FAKE-008"
items:
  - height_mm: 1000, width_mm: 400, quantity: 4, material: "МДФ", material_confirmed: true, color: "белый", finish: "матовый"
material: {raw: "МДФ", confirmed: true}
color: {raw: "белый", structured: null}
flags: {}
```

### Fake #9 — Фасады под ключ (нет данных)

```yaml
intake_id: "FAKE-009"
items: []
material: {raw: null, confirmed: false}
color: {raw: null, structured: null}
flags: {manager_review_required: true}
```

### Fake #10 — Всё чисто, 3 позиции

```yaml
intake_id: "FAKE-010"
items:
  - height_mm: 1000, width_mm: 400, quantity: 4, material: "МДФ", material_confirmed: true, color: "RAL 9010", finish: "матовый"
  - height_mm: 600, width_mm: 300, quantity: 2, material: "МДФ", material_confirmed: true, color: "RAL 8017", finish: "глянцевый"
  - height_mm: 800, width_mm: 500, quantity: 1, material: "МДФ", material_confirmed: true, color: "RAL 7016", finish: "матовый"
material: {raw: "МДФ", confirmed: true}
color: {raw: "RAL 9010", structured: "RAL 9010"}
flags: {}
```
