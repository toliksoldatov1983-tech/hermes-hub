# Malyarka Clean Core Contracts

Updated: 2026-06-12

Status: planning only. No working logic, functions, classes or tests are defined here.

## Purpose

This document fixes the minimum data contracts between future Malyarka Clean modules before implementation starts.

Core flow:

```text
text order -> parse sizes -> disputed rows -> area -> Corel export -> tests
```

## Order Statuses

```text
clean
has_disputes
empty_or_invalid
```

Meanings:

- `clean`: input was parsed and all rows are confirmed.
- `has_disputes`: input has at least one unclear row that must be reviewed by the user.
- `empty_or_invalid`: input is empty or cannot be treated as an order.

## order_input

Accepts:

- raw order text from the user;
- optional source label, for example manual input, future Telegram, or pasted text;
- optional received timestamp.

Returns:

- normalized raw text without changing meaning;
- input metadata;
- preliminary status if text is empty or invalid;
- list of original lines for later traceability.

Must not:

- parse sizes deeply;
- calculate area;
- guess missing values;
- call AI, Telegram, Vision, API or database.

## size_parser

Accepts:

- normalized order text;
- original lines from `order_input`.

Returns:

- candidate parsed rows;
- unparsed fragments;
- parsing notes;
- references to original line numbers.

Must not:

- silently fix doubtful rows;
- calculate final area;
- decide final order status alone;
- use AI as part of the local parser.

## dispute_detector

Accepts:

- candidate parsed rows from `size_parser`;
- unparsed fragments;
- parsing notes.

Returns:

- confirmed rows;
- disputed rows;
- reason for each dispute;
- suggested user question if clarification is needed;
- status hint: `clean`, `has_disputes`, or `empty_or_invalid`.

Must not:

- mix confirmed rows with disputed rows;
- hide doubtful rows;
- invent dimensions or quantities.

## area_calculator

Accepts:

- confirmed rows only.

Returns:

- confirmed rows with calculated area fields;
- total area;
- calculation notes.

Must not:

- calculate disputed rows as confirmed;
- calculate prices or costs;
- change source dimensions;
- prepare Corel export directly.

## corel_export_model

Accepts:

- confirmed rows with area;
- order-level metadata;
- optional layout/export preferences for future use.

Returns:

- neutral Corel export data model;
- objects/layers/text labels planned for future Corel output;
- export readiness flag.

Must not:

- create a real Corel file yet;
- mix Corel structure with Excel file logic;
- call Corel, COM automation, API or external services.

## order_result

Accepts:

- normalized input metadata;
- confirmed rows;
- disputed rows;
- total area;
- Corel export model readiness.

Returns:

- final order result object shape;
- final status;
- user-facing summary;
- next action recommendation.

Must not:

- overwrite source data;
- hide disputed rows;
- launch exports, bots, APIs or databases.

## Confirmed Row Fields

Minimum fields:

```text
row_id
source_line
raw_text
width
height
quantity
unit
area_each
area_total
notes
```

Rules:

- confirmed row is safe for area calculation;
- width, height and quantity must be explicit or safely derived by a documented local rule;
- confirmed row is separate from disputed row.

## Disputed Row Fields

Minimum fields:

```text
dispute_id
source_line
raw_text
reason
parsed_fragment
missing_fields
suggested_question
severity
```

Rules:

- disputed row is not used for final area;
- disputed row must remain visible to the user;
- every dispute needs a reason.

## Final Order Result Fields

Minimum fields:

```text
order_id
source
status
raw_text
confirmed_rows
disputed_rows
total_area
corel_export_ready
summary
next_action
warnings
```

Rules:

- `status` must be one of `clean`, `has_disputes`, `empty_or_invalid`;
- result must show what was confirmed and what still needs user review;
- result does not include price/cost in the first implementation.

## First Implementation Boundary

Allowed later:

- local parsing logic;
- local dispute detection;
- local area calculation;
- tests for local rules.

Not included yet:

```text
Telegram
Vision
API
database
prices
old bot.py
old Malyarka as active system
Corel automation
Excel export
```
