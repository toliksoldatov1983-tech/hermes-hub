# ChatGPT Context Bundle

Generated: 2026-06-20 07:17:36 +05:00

Generator:

~~~text
E:\Hermes-Hub\tools\Update-ChatGPTContextBundle.ps1
~~~

Use this file when ChatGPT cannot see local disk files.

This is a generated portable snapshot, not the main source of truth.

Main source of truth:

~~~text
E:\Hermes-Hub\HERMES_HUB_STATE.md
~~~

How ChatGPT should use this:

1. Read this bundle as the current project context.
2. Answer in Russian and simple words.
3. Show a short progress card regularly.
4. Prepare BATCH_PACKET for Codex instead of many small tasks.
5. Do not ask the user to remember hidden context.
6. If disk state is uncertain, ask Codex to verify files.

Important:

~~~text
Old Malyarka is archive-only.
Do not touch .env, orders.db, .git, tokens, keys, Telegram, Vision or APIs without separate permission.
~~~

---

## Source: HERMES_HUB_STATE.md

~~~markdown
# Hermes Hub State

Updated: 2026-06-12
Status: clean planning workspace created

## Project Name

Working name:

```text
Hermes Hub / Malyarka Clean
```

Final name is not fixed yet.

## Main Goal

Build a clean, safe, understandable system for future Malyarka work:

1. daily project thinking and planning;
2. clean Malyarka order-processing core;
3. future Telegram layer;
4. future Corel / Excel / CNC workflows;
5. future Hermes / Nous Portal workspace;
6. shared memory and task handoff between ChatGPT, Codex and Hermes.

## Current Phase

Phase 1: first local parser slice.

The first minimal local parser has been implemented inside the clean project only.

## Why We Restarted

The old workspace became noisy and risky:

- old Malyarka got real unreviewed changes;
- `start_bot.bat` previously contained a hardcoded Telegram token;
- `.env` and `orders.db` exist in the old project;
- some new modules tried to read secrets or call external APIs;
- old statuses contradicted real disk state.

The new project starts clean and treats old Malyarka only as an archive/source.

## Source Of Truth

These files are the current truth:

```text
E:\Hermes-Hub\HERMES_HUB_STATE.md
E:\Hermes-Hub\tasks\NEXT_TASKS.md
E:\Hermes-Hub\logs\WORKLOG.md
E:\Hermes-Hub\PROJECT_HINTS.md
E:\Hermes-Hub\SAFETY_RULES.md
E:\Hermes-Hub\docs\CHATGPT_CHAT_ROLES.md
E:\Hermes-Hub\docs\BATCH_WORKFLOW.md
```

Old audit references:

```text
E:\Hermes-General\logs\CODEX_AUDIT_2026-06-12.md
E:\Hermes-General\logs\MALYARKA_GIT_DIFF_REVIEW_2026-06-12.md
```

## Roles

| Role | Purpose |
|---|---|
| User | Makes final decisions and gives permissions |
| ChatGPT | Thinking partner, planning, task packets |
| Codex | Files, code, tests, audits, implementation |
| Hermes / Nous Portal | Future visual workspace and daily operating panel |
| DeepSeek / backup model | Reserve and independent review |

## ChatGPT Workspace

The ChatGPT project is named:

```text
HERMES HUB
```

The main ChatGPT chat for normal work is:

```text
Главный чат для работы
```

Chat roles are documented here:

```text
E:\Hermes-Hub\docs\CHATGPT_CHAT_ROLES.md
```

## Working Rule

ChatGPT discusses and prepares a task packet or batch packet.

Codex implements safe grouped work and verifies.

Hermes reads the state and continues from the same source of truth.

All important outcomes are written back to:

```text
E:\Hermes-Hub\HERMES_HUB_STATE.md
E:\Hermes-Hub\logs\WORKLOG.md
E:\Hermes-Hub\tasks\NEXT_TASKS.md
```

## Batch Mode

To avoid slow copy-paste between tools, normal work should happen in batches.

Batch rules:

```text
E:\Hermes-Hub\docs\BATCH_WORKFLOW.md
```

Batch template:

```text
E:\Hermes-Hub\handoff\BATCH_PACKET_TEMPLATE.md
```

Large batch packets should be stored as separate `.md` files in:

```text
E:\Hermes-Hub\handoff
```

Current executed batch:

```text
E:\Hermes-Hub\handoff\BATCH_001_HERMES_CONTEXT_HANDOFF.md
```

Executed architecture batch:

```text
E:\Hermes-Hub\handoff\BATCH_002_MALYARKA_CLEAN_ARCHITECTURE.md
```

Prepared scaffold batch:

```text
E:\Hermes-Hub\handoff\BATCH_003_MALYARKA_CLEAN_CORE_SCAFFOLD.md
```

Prepared simple handoff workflow batch:

```text
E:\Hermes-Hub\handoff\BATCH_004_SIMPLE_HANDOFF_WORKFLOW.md
```

Simple handoff files:

```text
E:\Hermes-Hub\handoff\ACTIVE_BATCH.md
E:\Hermes-Hub\handoff\REPORT_TO_CHATGPT.md
E:\Hermes-Hub\handoff\CHATGPT_CONTEXT_BUNDLE.md
```

Simple handoff mode status:

```text
enabled
```

Short command:

```text
Выполни ACTIVE_BATCH
```

Standing Codex rules:

```text
E:\Hermes-Hub\AGENTS.md
```

One-command workflow package:

```text
E:\Hermes-Hub\handoff\BATCH_005_ONE_COMMAND_CODEX_WORKFLOW.md
```

After each meaningful Codex batch, refresh the portable ChatGPT context bundle:

```text
E:\Hermes-Hub\tools\Update-ChatGPTContextBundle.ps1
```

Generated bundle:

```text
E:\Hermes-Hub\handoff\CHATGPT_CONTEXT_BUNDLE.md
```

After each meaningful Codex batch, prepare/update the latest acceptance patch:

```text
E:\Hermes-Hub\patches\LATEST_STATE_PATCH.md
```

Patch log:

```text
E:\Hermes-Hub\patches\PATCH_LOG.md
```

The patch is for ChatGPT review and does not replace state, bundle or report files.

## Malyarka Clean Architecture Plan

Status: planning block plus empty scaffold. No working application logic has been created yet.

The first clean core should follow this minimal flow:

## HERMES_PACKET_INBOX Transfer Rule

Status: active and installed

Installed at:

```text
C:\Users\user\Desktop\HERMES_PACKET_INBOX
```

Installed files/folders:

```text
01_INBOX_ZIP
02_EXTRACTED
03_ARCHIVE
04_LOGS
RUN_HERMES_PACKET_INBOX.cmd
INSTALL_OR_UPDATE_HERMES_PACKET_INBOX.ps1
LATEST_TASK_PATH.txt
OPEN_LATEST_TASK.cmd
```

Full rule:

```text
E:\Hermes-Hub\docs\HERMES_PACKET_INBOX_RULE.md
```

Summary:

- short tasks go as normal chat text;
- medium tasks first ask whether Codex/Hermes can accept approximately N characters in one message;
- large tasks, long handoffs, large markdown, many files/prohibitions, long server context, failed paste attempts, or text that does not fit should go through ZIP via `HERMES_PACKET_INBOX`;
- ZIP is not mandatory for every task;
- do not shorten important context or ask the user to paste large context in many parts when ZIP is the safer transfer method.

## Server Runtime Startup State

Date: 2026-06-20

Status: recorded / markdown-only.

Reference:

```text
E:\Hermes-Hub\docs\SERVER_RUNTIME_STARTUP_READONLY_RECONCILIATION.md
```

Current factual runtime state:

```text
malyarka-telegram-bot.service exists
ActiveState=inactive
SubState=dead
is-enabled=disabled
```

Known entrypoint:

```text
/opt/malyarka-telegram-bot/.venv/bin/python -m malyarka_telegram.app --run-polling
```

Adapter state:

```text
Hermes adapter installed.
Production enable not performed.
Live dry-run currently not confirmed.
Gate 9 must not be treated as complete without separate user decision.
```

No start/restart/enable is allowed without separate explicit approval.

## Server Bot Startup Gated Plan

Date: 2026-06-20

Created markdown-only plan:

```text
E:\Hermes-Hub\docs\SERVER_BOT_STARTUP_GATED_PLAN_ONLY.md
```

Purpose:

```text
Plan a future controlled startup of malyarka-telegram-bot.service without running it now.
```

Plan records:

- service exists but is currently inactive/dead and disabled;
- entrypoint is known;
- adapter is installed;
- feature flag must remain OFF;
- live dry-run is not currently confirmed;
- production enable has not been performed;
- Gate 9 must not be accepted as complete without separate user decision;
- real start requires separate explicit approval.

No server touch, no service start/restart/enable, no secrets, no DB/logs/orders, no code changes.

## Server Bot Controlled Startup Batch Packet

Date: 2026-06-20

Technical name:

```text
SERVER_BOT_CONTROLLED_STARTUP_BATCH_PLAN
```

Status:

```text
SERVER_BOT_CONTROLLED_STARTUP_BATCH_PLAN_READY
```

Created markdown-only batch packet:

```text
E:\Hermes-Hub\docs\SERVER_BOT_CONTROLLED_STARTUP_BATCH_PLAN.md
E:\Hermes-Hub\docs\SERVER_BOT_CONTROLLED_START_PRECHECK_CHECKLIST.md
E:\Hermes-Hub\docs\SERVER_BOT_CONTROLLED_START_COMMAND_PLAN.md
E:\Hermes-Hub\docs\SERVER_BOT_CONTROLLED_START_TELEGRAM_TEST_PLAN.md
E:\Hermes-Hub\docs\SERVER_BOT_CONTROLLED_START_ROLLBACK_PLAN.md
E:\Hermes-Hub\docs\SERVER_BOT_CONTROLLED_START_APPROVAL_GATE.md
E:\Hermes-Hub\docs\SERVER_BOT_CONTROLLED_START_REPORT_TEMPLATE.md
E:\Hermes-Hub\docs\SERVER_BOT_CONTROLLED_START_DECISION_MAP.md
```

Required approval phrase for any future real start:

```text
APPROVE_SERVER_BOT_CONTROLLED_START_ONCE
```

This packet does not start the bot and does not continue Phase 2.

No-touch: server, SSH, service start/restart/enable, bot, secrets, DB/logs/orders, `.py` code, git and production were not touched.

## Server Bot Controlled Start Result

Date: 2026-06-20

Status:

```text
CONTROLLED_START_AND_TELEGRAM_TEST_PASSED
```

Report:

```text
E:\Hermes-Hub\docs\SERVER_BOT_CONTROLLED_START_REPORT_2026_06_20.md
```

Result:

- service started once with approval phrase;
- post-start state: `active/running`;
- MainPID: `28149`;
- autostart remains `disabled`;
- feature flag remains OFF;
- Telegram phone test passed;
- production enable not performed;
- Phase 2 not continued.

Next required user decision:

```text
leave service running
```

or:

```text
perform controlled stop
```

## Server Bot Post-Start Stabilization

Date: 2026-06-20

Status:

```text
SERVER_BOT_POST_START_STABILIZATION_DOCUMENTED
```

Created:

```text
E:\Hermes-Hub\docs\SERVER_BOT_POST_START_STABILIZATION_REPORT.md
E:\Hermes-Hub\docs\SERVER_BOT_RUNNING_STATE_DECISION_REQUIRED.md
E:\Hermes-Hub\docs\SERVER_BOT_LEAVE_RUNNING_MONITORING_PLAN.md
E:\Hermes-Hub\docs\SERVER_BOT_CONTROLLED_STOP_PLAN_ONLY.md
E:\Hermes-Hub\docs\SERVER_HERMES_ADAPTER_PHASE2_DRY_RUN_NEXT_PLAN_ONLY.md
```

Read-only server confirmation:

```text
ActiveState=active
SubState=running
MainPID=28149
is-enabled=disabled
_HERMES_ADAPTER_ENABLED = False
```

Next decision required:

```text
leave running
controlled stop
Phase 2 dry-run plan only
```

No restart, stop, enable, production, Phase 2, secrets, DB/logs/orders, `.py` changes or git actions were performed.

```text
text order -> parse sizes -> disputed rows -> area -> Corel export -> tests
```

Detailed architecture packet:

```text
E:\Hermes-Hub\handoff\BATCH_002_MALYARKA_CLEAN_ARCHITECTURE.md
```

Future logical modules:

```text
order_input
size_parser
dispute_detector
area_calculator
corel_export_model
order_result
tests
```

Order statuses:

```text
clean
has_disputes
empty_or_invalid
```

Technical scaffold transition executed:

```text
E:\Hermes-Hub\handoff\BATCH_003_MALYARKA_CLEAN_CORE_SCAFFOLD.md
```

Created empty scaffold:

```text
E:\Hermes-Hub\projects\malyarka-clean\src\malyarka_clean_core
```

Scaffold modules created with docstrings only:

```text
order_input.py
size_parser.py
dispute_detector.py
area_calculator.py
corel_export_model.py
order_result.py
```

No working parser, area calculation, Corel export or test logic has been implemented.

Core contract planning executed:

```text
BATCH_007_CORE_CONTRACTS_PLANNING
```

Minimal data contracts are documented here:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_CORE_CONTRACTS.md
```

Contracts describe:

```text
order_input
size_parser
dispute_detector
area_calculator
corel_export_model
order_result
```

They also define:

```text
clean
has_disputes
empty_or_invalid
confirmed row fields
disputed row fields
final order result fields
```

First local parser rule planning executed:

```text
BATCH_008_FIRST_LOCAL_PARSER_RULES_PLANNING
```

Parser rules are documented here:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_PARSER_RULES.md
```

The first parser planning accepts these clear formats:

```text
1000 400
1000 400 2
1000x400
1000 x 400
1000*400
1000×400
```

Base parser rule:

```text
first number = height
second number = width
third number = quantity
missing quantity = 1
disputed data is not guessed
```

First local parser implementation executed:

```text
BATCH_009_FIRST_LOCAL_PARSER_IMPLEMENTATION
```

Implemented only inside:

```text
E:\Hermes-Hub\projects\malyarka-clean
```

Touched parser modules:

```text
src\malyarka_clean_core\order_input.py
src\malyarka_clean_core\size_parser.py
src\malyarka_clean_core\dispute_detector.py
src\malyarka_clean_core\__init__.py
tests\test_first_local_parser.py
```

Focused test result:

```text
7 passed
```

Area calculation planning executed:

```text
BATCH_010_AREA_CALCULATION_PLANNING
```

Area rules are documented here:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_AREA_RULES.md
```

Formula:

```text
area_m2 = height_mm * width_mm * quantity / 1_000_000
```

Area planning rules:

```text
calculate only confirmed rows
exclude disputed rows
show confirmed area even when disputes exist
block final export while disputes exist
do not calculate cost, prices, LKM or materials
```

Area calculation implementation executed:

```text
BATCH_011_AREA_CALCULATION_IMPLEMENTATION
```

Implemented only inside:

```text
E:\Hermes-Hub\projects\malyarka-clean
```

Touched area files:

```text
src\malyarka_clean_core\area_calculator.py
src\malyarka_clean_core\__init__.py
tests\test_area_calculator.py
```

Focused area test result:

```text
5 passed
```

Order result integration planning executed:

```text
BATCH_012_ORDER_RESULT_INTEGRATION_PLANNING
```

Order result rules are documented here:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_ORDER_RESULT_RULES.md
```

Future final result fields:

```text
status
confirmed_rows
disputed_rows
total_area_m2
export_blocked
short_summary
dispute_reasons
```

Status rules:

```text
no confirmed and no disputed rows -> empty_or_invalid
any disputed rows -> has_disputes and export_blocked = true
confirmed rows without disputes -> clean
area uses confirmed rows only
final export blocked when disputes exist
```

Still not implemented:

```text
area calculation
Corel export
Excel export
prices
LKM
Telegram
Vision
API
database
Docker
old Malyarka as active system
old bot.py
```

## BATCH_014 Russian Navigation Layer

Status:

```text
executed
```

Purpose:

```text
Add Russian navigation files so the user understands where to go, what folders mean and what package numbers mean.
```

Created:

```text
E:\Hermes-Hub\КАРТА_ПАПОК.md
E:\Hermes-Hub\КУДА_НАЖИМАТЬ.md
E:\Hermes-Hub\ЕЖЕДНЕВНИК.md
E:\Hermes-Hub\СПИСОК_ПАКЕТОВ_ПО_РУССКИ.md
```

No folders were renamed.
No code paths were changed.
No working logic, functions, classes or tests were created.

Package order updated:

```text
Пакет 014 — Русская навигация по проекту
BATCH_014_RUSSIAN_NAVIGATION_LAYER

Пакет 015 — Модель данных для Corel
BATCH_015_COREL_EXPORT_MODEL_PLANNING
```

## BATCH_015 Corel Export Model Planning

Status:

```text
executed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_COREL_MODEL_RULES.md
```

Decision:

```text
Future Corel export may use only confirmed rows from order_result.
Disputed rows are never included.
If export_blocked = true, Corel rows are not prepared.
If status = clean, Corel rows may be prepared.
```

Future Corel row fields:

```text
height_mm
width_mm
quantity
```

No export code, functions, classes, tests, Excel/Corel files or app launch were created.

## BATCH_016 Project Protection Layer

Status:

```text
executed / organizational only
```

Created:

```text
E:\Hermes-Hub\ЗАЩИТА_ПРОЕКТА.md
```

Purpose:

```text
Explain in Russian what must not be touched without separate permission, where the risks are, and how to continue safely.
```

Protected zones:

```text
.env
orders.db
.git
tokens
keys
Telegram
Vision
API
Docker
old Malyarka as active system
bot.py
commits/push
```

No working logic, functions, classes, tests, app launch, Corel/Excel export or folder renaming were done.

## BATCH_017 Corel Model Implementation Planning

Status:

```text
executed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_COREL_IMPLEMENTATION_PLAN.md
```

Purpose:

```text
Plan safe future implementation of a neutral Corel model before writing code.
```

Future allowed conditions:

```text
status = clean
disputed_rows is empty
export_blocked = false
```

Future blocking conditions:

```text
disputed_rows exists
export_blocked = true
status = has_disputes
status = empty_or_invalid
```

Future result fields:

```text
corel_rows
export_blocked
reason
source_status
```

No working logic, functions, classes, tests, Excel/Corel export or app launch were created.

## BATCH_018 Corel Model Implementation

Status:

```text
executed / neutral internal model only
```

Implemented only inside:

```text
E:\Hermes-Hub\projects\malyarka-clean
```

Changed:

```text
E:\Hermes-Hub\projects\malyarka-clean\src\malyarka_clean_core\corel_export_model.py
E:\Hermes-Hub\projects\malyarka-clean\src\malyarka_clean_core\__init__.py
E:\Hermes-Hub\projects\malyarka-clean\tests\test_corel_export_model.py
```

Implemented:

```text
build_corel_export_model
corel_rows
export_blocked
reason
source_status
```

Focused test result:

```text
5 passed
```

No Excel file, Corel file, export to disk, app launch, Telegram, Vision, API, database, prices, cost, LKM, materials, Docker, old Malyarka, old bot.py, commits or push.

## BATCH_019 Order Pipeline Smoke Test Planning

Status:

```text
executed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_PIPELINE_SMOKE_TEST_PLAN.md
```

Purpose:

```text
Plan future smoke checks for the full minimal chain from raw text order to neutral Corel model.
```

Future chain:

```text
raw order text
-> line parsing
-> confirmed rows
-> disputed rows
-> final order result
-> area calculation
-> Corel model
```

Planned scenarios:

```text
clean order
order with disputed row
empty or garbage order
```

No code, tests, Excel/Corel export, export files or app launch were created.

## BATCH_023 Manual Core Check Planning

Status:

```text
executed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_MANUAL_CORE_CHECK_PLAN.md
```

Purpose:

```text
Plan simple manual checks for the minimal Malyarka Clean core on understandable order examples.
```

Planned manual examples:

```text
clean order
order with disputed row
empty or garbage order
```

Next planned package:

```text
BATCH_024_MANUAL_CORE_CHECK_IMPLEMENTATION
```

No code, tests, Excel/Corel export, export files or app launch were created.

## BATCH_022 README Usage Guide Implementation

Status:

```text
executed / documentation only
```

Created:

```text
E:\Hermes-Hub\README_КАК_ПОЛЬЗОВАТЬСЯ.md
```

Purpose:

```text
Provide a simple Russian user guide for the current minimal Malyarka Clean core.
```

The guide explains:

- Hermes Hub and Malyarka Clean;
- what already works;
- supported size formats;
- statuses;
- disputed rows;
- area formula;
- Corel model readiness and blocking;
- what is not ready yet;
- where the user should look;
- what comes next.

No code, tests, Excel/Corel export, export files or app launch were created.

## BATCH_020 Order Pipeline Smoke Test Implementation

Status:

```text
executed / focused smoke-tests only
```

Created:

```text
E:\Hermes-Hub\projects\malyarka-clean\tests\test_order_pipeline_smoke.py
```

Smoke chain checked:

```text
raw order text
-> final order result
-> area calculation
-> neutral Corel model
```

Scenarios checked:

```text
clean order
order with disputed row
empty order
```

Focused smoke-test result:

```text
3 passed
```

No Excel file, Corel file, export to disk, export files, app launch, Telegram, Vision, API, database, prices, cost, LKM, materials, Docker, old Malyarka, old bot.py, commits or push.

## BATCH_021 Usage Guide Planning

Status:

```text
executed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_USAGE_GUIDE_PLAN.md
```

Future user guide:

```text
E:\Hermes-Hub\README_КАК_ПОЛЬЗОВАТЬСЯ.md
```

The plan documents:

- what the minimal core already does;
- supported size formats;
- statuses;
- disputed rows;
- area formula;
- when Corel rows are ready or blocked;
- what is still not implemented;
- future README sections.

No code, tests, Excel/Corel export, export files or app launch were created.

Meaning:

1. The user gives order text.
2. The system extracts sizes and rows.
3. The system marks unclear or disputed rows instead of guessing silently.
4. The system calculates area.
5. The system prepares data for future Corel export.
6. Tests protect the parsing and calculation rules.

Not included in the first core:

```text
Telegram
Vision
external APIs
database
old bot.py
production launch
```

## Current Decision

Start fresh in:

```text
E:\Hermes-Hub
```

Do not build inside old Malyarka.

## Frozen / Do Not Touch

Do not touch without separate explicit permission:

```text
C:\Users\user\Desktop\malyarka_codex_work
C:\Users\user\Desktop\malyarka_memory_cleanup
```

Do not read or modify:

```text
.env
orders.db
.git
tokens
keys
passwords
Telegram launch
Vision
external APIs
old bot.py
```

## Next Step

Continue the startup package:

1. Confirm final project name.
2. Decide Nous Portal free first or $20 subscription.
3. Prepare the first real Codex batch for `projects\malyarka-clean`.
4. Only then start building the minimal clean core.

Ready-to-paste prompts:

```text
E:\Hermes-Hub\handoff\CHATGPT_CONTEXT_BUNDLE.md
E:\Hermes-Hub\handoff\PROMPT_TO_PASTE_IN_CHATGPT.md
E:\Hermes-Hub\handoff\PROMPT_FOR_MAIN_CHAT_NOW.md
E:\Hermes-Hub\handoff\PROMPT_TO_ENABLE_BATCH_MODE_IN_CHATGPT.md
E:\Hermes-Hub\handoff\PROMPT_TO_PASTE_IN_HERMES.md
E:\Hermes-Hub\handoff\PROMPT_TO_PASTE_IN_CODEX.md
```
## BATCH_013 Order Result Implementation

Status:

```text
executed
```

Implemented only inside:

```text
E:\Hermes-Hub\projects\malyarka-clean
```

Changed:

```text
E:\Hermes-Hub\projects\malyarka-clean\src\malyarka_clean_core\order_result.py
E:\Hermes-Hub\projects\malyarka-clean\src\malyarka_clean_core\__init__.py
E:\Hermes-Hub\projects\malyarka-clean\tests\test_order_result.py
```

Implemented:

```text
build_order_result
combine_order_result
status
confirmed_rows
disputed_rows
total_area_m2
export_blocked
short_summary
dispute_reasons
warnings
next_action
```

Focused test result:

```text
3 passed
```

Still not implemented:

```text
Corel export
Excel export
prices
LKM
Telegram
Vision
API
database
Docker
old Malyarka as active system
old bot.py
```
## BATCH_024 Manual Core Check Implementation

Status:

```text
executed / local manual check only
```

Created:

```text
E:\Hermes-Hub\projects\malyarka-clean\tools\manual_core_check.py
E:\Hermes-Hub\РУЧНАЯ_ПРОВЕРКА_ЯДРА.md
```

Purpose:

```text
Give the user a simple local way to manually check the minimal Malyarka Clean core on three examples.
```

What the script checks:

```text
clean order
order with disputed row
empty or garbage order
```

The script uses the existing core only:

```text
build_order_result
build_corel_export_model
area calculation through the order result chain
```

No Excel/Corel export was created. No Telegram, Vision, API, database, Docker, old Malyarka or bot.py was touched.

Verification result:

```text
manual_core_check.py ran successfully.
clean order: clean
disputed order: has_disputes
empty/garbage order: has_disputes
```

Known mismatch found:

```text
For empty/garbage order the plan expected empty_or_invalid, but the current core returns has_disputes.
```

Next package:

```text
BATCH_025_EMPTY_INVALID_STATUS_FIX_PLANNING
```
## BATCH_025 Empty Invalid Status Fix Planning

Status:

```text
executed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_EMPTY_INVALID_STATUS_FIX_PLAN.md
```

Problem:

```text
Manual check found that fully garbage input currently returns has_disputes.
Expected status: empty_or_invalid.
```

Planned rule:

```text
empty input -> empty_or_invalid
fully garbage input without confirmed rows -> empty_or_invalid
confirmed rows + garbage/disputed rows -> has_disputes
clean confirmed rows only -> clean
```

Likely implementation touch points for the next technical package:

```text
order_result
dispute_detector
focused tests
manual_core_check
```

No code, functions, classes, tests, app launch, Telegram, Vision, API, database, Excel/Corel export or old Malyarka work was done in this package.

Next package:

```text
BATCH_026_EMPTY_INVALID_STATUS_FIX_IMPLEMENTATION
```
## BATCH_026 Empty Invalid Status Fix Implementation

Status:

```text
executed / focused implementation
```

Changed:

```text
E:\Hermes-Hub\projects\malyarka-clean\src\malyarka_clean_core\order_result.py
E:\Hermes-Hub\projects\malyarka-clean\tests\test_order_result.py
E:\Hermes-Hub\projects\malyarka-clean\tests\test_order_pipeline_smoke.py
E:\Hermes-Hub\projects\malyarka-clean\tests\test_corel_export_model.py
```

Implemented rule:

```text
empty input -> empty_or_invalid
fully garbage input without confirmed rows -> empty_or_invalid
confirmed rows + garbage/disputed rows -> has_disputes
clean confirmed rows only -> clean
```

Checks:

```text
PYTHONPATH=E:\Hermes-Hub\projects\malyarka-clean\src
python -m pytest tests\test_order_result.py tests\test_order_pipeline_smoke.py tests\test_corel_export_model.py -q
15 passed

python tools\manual_core_check.py
clean order -> clean
order with disputed row -> has_disputes
empty/garbage order -> empty_or_invalid
```

No Excel/Corel export was created. No Telegram, Vision, API, database, Docker, old Malyarka or bot.py was touched.

Next package:

```text
BATCH_027_MANUAL_CHECK_ACCEPTANCE_OR_USER_ENTRY_PLANNING
```
## BATCH_027 Manual Check Acceptance Or User Entry Planning

Status:

```text
executed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_USER_ENTRY_PLAN.md
```

Accepted:

```text
minimal chain works
clean order -> clean
order with disputed row -> has_disputes
empty/garbage order -> empty_or_invalid
```

Current inconvenience:

```text
manual check uses a technical Python script
pytest needs PYTHONPATH
user should not manually deal with Python commands
```

Next direction:

```text
simple local user entry for text orders
no Telegram, Vision, API, database, Excel/Corel export
```

No code, functions, classes, tests, app launch, Telegram, Vision, API, database, Excel/Corel export or old Malyarka work was done in this package.

Next package:

```text
BATCH_028_SIMPLE_RUN_COMMAND_PLANNING
```
## BATCH_028 Simple Run Command Planning

Status:

```text
executed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_SIMPLE_RUN_PLAN.md
```

Problem:

```text
pytest without PYTHONPATH cannot find malyarka_clean_core.
The user should not manually remember PYTHONPATH commands.
```

Planned direction:

```text
simple .cmd for focused tests
simple .cmd for manual core check
short Russian launch instruction
```

No code, `.cmd` files, functions, classes, tests, app launch, Telegram, Vision, API, database, Excel/Corel export or old Malyarka work was done in this package.

Next package:

```text
BATCH_029_SIMPLE_RUN_COMMAND_IMPLEMENTATION
```
## BATCH_029 Simple Run Command Implementation

Status:

```text
executed / local launch commands only
```

Created:

```text
E:\Hermes-Hub\ЗАПУСТИТЬ_РУЧНУЮ_ПРОВЕРКУ_ЯДРА.cmd
E:\Hermes-Hub\ЗАПУСТИТЬ_ТЕСТЫ_ЯДРА.cmd
```

Changed:

```text
E:\Hermes-Hub\РУЧНАЯ_ПРОВЕРКА_ЯДРА.md
```

Result:

```text
Both .cmd files set PYTHONPATH automatically.
Manual check can be run without writing PYTHONPATH.
Focused tests can be run without writing PYTHONPATH.
```

Checks:

```text
First .cmd attempt exposed a Windows command-file encoding issue with Cyrillic text inside .cmd.
The .cmd contents were changed to ASCII for stable Windows execution.

ЗАПУСТИТЬ_РУЧНУЮ_ПРОВЕРКУ_ЯДРА.cmd --no-pause -> success
ЗАПУСТИТЬ_ТЕСТЫ_ЯДРА.cmd --no-pause -> 27 passed
```

No Excel/Corel export was created. No Telegram, Vision, API, database, Docker, old Malyarka or bot.py was touched.

Next package:

```text
BATCH_030_SIMPLE_USER_ORDER_INPUT_PLANNING
```
## BATCH_030 Simple User Order Input Planning

Status:

```text
executed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_SIMPLE_USER_ORDER_INPUT_PLAN.md
```

Purpose:

```text
Plan a simple local way for the user to enter real order text into the minimal Malyarka Clean core.
```

Planned output:

```text
source text
status
confirmed_rows
disputed_rows
total_area_m2
export_blocked
corel_rows
blocking reason
```

No code, `.cmd` files, functions, classes, tests, app launch, Telegram, Vision, API, database, Excel/Corel export or old Malyarka work was done in this package.

Next package:

```text
BATCH_031_SIMPLE_USER_ORDER_INPUT_IMPLEMENTATION
```
## BATCH_031 Simple User Order Input Implementation

Status:

```text
executed / local user input only
```

Created:

```text
E:\Hermes-Hub\projects\malyarka-clean\tools\user_order_input.py
E:\Hermes-Hub\ВВЕСТИ_ЗАКАЗ_ВРУЧНУЮ.cmd
```

Changed:

```text
E:\Hermes-Hub\README_КАК_ПОЛЬЗОВАТЬСЯ.md
```

Result:

```text
User can paste order text locally, type ГОТОВО, and see status, rows, area, export_blocked, corel_rows and blocking reason.
```

Checks:

```text
First .cmd sample attempt passed --no-pause into Python and failed with argparse error.
The .cmd was fixed to filter --no-pause before calling user_order_input.py.
ВВЕСТИ_ЗАКАЗ_ВРУЧНУЮ.cmd --sample clean --no-pause -> clean
ВВЕСТИ_ЗАКАЗ_ВРУЧНУЮ.cmd --sample dispute --no-pause -> has_disputes
ВВЕСТИ_ЗАКАЗ_ВРУЧНУЮ.cmd --sample garbage --no-pause -> empty_or_invalid
```

No Excel/Corel export was created. No Telegram, Vision, API, database, Docker, old Malyarka or bot.py was touched.

Next package:

```text
BATCH_032_USER_INPUT_ACCEPTANCE_AND_NEXT_UI_PLANNING
```
## BATCH_032 User Input Acceptance And Next UI Planning

Status:

```text
executed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_USER_INPUT_ACCEPTANCE_AND_NEXT_UI_PLAN.md
```

Accepted:

```text
Simple user order input is accepted.
The user can run E:\Hermes-Hub\ВВЕСТИ_ЗАКАЗ_ВРУЧНУЮ.cmd, paste order text, type ГОТОВО, and read a Russian result.
```

Known limits:

```text
The current input is still a console window.
The result is not saved as a separate order file yet.
There is no visual UI, buttons or order history yet.
```

Next package:

```text
BATCH_033_SAVE_ORDER_RESULT_TEXT_PLANNING
```
## BATCH_033 Save Order Result Text Planning

Status:

```text
executed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_SAVE_ORDER_RESULT_TEXT_PLAN.md
```

Planned:

```text
Save the latest user order result into a plain text file:
E:\Hermes-Hub\outputs\LAST_ORDER_RESULT.txt
```

Rules:

```text
Plain .txt only.
Do not create Excel/Corel files.
Do not create outputs in this planning package.
Do not touch database, Telegram, Vision, API or old Malyarka.
The latest result may be overwritten to avoid clutter.
```

Next package:

```text
BATCH_034_SAVE_ORDER_RESULT_TEXT_IMPLEMENTATION
```
## BATCH_034 Save Order Result Text Implementation

Status:

```text
executed / local text result only
```

Created:

```text
E:\Hermes-Hub\outputs
E:\Hermes-Hub\outputs\LAST_ORDER_RESULT.txt
```

Changed:

```text
E:\Hermes-Hub\projects\malyarka-clean\tools\user_order_input.py
E:\Hermes-Hub\README_КАК_ПОЛЬЗОВАТЬСЯ.md
```

Result:

```text
User order input now prints the result on screen and saves the same result to LAST_ORDER_RESULT.txt.
The file is plain .txt and is overwritten on each run.
```

Checks:

```text
ВВЕСТИ_ЗАКАЗ_ВРУЧНУЮ.cmd --sample clean --no-pause -> clean, result saved
ВВЕСТИ_ЗАКАЗ_ВРУЧНУЮ.cmd --sample dispute --no-pause -> has_disputes, result saved
ВВЕСТИ_ЗАКАЗ_ВРУЧНУЮ.cmd --sample garbage --no-pause -> empty_or_invalid, result saved
```

