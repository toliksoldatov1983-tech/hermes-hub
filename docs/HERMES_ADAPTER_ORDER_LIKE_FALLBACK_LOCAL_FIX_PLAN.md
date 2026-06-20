# HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LOCAL_FIX_PLAN

Дата: 2026-06-20

Batch:

```text
BATCH_PHASE2_FETCH_LOCAL_ADAPTER_BOUNDARY_COPY_AND_TEST_PLAN
```

## Purpose

Plan a future local fix for Hermes adapter boundary so order-like input such as `700 x 500` always falls back to the existing Malyarka order flow.

No code is changed by this document.

## Snapshot source

Local read-only snapshot:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_snapshot\telegram.py
E:\Hermes-Hub\server_staging\adapter_boundary_snapshot\hermes_adapter.py
```

These files are not live code.

## Required rule

```text
order-like input -> fallback_required=true
```

Protected examples:

```text
700 x 500
700 500
700*500
700 x 500 x 1
```

## Future local fix shape

Future implementation should be local-first:

1. Add or reuse an order-like detector near the Hermes adapter boundary.
2. Before any generic Hermes/assistant clarification, check whether text looks like a Malyarka size/order.
3. If yes, return:

```python
{"fallback_required": True, "reason": "order_like_input"}
```

4. Ensure the call-site ignores adapter output when `fallback_required=true`.
5. Preserve `/start` and existing command routing.
6. Preserve safe generic handling for ordinary non-order questions.
7. Keep production, service, feature flag and live Telegram untouched.

## Forbidden future behavior

For order-like input the adapter must not return or trigger:

```text
What is 700 x 500 for?
Image dimensions
Canvas size
Window size
Other
```

## Likely future files for local-only work

Allowed only in a separate implementation batch:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_snapshot\telegram.py
E:\Hermes-Hub\server_staging\adapter_boundary_snapshot\hermes_adapter.py
local contract tests under E:\Hermes-Hub\local_tests
```

Server-side files are not changed by local work.

## Future acceptance

Future local fix can be accepted only if contract tests prove:

- order-like input falls back;
- inside order mode keeps existing parser behavior;
- no English clarification appears for dimensions;
- generic non-order question remains allowed where safe;
- `fallback_required=true` preserves old flow;
- side effects remain absent.

