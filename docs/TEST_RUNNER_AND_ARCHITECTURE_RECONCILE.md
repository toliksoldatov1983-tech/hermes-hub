# TEST_RUNNER_AND_ARCHITECTURE_RECONCILE

## Status

BATCH_073_SAFE_LOCAL_TEST_RUNNER_AND_ARCHITECTURE_RECONCILE links the new `hermes_clean` hardening layer to the main Malyarka module through an adapter.

## Decision

Keep `src\hermes_clean` as a local compatibility hardening layer for now.

Do not move it blindly into `src\hermes_modules\malyarka`, because the two layers use different data shapes:

- `hermes_clean` works with dict-based order results and dimensions;
- `hermes_modules.malyarka` works with `item | quantity | unit` parser contracts.

## Adapter

Added:

`src\hermes_modules\malyarka\hardening_adapter.py`

It exposes:

- `get_hardening_status()`
- `validate_synthetic_order_result()`
- `build_safe_export_preview()`

## Source Policy

Allowed preview sources:

- `synthetic`
- `manual`

Blocked sources:

- `real_order`
- `archive`
- `imported`
- `google_drive`
- `unknown`

## Safety

This layer does not:

- read `.env`;
- read tokens or keys;
- call external APIs;
- touch Google Drive;
- start live Telegram;
- read real orders;
- create real Excel files.

## Next

The next safe block can deepen the adapter into a full Malyarka state/preview workflow, or keep it as a compatibility boundary and continue local docs/release work.
