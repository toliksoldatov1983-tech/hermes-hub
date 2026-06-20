# HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LIVE_PATCH_TEST_PLAN

Дата: 2026-06-20

## Purpose

Plan future post-patch verification after applying the order-like fallback guard.

This document does not run tests and does not touch the server.

## Local checks before live patch

Already passed for fix-candidate:

```text
python -m pytest server_staging\adapter_boundary_tests -q -> 10 passed
python -m py_compile fix-candidate files -> exit 0
```

## Future server-side checks after patch

Documentation only.

1. Syntax check patched `hermes_adapter.py`.
2. Confirm feature flag remains OFF.
3. Confirm production remains OFF.
4. Confirm service state.
5. If restart is approved/required, verify service returns active/running.
6. Do not run Phase 2.

## Ordinary bot sanity check

Only after separate approval, not part of this plan:

```text
/start
```

Optional safe dummy text only after approval:

```text
700 x 500
```

Expected with feature flag OFF:

- old Malyarka behavior unchanged;
- no generic English clarification;
- no production effects.

## Future Phase 2 retry

Not approved by live patch.

Phase 2 retry requires separate future approval and must verify:

- `700 x 500` outside order mode falls back to Malyarka order flow;
- `700 x 500` inside order mode confirms row `700 500 1`;
- forbidden English clarification does not appear.

## Forbidden

- reading secrets;
- enabling production;
- enabling autostart;
- running Phase 2 without separate approval;
- live Telegram test without separate approval;
- DB/log/order reads;
- git/commit/push.

