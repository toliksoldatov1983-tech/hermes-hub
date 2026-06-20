# Full-Chain Outputs

Date: 2026-06-17 | Tests: 12/12 (0.07s)

## Summary

| # | Message | Sales | Malyarka | Corel | Area |
|---|---------|-------|----------|-------|------|
| 1 | All clear | ✅ | ✅ | ✅ 1 row | 1.6 |
| 2 | Two positions | ✅ | ✅ | ✅ 2 rows | 0.98 |
| 3 | Three positions | ✅ | ✅ | ✅ 3 rows | 2.36 |
| 4 | Discount | ❌ | — | — | — |
| 5 | Tech advice | ❌ | — | — | — |
| 6 | No sizes | ❌ | — | — | — |
| 7 | Ambiguous wood | ❌ | — | — | — |
| 8 | Paint only | ✅ | ✅ | ✅ 1 row | 1.6 |
| 9 | Old facades | ❌ | — | — | — |
| 10 | Incomplete | ❌ | — | — | — |

## Full Chain: 4/10 (40%)

### #3 — Best case
```
Sales → ready_for_review → ✅
Malyarka → ready_for_human_review, 2.36 m² → ✅
Corel → ready_for_corel=true, 3 rows (H×W)
  1000×400 mm, ×4, МДФ, RAL 9010
  600×300 mm, ×2, МДФ, RAL 9010
  800×500 mm, ×1, МДФ, RAL 9010
```

## Row Order: height_mm, width_mm, quantity ✅
