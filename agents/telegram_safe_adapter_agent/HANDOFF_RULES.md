# Handoff Rules

Date: 2026-06-17 | Gate 3

## When to Pass to Sales

| Condition | Action |
|-----------|--------|
| allowed=true | pass |
| text not empty | pass |
| no forbidden actions | pass |
| no unsafe patterns | pass |
| no photo-only | pass |
| no commands | pass |

## When to Block

| Condition | Action |
|-----------|--------|
| allowed=false | block |
| empty_message | block |
| unsafe_secret_like_input | block |
| forbidden_action | block |
| photo_not_supported | block |
| command_not_routed | block |

## Fields Passed

- text → Sales Agent
- source → adapter trace

## Fields NOT Passed

- token, secrets, env vars
- photo data
- commands
- admin actions

## Dry-Run Trace

All results include:
- adapter_mode, dry_run, telegram_api_called, server_called, side_effects

## Why Clean Order Reaches Corel but NOT Production

- Corel produces `not_final_export=true`
- production_ready is ALWAYS false
- Human review required before any production step

## Why Disputed Order Must NOT Reach Corel

- Disputed data → review_required
- No Corel export until disputes resolved
- export_blocked when disputed data present
