# HERMES MASTER MAP LEVELS AND PROMPTS

Status: ready for Hermes.
Date: 2026-06-21.

## Rule

Hermes must build the project map by levels.

Do not jump to implementation.

## Level 1 — Inventory Sources

Goal:

Find all information sources and classify them.

Prompt for Hermes:

```text
LEVEL 1 — INVENTORY SOURCES

Read only:
E:\Hermes-Hub
E:\Hermes-General

Do not change files.
Do not read secrets, DB, logs, real orders, .git.

Create a short inventory:
- live sources;
- local code sources;
- archive sources;
- agent sources;
- sandbox sources;
- sync/state/handoff sources;
- unknown sources.

Update:
E:\Hermes-Hub\PROJECT_MASTER_MAP_MALYARKA_HERMES.md

Answer shortly in Russian.
```

## Level 2 — Separate Live / Local / Archive / Plans

Goal:

Make clear what is active and what is historical.

Output:

- live now;
- local only;
- archive only;
- plan only;
- unsafe/forbidden.

## Level 3 — Architecture Map

Goal:

Build current architecture:

```text
Telegram → parser/order flow → exports → files
Hermes Hub → agents/sandbox/docs → future work
Hermes-General → Desktop OS/memory
```

## Level 4 — Missing Blocks

Goal:

List what is missing:

- GitHub workflow;
- Obsidian workflow;
- export callback robustness;
- regression tests;
- Phase 2 retry gate;
- production/autostart decision;
- old archive review.

## Level 5 — Risks And Forbidden Zones

Goal:

Keep safety visible:

- secrets;
- DB/logs/orders;
- server runtime;
- production;
- old Malyarka;
- external API/Vision;
- git push.

## Level 6 — Future Feature Map

Goal:

Group future features:

- order card;
- prices;
- materials;
- colors/coatings;
- milling;
- salary/economics;
- warehouse;
- Obsidian memory;
- GitHub checkpoints;
- Vision later.

## Level 7 — GitHub / Obsidian Workflow

Goal:

Design how Hermes uses:

- GitHub for checkpoints;
- Obsidian for memory;
- markdown state as source of truth.

No commit/push without approval.

## Level 8 — Priorities

Goal:

Make a ranked work queue:

- now;
- next;
- later;
- blocked;
- needs user decision.

## Level 9 — Codex Batch Packets

Goal:

Create exact Codex prompts for risky work.

Hermes prepares, Codex executes.

## Level 10 — Maintenance

Goal:

After each accepted batch:

- update master map;
- update next tasks;
- update report;
- update worklog;
- keep answer short.

