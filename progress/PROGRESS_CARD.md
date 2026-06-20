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
