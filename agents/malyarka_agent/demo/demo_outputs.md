# Malyarka Agent — Demo Outputs

Date: 2026-06-17

| # | Status | Confirmed | Disputed | Area (m²) | Export | Manager |
|---|--------|-----------|----------|-----------|--------|---------|
| 1 | ready_for_human_review | 1 | 0 | 0.8 | false | false |
| 2 | blocked_disputed_data | 0 | 1 | 0 | true | false |
| 3 | ready_for_human_review | 1 | 0 | 1.2 | false | false |
| 4 | blocked_disputed_data | 1 | 1 | 0.8 | true | false |
| 5 | blocked_disputed_data | 0 | 1 | 0 | true | true |
| 6 | blocked_disputed_data | 0 | 1 | 0 | true | true |
| 7 | blocked_disputed_data | 0 | 1 | 0 | true | true |
| 8 | ready_for_human_review | 1 | 0 | 1.6 | false | false |
| 9 | needs_clarification | 0 | 0 | 0 | true | true |
| 10 | ready_for_human_review | 3 | 0 | 2.36 | false | false |

## Expected outputs

### Demo #10 — All Clean (best case)
```yaml
status: ready_for_human_review
confirmed_rows: 3
total_area_m2: 2.36
export_blocked: false
not_final_order: true
```

### Demo #4 — Mixed
```yaml
status: blocked_disputed_data
confirmed_rows: 1 (МДФ, 0.8 м²)
disputed_rows: 1 (дерево, material_ambiguous)
export_blocked: true
not_final_order: true
```

### Demo #9 — No Data
```yaml
status: needs_clarification
confirmed_rows: 0
total_area_m2: 0
not_final_order: true
```
