# Codex To Hermes

Date: 2026-06-20

## Current Message

Codex confirmed:

- controlled start completed by explicit approval;
- post-start stabilization docs created;
- Telegram phone test passed;
- service currently active/running;
- autostart disabled;
- Hermes adapter feature flag OFF;
- production OFF;
- Phase 2 OFF.

## Hermes Micro Checks

Hermes may do micro runtime checks only if they are safe and read-only.

Allowed examples:

- check service active/running;
- check feature flag OFF;
- check docs updated;
- summarize blocker;
- prepare short ChatGPT status.

## Hard Limits

Hermes must not:

- start/restart/stop/enable service without approval;
- change feature flag;
- run Phase 2;
- enable production;
- read `.env`, `config.py`, token, `os.environ`, DB, logs or real orders;
- modify `.py` code;
- use git/commit/push.

Hermes should read current status from:

```text
E:\Hermes-Hub\sync\SHARED_CURRENT_STATUS.md
```

