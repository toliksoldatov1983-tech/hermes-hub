# Malyarka Agent — Demo Inputs

Date: 2026-06-17
Status: offline demo (no server, no live, no real orders)

## 10 Fake Intake Cards for Demo

---

### Demo #1 — Simple MDF
```yaml
intake_id: "DEMO-001"
items:
  - height_mm: 1000, width_mm: 400, quantity: 2, material: "МДФ", material_confirmed: true, color: "белый", finish: "матовый"
material: {raw: "МДФ", confirmed: true}
color: {raw: "белый", structured: null}
flags: {}
```

### Demo #2 — Ambiguous Wood
```yaml
intake_id: "DEMO-002"
items:
  - height_mm: 600, width_mm: 400, quantity: 5, material: "дерево", material_confirmed: false, color: "белый"
material: {raw: "дерево", confirmed: false}
color: {raw: "белый", structured: null}
flags: {material_question: true}
```

### Demo #3 — With RAL
```yaml
intake_id: "DEMO-003"
items:
  - height_mm: 800, width_mm: 500, quantity: 3, material: "МДФ", material_confirmed: true, color: "RAL 9010", finish: "матовый"
material: {raw: "МДФ", confirmed: true}
color: {raw: "RAL 9010", structured: "RAL 9010"}
flags: {}
```

### Demo #4 — Mixed (1 confirmed + 1 disputed)
```yaml
intake_id: "DEMO-004"
items:
  - height_mm: 1000, width_mm: 400, quantity: 2, material: "МДФ", material_confirmed: true, color: "RAL 9010", finish: "матовый"
  - height_mm: 600, width_mm: 300, quantity: 1, material: "дерево", material_confirmed: false, color: "коричневый", finish: "глянцевый"
material: {raw: "МДФ", confirmed: true}
color: {raw: "RAL 9010", structured: "RAL 9010"}
flags: {material_question: true}
```

### Demo #5 — Discount
```yaml
intake_id: "DEMO-005"
items:
  - height_mm: 1000, width_mm: 400, quantity: 10, material: "МДФ", material_confirmed: true, color: "RAL 9010", finish: "глянцевый"
material: {raw: "МДФ", confirmed: true}
color: {raw: "RAL 9010", structured: "RAL 9010"}
flags: {discount_request: true}
```

### Demo #6 — Technical Advice
```yaml
intake_id: "DEMO-006"
items:
  - height_mm: 800, width_mm: 500, quantity: 4, material: "МДФ", material_confirmed: true, color: "белый", finish: "матовый"
material: {raw: "МДФ", confirmed: true}
color: {raw: "белый", structured: null}
flags: {technical_advice_requested: true, manager_review_required: true}
```

### Demo #7 — Manager Review
```yaml
intake_id: "DEMO-007"
items:
  - height_mm: 1200, width_mm: 600, quantity: 1, material: "МДФ", material_confirmed: true, color: "RAL 7016", finish: "матовый"
material: {raw: "МДФ", confirmed: true}
color: {raw: "RAL 7016", structured: "RAL 7016"}
flags: {manager_review_required: true}
```

### Demo #8 — Paint Only
```yaml
intake_id: "DEMO-008"
items:
  - height_mm: 1000, width_mm: 400, quantity: 4, material: "МДФ", material_confirmed: true, color: "белый", finish: "матовый"
material: {raw: "МДФ", confirmed: true}
color: {raw: "белый", structured: null}
flags: {}
```

### Demo #9 — No Data
```yaml
intake_id: "DEMO-009"
items: []
material: {raw: null, confirmed: false}
color: {raw: null, structured: null}
flags: {manager_review_required: true}
```

### Demo #10 — All Clean (3 позиции)
```yaml
intake_id: "DEMO-010"
items:
  - height_mm: 1000, width_mm: 400, quantity: 4, material: "МДФ", material_confirmed: true, color: "RAL 9010", finish: "матовый"
  - height_mm: 600, width_mm: 300, quantity: 2, material: "МДФ", material_confirmed: true, color: "RAL 8017", finish: "глянцевый"
  - height_mm: 800, width_mm: 500, quantity: 1, material: "МДФ", material_confirmed: true, color: "RAL 7016", finish: "матовый"
material: {raw: "МДФ", confirmed: true}
color: {raw: "RAL 9010", structured: "RAL 9010"}
flags: {}
```
