# README For Codex — Bundle 255-270

This bundle prepares the next Hermes adapter block.

Do not implement code from this bundle unless the user gives separate explicit permission.

## Active Line

Safe connection of the existing server Telegram bot to Hermes Hub through a Hermes adapter layer.

## Current State

Planning completed:

- read-only inventory succeeded with explicit SSH key;
- minimal insertion design point is `malyarka_core/adapters/telegram.py`;
- local skeleton plan exists;
- contract interface exists;
- contract examples exist;
- implementation gate exists.

## Bundle Location

```text
E:\Hermes-Hub\task_bundles\BUNDLE_255_270_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_PREP
```

## Main Task File

```text
TASK.md
```

## Most Important Rules

- local-only;
- off by default;
- dry-run only;
- safe mode required;
- feature flags required;
- `side_effects=[]`;
- fallback to current flow;
- no direct Telegram send;
- no server/live changes;
- no secret reads.

## Do Not Touch

```text
server files
live Telegram
polling/webhook
token
.env
config.py contents
os.environ
databases
logs
real orders
staging/production code
Vision/API
.git
commit/push
```

## Future Local Files

Only after explicit permission, future implementation may create local files such as:

```text
E:\Hermes-Hub\local_tests\server_adapter_skeleton\server_adapter_skeleton.py
E:\Hermes-Hub\local_tests\server_adapter_skeleton\README.md
```

Tests require separate explicit approval if not included by the user's next package.

## Required Contract

Request:

```text
action, payload, dry_run, feature_flags, safe_mode, diagnostics
```

Response:

```text
ok, status, action, dry_run, blocked, fallback_required, reason, output_type, side_effects, diagnostics_safe
```

## Required Examples

The future skeleton must preserve:

- adapter off by default;
- safe dry-run allowed;
- export blocked;
- admin blocked;
- write blocked;
- unknown action blocked;
- malformed request;
- `fallback_required=true`;
- diagnostics safe-only;
- unsafe diagnostics blocked.

## Next Safe Step

Ask for or wait for separate explicit permission for the first local adapter skeleton implementation plan.

Suggested next package:

```text
BATCH_255_258_FIRST_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_PLAN
```
