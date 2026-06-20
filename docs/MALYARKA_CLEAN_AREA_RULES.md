# Malyarka Clean Area Rules

Updated: 2026-06-12

Status: planning only. No working calculation logic, functions, classes or tests are defined here.

## Purpose

This document fixes the first area calculation rules for confirmed Malyarka Clean rows before implementation starts.

## Inputs

The future area calculator needs only confirmed rows with these fields:

```text
height_mm
width_mm
quantity
```

Accepted mapping from current confirmed row fields:

```text
height -> height_mm
width -> width_mm
quantity -> quantity
```

## Formula

```text
area_m2 = height_mm * width_mm * quantity / 1_000_000
```

## Rules

1. Calculate area only for confirmed rows.
2. Disputed rows do not enter area calculation.
3. If there are no confirmed rows, total area is `0`.
4. If the whole input is empty or invalid, result status may stay `empty_or_invalid`.
5. If confirmed and disputed rows exist together, show area for confirmed rows only.
6. If disputed rows exist, final export remains blocked until the user resolves them.
7. Do not calculate cost.
8. Do not calculate prices.
9. Do not calculate LKM.
10. Do not calculate materials.

## Future area_calculator Output Fields

For each confirmed row:

```text
row_id
height_mm
width_mm
quantity
area_m2
calculation_note
```

For the whole order:

```text
total_area_m2
calculated_rows
excluded_disputed_rows
export_blocked
export_block_reason
warnings
```

## Minimal Examples

### Example 1

Input confirmed row:

```text
height_mm: 1000
width_mm: 400
quantity: 1
```

Expected:

```text
area_m2: 0.4
total_area_m2: 0.4
export_blocked: false
```

### Example 2

Input confirmed row:

```text
height_mm: 1000
width_mm: 400
quantity: 2
```

Expected:

```text
area_m2: 0.8
total_area_m2: 0.8
export_blocked: false
```

### Example 3

Input confirmed rows:

```text
1000 x 400 x 1 = 0.4
500 x 300 x 2 = 0.3
```

Expected:

```text
total_area_m2: 0.7
export_blocked: false
```

### Example 4

Input:

```text
confirmed:
  1000 x 400 x 1 = 0.4
disputed:
  1000
```

Expected:

```text
total_area_m2: 0.4
export_blocked: true
export_block_reason: unresolved_disputes
```

## Not Included

The first area calculation planning does not include:

```text
cost
prices
LKM
materials
Excel/Corel file
Telegram
Vision
API
database
old Malyarka
```

## Implementation Boundary

Later implementation may use these rules to create local area calculation code and focused tests.

This package does not create:

```text
working calculation logic
functions
classes
new tests
application launch
```
