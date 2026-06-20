# HERMES_ADAPTER_ORDER_LIKE_FALLBACK_CONTRACT_TEST_PLAN

Дата: 2026-06-20

## Purpose

Plan local contract tests for the adapter boundary snapshot before any future server patch or repeat Phase 2 dry-run.

No tests are implemented by this document.

## Test source

Future tests should target a local copy, not the live server:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_snapshot\telegram.py
E:\Hermes-Hub\server_staging\adapter_boundary_snapshot\hermes_adapter.py
```

## Required tests

### 1. `700 x 500` outside order mode

Expected:

- adapter returns `fallback_required=true`, or call-site falls back to existing router;
- existing route remains "looks like order / switch to order mode";
- no English clarification.

Forbidden output:

```text
What is 700 x 500 for?
Image dimensions
Canvas size
Window size
```

### 2. `700 x 500` inside order mode

Expected:

- adapter does not replace parser;
- existing Malyarka parser confirms:

```text
700 500 1
```

### 3. `/start`

Expected:

- existing menu flow is not broken;
- no production action;
- no feature flag side effect.

### 4. `тест`

Expected:

- safe generic path or fallback;
- no production side effects;
- no Telegram send inside adapter.

### 5. Unknown generic question

Expected:

- safe generic adapter path may be allowed if the input is not order-like;
- output must stay dry-run/safe;
- no secrets, DB, logs, orders, production or API calls.

### 6. `fallback_required=true`

Expected:

- call-site ignores adapter output;
- old Telegram flow continues;
- no side effects.

### 7. English clarification guard

Expected:

- any order-like input is protected;
- response must not contain:

```text
What is 700 x 500 for?
Image dimensions
Canvas size
Window size
```

## Safety invariants

All tests must be local-only.

Forbidden in tests:

- server access;
- SSH;
- systemctl;
- feature flag changes;
- Phase 2 launch;
- production enable;
- `.env`, `config.py`, token, `os.environ`;
- DB/live logs/real orders;
- live Telegram test;
- git/commit/push.

