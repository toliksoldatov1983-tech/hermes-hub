# Malyarka Clean Corel Model Implementation Plan

Planning package:

```text
BATCH_017_COREL_MODEL_IMPLEMENTATION_PLANNING
```

Status:

```text
planning only
```

This document plans a safe future implementation of the Corel model. It does not write code, tests or real export files.

## Purpose

The future Corel model should transform a clean final order result into neutral Corel-ready rows.

It must not create a real Corel file.

Minimal future flow:

```text
order_result -> corel_export_model -> neutral corel_rows
```

## Source Documents

This plan is based on:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_COREL_MODEL_RULES.md
E:\Hermes-Hub\docs\MALYARKA_CLEAN_ORDER_RESULT_RULES.md
E:\Hermes-Hub\ЗАЩИТА_ПРОЕКТА.md
```

## 1. How The Future Corel Model Reads Data

The future Corel model should accept the final result returned by `order_result`.

Required input fields:

```text
status
confirmed_rows
disputed_rows
export_blocked
```

The model should not parse raw text itself.
The model should not calculate area itself.
The model should not decide disputed rows itself.

It only receives already prepared order data and decides whether neutral Corel rows can be prepared.

## 2. Conditions That Allow Corel Rows

Corel rows may be prepared only when all conditions are true:

```text
status = clean
disputed_rows is empty
export_blocked = false
```

If these conditions are true, the model may transform `confirmed_rows` into `corel_rows`.

## 3. Conditions That Block Corel Rows

Corel rows must be blocked when any condition is true:

```text
disputed_rows is not empty
export_blocked = true
status = has_disputes
status = empty_or_invalid
```

Blocked result means:

```text
corel_rows = []
export_blocked = true
reason = short clear reason
```

## 4. Future Corel Row Fields

Each future Corel row must contain:

```text
height_mm
width_mm
quantity
```

The future implementation should copy these fields from confirmed rows.

The future implementation should not add:

```text
price
cost
material
LKM
client data
file paths
real Corel commands
```

## 5. Future Function Result

The future Corel model function should return:

```text
corel_rows
export_blocked
reason
source_status
```

Field meanings:

| Field | Meaning |
|---|---|
| `corel_rows` | Neutral rows prepared from confirmed rows, or empty list when blocked. |
| `export_blocked` | `true` when Corel rows must not be prepared. |
| `reason` | Short reason explaining allowed or blocked state. |
| `source_status` | Original `status` from `order_result`. |

## 6. Minimal Examples

Clean order:

```text
input:
status = clean
confirmed_rows = [{ height_mm: 1000, width_mm: 400, quantity: 2 }]
disputed_rows = []
export_blocked = false

output:
corel_rows = [{ height_mm: 1000, width_mm: 400, quantity: 2 }]
export_blocked = false
reason = ready
source_status = clean
```

Order with disputed rows:

```text
input:
status = has_disputes
confirmed_rows = [{ height_mm: 1000, width_mm: 400, quantity: 1 }]
disputed_rows = [{ raw_text: "1000", reason: "missing_width" }]
export_blocked = true

output:
corel_rows = []
export_blocked = true
reason = disputed_rows_present
source_status = has_disputes
```

Empty order:

```text
input:
status = empty_or_invalid
confirmed_rows = []
disputed_rows = []
export_blocked = true

output:
corel_rows = []
export_blocked = true
reason = source_not_clean
source_status = empty_or_invalid
```

## 7. Focused Tests Needed Later

When implementation is allowed, add focused tests for:

1. Clean order returns Corel rows.
2. Clean order copies only `height_mm`, `width_mm`, `quantity`.
3. Order with disputed rows returns empty `corel_rows` and `export_blocked = true`.
4. Order with `export_blocked = true` returns empty `corel_rows`.
5. Order with `status = has_disputes` is blocked.
6. Order with `status = empty_or_invalid` is blocked.
7. Disputed rows are never included in `corel_rows`.

## 8. What Is Not Included

This plan does not include:

```text
real Excel file
real Corel file
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

## 9. Safety Rule

Future implementation may create only neutral data structures unless the user gives separate permission for real Corel or Excel export.

Real production export is a risky future layer and must follow:

```text
plan -> user permission -> implementation -> report -> accept/reject
```
