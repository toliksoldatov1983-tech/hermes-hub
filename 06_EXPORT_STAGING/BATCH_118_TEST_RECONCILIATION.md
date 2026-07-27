# BATCH_118 — TEST RECONCILIATION

## Test Count Summary

| Метрика | Значение |
|---------|----------|
| Collected | **822** |
| Passed | **809** |
| Failed | **13** |
| Skipped | **0** |

## Failure Analysis

| Failure | Count | Zone |
|---------|-------|------|
| E2E shared-state (BATCH_106/107 regression) | 10 | Telegram E2E (unrelated) |
| CLI parser import (BATCH_109) | 2 | CLI (unrelated) |
| test_count subprocess (BATCH_114) | 1 | Test infra (unrelated) |

## Export/Staging/Safety Zone Failures

**NONE.** Ни одного failure в зонах:
- export ❌ none
- staging ❌ none
- file safety ❌ none
- path safety ❌ none
- overwrite/delete protection ❌ none
- approval gates ❌ none
- go/no-go ❌ none

## BATCH_117 Added Tests

10 tests in `test_batch_117_hold.py` — all PASS.

## Known E2E/CLI Failures (13)

Эти failures известны с BATCH_106–114 и не блокируют экспортную линию.
Они относятся к Telegram E2E shared-state и CLI parser entries.
Устранение — отдельный task, не блокирует Malyarka export.

## Verdict

**RECONCILED.** Export/staging/safety тесты — 100% PASS.
