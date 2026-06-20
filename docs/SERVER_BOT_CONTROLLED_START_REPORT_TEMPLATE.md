# Server Bot Controlled Start Report Template

Date: 2026-06-20

Mode: template only.

## Metadata

Technical name:

```text
SERVER_BOT_CONTROLLED_START_REPORT
```

Approval phrase received:

```text
APPROVE_SERVER_BOT_CONTROLLED_START_ONCE / not received
```

Date/time:

```text
TODO
```

Operator:

```text
TODO
```

## Precheck Result

- SSH access:
- service exists:
- pre-start service state:
- autostart state:
- entrypoint:
- working directory:
- service user:
- adapter present:
- feature flag OFF:
- no production enable:
- no secrets read:

## Start Result

- start command run:
- start result:
- post-start service state:
- process check:
- unexpected output:

## Telegram Test Result

- safe messages sent:
- expected responses:
- actual responses:
- bot stability:
- no real orders:
- no Vision/API:
- no production behavior:

## Rollback / Stop Result

- stop needed:
- stop command run:
- final service state:
- rollback notes:

## Final State

- final service state:
- final enabled/autostart state:
- final feature flag state:
- production enable:
- Phase 2:

## No-Touch Confirmations

Confirm:

- `.env` not read:
- `config.py` not read:
- token not read:
- `os.environ` not read:
- DB not read:
- logs not read:
- real orders not read:
- `.py` code not changed:
- git/commit/push not used:
- production not enabled:

## Final Decision

```text
SUCCESS / FAILED / STOPPED / ROLLBACK_PERFORMED / INCONCLUSIVE
```

## Next Step

```text
TODO
```

