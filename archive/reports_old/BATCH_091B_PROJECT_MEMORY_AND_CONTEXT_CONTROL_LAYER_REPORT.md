# BATCH_091B_PROJECT_MEMORY_AND_CONTEXT_CONTROL_LAYER_REPORT

Date: 2026-07-02
Executor: Codex

## Short Result

Created a local safe-memory and context-control layer for Hermes-Clean.

This is not external memory, not a database, not cloud storage, not Google Drive, and not live Telegram. It is a small set of local markdown files that tells Hermes/Codex what to read first and what not to autoload.

## Created Memory Files

- `00_MEMORY\ACTIVE_CONTEXT.md`
- `00_MEMORY\PROJECT_MEMORY_INDEX.md`
- `00_MEMORY\CONTEXT_LOAD_POLICY.md`
- `00_MEMORY\START_NEW_HERMES_CHAT_PROMPT.md`
- `00_MEMORY\START_NEW_CODEX_CHAT_PROMPT.md`
- `00_MEMORY\COMPACT_STATE_FOR_AGENTS.md`
- `00_MEMORY\DO_NOT_AUTOLOAD.md`
- `00_MEMORY\CONTEXT_REFRESH_RULES.md`

## Updated Files

- `00_START\CURRENT_STATE.md`
- `03_TASKS\ACTIVE_BATCH.md`
- `03_TASKS\DONE.md`
- `03_TASKS\NEXT_TASK.md`
- `05_REPORTS\REPORT_TO_USER.md`
- `START_HERE.md`
- `docs\USER_RUNBOOK_RU.md`
- `scripts\check_local.cmd`

`scripts\check_local.cmd` was converted to ASCII-only console text because its previous mojibake box-drawing/Russian strings were parsed by CMD as stray commands. The check sequence was preserved.

## Minimal Context Policy

New Hermes/Codex chats should read only:

- `AGENTS.md`
- `START_HERE.md`
- `00_START\CURRENT_STATE.md`
- `03_TASKS\NEXT_TASK.md`
- `05_REPORTS\REPORT_TO_USER.md`
- `00_MEMORY\ACTIVE_CONTEXT.md`
- `00_MEMORY\COMPACT_STATE_FOR_AGENTS.md`
- `00_MEMORY\CONTEXT_LOAD_POLICY.md`

## Do Not Autoload

- all `05_REPORTS`;
- all `src`;
- all `tests`;
- old archives;
- old projects;
- Google Drive data;
- real orders;
- [удалённый проект] history;
- `E:\«Гермес Клин»`;
- `[удалён]`;
- `.env`, tokens and keys.

## Context Budget Rule

- New chat target: under 30-40% context usage.
- If above 70%: stop and diagnose autocontext.
- If 100%: do not execute a batch; first reduce context.

## Safety

- `.env` was not read.
- Tokens were not read.
- Keys were not read.
- Google Drive was not touched.
- Live Telegram was not started.
- Polling/webhook was not started.
- External APIs were not called.
- Real orders were not used.
- Archives were not touched.
- Old projects were not scanned.
- No files were deleted.
- Malyarka logic was not changed.

## Checks

Executed:

- `scripts\hermes.cmd help-local` - OK.
- `scripts\hermes.cmd app-status` - OK, enabled 6, disabled 6.
- `scripts\hermes.cmd dashboard` - OK.
- `scripts\hermes.cmd project-audit` - OK, 25 checks, 0 failed.
- `scripts\hermes.cmd smoke` - OK, 27 checks, 0 failed.
- `scripts\run_tests.cmd` - OK, 336 passed.
- `scripts\check_local.cmd` - OK after ASCII repair, all 10 standard checks passed.

Not executed:

- `scripts\check_full.cmd` - skipped because `check_local.cmd`, smoke, audit and full tests already covered this documentation-only batch; run it before BATCH_092 only if a full duplicate verification is needed.

## Next Step

`BATCH_092_MACRO_AI_PROVIDER_INTEGRATION_AND_DAILY_ASSISTANT_MODE`

Before BATCH_092, use the minimal context prompt from `00_MEMORY`.
