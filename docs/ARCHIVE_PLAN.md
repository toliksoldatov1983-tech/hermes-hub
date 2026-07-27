# ARCHIVE_PLAN

## Purpose

This is a safe local plan for archiving Hermes-Clean Release Candidate v2.

This file is a plan only. It does not create an archive, move files, delete files, or touch old projects.

## Archive Candidate

Archive only:

```text
C:\Users\user\Desktop\Hermes-Clean
```

Recommended output name:

```text
Hermes-Clean-RC2-2026-07-01.zip
```

Recommended output location:

```text
C:\Users\user\Desktop\Hermes-Clean-RC2-2026-07-01.zip
```

## Include

Include the whole Hermes-Clean folder:

- `00_START`
- `03_TASKS`
- `05_REPORTS`
- `docs`
- `src`
- `tests`
- `scripts`
- `tools`
- `config`
- root docs such as `README.md`, `START_HERE.md`, `AGENTS.md`

## Do Not Include

Do not include or touch:

- `[удалён] C:\Users\user\Desktop\«Гермес Клин».zip [архив]`
- `C:\Users\user\Desktop\[архив] архивный zip-файл`
- `C:\Users\user\Desktop\[удалён]`
- [удалённый проект] / Malyarka folders;
- Google Drive files;
- real orders;
- client documents;
- `.env`, tokens, keys;
- live Telegram files;
- server folders;
- old databases.

## Pre-Archive Checks

Before creating the archive, run:

```cmd
cd C:\Users\user\Desktop\Hermes-Clean
scripts\run_tests.cmd
scripts\hermes.cmd project-audit
scripts\hermes.cmd smoke
scripts\hermes.cmd tasks
```

Expected:

- tests: `278 passed`;
- project audit: `25 checks, 0 failed`;
- smoke: `23 checks, 0 failed`;
- task state: `END_OF_PIPELINE`.

## Archive Command Plan

Only after explicit user approval to create the archive, use a safe PowerShell command:

```powershell
Compress-Archive -LiteralPath "C:\Users\user\Desktop\Hermes-Clean" -DestinationPath "C:\Users\user\Desktop\Hermes-Clean-RC2-2026-07-01.zip" -Force
```

## Post-Archive Checks

After archive creation:

1. Confirm the zip file exists.
2. Record file size and modified time.
3. Do not delete Hermes-Clean.
4. Do not delete old archives.
5. Do not move the archive unless the user separately asks.

## Safety

Archive creation is not destructive, but it still writes a new file on Desktop.

Actual archive creation should wait for explicit user wording such as:

```text
создай архив Hermes-Clean
```

or

```text
разрешаю создать архив
```
