# MALYARKA_DIALOG_COMMANDS

## Purpose

This document describes local operator-style Malyarka dialog commands.

The command layer is dry-run only. It lets the user test a future Telegram-like workflow without starting Telegram.

## Commands

```text
/order <text>
/questions
/resolve-delete <dispute_id>
/resolve-all-delete
/preview
/export
/report
/reset
/help
```

## Safe Windows Commands

```cmd
scripts\malyarka_dialog.cmd --script clean
scripts\malyarka_dialog.cmd --script disputed
scripts\hermes.cmd malyarka-dialog --script disputed
```

## Safety

These commands do not:

- start live Telegram;
- read Telegram tokens;
- read `.env`;
- call external APIs;
- touch real orders;
- write export files;
- change Google Drive;
- touch old projects or archives.

## Current Scope

The commands use synthetic/manual test strings only. They are not a production parser and not a real order workflow.
