# LOCAL_APP_RUN

## Purpose

This document describes the safe local Hermes-Clean app runner.

## Commands

Run from `C:\Users\user\Desktop\Hermes-Clean`:

```cmd
scripts\hermes.cmd status
scripts\hermes.cmd message /статус
scripts\hermes.cmd route "удали файл"
scripts\hermes.cmd safety delete
scripts\hermes.cmd malyarka-preview "пример заказа"
```

## Safety

The local app:

- does not call Gemini;
- does not call DeepSeek / DeepSig;
- does not read real tokens;
- does not start live Telegram;
- does not touch Google Drive;
- does not read real orders;
- does not import old archives.

All external integrations remain behind approval gates.
