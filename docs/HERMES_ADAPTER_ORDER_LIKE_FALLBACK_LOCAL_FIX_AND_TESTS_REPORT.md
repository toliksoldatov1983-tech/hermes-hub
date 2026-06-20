# HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LOCAL_FIX_AND_TESTS_REPORT

Дата: 2026-06-20

Batch:

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_LOCAL_FIX_AND_TESTS
```

Итоговый статус:

```text
ORDER_LIKE_FALLBACK_FIX_CANDIDATE_TESTS_PASSED
```

## Snapshot files used

Read-only source snapshot:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_snapshot\telegram.py
E:\Hermes-Hub\server_staging\adapter_boundary_snapshot\hermes_adapter.py
E:\Hermes-Hub\server_staging\adapter_boundary_snapshot\SNAPSHOT_MANIFEST.md
```

The original snapshot was not modified.

## Fix-candidate files created

```text
E:\Hermes-Hub\server_staging\adapter_boundary_fix_candidate\telegram.py
E:\Hermes-Hub\server_staging\adapter_boundary_fix_candidate\hermes_adapter.py
```

## Changes made in fix-candidate

Changed only:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_fix_candidate\hermes_adapter.py
```

Changes:

- added local regex-based order-like detector;
- protected dimension/order-like inputs:
  - `700 x 500`;
  - `700х500`;
  - `700 × 500`;
  - `700*500`;
  - `700 x 500 x 2`;
- order-like inputs now return:

```python
fallback_required = True
blocked = False
block_reason = "order_like_input_fallback"
```

- slash commands such as `/start` now return fallback to existing router instead of blocked command:

```python
fallback_required = True
blocked = False
block_reason = "command_fallback"
```

Unchanged:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_fix_candidate\telegram.py
```

## Contract tests added

Created:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_tests\test_order_like_fallback.py
```

Covered scenarios:

1. `700 x 500` outside order mode -> fallback, no English clarification.
2. `700 x 500` inside order mode -> fallback/parser not replaced, no English clarification.
3. `700х500` with Cyrillic `х` -> fallback.
4. `700 × 500` with multiplication sign -> fallback.
5. `700*500` -> fallback.
6. `700 x 500 x 2` -> fallback.
7. `/start` -> fallback to existing router/menu flow.
8. `тест` -> safe generic adapter path.
9. unknown generic question -> safe generic adapter path.
10. guard: order-like input cannot produce:
    - `What is 700 x 500 for?`;
    - `Image dimensions`;
    - `Canvas size`;
    - `Window size`.

## Checks run

Command:

```text
Set-Location -LiteralPath 'E:\Hermes-Hub'
python -m pytest 'server_staging\adapter_boundary_tests' -q
python -m py_compile 'server_staging\adapter_boundary_fix_candidate\hermes_adapter.py' 'server_staging\adapter_boundary_fix_candidate\telegram.py'
```

Result:

```text
10 passed in 0.03s
PYTEST_EXIT=0
PY_COMPILE_EXIT=0
```

## Can this be transferred to live adapter later?

Yes, as a fix-candidate only.

It should not be applied directly without a separate live patch batch.

Future live patch batch must:

1. prepare a minimal server patch based on the candidate;
2. backup live files;
3. apply only the reviewed guard;
4. keep feature flag OFF by default;
5. run server-side syntax/import checks without secrets;
6. perform controlled restart only if approved;
7. keep production OFF;
8. require separate controlled Phase 2 retry approval.

## Remaining blockers

Phase 2 remains blocked until the fix-candidate is reviewed and a separate live patch batch is approved.

Do not re-enable the Hermes adapter flag yet.

## No-touch confirmation

Not performed:

- server access;
- SSH;
- systemctl;
- service changes;
- live feature flag changes;
- Phase 2 launch;
- production enable;
- `.env` read;
- `config.py` read;
- token read;
- `os.environ` read;
- database read;
- live log read;
- real order read;
- live server file changes;
- live Telegram test;
- git/commit/push.

