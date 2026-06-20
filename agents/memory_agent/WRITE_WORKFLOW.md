# Memory Agent — WRITE WORKFLOW

Date: 2026-06-17 | Status: `accepted`, not active

## Write Rules

1. Source priority: STATE/INDEX/REPORTS > chat > archive
2. Mark all entries: source, confidence, timestamp
3. Never save disputed as confirmed
4. Never read secrets
5. Never read real orders

## Entry Format

```yaml
- source: "HERMES_HUB_STATE.md"
  confidence: "confirmed"
  timestamp: "2026-06-17T..."
  summary: "Agent #1 accepted, 48/48"
  not_secret: true
```
