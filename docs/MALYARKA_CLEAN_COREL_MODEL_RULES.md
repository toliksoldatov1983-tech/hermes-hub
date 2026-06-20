# Malyarka Clean Corel Model Rules

Planning package:

```text
BATCH_015_COREL_EXPORT_MODEL_PLANNING
```

Status:

```text
planning only
```

This document describes the neutral data model for a future Corel export. It does not implement export logic.

## Purpose

The future Corel export should receive only clean, confirmed order data from the final order result.

Minimal flow:

```text
order_result -> corel_export_model -> future Corel export
```

## Source Data

Future Corel export should read from the final order result created by `order_result`.

Required fields from order result:

```text
status
confirmed_rows
disputed_rows
export_blocked
```

Optional reference fields:

```text
total_area_m2
short_summary
dispute_reasons
```

## Rows Allowed For Corel

Only confirmed rows may be prepared for Corel.

Rules:

```text
confirmed_rows -> allowed
disputed_rows -> not allowed
```

Disputed rows are never included in the future Corel model.

## Required Corel Row Fields

Each future Corel row needs only these fields:

```text
height_mm
width_mm
quantity
```

Meaning:

| Field | Meaning |
|---|---|
| `height_mm` | Height in millimeters. |
| `width_mm` | Width in millimeters. |
| `quantity` | Number of repeated items. |

## Export Blocking Rules

Corel rows may be prepared only when the order is clean.

Rules:

```text
if disputed_rows exists -> export_blocked = true
if export_blocked = true -> Corel export is not prepared
if status = clean -> Corel rows may be prepared
```

## Future Corel Row Format

Future Corel rows should be neutral data, not a real Corel file.

Minimal row shape:

```text
height_mm
width_mm
quantity
```

Example:

```text
height_mm: 1000
width_mm: 400
quantity: 2
```

## Minimal Examples

Clean order:

```text
input:
status = clean
confirmed_rows = [{ height_mm: 1000, width_mm: 400, quantity: 2 }]
disputed_rows = []
export_blocked = false

future corel rows:
[{ height_mm: 1000, width_mm: 400, quantity: 2 }]
```

Order with disputes:

```text
input:
status = has_disputes
confirmed_rows = [{ height_mm: 1000, width_mm: 400, quantity: 1 }]
disputed_rows = [{ raw_text: "1000", reason: "missing_width" }]
export_blocked = true

future corel rows:
not prepared
```

Empty or invalid order:

```text
input:
status = empty_or_invalid
confirmed_rows = []
disputed_rows = []
export_blocked = true

future corel rows:
not prepared
```

## What Is Not Included

This package does not include:

```text
Excel file
real Corel export
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

## Implementation Boundary

No working export code is written in this package.

No functions, classes, tests, files for Corel, Excel files or application launch are created here.
