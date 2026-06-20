# REPORT — Server Adapter Gate 3: Dry-Run Patch Plan

Date: 2026-06-17 | Status: ✅ COMPLETE

## Created — 8 docs

| Doc | Content |
|-----|---------|
| `SERVER_ADAPTER_GATE_3_DRY_RUN_PATCH_PLAN_NO_CODE.md` | No-code integration plan |
| `SERVER_HERMES_ADAPTER_PROPOSED_CONTRACT.md` | Input/output contract |
| `SERVER_TELEGRAM_ADAPTER_HOOK_PLAN.md` | Hook location + feature flag |
| `SERVER_DRY_RUN_FEATURE_FLAG_PLAN.md` | 2 flags, off-by-default |
| `SERVER_GATE_4_PATCH_PLAN_INPUTS.md` | Gate 4 candidate files |
| `SERVER_ADAPTER_TEST_PLAN_NO_CODE.md` | 11 future tests |
| `TEMP_ROOT_KEY_REMOVAL_PLAN_AFTER_SERVER_GATES.md` | Key removal (not yet) |
| `REPORT_SERVER_ADAPTER_GATE_3_DRY_RUN_PATCH_PLAN_NO_CODE.md` | This doc |

## Key Design

- New file: `malyarka_core/adapters/hermes_adapter.py`
- Hook: `adapters/telegram.py::build_order_preview_from_text`
- Flag: `_HERMES_ADAPTER_ENABLED = False` (off by default)
- No code written, no patch created

## Next

`SERVER_ADAPTER_GATE_4_ROLLBACK_BACKUP_PLAN_OR_PATCH_PLAN_WITHOUT_APPLY` (YELLOW)
