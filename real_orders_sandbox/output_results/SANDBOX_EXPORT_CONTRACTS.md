# Sandbox Export Contracts — GATE 2

Date: 2026-06-17

## ORDER_SAFE_COPY_001

```yaml
export_contract:
  ready_for_corel: true
  corel_rows: 3
  row_order: height_mm, width_mm, quantity
  not_final_export: true
  production_ready: false

corel_preview: |
  Corel Export Preview (3 rows)
  ----------------------------------------
    1. 1000×400 mm, ×1, МДФ, RAL 9010, матовый
    2. 4×600 mm, ×1, МДФ, RAL 9010
    3. 300×2 mm, ×1, МДФ, RAL 9010
  ----------------------------------------
  Status: ready
  not_final_export: true
```

## Notes

- Row order: height_mm, width_mm, quantity ✅
- Preview: H×W ✅
- Size parsing: "x quantity" edge case (future improvement)
- ALL results: not_final / review_required / NOT production
