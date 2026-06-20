# BATCH 002 - Malyarka Clean Architecture

Updated: 2026-06-12

Purpose:

Store the architecture `BATCH_PACKET` for the future clean Malyarka core.

Status:

```text
planning only
no code
no core files
no tests
no service launches
```

Execution status:

```text
executed by Codex on 2026-06-12
```

## Short Command For ChatGPT

Paste only this short command into ChatGPT:

```text
Прочитай файл BATCH_002_MALYARKA_CLEAN_ARCHITECTURE.md как архитектурный BATCH_PACKET по Malyarka Clean. Если ты не видишь файл, попроси меня загрузить или вставить его. После чтения дай короткую карточку прогресса и предложи следующий BATCH_PACKET для Codex только если нужна работа с файлами.
```

## BATCH_PACKET

```text
BATCH_PACKET:

GOAL:
Fix the modular architecture of the future clean Malyarka core without writing implementation code.

CURRENT CONTEXT:
Project: Hermes Hub / Malyarka Clean.
Root folder: E:\Hermes-Hub
Main source of truth: E:\Hermes-Hub\HERMES_HUB_STATE.md
This package is architecture planning only.

ACCEPTED DECISIONS:
- Build a clean new Malyarka core instead of continuing old bot.py.
- Old Malyarka is archive/source only, not active system.
- First core must be small and testable.
- First core flow:
  text order -> parse sizes -> disputed rows -> area -> Corel export -> tests
- Do not include Telegram, Vision, API, database, prices, LKM, reference books or old Malyarka as an active system in the first implementation.

TASKS:
1. Use this package as the architecture boundary for the first Malyarka Clean core.
2. Keep modules separate and simple.
3. Do not mix business concepts that should stay separate.
4. Prepare future implementation batches from this architecture only after user approval.

WHAT CODEX MAY DO WITHOUT ASKING:
- Read this architecture packet.
- Update planning documentation inside E:\Hermes-Hub.
- Prepare the next batch packet.
- Refresh CHATGPT_CONTEXT_BUNDLE.md.

WHAT CODEX MUST NOT TOUCH:
- .env
- orders.db
- .git
- tokens
- keys
- passwords
- Telegram launch
- Vision
- external APIs
- old bot.py
- old Malyarka as an active system

WHAT NEEDS USER CONFIRMATION:
- Writing the first code files.
- Creating tests.
- Reading old Malyarka folders.
- Using old Malyarka code as source.
- Connecting Telegram, Vision, APIs, database or Docker.
- Adding prices, LKM, reference books or CNC/ArtCam automation.

EXPECTED RESULT:
Everyone understands the planned module boundaries before implementation starts.

CHECKS:
- Confirm this is planning only.
- Confirm no code files were created.
- Confirm no tests were created or run.
- Confirm no forbidden files or services were touched.

FILES TO UPDATE:
E:\Hermes-Hub\handoff\BATCH_002_MALYARKA_CLEAN_ARCHITECTURE.md
E:\Hermes-Hub\handoff\CHATGPT_CONTEXT_BUNDLE.md
```

## General Flow

```text
text order -> parse sizes -> disputed rows -> area -> Corel export -> tests
```

Meaning:

1. User gives raw order text.
2. Parser extracts candidate size rows.
3. Dispute detector separates unclear rows from confirmed rows.
4. Area calculator calculates only confirmed rows.
5. Corel export model prepares neutral export data.
6. Tests check parser, dispute detection, area calculation and export model.

## Future Logical Modules

### 1. order_input

Purpose:

Receive and normalize raw order text before parsing.

Input:

```text
raw_text
source_label optional
received_at optional
```

Output:

```text
OrderInput
- raw_text
- normalized_text
- source_label
- warnings
```

Should do:

- keep original text;
- make a normalized copy for parsing;
- detect empty text;
- collect input-level warnings.

Should not do:

- calculate area;
- decide price;
- build Corel export;
- call AI.

### 2. size_parser

Purpose:

Extract possible size rows from normalized order text.

Input:

```text
OrderInput.normalized_text
```

Output:

```text
ParsedSizeRows
- confirmed_candidate_rows
- raw_fragments
- parser_warnings
```

Should do:

- find size-like fragments;
- parse width/height/count where possible;
- preserve raw fragments for review;
- mark parser uncertainty.

