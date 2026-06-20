# Malyarka Clean Pipeline Smoke Test Plan

Planning package:

```text
BATCH_019_ORDER_PIPELINE_SMOKE_TEST_PLANNING
```

Status:

```text
planning only
```

This document plans a future smoke check for the minimal Malyarka Clean order pipeline.

No code, tests, export files or application launch are created in this package.

## Purpose

The future smoke check should verify that the minimal order chain works from text input to neutral Corel-ready data.

Minimal chain:

```text
raw order text
-> line parsing
-> confirmed rows
-> disputed rows
-> final order result
-> area calculation
-> Corel model
```

## 1. Full Chain To Check

The future smoke check should cover:

1. Raw text order.
2. Order line preparation.
3. Size parsing.
4. Confirmed rows.
5. Disputed rows.
6. Final order result.
7. Area calculation.
8. Neutral Corel model.

The check should not create a real Excel or Corel file.

## 2. Required Scenarios

The future smoke check needs three scenarios:

```text
clean order
order with disputed row
empty or garbage order
```

## 3. Clean Order Expected Result

Example:

```text
1000 400 2
```

Expected:

```text
status = clean
disputed_rows = []
export_blocked = false
total_area_m2 is calculated
corel_rows are ready
```

Expected area example:

```text
1000 * 400 * 2 / 1_000_000 = 0.8
```

Expected Corel model:

```text
corel_rows = [{ height_mm: 1000, width_mm: 400, quantity: 2 }]
export_blocked = false
reason = ready
source_status = clean
```

## 4. Order With Disputed Row Expected Result

Example:

```text
1000 400
1000
```

Expected:

```text
status = has_disputes
disputed_rows is not empty
area is calculated only for confirmed rows
export_blocked = true
corel_rows are not ready
```

Expected Corel model:

```text
corel_rows = []
export_blocked = true
reason = disputed_rows_present
source_status = has_disputes
```

## 5. Empty Or Garbage Order Expected Result

Examples:

```text
empty string
```

or:

```text
abc
```

Expected:

```text
status = empty_or_invalid
total_area_m2 = 0
export_blocked = true
corel_rows are not ready
```

Expected Corel model:

```text
corel_rows = []
export_blocked = true
source_status = empty_or_invalid
```

## 6. Focused Tests Needed Later

When implementation is allowed, add focused tests for:

1. Clean text order produces `status = clean`.
2. Clean text order produces `total_area_m2 = 0.8` for `1000 400 2`.
3. Clean text order produces one neutral Corel row.
4. Order with disputed row produces `status = has_disputes`.
5. Order with disputed row calculates area only for confirmed rows.
6. Order with disputed row blocks Corel rows.
7. Empty order produces `status = empty_or_invalid`.
8. Empty order produces `total_area_m2 = 0`.
9. Empty order blocks Corel rows.
10. No smoke test creates Excel/Corel files or writes export files to disk.

## 7. What Is Not Included

This smoke plan does not include:

```text
Excel file
Corel file
export to disk
Telegram
Vision
API
database
prices
cost
LKM
materials
old Malyarka as active system
old bot.py
```

## 8. Safety Rule

The future smoke test may call existing internal functions only.

It must not:

```text
launch the application
create export files
connect to external services
touch secrets
touch old Malyarka
```
