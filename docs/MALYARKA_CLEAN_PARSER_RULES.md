# Malyarka Clean Parser Rules

Updated: 2026-06-12

Status: planning only. No working parser logic, functions, classes or tests are defined here.

## Purpose

This document fixes the first local parsing rules for text orders before implementation starts.

Parser scope:

```text
plain text line -> height -> width -> quantity -> confirmed or disputed row
```

## Clear Size Formats

These formats are considered understandable:

```text
1000 400
1000 400 2
1000x400
1000 x 400
1000*400
1000×400
```

Meaning:

- `1000 400` means height `1000`, width `400`, quantity `1`.
- `1000 400 2` means height `1000`, width `400`, quantity `2`.
- `1000x400`, `1000 x 400`, `1000*400`, `1000×400` mean height `1000`, width `400`, quantity `1`.

## Base Rules

1. First number is height.
2. Second number is width.
3. Third number is quantity.
4. If quantity is not specified, quantity is `1`.
5. Disputed data must not be guessed.
6. The local parser must stay separate from AI parsing.
7. Prices, materials and comments must not be mixed into size parsing.

## Disputed Lines

A line should become disputed if:

- height is missing;
- width is missing;
- there are too many numbers;
- quantity is unclear;
- text affects the order but is not parsed;
- line is empty or garbage.

## Short Dispute Reasons

Use these short reason codes:

```text
missing_height
missing_width
too_many_numbers
unclear_quantity
unparsed_order_text
empty_or_garbage
unsupported_format
```

Meanings:

- `missing_height`: no usable first size number.
- `missing_width`: no usable second size number.
- `too_many_numbers`: more numbers than the first parser version can safely understand.
- `unclear_quantity`: quantity exists but cannot be trusted.
- `unparsed_order_text`: meaningful order text remains outside parsed sizes.
- `empty_or_garbage`: line has no useful order information.
- `unsupported_format`: line looks like an order but the format is not yet supported.

## Minimal Examples

### Example 1

Input:

```text
1000 400
```

Expected:

```text
status: clean
confirmed_rows:
  - height: 1000
    width: 400
    quantity: 1
disputed_rows: []
```

### Example 2

Input:

```text
1000 400 2
```

Expected:

```text
status: clean
confirmed_rows:
  - height: 1000
    width: 400
    quantity: 2
disputed_rows: []
```

### Example 3

Input:

```text
1000x400
```

Expected:

```text
status: clean
confirmed_rows:
  - height: 1000
    width: 400
    quantity: 1
disputed_rows: []
```

### Example 4

Input:

```text
1000 x 400
```

Expected:

```text
status: clean
confirmed_rows:
  - height: 1000
    width: 400
    quantity: 1
disputed_rows: []
```

### Example 5

Input:

```text
1000*400
```

Expected:

```text
status: clean
confirmed_rows:
  - height: 1000
    width: 400
    quantity: 1
disputed_rows: []
```

### Example 6

Input:

```text
1000×400
```

Expected:

```text
status: clean
confirmed_rows:
  - height: 1000
    width: 400
    quantity: 1
disputed_rows: []
```

### Example 7

Input:

```text
1000
```

Expected:

```text
status: has_disputes
confirmed_rows: []
disputed_rows:
  - reason: missing_width
```

### Example 8

Input:

```text
1000 400 2 5
```

Expected:

```text
status: has_disputes
confirmed_rows: []
disputed_rows:
  - reason: too_many_numbers
```

### Example 9

Input:

```text
срочно 1000 400
```

Expected:

```text
status: has_disputes
confirmed_rows: []
disputed_rows:
  - reason: unparsed_order_text
```

Note:

If later the user confirms that some words are safe comments, a separate rule can move them to notes. For the first parser version, meaningful text is disputed.

### Example 10

Input:

```text

```

Expected:

```text
status: empty_or_invalid
confirmed_rows: []
disputed_rows:
  - reason: empty_or_garbage
```

## Not Included

The first local parser rules do not include:

```text
prices
cost
LKM
materials
Telegram
Vision
API
old Malyarka
AI parsing
database
Corel automation
Excel export
```

## Implementation Boundary

Later implementation may use these rules to create local parser code and tests.

This package does not create:

```text
functions
classes
tests
working parser logic
application launch
```
