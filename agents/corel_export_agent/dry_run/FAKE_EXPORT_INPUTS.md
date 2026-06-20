# Fake Export Inputs — Corel Dry-Run

Date: 2026-06-17

### Input #1 — Single position
```yaml
confirmed_rows:
  - height_mm: 1000, width_mm: 400, quantity: 4, material: "МДФ", color: "RAL 9010", finish: "матовый"
disputed_rows: []
export_blocked: false
manager_review_required: false
not_final_order: true
```

### Input #2 — Two positions
```yaml
confirmed_rows:
  - height_mm: 1000, width_mm: 400, quantity: 2, material: "МДФ", color: "RAL 9010", finish: "матовый"
  - height_mm: 600, width_mm: 300, quantity: 1, material: "МДФ", color: "RAL 8017", finish: "глянцевый"
disputed_rows: []
export_blocked: false
not_final_order: true
```

### Input #3 — Blocked (disputed)
```yaml
confirmed_rows:
  - height_mm: 1000, width_mm: 400, quantity: 2, material: "МДФ", color: "RAL 9010"
disputed_rows:
  - height_mm: 600, width_mm: 300, quantity: 1, material: "дерево"
export_blocked: true
not_final_order: true
```

### Input #4 — Three positions (best case)
```yaml
confirmed_rows:
  - height_mm: 1000, width_mm: 400, quantity: 4, material: "МДФ", color: "RAL 9010", finish: "матовый"
  - height_mm: 600, width_mm: 300, quantity: 2, material: "МДФ", color: "RAL 8017", finish: "глянцевый"
  - height_mm: 800, width_mm: 500, quantity: 1, material: "МДФ", color: "RAL 7016", finish: "матовый"
disputed_rows: []
export_blocked: false
not_final_order: true
```
