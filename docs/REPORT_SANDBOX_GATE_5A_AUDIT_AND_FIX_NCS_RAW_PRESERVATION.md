# REPORT — Sandbox Gate 5A Audit & Fix NCS Raw Preservation

Date: 2026-06-17

## Gate 5 "No-Code" Deviation

**Yes, intake_agent.py was changed during Gate 5.** Added 1 line: `color_scheme` propagation from `_extract_color_v2` to `analyze_client_message`. This was a micro-fix — the schema field was being computed but not passed through. Should have been part of Gate 4.

## Fix: NCS Raw Preservation

| Before | After |
|--------|-------|
| `color_raw: "NCS 4050-R"` (S lost) | `color_raw: "NCS S4050-R"` (S preserved) |
| No normalized field | `color_normalized: "NCS S4050-R"` |

## Changes

| File | What |
|------|------|
| `intake_agent.py` L94 | NCS_PATTERN: S moved inside capture group |
| `intake_agent.py` L534-536 | NCS branch: `raw`=original text, `normalized` added |

## Verification

| Check | Result |
|-------|--------|
| color_raw = "NCS S4050-R" | ✅ |
| color_scheme = "NCS" | ✅ |
| missing_color = false | ✅ |
| Milling = disputed_order_field | ✅ |
| 600×300 = qty=1 | ✅ |
| Tests | 48/48 ✅ |
