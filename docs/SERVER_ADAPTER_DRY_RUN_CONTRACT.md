# Server Adapter Dry-Run Contract

Date: 2026-06-17 | No code

## Fields

| Field | Type | Always | Description |
|-------|------|--------|-------------|
| `adapter_mode` | str | "dry_run" | Never "live" without approval |
| `dry_run` | bool | true | Always true |
| `telegram_api_called` | bool | false | Never calls API |
| `server_called` | bool | false | Never writes to server |
| `side_effects` | list | [] | Always empty |
| `handoff_allowed` | bool | — | Can pass to Sales |
| `review_required` | bool | — | Needs manager |
| `production_ready` | bool | false | Always false |
| `block_reason` | str/null | — | Why blocked |
| `trace_id` | str | — | For debugging |
| `source` | str | "telegram" | Message source |

## Forbidden in Contract

| Field | Reason |
|-------|--------|
| token | NEVER |
| env | NEVER |
| config | NEVER |
| secrets | NEVER |
| price | NEVER |
| production path | NEVER |
