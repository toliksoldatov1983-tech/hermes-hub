# Corel Export Agent — EXPORT CONTRACT

Date: 2026-06-17 | Status: `accepted`, not active

## Format

```yaml
export_contract:
  source: "malyarka_agent"
  target: "corel_export_agent"
  ready_for_corel: true
  corel_rows:
    - width_mm: 400   # Corel order: W×H
      height_mm: 1000
      quantity: 2
      area_m2: 0.8
      material: "МДФ"
      color: "RAL 9010"
      finish: "матовый"
  not_final_export: true
```

## Rules

- Only confirmed_rows → corel_rows
- Export order: **height_mm, width_mm, quantity**
- Preview shows: H×W (height first)
- export_blocked → ready_for_corel=false
- Always not_final_export: true
