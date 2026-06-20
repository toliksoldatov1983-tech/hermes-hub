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