Should not do:

- silently guess disputed values;
- calculate price;
- export to Corel;
- use old bot.py logic directly.

### 3. dispute_detector

Purpose:

Separate confirmed rows from unclear/disputed rows.

Input:

```text
ParsedSizeRows
```

Output:

```text
DisputeReport
- confirmed_rows
- disputed_rows
- dispute_reasons
```

Should do:

- detect missing width/height/count;
- detect ambiguous separators or strange formats;
- detect impossible or suspicious values;
- keep disputed rows visible for the user.

Should not do:

- hide unclear rows;
- mix disputed rows into area totals;
- ask AI to guess final values in the first core.

### 4. area_calculator

Purpose:

Calculate area for confirmed rows only.

Input:

```text
DisputeReport.confirmed_rows
```

Output:

```text
AreaResult
- row_areas
- total_area
- calculation_warnings
```

Should do:

- calculate per-row area;
- calculate total area;
- use predictable rounding rules later;
- ignore disputed rows except for warning references.

Should not do:

- calculate price;
- include disputed rows as confirmed;
- know about Excel files;
- know about Telegram.

### 5. corel_export_model

Purpose:

Prepare neutral structured data for future Corel export.

Input:

```text
confirmed_rows
AreaResult
DisputeReport
```

Output:

```text
CorelExportModel
- export_rows
- labels
- dimensions
- warnings
```

Should do:

- describe what Corel will need later;
- keep export data separate from Excel and UI;
- include warning metadata.

Should not do:

- create real Corel files in the first planning stage;
- write Excel files;
- calculate prices;
- launch external programs.

### 6. order_result

Purpose:

Return one final result object for the processed order.

Input:

```text
OrderInput
ParsedSizeRows
DisputeReport
AreaResult
CorelExportModel
```

Output:

```text
OrderResult
- status
- confirmed_rows
- disputed_rows
- total_area
- corel_export_model
- warnings
```

Should do:

- combine module results;
- expose status clearly;
- keep confirmed and disputed data separate.

Should not do:

- hide uncertainty;
- start Telegram/API/database work;
- depend on old Malyarka.

### 7. tests

Purpose:

Protect the clean core behavior.

Input:

```text
sample order texts
expected parsed rows
expected dispute reports
expected area results
expected statuses
```

Output:

```text
test results
```

Should check:

- empty input;
- clean order;
- unclear order;
- strange separators;
- confirmed rows vs disputed rows;
- area calculation;
- Corel export model shape.

Should not do:

- run Telegram;
- call APIs;
- read `.env`;
- use real customer data without permission.

## Order Statuses

### clean

Use when:

- input is valid;
- at least one confirmed row exists;
- no disputed rows remain.

Meaning:

```text
The order can continue to area and export steps.
```

### has_disputes

Use when:

- at least one row is unclear;
- some values are missing, strange or ambiguous;
- confirmed rows may exist, but disputed rows need user review.

Meaning:

```text
The result is useful, but user review is required before final production.
```

### empty_or_invalid

Use when:

- text is empty;
- no size-like rows can be extracted;
- input is not usable as an order.

Meaning:

```text
The order cannot be processed yet.
```

## Things That Must Not Be Mixed

Do not mix:

- area and cost;
- Corel structure and Excel file;
- local parser and AI;
- new clean core and old `bot.py`;
- confirmed rows and disputed rows.

Reason:

Each part must stay testable, replaceable and easy to explain.

## Not Included In First Implementation

Do not include in the first implementation:

```text
Telegram
Vision
API
database
prices
LKM
reference books
old Malyarka as an active system
```

These belong to later phases after the clean core is stable.

## Codex Execution Result

Done:

- confirmed this package is architecture planning only;
- accepted the module boundary for the future clean core;
- confirmed the first flow stays:
  `text order -> parse sizes -> disputed rows -> area -> Corel export -> tests`;
- confirmed order statuses:
  `clean`, `has_disputes`, `empty_or_invalid`;
- confirmed forbidden mixing rules and first-version exclusions.

No implementation code was written.
No core files were created.
No tests were created or run.
No old Malyarka files were touched.
No `.env`, `orders.db`, `.git`, tokens, Telegram, Vision or APIs were touched.