No Excel/Corel export was created. No Telegram, Vision, API, database, Docker, old Malyarka or bot.py was touched.

Next package:

```text
BATCH_035_SAVE_RESULT_ACCEPTANCE_AND_INPUT_FILE_PLANNING
```
## BATCH_035 Save Result Acceptance And Input File Planning

Status:

```text
executed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_INPUT_FILE_PLAN.md
```

Accepted:

```text
Saving the latest result to E:\Hermes-Hub\outputs\LAST_ORDER_RESULT.txt is accepted.
```

Planned:

```text
Future input file:
E:\Hermes-Hub\inputs\ORDER_INPUT.txt
```

Rules:

```text
Plain .txt only.
Do not create inputs or ORDER_INPUT.txt in this planning package.
Do not create Excel/Corel files.
Do not touch database, Telegram, Vision, API or old Malyarka.
```

Next package:

```text
BATCH_036_INPUT_FILE_IMPLEMENTATION
```
## BATCH_036 Input File Implementation

Status:

```text
executed / local txt input only
```

Created:

```text
E:\Hermes-Hub\inputs
E:\Hermes-Hub\inputs\ORDER_INPUT.txt
E:\Hermes-Hub\ПРОВЕРИТЬ_ЗАКАЗ_ИЗ_ФАЙЛА.cmd
```

Changed:

```text
E:\Hermes-Hub\projects\malyarka-clean\tools\user_order_input.py
E:\Hermes-Hub\README_КАК_ПОЛЬЗОВАТЬСЯ.md
```

Result:

```text
User can edit ORDER_INPUT.txt, run ПРОВЕРИТЬ_ЗАКАЗ_ИЗ_ФАЙЛА.cmd, see the result on screen, and get LAST_ORDER_RESULT.txt updated.
```

Check:

```text
ПРОВЕРИТЬ_ЗАКАЗ_ИЗ_ФАЙЛА.cmd --no-pause -> clean, result saved
```

No Excel/Corel export was created. No Telegram, Vision, API, database, Docker, old Malyarka or bot.py was touched.

Next package:

```text
BATCH_037_INPUT_FILE_ACCEPTANCE_AND_USER_SHORTCUTS_PLANNING
```
## BATCH_SERIES_037_040 Local v0.1 And Shortcuts

Status:

```text
executed / documentation and user shortcuts
```

Created:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_INPUT_FILE_ACCEPTANCE.md
E:\Hermes-Hub\docs\MALYARKA_CLEAN_LOCAL_V0_1_ACCEPTANCE.md
E:\Hermes-Hub\docs\MALYARKA_CLEAN_RESULT_READABILITY_PLAN.md
E:\Hermes-Hub\ОТКРЫТЬ_ФАЙЛ_ЗАКАЗА.cmd
E:\Hermes-Hub\ОТКРЫТЬ_ПОСЛЕДНИЙ_РЕЗУЛЬТАТ.cmd
E:\Hermes-Hub\ОТКРЫТЬ_ИНСТРУКЦИЮ.cmd
```

Accepted:

```text
Input-file mode is accepted.
Local Malyarka Clean v0.1 is accepted as a safe local version.
```

Planned:

```text
Improve LAST_ORDER_RESULT.txt readability in the next technical package.
```

Checks:

```text
Shortcut .cmd contents checked without opening Notepad windows.
README launcher path encoding was fixed by using README_*.md pattern.
```

No parser, area calculation, dispute rules, Excel/Corel export, Telegram, Vision, API, database, Docker, old Malyarka or bot.py was touched.

Next package:

```text
BATCH_041_RESULT_READABILITY_IMPLEMENTATION
```
## BATCH_SERIES_041_044 Readable Result And Examples

Status:

```text
executed / readable local result and examples
```

Created:

```text
E:\Hermes-Hub\examples
E:\Hermes-Hub\examples\CLEAN_ORDER.txt
E:\Hermes-Hub\examples\DISPUTED_ORDER.txt
E:\Hermes-Hub\examples\EMPTY_OR_INVALID_ORDER.txt
E:\Hermes-Hub\examples\MIXED_SEPARATORS_ORDER.txt
E:\Hermes-Hub\ПРОВЕРИТЬ_ПРИМЕР_ЧИСТЫЙ.cmd
E:\Hermes-Hub\ПРОВЕРИТЬ_ПРИМЕР_СПОРНЫЙ.cmd
E:\Hermes-Hub\ПРОВЕРИТЬ_ПРИМЕР_МУСОРНЫЙ.cmd
E:\Hermes-Hub\ПРОВЕРИТЬ_ПРИМЕР_РАЗНЫЕ_РАЗДЕЛИТЕЛИ.cmd
E:\Hermes-Hub\docs\MALYARKA_CLEAN_READABLE_RESULT_AND_EXAMPLES_ACCEPTANCE.md
```

Changed:

```text
E:\Hermes-Hub\projects\malyarka-clean\tools\user_order_input.py
E:\Hermes-Hub\README_КАК_ПОЛЬЗОВАТЬСЯ.md
```

Checks:

```text
ПРОВЕРИТЬ_ПРИМЕР_ЧИСТЫЙ.cmd --no-pause -> clean
ПРОВЕРИТЬ_ПРИМЕР_СПОРНЫЙ.cmd --no-pause -> has_disputes
ПРОВЕРИТЬ_ПРИМЕР_МУСОРНЫЙ.cmd --no-pause -> empty_or_invalid
ПРОВЕРИТЬ_ПРИМЕР_РАЗНЫЕ_РАЗДЕЛИТЕЛИ.cmd --no-pause -> clean
```

Notes:

```text
Only result formatting was changed.
Parser, area calculation and dispute rules were not changed.
The Windows console did not support some symbols, so result display uses m2 and x instead of m² and ×.
```

Next package:

```text
BATCH_045_LOCAL_V01_ACCEPTANCE_AND_NEXT_ROADMAP_PLANNING
```
## BATCH_SERIES_045_047 Local v0.1 Acceptance And Roadmap

Status:

```text
executed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_LOCAL_V0_1_FINAL_ACCEPTANCE.md
E:\Hermes-Hub\docs\MALYARKA_CLEAN_NEXT_ROADMAP_OPTIONS.md
E:\Hermes-Hub\docs\MALYARKA_CLEAN_RECOMMENDED_NEXT_STAGE.md
```

Accepted:

```text
Malyarka Clean v0.1 is accepted as a local working point.
```

Roadmap options:

```text
Excel/Corel export
local interface improvement
Telegram
Vision
order database
prices and calculations
LKM and materials
```

Recommended next stage:

```text
Plan safe Excel/Corel export.
No export implementation was done in this series.
```

Next series:

```text
BATCH_SERIES_048_050_SAFE_EXCEL_COREL_EXPORT_PLANNING
```
## BATCH_SERIES_048_050 Safe Excel/Corel Export Planning

Status:

```text
executed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_SAFE_EXCEL_COREL_EXPORT_RULES.md
E:\Hermes-Hub\docs\MALYARKA_CLEAN_EXCEL_COREL_FILE_STRUCTURE.md
E:\Hermes-Hub\docs\MALYARKA_CLEAN_EXCEL_COREL_IMPLEMENTATION_PLAN.md
```

Planned:

```text
Safe transition from local v0.1 to future Excel/Corel export.
```

Rules:

```text
Excel/Corel export is allowed only for clean orders.
has_disputes and empty_or_invalid block export.
Disputed rows are never included in future Excel.
Export must use existing internal corel_rows.
Export must not change parser, area calculation or dispute rules.
Future Excel is only a technical file for Corel, not a production cost calculation.
```

Future file structure:

```text
.xlsx
3 columns: height, width, quantity
no headers
first row empty
only confirmed rows
same row order as source order
numbers only
```

Recommended next series:

```text
BATCH_SERIES_051_053_SAFE_EXCEL_COREL_EXPORT_IMPLEMENTATION
```

No code, .cmd files, tests, Excel/Corel files, export, Telegram, Vision, API, database, old Malyarka or bot.py were touched.
## BATCH_SERIES_051_053 Safe Excel/Corel Export Implementation

Status:

```text
executed / safe local .xlsx export
```

Created:

```text
E:\Hermes-Hub\projects\malyarka-clean\src\malyarka_clean_core\excel_corel_export.py
E:\Hermes-Hub\projects\malyarka-clean\tests\test_excel_corel_export.py
E:\Hermes-Hub\projects\malyarka-clean\tools\create_corel_excel.py
E:\Hermes-Hub\СОЗДАТЬ_EXCEL_ДЛЯ_COREL.cmd
E:\Hermes-Hub\outputs\COREL_EXPORT.xlsx
```

Changed:

```text
E:\Hermes-Hub\projects\malyarka-clean\src\malyarka_clean_core\__init__.py
E:\Hermes-Hub\projects\malyarka-clean\src\malyarka_clean_core\corel_export_model.py
E:\Hermes-Hub\projects\malyarka-clean\tools\user_order_input.py
E:\Hermes-Hub\README_КАК_ПОЛЬЗОВАТЬСЯ.md
```

Implemented:

```text
Safe .xlsx export for clean orders only.
Output file: E:\Hermes-Hub\outputs\COREL_EXPORT.xlsx
Blocked for has_disputes and empty_or_invalid.
Uses existing corel_rows.
Does not change parser, area calculation or dispute rules.
```

Checks:

```text
Focused pytest -> 33 passed.
Clean launcher check -> COREL_EXPORT.xlsx created.
Disputed launcher check -> export blocked, no new Excel created.
Empty/garbage launcher check -> export blocked with empty_or_invalid.
Workbook structure check -> row 1 empty, no headers, rows contain height/width/quantity only.
```

No Telegram, Vision, API, database, prices, cost, LKM, materials, .env, orders.db, .git, tokens, keys, old Malyarka, bot.py, Docker, commits/push or Corel file were touched.
## BATCH_SERIES_054_056 Excel/Corel Export Acceptance And Next Layer

Status:

```text
executed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_EXCEL_COREL_EXPORT_ACCEPTANCE.md
E:\Hermes-Hub\docs\MALYARKA_CLEAN_CURRENT_USER_WORKFLOW.md
E:\Hermes-Hub\docs\MALYARKA_CLEAN_NEXT_LAYER_OPTIONS_AFTER_EXCEL.md
```

Accepted:

```text
Safe Excel/Corel export accepted as a local working layer.
COREL_EXPORT.xlsx is created only for clean orders.
has_disputes and empty_or_invalid block export.
Disputed rows are not included in Excel.
Parser, area calculation and dispute rules were not changed.
```

Current user workflow:

```text
Open ORDER_INPUT.txt -> paste order -> save -> run file check -> read LAST_ORDER_RESULT.txt -> if clean run СОЗДАТЬ_EXCEL_ДЛЯ_COREL.cmd -> take COREL_EXPORT.xlsx. If disputed, fix ORDER_INPUT.txt and repeat.
```

Recommended next series:

```text
BATCH_SERIES_057_060_SINGLE_LOCAL_ORDER_RUNNER
```

No code, .cmd files, tests, Excel/Corel files, Telegram, Vision, API, database, prices, cost, LKM, materials, parser, area calculation or dispute rules were touched.
## BATCH_SERIES_057_060 Single Local Order Runner

Status:

```text
executed / single local runner
```

Created:

```text
E:\Hermes-Hub\projects\malyarka-clean\tools\run_local_order.py
E:\Hermes-Hub\projects\malyarka-clean\tests\test_single_local_runner.py
E:\Hermes-Hub\ЗАПУСТИТЬ_ЗАКАЗ.cmd
E:\Hermes-Hub\docs\MALYARKA_CLEAN_SINGLE_LOCAL_RUNNER_ACCEPTANCE.md
```

Changed:

```text
E:\Hermes-Hub\README_КАК_ПОЛЬЗОВАТЬСЯ.md
```

Implemented:

```text
Single local order runner reads ORDER_INPUT.txt, saves LAST_ORDER_RESULT.txt, creates COREL_EXPORT.xlsx only for clean orders, and blocks Excel for has_disputes or empty_or_invalid.
```

Checks:

```text
Focused pytest -> 37 passed.
ЗАПУСТИТЬ_ЗАКАЗ.cmd clean -> exit 0, Excel created.
ЗАПУСТИТЬ_ЗАКАЗ.cmd has_disputes -> exit 2, Excel not updated.
ЗАПУСТИТЬ_ЗАКАЗ.cmd empty_or_invalid -> exit 2, Excel not updated.
```

Recommended next series:

```text
BATCH_SERIES_061_063_USER_GUIDE_AND_LOCAL_RELEASE_CHECK
```

No parser, area calculation, dispute rules, Telegram, Vision, API, database, prices, cost, LKM, materials, .env, orders.db, .git, tokens, keys, old Malyarka, bot.py, Docker, commits/push, folder renames, Corel files or production export were touched.

## BATCH_SERIES_061_063 User Guide And Local Release Check

Status:

```text
executed / documentation and control check
```

Created:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_LOCAL_RELEASE_CHECK.md
E:\Hermes-Hub\docs\MALYARKA_CLEAN_CURRENT_LOCAL_RELEASE.md
```

Changed:

```text
E:\Hermes-Hub\README_КАК_ПОЛЬЗОВАТЬСЯ.md
```

Instruction update:

```text
README now starts with the short main workflow:
open ORDER_INPUT.txt -> paste and save order -> run ЗАПУСТИТЬ_ЗАКАЗ.cmd -> open LAST_ORDER_RESULT.txt -> take COREL_EXPORT.xlsx if status is clean.
```

Control checks:

```text
ЗАПУСТИТЬ_ЗАКАЗ.cmd clean -> exit 0, Excel created/updated.
ЗАПУСТИТЬ_ЗАКАЗ.cmd has_disputes -> exit 2, Excel not updated.
ЗАПУСТИТЬ_ЗАКАЗ.cmd empty_or_invalid -> exit 2, Excel not updated.
Focused pytest -> 37 passed.
```

Current local release:

```text
Local version with Excel/Corel export is fixed as the current working local release.
Main launcher: E:\Hermes-Hub\ЗАПУСТИТЬ_ЗАКАЗ.cmd
Input: E:\Hermes-Hub\inputs\ORDER_INPUT.txt
Text result: E:\Hermes-Hub\outputs\LAST_ORDER_RESULT.txt
Excel for Corel: E:\Hermes-Hub\outputs\COREL_EXPORT.xlsx
```

Recommended next series:

```text
BATCH_SERIES_064_066_NEXT_MAJOR_DIRECTION_SELECTION
```

No new working logic, functions, parser changes, area calculation changes, dispute rule changes, Telegram, Vision, API, database, prices, cost, LKM, materials, .env, orders.db, .git, tokens, keys, old Malyarka, bot.py, Docker, commits/push, folder renames, Corel files or production export were touched.

## BATCH_SERIES_064_066 Next Major Direction Selection

Status:

```text
executed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_NEXT_MAJOR_DIRECTION_REVIEW.md
E:\Hermes-Hub\docs\MALYARKA_CLEAN_TELEGRAM_STAGE_PREVIEW.md
E:\Hermes-Hub\docs\MALYARKA_CLEAN_RECOMMENDED_NEXT_MAJOR_DIRECTION.md
```

Reviewed next directions:

```text
Telegram
local interface / menu
order database
Vision / photo
prices and calculations
LKM and materials
order archive
production workflow preparation
```

Recommended next major direction:

```text
Telegram layer, but only after a separate safe planning series.
```

Telegram constraints:

```text
Do not implement Telegram now.
Do not write Telegram code.
Do not touch Telegram token.
Do not read or edit .env.
Do not run polling.
Do not use old bot.py as active source.
```

Recommended next series:

```text
BATCH_SERIES_067_069_SAFE_TELEGRAM_LAYER_PLANNING
```

No code, .cmd files, tests, Telegram launch, polling, Telegram token, .env, orders.db, .git, tokens, keys, old Malyarka, old bot.py, Vision, API, database, prices, cost, LKM, materials, Docker, commits/push, folder renames, parser changes, area calculation changes, dispute rule changes or production export were touched.

## STRATEGIC TELEGRAM PRINCIPLE: Flexibility and Reliability

Existing server Telegram bot must not become an experimental playground.

Current priority:

```text
1. flexibility
2. reliability
3. controllability
4. rollback ability
5. minimal risk for live polling
```

Do not inject Hermes directly into the live bot now.

First build safe infrastructure around the existing bot:

```text
1. Safe read-only collector
2. Architecture map
3. Hermes adapter layer
4. Feature flags / safe diagnostics
5. Rollback plan
```

Allowed future automation:

```text
collect structure
read allowlisted files
redact suspicious lines
create report
map handlers
map buttons
map modes
map Telegram -> core relation
```

Not allowed without separate user permission:

```text
change server code
stop Telegram bot
restart polling
connect token
read .env
read token environment variables
change systemd
change cron
change database
deploy
live integration
actions with real orders
```

Main formula:

```text
map and protection layer first,
then adapter,
then diagnostics and flags,
only after that small live-bot changes.
```

Next safe step:

```text
Safe read-only collector series for the server Telegram bot.
```

## BATCH_SERIES_131_134 Server Bot Safe Read-Only Collector

Status:

```text
executed / local tool only
```

Created:

```text
E:\Hermes-Hub\tools\server_bot\collect_server_bot_read_only.py
E:\Hermes-Hub\tests\test_server_bot_read_only_collector.py
E:\Hermes-Hub\docs\SERVER_BOT_READ_ONLY_COLLECTOR.md
E:\Hermes-Hub\docs\SERVER_BOT_READ_ONLY_COLLECTOR_ACCEPTANCE.md
```

Collector:

```text
reads only whitelist files
read-only
does not import bot modules
does not execute bot code
does not start processes
does not read environment variables
does not read .env/token/secrets/db/logs
redacts suspicious secret-like lines
builds SERVER_BOT_READ_ONLY_REPORT.md
```

Whitelist:

```text
malyarka_telegram/app.py
malyarka_telegram/router.py
malyarka_telegram/handlers.py
malyarka_telegram/keyboards.py
malyarka_telegram/messages.py
malyarka_telegram/access.py
malyarka_telegram/modes.py
malyarka_telegram/session.py
malyarka_telegram/intent.py
malyarka_telegram/models.py
malyarka_core/services/orders.py
malyarka_core/services/archive.py
malyarka_core/parsing.py
malyarka_core/validation.py
malyarka_core/calculations.py
requirements.txt
MALYARKA_CURRENT_STATE.md
```

Checks:

```text
python -m pytest E:\Hermes-Hub\tests\test_server_bot_read_only_collector.py -q -> 5 passed
local dry-run on temporary test folder -> SERVER_BOT_READ_ONLY_REPORT.md created
```

Important:

```text
Server was not touched.
Server files were not read.
Token and .env were not read.
Telegram/polling was not started, stopped or restarted.
Existing bot code was not changed.
```

Recommended next safe step:

```text
Plan a safe first use of the collector on a read-only copy, or request separate permission for future server-side read-only collection.
```

## BATCH_SERIES_117_120 Telegram Pre-Token Readiness Check

Status:

```text
executed / safe dry-run only
```

Created:

```text
E:\Hermes-Hub\projects\malyarka-clean\src\malyarka_clean_telegram\readiness.py
E:\Hermes-Hub\projects\malyarka-clean\tools\check_telegram_pre_token_readiness.py
E:\Hermes-Hub\projects\malyarka-clean\tests\test_telegram_pre_token_readiness.py
E:\Hermes-Hub\docs\MALYARKA_CLEAN_TELEGRAM_PRE_TOKEN_READINESS.md
```

Readiness diagnostics:

```text
telegram_skeleton_ready: true
adapter_ready: true
safe_check_ready: true
config_check_ready: true
token_env_safety_plan_ready: true
ready_for_token_stage: false
requires_user_permission_for_token: true
requires_user_permission_for_env: true
live_telegram_allowed: false
polling_allowed: false
token_used: false
env_read: false
old_bot_py_used: false
```

Checks:

```text
python -m pytest E:\Hermes-Hub\projects\malyarka-clean\tests\test_telegram_pre_token_readiness.py -q -> 7 passed
python E:\Hermes-Hub\projects\malyarka-clean\tools\check_telegram_pre_token_readiness.py -> OK
```

Important:

```text
Telegram live was not started.
Polling was not started.
Token was not used.
.env was not read or created.
Environment variables with token were not read.
Old bot.py was not used.
Excel was not created.
```

Recommended next safe step:

```text
Choose the next direction: continue safe planning without token, or separately plan the future token/.env stage before any live Telegram work.
```

## BATCH_SERIES_121_124 Existing Telegram Bot Server Inventory

Status:

```text
executed / documentation only
```

Created:

```text
E:\Hermes-Hub\docs\EXISTING_TELEGRAM_BOT_SERVER_INVENTORY.md
```

Fixed facts:

```text
Server: hermes
IP: 178.104.95.187
Bot path: /opt/malyarka-telegram-bot
Running process: /opt/malyarka-telegram-bot/.venv/bin/python -m malyarka_telegram.app --run-polling
Mode: polling
Environment: .venv
Explicit systemd/screen/tmux/root cron launch was not found during manual inventory.
Autostart method is still unknown and requires a separate future read-only check.
```

Important:

```text
Codex did not connect to the server.
Server files were not read by Codex.
Token was not read.
.env was not read.
Telegram bot was not stopped, started or restarted.
Existing server bot code was not changed.
```

Recommended next safe step:

```text
Plan a separate read-only server bot map: allowed files, forbidden files, safe way to inspect app.py/config.py/handlers.py without token, and safe way to identify autostart without stopping the bot.
```

## BATCH_SERIES_125_128 Server Bot Read-Only Map Plan

Status:

```text
executed / documentation only
```

Created:

```text
E:\Hermes-Hub\docs\SERVER_BOT_READ_ONLY_MAP_PLAN.md
```

Fixed plan:

```text
Future read-only mapping of the existing server Telegram bot must be done only after separate user permission.
The plan lists allowed files, forbidden secret zones, future read-only order, and hard prohibitions.
Codex did not connect to the server and did not read server files.
```

Important:

```text
Server was not touched.
Existing Telegram bot was not touched.
Token was not read.
.env was not read.
Telegram bot was not started, stopped or restarted.
Existing bot code was not changed.
```

Recommended next safe step:

```text
After separate user permission, perform a manual read-only inspection of app.py/config.py/handlers.py/router.py without token, without .env and without stopping polling.
```

## BATCH_SERIES_099_101_CREATE_TEST_ORDER_CARD

Status:

```text
executed / one test ORDER_CARD.md created
```

Created:

```text
E:\РАБОТА\01_ЗАКАЗЫ\2026\06_Июнь\Тестовый_заказ\ORDER_CARD.md
E:\Hermes-Hub\docs\TEST_ORDER_CARD_ACCEPTANCE.md
```

Verified before creation:

```text
E:\РАБОТА\01_ЗАКАЗЫ\2026\06_Июнь\Тестовый_заказ exists
01_Исходные exists
02_Corel exists
03_ArtCAM exists
04_Excel exists
05_Покраска exists
```

Important:

```text
Only one ORDER_CARD.md was created.
It was created only inside the test order folder.
No other ORDER_CARD.md files were created.
E:\Заказы 2026 was not touched.
Old orders were not touched.
Real .cdr/.art/.xlsx files were not touched.
Абай_планки and Петр_столики were not created or changed.
Prices, salaries, warehouse, materials, LKM and economy were not calculated.
```

Next safe step:

```text
Review the test ORDER_CARD.md and decide whether to plan a read-only validation checklist for order folders.
```

## BATCH_SERIES_102_104_ACCEPT_ORDER_CARD_AND_WORK_FOLDER_BASE

Status:

```text
executed / acceptance only
```

Created:

```text
E:\Hermes-Hub\docs\ORDER_CARD_V0_1_ACCEPTANCE.md
```

Accepted:

```text
ORDER_CARD.md v0.1 accepted.
User decision: ОСТАВЛЯЕМ.
The test card in Тестовый_заказ is suitable.
Do not simplify or redesign the card now.
E:\РАБОТА v0.1 is ready as the base working structure.
```

Current base:

```text
E:\РАБОТА exists.
01_ЗАКАЗЫ exists.
02_ШАБЛОНЫ exists.
03_ИНСТРУМЕНТЫ exists.
04_АРХИВ exists.
05_РАЗОБРАТЬ exists.
```

Test order:

```text
E:\РАБОТА\01_ЗАКАЗЫ\2026\06_Июнь\Тестовый_заказ exists.
01_Исходные exists.
02_Corel exists.
03_ArtCAM exists.
04_Excel exists.
05_Покраска exists.
ORDER_CARD.md exists.
```

Important:

```text
The test order is a template, not a real order.
First real order must be created only after a separate user instruction.
E:\Заказы 2026 was not touched.
Old orders were not moved.
Real .cdr/.art/.xlsx files were not touched.
```

Next safe step:

```text
Wait for a separate user instruction before creating the first real order.
```

## BATCH_SERIES_105_108_TELEGRAM_SAFE_CONFIG_CHECK

Status:

```text
executed / safe config-check only
```

Created:

```text
E:\Hermes-Hub\projects\malyarka-clean\src\malyarka_clean_telegram\config_check.py
E:\Hermes-Hub\projects\malyarka-clean\tools\check_telegram_config.py
E:\Hermes-Hub\projects\malyarka-clean\tests\test_telegram_config_check.py
E:\Hermes-Hub\docs\MALYARKA_CLEAN_TELEGRAM_SAFE_CONFIG_CHECK.md
```

Changed:

```text
E:\Hermes-Hub\projects\malyarka-clean\src\malyarka_clean_telegram\__init__.py
```

Diagnostics:

```text
live_telegram: false
polling: false
token_required: false
real_token_used: false
reads_env_file: false
uses_old_bot_py: false
safe_to_run_without_token: true
```

Checks:

```text
python -m pytest tests\test_telegram_config_check.py -q -> 7 passed
python tools\check_telegram_config.py -> exit 0, safe diagnostics OK
```

Important:

```text
Telegram live was not started.
Polling was not started.
Token was not used.
.env was not read.
Token environment variables were not read by the config-check.
Old bot.py was not imported.
Excel was not created by the config-check.
```

Next safe step:

```text
Plan a separate future token/.env handling stage before any real Telegram connection.
```

## BATCH_SERIES_113_116_CREATE_HERMES_NAVIGATION_INDEX

Status:

```text
executed / navigation index created
```

Created:

```text
E:\Hermes-Hub\handoff\HERMES_NAVIGATION_INDEX.md
```

Purpose:

```text
Short navigation file for ChatGPT/Hermes so large files like CHATGPT_CONTEXT_BUNDLE.md do not need to be pasted into chat.
```

Included:

```text
active project
main working zones
main document paths
latest accepted blocks
current forbidden zones
next safe step
instruction for working with large files
```

Next safe step:

```text
Серия 109–112 — План безопасной работы с Telegram token и .env
BATCH_SERIES_109_112_TELEGRAM_TOKEN_ENV_SAFETY_PLAN
```

Important:

```text
CHATGPT_CONTEXT_BUNDLE.md was used only as a local status source, not copied or summarized fully.
No secrets were added to HERMES_NAVIGATION_INDEX.md.
Telegram live, polling, token and .env were not touched.
No code was changed.
```

## BATCH_SERIES_109_112_TELEGRAM_TOKEN_ENV_SAFETY_PLAN

Status:

```text
executed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_TELEGRAM_TOKEN_ENV_SAFETY_PLAN.md
```

Accepted status:

```text
Telegram skeleton exists.
Safe check command exists.
Config-check exists.
Telegram token is not connected.
.env is not used.
Live Telegram has not been started.
Polling has not been started.
```

Rules:

```text
Token is introduced only after separate user permission.
Token is never printed to console, reports, bundle or state.
.env is not read, created or changed without separate user permission.
Old archive token/JSON data must not be used as active code or active secrets.
Future token/.env check may show only presence, never value.
Live Telegram is allowed only as a separate future stage.
```

Source reading:

```text
HERMES_NAVIGATION_INDEX.md was read.
CHATGPT_CONTEXT_BUNDLE.md was not read fully.
```

Next safe step:

```text
Wait for separate user instruction before any token/.env or live Telegram work.
```

## BATCH_SERIES_080_082_OLD_MALYARKA_ARCHIVE_FUTURE_PLAN

Status:

```text
executed / documentation only
```

Created:

```text
E:\Hermes-Hub\docs\OLD_MALYARKA_ARCHIVE_FUTURE_USE_PLAN.md
```

Archive status:

```text
old Malyarka archive is useful only as a source of future ideas
old archive is not current Hermes rules
nothing from the archive is transferred automatically
prices, salaries, materials, warehouse and LKM are unconfirmed archive candidates
old code / JSON / Telegram / Google Apps Script are archive-only, not active systems
```

Future blocks documented:

```text
order templates
Corel file template
prices
order economics
worker salaries
warehouse and materials
final order file
reference order runs
old rules
old code / JSON / Telegram / Google Apps Script
```

Not touched:

```text
Telegram live
polling
token
.env
orders.db
.git
old bot.py
old JSON as active code
real orders
E:\Заказы 2026
E:\РАБОТА
Corel
ArtCAM
CNC
Excel/Corel automation
active prices, salaries, warehouse, materials or LKM
parser
area calculation
dispute rules
commit/push
Docker
file moves
folder renames
```

Recommended next safe step:

```text
Continue safe Telegram layer first, then review archive blocks one by one with separate user confirmation.
```

## BATCH_SERIES_083_086_TELEGRAM_SAFE_CHECK_COMMAND

Status:

```text
executed / safe dry-check command
```

Created:

```text
E:\Hermes-Hub\projects\malyarka-clean\tools\check_telegram_skeleton.py
E:\Hermes-Hub\projects\malyarka-clean\tests\test_telegram_skeleton_check_command.py
E:\Hermes-Hub\docs\MALYARKA_CLEAN_TELEGRAM_SAFE_CHECK_COMMAND.md
```

Check command:

```text
python E:\Hermes-Hub\projects\malyarka-clean\tools\check_telegram_skeleton.py
```

What it checks:

```text
imports malyarka_clean_telegram
calls get_telegram_skeleton_diagnostics()
checks build_telegram_order_reply() on clean / has_disputes / empty_or_invalid
prints a Russian dry-check report
returns exit code 0 when the skeleton is safe
```

Diagnostics verified:

```text
live_telegram: false
polling: false
token_required: false
reads_env_file: false
uses_old_bot_py: false
sends_files=false
creates_excel=false
```

Tests:

```text
python -m pytest E:\Hermes-Hub\projects\malyarka-clean\tests\test_telegram_skeleton_check_command.py -q
6 passed
```

Not touched:

```text
Telegram live
polling
token
.env
orders.db
.git
old bot.py
old Telegram code
old JSON
Vision
API
database
prices
salaries
warehouse
materials
LKM
E:\Заказы 2026
E:\РАБОТА
real orders
real .cdr files
real .art files
real .xlsx files
Corel
ArtCAM
CNC
Excel/Corel automation
parser
area calculation
dispute rules
commit/push
Docker
file moves
folder renames
```

Recommended next safe step:

```text
Plan a safe Telegram configuration check without reading .env or using a real token, then request separate permission before any live connection.
```

## BATCH_SERIES_087_089_CREATE_EMPTY_WORK_FOLDER_STRUCTURE

Status:

```text
executed / existing empty work root verified
```

Result:

```text
E:\РАБОТА existed before this series.
The required five top-level v0.1 folders were present after the series.
Nothing was deleted, overwritten, moved or renamed.
```

Confirmed structure:

```text
E:\РАБОТА
├─ 01_ЗАКАЗЫ
├─ 02_ШАБЛОНЫ
├─ 03_ИНСТРУМЕНТЫ
├─ 04_АРХИВ
└─ 05_РАЗОБРАТЬ
```

Acceptance document:

```text
E:\Hermes-Hub\docs\WORK_FOLDER_EMPTY_STRUCTURE_ACCEPTANCE.md
```

Not created:

```text
specific order folders
Абай_планки
Петр_столики
year folders
month folders
order cards
```

Not touched:

```text
E:\Заказы 2026
old orders
real .cdr files
real .art files
real .xlsx files
Corel
ArtCAM
CNC
Telegram
polling
token
.env
orders.db
.git
old bot.py
Vision
API
database
prices
salaries
warehouse
materials
LKM
Excel/Corel automation
parser
area calculation
dispute rules
commit/push
Docker
folder renames
file moves
```

Recommended next safe step:

```text
Plan a first empty order-folder template under E:\РАБОТА only after separate user permission, without moving old orders.
```

## BATCH_SERIES_090_092_ORDER_FOLDER_TEMPLATE_PLANNING

Status:

```text
executed / documentation only
```

Created:

```text
E:\Hermes-Hub\docs\ORDER_FOLDER_TEMPLATE_V0_1.md
```

Planned future order path:

```text
E:\РАБОТА\01_ЗАКАЗЫ\2026\06_Июнь\Название_заказа
```

Planned single order folder structure:

```text
Название_заказа
├─ 01_Исходные
├─ 02_Corel
├─ 03_ArtCAM
├─ 04_Excel
└─ 05_Покраска
```

Future order card documented:

```text
Название_заказа\ORDER_CARD.md
```

Status of order card:

```text
future idea only
not created in E:\РАБОТА
```

Not created:

```text
real order folder
Название_заказа
Абай_планки
Петр_столики
year folders in E:\РАБОТА
month folders in E:\РАБОТА
ORDER_CARD.md in E:\РАБОТА
```

Not touched:

```text
E:\Заказы 2026
old orders
real .cdr files
real .art files
real .xlsx files
Corel
ArtCAM
CNC
Telegram
polling
token
.env
orders.db
.git
old bot.py
Vision
API
database
prices
salaries
warehouse
materials
LKM
Excel/Corel automation
parser
area calculation
dispute rules
commit/push
Docker
folder renames
file moves
```

Recommended next safe step:

```text
After separate user permission, create one empty real order folder from the v0.1 template; do not move old orders.
```

## BATCH_SERIES_093_095_CREATE_ONE_EMPTY_TEST_ORDER_FOLDER

Status:

```text
executed / one empty test order folder created
```

Base structure checked:

```text
E:\РАБОТА exists
E:\РАБОТА\01_ЗАКАЗЫ exists
```

Created:

