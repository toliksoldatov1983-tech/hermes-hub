# Codex Task Queue — When Available

Date: 2026-06-17 | DO NOT execute

| # | Task | Gate | Prerequisite |
|---|------|------|-------------|
| 1 | Server Read-Only Gate 1 | RED | SSH restored |
| 2 | Server Safe File Review | RED/YELLOW | Gate 1 passed |
| 3 | Adapter insertion dry-run plan | YELLOW | Gate 2 passed |
| 4 | Server-side no-code patch plan | YELLOW | Gate 3 passed |
| 5 | Staging patch plan (no apply) | YELLOW | Gate 4 passed |
| 6 | Feature flag implementation | YELLOW | Gate 5 passed |
| 7 | Controlled dry-run test | YELLOW | Gate 7 passed |
| 8 | Production approval | RED | All gates |

## Rule

No Codex calls until explicitly approved. No live/server changes without gate.
