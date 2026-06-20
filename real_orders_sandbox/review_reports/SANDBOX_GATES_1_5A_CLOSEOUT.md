# Sandbox Gates 1-5A Closeout

Date: 2026-06-17

## All Gates

| Gate | Action | Result |
|------|--------|--------|
| 1 | Zone created | ✅ 9 docs, 3 folders |
| 2 | Clean safe copy (001) | ✅ FULL CHAIN PASS |
| 3 | Disputed safe copy (002) | ✅ blocked (wrong reasons) |
| 4 | intake_agent.py fix | ✅ 48/48 |
| 5 | Recheck after fix | ✅ blocked (right reasons) |
| 5A | NCS raw preservation | ✅ "NCS S4050-R" saved |

## Final Regression

```text
118/118 tests passed (0.22s)
Sales: 48 | Malyarka: 28 | Corel: 18 | Integration: 24
```

## Verified

- Clean data → full chain works
- Disputed data → correctly blocked
- NCS → raw preserved, scheme=NCS
- Milling → disputed_order_field
- 600×300 → qty=1
- All results not_final/review_required
- Zero real folder access

## Sandbox CLOSED ✅
