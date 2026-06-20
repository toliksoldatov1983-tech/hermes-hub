# Project Hints

Use these hints to make work easier and avoid repeating old mistakes.

## Active Hints

1. Always give the user a full Win+R path when sending them to a folder or file.
2. Keep old Malyarka frozen; build clean in Hermes Hub.
3. Use one source of truth: `HERMES_HUB_STATE.md`.
4. For big work, first make a task packet, then implement.
5. After every meaningful step, update state, worklog and next tasks.
6. Experiments go to `_scratch`, suspicious files go to `_quarantine`, old material goes to `_archive`.
7. Do not trust chat history as memory. Trust files.
8. Before risky actions, say what is risky and wait for explicit permission.
9. Show the user a short progress card regularly.
10. Do not accept agent output as working until it is checked.

## How To Add A Hint

User command:

```text
сохрани подсказку: ...
```

Agent should propose the exact text and ask for confirmation before adding.

