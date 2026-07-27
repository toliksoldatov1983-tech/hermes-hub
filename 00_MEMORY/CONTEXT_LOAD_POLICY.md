# CONTEXT_LOAD_POLICY

## Goal

Keep new Hermes/Codex chats small enough to work. Do not load the whole project just to start.

## Always Read At Startup

Read only these files at the start of a new chat:

```text
AGENTS.md
START_HERE.md
00_MEMORY\PROJECT_MEMORY_INDEX.md
00_MEMORY\USER_PROFILE.md
00_START\CURRENT_STATE.md
03_TASKS\NEXT_TASK.md
05_REPORTS\REPORT_TO_USER.md
00_MEMORY\ACTIVE_CONTEXT.md
00_MEMORY\COMPACT_STATE_FOR_AGENTS.md
00_MEMORY\CONTEXT_LOAD_POLICY.md
```

## Read Only On Request Or When Relevant

- `docs\USER_RUNBOOK_RU.md`
- `docs\AI_PROVIDER_ARCHITECTURE.md`
- one specific report from `05_REPORTS`
- one specific module from `src`
- one specific test file from `tests`
- one specific script from `scripts`

## Never Read Without Explicit Approval

- `.env`;
- tokens;
- keys;
- real order files;
- Google Drive data;
- old archives as working projects;
- old project trees;
- `[удалён]`;
- `E:\«Гермес Клин»`.
- `E:\[архив] [удалённый архив]`.

## Context Budget Rule

- A new Hermes/Codex chat should start under 30-40% context usage.
- If context usage is already above 70%, stop and diagnose what was autoloaded.
- If context usage is 100%, do not execute the batch. First reduce context.

## How To Ask For Missing Context

If more context is needed, ask for one named file or one named report.

Good:

```text
Need `05_REPORTS\BATCH_091_AI_PROVIDER_SECRET_GATE_SETUP_REPORT.md` to continue.
```

Bad:

```text
Load all reports.
Load all source.
Scan [удалённый проект].
```

## Reports Policy

Do not read all of `05_REPORTS`. Use:

- `05_REPORTS\REPORT_TO_USER.md` for latest summary;
- one specific batch report only when the current task requires it;
- `05_REPORTS\LOCAL_PROJECT_AUDIT.md` only for audit failures;
- `05_REPORTS\LOCAL_DASHBOARD.md` only for current dashboard status.

## Source Policy

Do not read all of `src`. Read only the relevant module:

- AI Provider task: `src\hermes_core\ai_provider\`
- Malyarka task: `src\hermes_modules\malyarka\`
- compatibility check: `src\hermes_clean\`
- CLI task: `src\hermes_core\cli.py` plus related command module.

## Old Project Policy

Old projects are not source of truth. `E:\[архив] [удалённый архив]` and `E:\«Гермес Клин»` must never be autoloaded or used to override Hermes-Clean. Read one historical file only for an explicitly approved comparison.

