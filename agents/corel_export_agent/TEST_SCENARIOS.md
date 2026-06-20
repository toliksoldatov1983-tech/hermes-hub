# Corel Export Agent — TEST SCENARIOS

Date: 2026-06-17
Agent: Corel Export Agent (#3, `accepted`, not active)

## 10 Test Scenarios

### #1 — Single confirmed row
```yaml
input: 1 confirmed row (1000×400, МДФ, RAL 9010, 0.8 м²)
expected: export_contract with 1 item, ready_for_corel=true
```

### #2 — Multiple confirmed rows
```yaml
input: 3 confirmed rows (total 2.36 м²)
expected: export_contract with 3 items
```

### #3 — Export blocked (disputed data)
```yaml
input: order_result with export_blocked=true
expected: export_contract with ready_for_corel=false
```

### #4 — Empty result
```yaml
input: 0 confirmed rows
expected: export_contract with 0 items
```

### #5 — Mixed finish (матовый + глянцевый)
```yaml
input: 2 rows, разные finish
expected: finish preserved per item
```

### #6 — Raw color (no RAL)
```yaml
input: color_raw="белый", color_structured=null
expected: color note = "белый (уточнить RAL)"
```

### #7 — Corel format transform
```yaml
input: height_mm=1000, width_mm=400
expected: width_mm=400, height_mm=1000 (Corel order: W×H)
```

### #8 — Multiple quantities
```yaml
input: quantity=4
expected: label includes "×4 шт"
```

### #9 — Material note
```yaml
input: material="МДФ", material_confirmed=true
expected: material_note="МДФ"
```

### #10 — Not ready for Corel
```yaml
input: export_blocked=true or 0 confirmed rows
expected: ready_for_corel=false, empty items list
```
