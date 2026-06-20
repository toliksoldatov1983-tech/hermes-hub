# Malyarka Clean Order Result Rules

Updated: 2026-06-13

Status: planning only. No working `order_result` logic, functions, classes or tests are defined here.

## Purpose

This document fixes how the parser, dispute detector and area calculator should later combine into one final order result.

## Common Input

The future `order_result` step accepts:

```text
raw_order_text
order_lines
parse_result
confirmed_rows
disputed_rows
area_calculation_result
```

Meanings:

- `raw_order_text`: original user text.
- `order_lines`: normalized lines prepared from the raw text.
- `parse_result`: raw result from local parser/dispute detector.
- `confirmed_rows`: rows safe for calculation.
- `disputed_rows`: rows that need user review.
- `area_calculation_result`: total area and per-row calculated area for confirmed rows only.

## Final Result Fields

The future final result should return:

```text
status
confirmed_rows
disputed_rows
total_area_m2
export_blocked
short_summary
dispute_reasons
```

Optional later fields:

```text
source
raw_text
warnings
next_action
```

## Statuses

Allowed statuses:

```text
clean
has_disputes
empty_or_invalid
```

## Rules

1. If there are no confirmed rows and no disputed rows, status is `empty_or_invalid`.
2. If there are disputed rows, status is `has_disputes`.
3. If there are disputed rows, `export_blocked = true`.
4. If there are no disputed rows and there is at least one confirmed row, status is `clean`.
5. Area is calculated only from confirmed rows.
6. Disputed rows never enter area calculation.
7. Final export is blocked while disputed rows exist.
8. Dispute reasons must be visible in the result.
9. Do not calculate price, LKM, materials or costs.
10. Do not create Excel/Corel files in this step.

## Minimal Examples

### Clean Order

Input:

```text
raw_order_text: 1000 400 2
confirmed_rows:
  - height: 1000
    width: 400
    quantity: 2
disputed_rows: []
area_calculation_result:
  total_area_m2: 0.8
```

Expected result:

```text
status: clean
confirmed_rows: 1
disputed_rows: 0
total_area_m2: 0.8
export_blocked: false
short_summary: 1 confirmed row, 0.8 m2 total
dispute_reasons: []
```

### Order With Dispute

Input:

```text
raw_order_text:
  1000 400
  1000
confirmed_rows:
  - height: 1000
    width: 400
    quantity: 1
disputed_rows:
  - reason: missing_width
area_calculation_result:
  total_area_m2: 0.4
```

Expected result:

```text
status: has_disputes
confirmed_rows: 1
disputed_rows: 1
total_area_m2: 0.4
export_blocked: true
short_summary: 1 confirmed row, 1 disputed row, export blocked
dispute_reasons:
  - missing_width
```

### Empty Or Garbage Order

Input:

```text
raw_order_text:
confirmed_rows: []
disputed_rows: []
area_calculation_result:
  total_area_m2: 0
```

Expected result:

```text
status: empty_or_invalid
confirmed_rows: 0
disputed_rows: 0
total_area_m2: 0
export_blocked: true
short_summary: no valid order rows found
dispute_reasons: []
```

## Not Included

This planning step does not include:

```text
Excel/Corel file
Telegram
Vision
API
database
prices
LKM
materials
old Malyarka
```

## Implementation Boundary

Later implementation may use this document to implement `order_result.py` and focused tests.

This package does not create:

```text
working order_result logic
functions
classes
new tests
application launch
```
