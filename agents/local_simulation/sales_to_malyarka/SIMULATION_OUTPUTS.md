# Sales → Malyarka Simulation Outputs

Date: 2026-06-17
Tests: 12/12 passed (0.07s)
Simulation: 10 messages, 4 passed, 6 blocked

## Summary

| # | Message | Sales Status | Handoff | Malyarka Status | Area |
|---|---------|-------------|---------|-----------------|------|
| 1 | All clear | ready_for_review | ✅ passed | ready_for_human_review | 1.6 |
| 2 | Two positions | ready_for_review | ✅ passed | ready_for_human_review | 0.98 |
| 3 | Ambiguous wood | needs_more_info | ❌ blocked | — | — |
| 4 | Discount | ready_for_review | ❌ blocked | — | — |
| 5 | Technical advice | needs_more_info | ❌ blocked | — | — |
| 6 | No sizes | needs_more_info | ❌ blocked | — | — |
| 7 | Incomplete | needs_more_info | ❌ blocked | — | — |
| 8 | Paint only | ready_for_review | ✅ passed | ready_for_human_review | 1.6 |
| 9 | Old facades | needs_more_info | ❌ blocked | — | — |
| 10 | Three positions | ready_for_review | ✅ passed | ready_for_human_review | 2.36 |

## Sample Outputs

### #10 — Best case (3 positions, all RAL)
```yaml
from: Sales Agent
to: Malyarka Agent
status: ready_for_human_review
confirmed_rows: 3
total_area_m2: 2.36
export_blocked: false
not_final_order: true
```

### #4 — Blocked by Sales (discount)
```yaml
sales_status: ready_for_review
handoff_ready: false
blocker: discount_request — менеджер должен подтвердить условия
passed_to_malyarka: false
```