```text
E:\РАБОТА\01_ЗАКАЗЫ\2026
E:\РАБОТА\01_ЗАКАЗЫ\2026\06_Июнь
E:\РАБОТА\01_ЗАКАЗЫ\2026\06_Июнь\Тестовый_заказ
E:\РАБОТА\01_ЗАКАЗЫ\2026\06_Июнь\Тестовый_заказ\01_Исходные
E:\РАБОТА\01_ЗАКАЗЫ\2026\06_Июнь\Тестовый_заказ\02_Corel
E:\РАБОТА\01_ЗАКАЗЫ\2026\06_Июнь\Тестовый_заказ\03_ArtCAM
E:\РАБОТА\01_ЗАКАЗЫ\2026\06_Июнь\Тестовый_заказ\04_Excel
E:\РАБОТА\01_ЗАКАЗЫ\2026\06_Июнь\Тестовый_заказ\05_Покраска
```

Acceptance document:

```text
E:\Hermes-Hub\docs\TEST_ORDER_FOLDER_ACCEPTANCE.md
```

Not created:

```text
real order files
ORDER_CARD.md
Excel files
Абай_планки
Петр_столики
```

Not touched:

```text
E:\Заказы 2026
old orders
real .cdr files
real .art files
real .xlsx files
Corel
ArtCAM
CNC
Telegram
polling
token
.env
orders.db
.git
old bot.py
Vision
API
database
prices
salaries
warehouse
materials
LKM
Excel/Corel automation
parser
area calculation
dispute rules
commit/push
Docker
file moves
old folder renames
```

Recommended next safe step:

```text
Review the empty test order folder, then plan whether to add a documentation-only ORDER_CARD.md template before creating any real order folders.
```

## BATCH_SERIES_096_098_ORDER_CARD_TEMPLATE_PLANNING

Status:

```text
executed / documentation only
```

Created:

```text
E:\Hermes-Hub\docs\ORDER_CARD_TEMPLATE_V0_1.md
```

Planned future file:

```text
ORDER_CARD.md inside a real order folder
```

Purpose:

```text
short human-readable order card
helps understand order name, client, material, files, work status, painting and unclear points
does not replace Corel, ArtCAM or Excel
```

Template sections:

```text
Основное
Тип заказа
Материал
Файлы
Детали
Примечания
Будущие данные
```

Future fields only:

```text
price
materials / warehouse
workers
salaries
final order economics
```

Important:

```text
future economy fields are not active
old Malyarka archive prices are not active
no price, warehouse, salary, material or LKM calculations were made
```

Not created:

```text
E:\РАБОТА\01_ЗАКАЗЫ\2026\06_Июнь\Тестовый_заказ\ORDER_CARD.md
```

Not touched:

```text
E:\РАБОТА\01_ЗАКАЗЫ\2026\06_Июнь\Тестовый_заказ
E:\Заказы 2026
old orders
real .cdr files
real .art files
real .xlsx files
Corel
ArtCAM
CNC
Telegram
polling
token
.env
orders.db
.git
old bot.py
Vision
API
database
prices
salaries
warehouse
materials
LKM
Excel/Corel automation
parser
area calculation
dispute rules
commit/push
Docker
file moves
folder renames
```

Recommended next safe step:

```text
Review ORDER_CARD_TEMPLATE_V0_1.md, then request separate permission before creating a real ORDER_CARD.md in the test order folder.
```

## BATCH_SERIES_070_073 Safe Telegram Skeleton No Live Run

Status:

```text
executed / safe non-live Telegram skeleton
```

Created:

```text
E:\Hermes-Hub\projects\malyarka-clean\src\malyarka_clean_telegram\__init__.py
E:\Hermes-Hub\projects\malyarka-clean\src\malyarka_clean_telegram\adapter.py
E:\Hermes-Hub\projects\malyarka-clean\src\malyarka_clean_telegram\messages.py
E:\Hermes-Hub\projects\malyarka-clean\src\malyarka_clean_telegram\diagnostics.py
E:\Hermes-Hub\projects\malyarka-clean\tests\test_telegram_adapter.py
E:\Hermes-Hub\docs\MALYARKA_CLEAN_TELEGRAM_SKELETON_ACCEPTANCE.md
```

Implemented:

```text
build_telegram_order_reply(order_text: str) -> str
```

The adapter:

```text
uses existing malyarka_clean_core.build_order_result
formats a Russian Telegram-style reply
shows status, confirmed rows, disputed rows, total_area_m2 and export_blocked
does not create Excel
does not send files
does not start Telegram or polling
does not read .env or require tokens
```

Checks:

```text
python -m pytest tests\test_telegram_adapter.py -q -> 7 passed
```

Recommended next series:

```text
Серия 074–076 — Проверка Telegram-каркаса и план безопасного подключения
BATCH_SERIES_074_076_TELEGRAM_SKELETON_CHECK_AND_CONNECTION_PLAN
```

No Telegram launch, polling, Telegram token, .env, orders.db, .git, tokens, keys, old Malyarka, old bot.py, Vision, API, database, prices, cost, LKM, materials, Docker, commits/push, folder renames, parser changes, area calculation changes, dispute rule changes, Excel/Corel export changes or production export were touched.

## BATCH_SERIES_074_076 Telegram Skeleton Check And Connection Plan

Status:

```text
executed / safe check and planning only
```

Created:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_TELEGRAM_SKELETON_CHECK.md
E:\Hermes-Hub\docs\MALYARKA_CLEAN_TELEGRAM_SAFE_CONNECTION_PLAN.md
```

Checked:

```text
malyarka_clean_telegram imports without token
import does not read .env
diagnostics reports live_telegram: false, polling: false, token_required: false, reads_env_file: false
adapter replies for clean / has_disputes / empty_or_invalid
adapter does not create COREL_EXPORT.xlsx
polling is not started
```

Focused test result:

```text
python -m pytest tests\test_telegram_adapter.py -q -> 7 passed
```

Planned future safe Telegram connection:

```text
separate check mode
safe import check without live launch
safe config check without showing token
only after separate permission connect token/.env
only after separate permission start polling
old bot.py not active
first live stage text orders only
no photo, Vision, API, database or prices
```

Recommended next series:

```text
Серия 077–079 — План структуры рабочей папки заказов
BATCH_SERIES_077_079_WORK_ORDERS_FOLDER_STRUCTURE_PLANNING
```

No Telegram live launch, polling, Telegram token, .env, orders.db, .git, tokens, keys, old Malyarka, old bot.py, Vision, API, database, prices, cost, LKM, materials, Docker, commits/push, folder renames, parser changes, area calculation changes, dispute rule changes, Excel/Corel export changes or production export were touched.

## BATCH_SERIES_077_079 Work Orders Folder Structure Planning

Status:

```text
executed / documentation only
```

Created:

```text
E:\Hermes-Hub\docs\WORK_FOLDER_STRUCTURE_V0_1.md
```

Planned future root:

```text
E:\РАБОТА
├─ 01_ЗАКАЗЫ
├─ 02_ШАБЛОНЫ
├─ 03_ИНСТРУМЕНТЫ
├─ 04_АРХИВ
└─ 05_РАЗОБРАТЬ
```

Planned single order structure:

```text
Папка_заказа
├─ 01_Исходные
├─ 02_Corel
├─ 03_ArtCAM
├─ 04_Excel
└─ 05_Покраска
```

Examples fixed:

```text
Абай планки
Петр столики
```

Important decisions:

```text
E:\РАБОТА was not created.
E:\Заказы 2026 was not touched.
Real .cdr/.art/.xlsx files were not touched.
The order folder structure is accepted as v0.1 documentation only.
```

Recommended next safe step:

```text
Review and accept WORK_FOLDER_STRUCTURE_V0_1.md before any real folder creation.
```

## BATCH_SERIES_080_082_CREATE_EMPTY_WORK_FOLDER_STRUCTURE

Status:

```text
executed / empty folders only
```

Created on disk:

```text
E:\РАБОТА
E:\РАБОТА\01_ЗАКАЗЫ
E:\РАБОТА\02_ШАБЛОНЫ
E:\РАБОТА\03_ИНСТРУМЕНТЫ
E:\РАБОТА\04_АРХИВ
E:\РАБОТА\05_РАЗОБРАТЬ
```

Created documentation:

```text
E:\Hermes-Hub\docs\WORK_FOLDER_EMPTY_STRUCTURE_ACCEPTANCE.md
```

Result:

```text
E:\РАБОТА did not exist before this series.
Only the empty root and five empty top-level folders were created.
No specific order folders were created.
```

Not touched:

```text
E:\Заказы 2026
old orders
real .cdr files
real .art files
real .xlsx files
Corel
ArtCAM
CNC
Telegram
polling
token
.env
orders.db
.git
old bot.py
Vision
API
database
prices
salaries
warehouse
materials
LKM
Excel/Corel automation
parser
area calculation
dispute rules
commit/push
Docker
folder renames
file moves
```

Recommended next safe step:

```text
Plan how to create the first empty order folder template inside E:\РАБОТА, without moving old orders.
```

## BATCH_SERIES_067_069 Safe Telegram Layer Planning

Status:

```text
executed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\MALYARKA_CLEAN_SAFE_TELEGRAM_RULES.md
E:\Hermes-Hub\docs\MALYARKA_CLEAN_TELEGRAM_MINIMAL_UX_PLAN.md
E:\Hermes-Hub\docs\MALYARKA_CLEAN_TELEGRAM_IMPLEMENTATION_PLAN.md
```

Planned:

```text
Safe Telegram layer on top of the existing local Malyarka Clean version.
Telegram must use the existing core and must not replace parser, area calculation or dispute rules.
```

Rules:

```text
Do not read .env.
Do not touch tokens or keys.
Do not run Telegram or polling.
Do not use old bot.py as active system.
Do not touch Excel/Corel export without separate plan.
Do not change parser, area calculation or dispute rules.
```

Minimal Telegram UX:

```text
User sends text order.
Bot returns status, confirmed rows, disputed rows and total area.
If clean, bot says Excel can be created locally.
If disputed, bot asks to fix only disputed rows.
No files, no photo, no Vision in the first Telegram UX.
```

Future implementation plan:

```text
Create a separate new Telegram adapter.
Start with import/check mode and no live Telegram launch.
Add focused tests.
Use dry-run before any live step.
Only after separate user permission touch token/.env/polling.
```

Recommended next series:

```text
Серия 070–073 — Безопасный Telegram-каркас без live-запуска
BATCH_SERIES_070_073_SAFE_TELEGRAM_SKELETON_NO_LIVE_RUN
```

No code, .cmd files, tests, Telegram launch, polling, Telegram token, .env, orders.db, .git, tokens, keys, old Malyarka, old bot.py, Vision, API, database, prices, cost, LKM, materials, Docker, commits/push, folder renames, parser changes, area calculation changes, dispute rule changes or production export were touched.


## BATCH_SERIES_135_138_SERVER_BOT_READ_ONLY_COPY_COLLECTION_PLAN

Status:

```text
executed / planning and local empty staging only
```

Created:

```text
E:\Hermes-Hub\docs\SERVER_BOT_READ_ONLY_COPY_COLLECTION_PLAN.md
E:\Hermes-Hub\inputs\server_bot_read_only_copy\README.md
E:\Hermes-Hub\inputs\server_bot_read_only_copy\MANIFEST.md
```

Result:

```text
Prepared a local empty staging folder for a future read-only copy of whitelisted server bot files.
Collector must not run on the server. Server files were not copied in this package.
```

Rules:

```text
Copy only whitelist files after separate user permission.
Do not copy .env, token, secrets, db, logs, .git, real orders or private data.
Run collector only on the local copy.
Expected future report: SERVER_BOT_READ_ONLY_REPORT.md.
After report creation, architecture analysis must be a separate step.
```

Next safe step:

```text
After separate user permission: place only whitelist files into E:\Hermes-Hub\inputs\server_bot_read_only_copy, then run the collector locally on that copy.
```

## BATCH_SERIES_139_142_SERVER_BOT_WHITELIST_COPY_INSTRUCTIONS

Status:

```text
executed / instructions only
```

Created:

```text
E:\Hermes-Hub\docs\SERVER_BOT_WHITELIST_COPY_INSTRUCTIONS.md
```

Updated:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy\MANIFEST.md
```

Result:

```text
Prepared instructions for future manual copying of only whitelist files into the local read-only staging folder.
No server connection was made. No server files were copied. Collector was not run.
```

Whitelist:

```text
malyarka_telegram/app.py
malyarka_telegram/router.py
malyarka_telegram/handlers.py
malyarka_telegram/keyboards.py
malyarka_telegram/messages.py
malyarka_telegram/access.py
malyarka_telegram/modes.py
malyarka_telegram/session.py
malyarka_telegram/intent.py
malyarka_telegram/models.py
malyarka_core/services/orders.py
malyarka_core/services/archive.py
malyarka_core/parsing.py
malyarka_core/validation.py
malyarka_core/calculations.py
requirements.txt
MALYARKA_CURRENT_STATE.md
```

Forbidden to copy:

```text
.env, token, secret files, environment dumps, orders.db, database files, logs, .git, JSON with secrets, private keys, real orders, real .cdr/.art/.xlsx files, whole folders without filtering.
```

Next safe step:

```text
After separate user permission: manually place only whitelist files into E:\Hermes-Hub\inputs\server_bot_read_only_copy, verify the checklist, then run the collector locally to create SERVER_BOT_READ_ONLY_REPORT.md.
```

## BATCH_SERIES_143_146_SERVER_BOT_MANUAL_WHITELIST_COPY_PACKAGE

Status:

```text
executed / manual instructions only
```

Created:

```text
E:\Hermes-Hub\docs\SERVER_BOT_MANUAL_WHITELIST_COPY_PACKAGE.md
E:\Hermes-Hub\docs\SERVER_BOT_STAGING_CHECKLIST.md
```

Updated:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy\MANIFEST.md
```

Result:

```text
Prepared a simple manual package for future safe copying of only whitelist server bot files into local staging.
No server connection was made. No server files were copied. Collector was not run.
```

Manual package covers:

```text
which files to copy
where to place them locally
which folders to create
how to check that .env/token/db/logs/.git were not copied
what to do after copying
```

Next safe step:

```text
After separate user permission: manually copy only whitelist files into E:\Hermes-Hub\inputs\server_bot_read_only_copy, complete SERVER_BOT_STAGING_CHECKLIST.md, update MANIFEST.md, then run collector locally.
```

## BATCH_SERIES_147_150_SERVER_BOT_STAGING_READY_FOR_MANUAL_COPY

Status:

```text
executed / local empty folder structure only
```

Created folders:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy\malyarka_telegram
E:\Hermes-Hub\inputs\server_bot_read_only_copy\malyarka_core
E:\Hermes-Hub\inputs\server_bot_read_only_copy\malyarka_core\services
```

Created document:

```text
E:\Hermes-Hub\docs\SERVER_BOT_STAGING_READY_FOR_MANUAL_COPY.md
```

Updated:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy\MANIFEST.md
```

Result:

```text
Local staging folder structure is ready for future manual whitelist file placement.
Server files were not copied. Collector was not run.
```

Next safe step:

```text
After separate user permission: manually place only whitelist files into staging, complete SERVER_BOT_STAGING_CHECKLIST.md, update MANIFEST.md, then run collector locally.
```

## BATCH_SERIES_151_154_SERVER_BOT_SFTP_WHITELIST_COPY

Status:

```text
executed / SFTP whitelist copy completed with one missing whitelist file
```

Connection:

```text
Connected to 178.104.95.187 by SFTP only.
No server shell commands were executed.
No collector was run on the server.
```

Copied whitelist files:

```text
malyarka_telegram/app.py
malyarka_telegram/router.py
malyarka_telegram/handlers.py
malyarka_telegram/keyboards.py
malyarka_telegram/messages.py
malyarka_telegram/access.py
malyarka_telegram/modes.py
malyarka_telegram/session.py
malyarka_telegram/intent.py
malyarka_core/services/orders.py
malyarka_core/services/archive.py
malyarka_core/parsing.py
malyarka_core/validation.py
malyarka_core/calculations.py
requirements.txt
MALYARKA_CURRENT_STATE.md
```

Missing whitelist file:

```text
malyarka_telegram/models.py - not found on server during SFTP get
```

Updated:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy\MANIFEST.md
```

Not copied:

```text
.env, token, secret files, environment dumps, config.py, orders.db, database files, logs, .git, JSON with secrets, private keys, real orders, real .cdr/.art/.xlsx files, folders recursively.
```

Next safe step:

```text
Review staging checklist, then separately decide whether to run the collector locally on E:\Hermes-Hub\inputs\server_bot_read_only_copy.
```

## BATCH_SERIES_155_158_SERVER_BOT_STAGING_CHECK_BEFORE_COLLECTOR

Status:

```text
executed / local staging check only
```

Created:

```text
E:\Hermes-Hub\docs\SERVER_BOT_STAGING_CHECK_RESULT.md
```

Checked staging:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy
```

Present whitelist files:

```text
malyarka_telegram/app.py
malyarka_telegram/router.py
malyarka_telegram/handlers.py
malyarka_telegram/keyboards.py
malyarka_telegram/messages.py
malyarka_telegram/access.py
malyarka_telegram/modes.py
malyarka_telegram/session.py
malyarka_telegram/intent.py
malyarka_core/services/orders.py
malyarka_core/services/archive.py
malyarka_core/parsing.py
malyarka_core/validation.py
malyarka_core/calculations.py
requirements.txt
MALYARKA_CURRENT_STATE.md
```

Missing whitelist file:

```text
malyarka_telegram/models.py - absent in staging and was not found on server during SFTP get
```

Forbidden files:

```text
No forbidden names found: .env, token/secrets, config.py, db/orders.db, logs, .git, JSON, real orders, real .cdr/.art/.xlsx.
```

Collector:

```text
not run
```

Next safe step:

```text
Separately decide whether to run the collector locally on E:\Hermes-Hub\inputs\server_bot_read_only_copy.
```

## BATCH_SERIES_159_162_SERVER_BOT_LOCAL_COLLECTOR_RUN

Status:

```text
executed / local collector run completed
```

Collector:

```text
E:\Hermes-Hub\tools\server_bot\collect_server_bot_read_only.py
```

Source:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy
```

Report created:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy\SERVER_BOT_READ_ONLY_REPORT.md
```

Files read by collector:

```text
malyarka_telegram/app.py
malyarka_telegram/router.py
malyarka_telegram/handlers.py
malyarka_telegram/keyboards.py
malyarka_telegram/messages.py
malyarka_telegram/access.py
malyarka_telegram/modes.py
malyarka_telegram/session.py
malyarka_telegram/intent.py
malyarka_core/services/orders.py
malyarka_core/services/archive.py
malyarka_core/parsing.py
malyarka_core/validation.py
malyarka_core/calculations.py
requirements.txt
MALYARKA_CURRENT_STATE.md
```

Missing file:

```text
malyarka_telegram/models.py
```

Safety status:

```text
read_only: true
whitelist_only: true
bot_code_executed: false
bot_modules_imported: false
processes_started: false
environment_read: false
env_file_read: false
token_read: false
files_changed: false
```

Redaction:

```text
22 suspicious secret-like lines were redacted in the report.
```

Not touched:

```text
server, live bot, polling, webhook, token, .env, config.py, environment variables, databases, logs, .git, real orders, Corel, ArtCAM, CNC, commit/push.
```

Next safe step:

```text
Analyze SERVER_BOT_READ_ONLY_REPORT.md and build an architecture map of the server Telegram bot without touching live Telegram.
```

## BATCH_SERIES_159_162_SERVER_BOT_LOCAL_COLLECTOR_RUN_REPEAT

Status:

```text
executed again / local collector run confirmed
```

Report updated:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy\SERVER_BOT_READ_ONLY_REPORT.md
```

Files read by collector:

```text
malyarka_telegram/app.py
malyarka_telegram/router.py
malyarka_telegram/handlers.py
malyarka_telegram/keyboards.py
malyarka_telegram/messages.py
malyarka_telegram/access.py
malyarka_telegram/modes.py
malyarka_telegram/session.py
malyarka_telegram/intent.py
malyarka_core/services/orders.py
malyarka_core/services/archive.py
malyarka_core/parsing.py
malyarka_core/validation.py
malyarka_core/calculations.py
requirements.txt
MALYARKA_CURRENT_STATE.md
```

Missing:

```text
malyarka_telegram/models.py
```

Safety status:

```text
read_only: true
whitelist_only: true
bot_code_executed: false
environment_read: false
env_file_read: false
token_read: false
```

Redaction:

```text
22 suspicious secret-like lines redacted.
```

Not touched:

```text
server, live bot, polling, webhook, token, .env, config.py, Vision, API, environment variables, databases, logs, .git, real orders, Corel, ArtCAM, CNC, commit/push.
```

## BATCH_SERIES_163_166_SERVER_TELEGRAM_BOT_ARCHITECTURE_MAP

Status:

```text
completed / local report analysis only
```

Created:

```text
E:\Hermes-Hub\docs\SERVER_TELEGRAM_BOT_ARCHITECTURE_MAP.md
E:\Hermes-Hub\docs\SERVER_TELEGRAM_BOT_ARCHITECTURE_MAP_SUMMARY.md
```

