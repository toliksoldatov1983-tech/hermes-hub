# Approval Gate Registry

Date: 2026-06-20

Status: `ACTIVE`

## Used Gates

### Controlled Server Bot Start

```text
APPROVE_SERVER_BOT_CONTROLLED_START_ONCE
```

Status:

```text
USED
```

Result:

```text
Controlled start succeeded.
Telegram phone test passed.
```

## Future Gates

### Controlled Server Bot Stop

```text
APPROVE_SERVER_BOT_CONTROLLED_STOP_ONCE
```

Status:

```text
NOT USED
```

### Hermes Adapter Phase 2 Dry-Run

```text
APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE
```

Status:

```text
NOT USED
```

## Non-Approval Phrases

These do not authorize live/server actions:

```text
да
+
продолжай
делай дальше
можно
```

## Rule

Approval phrases authorize only the exact scoped action named by the phrase.

