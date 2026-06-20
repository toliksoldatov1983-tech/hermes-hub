# Gate 6 — Backup Location Report

Date: 2026-06-18

## Directory

```
/opt/malyarka-telegram-bot/_hermes_backups/20260618_200023/
```

## Contents

```
telegram.py  (original, before hook)
```

## Rollback Command

```bash
cp _hermes_backups/20260618_200023/telegram.py malyarka_core/adapters/telegram.py
rm malyarka_core/adapters/hermes_adapter.py
```
