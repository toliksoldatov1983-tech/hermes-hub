# Memory Agent — Read Workflow

Date: 2026-06-17 | Status: `accepted`, not active

## Query Priority

```text
1. STATE.md → current facts (highest trust)
2. INDEX.md → project map
3. REPORTS → recent outcomes
4. WORKLOG.md → action history
5. Chat → session context (medium trust)
6. Archive → old records (lowest trust)
```

## Read Rules

- Secrets: NEVER
- Real orders: NEVER without approval
- Disputed: mark as `confidence: disputed`
- Source: always record where data came from
