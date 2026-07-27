# BATCH_122 — NEXT CHAIN OPTIONS

## Based on Operator Decision

### If option A (restore E:\)

```
BATCH_123_124_125_REAL_FOLDER_PREFLIGHT_PREPARE_COPY_RETRY_ON_E
→ BATCH_123: preflight retry (check E:\ availability)
→ BATCH_124: target folder preparation
→ BATCH_125: controlled copy no-overwrite
```

### If option B (user-selected root)

```
BATCH_123_124_125_REAL_FOLDER_PREFLIGHT_PREPARE_COPY_ON_USER_SELECTED_ROOT
→ BATCH_123: preflight on user-specified root
→ BATCH_124: target folder preparation
→ BATCH_125: controlled copy no-overwrite
```

### If option C (safe-local simulation)

```
BATCH_123_124_125_SAFE_LOCAL_SIMULATION_COPY_VERIFY_CLOSE
→ BATCH_123: create simulation folder + copy
→ BATCH_124: verify simulated copy
→ BATCH_125: closeout simulation
```

### If option D (HOLD)

```
BATCH_123_HOLD_AND_ARCHIVE_READY_STAGING_PACKAGE
→ BATCH_123: archive staging, close real-folder chain
```

## Default (no operator input)

Staging remains in HOLD. Real-folder chain paused.
