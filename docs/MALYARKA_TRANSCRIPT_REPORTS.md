# MALYARKA_TRANSCRIPT_REPORTS

## Purpose

Malyarka transcript reports save local dry-run dialog sessions as markdown files.

They are useful for checking the future operator flow without using live Telegram or real orders.

## Safe Commands

```cmd
scripts\malyarka_transcript.cmd --script disputed
scripts\malyarka_transcript.cmd --script clean --output MALYARKA_DIALOG_TRANSCRIPT_CLEAN.md
scripts\hermes.cmd malyarka-transcript --script disputed
```

## Output

Reports are written to:

```text
05_REPORTS\MALYARKA_DIALOG_TRANSCRIPT.md
```

Each report contains:

- safety notice;
- input dry-run commands;
- per-command result table;
- confirmed rows count;
- pending disputes count;
- resolved disputes count;
- export policy status;
- blocked action list.

## Safety

Transcript reports do not:

- start Telegram;
- read tokens;
- read `.env`;
- call external APIs;
- touch real orders;
- write real export files;
- change Google Drive;
- touch old projects or archives.
