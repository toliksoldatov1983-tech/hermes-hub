# LOCAL_SMOKE_TEST

Use this command from `C:\Users\user\Desktop\Hermes-Clean`:

```cmd
scripts\hermes.cmd smoke
```

## What it checks

- `start-summary`
- `health`
- `reports`
- `tasks`
- `memory`
- `help-local`
- Telegram `message` dry-run
- `malyarka-preview` contract
- disabled Gemini provider gate
- disabled DeepSeek review gate
- `safety delete`

## Safety

The smoke test runs only local contracts. It does not call external APIs, does not read Google Drive, does not read old archives, does not read secrets and does not touch real orders.