Source analyzed:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy\SERVER_BOT_READ_ONLY_REPORT.md
```

Architecture summary:

```text
Telegram -> app.py -> aiogram Dispatcher -> router.py -> handlers.py -> malyarka_core/services/orders.py -> parsing / validation / calculations -> exports / files
```

Key findings:

```text
entry point: malyarka_telegram/app.py
run mode: polling via --run-polling
missing file: malyarka_telegram/models.py
redaction: 22 suspicious secret-like lines redacted
Hermes adapter points: between router/handlers and core services, around order preview, before export callbacks, and as separate diagnostics/feature flags layer
```

Not touched:

```text
server, live bot, polling, webhook, token, .env, config.py, Vision, API, environment variables, databases, logs, .git, real orders, Corel, ArtCAM, CNC, commit/push.
```

Next safe step:

```text
BATCH_SERIES_167_170_HERMES_ADAPTER_LAYER_PLAN
```

## BATCH_SERIES_167_170_HERMES_ADAPTER_LAYER_PLAN

Status:

```text
completed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_LAYER_PLAN.md
E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_LAYER_PLAN_SUMMARY.md
```

Adapter position:

```text
Telegram -> app.py -> router.py / handlers.py -> Hermes adapter -> malyarka_core/services/orders.py
```

Proposed feature flags:

```text
HERMES_ADAPTER_ENABLED
HERMES_ASSISTANT_MODE_ENABLED
HERMES_ENGINEER_MODE_ENABLED
HERMES_ADMIN_CHANGES_ENABLED
HERMES_EXPORT_CALLBACKS_ENABLED
HERMES_SAFE_MODE
```

Fallback rule:

```text
If Hermes adapter is disabled, unavailable, unsafe, or fails, the existing Telegram bot must continue through the current logic.
```

Not touched:

```text
server, live bot, polling, webhook, token, .env, config.py, Vision, API, environment variables, databases, logs, .git, real orders, Corel, ArtCAM, CNC, commit/push.
```

Next safe step:

```text
BATCH_SERIES_171_174_HERMES_ADAPTER_FLAGS_DIAGNOSTICS_ROLLBACK_PLAN
```

## BATCH_SERIES_171_174_HERMES_ADAPTER_FLAGS_DIAGNOSTICS_ROLLBACK_PLAN

Status:

```text
completed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FLAGS_DIAGNOSTICS_ROLLBACK_PLAN.md
E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FLAGS_DIAGNOSTICS_ROLLBACK_PLAN_SUMMARY.md
```

Feature flags:

```text
HERMES_ADAPTER_ENABLED
HERMES_ASSISTANT_MODE_ENABLED
HERMES_ENGINEER_MODE_ENABLED
HERMES_ADMIN_CHANGES_ENABLED
HERMES_EXPORT_CALLBACKS_ENABLED
HERMES_SAFE_MODE
```

Defaults:

```text
all new features off
HERMES_SAFE_MODE=true
existing Telegram bot works as before
```

Rollback:

```text
HERMES_ADAPTER_ENABLED=false
HERMES_SAFE_MODE=true
keep old router/handlers/core flow
no direct app.py, polling, token, .env, config.py, or database changes
```

Not touched:

```text
server, live bot, polling, webhook, token, .env, config.py, Vision, API, environment variables, databases, logs, .git, real orders, Corel, ArtCAM, CNC, commit/push.
```

Next safe step:

```text
BATCH_SERIES_175_178_HERMES_ADAPTER_DRY_RUN_CONTRACT_PLAN
```

## BATCH_SERIES_175_178_HERMES_ADAPTER_DRY_RUN_CONTRACT_PLAN

Status:

```text
completed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_DRY_RUN_CONTRACT_PLAN.md
E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_DRY_RUN_CONTRACT_PLAN_SUMMARY.md
```

Dry-run principle:

```text
adapter changes nothing, sends no Telegram messages, creates no files, and starts no external actions
```

Input contract:

```text
text
user_id
current_mode
route_result
order_preview
owner_access_status
feature_flags
safe_context_summary
```

Output contract:

```text
status
response_text
action
warnings
blocked_reason
suggested_next_step
export_allowed
engineer_task_draft
diagnostics
fallback_required
```

Safety:

```text
forbidden or unknown actions are ignored; old Telegram flow uses fallback
```

Not touched:

```text
server, live bot, polling, webhook, token, .env, config.py, Vision, API, environment variables, databases, logs, .git, real orders, Corel, ArtCAM, CNC, commit/push.
```

Next safe step:

```text
BATCH_SERIES_179_182_HERMES_ADAPTER_CONTRACT_TEST_PLAN
```

## BATCH_SERIES_179_182_HERMES_ADAPTER_CONTRACT_TEST_PLAN

Status:

```text
completed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_CONTRACT_TEST_PLAN.md
E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_CONTRACT_TEST_PLAN_SUMMARY.md
```

Planned contract test groups:

```text
allowed actions
forbidden actions
unknown action
missing required fields
wrong field types
empty output
dangerous extra fields
fallback_required=true
unsafe diagnostics
adapter off by default
feature flags
```

Safety:

```text
No code, no pytest files, no adapter implementation, no server/live bot/token/.env/config.py/db/logs/.git access.
```

Next safe step:

```text
BATCH_SERIES_183_186_HERMES_ADAPTER_FAKE_ADAPTER_TEST_DOUBLE_PLAN
```

## SERVICE_START_NEW_CHAT_PROMPT_AUTO_HANDOFF

Status:

```text
completed / service handoff file created
```

Created:

```text
E:\Hermes-Hub\handoff\START_NEW_CHAT_PROMPT.md
```

Purpose:

```text
Short prompt for starting a new ChatGPT chat without pasting large context files.
```

Active line:

```text
Safe connection of the existing server Telegram bot to Hermes Hub through Hermes adapter layer.
```

Last accepted package:

```text
BATCH_SERIES_179_182_HERMES_ADAPTER_CONTRACT_TEST_PLAN
```

Next safe step:

```text
BATCH_SERIES_183_186_HERMES_ADAPTER_FAKE_ADAPTER_TEST_DOUBLE_PLAN
```

Auto-handoff rule:

```text
After each accepted package, Codex must update E:\Hermes-Hub\handoff\START_NEW_CHAT_PROMPT.md with current status and next safe step.
```

Not touched:

```text
server, live bot, polling, webhook, token, .env, config.py, environment variables, databases, logs, .git, real orders, Corel, ArtCAM, CNC, Vision/API, commit/push, existing bot code.
```

## BATCH_SERIES_183_186_HERMES_ADAPTER_FAKE_ADAPTER_TEST_DOUBLE_PLAN

Status:

```text
completed / planning only
```

Created:

```text
E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FAKE_ADAPTER_TEST_DOUBLE_PLAN.md
E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FAKE_ADAPTER_TEST_DOUBLE_PLAN_SUMMARY.md
```

Planned fake scenarios:

```text
safe allowed action
forbidden action
unknown action
empty output
missing required fields
wrong field types
unsafe diagnostics
fallback_required=true
adapter off by default
feature flags blocking export/admin/write actions
```

Planned fake outputs:

```text
valid output
blocked output
unsafe output
malformed output
fallback output
```

Safety:

```text
No code, no pytest files, no fake adapter implementation, no server/live bot/token/.env/config.py/db/logs/.git/staging-code/Vision/API access.
```

Next safe step:

```text
BATCH_SERIES_187_190_HERMES_ADAPTER_FAKE_ADAPTER_TEST_DOUBLE_IMPLEMENTATION
only after separate user permission
```

## Update 2026-06-15 07:57:28 — BATCH_SERIES_187_190

Implemented local fake adapter / local test double for Hermes adapter contract tests.

Created:
- E:\Hermes-Hub\local_tests\hermes_adapter_fake\fake_adapter.py
- E:\Hermes-Hub\local_tests\hermes_adapter_fake\test_fake_adapter_contract.py
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FAKE_ADAPTER_IMPLEMENTATION_187_190_REPORT.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FAKE_ADAPTER_IMPLEMENTATION_187_190_SUMMARY.md

Verification:
- python -m pytest local_tests\hermes_adapter_fake -q
- 33 passed

Safety: server/live bot/token/.env/config.py/polling/webhook/Vision/API/real orders were not touched.

Next safe step:
- Series 191-194 — local contract boundary check between fake adapter and dry-run contract schema.

## Update 2026-06-15 08:03:17 — BATCH_SERIES_191_194

Added local dry-run contract boundary checks for Hermes adapter fake adapter.

Created:
- E:\Hermes-Hub\local_tests\hermes_adapter_fake\test_fake_adapter_dry_run_boundary.py
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_DRY_RUN_BOUNDARY_CHECK_191_194_REPORT.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_DRY_RUN_BOUNDARY_CHECK_191_194_SUMMARY.md

Verification:
- python -m pytest local_tests\hermes_adapter_fake -q
- 66 passed

fake_adapter.py was not changed.
Safety: server/live bot/token/.env/config.py/polling/webhook/Vision/API/real orders were not touched.

Next safe step:
- Series 195-198 — local feature flags gate check for fake adapter contract.

## Update 2026-06-15 08:11:30 — BATCH_SERIES_195_198

Added local feature flags gate checks for Hermes adapter fake adapter.

Created:
- E:\Hermes-Hub\local_tests\hermes_adapter_fake\test_fake_adapter_feature_flags_gate.py
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FEATURE_FLAGS_GATE_CHECK_195_198_REPORT.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FEATURE_FLAGS_GATE_CHECK_195_198_SUMMARY.md

Verification:
- python -m pytest local_tests\hermes_adapter_fake -q
- 99 passed

fake_adapter.py was not changed.
Safety: server/live bot/token/.env/config.py/polling/webhook/Vision/API/real orders/staging/production bot code were not touched.

Next safe step:
- Series 199-202 — local diagnostics safety check for fake adapter contract.

## Update 2026-06-15 08:22:42 — BATCH_SERIES_199_202

Added local diagnostics safety checks for Hermes adapter fake adapter.

Created:
- E:\Hermes-Hub\local_tests\hermes_adapter_fake\test_fake_adapter_diagnostics_safety.py
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_DIAGNOSTICS_SAFETY_CHECK_199_202_REPORT.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_DIAGNOSTICS_SAFETY_CHECK_199_202_SUMMARY.md

Changed:
- E:\Hermes-Hub\local_tests\hermes_adapter_fake\fake_adapter.py

Reason: diagnostics safety tests found missing unsafe markers for server paths and live log paths; only local fake adapter sensitive markers were extended.

Verification:
- python -m pytest local_tests\hermes_adapter_fake -q
- 114 passed

Safety: server/live bot/token/.env/config.py/polling/webhook/Vision/API/real orders/staging/production bot code were not touched.

Next safe step:
- Series 203-206 — local rollback/no-side-effects contract check for fake adapter.

## Update 2026-06-15 08:33:00 — BATCH_SERIES_203_206

Added local rollback/no-side-effects contract checks for Hermes adapter fake adapter.

Created:
- E:\Hermes-Hub\local_tests\hermes_adapter_fake\test_fake_adapter_rollback_no_side_effects.py
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_ROLLBACK_NO_SIDE_EFFECTS_CHECK_203_206_REPORT.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_ROLLBACK_NO_SIDE_EFFECTS_CHECK_203_206_SUMMARY.md

Verification:
- python -m pytest local_tests\hermes_adapter_fake -q
- 140 passed

fake_adapter.py was not changed.
Safety: server/live bot/token/.env/config.py/polling/webhook/Vision/API/real orders/staging/production bot code were not touched.

Next safe step:
- Series 207-210 — local final fake adapter safety baseline before server adapter boundary plan.

## Update 2026-06-15 11:32:58 — BATCH_SERIES_207_210

Added final local safety baseline checks for Hermes adapter fake adapter.

Created:
- E:\Hermes-Hub\local_tests\hermes_adapter_fake\test_fake_adapter_final_safety_baseline.py
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FINAL_FAKE_ADAPTER_SAFETY_BASELINE_207_210_REPORT.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FINAL_FAKE_ADAPTER_SAFETY_BASELINE_207_210_SUMMARY.md

Verification:
- python -m pytest local_tests\hermes_adapter_fake -q
- 166 passed

fake_adapter.py was not changed.
Safety: server/live bot/token/.env/config.py/polling/webhook/Vision/API/real orders/staging/production bot code were not touched.

Next safe step:
- Series 211-214 — plan server adapter boundary between future server adapter and existing live bot.

## Update 2026-06-15 11:44:50 — BATCH_SERIES_211_214

Created server adapter boundary plan for future Hermes adapter integration with existing live Telegram bot.

Created:
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_SERVER_BOUNDARY_PLAN_211_214.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_SERVER_BOUNDARY_PLAN_211_214_SUMMARY.md

Planning only: no code, no tests, no pytest.

Boundary summary:
- future path: Telegram -> app.py -> router.py / handlers.py -> server adapter boundary -> Hermes adapter logic -> safe core/services/orders interaction
- adapter off by default
- feature flags required
- dry-run first
- diagnostics safe-only
- no side effects
- rollback-safe fallback
- no token/env/config/server path leaks
- no production imports
- no live Telegram calls

Safety: server/live bot/token/.env/config.py/os.environ/polling/webhook/Vision/API/real orders/staging/production bot code were not touched.

Next safe step:
- Series 215-218 — plan read-only server inventory procedure.

## Update 2026-06-15 12:03:29 — BATCH_SERIES_215_218

Created read-only server inventory procedure plan for existing server Telegram bot.

Created:
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_PROCEDURE_PLAN_215_218.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_PROCEDURE_PLAN_215_218_SUMMARY.md

Planning only: no code, no tests, no pytest, no SSH/server connection.

Procedure summary:
- future inventory is read-only only
- no execution/imports/polling/webhook/subprocess/network/API calls
- token/.env/config.py/os.environ/database/log/order contents are forbidden
- sensitive zones are presence-only
- redact-by-default
- explicit approval required before any inventory run

Safety: server/live bot/token/.env/config.py/os.environ/polling/webhook/Vision/API/real orders/staging/production bot code were not touched.

Next safe step:
- Series 219-222 — plan safe inventory report template.

## 2026-06-15 — BATCH_SERIES_219_222_HERMES_ADAPTER_SAFE_INVENTORY_REPORT_TEMPLATE_PLAN

Созданы markdown-документы:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_SAFE_INVENTORY_REPORT_TEMPLATE_PLAN_219_222.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_SAFE_INVENTORY_REPORT_TEMPLATE_PLAN_219_222_SUMMARY.md

Зафиксирован шаблон будущего safe inventory report для read-only server inventory: inventory scope, approval reference, checked/not checked, presence-only structure, bot layer map by filenames only, adapter boundary points, forbidden zones, redaction confirmation, runtime/live safety, risks, questions, no-touch confirmation и next safe step.

Presence-only поля: верхнеуровневые папки, имена Python-модулей, app/router/handlers, core/service/order, config/token/env/db/log zones только как факт, adapter insertion points по именам и структуре.

Запрещённые поля: token values, .env values, config.py secret values, os.environ values, database contents, live logs contents, реальные заказы, chat/user/owner IDs, private credentials, API keys, webhook URLs, production secrets.

Redaction rules: redact-by-default, secrets-as-presence-only, secret value/private ID никогда не записывать, sensitive zones только category/presence, unknown не угадывать, unsafe finding фиксировать без значения, отчёт должен быть безопасен для ChatGPT.

No-touch: server/live Telegram/token/.env/config.py/os.environ/Vision/API/реальные заказы/code/tests не трогались. Серверная inventory не выполнялась.

Следующий безопасный шаг: Серия 223-226 — план safe server inventory approval gate.

## 2026-06-15 — BATCH_SERIES_223_226_HERMES_ADAPTER_SAFE_SERVER_INVENTORY_APPROVAL_GATE_PLAN

Созданы markdown-документы:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_SAFE_SERVER_INVENTORY_APPROVAL_GATE_PLAN_223_226.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_SAFE_SERVER_INVENTORY_APPROVAL_GATE_PLAN_223_226_SUMMARY.md

Зафиксирован approval gate для будущей read-only server inventory. Будущий запуск inventory требует отдельной явной команды пользователя, ограниченной, одноразовой и с точной областью действия.

Явное разрешение должно прямо указывать read-only server inventory, процедуру 215-218, шаблон 219-222, запрет secret values, запрет запуска кода, запрет polling/webhook и запрет изменений файлов.

Не считаются разрешением: продолжай, +, делай дальше, посмотри сервер, проверь бота и любые расплывчатые сообщения без точного указания read-only inventory и границ.

Даже после разрешения остаются запрещёнными: token values, .env values, config.py secret values, os.environ values, database contents, live logs contents, реальные заказы, chat/user/owner IDs, private credentials, API keys, webhook URLs, production secrets и любые write operations.

Stop conditions: требуется прочитать secret value, запустить код, импортировать live bot module, открыть database/log/order contents, подключиться к Telegram/API/network вне scope, изменить файл, выполнить commit/push, scope неясный или есть риск раскрытия private data.

No-touch: server/live Telegram/token/.env/config.py/os.environ/Vision/API/реальные заказы/code/tests не трогались. Server inventory не выполнялась.

Следующий безопасный шаг: Серия 227-230 — финальная сверка документов server inventory readiness.

## 2026-06-15 — BATCH_SERIES_227_230_HERMES_ADAPTER_SERVER_INVENTORY_READINESS_FINAL_CHECK

Созданы markdown-документы:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_SERVER_INVENTORY_READINESS_FINAL_CHECK_227_230.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_SERVER_INVENTORY_READINESS_FINAL_CHECK_227_230_SUMMARY.md

Проведена финальная readiness-сверка документов 215-226 перед возможным отдельным разрешением на будущую read-only server inventory.

Подтверждено:

- procedure plan 215-218 готов;
- safe inventory report template 219-222 готов;
- approval gate 223-226 готов;
- server adapter boundary context 211-214 учтён;
- future inventory read-only only;
- требуется отдельное явное разрешение пользователя;
- +, продолжай, делай дальше, посмотри сервер, проверь бота не являются разрешением;
- presence-only поля зафиксированы;
- forbidden fields зафиксированы;
- redaction rules зафиксированы;
- stop conditions зафиксированы;
- secret values/db/log/order contents/private IDs/API keys/webhook URLs/write operations остаются запрещёнными даже после разрешения;
- no execution/no imports/no polling/no webhook/no subprocess/no network/API calls/no file modifications зафиксированы.

Противоречия между documents 215-226 не найдены.

No-touch: server/live Telegram/token/.env/config.py/os.environ/Vision/API/реальные заказы/code/tests не трогались. Server inventory не выполнялась.

Следующий безопасный шаг: остановиться и ждать отдельного явного разрешения пользователя на будущую read-only server inventory. Разрешением считается только точная команда из approval gate 223-226 или эквивалент с теми же границами.

## 2026-06-15 — BATCH_SERIES_231_234_HERMES_ADAPTER_READ_ONLY_SERVER_INVENTORY_RUN

Созданы markdown-документы:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_REPORT_231_234.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_REPORT_231_234_SUMMARY.md

Пользователь дал явное разрешение, совпадающее с approval gate 223-226:

Разрешаю выполнить read-only server inventory по утверждённой процедуре 215–218 и шаблону 219–222. Без чтения secret values, без запуска кода, без polling/webhook, без изменений файлов.

Результат: inventory заблокирована до сбора presence-only данных, потому что non-interactive SSH-доступ к root@178.104.95.187 завершился ошибкой: Permission denied (publickey,password).

Server presence-only данные не собраны:

- имена серверных файлов не получены;
- имена серверных папок не получены;
- /opt/malyarka-telegram-bot не пере-проверен в этом пакете;
- potential adapter boundary points не подтверждены свежей серверной структурой.

Safety confirmation:

Secret values were not read, copied, displayed, summarized, logged, or stored. Sensitive zones are recorded only as presence/category, not content.

Не читались: token values, .env, config.py content, os.environ, database contents, live logs contents, реальные заказы, private IDs, API keys, webhook URLs.

Не запускались: Python-код, live bot modules, app/router/handlers, polling/webhook, collector, bot subprocess, Telegram/API calls.

Не менялись: server files, базы, logs, production/staging bot code, git.

Следующий безопасный шаг: уточнить безопасный read-only способ доступа или предоставить ручной presence-only список. Переход к анализу 235-238 стоит отложить до появления реального safe inventory report с server presence-only данными.

## 2026-06-15 — BATCH_SERIES_231B_234B_HERMES_ADAPTER_SAFE_SSH_ACCESS_RECOVERY_PLAN

Созданы markdown-документы:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_SAFE_SSH_ACCESS_RECOVERY_PLAN_231B_234B.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_SAFE_SSH_ACCESS_RECOVERY_PLAN_231B_234B_SUMMARY.md

Контекст: read-only inventory 231-234 была заблокирована ошибкой Permission denied (publickey,password).

Локальная диагностика:

- SSH client установлен: OpenSSH_for_Windows_9.5p2, LibreSSL 3.8.2;
- локальная .ssh зона есть;
- presence-only SSH файлы: hetzner_hermes, hetzner_hermes.pub, known_hosts, known_hosts.old;
- SSH config отсутствует;
- public key name: hetzner_hermes.pub;
- private key candidate name only: hetzner_hermes.

Вероятная причина: предыдущая команда использовала прямой target root@178.104.95.187 без SSH config alias и без явного identity file, поэтому нужный ключ мог не выбраться автоматически или server не принимает user/key combination.

No-touch: private key contents/password/passphrase/token/.env/config.py/os.environ/server files/db/log/order contents не читались. Server inventory не выполнялась. Polling/webhook не запускались. Server files не изменялись.

Следующий безопасный шаг: пользователь предоставляет безопасные SSH-метаданные без секретов (SSH user, подтверждение key file hetzner_hermes или иной alias) либо ручной presence-only список. Повторная read-only inventory — только после восстановления доступа и отдельного подтверждения.

## 2026-06-16 — BATCH_231C_234C_EXPLICIT_SSH_KEY_INVENTORY_RETRY

Созданы markdown-документы:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_REPORT_231C_234C.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_REPORT_231C_234C_SUMMARY.md

Результат: SSH-доступ с явным ключом прошёл: ssh_ok.

Presence-only inventory выполнена для /opt/malyarka-telegram-bot.

Собрано только presence-only:

- ROOT_PRESENT yes;
- top-level: .venv, MALYARKA_CURRENT_STATE.md, malyarka_ai, malyarka_core, malyarka_telegram, malyarka_vision, requirements.txt;
- Python filenames до глубины 3;
- zone presence: app.py/router.py/handlers.py/services/orders.py/config.py present; .env/orders.db/db/database/logs/log not_present at project root.

Potential adapter boundary points by filename only:

- malyarka_telegram/router.py;
- malyarka_telegram/handlers.py;
- malyarka_telegram/app.py;
- malyarka_core/adapters/telegram.py;
- malyarka_core/services/orders.py;
- malyarka_core/exports/*.

No-secret/no-run/no-write:

Secret values were not read, copied, displayed, summarized, logged, or stored. Sensitive zones are recorded only as presence/category, not content.

Не читались: .env, config.py contents, token values, os.environ, databases, logs, real orders, private IDs, API keys, webhook URLs.

Не запускались: Python code, live bot modules, app/router/handlers, polling/webhook, collector. Server files не изменялись и не создавались.

Следующий безопасный шаг: 235-238 — анализ read-only inventory report и план минимального server adapter insertion design, без реализации кода и без изменения live-бота.

## 2026-06-16 — BATCH_235_238_SERVER_ADAPTER_INSERTION_DESIGN_PLAN

Созданы markdown-документы:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_ADAPTER_INSERTION_DESIGN_PLAN_235_238.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_ADAPTER_INSERTION_DESIGN_PLAN_235_238_SUMMARY.md

Проанализирован read-only inventory report 231C-234C и server boundary plan 211-214.

Presence-only server layers:

- malyarka_telegram;
- malyarka_core;
- malyarka_core/services/orders.py;
- malyarka_core/adapters/telegram.py;
- malyarka_core/exports/*;
- malyarka_ai;
- malyarka_vision;
- .venv;
- requirements.txt.

Candidate boundary points:

- malyarka_telegram/app.py;
- malyarka_telegram/router.py;
- malyarka_telegram/handlers.py;
- malyarka_core/adapters/telegram.py;
- malyarka_core/services/orders.py.

Минимальная безопасная design-точка выбрана: malyarka_core/adapters/telegram.py.

Причина: это adapter-shaped место по имени, оно не является app.py/polling entrypoint, позволяет оставить router.py/handlers.py как будущие tiny guarded call-sites, не трогать services/orders.py первым этапом и сохранить rollback через feature flags.

Первый будущий implementation должен быть off by default и dry-run only. Нужны feature flags: HERMES_ADAPTER_ENABLED=false, HERMES_SAFE_MODE=true, HERMES_DRY_RUN_ONLY=true, HERMES_SERVER_ADAPTER_ENABLED=false, HERMES_TELEGRAM_INSERTION_ENABLED=false, HERMES_EXPORT_CALLBACKS_ENABLED=false, HERMES_ADMIN_CHANGES_ENABLED=false.

No-touch: server files не читались и не менялись; live Telegram/polling/webhook не трогались; token/.env/config.py contents/os.environ/db/log/order contents не читались; код и тесты не создавались; collector/pytest не запускались.

Следующий безопасный шаг: 239-242 — план локального server adapter skeleton без подключения к live-боту.

## 2026-06-16 — BATCH_239_242_LOCAL_SERVER_ADAPTER_SKELETON_PLAN

Созданы markdown-документы:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_SKELETON_PLAN_239_242.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_SKELETON_PLAN_239_242_SUMMARY.md

Спроектирован локальный server adapter skeleton plan. Implementation пока запрещён.

Ключевые правила skeleton:

- будущая design-точка: malyarka_core/adapters/telegram.py;
- skeleton локальный, не подключается к live-боту;
- adapter off by default;
- первый режим dry-run only;
- feature flags обязательны;
- safe mode обязателен;
- fallback к текущему flow обязателен;
- side_effects=[];
- adapter не отправляет Telegram-сообщения напрямую;
- router.py/handlers.py могут быть только будущими tiny guarded call-sites;
- app.py первым этапом не трогать;
- services/orders.py первым этапом не менять.

Запреты зафиксированы: не читать token/.env/config.py contents/os.environ/db/log/order contents; не запускать polling/webhook/live modules/collector; не менять server files/staging/production code; не писать код и тесты.

No-touch: server files/live Telegram/token/.env/config.py contents/os.environ/db/log/order contents/Vision/API/staging/production code не трогались. Код и тесты не создавались.

Следующий безопасный шаг: 243-246 — план локального server adapter contract interface без реализации кода.

## 2026-06-16 — BATCH_243_246_LOCAL_SERVER_ADAPTER_CONTRACT_INTERFACE_PLAN

Созданы markdown-документы:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_CONTRACT_INTERFACE_PLAN_243_246.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_CONTRACT_INTERFACE_PLAN_243_246_SUMMARY.md

Спроектирован локальный server adapter contract interface для будущего Hermes adapter layer.

Future target: malyarka_core/adapters/telegram.py.

Request fields:

- action;
- payload;
- dry_run;
- feature_flags;
- safe_mode;
- diagnostics.

Response fields:

- ok;
- status;
- action;
- dry_run;
- blocked;
- fallback_required;
- reason;
- output_type;
- side_effects;
- diagnostics_safe.

Зафиксировано: adapter off by default, dry-run only, safe mode required, feature flags required, fallback to current flow, blocked/fallback/error responses structured and redacted, diagnostics safe-only, side_effects=[], adapter не отправляет Telegram-сообщения напрямую.

Запреты: token/.env/config.py contents/os.environ/db/log/order contents/private IDs/API keys/webhook URLs не читать; live modules/polling/webhook не запускать; file/db/log writes, exports/admin/write actions запрещены.

No-touch: server files/live Telegram/token/.env/config.py contents/os.environ/db/log/order contents/Vision/API/staging/production code не трогались. Код и тесты не создавались.

Следующий безопасный шаг: 247-250 — план локальных contract examples для server adapter interface без реализации кода.

## 2026-06-16 — BATCH_247_250_LOCAL_SERVER_ADAPTER_CONTRACT_EXAMPLES_PLAN

Созданы markdown-документы:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_CONTRACT_EXAMPLES_PLAN_247_250.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_CONTRACT_EXAMPLES_PLAN_247_250_SUMMARY.md

Спроектированы локальные contract examples для будущего server adapter interface.

Examples:

- adapter off by default;
- safe dry-run allowed;
- export blocked;
- admin blocked;
- write blocked;
- unknown action blocked;
- malformed request;
- fallback_required=true;
- diagnostics safe-only;
- unsafe diagnostics blocked.

Для каждого example описаны request shape, expected response shape, expected status, blocked/fallback flag, side_effects=[] и почему это безопасно.

Safety rules подтверждены: no direct Telegram send; no token/env/config/os.environ reads; no db/log/order contents; no private IDs/API keys/webhook URLs; no file/db/log writes; no polling/webhook; fallback to current flow when blocked or unsafe.

No-touch: server files/live Telegram/token/.env/config.py contents/os.environ/db/log/order contents/Vision/API/staging/production code не трогались. Код и тесты не создавались.

Следующий безопасный шаг: 251-254 — план локального adapter skeleton implementation gate, без реализации кода.

## 2026-06-16 — BATCH_251_254_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_GATE_PLAN

Созданы markdown-документы:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_GATE_PLAN_251_254.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_GATE_PLAN_251_254_SUMMARY.md

Спроектирован implementation gate для будущего локального adapter skeleton.

Gate требует:

- отдельное явное разрешение пользователя;
- local-only scope;
- точный список файлов, которые можно создать/изменить;
- точный список forbidden files/zones;
- rollback plan;
- contract interface 243-246;
- contract examples 247-250;
- off by default;
- dry-run only;
- safe mode required;
- feature flags required;
- side_effects=[];
- fallback к текущему flow;
- no direct Telegram send;
- no server/live changes.

Future target: malyarka_core/adapters/telegram.py, но первый implementation должен быть local-only, не server/production/staging.

Gate decision: implementation пока не разрешён.

No-touch: server files/live Telegram/token/.env/config.py contents/os.environ/db/log/order contents/Vision/API/staging/production code не трогались. Код и тесты не создавались.

Следующий безопасный шаг: 255-258 — план первого локального adapter skeleton implementation только после отдельного разрешения.

## 2026-06-16 — BUNDLE_255_270_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_PREP

Создан task-bundle:

- E:\Hermes-Hub\task_bundles\BUNDLE_255_270_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_PREP\TASK.md
- E:\Hermes-Hub\task_bundles\BUNDLE_255_270_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_PREP\README_FOR_CODEX.md

Созданы отчёты:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_ADAPTER_IMPLEMENTATION_PREP_BUNDLE_255_270_REPORT.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_ADAPTER_IMPLEMENTATION_PREP_BUNDLE_255_270_SUMMARY.md

Bundle включает крупный связанный план 255-270: первый локальный skeleton implementation plan, allowed/forbidden files, rollback, contract examples, acceptance checks, stop conditions, future test gates и порядок выполнения.

Этапы 255-270:

- 255-258: first local skeleton implementation plan;
- 259-262: local skeleton implementation after permission;
- 263-266: contract checks plan/tests after permission;
- 267-270: local acceptance and next boundary plan.

Правила: implementation не разрешён; требуется отдельное явное разрешение; local-only; off by default; dry-run only; safe mode required; feature flags required; side_effects=[]; fallback to current flow; no direct Telegram send; no server/live/staging/production changes; no secret reads.

No-touch: код не писался, tests не создавались, server/live/staging/production code не менялся, server connection не выполнялся, token/.env/config.py contents/os.environ/db/log/order contents не читались, polling/webhook/live modules не запускались, commit/push не выполнялся.

Следующий безопасный шаг: ждать отдельное явное разрешение на BATCH_255_258_FIRST_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_PLAN.

## HERMES-RULE-CONVEYOR-001

Status: installed (2026-06-17)

Правило конвейера установлено:

```text
E:\Hermes-Hub\rules\HERMES_RULE_CONVEYOR_001.md
```

Источник: `C:\Users\user\Desktop\hermes_hub_accelerated_conveyor_2026-06-17.zip`

Конвейер содержит 44 bundle-пакета (255–1560). Первый практический bundle: BUNDLE_255_270_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_PREP (AUTO_MARKDOWN).

Правило добавлено в:
- `AGENTS.md` — секция Conveyor Rule
- `START_HERE_FOR_HERMES.md` — ссылка в списке файлов
- `README.md` — ссылка в секции правил

## Agent Factory & Sales Client Intake Agent

Status: proposed (2026-06-17)

Создана система суб-агентов Hermes Hub:

```text
E:\Hermes-Hub\agents\AGENT_FACTORY_RULES.md
E:\Hermes-Hub\agents\AGENT_REGISTRY.md
E:\Hermes-Hub\agents\sales_client_intake_agent\
  AGENT_SPEC.md
  QUESTIONS.md
  INTAKE_CARD_TEMPLATE.md
  RESPONSE_TEMPLATES.md
  SAFETY_RULES.md
  HANDOFF_TO_MALYARKA.md
```

Первый агент: **Sales + Client Intake Agent** (`accepted`, not active).

Принят 2026-06-17. Код не пишется, live не подключается.

Документы агента (9 файлов): AGENT_SPEC, QUESTIONS, INTAKE_CARD_TEMPLATE, RESPONSE_TEMPLATES, SAFETY_RULES, HANDOFF_TO_MALYARKA, TEST_SCENARIOS (15 сценариев), ACCEPTANCE_CRITERIA (9 критериев).

Python-модуль создан 2026-06-17: `src/intake_agent.py` (5 функций), `tests/test_intake_agent.py` (23 теста), `tests/test_golden_cases.py` (25 тестов). Edge-case hardening выполнен: материал raw/confirmed, цвет raw/structured, location, finish_raw, handoff строже. 48/48 passed. Агент остаётся `accepted`, not active.

Цепочка: Клиент → Sales Intake → Intake Card → Malyarka Agent → Order Result → Corel Export.

Статусы агентов: proposed → accepted → active → blocked → archived.

В реестре запланировано 6 агентов.

## Server Patch Branch

```text
Статус: PAUSED на STOP_APPROVAL #9
Выполнено: 8 из 44 bundles (18%) + 1 skipped
TRUST_TEST_7: ✅ пройден без нарушений
- HERMES_AUTOPILOT_001: лимит зелёных задач увеличен с 7 до 10 (2026-06-17)
- GREEN_AUTOPILOT_PASS_10: первый проход — 10/10 задач (2026-06-17)
- Агенты: #1 accepted, #2-3 proposed, #4-5 planned, #6 proposed
- GREEN_AUTOPILOT_PASS_10_AGENT_SPEC_REVIEW: #2, #3, #6 → accepted_as_spec (not active)
- Handoff contracts: Sales→Malyarka, Malyarka Input/Output, Handoff Map
- GREEN_AUTOPILOT_PASS_10_AGENT_ECOSYSTEM_COMPLETION: #2, #3, #6 → accepted (not active)
- #4 Telegram Safe Adapter, #5 Memory → proposed (specs created)
- Active agents: 0 | Всего агентов: 6 | 3 автопрохода: 30/30 задач
- GREEN_AUTOPILOT_PASS_10_MALYARKA_AGENT_PRE_IMPLEMENTATION: #4, #5 → accepted
- Malyarka Agent pre-implementation: 4 docs (scenarios, criteria, fake cards, result template)
- 4 автопрохода: 40/40 задач. 0 нарушений.
- Malyarka Agent: offline module created (28/28 tests passed)
- Malyarka Agent: demo created (4/4 passed), golden cases documented
- Agent chain: Sales→Malyarka handoff ready
- Sales→Malyarka integration: verified offline (12/12 tests, 4/10 passed chain)
- Corel Export Agent: offline module created (18/18 tests passed)
- Corel Export Agent: row-order corrected (height_mm, width_mm, quantity)
- Full chain: Sales→Malyarka→Corel Export (94 tests total, all passed)
- Full-chain simulation: verified (12/12 tests, 4/10 full chain)
- FINAL CHECKPOINT 2026-06-17: 6 agents accepted, 118 tests passed, 0 active
- Next: NEXT_DECISION_GATE_AFTER_OFFLINE_CHAIN.md
- GREEN_SERIES_AUTOPILOT_200: 3 passes, 24+ docs created (launch readiness, preplans, runbooks)
- All green tasks for current sprint complete. Yellow/red gates require user approval.
- Real orders sandbox: GATE 2 complete (1 safe copy processed, full chain pass)
- Sandbox verified: not_final_order=true, review_required=true, production_ready=false
- Corrected: Corel dry-run created 9 files (not 7).
- Post-sandbox: diagnostics/memory snapshots created, Gate 3 instructions ready
- Sandbox checks: sandbox run (not pytest) — safe copy chain pass, tests unchanged
- Sandbox Gate 3: second safe copy (002) correctly blocked on disputed data
- Sandbox gates 1-3 complete: 001=chain pass, 002=correctly blocked
- Post-Gate 3 findings: 3 classification issues identified, fix plan created (NO code changed)
- Next: SALES_MALYARKA_GATE_4_FIX_NCS_AND_DISPUTED_CLASSIFICATION (YELLOW)
- Gate 5A complete: NCS raw preservation fixed — color_raw="NCS S4050-R" (S preserved)
- Full offline regression: 118/118 passed (0.22s)
- Sandbox closed. Next: A (more copies) / B (Telegram adapter) / C (server read-only)
- Telegram Safe Adapter Gate 1A: audit passed — 3 missing docs created, verifier warning harmless
- Total: 130/130 tests. Ready for Gate 2 (full-chain simulation)
- Telegram Safe Adapter Gate 2: full-chain simulation — 138/138 passed (20 adapter + 118 regression)
- Fake event → Adapter → Sales → Malyarka → Corel: verified offline
- Gate 2A audit: passed — warning harmless, 138/138 tests, ready for Gate 3
- Gate 3: contract hardening + failure matrix — 6 docs created, code unchanged
- Gate 4: failure tests added — 7 new tests, 145/145 passed, adapter hardened
- Server read-only prep: 8 docs created, ready RED prompt
- Server Gate 1: BLOCKED — SSH unavailable (Permission denied). No files read. No commands run.
- SSH recovery prep: local key verified, no new attempts, user steps created
- Autonomous recovery: 2 attempts, SSH still blocked — requires user console action to add public key
- Server Gate 1: BLOCKED_BY_MANUAL_RELAY_UNAVAILABLE — SSH not restored, manual relay not possible
- Parallel acceleration: 8 docs created while server blocked. Ready for SSH restoration.
- No-Codex acceleration: 10 docs created. Local MVP closeout complete. 145/145 tests.
- Project consolidation: 10 docs created. Codex handoff ready. Waiting state final.
- Temp SSH key created: ED25519, fingerprint SHA256:8cikYI... User adds via console.
- Gate 1 attempt: SSH to 178.104.95.187 — TIMEOUT → now Permission denied
- Diagnostic: TCP 22 OPEN. NOT firewall. Key not accepted by server.
- Hermes IP: 185.13.22.202. User: verify public key in authorized_keys via console.
- Server Gate 1: ✅ COMPLETE. Architecture verified via root SSH.
- Server Gate 2: ✅ COMPLETE. All 6 whitelist files reviewed.
- Server Gate 3: ✅ COMPLETE. Dry-run patch plan. 8 docs created. No code written.
- Server Gate 4: ✅ COMPLETE. Rollback/backup plan. 8 docs created. No code/patch/backup.
- Server Gate 5: ✅ COMPLETE. Staging patch plan. 8 docs created. Code drafts in markdown only.
- Server Gate 6: ✅ COMPLETE. Backup + staging apply. hermes_adapter.py created on server.
- Server Gate 7: ✅ COMPLETE. Focused tests passed (4/4). No live restart.
- Server Gate 8: ✅ COMPLETE. Isolated flag test. In-memory flag ON → all tests passed.
- Server Gate 9: ✅ COMPLETE. Live dry-run. Bot started with flag ON, tested, reverted OFF.
- Cleanup: ✅ Temp key removed. Server adapter integration COMPLETE. 9 gates. 4 backups.
- Reconnect kit: 6 docs created. Rescue steps documented. Key already removed.
- Final closeout: 7 docs. Server adapter complete. Safe state closed.
- Phase 2 plan: 6 docs created. Controlled enable + monitoring + rollback + test matrix + RED prompt.
- Phase 2 blocked: SSH unavailable. Rescue required. User action needed.
- Markdown cleanup: 2026-06-20. START_NEW_CHAT_PROMPT, NEXT_TASKS, ACTIVE_BATCH, NAVIGATION, sync/* updated.
- Status: HERMES_MARKDOWN_STATUS_CLEANUP_DONE. Next: Phase 2 requires separate decision.
- Next: REAL_ORDERS_SANDBOX_GATE_5_RECHECK_GATE_3_SCENARIO_AFTER_FIX
```
## 2026-06-20 — CODEX_HERMES_SYNC_LAYER_READY

Created shared sync folder:

```text
E:\Hermes-Hub\sync
```

Created protocol docs:

```text
E:\Hermes-Hub\docs\CODEX_HERMES_SYNC_PROTOCOL.md
E:\Hermes-Hub\docs\AGENT_ROUTING_RULES.md
E:\Hermes-Hub\docs\BATCH_VS_MICRO_TASK_RULES.md
E:\Hermes-Hub\docs\HERMES_CODEX_REPORT_FORMATS.md
E:\Hermes-Hub\docs\APPROVAL_GATE_REGISTRY.md
```

Routing:

- ChatGPT: decisions, acceptance, large task framing.
- Codex: batch packets, implementation, docs, complex checks, state/handoff updates.
- Hermes/cheap agent: safe micro-checks and summaries.
- Big contexts: `HERMES_PACKET_INBOX`.

Current shared status: server bot running, autostart disabled, feature flag OFF, Telegram test passed, production OFF, Phase 2 OFF.

Next queued batch:

```text
BATCH_HERMES_ADAPTER_PHASE2_DRY_RUN_PREP_AND_APPROVAL
```

No server, SSH, service, secrets, `.py`, git, production or Phase 2 actions were performed for the sync layer.

## Script Launcher Workflow Rule

Date: 2026-06-20

Status:

```text
SCRIPT_LAUNCHER_WORKFLOW_RULE_READY
```

Rule:

```text
NO_MANUAL_CMD_ONE_LINERS_FOR_PACKET_WORKFLOW
```

Long manual CMD/PowerShell one-liners are no longer the primary way to process ZIP/batch packets.

New standard:

- Micro tasks -> Hermes/cheap agent.
- Big batch -> Codex.
- Big context -> ZIP package.
- User-facing batch launch -> launcher script, not manual CMD.
- Shared state -> markdown sync/state/handoff files.

Launcher scripts should find ZIP, extract it, find `01_CODEX_TASK_*.md`, create `CODEX_PROMPT.txt`, copy prompt to clipboard, open prompt in Notepad, and show clear errors if ZIP/task is missing.

`HERMES_PACKET_INBOX` remains a legacy/additional mechanism.

If a terminal command is still needed, ask user first and keep it short.

No server, SSH, service, runtime, secrets, `.py`, git, Phase 2 or production actions were performed.

## 2026-06-20 — SIMPLE_CHATGPT_TO_CODEX_PROMPT_WORKFLOW_RESTORED

Active status:

```text
SIMPLE_CHATGPT_TO_CODEX_PROMPT_WORKFLOW_RESTORED
```

Active workflow:

1. Main task transfer to Codex is prompt text directly in ChatGPT.
2. ZIP / launcher / HERMES_PACKET_INBOX / LATEST_TASK_PATH are not used by default.
3. Launcher scripts are no longer the main workflow.
4. HERMES_PACKET_INBOX is no longer the main workflow.
5. Long user-facing CMD/PowerShell one-liners are not the main workflow.
6. If large context is needed, first agree on a simple file/ZIP separately, but still provide the prompt text in ChatGPT.
7. Always additionally provide the prompt text in ChatGPT.

Superseded / not active by default:

- NO_MANUAL_CMD_ONE_LINERS_FOR_PACKET_WORKFLOW
- SCRIPT_LAUNCHER_WORKFLOW_RULE_READY
- HERMES_PACKET_INBOX as default workflow

Still active:

- E:\Hermes-Hub\sync
- Codex/Hermes/ChatGPT sync through markdown files
- Micro tasks -> Hermes / cheap agent
- Big batch -> Codex
- Shared state -> markdown sync/state/handoff files

No-touch: server, SSH, service, Telegram runtime, feature flag, secrets, DB/logs/orders, `.py` code, git, Phase 2 and production were not touched.

## 2026-06-20 — BATCH_PHASE2_PREP_SSH_VERIFY_ROLLBACK

Status:

```text
PHASE2_DRY_RUN_PREP_READY_SSH_VERIFIED
```

Current verified state:

```text
server: hermes / 178.104.95.187
service: malyarka-telegram-bot.service
service state: active/running
autostart: disabled
process: /opt/malyarka-telegram-bot/.venv/bin/python -m malyarka_telegram.app --run-polling
Hermes adapter: installed
feature flag: _HERMES_ADAPTER_ENABLED = False
Telegram test: passed
production: OFF
Phase 2: OFF
SSH: verified read-only
```

Created/updated plan-only docs:

```text
E:\Hermes-Hub\docs\SERVER_SSH_ACCESS_CURRENT_STATUS.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_DRY_RUN_PREP_AND_APPROVAL.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_PRECHECK_CHECKLIST.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_COMMAND_PLAN_ONLY.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_TELEGRAM_TEST_PLAN.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_ROLLBACK_PLAN.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_REPORT_TEMPLATE.md
```

Approval phrase for any future Phase 2 dry-run:

```text
APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE
```

Routing remains active:

- Codex is not used for micro tasks.
- Hermes / DeepSeek handles safe micro checks.
- Codex is reserved for complex/risky batch work.

No-touch: Phase 2 was not launched; feature flag was not changed; production remains OFF; no service start/restart/stop/enable/disable was performed; `.env`, `config.py`, token, `os.environ`, DB, live logs and real orders were not read; `.py` code was not changed; git was not used.


## 2026-06-20 — PHASE2_DRY_RUN_FAILED_ROLLBACK_DONE

Status:

```text
PHASE2_DRY_RUN_FAILED_ROLLBACK_DONE
```

Summary:

- Phase 2 dry-run was explicitly approved with `APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE`.
- Precheck passed: SSH verified, service active/running, autostart disabled, feature flag OFF, adapter/hook present.
- Backup created: `/opt/malyarka-telegram-bot/malyarka_core/adapters/telegram.py.phase2_dry_run_backup_20260620`.
- Feature flag was temporarily set ON for controlled dry-run.
- Controlled restart was performed to apply temporary flag.
- Telegram test failed: `700 x 500` was diverted to English clarification (`What is 700 x 500 for?`) instead of expected Malyarka order flow.
- Rollback was executed immediately.
- Feature flag is now OFF.
- Controlled restart was performed to apply rollback.
- Final service state: active/running.
- Autostart remains disabled.
- Production remains OFF.

Created report:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_DRY_RUN_REPORT.md
```

Blocker:

```text
Hermes adapter currently interferes incorrectly with simple order-like input `700 x 500`.
```

Next safe step:

```text
Plan-only investigation of adapter dry-run behavior before any future flag enable.
```

No-touch: no production enable, no systemctl enable/stop, no autostart change, no `.env`, `config.py`, token, `os.environ`, DB, live logs or real orders read, no adapter logic change, no git.

## 2026-06-20 — PHASE2_FAILURE_INVESTIGATION_READY

Status:

```text
PHASE2_FAILURE_INVESTIGATION_READY
```

Source failure:

```text
PHASE2_DRY_RUN_FAILED_ROLLBACK_DONE
```

Finding:

`700 x 500` is order-like production-size input and must remain under Malyarka order flow. During Phase 2 dry-run the Hermes adapter diverted it to generic English clarification (`What is 700 x 500 for?`), so Phase 2 remains blocked.

Likely failure point:

```text
malyarka_core/adapters/telegram.py / malyarka_core/adapters/hermes_adapter.py boundary
```

Expected rule:

- order-like input -> adapter returns `fallback_required=true`;
- existing Telegram router/parser handles order flow;
- adapter must not replace parser in order mode;
- no generic English clarification for dimensions.

Investigation report:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_FAILURE_INVESTIGATION.md
```

Next safe Codex batch:

```text
BATCH_PHASE2_ADAPTER_ORDER_LIKE_FALLBACK_FIX_PLAN
```

No-touch: no server/SSH/service/feature flag/Phase 2 runtime, no secrets/DB/logs/orders, no `.py` changes, no git.

## 2026-06-20 — ORDER_LIKE_FALLBACK_FIX_PLAN_ONLY

Batch:

```text
BATCH_PHASE2_ADAPTER_ORDER_LIKE_FALLBACK_FIX
```

Status:

```text
ORDER_LIKE_FALLBACK_FIX_PLAN_ONLY
```

Reason:

Safe local copies of the real adapter boundary files were not found:

```text
malyarka_core/adapters/telegram.py
malyarka_core/adapters/hermes_adapter.py
```

Only markdown draft/report mentions and local test doubles were available. Because server/SSH/service/feature flag/Phase 2 runtime were forbidden, no `.py` fix was applied.

Created/updated:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_FIX_REPORT.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_FAILURE_INVESTIGATION.md
```

Next safe batch:

```text
BATCH_PHASE2_FETCH_OR_CREATE_LOCAL_ADAPTER_BOUNDARY_COPY_AND_TEST_PLAN
```

No-touch: server, SSH, service, feature flag, Phase 2, production, secrets, DB/logs/orders, real adapter code, Telegram live test and git were not touched.

## 2026-06-20 — ADAPTER_BOUNDARY_SNAPSHOT_READY

Batch:

```text
BATCH_PHASE2_FETCH_LOCAL_ADAPTER_BOUNDARY_COPY_AND_TEST_PLAN
```

Status:

```text
ADAPTER_BOUNDARY_SNAPSHOT_READY
```

Copied read-only from server:

```text
/opt/malyarka-telegram-bot/malyarka_core/adapters/telegram.py
/opt/malyarka-telegram-bot/malyarka_core/adapters/hermes_adapter.py
```

Saved locally as non-live snapshot:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_snapshot\telegram.py
E:\Hermes-Hub\server_staging\adapter_boundary_snapshot\hermes_adapter.py
E:\Hermes-Hub\server_staging\adapter_boundary_snapshot\SNAPSHOT_MANIFEST.md
```

Created plans:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LOCAL_FIX_PLAN.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_CONTRACT_TEST_PLAN.md
```

Next safe batch:

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_LOCAL_FIX_AND_TESTS
```

No-touch: server files were not modified; service/systemctl/feature flag/Phase 2/production were not touched; secrets/DB/logs/orders were not read; live Telegram test and git were not used.

## 2026-06-20 — ORDER_LIKE_FALLBACK_FIX_CANDIDATE_TESTS_PASSED

Batch:

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_LOCAL_FIX_AND_TESTS
```

Status:

```text
ORDER_LIKE_FALLBACK_FIX_CANDIDATE_TESTS_PASSED
```

Created fix-candidate:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_fix_candidate\telegram.py
E:\Hermes-Hub\server_staging\adapter_boundary_fix_candidate\hermes_adapter.py
```

Changed locally only:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_fix_candidate\hermes_adapter.py
```

Created tests:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_tests\test_order_like_fallback.py
```

Checks:

```text
python -m pytest server_staging\adapter_boundary_tests -q -> 10 passed
python -m py_compile fix-candidate files -> exit 0
```

Report:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LOCAL_FIX_AND_TESTS_REPORT.md
```

Next safe batch:

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_LIVE_PATCH_PLAN
```

No-touch: server, SSH, service, live feature flag, Phase 2, production, secrets, DB/logs/orders, live server files, live Telegram test and git were not touched.

## 2026-06-20 — ORDER_LIKE_FALLBACK_LIVE_PATCH_PLAN_READY

Batch:

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_LIVE_PATCH_PLAN
```

Status:

```text
ORDER_LIKE_FALLBACK_LIVE_PATCH_PLAN_READY
```

Created plan docs:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LIVE_PATCH_PLAN.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LIVE_PATCH_ROLLBACK_PLAN.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LIVE_PATCH_PRECHECK.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LIVE_PATCH_TEST_PLAN.md
```

Diff summary:

- `hermes_adapter.py` only.
- Added `re` import.
- Added order-like regex guard.
- `700 x 500` / `700х500` / `700 × 500` / `700*500` / `700 x 500 x 2` fallback to old Malyarka flow.
- `/start` falls back to existing router/menu flow.
- Safe generic text remains allowed.

Future approval phrase:

```text
APPROVE_ORDER_LIKE_FALLBACK_LIVE_PATCH_ONCE
```

Next live patch batch after approval:

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_APPLY_LIVE_PATCH_ONCE
```

No-touch: server/SSH/systemctl/live files/feature flag/Phase 2/production/secrets/DB/logs/orders/live Telegram/git were not touched.

## 2026-06-20 — ORDER_LIKE_FALLBACK_LIVE_PATCH_APPLIED_SANITY_PASSED

Batch:

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_APPLY_LIVE_PATCH_ONCE
```

Status:

```text
ORDER_LIKE_FALLBACK_LIVE_PATCH_APPLIED_SANITY_PASSED
```

Applied live patch:

```text
/opt/malyarka-telegram-bot/malyarka_core/adapters/hermes_adapter.py
```

Backup:

```text
/opt/malyarka-telegram-bot/malyarka_core/adapters/hermes_adapter.py.20260620_021040.before_order_like_fallback_patch
```

Final verified state:

```text
service: active/running
autostart: disabled
feature flag: OFF
production: OFF
Phase 2: OFF
patch guard: present
```

Sanity Telegram test:

- `/start` and `700 x 500` reported normal by user.
- Previous English clarification did not recur in reported sanity result.
- User noted: Malyarka file does not download. This is tracked as a separate export/callback blocker, not a rollback trigger for the order-like fallback patch.

Report:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LIVE_PATCH_REPORT.md
```

Next safe batch:

```text
BATCH_MALYARKA_FILE_DOWNLOAD_READ_ONLY_INVESTIGATION
```

No-touch: feature flag was not enabled; Phase 2 was not launched; production was not enabled; `telegram.py` was not changed; secrets/DB/logs/orders were not read; git was not used.
~~~

---

## Source: progress\PROGRESS_CARD.md

~~~markdown
# Progress Card

Updated: 2026-06-12

## Where We Came From

Old Hermes-General and old Malyarka continuation became noisy and risky.

Key risks found:

- old Malyarka has unreviewed changes;
- `.env` and `orders.db` exist in old project;
- a Telegram token was previously hardcoded in `start_bot.bat`;
- some new files tried to read secrets or call external APIs;
- old status files contradicted actual disk state.

## Where We Are

Creating a clean control layer:

```text
E:\Hermes-Hub
```

Current status:

```text
ChatGPT main chat connected / batch mode + architecture plan saved
```

ChatGPT project:

```text
HERMES HUB -> Главный чат для работы
```

## Where We Go Next

1. Confirm project name.
2. Decide Nous Portal free vs $20.
3. Prepare first Codex implementation batch.
4. Build minimal clean core.
5. Later connect Hermes / Nous Portal as visual workspace.

## Estimated Time

Clean control layer:

```text
30-60 minutes
```

Clean MVP:

```text
1-2 working days / 3-5 Codex sessions
```

## User Decisions Needed

- final name;
- Nous Portal free first or $20 subscription;
- when to start code;
- when old Malyarka may be used as source.
~~~

---

## Source: tasks\NEXT_TASKS.md

~~~markdown
# Next Tasks

Date: 2026-06-20

## Current Status

- Bot: active/running, autostart disabled
- Feature flag: OFF
- Production: NOT enabled
- Phase 2: NOT started
- Server gates 1-9: completed
- SSH/Phase 2 access: requires separate verification

## Routing

| Р—РѕРЅР° | РљРѕРјСѓ |
|------|------|
| Micro checks, read-only | Hermes / DeepSeek |
| Code, tests, multi-file | Codex (batch, 5-10 РїСѓРЅРєС‚РѕРІ) |
| Decisions | РџРѕР»СЊР·РѕРІР°С‚РµР»СЊ + ChatGPT |
| Prompt workflow | РўРµРєСЃС‚ РІ ChatGPT в†’ РєРѕРїРёСЏ РІ Codex/Hermes |

## Next Steps

1. Markdown cleanup вЂ” done вњ…
2. Phase 2 dry-run prep вЂ” requires separate user decision
3. Server SSH diagnostic вЂ” if Phase 2 is chosen

## 2026-06-20 вЂ” BATCH_PHASE2_PREP_SSH_VERIFY_ROLLBACK

Status:

```text
PHASE2_DRY_RUN_PREP_READY_SSH_VERIFIED
```

Current verified state:

```text
server: hermes / 178.104.95.187
service: malyarka-telegram-bot.service
service state: active/running
autostart: disabled
process: /opt/malyarka-telegram-bot/.venv/bin/python -m malyarka_telegram.app --run-polling
Hermes adapter: installed
feature flag: _HERMES_ADAPTER_ENABLED = False
Telegram test: passed
production: OFF
Phase 2: OFF
SSH: verified read-only
```

Created/updated plan-only docs:

```text
E:\Hermes-Hub\docs\SERVER_SSH_ACCESS_CURRENT_STATUS.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_DRY_RUN_PREP_AND_APPROVAL.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_PRECHECK_CHECKLIST.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_COMMAND_PLAN_ONLY.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_TELEGRAM_TEST_PLAN.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_ROLLBACK_PLAN.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_REPORT_TEMPLATE.md
```

Approval phrase for any future Phase 2 dry-run:

```text
APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE
```

Routing remains active:

- Codex is not used for micro tasks.
- Hermes / DeepSeek handles safe micro checks.
- Codex is reserved for complex/risky batch work.

No-touch: Phase 2 was not launched; feature flag was not changed; production remains OFF; no service start/restart/stop/enable/disable was performed; `.env`, `config.py`, token, `os.environ`, DB, live logs and real orders were not read; `.py` code was not changed; git was not used.


## 2026-06-20 — PHASE2_DRY_RUN_FAILED_ROLLBACK_DONE

Status:

```text
PHASE2_DRY_RUN_FAILED_ROLLBACK_DONE
```

Summary:

- Phase 2 dry-run was explicitly approved with `APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE`.
- Precheck passed: SSH verified, service active/running, autostart disabled, feature flag OFF, adapter/hook present.
- Backup created: `/opt/malyarka-telegram-bot/malyarka_core/adapters/telegram.py.phase2_dry_run_backup_20260620`.
- Feature flag was temporarily set ON for controlled dry-run.
- Controlled restart was performed to apply temporary flag.
- Telegram test failed: `700 x 500` was diverted to English clarification (`What is 700 x 500 for?`) instead of expected Malyarka order flow.
- Rollback was executed immediately.
- Feature flag is now OFF.
- Controlled restart was performed to apply rollback.
- Final service state: active/running.
- Autostart remains disabled.
- Production remains OFF.

Created report:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_DRY_RUN_REPORT.md
```

Blocker:

```text
Hermes adapter currently interferes incorrectly with simple order-like input `700 x 500`.
```

Next safe step:

```text
Plan-only investigation of adapter dry-run behavior before any future flag enable.
```

No-touch: no production enable, no systemctl enable/stop, no autostart change, no `.env`, `config.py`, token, `os.environ`, DB, live logs or real orders read, no adapter logic change, no git.

## 2026-06-20 — PHASE2_FAILURE_INVESTIGATION_READY

Status:

```text
PHASE2_FAILURE_INVESTIGATION_READY
```

Source failure:

```text
PHASE2_DRY_RUN_FAILED_ROLLBACK_DONE
```

Finding:

`700 x 500` is order-like production-size input and must remain under Malyarka order flow. During Phase 2 dry-run the Hermes adapter diverted it to generic English clarification (`What is 700 x 500 for?`), so Phase 2 remains blocked.

Likely failure point:

```text
malyarka_core/adapters/telegram.py / malyarka_core/adapters/hermes_adapter.py boundary
```

Expected rule:

- order-like input -> adapter returns `fallback_required=true`;
- existing Telegram router/parser handles order flow;
- adapter must not replace parser in order mode;
- no generic English clarification for dimensions.

Investigation report:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_FAILURE_INVESTIGATION.md
```

Next safe Codex batch:

```text
BATCH_PHASE2_ADAPTER_ORDER_LIKE_FALLBACK_FIX_PLAN
```

No-touch: no server/SSH/service/feature flag/Phase 2 runtime, no secrets/DB/logs/orders, no `.py` changes, no git.

## 2026-06-20 — ORDER_LIKE_FALLBACK_FIX_PLAN_ONLY

Batch:

```text
BATCH_PHASE2_ADAPTER_ORDER_LIKE_FALLBACK_FIX
```

Status:

```text
ORDER_LIKE_FALLBACK_FIX_PLAN_ONLY
```

Reason:

Safe local copies of the real adapter boundary files were not found:

```text
malyarka_core/adapters/telegram.py
malyarka_core/adapters/hermes_adapter.py
```

Only markdown draft/report mentions and local test doubles were available. Because server/SSH/service/feature flag/Phase 2 runtime were forbidden, no `.py` fix was applied.

Created/updated:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_FIX_REPORT.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_FAILURE_INVESTIGATION.md
```

Next safe batch:

```text
BATCH_PHASE2_FETCH_OR_CREATE_LOCAL_ADAPTER_BOUNDARY_COPY_AND_TEST_PLAN
```

No-touch: server, SSH, service, feature flag, Phase 2, production, secrets, DB/logs/orders, real adapter code, Telegram live test and git were not touched.

## 2026-06-20 — ADAPTER_BOUNDARY_SNAPSHOT_READY

Batch:

```text
BATCH_PHASE2_FETCH_LOCAL_ADAPTER_BOUNDARY_COPY_AND_TEST_PLAN
```

Status:

```text
ADAPTER_BOUNDARY_SNAPSHOT_READY
```

Copied read-only from server:

```text
/opt/malyarka-telegram-bot/malyarka_core/adapters/telegram.py
/opt/malyarka-telegram-bot/malyarka_core/adapters/hermes_adapter.py
```

Saved locally as non-live snapshot:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_snapshot\telegram.py
E:\Hermes-Hub\server_staging\adapter_boundary_snapshot\hermes_adapter.py
E:\Hermes-Hub\server_staging\adapter_boundary_snapshot\SNAPSHOT_MANIFEST.md
```

Created plans:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LOCAL_FIX_PLAN.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_CONTRACT_TEST_PLAN.md
```

Next safe batch:

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_LOCAL_FIX_AND_TESTS
```

No-touch: server files were not modified; service/systemctl/feature flag/Phase 2/production were not touched; secrets/DB/logs/orders were not read; live Telegram test and git were not used.

## 2026-06-20 — ORDER_LIKE_FALLBACK_FIX_CANDIDATE_TESTS_PASSED

Batch:

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_LOCAL_FIX_AND_TESTS
```

Status:

```text
ORDER_LIKE_FALLBACK_FIX_CANDIDATE_TESTS_PASSED
```

Created fix-candidate:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_fix_candidate\telegram.py
E:\Hermes-Hub\server_staging\adapter_boundary_fix_candidate\hermes_adapter.py
```

Changed locally only:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_fix_candidate\hermes_adapter.py
```

Created tests:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_tests\test_order_like_fallback.py
```

Checks:

```text
python -m pytest server_staging\adapter_boundary_tests -q -> 10 passed
python -m py_compile fix-candidate files -> exit 0
```

Report:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LOCAL_FIX_AND_TESTS_REPORT.md
```

Next safe batch:

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_LIVE_PATCH_PLAN
```

No-touch: server, SSH, service, live feature flag, Phase 2, production, secrets, DB/logs/orders, live server files, live Telegram test and git were not touched.

## 2026-06-20 — ORDER_LIKE_FALLBACK_LIVE_PATCH_PLAN_READY

Batch:

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_LIVE_PATCH_PLAN
```

Status:

```text
ORDER_LIKE_FALLBACK_LIVE_PATCH_PLAN_READY
```

Created plan docs:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LIVE_PATCH_PLAN.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LIVE_PATCH_ROLLBACK_PLAN.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LIVE_PATCH_PRECHECK.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LIVE_PATCH_TEST_PLAN.md
```

Diff summary:

- `hermes_adapter.py` only.
- Added `re` import.
- Added order-like regex guard.
- `700 x 500` / `700х500` / `700 × 500` / `700*500` / `700 x 500 x 2` fallback to old Malyarka flow.
- `/start` falls back to existing router/menu flow.
- Safe generic text remains allowed.

Future approval phrase:

```text
APPROVE_ORDER_LIKE_FALLBACK_LIVE_PATCH_ONCE
```

Next live patch batch after approval:

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_APPLY_LIVE_PATCH_ONCE
```

No-touch: server/SSH/systemctl/live files/feature flag/Phase 2/production/secrets/DB/logs/orders/live Telegram/git were not touched.

## 2026-06-20 — ORDER_LIKE_FALLBACK_LIVE_PATCH_APPLIED_SANITY_PASSED

Batch:

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_APPLY_LIVE_PATCH_ONCE
```

Status:

```text
ORDER_LIKE_FALLBACK_LIVE_PATCH_APPLIED_SANITY_PASSED
```

Applied live patch:

```text
/opt/malyarka-telegram-bot/malyarka_core/adapters/hermes_adapter.py
```

Backup:

```text
/opt/malyarka-telegram-bot/malyarka_core/adapters/hermes_adapter.py.20260620_021040.before_order_like_fallback_patch
```

Final verified state:

```text
service: active/running
autostart: disabled
feature flag: OFF
production: OFF
Phase 2: OFF
patch guard: present
```

Sanity Telegram test:

- `/start` and `700 x 500` reported normal by user.
- Previous English clarification did not recur in reported sanity result.
- User noted: Malyarka file does not download. This is tracked as a separate export/callback blocker, not a rollback trigger for the order-like fallback patch.

Report:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LIVE_PATCH_REPORT.md
```

Next safe batch:

```text
BATCH_MALYARKA_FILE_DOWNLOAD_READ_ONLY_INVESTIGATION
```

No-touch: feature flag was not enabled; Phase 2 was not launched; production was not enabled; `telegram.py` was not changed; secrets/DB/logs/orders were not read; git was not used.
~~~

---

## Source: decisions\DECISIONS.md

~~~markdown
# Decisions

## Accepted

- Start a clean new project instead of fixing the messy old continuation.
- Use old Malyarka only as an archive/source after review.
- Build a shared state system for ChatGPT, Codex and Hermes.
- Add Project Hints so useful agreements are not forgotten.
- Add cleanup rules before writing real application code.
- Use ChatGPT project `HERMES HUB` and chat `Главный чат для работы` as the main planning chat.
- Use batch workflow for normal work so ChatGPT and Codex exchange larger blocks instead of many tiny steps.
- Accept high-level Malyarka Clean architecture flow: text order -> parse sizes -> disputed rows -> area -> Corel export -> tests.

## Proposed

- Working project name: Hermes Hub / Malyarka Clean.
- Use Nous Portal free first, then consider $20 subscription if it is useful.

## Not Accepted Yet

- Final project name.
- Real Telegram launch.
- Vision/API integration.
- Database design.
- CNC/ArtCam automation.

## Forbidden For Now

- Use old Malyarka as active system.
- Store tokens in scripts or docs.
- Start Telegram.
- Read `.env` or `orders.db`.
- Call external APIs.
~~~

---

## Source: PROJECT_HINTS.md

~~~markdown
# Project Hints

Use these hints to make work easier and avoid repeating old mistakes.

## Active Hints

1. Always give the user a full Win+R path when sending them to a folder or file.
2. Keep old Malyarka frozen; build clean in Hermes Hub.
3. Use one source of truth: `HERMES_HUB_STATE.md`.
4. For big work, first make a task packet, then implement.
5. After every meaningful step, update state, worklog and next tasks.
6. Experiments go to `_scratch`, suspicious files go to `_quarantine`, old material goes to `_archive`.
7. Do not trust chat history as memory. Trust files.
8. Before risky actions, say what is risky and wait for explicit permission.
9. Show the user a short progress card regularly.
10. Do not accept agent output as working until it is checked.

## How To Add A Hint

User command:

```text
сохрани подсказку: ...
```

Agent should propose the exact text and ask for confirmation before adding.

~~~

---

## Source: SAFETY_RULES.md

~~~markdown
# Safety Rules

## Default Rule

When uncertain, do less and ask for explicit permission.

## Safe By Default

Inside `E:\Hermes-Hub` it is safe to:

- create planning files;
- create docs;
- create empty project scaffolds;
- write logs;
- write task packets;
- write progress cards;
- write cleanup rules.

## Not Safe Without Separate Permission

Do not read, modify, run or expose:

```text
.env
orders.db
.git
tokens
keys
passwords
Telegram bot launch
Vision/photo API
external APIs
old bot.py
```

Do not touch old folders without separate permission:

```text
C:\Users\user\Desktop\malyarka_codex_work
C:\Users\user\Desktop\malyarka_memory_cleanup
```

## API Rule

No real API calls unless the user says exactly which API may be called.

## Telegram Rule

No polling, no bot launch, no token handling until a dedicated Telegram phase.

## Secret Rule

Never paste, print, copy into docs, or store secrets in `.bat`, `.md`, `.py`, logs or chat.

~~~

---

## Source: docs\CHATGPT_CHAT_ROLES.md

~~~markdown
# ChatGPT Chat Roles

Updated: 2026-06-12

This file explains how to use the ChatGPT project `HERMES HUB`.

## Main Rule

The user should not keep the workflow in memory.

ChatGPT, Codex and future Hermes / Nous Portal must use the same project files:

```text
E:\Hermes-Hub\HERMES_HUB_STATE.md
E:\Hermes-Hub\progress\PROGRESS_CARD.md
E:\Hermes-Hub\tasks\NEXT_TASKS.md
E:\Hermes-Hub\logs\WORKLOG.md
```

## ChatGPT Project

Project name in ChatGPT:

```text
HERMES HUB
```

## Chats

| Chat | Purpose |
|---|---|
| Главный чат для работы | Main control chat. Decisions, progress cards, next steps, task packets for Codex. |
| Инженер проекта Hermes Hub | Review chat. Architecture criticism, risks, checks, alternative plans. |
| Рабочий чат 0.0.1 | Drafts and temporary experiments. Nothing becomes official until moved to the state files. |
| Архив-перенос чат | Old-context transfer and archive review. Old Malyarka stays archive-only. |

## How To Work In The Main Chat

Use `Главный чат для работы` for normal project work.

ChatGPT should regularly show:

```text
Откуда пришли:
Где сейчас:
Куда идем:
Сколько примерно времени:
Что нужно решить:
```

If ChatGPT wants Codex to do work, it must prepare:

```text
TASK:
CONTEXT:
WHAT TO DO:
WHAT NOT TO TOUCH:
EXPECTED RESULT:
CHECKS:
FILES TO UPDATE:
```

## What Counts As Official

A decision is official only when it is written to one of these files:

```text
E:\Hermes-Hub\HERMES_HUB_STATE.md
E:\Hermes-Hub\decisions\DECISIONS.md
E:\Hermes-Hub\tasks\NEXT_TASKS.md
```

Chat messages alone are not enough.

## Safety

Do not touch without separate explicit permission:

```text
C:\Users\user\Desktop\malyarka_codex_work
C:\Users\user\Desktop\malyarka_memory_cleanup
.env
orders.db
.git
tokens
keys
passwords
Telegram launch
Vision
external APIs
old bot.py
```

~~~

---

## Source: docs\BATCH_WORKFLOW.md

~~~markdown
# Batch Workflow

Updated: 2026-06-12

This file defines how ChatGPT, Codex and future Hermes should work without
micro-copying every small step.

## Main Idea

Work in batches.

One batch should contain enough context for Codex to work for a while without
asking the user to paste every small answer back and forth.

## Roles

| Role | Does |
|---|---|
| ChatGPT | Discusses with user, groups decisions, prepares `BATCH_PACKET`. |
| Codex | Executes safe parts of the batch, verifies, updates project files, reports one summary. |
| Hermes / Nous Portal | Later becomes the visual workspace that reads the same state files. |
| User | Confirms risky steps and final decisions. |

## Batch Size

A normal batch should include:

- 1 clear goal;
- 3-7 related tasks;
- safety limits;
- expected outputs;
- checks;
- files to update;
- user decisions that are still open.

Avoid batches that mix unrelated work, for example:

- architecture + Telegram launch + Vision + database migration;
- old Malyarka audit + production bot launch;
- UI design + real API calls.

## Batch Packet Format

```text
BATCH_PACKET:

GOAL:

CURRENT CONTEXT:

ACCEPTED DECISIONS:

TASKS:
1.
2.
3.

WHAT CODEX MAY DO WITHOUT ASKING:

WHAT CODEX MUST NOT TOUCH:

WHAT NEEDS USER CONFIRMATION:

EXPECTED RESULT:

CHECKS:

FILES TO UPDATE:

REPORT BACK TO CHATGPT:
```

## Large Batch Files

Large `BATCH_PACKET` texts should be stored as separate `.md` files in:

```text
E:\Hermes-Hub\handoff
```

Do not paste huge packet text into ChatGPT when a file can hold it.

In chat, paste only a short command with a file reference, for example:

```text
Прочитай файл E:\Hermes-Hub\handoff\BATCH_001_HERMES_CONTEXT_HANDOFF.md как BATCH_PACKET. Если ты не видишь файл, попроси меня загрузить или вставить его.
```

Recommended naming:

```text
BATCH_001_TOPIC_NAME.md
BATCH_002_TOPIC_NAME.md
BATCH_003_TOPIC_NAME.md
```

## Simple Handoff Files

For everyday work, use fixed handoff files:

```text
E:\Hermes-Hub\handoff\ACTIVE_BATCH.md
E:\Hermes-Hub\handoff\REPORT_TO_CHATGPT.md
E:\Hermes-Hub\handoff\CHATGPT_CONTEXT_BUNDLE.md
```

Meaning:

- `ACTIVE_BATCH.md` stores the current active package for Codex.
- `REPORT_TO_CHATGPT.md` stores the short Codex report that the user can paste back into ChatGPT.
- `CHATGPT_CONTEXT_BUNDLE.md` stores the portable context snapshot for ChatGPT.

Rule:

ChatGPT should not give long commands in chat. It should point to the active
package file.

Codex should write its short report into `REPORT_TO_CHATGPT.md` after executing
a meaningful package.

Short execution command:

```text
Выполни ACTIVE_BATCH
```

Standing Codex rules live here:

```text
E:\Hermes-Hub\AGENTS.md
```

Codex should use `AGENTS.md` as the durable project instruction file for the
one-command workflow.

When this command is used, Codex should:

1. read `E:\Hermes-Hub\handoff\ACTIVE_BATCH.md`;
2. find the current active package;
3. execute only the safe allowed parts;
4. write the user-facing report to `E:\Hermes-Hub\handoff\REPORT_TO_CHATGPT.md`;
5. refresh `E:\Hermes-Hub\handoff\CHATGPT_CONTEXT_BUNDLE.md`.

## Codex Execution Rule

Codex may complete all safe tasks in the batch without stopping after each
micro-step.

Codex must stop and ask only if:

- the batch asks to read or modify secrets;
- the batch asks to touch old Malyarka as an active system;
- there is a real risk of deleting or overwriting data;
- a required user decision is missing;
- a command would launch Telegram, Vision, external APIs or production services.

## End Of Batch Report

Codex should return one compact report:

```text
DONE:
CHANGED FILES:
CHECKS:
NOT DONE:
NEXT BATCH:
COPY TO CHATGPT:
```

## Context Bundle Update Rule

After each meaningful batch, Codex should update the portable ChatGPT bundle:

```text
E:\Hermes-Hub\tools\Update-ChatGPTContextBundle.ps1
```

Output file:

```text
E:\Hermes-Hub\handoff\CHATGPT_CONTEXT_BUNDLE.md
```

This keeps ChatGPT synchronized even though ChatGPT cannot read local files by
itself.

## State Patch Rule

After each meaningful batch, Codex should prepare/update:

```text
E:\Hermes-Hub\patches\LATEST_STATE_PATCH.md
```

Patch log:

```text
E:\Hermes-Hub\patches\PATCH_LOG.md
```

The patch is a short acceptance/review summary for ChatGPT.

It must include:

- what was accepted;
- what changed;
- what was not accepted;
- what is forbidden;
- touched files;
- untouched areas;
- next step.

The patch does not replace:

```text
E:\Hermes-Hub\HERMES_HUB_STATE.md
E:\Hermes-Hub\handoff\CHATGPT_CONTEXT_BUNDLE.md
E:\Hermes-Hub\handoff\REPORT_TO_CHATGPT.md
```

## Rule For ChatGPT

ChatGPT should not send Codex one tiny task at a time.

If the next work is not risky, ChatGPT should prepare a batch with several
safe related tasks.
~~~

---

## Source: docs\MALYARKA_CLEAN_CORE_CONTRACTS.md

~~~markdown
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
~~~

---

## Source: docs\MALYARKA_CLEAN_PARSER_RULES.md

~~~markdown
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
~~~

---

## Source: docs\MALYARKA_CLEAN_AREA_RULES.md

~~~markdown
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
~~~

---

## Source: docs\MALYARKA_CLEAN_ORDER_RESULT_RULES.md

~~~markdown
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
~~~

---

## Source: docs\MALYARKA_CLEAN_COREL_MODEL_RULES.md

~~~markdown
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
~~~

---

## Source: docs\MALYARKA_CLEAN_COREL_IMPLEMENTATION_PLAN.md

~~~markdown
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
~~~

---

## Source: docs\MALYARKA_CLEAN_PIPELINE_SMOKE_TEST_PLAN.md

~~~markdown
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
~~~

---

## Source: docs\MALYARKA_CLEAN_USAGE_GUIDE_PLAN.md

~~~markdown
# План русской инструкции по использованию Malyarka Clean

Пакет:

```text
BATCH_021_README_AND_USAGE_GUIDE_PLANNING
```

Статус:

```text
только планирование
```

Этот документ описывает, какую русскую инструкцию нужно будет создать для минимального ядра Malyarka Clean.

Рабочий файл будущей инструкции:

```text
E:\Hermes-Hub\README_КАК_ПОЛЬЗОВАТЬСЯ.md
```

## 1. Что уже умеет минимальное ядро

Минимальное ядро уже умеет:

- принимать текст заказа;
- разбирать размеры;
- отделять подтверждённые строки от спорных;
- считать площадь подтверждённых строк;
- формировать итоговый результат заказа;
- готовить нейтральные Corel-строки;
- блокировать Corel-строки при спорных или пустых заказах.

## 2. Какие форматы размеров сейчас поддерживаются

```text
1000 400
1000 400 2
1000x400
1000 x 400
1000*400
1000×400
```

Правило:

```text
первое число = высота
второе число = ширина
третье число = количество
если количество не указано, количество = 1
```

## 3. Какие статусы бывают

| Статус | Значение |
|---|---|
| `clean` | Чистый заказ. |
| `has_disputes` | Есть спорные строки. |
| `empty_or_invalid` | Пустой или непонятный заказ. |

## 4. Что считается спорным

Спорным считается:

- не хватает высоты;
- не хватает ширины;
- слишком много чисел;
- количество непонятно;
- строка не похожа на размер;
- текст нельзя безопасно разобрать.

Главное правило:

```text
Спорное не додумывать.
```

## 5. Как считается площадь

Формула:

```text
area_m2 = height_mm * width_mm * quantity / 1_000_000
```

Площадь считается только по подтверждённым строкам.

Спорные строки в площадь не входят.

## 6. Когда Corel-строки готовы

Corel-строки готовы, если:

```text
status = clean
disputed_rows пустой
export_blocked = false
```

Corel-строки сейчас являются только внутренними данными.

Это не Corel-файл.

## 7. Когда Corel-строки заблокированы

Corel-строки заблокированы, если:

- есть спорные строки;
- `status = has_disputes`;
- `status = empty_or_invalid`;
- `export_blocked = true`.

## 8. Что ещё НЕ реализовано

```text
Excel-файл
реальный Corel export
Telegram
Vision
API
база данных
цены
стоимость
ЛКМ
материалы
производство
CNC-обучение
```

## 9. Какую реальную инструкцию нужно будет создать

Будущая инструкция должна быть здесь:

```text
E:\Hermes-Hub\README_КАК_ПОЛЬЗОВАТЬСЯ.md
```

Она должна быть написана простыми словами для пользователя, не как техническая документация.

## 10. Разделы будущей инструкции

В будущей инструкции должны быть разделы:

1. Что это такое.
2. Что уже работает.
3. Как выглядит входной текст.
4. Какие есть примеры.
5. Что делать со спорными строками.
6. Что значит площадь.
7. Что значит Corel-модель.
8. Что ещё не готово.
9. Куда смотреть пользователю.
10. Что будет следующим этапом.

## 11. Граница пакета

В этом пакете не создаётся сама инструкция `README_КАК_ПОЛЬЗОВАТЬСЯ.md`.

В этом пакете создаётся только план будущей инструкции.

Код, тесты, приложение, Excel/Corel export и внешние сервисы не трогаются.
~~~

---

## Source: docs\MALYARKA_CLEAN_MANUAL_CORE_CHECK_PLAN.md

~~~markdown
# План простой ручной проверки ядра Malyarka Clean

Пакет:

```text
BATCH_023_MANUAL_CORE_CHECK_PLANNING
```

Статус:

```text
только планирование
```

Этот документ описывает будущую простую ручную проверку минимального ядра Malyarka Clean на понятных примерах заказа.

Код, тесты, приложение, Telegram, Vision, API, база данных и Excel/Corel export в этом пакете не трогаются.

## 1. Зачем нужна ручная проверка

Ручная проверка нужна, чтобы:

- убедиться, что пользователь понимает, что уже работает;
- проверить ядро на простых текстовых заказах;
- увидеть ожидаемый результат простыми словами;
- не переходить к Telegram, Vision, API и Excel раньше времени.

## 2. Какие примеры проверить вручную

Нужно проверить три типа заказов:

```text
чистый заказ
заказ со спорной строкой
пустой или мусорный заказ
```

## 3. Пример чистого заказа

Входной текст:

```text
1000 400 2
700 300
```

Ожидается:

```text
status = clean
disputed_rows пустой
total_area_m2 посчитан
corel_rows готовы
export_blocked = false
```

Пояснение:

- обе строки понятны;
- спорных строк нет;
- площадь считается по обеим строкам;
- нейтральные Corel-строки можно подготовить.

## 4. Пример заказа со спорной строкой

Входной текст:

```text
1000 400 2
мусор
700 300
```

Ожидается:

```text
status = has_disputes
disputed_rows не пустой
площадь считается только по подтверждённым строкам
corel_rows заблокированы
export_blocked = true
```

Пояснение:

- понятные строки можно использовать для расчёта площади;
- строка `мусор` должна попасть в спорные;
- Corel-строки не готовы, пока спор не разобран.

## 5. Пример пустого или мусорного заказа

Входной текст:

```text
привет
ничего непонятно
```

Ожидается:

```text
status = empty_or_invalid
total_area_m2 = 0
corel_rows заблокированы
export_blocked = true
```

Пояснение:

- в заказе нет безопасных размеров;
- площадь равна 0;
- Corel-строки не готовятся.

## 6. Что НЕ входит

В ручную проверку не входит:

```text
Telegram
Vision
API
база данных
Excel-файл
Corel-файл
экспорт на диск
цены
стоимость
ЛКМ
материалы
производство
```

## 7. Следующий пакет после плана

Следующий пакет:

```text
Пакет 024 — Реализация простой ручной проверки ядра
BATCH_024_MANUAL_CORE_CHECK_IMPLEMENTATION
```

Он должен быть техническим и потребует отдельного разрешения, если нужно создавать скрипт, тест или команду для ручной проверки.
~~~

---

## Source: docs\MALYARKA_CLEAN_EMPTY_INVALID_STATUS_FIX_PLAN.md

~~~markdown
# План исправления статуса пустого/мусорного заказа

Пакет:

```text
BATCH_025_EMPTY_INVALID_STATUS_FIX_PLANNING
```

Статус:

```text
только планирование
```

Этот документ фиксирует найденное ручной проверкой расхождение в статусах минимального ядра Malyarka Clean.

Код, функции, классы, тесты, приложение, Telegram, Vision, API, база данных и Excel/Corel export в этом пакете не создаются.

## 1. В чём найденное расхождение

В пакете 024 ручной скрипт `manual_core_check.py` проверил три примера:

```text
чистый заказ
заказ со спорной строкой
пустой/мусорный заказ
```

Для пустого/мусорного заказа текущее ядро вернуло:

```text
status = has_disputes
```

Ожидание по ручному плану:

```text
status = empty_or_invalid
```

## 2. Какой статус сейчас возвращается

Сейчас полностью мусорный текст вроде:

```text
привет
ничего непонятно
```

разбирается как набор спорных строк, поэтому итоговый результат становится:

```text
status = has_disputes
confirmed_rows = 0
disputed_rows > 0
total_area_m2 = 0
export_blocked = true
```

## 3. Какой статус должен возвращаться

Если в заказе нет подтверждённых строк и нет безопасно распознанных строк заказа, результат должен быть:

```text
status = empty_or_invalid
confirmed_rows = 0
total_area_m2 = 0
export_blocked = true
```

Полностью мусорный текст не должен считаться обычным спорным заказом.

## 4. Разница между типами проблем

### Заказ со спорной строкой

Пример:

```text
1000 400 2
мусор
700 300
```

Ожидается:

```text
status = has_disputes
confirmed_rows > 0
disputed_rows > 0
```

Почему:

- в заказе есть хотя бы одна подтверждённая строка;
- есть строка, которую нужно уточнить;
- площадь можно считать только по подтверждённым строкам;
- экспорт остаётся заблокированным до уточнения спора.

### Полностью пустой заказ

Пример:

```text

```

Ожидается:

```text
status = empty_or_invalid
confirmed_rows = 0
disputed_rows = 0 или только служебная причина пустоты
```

Почему:

- пользователь не дал ни одной рабочей строки заказа;
- уточнять нечего, нужно попросить нормальный текст заказа.

### Полностью мусорный заказ

Пример:

```text
привет
ничего непонятно
```

Ожидается:

```text
status = empty_or_invalid
confirmed_rows = 0
total_area_m2 = 0
export_blocked = true
```

Почему:

- нет ни одной подтверждённой строки;
- нет строки, похожей на безопасный размер;
- это не частично спорный заказ, а непригодный ввод.

## 5. Где вероятно исправлять логику

Следующий технический пакет должен проверить и при необходимости изменить:

```text
order_result
dispute_detector
related focused tests
manual_core_check
```

Вероятный смысл изменения:

- если `confirmed_rows` пустой;
- и все спорные строки имеют причины мусора/неразобранного текста;
- и нет строк, похожих на частичный размер;
- тогда итоговый статус должен быть `empty_or_invalid`, а не `has_disputes`.

При этом нельзя ломать правило:

```text
confirmed_rows > 0 + disputed_rows > 0 => has_disputes
```

## 6. Какие focused tests нужны после исправления

После реализации исправления нужны focused tests:

```text
пустая строка -> empty_or_invalid
полностью мусорный текст -> empty_or_invalid
чистый заказ -> clean
заказ с подтверждённой строкой и мусором -> has_disputes
Corel-модель блокируется для empty_or_invalid
```

Дополнительно полезно проверить:

```text
manual_core_check.py показывает empty_or_invalid для пустого/мусорного примера
```

## 7. Что НЕ входит

В этот пакет не входит:

```text
Telegram
Vision
API
база данных
Excel/Corel export
цены
стоимость
ЛКМ
материалы
старая Малярка
```

## 8. Следующий пакет

Следующий пакет должен быть техническим и выполняться только с разрешения пользователя:

```text
Пакет 026 — Исправление статуса пустого/мусорного заказа
BATCH_026_EMPTY_INVALID_STATUS_FIX_IMPLEMENTATION
```
~~~

---

## Source: docs\MALYARKA_CLEAN_USER_ENTRY_PLAN.md

~~~markdown
# План удобного пользовательского ввода Malyarka Clean

Пакет:

```text
BATCH_027_MANUAL_CHECK_ACCEPTANCE_OR_USER_ENTRY_PLANNING
```

Статус:

```text
только планирование
```

Этот документ фиксирует приёмку ручной проверки минимального ядра Malyarka Clean и описывает следующий удобный способ ввода заказа.

Код, функции, классы, тесты, приложение, Telegram, Vision, API, база данных и Excel/Corel export в этом пакете не создаются.

## 1. Ручная проверка считается принятой

После пакета 026 минимальная цепочка считается рабочей на базовом уровне:

```text
текст заказа
-> разбор строк
-> подтверждённые строки
-> спорные строки
-> расчёт площади
-> итоговый результат
-> нейтральная Corel-модель
```

Принятые результаты:

```text
чистый заказ -> status = clean
заказ со спорной строкой -> status = has_disputes
пустой/мусорный заказ -> status = empty_or_invalid
```

Что это значит:

- минимальная цепочка работает;
- чистый заказ проходит;
- спорный заказ блокирует Corel-модель;
- пустой/мусорный заказ получает `empty_or_invalid`;
- ручной скрипт показывает понятный результат.

## 2. Что сейчас неудобно

Сейчас проверка всё ещё техническая:

- проверка идёт через Python-скрипт;
- для pytest нужен `PYTHONPATH`;
- пользователь не должен вручную разбираться в Python-командах;
- пользователь должен видеть простой способ: куда нажать или какую короткую команду запустить.

## 3. Какой следующий удобный ввод нужен

Следующий слой должен дать простой локальный ввод текстового заказа:

```text
без Telegram
без Vision
без API
без базы данных
без Excel/Corel export
без производства
```

Цель: пользователь вводит текст заказа и видит понятный результат.

## 4. Что должен делать будущий простой ввод

Будущий удобный ввод должен:

- принять текст заказа;
- показать `status`;
- показать подтверждённые строки;
- показать спорные строки;
- показать площадь;
- показать, готовы ли Corel-строки;
- показать причину блокировки, если есть.

Минимальный вывод должен быть понятен без чтения кода.

## 5. Варианты реализации позже

Позже можно выбрать один из вариантов:

```text
простой .cmd-файл для запуска
простой CLI-скрипт
текстовый файл с заказом на вход
интерактивный ввод в консоли
```

Рекомендуемый следующий маленький шаг:

```text
сначала сделать удобный запуск без ручного PYTHONPATH
```

## 6. Что НЕ входит

В этот план не входит:

```text
Telegram
Vision
API
база данных
Excel-файл
Corel-файл
экспорт на диск
цены
стоимость
ЛКМ
материалы
производство
```

## 7. Следующий пакет

Следующий пакет:

```text
Пакет 028 — План удобного запуска без PYTHONPATH
BATCH_028_SIMPLE_RUN_COMMAND_PLANNING
```
~~~

---

## Source: docs\MALYARKA_CLEAN_SIMPLE_RUN_PLAN.md

~~~markdown
# План удобного запуска без PYTHONPATH

Пакет:

```text
BATCH_028_SIMPLE_RUN_COMMAND_PLANNING
```

Статус:

```text
только планирование
```

Этот документ описывает, как сделать запуск проверок Malyarka Clean удобным для пользователя, чтобы не вспоминать `PYTHONPATH` и длинные Python-команды.

Код, `.cmd`-файлы, функции, классы, тесты, приложение, Telegram, Vision, API, база данных и Excel/Corel export в этом пакете не создаются.

## 1. В чём проблема

В пакете 026 первый запуск pytest без `PYTHONPATH` упал:

```text
ModuleNotFoundError: No module named 'malyarka_clean_core'
```

Причина:

```text
исходный код лежит в папке src,
а Python без дополнительной настройки не знает, где искать пакет malyarka_clean_core.
```

Повторный запуск с `PYTHONPATH` прошёл успешно:

```text
15 passed
```

Проблема для пользователя:

- неудобно помнить технические команды;
- неудобно вручную выставлять `PYTHONPATH`;
- ручная проверка должна запускаться проще;
- пользователь должен видеть короткий понятный способ запуска.

## 2. Что нужно спланировать

Нужно подготовить удобный запуск:

- focused tests;
- ручной проверки ядра;
- русской инструкции, куда нажать;
- возможно `.cmd`-файлов для Windows.

Цель:

```text
пользователь запускает одну понятную команду и видит русский результат.
```

## 3. Какие варианты рассмотреть

### Вариант 1. .cmd-файл для focused tests

Будущий файл может запускать только нужные проверки ядра и сам выставлять `PYTHONPATH`.

Плюс:

- просто запускать двойным кликом или через Win+R;
- пользователь не думает про Python-пути.

Минус:

- нужно аккуратно назвать файл и объяснить, что он делает.

### Вариант 2. .cmd-файл для ручной проверки

Будущий файл может запускать:

```text
manual_core_check.py
```

Плюс:

- пользователь видит понятный русский вывод;
- можно быстро проверить ядро после изменений.

### Вариант 3. Настройка проекта для импортов без PYTHONPATH

Можно позже рассмотреть техническую настройку проекта, чтобы `pytest` сам видел `src`.

Возможные способы:

```text
pytest.ini
pyproject.toml
editable install
```

Для текущего этапа безопаснее сначала сделать понятный `.cmd`, а не усложнять упаковку проекта.

### Вариант 4. Отдельная русская инструкция запуска

Нужна короткая инструкция:

- где лежит файл запуска;
- как его открыть;
- что должно появиться;
- что делать, если появилась ошибка.

## 4. Что должно быть удобно пользователю

Пользователь должен:

- открыть файл или выполнить одну команду;
- увидеть понятный русский результат;
- не думать про `PYTHONPATH`;
- не открывать технические Python-файлы;
- понимать, прошла проверка или нет.

## 5. Что НЕ входит

В этот план не входит:

```text
Telegram
Vision
API
база данных
Excel/Corel export
цены
стоимость
ЛКМ
материалы
производство
старая Малярка
```

## 6. Следующий пакет

Следующий пакет:

```text
Пакет 029 — Реализация удобного запуска без PYTHONPATH
BATCH_029_SIMPLE_RUN_COMMAND_IMPLEMENTATION
```

Ожидаемо он может создать:

```text
.cmd-файл для ручной проверки
.cmd-файл для focused tests
короткую русскую инструкцию запуска
```

Но только после отдельного разрешения пользователя.
~~~

---

## Source: docs\MALYARKA_CLEAN_SIMPLE_USER_ORDER_INPUT_PLAN.md

~~~markdown
# План простого пользовательского ввода заказа

Пакет:

```text
BATCH_030_SIMPLE_USER_ORDER_INPUT_PLANNING
```

Статус:

```text
только планирование
```

Этот документ описывает будущий простой локальный способ ввода пользовательского заказа в минимальное ядро Malyarka Clean.

Код, `.cmd`-файлы, функции, классы, тесты, Telegram, Vision, API, база данных и Excel/Corel export в этом пакете не создаются.

## 1. Зачем нужен простой пользовательский ввод

Простой ввод нужен, чтобы пользователь мог:

- вставить свой текст заказа;
- не редактировать Python-код;
- не запускать Telegram;
- не запускать Vision;
- не подключать API;
- не открывать Excel/Corel;
- увидеть результат ядра локально и безопасно.

Цель:

```text
ввести текст заказа -> увидеть понятный результат обработки
```

## 2. Какие варианты ввода рассмотреть

### Вариант 1. Ввод текста прямо в консоли

Пользователь запускает команду, вставляет текст заказа, завершает ввод и получает результат.

Плюсы:

- быстро;
- без файлов;
- удобно для маленьких проверок.

Минусы:

- многострочный ввод в консоли может быть неудобен.

### Вариант 2. Чтение заказа из текстового файла

Пользователь открывает пример файла, вставляет туда заказ и запускает проверку.

Плюсы:

- удобно для длинных заказов;
- можно сохранить пример;
- проще повторять проверку.

Минусы:

- нужно объяснить, какой файл открывать.

### Вариант 3. Отдельный пример файла заказа

Можно создать файл вроде:

```text
E:\Hermes-Hub\examples\order_input_example.txt
```

Пользователь меняет текст внутри файла, а запуск читает его.

### Вариант 4. Отдельный .cmd-файл запуска

Можно сделать `.cmd`, который:

- сам выставляет `PYTHONPATH`;
- запускает скрипт пользовательского ввода;
- показывает результат;
- не требует от пользователя технических команд.

## 3. Что должен показывать будущий вывод

Будущий вывод должен показывать:

- исходный текст заказа;
- `status`;
- `confirmed_rows`;
- `disputed_rows`;
- `total_area_m2`;
- `export_blocked`;
- `corel_rows`;
- причину блокировки, если есть.

Вывод должен быть простым и русским.

## 4. Какие сценарии должны быть удобны пользователю

### Чистый заказ

Пользователь вставил:

```text
1000 400 2
700 300
```

Ожидает увидеть:

```text
status = clean
площадь посчитана
Corel-строки готовы
```

### Заказ со спорной строкой

Пользователь вставил:

```text
1000 400 2
мусор
700 300
```

Ожидает увидеть:

```text
status = has_disputes
спорная строка показана
причина спора показана
Corel-строки заблокированы
```

### Мусорный ввод

Пользователь вставил:

```text
привет
ничего непонятно
```

Ожидает увидеть:

```text
status = empty_or_invalid
площадь = 0
Corel-строки заблокированы
```

## 5. Что НЕ входит

В этот план не входит:

```text
Telegram
Vision
API
база данных
Excel-файл
Corel-файл
экспорт на диск
цены
стоимость
ЛКМ
материалы
производство
старая Малярка
```

## 6. Следующий пакет

Следующий пакет:

```text
Пакет 031 — Реализация простого пользовательского ввода заказа
BATCH_031_SIMPLE_USER_ORDER_INPUT_IMPLEMENTATION
```

Ожидаемый безопасный вариант для реализации:

```text
скрипт, который читает заказ из текстового файла
пример текстового файла заказа
.cmd-файл запуска
русская инструкция
```

Только после отдельного разрешения пользователя.
~~~

---

## Source: handoff\BATCH_PACKET_TEMPLATE.md

~~~markdown
# Batch Packet Template

Use this for larger handoff from ChatGPT, Hermes or the user to Codex.

```text
BATCH_PACKET:

GOAL:

CURRENT CONTEXT:

ACCEPTED DECISIONS:

TASKS:
1.
2.
3.

WHAT CODEX MAY DO WITHOUT ASKING:

WHAT CODEX MUST NOT TOUCH:

WHAT NEEDS USER CONFIRMATION:

EXPECTED RESULT:

CHECKS:

FILES TO UPDATE:

REPORT BACK TO CHATGPT:
```

~~~

---

## Source: README_КАК_ПОЛЬЗОВАТЬСЯ.md

~~~markdown
# Как пользоваться Hermes Hub / Malyarka Clean

Это короткая русская инструкция по текущему минимальному ядру Malyarka Clean.

## Быстрый рабочий порядок

Главный способ работы сейчас такой:

1. Открыть файл заказа:

```text
E:\Hermes-Hub\ОТКРЫТЬ_ФАЙЛ_ЗАКАЗА.cmd
```

2. Вставить заказ и сохранить файл.

3. Запустить обработку заказа:

```text
E:\Hermes-Hub\ЗАПУСТИТЬ_ЗАКАЗ.cmd
```

4. Открыть последний результат:

```text
E:\Hermes-Hub\ОТКРЫТЬ_ПОСЛЕДНИЙ_РЕЗУЛЬТАТ.cmd
```

5. Если заказ получил статус `clean`, Excel для Corel лежит здесь:

```text
E:\Hermes-Hub\outputs\COREL_EXPORT.xlsx
```

Если есть спорные строки, исправь заказ в `ORDER_INPUT.txt`, сохрани файл и снова запусти `ЗАПУСТИТЬ_ЗАКАЗ.cmd`.

## 1. Что это такое

`Hermes Hub` — это общая рабочая папка проекта, где лежат планы, отчёты, правила, проверки и код.

`Malyarka Clean` — это новая чистая версия логики для обработки заказов. Она делается отдельно от старой Малярки, чтобы не тащить мусор и рискованные изменения.

Минимальное ядро обработки заказа — это первая рабочая часть Malyarka Clean. Сейчас оно умеет принять простой текст заказа, разобрать размеры, найти спорные строки, посчитать площадь и подготовить внутренние строки для будущего Corel.

## 2. Что уже работает

Уже работает:

- разбор текста заказа;
- разделение строк на подтверждённые и спорные;
- расчёт площади по подтверждённым строкам;
- итоговый результат заказа;
- нейтральные Corel-строки;
- блокировка Corel-строк, если заказ спорный или пустой.

Важно: Corel-строки сейчас являются только внутренними данными. Это не Corel-файл и не экспорт.

## 3. Какие форматы размеров поддерживаются

Сейчас поддерживаются простые форматы:

```text
1000 400
1000 400 2
1000x400
1000 x 400
1000*400
1000×400
```

Правило чтения:

```text
первое число = высота
второе число = ширина
третье число = количество
если количество не указано, количество = 1
```

Примеры:

```text
1000 400
```

Означает: высота 1000 мм, ширина 400 мм, количество 1.

```text
1000 400 2
```

Означает: высота 1000 мм, ширина 400 мм, количество 2.

## 4. Что означают статусы

| Статус | Простое значение |
|---|---|
| `clean` | Чистый заказ. Можно продолжать обработку. |
| `has_disputes` | Есть спорные строки. Нужно уточнить данные. |
| `empty_or_invalid` | Заказ пустой или непонятный. |

## 5. Что такое спорные строки

Спорная строка — это строка, которую нельзя безопасно обработать без уточнения.

Спорным считается:

- не хватает высоты;
- не хватает ширины;
- слишком много чисел;
- количество непонятно;
- строка не похожа на размер;
- текст нельзя безопасно разобрать.

Главное правило:

```text
Спорное не додумывать.
```

Если строка непонятная, ядро не должно притворяться, что всё ясно. Оно должно пометить строку как спорную.

## 6. Как считается площадь

Формула:

```text
area_m2 = height_mm * width_mm * quantity / 1_000_000
```

Пример:

```text
1000 * 400 * 2 / 1_000_000 = 0.8 м²
```

Площадь считается только по подтверждённым строкам.

Спорные строки в площадь не входят.

## 7. Что значит Corel-модель

Corel-модель сейчас — это не реальный экспорт.

Это внутренняя подготовка данных для будущего Corel export.

Одна нейтральная Corel-строка содержит только:

```text
height_mm
width_mm
quantity
```

Никаких цен, материалов, ЛКМ, файлов и команд Corel сейчас нет.

## 8. Когда Corel-строки готовы

Corel-строки готовы, если:

```text
status = clean
disputed_rows пустой
export_blocked = false
```

То есть заказ должен быть чистым и без спорных строк.

## 9. Когда Corel-строки заблокированы

Corel-строки заблокированы, если:

- есть спорные строки;
- `status = has_disputes`;
- `status = empty_or_invalid`;
- `export_blocked = true`.

Если Corel-строки заблокированы, значит сначала нужно уточнить заказ.

## 10. Что ещё не готово

Пока не готово:

```text
Excel-файл
реальный Corel export
Telegram
Vision
API
база данных
цены
стоимость
ЛКМ
материалы
производство
CNC-обучение
```

Эти слои нельзя запускать без отдельного решения и отдельного разрешения.

## 11. Куда смотреть пользователю

Если непонятно, что происходит, открывай эти файлы:

```text
E:\Hermes-Hub\КУДА_НАЖИМАТЬ.md
E:\Hermes-Hub\КАРТА_ПАПОК.md
E:\Hermes-Hub\ЕЖЕДНЕВНИК.md
E:\Hermes-Hub\СПИСОК_ПАКЕТОВ_ПО_РУССКИ.md
E:\Hermes-Hub\ЗАЩИТА_ПРОЕКТА.md
```

Самый простой старт:

```text
E:\Hermes-Hub\КУДА_НАЖИМАТЬ.md
```

## 11.1 Главные запускатели

Главные файлы для работы:

Открыть файл заказа:

```text
E:\Hermes-Hub\ОТКРЫТЬ_ФАЙЛ_ЗАКАЗА.cmd
```

Проверить заказ из файла:

```text
E:\Hermes-Hub\ПРОВЕРИТЬ_ЗАКАЗ_ИЗ_ФАЙЛА.cmd
```

Открыть последний результат:

```text
E:\Hermes-Hub\ОТКРЫТЬ_ПОСЛЕДНИЙ_РЕЗУЛЬТАТ.cmd
```

Открыть эту инструкцию:

```text
E:\Hermes-Hub\ОТКРЫТЬ_ИНСТРУКЦИЮ.cmd
```

Обычный порядок:

1. Открой файл заказа.
2. Вставь заказ и сохрани.
3. Запусти проверку заказа из файла.
4. Открой последний результат.

Быстрые проверки примеров:

```text
E:\Hermes-Hub\ПРОВЕРИТЬ_ПРИМЕР_ЧИСТЫЙ.cmd
E:\Hermes-Hub\ПРОВЕРИТЬ_ПРИМЕР_СПОРНЫЙ.cmd
E:\Hermes-Hub\ПРОВЕРИТЬ_ПРИМЕР_МУСОРНЫЙ.cmd
E:\Hermes-Hub\ПРОВЕРИТЬ_ПРИМЕР_РАЗНЫЕ_РАЗДЕЛИТЕЛИ.cmd
```

## 12. Как вручную ввести свой заказ

Чтобы проверить свой текст заказа локально, открой через Win+R или двойным кликом:

```text
E:\Hermes-Hub\ВВЕСТИ_ЗАКАЗ_ВРУЧНУЮ.cmd
```

Что делать дальше:

1. Вставь текст заказа.
2. На новой строке напиши:

```text
ГОТОВО
```

3. Нажми Enter.

В результате будет показано:

- исходный текст заказа;
- `status`;
- подтверждённые строки;
- спорные строки;
- площадь;
- заблокирован ли будущий экспорт;
- внутренние Corel-строки;
- причина блокировки, если она есть.

Этот же результат сохраняется в обычный текстовый файл:

```text
E:\Hermes-Hub\outputs\LAST_ORDER_RESULT.txt
```

Чтобы открыть последний результат через Win+R:

```text
notepad E:\Hermes-Hub\outputs\LAST_ORDER_RESULT.txt
```

Файл перезаписывается при каждой новой проверке заказа, чтобы не плодить мусор.

Это не Telegram, не Excel, не Corel-файл и не производство. Это только локальная проверка текста заказа через минимальное ядро.

## 13. Как проверить заказ из файла

Если не хочешь каждый раз вставлять заказ в консоль, используй входной файл:

```text
E:\Hermes-Hub\inputs\ORDER_INPUT.txt
```

Открыть его через Win+R:

```text
notepad E:\Hermes-Hub\inputs\ORDER_INPUT.txt
```

Что делать:

1. Открой `ORDER_INPUT.txt`.
2. Удали старый пример.
3. Вставь свой заказ.
4. Сохрани файл.
5. Запусти через Win+R или двойным кликом:

```text
E:\Hermes-Hub\ПРОВЕРИТЬ_ЗАКАЗ_ИЗ_ФАЙЛА.cmd
```

Результат появится на экране и сохранится сюда:

```text
E:\Hermes-Hub\outputs\LAST_ORDER_RESULT.txt
```

Открыть результат через Win+R:

```text
notepad E:\Hermes-Hub\outputs\LAST_ORDER_RESULT.txt
```

Это не Excel, не Corel-файл и не производственный экспорт. Это только локальная проверка обычного `.txt`-заказа.

## 14. Как читать результат

Последний результат лежит здесь:

```text
E:\Hermes-Hub\outputs\LAST_ORDER_RESULT.txt
```

Открыть его можно так:

```text
E:\Hermes-Hub\ОТКРЫТЬ_ПОСЛЕДНИЙ_РЕЗУЛЬТАТ.cmd
```

В новом формате результата есть:

- короткий итог;
- исходный заказ;
- подтверждённые строки;
- спорные строки;
- Corel-строки;
- подсказка, что делать дальше.

## 15. Где лежат примеры

Примеры заказов:

```text
E:\Hermes-Hub\examples\CLEAN_ORDER.txt
E:\Hermes-Hub\examples\DISPUTED_ORDER.txt
E:\Hermes-Hub\examples\EMPTY_OR_INVALID_ORDER.txt
E:\Hermes-Hub\examples\MIXED_SEPARATORS_ORDER.txt
```

Они нужны, чтобы быстро проверить ядро без ручного набора заказа.

## 16. Что будет следующим этапом

Следующий логичный этап — спланировать простой способ ручной проверки ядра, чтобы пользователь мог понятным способом дать текст заказа и увидеть результат.

Пока не переходим к:

```text
Telegram
Vision
API
база данных
реальный Excel/Corel export
производство
```

Эти направления требуют отдельного решения.

## 17. Как создать Excel для Corel

Excel для Corel создаётся только из чистого заказа.

Сначала открой входной файл заказа:

```text
notepad E:\Hermes-Hub\inputs\ORDER_INPUT.txt
```

Вставь заказ, сохрани файл и запусти:

```text
E:\Hermes-Hub\СОЗДАТЬ_EXCEL_ДЛЯ_COREL.cmd
```

Если заказ чистый (`status = clean`), будет создан файл:

```text
E:\Hermes-Hub\outputs\COREL_EXPORT.xlsx
```

Структура файла:

- первая строка пустая;
- заголовков нет;
- 3 колонки: высота, ширина, количество;
- только подтверждённые строки;
- спорные строки не попадают в Excel.

Если есть спорные строки или заказ пустой/непонятный, Excel не создаётся. Сначала исправь `ORDER_INPUT.txt`, потом запусти проверку снова.

Это не Telegram, не Vision, не API, не база, не расчёт цены и не производство. Это только локальный `.xlsx` для будущей работы с Corel.

## 18. Главный запуск заказа

Теперь основной простой способ работы — один запускатель:

```text
E:\Hermes-Hub\ЗАПУСТИТЬ_ЗАКАЗ.cmd
```

Порядок:

1. Открой файл заказа:

```text
notepad E:\Hermes-Hub\inputs\ORDER_INPUT.txt
```

2. Вставь заказ и сохрани файл.

3. Запусти:

```text
E:\Hermes-Hub\ЗАПУСТИТЬ_ЗАКАЗ.cmd
```

Что произойдёт:

- заказ будет проверен;
- результат сохранится сюда:

```text
E:\Hermes-Hub\outputs\LAST_ORDER_RESULT.txt
```

- если заказ чистый, Excel для Corel будет создан или обновлён здесь:

```text
E:\Hermes-Hub\outputs\COREL_EXPORT.xlsx
```

- если есть спорные строки или заказ пустой/непонятный, Excel не создаётся и не обновляется.

Если Excel заблокирован, открой результат:

```text
notepad E:\Hermes-Hub\outputs\LAST_ORDER_RESULT.txt
```

Исправь спорные строки в `ORDER_INPUT.txt` и снова запусти `ЗАПУСТИТЬ_ЗАКАЗ.cmd`.
~~~

---

## Source: ЕЖЕДНЕВНИК.md

~~~markdown
# Ежедневник Hermes Hub

Этот файл можно копировать как шаблон для дневной записи.

## Дата

```text
YYYY-MM-DD
```

## Главная задача дня

```text
Коротко: что сегодня главное?
```

## Направление дня

```text
Планирование / код / проверка / уборка / обучение / другое.
```

## Что сделал

```text
1.
2.
3.
```

## Что понял

```text
Главные выводы дня.
```

## Где застрял

```text
Что мешает двигаться дальше?
```

## Что не трогать сегодня

```text
.env, orders.db, .git, токены, Telegram, Vision, API, старую Малярку, bot.py, Docker, commits/push.
```

## Следующий шаг завтра

```text
Один понятный следующий шаг.
```

## Оценка дня

```text
0-10 и коротко почему.
```
~~~

---

## Source: ЗАЩИТА_ПРОЕКТА.md

~~~markdown
# Защита проекта Hermes Hub / Malyarka Clean

Этот файл нужен, чтобы пользователь, Codex, ChatGPT и будущий Hermes понимали, где находятся риски и что нельзя трогать без отдельного разрешения.

## 1. Главные запретные зоны

Без отдельного прямого разрешения нельзя трогать:

```text
.env
orders.db
.git
токены
ключи
Telegram
Vision
API
Docker
старая Малярка как активная система
bot.py
commits/push
```

## 2. Что Codex не должен делать без отдельного разрешения

Codex не должен:

- запускать приложение;
- запускать Telegram или polling;
- подключать внешние API;
- читать или менять секреты;
- менять базу данных;
- делать commit или push;
- переименовывать технические папки;
- использовать старую Малярку как активную систему.

## 3. Что разрешено в обычных безопасных пакетах

В обычных безопасных пакетах можно:

- создавать документацию;
- обновлять `state`, `tasks`, `worklog`, `patch`, `report`, `bundle`;
- писать код только если пакет явно технический и пользователь дал разрешение;
- запускать только focused tests, если они относятся к текущему пакету.

## 4. Как проверять безопасность после каждого пакета

После каждого пакета нужно проверить и записать в отчёт:

- `CHATGPT_CONTEXT_BUNDLE.md` обновлён;
- реальные секреты не найдены;
- запретные зоны не тронуты;
- если `tools` изменялись, указать зачем;
- если код писался, указать какие тесты прошли;
- если приложение не запускалось, явно указать это.

## 5. Что нельзя отправлять в ChatGPT

В ChatGPT нельзя отправлять:

- токены;
- ключи;
- содержимое `.env`;
- личные данные;
- содержимое базы `orders.db`;
- приватные данные клиентов.

## 6. Как действовать перед рискованным пакетом

Перед рискованным пакетом порядок такой:

1. Сначала план.
2. Потом отдельное разрешение пользователя.
3. Потом выполнение.
4. Потом отчёт.
5. Потом принятие или отклонение результата.

## 7. Будущие рискованные слои

Эти направления считаются будущими рискованными слоями:

```text
CNC-обучение
Vision
Telegram
API
база данных
Excel/Corel export
производство
```

Их нельзя запускать без отдельного разрешения пользователя.

## 8. Простое правило

Если действие может:

- отправить данные наружу;
- запустить бота;
- изменить базу;
- раскрыть секреты;
- повлиять на старую Малярку;
- создать реальный производственный файл;
- сделать commit или push;

значит сначала нужен отдельный план и отдельное разрешение.
~~~

---

## Source: КАРТА_ПАПОК.md

~~~markdown
# Карта папок Hermes Hub

Этот файл нужен, чтобы быстро понимать английские названия папок в проекте.

## Главные папки

| Папка | Простое объяснение |
|---|---|
| `logs` | Журнал работ: что уже делали, когда и зачем. |
| `tasks` | Следующие задачи: что делать дальше. |
| `patches` | Изменения проекта: короткая приёмка последнего изменения. |
| `handoff` | Передача между ChatGPT и Codex: активный пакет, отчёт и общий контекст. |
| `progress` | Карточка прогресса: где мы сейчас, куда идём, что уже закрыто. |
| `projects` | Рабочие проекты: здесь лежит `malyarka-clean`. |
| `docs` | Документы и правила: архитектура, контракты, правила парсинга и расчёта. |
| `tools` | Инструменты: скрипты для обновления контекста и служебных файлов. |

## Внутри рабочего проекта

| Папка | Простое объяснение |
|---|---|
| `src` | Исходный код будущей программы. |
| `tests` | Проверки: тесты, которые подтверждают, что код работает как задумано. |

## Важное правило

Папки не переименовываем. Английские имена нужны для кода и инструментов. Для человека используем эту русскую карту.
~~~

---

## Source: КУДА_НАЖИМАТЬ.md

~~~markdown
# Куда нажимать

Простая шпаргалка по проекту Hermes Hub.

## Если хочу понять, что сейчас происходит

Открыть:

```text
E:\Hermes-Hub\progress\PROGRESS_CARD.md
```

## Если хочу увидеть, что уже делали

Открыть:

```text
E:\Hermes-Hub\logs\WORKLOG.md
```

## Если хочу увидеть следующий шаг

Открыть:

```text
E:\Hermes-Hub\tasks\NEXT_TASKS.md
```

## Если хочу передать отчёт ChatGPT

Открыть:

```text
E:\Hermes-Hub\handoff\REPORT_TO_CHATGPT.md
```

## Если хочу понять последнее изменение

Открыть:

```text
E:\Hermes-Hub\patches\LATEST_STATE_PATCH.md
```

## Если не понимаю английское имя папки

Открыть:

```text
E:\Hermes-Hub\КАРТА_ПАПОК.md
```

## Если не понимаю номер пакета

Открыть:

```text
E:\Hermes-Hub\СПИСОК_ПАКЕТОВ_ПО_РУССКИ.md
```

## Быстро открыть папку проекта через Win+R

```text
explorer E:\Hermes-Hub
```
~~~

---

## Source: РУЧНАЯ_ПРОВЕРКА_ЯДРА.md

~~~markdown
# Ручная проверка ядра Malyarka Clean

Этот файл нужен, чтобы простыми словами проверить минимальное ядро Malyarka Clean на трёх понятных примерах.

Это не Telegram, не Vision, не API, не база данных, не Excel и не реальный Corel export.

## Зачем нужна ручная проверка

Ручная проверка нужна, чтобы увидеть, что ядро уже умеет:

- принимать текст заказа;
- разбирать понятные размеры;
- отделять подтверждённые строки от спорных;
- считать площадь подтверждённых строк;
- формировать итоговый результат заказа;
- готовить нейтральные Corel-строки только для чистого заказа;
- блокировать Corel-строки, если заказ спорный или пустой.

## Как запускать двойным кликом

Для ручной проверки открой через Проводник или Win+R:

```text
E:\Hermes-Hub\ЗАПУСТИТЬ_РУЧНУЮ_ПРОВЕРКУ_ЯДРА.cmd
```

Для focused tests ядра открой через Проводник или Win+R:

```text
E:\Hermes-Hub\ЗАПУСТИТЬ_ТЕСТЫ_ЯДРА.cmd
```

Эти команды сами настраивают `PYTHONPATH`, поэтому вручную писать его не нужно.

Они не запускают Telegram, Vision, API, базу данных и Excel/Corel export.

## Альтернативная ручная команда

Открой PowerShell и выполни:

```powershell
python E:\Hermes-Hub\projects\malyarka-clean\tools\manual_core_check.py
```

## Какие примеры проверяются

### 1. Чистый заказ

```text
1000 400 2
700 300
```

Должно получиться:

- `status = clean`;
- спорных строк нет;
- площадь посчитана;
- `corel_rows` готовы;
- `export_blocked = false`.

### 2. Заказ со спорной строкой

```text
1000 400 2
мусор
700 300
```

Должно получиться:

- `status = has_disputes`;
- спорная строка есть;
- площадь считается только по понятным строкам;
- `corel_rows` заблокированы;
- `export_blocked = true`.

### 3. Пустой или мусорный заказ

```text
привет
ничего непонятно
```

Должно получиться:

- `status = empty_or_invalid`;
- `total_area_m2 = 0`;
- `corel_rows` заблокированы;
- `export_blocked = true`.

Важно:

Если сейчас в этом примере появляется `status = has_disputes`, это найденное расхождение в правилах статуса. Его нужно исправлять отдельным следующим пакетом, а не маскировать в ручной проверке.

## Что эта проверка не делает

Она не делает:

- Telegram;
- Vision;
- API;
- базу данных;
- Excel-файл;
- Corel-файл;
- экспорт на диск;
- цены;
- стоимость;
- ЛКМ;
- материалы;
- производство.

## Следующий этап

После успешной ручной проверки можно планировать следующий безопасный слой: удобный пользовательский запуск или простую входную форму, но не переходить к Telegram, Vision, API и базе без отдельного решения.

Если ручная проверка показывает расхождение в статусах, следующий этап должен сначала исправить правила ядра.
~~~

---

## Source: СПИСОК_ПАКЕТОВ_ПО_РУССКИ.md

~~~markdown
# Список пакетов по-русски

Здесь простыми словами описано, что означает каждый пакет работ.

## Уже сделано

| Пакет | Техническое имя | Что означает |
|---|---|---|
| Пакет 009 | `BATCH_009_FIRST_LOCAL_PARSER_IMPLEMENTATION` | Первый локальный парсер: научили ядро понимать простые размеры из текста. |
| Пакет 010 | `BATCH_010_AREA_CALCULATION_PLANNING` | Правила расчёта площади: заранее решили, как считать площадь. |
| Пакет 011 | `BATCH_011_AREA_CALCULATION_IMPLEMENTATION` | Расчёт площади: реализовали площадь только по подтверждённым строкам. |
| Пакет 012 | `BATCH_012_ORDER_RESULT_INTEGRATION_PLANNING` | Правила итогового результата заказа: решили, как объединять строки, споры и площадь. |
| Пакет 013 | `BATCH_013_ORDER_RESULT_IMPLEMENTATION` | Итоговый результат заказа: объединили парсер, споры и площадь в один результат. |
| Пакет 014 | `BATCH_014_RUSSIAN_NAVIGATION_LAYER` | Русская навигация по проекту: понятные русские файлы, куда смотреть и что означает каждая папка. |
| Пакет 015 | `BATCH_015_COREL_EXPORT_MODEL_PLANNING` | Модель данных для Corel: спланировали, какие подтверждённые данные можно будет отдавать в будущий Corel export. |
| Пакет 016 | `BATCH_016_PROJECT_PROTECTION_LAYER` | Защита проекта: описали запретные зоны, рискованные действия и безопасный порядок работы. |
| Пакет 017 | `BATCH_017_COREL_MODEL_IMPLEMENTATION_PLANNING` | План реализации Corel-модели: описали, как безопасно потом сделать нейтральные Corel-строки без реального экспорта. |
| Пакет 018 | `BATCH_018_COREL_MODEL_IMPLEMENTATION` | Реализация нейтральной Corel-модели: подготовили внутренние строки данных без Excel/Corel-файла и без экспорта на диск. |
| Пакет 019 | `BATCH_019_ORDER_PIPELINE_SMOKE_TEST_PLANNING` | План общей проверки цепочки: описали будущую проверку от текста заказа до нейтральных Corel-строк. |
| Пакет 020 | `BATCH_020_ORDER_PIPELINE_SMOKE_TEST_IMPLEMENTATION` | Реализация общей smoke-проверки цепочки: проверили связку от текста заказа до нейтральных Corel-строк. |
| Пакет 021 | `BATCH_021_README_AND_USAGE_GUIDE_PLANNING` | План инструкции по использованию ядра: описали, какую простую русскую инструкцию нужно сделать для пользователя. |
| Пакет 022 | `BATCH_022_README_USAGE_GUIDE_IMPLEMENTATION` | Создание русской инструкции: сделали README_КАК_ПОЛЬЗОВАТЬСЯ.md для пользователя. |
| Пакет 023 | `BATCH_023_MANUAL_CORE_CHECK_PLANNING` | План ручной проверки ядра: описали простые примеры, которые пользователь сможет проверить вручную. |

## Следующие пакеты

| Пакет | Техническое имя | Что означает |
|---|---|---|
| Пакет 024 | `BATCH_024_MANUAL_CORE_CHECK_IMPLEMENTATION` | Реализация простой ручной проверки ядра без Telegram, API и экспорта. |
| Пакет 025 | `BATCH_025_EMPTY_INVALID_STATUS_FIX_PLANNING` | План исправления статуса пустого/мусорного заказа: сейчас ручная проверка нашла расхождение. |
| Пакет 026 | `BATCH_026_EMPTY_INVALID_STATUS_FIX_IMPLEMENTATION` | Исправление статуса пустого/мусорного заказа и focused tests. |
| Пакет 027 | `BATCH_027_MANUAL_CHECK_ACCEPTANCE_OR_USER_ENTRY_PLANNING` | Приёмка ручной проверки или план простого пользовательского ввода. |
| Пакет 028 | `BATCH_028_SIMPLE_RUN_COMMAND_PLANNING` | План удобного запуска без ручного PYTHONPATH. |
| Пакет 029 | `BATCH_029_SIMPLE_RUN_COMMAND_IMPLEMENTATION` | Реализация удобного запуска без ручного PYTHONPATH. |
| Пакет 030 | `BATCH_030_SIMPLE_USER_ORDER_INPUT_PLANNING` | План простого пользовательского ввода заказа. |
| Пакет 031 | `BATCH_031_SIMPLE_USER_ORDER_INPUT_IMPLEMENTATION` | Реализация простого пользовательского ввода заказа. |
| Пакет 032 | `BATCH_032_USER_INPUT_ACCEPTANCE_AND_NEXT_UI_PLANNING` | Приёмка пользовательского ввода и план следующего удобного интерфейса. |
| Пакет 033 | `BATCH_033_SAVE_ORDER_RESULT_TEXT_PLANNING` | План сохранения результата заказа в текстовый файл. |
| Пакет 034 | `BATCH_034_SAVE_ORDER_RESULT_TEXT_IMPLEMENTATION` | Реализация сохранения результата заказа в текстовый файл. |
| Пакет 035 | `BATCH_035_SAVE_RESULT_ACCEPTANCE_AND_INPUT_FILE_PLANNING` | Приёмка сохранения результата и план входного файла заказа. |
| Пакет 036 | `BATCH_036_INPUT_FILE_IMPLEMENTATION` | Реализация входного файла заказа. |
| Пакет 037 | `BATCH_037_INPUT_FILE_ACCEPTANCE_AND_USER_SHORTCUTS_PLANNING` | Приёмка входного файла и план пользовательских ярлыков. |
| Пакет 038 | `BATCH_038_USER_SHORTCUTS_IMPLEMENTATION` | Пользовательские ярлыки для заказа, результата и инструкции. |
| Пакет 039 | `BATCH_039_LOCAL_V0_1_ACCEPTANCE` | Приёмка локальной версии Malyarka Clean v0.1. |
| Пакет 040 | `BATCH_040_RESULT_READABILITY_PLANNING` | План улучшения читаемости текстового результата. |
| Пакет 041 | `BATCH_041_RESULT_READABILITY_IMPLEMENTATION` | Реализация улучшенного текстового результата. |
| Пакет 042 | `BATCH_042_ORDER_EXAMPLES_IMPLEMENTATION` | Примеры заказов для быстрой проверки. |
| Пакет 043 | `BATCH_043_EXAMPLE_CHECK_COMMANDS_IMPLEMENTATION` | Быстрые .cmd-проверки примеров. |
| Пакет 044 | `BATCH_044_READABLE_RESULT_AND_EXAMPLES_ACCEPTANCE` | Приёмка читаемого результата и примеров. |
| Пакет 045 | `BATCH_045_LOCAL_V01_ACCEPTANCE_AND_NEXT_ROADMAP_PLANNING` | Приёмка локальной v0.1 и план следующей дорожной карты. |
| Пакет 046 | `BATCH_046_NEXT_ROADMAP_OPTIONS` | Варианты следующего крупного направления. |
| Пакет 047 | `BATCH_047_RECOMMENDED_NEXT_STAGE` | Рекомендованный следующий этап. |
| Серия 048–050 | `BATCH_SERIES_048_050_SAFE_EXCEL_COREL_EXPORT_PLANNING` | План безопасного Excel/Corel export. |
| Пакет 048 | `BATCH_048_SAFE_EXCEL_COREL_EXPORT_RULES` | Правила безопасного Excel/Corel export. |
| Пакет 049 | `BATCH_049_EXCEL_COREL_FILE_STRUCTURE` | Структура будущего Excel-файла для Corel. |
| Пакет 050 | `BATCH_050_EXCEL_COREL_IMPLEMENTATION_PLAN` | План будущей реализации Excel/Corel export. |
| Серия 051–053 | `BATCH_SERIES_051_053_SAFE_EXCEL_COREL_EXPORT_IMPLEMENTATION` | Реализация безопасного Excel/Corel export после отдельного разрешения. |
| Пакет 051 | `BATCH_051_SAFE_EXCEL_COREL_EXPORT_CODE` | Код безопасного создания Excel для Corel из clean-заказа. |
| Пакет 052 | `BATCH_052_SAFE_EXCEL_COREL_EXPORT_TESTS` | Focused tests для Excel/Corel export. |
| Пакет 053 | `BATCH_053_SAFE_EXCEL_COREL_EXPORT_CMD` | Удобный запускатель СОЗДАТЬ_EXCEL_ДЛЯ_COREL.cmd. |
| Серия 054–056 | `BATCH_SERIES_054_056_EXCEL_COREL_EXPORT_ACCEPTANCE_AND_NEXT_LAYER` | Приёмка Excel/Corel export и план следующего удобного слоя. |
| Пакет 054 | `BATCH_054_EXCEL_COREL_EXPORT_ACCEPTANCE` | Приёмка безопасного Excel/Corel export. |
| Пакет 055 | `BATCH_055_CURRENT_USER_WORKFLOW` | Текущий рабочий путь пользователя. |
| Пакет 056 | `BATCH_056_NEXT_LAYER_OPTIONS_AFTER_EXCEL` | Варианты следующего удобного слоя после Excel export. |
| Серия 057–060 | `BATCH_SERIES_057_060_SINGLE_LOCAL_ORDER_RUNNER` | Единый локальный запуск заказа: проверить заказ и создать Excel если можно. |
| Пакет 057 | `BATCH_057_SINGLE_LOCAL_RUNNER_CODE` | Код единого локального запуска заказа. |
| Пакет 058 | `BATCH_058_SINGLE_LOCAL_RUNNER_TESTS` | Focused tests для единого локального запуска. |
| Пакет 059 | `BATCH_059_SINGLE_LOCAL_RUNNER_CMD` | Главный запускатель ЗАПУСТИТЬ_ЗАКАЗ.cmd. |
| Пакет 060 | `BATCH_060_SINGLE_LOCAL_RUNNER_ACCEPTANCE` | Приёмка единого локального запуска заказа. |
| Серия 061–063 | `BATCH_SERIES_061_063_USER_GUIDE_AND_LOCAL_RELEASE_CHECK` | Упрощение пользовательской инструкции и контрольная проверка локальной версии. |
| Пакет 061 | `BATCH_061_SIMPLIFY_USER_GUIDE` | Упрощение пользовательской инструкции. |
| Пакет 062 | `BATCH_062_LOCAL_RELEASE_CONTROL_CHECK` | Контрольная проверка локальной версии. |
| Пакет 063 | `BATCH_063_CURRENT_LOCAL_RELEASE_DOCUMENT` | Итоговый документ текущей локальной версии. |
| Серия 064–066 | `BATCH_SERIES_064_066_NEXT_MAJOR_DIRECTION_SELECTION` | Выбор следующего крупного направления после локальной версии. |
| Пакет 064 | `BATCH_064_NEXT_MAJOR_DIRECTION_REVIEW` | Обзор возможных следующих крупных направлений. |
| Пакет 065 | `BATCH_065_TELEGRAM_STAGE_PREVIEW` | Предварительный обзор Telegram-этапа. |
| Пакет 066 | `BATCH_066_RECOMMENDED_NEXT_MAJOR_DIRECTION` | Рекомендация следующего крупного направления. |
| Серия 067–069 | `BATCH_SERIES_067_069_SAFE_TELEGRAM_LAYER_PLANNING` | План безопасного Telegram-слоя. |
| Пакет 067 | `BATCH_067_SAFE_TELEGRAM_RULES` | Правила безопасного Telegram-слоя: использовать существующее ядро, не трогать секреты, polling, старый bot.py и Excel/Corel export без отдельного плана. |
| Пакет 068 | `BATCH_068_TELEGRAM_MINIMAL_UX_PLAN` | Минимальный UX Telegram: отправить текст заказа, получить статус, строки, площадь и подсказку. |
| Пакет 069 | `BATCH_069_TELEGRAM_IMPLEMENTATION_PLAN` | План будущей реализации: новый adapter, check-режим, тесты, dry-run и только потом отдельное разрешение на token/polling. |
| Серия 070–073 | `BATCH_SERIES_070_073_SAFE_TELEGRAM_SKELETON_NO_LIVE_RUN` | Безопасный Telegram-каркас без live-запуска. |
| Пакет 070 | `BATCH_070_SAFE_TELEGRAM_LAYER_SKELETON` | Новый безопасный Telegram-пакет внутри Malyarka Clean без token, .env, aiogram и live-запуска. |
| Пакет 071 | `BATCH_071_SAFE_TELEGRAM_ADAPTER` | Adapter, который принимает текст заказа и возвращает русский ответ через существующее ядро. |
| Пакет 072 | `BATCH_072_SAFE_TELEGRAM_ADAPTER_TESTS` | Focused tests для adapter: импорт без token/.env, clean/disputed/invalid ответы, без Excel и polling. |
| Пакет 073 | `BATCH_073_TELEGRAM_SKELETON_ACCEPTANCE` | Приёмка безопасного Telegram-каркаса. |
| Серия 074–076 | `BATCH_SERIES_074_076_TELEGRAM_SKELETON_CHECK_AND_CONNECTION_PLAN` | Проверка Telegram-каркаса и план безопасного подключения. |
| Пакет 074 | `BATCH_074_TELEGRAM_SKELETON_CHECK` | Проверка Telegram-каркаса focused tests и безопасными import/check-командами. |
| Пакет 075 | `BATCH_075_TELEGRAM_SKELETON_CHECK_DOCUMENT` | Документ проверки Telegram-каркаса: что проверено и что не запускалось. |
| Пакет 076 | `BATCH_076_TELEGRAM_SAFE_CONNECTION_PLAN` | План будущего безопасного подключения Telegram без реального запуска. |
| Серия 077–079 | `BATCH_SERIES_077_079_WORK_ORDERS_FOLDER_STRUCTURE_PLANNING` | План структуры рабочей папки заказов. |
| Пакет 077 | `BATCH_077_WORK_ROOT_STRUCTURE_PLAN` | План главной структуры будущей папки E:\РАБОТА без создания реальных папок. |
| Пакет 078 | `BATCH_078_SINGLE_ORDER_FOLDER_STRUCTURE_PLAN` | План структуры одной папки заказа: Исходные, Corel, ArtCAM, Excel, Покраска. |
| Пакет 079 | `BATCH_079_WORK_FOLDER_EXAMPLES_AND_ACCEPTANCE` | Примеры Абай планки и Петр столики, решения v0.1 и запрет трогать реальные заказы. |
| Серия 080–082 | `BATCH_SERIES_080_082_CREATE_EMPTY_WORK_FOLDER_STRUCTURE` | Создание пустой рабочей папки E:\РАБОТА и пяти верхних подпапок. |
| Пакет 080 | `BATCH_080_CREATE_WORK_ROOT_IF_MISSING` | Проверка и создание пустой папки E:\РАБОТА, если её ещё нет. |
| Пакет 081 | `BATCH_081_CREATE_EMPTY_WORK_TOP_FOLDERS` | Создание пяти пустых подпапок: Заказы, Шаблоны, Инструменты, Архив, Разобрать. |
| Пакет 082 | `BATCH_082_EMPTY_WORK_FOLDER_ACCEPTANCE` | Документ приёмки пустой рабочей структуры без переноса старых заказов. |
| Серия 080-082 | `BATCH_SERIES_080_082_OLD_MALYARKA_ARCHIVE_FUTURE_PLAN` | План будущего использования архива старой Малярки как источника идей, не действующих правил. |
| Пакет 080 | `BATCH_080_OLD_ARCHIVE_STATUS_PLAN` | Статус архива: полезен как источник идей, но не является актуальными правилами Hermes. |
| Пакет 081 | `BATCH_081_OLD_ARCHIVE_FUTURE_BLOCKS` | Разбор будущих блоков: шаблоны, цены, экономика, зарплаты, склад, итоговый файл, старый код. |
| Пакет 082 | `BATCH_082_OLD_ARCHIVE_WORK_ORDER_PLAN` | Будущий порядок работы: разбирать архивные блоки отдельно и переносить только после подтверждения. |
| Серия 083-086 | `BATCH_SERIES_083_086_TELEGRAM_SAFE_CHECK_COMMAND` | Безопасная Telegram check-команда без live-запуска. |
| Пакет 083 | `BATCH_083_TELEGRAM_SAFE_CHECK_SCRIPT` | Скрипт `check_telegram_skeleton.py`: проверяет импорт, diagnostics и adapter без token, .env, Telegram и polling. |
| Пакет 084 | `BATCH_084_TELEGRAM_SAFE_CHECK_TESTS` | Focused tests для check-команды: без token/.env, без старого bot.py, без Excel, без polling. |
| Пакет 085 | `BATCH_085_TELEGRAM_SAFE_CHECK_DOCUMENT` | Документ `MALYARKA_CLEAN_TELEGRAM_SAFE_CHECK_COMMAND.md` с назначением и границами dry-check. |
| Пакет 086 | `BATCH_086_TELEGRAM_SAFE_CHECK_STATE_UPDATE` | Обновление состояния Hermes Hub и context bundle после безопасной check-команды. |
| Серия 087-089 | `BATCH_SERIES_087_089_CREATE_EMPTY_WORK_FOLDER_STRUCTURE` | Проверка и подтверждение пустой рабочей папки E:\РАБОТА и пяти верхних подпапок. |
| Пакет 087 | `BATCH_087_CREATE_OR_VERIFY_WORK_ROOT` | Проверка `E:\РАБОТА`: папка уже существовала, ничего не удалялось и не перезаписывалось. |
| Пакет 088 | `BATCH_088_CREATE_OR_VERIFY_WORK_TOP_FOLDERS` | Подтверждены пять верхних подпапок: Заказы, Шаблоны, Инструменты, Архив, Разобрать. |
| Пакет 089 | `BATCH_089_EMPTY_WORK_FOLDER_ACCEPTANCE_UPDATE` | Обновлён документ приёмки пустой рабочей структуры без переноса старых заказов. |
| Серия 090-092 | `BATCH_SERIES_090_092_ORDER_FOLDER_TEMPLATE_PLANNING` | План шаблона первой папки заказа внутри E:\РАБОТА без создания реальных папок заказа. |
| Пакет 090 | `BATCH_090_ORDER_FOLDER_TEMPLATE_DOCUMENT` | Документ `ORDER_FOLDER_TEMPLATE_V0_1.md` с будущим путём и структурой папки заказа. |
| Пакет 091 | `BATCH_091_ORDER_FOLDER_PURPOSES_AND_DECISIONS` | Назначение подпапок заказа и решения v0.1: без Фото_заметки, сложность в карточке, итоговый файл позже. |
| Пакет 092 | `BATCH_092_FUTURE_ORDER_CARD_PLAN` | Будущая карточка заказа описана как идея без создания реального файла. |
| Серия 093-095 | `BATCH_SERIES_093_095_CREATE_ONE_EMPTY_TEST_ORDER_FOLDER` | Создание одной пустой папки тестового заказа по шаблону v0.1. |
| Пакет 093 | `BATCH_093_TEST_ORDER_BASE_STRUCTURE_CHECK` | Проверка базовой структуры `E:\РАБОТА` и `E:\РАБОТА\01_ЗАКАЗЫ` перед созданием тестового шаблона. |
| Пакет 094 | `BATCH_094_CREATE_EMPTY_TEST_ORDER_FOLDER` | Создание `Тестовый_заказ` и пяти пустых подпапок без файлов заказа и без `ORDER_CARD.md`. |
| Пакет 095 | `BATCH_095_TEST_ORDER_FOLDER_ACCEPTANCE` | Документ приёмки пустой тестовой папки заказа без переноса старых заказов. |
| Серия 096-098 | `BATCH_SERIES_096_098_ORDER_CARD_TEMPLATE_PLANNING` | План шаблона будущей карточки заказа `ORDER_CARD.md` без создания файла в E:\РАБОТА. |
| Пакет 096 | `BATCH_096_ORDER_CARD_PURPOSE_DOCUMENT` | Документ `ORDER_CARD_TEMPLATE_V0_1.md` и назначение карточки заказа. |
| Пакет 097 | `BATCH_097_ORDER_CARD_SIMPLE_TEMPLATE` | Простой шаблон карточки: основное, тип заказа, материал, файлы, детали, примечания, будущие данные. |
| Пакет 098 | `BATCH_098_ORDER_CARD_TEST_EXAMPLE` | Пример заполнения для `Тестовый_заказ` только в документации, без создания реального `ORDER_CARD.md`. |
| Серия 099-101 | `BATCH_SERIES_099_101_CREATE_TEST_ORDER_CARD` | Создание `ORDER_CARD.md` только в тестовой папке заказа. |
| Пакет 099 | `BATCH_099_TEST_ORDER_FOLDER_CHECK` | Проверка существования тестовой папки и пяти подпапок. |
| Пакет 100 | `BATCH_100_CREATE_TEST_ORDER_CARD` | Создание тестовой карточки `ORDER_CARD.md` по шаблону v0.1. |
| Пакет 101 | `BATCH_101_TEST_ORDER_CARD_ACCEPTANCE` | Документ приёмки тестовой карточки заказа. |
| Серия 102-104 | `BATCH_SERIES_102_104_ACCEPT_ORDER_CARD_AND_WORK_FOLDER_BASE` | Приёмка `ORDER_CARD.md v0.1` и закрытие базовой структуры `E:\РАБОТА`. |
| Пакет 102 | `BATCH_102_ORDER_CARD_V01_ACCEPTANCE` | Документ приёмки `ORDER_CARD.md v0.1`: решение пользователя `ОСТАВЛЯЕМ`. |
| Пакет 103 | `BATCH_103_WORK_FOLDER_BASE_STATUS_ACCEPTANCE` | Фиксация статуса `E:\РАБОТА`, тестового заказа и базовой структуры. |
| Пакет 104 | `BATCH_104_ACCEPTANCE_STATE_UPDATE` | Обновление состояния Hermes Hub и context bundle. |
| Серия 105-108 | `BATCH_SERIES_105_108_TELEGRAM_SAFE_CONFIG_CHECK` | Безопасная Telegram config-check проверка без token, .env, polling и live Telegram. |
| Пакет 105 | `BATCH_105_TELEGRAM_CONFIG_CHECK_MODULE` | Модуль `config_check.py` со статическими безопасными diagnostics. |
| Пакет 106 | `BATCH_106_TELEGRAM_CONFIG_CHECK_CLI` | CLI `check_telegram_config.py` для безопасной config-check проверки. |
| Пакет 107 | `BATCH_107_TELEGRAM_CONFIG_CHECK_TESTS` | Focused tests для config-check. |
| Пакет 108 | `BATCH_108_TELEGRAM_CONFIG_CHECK_DOC` | Документ `MALYARKA_CLEAN_TELEGRAM_SAFE_CONFIG_CHECK.md`. |
| Серия 109-112 | `BATCH_SERIES_109_112_TELEGRAM_TOKEN_ENV_SAFETY_PLAN` | План безопасной работы с Telegram token и .env перед реальным подключением. |
| Пакет 109 | `BATCH_109_TELEGRAM_TOKEN_ENV_STATUS_PLAN` | Фиксация текущего статуса: token не подключён, .env не используется, live/polling не запускались. |
| Пакет 110 | `BATCH_110_TELEGRAM_TOKEN_ENV_RULES` | Правила: token не выводить, .env не читать/создавать без разрешения, старые token/JSON не использовать. |
| Пакет 111 | `BATCH_111_TELEGRAM_TOKEN_ENV_FUTURE_CHECK_RULES` | Будущая проверка может показывать только наличие token/.env, но не значение. |
| Пакет 112 | `BATCH_112_TELEGRAM_TOKEN_ENV_STATE_UPDATE` | Обновление состояния Hermes Hub и bundle после плана. |
| Серия 113-116 | `BATCH_SERIES_113_116_CREATE_HERMES_NAVIGATION_INDEX` | Короткий навигационный индекс Hermes Hub для больших файлов. |
| Пакет 113 | `BATCH_113_CREATE_HERMES_NAVIGATION_INDEX` | Создание `HERMES_NAVIGATION_INDEX.md`. |
| Пакет 114 | `BATCH_114_NAVIGATION_ACCEPTED_BLOCKS` | Фиксация последних принятых блоков в индексе. |
| Пакет 115 | `BATCH_115_NAVIGATION_FORBIDDEN_ZONES` | Фиксация текущих запретов в индексе. |
| Пакет 116 | `BATCH_116_NAVIGATION_NEXT_STEP_AND_BIG_FILE_RULE` | Следующий безопасный шаг и правило работы с большими файлами. |

## Будущие идеи, не сейчас

| Идея | Статус |
|---|---|
| CNC-обучение | Будущая идея. Сейчас не делаем. |
| Карточки заказов | Будущая идея. Сейчас не делаем. |
| Telegram | Позже, только после отдельного разрешения. |
| Vision | Позже, только после отдельного разрешения. |
| API | Позже, только после отдельного разрешения. |

## Серия 117-120

| Пакет | Техническое имя | По-русски |
|---|---|---|
| Серия 117-120 | `BATCH_SERIES_117_120_TELEGRAM_PRE_TOKEN_READINESS_CHECK` | Предстартовая Telegram readiness-проверка без token и без `.env`. |
| Пакет 117 | `BATCH_117_TELEGRAM_PRE_TOKEN_READINESS_MODULE` | Модуль `readiness.py` со статическими безопасными diagnostics. |
| Пакет 118 | `BATCH_118_TELEGRAM_PRE_TOKEN_READINESS_CLI` | CLI `check_telegram_pre_token_readiness.py` с русским dry-run отчётом. |
| Пакет 119 | `BATCH_119_TELEGRAM_PRE_TOKEN_READINESS_TESTS` | Focused tests: без token, без `.env`, без Telegram/polling, без Excel. |
| Пакет 120 | `BATCH_120_TELEGRAM_PRE_TOKEN_READINESS_DOC` | Документ `MALYARKA_CLEAN_TELEGRAM_PRE_TOKEN_READINESS.md`. |

## Серия 121-124

| Пакет | Техническое имя | По-русски |
|---|---|---|
| Серия 121-124 | `BATCH_SERIES_121_124_EXISTING_TELEGRAM_BOT_SERVER_INVENTORY` | Документирование ручной read-only инвентаризации существующего Telegram-бота на сервере hermes. |
| Пакет 121 | `BATCH_121_EXISTING_BOT_SERVER_IDENTITY` | Фиксация сервера hermes, IP и пути `/opt/malyarka-telegram-bot`. |
| Пакет 122 | `BATCH_122_EXISTING_BOT_PROJECT_STRUCTURE` | Фиксация найденной структуры server bot: корень, Telegram-слой, core-слой и services. |
| Пакет 123 | `BATCH_123_EXISTING_BOT_RUNNING_PROCESS` | Фиксация работающего polling-процесса и неизвестного способа автозапуска. |
| Пакет 124 | `BATCH_124_EXISTING_BOT_SAFETY_BOUNDARIES` | Фиксация границ безопасности и следующего read-only шага. |

## Серия 125-128

| Пакет | Техническое имя | По-русски |
|---|---|---|
| Серия 125-128 | `BATCH_SERIES_125_128_SERVER_BOT_READ_ONLY_MAP_PLAN` | План безопасной read-only карты существующего серверного Telegram-бота. |
| Пакет 125 | `BATCH_125_SERVER_BOT_READ_ONLY_MAP_GOAL` | Цель: позже безопасно изучить запуск, команды и обработчики без остановки polling. |
| Пакет 126 | `BATCH_126_SERVER_BOT_ALLOWED_AND_FORBIDDEN_FILES` | Список файлов для будущего чтения и запретные зоны: .env, token, секреты, базы, логи с личными данными. |
| Пакет 127 | `BATCH_127_SERVER_BOT_READ_ONLY_MAP_ORDER` | Будущий порядок read-only карты: app.py, config.py, handlers.py, router.py, UX и core-связи. |
| Пакет 128 | `BATCH_128_SERVER_BOT_INVENTORY_PROHIBITIONS` | Запреты будущей инвентаризации и следующий безопасный шаг. |

## Серия 131-134

| Пакет | Техническое имя | По-русски |
|---|---|---|
| Серия 131-134 | `BATCH_SERIES_131_134_SERVER_BOT_SAFE_READ_ONLY_COLLECTOR` | Локальный safe read-only collector для будущей карты серверного Telegram-бота. |
| Пакет 131 | `BATCH_131_SERVER_BOT_COLLECTOR_TOOL` | Collector `collect_server_bot_read_only.py`, whitelist-only, read-only, без выполнения кода бота. |
| Пакет 132 | `BATCH_132_SERVER_BOT_COLLECTOR_TESTS` | Focused tests для whitelist, запретов, redaction и временного отчёта. |
| Пакет 133 | `BATCH_133_SERVER_BOT_COLLECTOR_DOCS` | Документы `SERVER_BOT_READ_ONLY_COLLECTOR.md` и acceptance. |
| Пакет 134 | `BATCH_134_SERVER_BOT_COLLECTOR_STATE_UPDATE` | Обновление state/tasks/worklog/patch/report/bundle/index. |

## Серия 135–138 — План безопасного запуска collector на read-only копии

Техническое имя:

```text
BATCH_SERIES_135_138_SERVER_BOT_READ_ONLY_COPY_COLLECTION_PLAN
```

Статус:

```text
выполнено
```

Итог:

```text
Создан план и локальная пустая папка-заготовка для будущей read-only копии whitelist-файлов серверного Telegram-бота.
Collector не запускался на сервере.
Серверные файлы не копировались.
```

Следующий безопасный шаг:

```text
Только после отдельного разрешения пользователя: поместить whitelist-файлы в локальную копию и запустить collector локально.
```

## Серия 139–142 — Инструкция безопасного копирования whitelist-файлов в read-only staging

Техническое имя:

```text
BATCH_SERIES_139_142_SERVER_BOT_WHITELIST_COPY_INSTRUCTIONS
```

Статус:

```text
выполнено
```

Итог:

```text
Создана инструкция будущего ручного копирования только whitelist-файлов в локальную staging-папку.
MANIFEST.md обновлён.
Серверные файлы не копировались, collector не запускался.
```

Следующий безопасный шаг:

```text
Только после отдельного разрешения пользователя: вручную поместить whitelist-файлы в staging, проверить checklist и запустить collector локально.
```

## Серия 143–146 — Ручной пакет копирования whitelist-файлов серверного бота

Техническое имя:

```text
BATCH_SERIES_143_146_SERVER_BOT_MANUAL_WHITELIST_COPY_PACKAGE
```

Статус:

```text
выполнено
```

Итог:

```text
Создана понятная ручная инструкция копирования whitelist-файлов и checklist staging-папки.
MANIFEST.md обновлён.
Серверные файлы не копировались, collector не запускался.
```

Следующий безопасный шаг:

```text
Только после отдельного разрешения пользователя: вручную скопировать whitelist-файлы, пройти checklist, обновить MANIFEST.md и запустить collector локально.
```

## Серия 147–150 — Подготовка staging к ручному копированию whitelist-файлов

Техническое имя:

```text
BATCH_SERIES_147_150_SERVER_BOT_STAGING_READY_FOR_MANUAL_COPY
```

Статус:

```text
выполнено
```

Итог:

```text
Созданы пустые staging-папки под whitelist-файлы.
Серверные файлы не копировались, collector не запускался.
```

Следующий безопасный шаг:

```text
Только после отдельного разрешения пользователя: вручную поместить whitelist-файлы в staging, пройти checklist, обновить MANIFEST.md и запустить collector локально.
```

## Серия 151–154 — SFTP-копирование whitelist-файлов серверного бота в staging

Техническое имя:

```text
BATCH_SERIES_151_154_SERVER_BOT_SFTP_WHITELIST_COPY
```

Статус:

```text
выполнено частично: whitelist скопирован, один файл отсутствует на сервере
```

Итог:

```text
Через SFTP скопированы только явные whitelist-файлы.
malyarka_telegram/models.py не найден на сервере.
config.py, .env, token, db, logs, .git, реальные заказы и реальные .cdr/.art/.xlsx не копировались.
Collector не запускался.
```

Следующий безопасный шаг:

```text
Пройти staging checklist и отдельно решить, запускать ли collector локально.
```

## Серия 155–158 — Проверка staging перед локальным запуском collector

Техническое имя:

```text
BATCH_SERIES_155_158_SERVER_BOT_STAGING_CHECK_BEFORE_COLLECTOR
```

Статус:

```text
выполнено
```

Итог:

```text
Локальная staging-папка проверена.
Запрещённые файлы не найдены.
malyarka_telegram/models.py отсутствует.
Collector не запускался.
```

Следующий безопасный шаг:

```text
Отдельно решить, запускать ли collector локально по staging.
```

## Серия 159–162 — Локальный запуск collector по staging-копии серверного бота

Техническое имя:

```text
BATCH_SERIES_159_162_SERVER_BOT_LOCAL_COLLECTOR_RUN
```

Статус:

```text
выполнено
```

Итог:

```text
Collector запущен только локально по staging-копии.
Создан SERVER_BOT_READ_ONLY_REPORT.md.
Сервер/live-бот/polling/token/.env/config.py не трогались.
```

Следующий безопасный шаг:

```text
Проанализировать SERVER_BOT_READ_ONLY_REPORT.md и построить architecture map серверного Telegram-бота без live-вмешательства.
```

## Серия 159–162 — Локальный запуск collector по staging-копии серверного бота, повторная проверка

Техническое имя:

```text
BATCH_SERIES_159_162_SERVER_BOT_LOCAL_COLLECTOR_RUN_REPEAT
```

Статус:

```text
выполнено повторно
```

Итог:

```text
Collector повторно запущен только локально по staging-копии.
SERVER_BOT_READ_ONLY_REPORT.md обновлён.
Сервер/live-бот/polling/token/.env/config.py/Vision/API не трогались.
```

Следующий безопасный шаг:

```text
Проанализировать SERVER_BOT_READ_ONLY_REPORT.md и построить architecture map серверного Telegram-бота без live-вмешательства.
```

## Серия 163-166 — Анализ collector-отчёта и architecture map серверного Telegram-бота

Техническое имя: BATCH_SERIES_163_166_SERVER_TELEGRAM_BOT_ARCHITECTURE_MAP

Статус: выполнено.

Создано:
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_BOT_ARCHITECTURE_MAP.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_BOT_ARCHITECTURE_MAP_SUMMARY.md

Зафиксировано:
- architecture map по локальному collector-отчёту;
- цепочка Telegram -> app.py -> router.py -> handlers.py -> core -> exports/files;
- missing malyarka_telegram/models.py;
- 22 redaction-срабатывания;
- будущие точки Hermes adapter layer.

Следующий безопасный шаг:
- Серия 167-170 — План Hermes adapter layer для серверного Telegram-бота
- техническое имя: BATCH_SERIES_167_170_HERMES_ADAPTER_LAYER_PLAN

## Серия 167-170 — План Hermes adapter layer для серверного Telegram-бота

Техническое имя: BATCH_SERIES_167_170_HERMES_ADAPTER_LAYER_PLAN

Статус: выполнено.

Создано:
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_LAYER_PLAN.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_LAYER_PLAN_SUMMARY.md

Зафиксировано:
- adapter должен стоять между router.py / handlers.py и core/services/orders.py;
- adapter принимает text, user_id, current_mode, route_result, order context, safe feature flags;
- adapter возвращает ответ, action, warnings, export availability, engineer task draft, diagnostics и fallback;
- предложены feature flags;
- старый бот должен продолжать работать, если adapter выключен или упал;
- следующий шаг — feature flags / diagnostics / rollback plan.

Следующий безопасный шаг:
- Серия 171-174 — План feature flags, diagnostics и rollback для Hermes adapter
- техническое имя: BATCH_SERIES_171_174_HERMES_ADAPTER_FLAGS_DIAGNOSTICS_ROLLBACK_PLAN

## Серия 171-174 — План feature flags, diagnostics и rollback для Hermes adapter

Техническое имя: BATCH_SERIES_171_174_HERMES_ADAPTER_FLAGS_DIAGNOSTICS_ROLLBACK_PLAN

Статус: выполнено.

Создано:
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FLAGS_DIAGNOSTICS_ROLLBACK_PLAN.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FLAGS_DIAGNOSTICS_ROLLBACK_PLAN_SUMMARY.md

Зафиксировано:
- feature flags для будущего Hermes adapter;
- значения по умолчанию: всё новое выключено, safe mode включён;
- безопасные diagnostics без token/.env/секретов/личных данных;
- rollback через HERMES_ADAPTER_ENABLED=false и HERMES_SAFE_MODE=true;
- failure modes и fallback;
- первым этапом нельзя включать admin changes, цены, правила, базу, Vision/API, live deploy и auto-restart polling.

Следующий безопасный шаг:
- Серия 175-178 — План dry-run contract для Hermes adapter
- техническое имя: BATCH_SERIES_175_178_HERMES_ADAPTER_DRY_RUN_CONTRACT_PLAN

## Серия 175-178 — План dry-run contract для Hermes adapter

Техническое имя: BATCH_SERIES_175_178_HERMES_ADAPTER_DRY_RUN_CONTRACT_PLAN

Статус: выполнено.

Создано:
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_DRY_RUN_CONTRACT_PLAN.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_DRY_RUN_CONTRACT_PLAN_SUMMARY.md

Зафиксировано:
- dry-run adapter ничего не меняет, не отправляет сообщения, не создаёт файлы и не запускает внешние действия;
- input contract: text, user_id, current_mode, route_result, order_preview, owner_access_status, feature_flags, safe_context_summary;
- output contract: status, response_text, action, warnings, blocked_reason, suggested_next_step, export_allowed, engineer_task_draft, diagnostics, fallback_required;
- allowed/forbidden actions;
- safety validation и fallback;
- contract examples.

Следующий безопасный шаг:
- Серия 179-182 — План локального contract test для Hermes adapter
- техническое имя: BATCH_SERIES_179_182_HERMES_ADAPTER_CONTRACT_TEST_PLAN

## Серия 179-182 — План локального contract test для Hermes adapter

Техническое имя: BATCH_SERIES_179_182_HERMES_ADAPTER_CONTRACT_TEST_PLAN

Статус: выполнено.

Создано:
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_CONTRACT_TEST_PLAN.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_CONTRACT_TEST_PLAN_SUMMARY.md

Зафиксировано:
- какие локальные contract tests нужны;
- какие dry-run input/output поля проверяются;
- какие actions разрешены и какие блокируются;
- как проверяется fallback;
- как проверяются diagnostics без секретов;
- как проверяется adapter off by default;
- как проверяются feature flags;
- какие ошибки блокируют следующий этап.

Следующий безопасный шаг:
- Серия 183-186 — План fake adapter / локального test double для Hermes adapter
- техническое имя: BATCH_SERIES_183_186_HERMES_ADAPTER_FAKE_ADAPTER_TEST_DOUBLE_PLAN

## Служебный пакет — Автоперенос контекста в новый чат

Техническое имя: SERVICE_START_NEW_CHAT_PROMPT_AUTO_HANDOFF

Статус: выполнено.

Создано:
- E:\Hermes-Hub\handoff\START_NEW_CHAT_PROMPT.md

Зафиксировано:
- роль нового чата;
- активная линия Hermes adapter layer;
- последний принятый пакет 179-182;
- следующий безопасный шаг 183-186;
- запреты;
- формат ответа компактным Codex-пакетом;
- правило: после каждого принятого пакета Codex должен обновлять START_NEW_CHAT_PROMPT.md.

Следующий безопасный шаг:
- Серия 183-186 — План fake adapter / локального test double для Hermes adapter
- техническое имя: BATCH_SERIES_183_186_HERMES_ADAPTER_FAKE_ADAPTER_TEST_DOUBLE_PLAN

## Серия 183-186 — План fake adapter / локального test double для Hermes adapter

Техническое имя: BATCH_SERIES_183_186_HERMES_ADAPTER_FAKE_ADAPTER_TEST_DOUBLE_PLAN

Статус: выполнено.

Создано:
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FAKE_ADAPTER_TEST_DOUBLE_PLAN.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FAKE_ADAPTER_TEST_DOUBLE_PLAN_SUMMARY.md

Зафиксировано:
- fake adapter нужен только для локальной проверки contract tests;
- fake adapter не является live Hermes adapter;
- fake adapter не подключается к Telegram;
- fake adapter не читает token/.env/config.py;
- fake adapter не импортирует live bot modules;
- fake scenarios и fake outputs;
- side effects запрещены;
- следующий этап — реализация локального fake adapter и focused contract tests только после отдельного разрешения.

Следующий безопасный шаг:
- Серия 187-190 — Реализация локального fake adapter и focused contract tests
- техническое имя: BATCH_SERIES_187_190_HERMES_ADAPTER_FAKE_ADAPTER_TEST_DOUBLE_IMPLEMENTATION

## Update 2026-06-15 07:57:28 — BATCH_SERIES_187_190

Implemented local fake adapter / local test double for Hermes adapter contract tests.

Created:
- E:\Hermes-Hub\local_tests\hermes_adapter_fake\fake_adapter.py
- E:\Hermes-Hub\local_tests\hermes_adapter_fake\test_fake_adapter_contract.py
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FAKE_ADAPTER_IMPLEMENTATION_187_190_REPORT.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FAKE_ADAPTER_IMPLEMENTATION_187_190_SUMMARY.md

Verification:
- python -m pytest local_tests\hermes_adapter_fake -q
- 33 passed

Safety: server/live bot/token/.env/config.py/polling/webhook/Vision/API/real orders were not touched.

Next safe step:
- Series 191-194 — local contract boundary check between fake adapter and dry-run contract schema.

## Update 2026-06-15 08:03:17 — BATCH_SERIES_191_194

Added local dry-run contract boundary checks for Hermes adapter fake adapter.

Created:
- E:\Hermes-Hub\local_tests\hermes_adapter_fake\test_fake_adapter_dry_run_boundary.py
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_DRY_RUN_BOUNDARY_CHECK_191_194_REPORT.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_DRY_RUN_BOUNDARY_CHECK_191_194_SUMMARY.md

Verification:
- python -m pytest local_tests\hermes_adapter_fake -q
- 66 passed

fake_adapter.py was not changed.
Safety: server/live bot/token/.env/config.py/polling/webhook/Vision/API/real orders were not touched.

Next safe step:
- Series 195-198 — local feature flags gate check for fake adapter contract.

## Update 2026-06-15 08:11:30 — BATCH_SERIES_195_198

Added local feature flags gate checks for Hermes adapter fake adapter.

Created:
- E:\Hermes-Hub\local_tests\hermes_adapter_fake\test_fake_adapter_feature_flags_gate.py
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FEATURE_FLAGS_GATE_CHECK_195_198_REPORT.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FEATURE_FLAGS_GATE_CHECK_195_198_SUMMARY.md

Verification:
- python -m pytest local_tests\hermes_adapter_fake -q
- 99 passed

fake_adapter.py was not changed.
Safety: server/live bot/token/.env/config.py/polling/webhook/Vision/API/real orders/staging/production bot code were not touched.

Next safe step:
- Series 199-202 — local diagnostics safety check for fake adapter contract.

## Update 2026-06-15 08:22:42 — BATCH_SERIES_199_202

Added local diagnostics safety checks for Hermes adapter fake adapter.

Created:
- E:\Hermes-Hub\local_tests\hermes_adapter_fake\test_fake_adapter_diagnostics_safety.py
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_DIAGNOSTICS_SAFETY_CHECK_199_202_REPORT.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_DIAGNOSTICS_SAFETY_CHECK_199_202_SUMMARY.md

Changed:
- E:\Hermes-Hub\local_tests\hermes_adapter_fake\fake_adapter.py

Reason: diagnostics safety tests found missing unsafe markers for server paths and live log paths; only local fake adapter sensitive markers were extended.

Verification:
- python -m pytest local_tests\hermes_adapter_fake -q
- 114 passed

Safety: server/live bot/token/.env/config.py/polling/webhook/Vision/API/real orders/staging/production bot code were not touched.

Next safe step:
- Series 203-206 — local rollback/no-side-effects contract check for fake adapter.

## Update 2026-06-15 08:33:00 — BATCH_SERIES_203_206

Added local rollback/no-side-effects contract checks for Hermes adapter fake adapter.

Created:
- E:\Hermes-Hub\local_tests\hermes_adapter_fake\test_fake_adapter_rollback_no_side_effects.py
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_ROLLBACK_NO_SIDE_EFFECTS_CHECK_203_206_REPORT.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_ROLLBACK_NO_SIDE_EFFECTS_CHECK_203_206_SUMMARY.md

Verification:
- python -m pytest local_tests\hermes_adapter_fake -q
- 140 passed

fake_adapter.py was not changed.
Safety: server/live bot/token/.env/config.py/polling/webhook/Vision/API/real orders/staging/production bot code were not touched.

Next safe step:
- Series 207-210 — local final fake adapter safety baseline before server adapter boundary plan.

## Update 2026-06-15 11:32:58 — BATCH_SERIES_207_210

Added final local safety baseline checks for Hermes adapter fake adapter.

Created:
- E:\Hermes-Hub\local_tests\hermes_adapter_fake\test_fake_adapter_final_safety_baseline.py
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FINAL_FAKE_ADAPTER_SAFETY_BASELINE_207_210_REPORT.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FINAL_FAKE_ADAPTER_SAFETY_BASELINE_207_210_SUMMARY.md

Verification:
- python -m pytest local_tests\hermes_adapter_fake -q
- 166 passed

fake_adapter.py was not changed.
Safety: server/live bot/token/.env/config.py/polling/webhook/Vision/API/real orders/staging/production bot code were not touched.

Next safe step:
- Series 211-214 — plan server adapter boundary between future server adapter and existing live bot.

## Update 2026-06-15 11:44:50 — BATCH_SERIES_211_214

Created server adapter boundary plan for future Hermes adapter integration with existing live Telegram bot.

Created:
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_SERVER_BOUNDARY_PLAN_211_214.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_SERVER_BOUNDARY_PLAN_211_214_SUMMARY.md

Planning only: no code, no tests, no pytest.

Boundary summary:
- future path: Telegram -> app.py -> router.py / handlers.py -> server adapter boundary -> Hermes adapter logic -> safe core/services/orders interaction
- adapter off by default
- feature flags required
- dry-run first
- diagnostics safe-only
- no side effects
- rollback-safe fallback
- no token/env/config/server path leaks
- no production imports
- no live Telegram calls

Safety: server/live bot/token/.env/config.py/os.environ/polling/webhook/Vision/API/real orders/staging/production bot code were not touched.

Next safe step:
- Series 215-218 — plan read-only server inventory procedure.

## Update 2026-06-15 12:03:29 — BATCH_SERIES_215_218

Created read-only server inventory procedure plan for existing server Telegram bot.

Created:
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_PROCEDURE_PLAN_215_218.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_PROCEDURE_PLAN_215_218_SUMMARY.md

Planning only: no code, no tests, no pytest, no SSH/server connection.

Procedure summary:
- future inventory is read-only only
- no execution/imports/polling/webhook/subprocess/network/API calls
- token/.env/config.py/os.environ/database/log/order contents are forbidden
- sensitive zones are presence-only
- redact-by-default
- explicit approval required before any inventory run

Safety: server/live bot/token/.env/config.py/os.environ/polling/webhook/Vision/API/real orders/staging/production bot code were not touched.

Next safe step:
- Series 219-222 — plan safe inventory report template.

## 2026-06-15 — BATCH_SERIES_219_222_HERMES_ADAPTER_SAFE_INVENTORY_REPORT_TEMPLATE_PLAN

Созданы markdown-документы:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_SAFE_INVENTORY_REPORT_TEMPLATE_PLAN_219_222.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_SAFE_INVENTORY_REPORT_TEMPLATE_PLAN_219_222_SUMMARY.md

Зафиксирован шаблон будущего safe inventory report для read-only server inventory: inventory scope, approval reference, checked/not checked, presence-only structure, bot layer map by filenames only, adapter boundary points, forbidden zones, redaction confirmation, runtime/live safety, risks, questions, no-touch confirmation и next safe step.

Presence-only поля: верхнеуровневые папки, имена Python-модулей, app/router/handlers, core/service/order, config/token/env/db/log zones только как факт, adapter insertion points по именам и структуре.

Запрещённые поля: token values, .env values, config.py secret values, os.environ values, database contents, live logs contents, реальные заказы, chat/user/owner IDs, private credentials, API keys, webhook URLs, production secrets.

Redaction rules: redact-by-default, secrets-as-presence-only, secret value/private ID никогда не записывать, sensitive zones только category/presence, unknown не угадывать, unsafe finding фиксировать без значения, отчёт должен быть безопасен для ChatGPT.

No-touch: server/live Telegram/token/.env/config.py/os.environ/Vision/API/реальные заказы/code/tests не трогались. Серверная inventory не выполнялась.

Следующий безопасный шаг: Серия 223-226 — план safe server inventory approval gate.

## 2026-06-15 — BATCH_SERIES_223_226_HERMES_ADAPTER_SAFE_SERVER_INVENTORY_APPROVAL_GATE_PLAN

Созданы markdown-документы:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_SAFE_SERVER_INVENTORY_APPROVAL_GATE_PLAN_223_226.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_SAFE_SERVER_INVENTORY_APPROVAL_GATE_PLAN_223_226_SUMMARY.md

Зафиксирован approval gate для будущей read-only server inventory. Будущий запуск inventory требует отдельной явной команды пользователя, ограниченной, одноразовой и с точной областью действия.

Явное разрешение должно прямо указывать read-only server inventory, процедуру 215-218, шаблон 219-222, запрет secret values, запрет запуска кода, запрет polling/webhook и запрет изменений файлов.

Не считаются разрешением: продолжай, +, делай дальше, посмотри сервер, проверь бота и любые расплывчатые сообщения без точного указания read-only inventory и границ.

Даже после разрешения остаются запрещёнными: token values, .env values, config.py secret values, os.environ values, database contents, live logs contents, реальные заказы, chat/user/owner IDs, private credentials, API keys, webhook URLs, production secrets и любые write operations.

Stop conditions: требуется прочитать secret value, запустить код, импортировать live bot module, открыть database/log/order contents, подключиться к Telegram/API/network вне scope, изменить файл, выполнить commit/push, scope неясный или есть риск раскрытия private data.

No-touch: server/live Telegram/token/.env/config.py/os.environ/Vision/API/реальные заказы/code/tests не трогались. Server inventory не выполнялась.

Следующий безопасный шаг: Серия 227-230 — финальная сверка документов server inventory readiness.

## 2026-06-15 — BATCH_SERIES_227_230_HERMES_ADAPTER_SERVER_INVENTORY_READINESS_FINAL_CHECK

Созданы markdown-документы:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_SERVER_INVENTORY_READINESS_FINAL_CHECK_227_230.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_SERVER_INVENTORY_READINESS_FINAL_CHECK_227_230_SUMMARY.md

Проведена финальная readiness-сверка документов 215-226 перед возможным отдельным разрешением на будущую read-only server inventory.

Подтверждено:

- procedure plan 215-218 готов;
- safe inventory report template 219-222 готов;
- approval gate 223-226 готов;
- server adapter boundary context 211-214 учтён;
- future inventory read-only only;
- требуется отдельное явное разрешение пользователя;
- +, продолжай, делай дальше, посмотри сервер, проверь бота не являются разрешением;
- presence-only поля зафиксированы;
- forbidden fields зафиксированы;
- redaction rules зафиксированы;
- stop conditions зафиксированы;
- secret values/db/log/order contents/private IDs/API keys/webhook URLs/write operations остаются запрещёнными даже после разрешения;
- no execution/no imports/no polling/no webhook/no subprocess/no network/API calls/no file modifications зафиксированы.

Противоречия между documents 215-226 не найдены.

No-touch: server/live Telegram/token/.env/config.py/os.environ/Vision/API/реальные заказы/code/tests не трогались. Server inventory не выполнялась.

Следующий безопасный шаг: остановиться и ждать отдельного явного разрешения пользователя на будущую read-only server inventory. Разрешением считается только точная команда из approval gate 223-226 или эквивалент с теми же границами.

## 2026-06-15 — BATCH_SERIES_231_234_HERMES_ADAPTER_READ_ONLY_SERVER_INVENTORY_RUN

Созданы markdown-документы:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_REPORT_231_234.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_REPORT_231_234_SUMMARY.md

Пользователь дал явное разрешение, совпадающее с approval gate 223-226:

Разрешаю выполнить read-only server inventory по утверждённой процедуре 215–218 и шаблону 219–222. Без чтения secret values, без запуска кода, без polling/webhook, без изменений файлов.

Результат: inventory заблокирована до сбора presence-only данных, потому что non-interactive SSH-доступ к root@178.104.95.187 завершился ошибкой: Permission denied (publickey,password).

Server presence-only данные не собраны:

- имена серверных файлов не получены;
- имена серверных папок не получены;
- /opt/malyarka-telegram-bot не пере-проверен в этом пакете;
- potential adapter boundary points не подтверждены свежей серверной структурой.

Safety confirmation:

Secret values were not read, copied, displayed, summarized, logged, or stored. Sensitive zones are recorded only as presence/category, not content.

Не читались: token values, .env, config.py content, os.environ, database contents, live logs contents, реальные заказы, private IDs, API keys, webhook URLs.

Не запускались: Python-код, live bot modules, app/router/handlers, polling/webhook, collector, bot subprocess, Telegram/API calls.

Не менялись: server files, базы, logs, production/staging bot code, git.

Следующий безопасный шаг: уточнить безопасный read-only способ доступа или предоставить ручной presence-only список. Переход к анализу 235-238 стоит отложить до появления реального safe inventory report с server presence-only данными.

## 2026-06-15 — BATCH_SERIES_231B_234B_HERMES_ADAPTER_SAFE_SSH_ACCESS_RECOVERY_PLAN

Созданы markdown-документы:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_SAFE_SSH_ACCESS_RECOVERY_PLAN_231B_234B.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_SAFE_SSH_ACCESS_RECOVERY_PLAN_231B_234B_SUMMARY.md

Контекст: read-only inventory 231-234 была заблокирована ошибкой Permission denied (publickey,password).

Локальная диагностика:

- SSH client установлен: OpenSSH_for_Windows_9.5p2, LibreSSL 3.8.2;
- локальная .ssh зона есть;
- presence-only SSH файлы: hetzner_hermes, hetzner_hermes.pub, known_hosts, known_hosts.old;
- SSH config отсутствует;
- public key name: hetzner_hermes.pub;
- private key candidate name only: hetzner_hermes.

Вероятная причина: предыдущая команда использовала прямой target root@178.104.95.187 без SSH config alias и без явного identity file, поэтому нужный ключ мог не выбраться автоматически или server не принимает user/key combination.

No-touch: private key contents/password/passphrase/token/.env/config.py/os.environ/server files/db/log/order contents не читались. Server inventory не выполнялась. Polling/webhook не запускались. Server files не изменялись.

Следующий безопасный шаг: пользователь предоставляет безопасные SSH-метаданные без секретов (SSH user, подтверждение key file hetzner_hermes или иной alias) либо ручной presence-only список. Повторная read-only inventory — только после восстановления доступа и отдельного подтверждения.

## 2026-06-16 — BATCH_231C_234C_EXPLICIT_SSH_KEY_INVENTORY_RETRY

Созданы markdown-документы:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_REPORT_231C_234C.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_REPORT_231C_234C_SUMMARY.md

Результат: SSH-доступ с явным ключом прошёл: ssh_ok.

Presence-only inventory выполнена для /opt/malyarka-telegram-bot.

Собрано только presence-only:

- ROOT_PRESENT yes;
- top-level: .venv, MALYARKA_CURRENT_STATE.md, malyarka_ai, malyarka_core, malyarka_telegram, malyarka_vision, requirements.txt;
- Python filenames до глубины 3;
- zone presence: app.py/router.py/handlers.py/services/orders.py/config.py present; .env/orders.db/db/database/logs/log not_present at project root.

Potential adapter boundary points by filename only:

- malyarka_telegram/router.py;
- malyarka_telegram/handlers.py;
- malyarka_telegram/app.py;
- malyarka_core/adapters/telegram.py;
- malyarka_core/services/orders.py;
- malyarka_core/exports/*.

No-secret/no-run/no-write:

Secret values were not read, copied, displayed, summarized, logged, or stored. Sensitive zones are recorded only as presence/category, not content.

Не читались: .env, config.py contents, token values, os.environ, databases, logs, real orders, private IDs, API keys, webhook URLs.

Не запускались: Python code, live bot modules, app/router/handlers, polling/webhook, collector. Server files не изменялись и не создавались.

Следующий безопасный шаг: 235-238 — анализ read-only inventory report и план минимального server adapter insertion design, без реализации кода и без изменения live-бота.

## 2026-06-16 — BATCH_235_238_SERVER_ADAPTER_INSERTION_DESIGN_PLAN

Созданы markdown-документы:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_ADAPTER_INSERTION_DESIGN_PLAN_235_238.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_ADAPTER_INSERTION_DESIGN_PLAN_235_238_SUMMARY.md

Проанализирован read-only inventory report 231C-234C и server boundary plan 211-214.

Presence-only server layers:

- malyarka_telegram;
- malyarka_core;
- malyarka_core/services/orders.py;
- malyarka_core/adapters/telegram.py;
- malyarka_core/exports/*;
- malyarka_ai;
- malyarka_vision;
- .venv;
- requirements.txt.

Candidate boundary points:

- malyarka_telegram/app.py;
- malyarka_telegram/router.py;
- malyarka_telegram/handlers.py;
- malyarka_core/adapters/telegram.py;
- malyarka_core/services/orders.py.

Минимальная безопасная design-точка выбрана: malyarka_core/adapters/telegram.py.

Причина: это adapter-shaped место по имени, оно не является app.py/polling entrypoint, позволяет оставить router.py/handlers.py как будущие tiny guarded call-sites, не трогать services/orders.py первым этапом и сохранить rollback через feature flags.

Первый будущий implementation должен быть off by default и dry-run only. Нужны feature flags: HERMES_ADAPTER_ENABLED=false, HERMES_SAFE_MODE=true, HERMES_DRY_RUN_ONLY=true, HERMES_SERVER_ADAPTER_ENABLED=false, HERMES_TELEGRAM_INSERTION_ENABLED=false, HERMES_EXPORT_CALLBACKS_ENABLED=false, HERMES_ADMIN_CHANGES_ENABLED=false.

No-touch: server files не читались и не менялись; live Telegram/polling/webhook не трогались; token/.env/config.py contents/os.environ/db/log/order contents не читались; код и тесты не создавались; collector/pytest не запускались.

Следующий безопасный шаг: 239-242 — план локального server adapter skeleton без подключения к live-боту.

## 2026-06-16 — BATCH_239_242_LOCAL_SERVER_ADAPTER_SKELETON_PLAN

Созданы markdown-документы:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_SKELETON_PLAN_239_242.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_SKELETON_PLAN_239_242_SUMMARY.md

Спроектирован локальный server adapter skeleton plan. Implementation пока запрещён.

Ключевые правила skeleton:

- будущая design-точка: malyarka_core/adapters/telegram.py;
- skeleton локальный, не подключается к live-боту;
- adapter off by default;
- первый режим dry-run only;
- feature flags обязательны;
- safe mode обязателен;
- fallback к текущему flow обязателен;
- side_effects=[];
- adapter не отправляет Telegram-сообщения напрямую;
- router.py/handlers.py могут быть только будущими tiny guarded call-sites;
- app.py первым этапом не трогать;
- services/orders.py первым этапом не менять.

Запреты зафиксированы: не читать token/.env/config.py contents/os.environ/db/log/order contents; не запускать polling/webhook/live modules/collector; не менять server files/staging/production code; не писать код и тесты.

No-touch: server files/live Telegram/token/.env/config.py contents/os.environ/db/log/order contents/Vision/API/staging/production code не трогались. Код и тесты не создавались.

Следующий безопасный шаг: 243-246 — план локального server adapter contract interface без реализации кода.

## 2026-06-16 — BATCH_243_246_LOCAL_SERVER_ADAPTER_CONTRACT_INTERFACE_PLAN

Созданы markdown-документы:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_CONTRACT_INTERFACE_PLAN_243_246.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_CONTRACT_INTERFACE_PLAN_243_246_SUMMARY.md

Спроектирован локальный server adapter contract interface для будущего Hermes adapter layer.

Future target: malyarka_core/adapters/telegram.py.

Request fields:

- action;
- payload;
- dry_run;
- feature_flags;
- safe_mode;
- diagnostics.

Response fields:

- ok;
- status;
- action;
- dry_run;
- blocked;
- fallback_required;
- reason;
- output_type;
- side_effects;
- diagnostics_safe.

Зафиксировано: adapter off by default, dry-run only, safe mode required, feature flags required, fallback to current flow, blocked/fallback/error responses structured and redacted, diagnostics safe-only, side_effects=[], adapter не отправляет Telegram-сообщения напрямую.

Запреты: token/.env/config.py contents/os.environ/db/log/order contents/private IDs/API keys/webhook URLs не читать; live modules/polling/webhook не запускать; file/db/log writes, exports/admin/write actions запрещены.

No-touch: server files/live Telegram/token/.env/config.py contents/os.environ/db/log/order contents/Vision/API/staging/production code не трогались. Код и тесты не создавались.

Следующий безопасный шаг: 247-250 — план локальных contract examples для server adapter interface без реализации кода.

## 2026-06-16 — BATCH_247_250_LOCAL_SERVER_ADAPTER_CONTRACT_EXAMPLES_PLAN

Созданы markdown-документы:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_CONTRACT_EXAMPLES_PLAN_247_250.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_CONTRACT_EXAMPLES_PLAN_247_250_SUMMARY.md

Спроектированы локальные contract examples для будущего server adapter interface.

Examples:

- adapter off by default;
- safe dry-run allowed;
- export blocked;
- admin blocked;
- write blocked;
- unknown action blocked;
- malformed request;
- fallback_required=true;
- diagnostics safe-only;
- unsafe diagnostics blocked.

Для каждого example описаны request shape, expected response shape, expected status, blocked/fallback flag, side_effects=[] и почему это безопасно.

Safety rules подтверждены: no direct Telegram send; no token/env/config/os.environ reads; no db/log/order contents; no private IDs/API keys/webhook URLs; no file/db/log writes; no polling/webhook; fallback to current flow when blocked or unsafe.

No-touch: server files/live Telegram/token/.env/config.py contents/os.environ/db/log/order contents/Vision/API/staging/production code не трогались. Код и тесты не создавались.

Следующий безопасный шаг: 251-254 — план локального adapter skeleton implementation gate, без реализации кода.

## 2026-06-16 — BATCH_251_254_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_GATE_PLAN

Созданы markdown-документы:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_GATE_PLAN_251_254.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_GATE_PLAN_251_254_SUMMARY.md

Спроектирован implementation gate для будущего локального adapter skeleton.

Gate требует:

- отдельное явное разрешение пользователя;
- local-only scope;
- точный список файлов, которые можно создать/изменить;
- точный список forbidden files/zones;
- rollback plan;
- contract interface 243-246;
- contract examples 247-250;
- off by default;
- dry-run only;
- safe mode required;
- feature flags required;
- side_effects=[];
- fallback к текущему flow;
- no direct Telegram send;
- no server/live changes.

Future target: malyarka_core/adapters/telegram.py, но первый implementation должен быть local-only, не server/production/staging.

Gate decision: implementation пока не разрешён.

No-touch: server files/live Telegram/token/.env/config.py contents/os.environ/db/log/order contents/Vision/API/staging/production code не трогались. Код и тесты не создавались.

Следующий безопасный шаг: 255-258 — план первого локального adapter skeleton implementation только после отдельного разрешения.

## 2026-06-16 — BUNDLE_255_270_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_PREP

Создан task-bundle:

- E:\Hermes-Hub\task_bundles\BUNDLE_255_270_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_PREP\TASK.md
- E:\Hermes-Hub\task_bundles\BUNDLE_255_270_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_PREP\README_FOR_CODEX.md

Созданы отчёты:

- E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_ADAPTER_IMPLEMENTATION_PREP_BUNDLE_255_270_REPORT.md
- E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_ADAPTER_IMPLEMENTATION_PREP_BUNDLE_255_270_SUMMARY.md

Bundle включает крупный связанный план 255-270: первый локальный skeleton implementation plan, allowed/forbidden files, rollback, contract examples, acceptance checks, stop conditions, future test gates и порядок выполнения.

Этапы 255-270:

- 255-258: first local skeleton implementation plan;
- 259-262: local skeleton implementation after permission;
- 263-266: contract checks plan/tests after permission;
- 267-270: local acceptance and next boundary plan.

Правила: implementation не разрешён; требуется отдельное явное разрешение; local-only; off by default; dry-run only; safe mode required; feature flags required; side_effects=[]; fallback to current flow; no direct Telegram send; no server/live/staging/production changes; no secret reads.

No-touch: код не писался, tests не создавались, server/live/staging/production code не менялся, server connection не выполнялся, token/.env/config.py contents/os.environ/db/log/order contents не читались, polling/webhook/live modules не запускались, commit/push не выполнялся.

Следующий безопасный шаг: ждать отдельное явное разрешение на BATCH_255_258_FIRST_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_PLAN.
~~~
