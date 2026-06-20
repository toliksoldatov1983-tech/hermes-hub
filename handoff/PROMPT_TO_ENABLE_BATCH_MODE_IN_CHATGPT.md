# Prompt To Enable Batch Mode In ChatGPT

Paste this into the ChatGPT main chat when you want fewer back-and-forth steps.

```text
Включаем пакетный режим работы.

Не отправляй Codex микрозадачи по одному маленькому шагу.
Собирай работу в BATCH_PACKET: один понятный блок из 3-7 связанных безопасных задач.

Главные файлы:
E:\Hermes-Hub\HERMES_HUB_STATE.md
E:\Hermes-Hub\docs\BATCH_WORKFLOW.md
E:\Hermes-Hub\handoff\BATCH_PACKET_TEMPLATE.md
E:\Hermes-Hub\tasks\NEXT_TASKS.md
E:\Hermes-Hub\progress\PROGRESS_CARD.md

Формат:

BATCH_PACKET:

GOAL:

CURRENT CONTEXT:

ACCEPTED DECISIONS:

TASKS:
1.
2.
3.

WHAT CODEX MAY DO WITHOUT ASKING:

WHAT CODEX MUST NOT TOUCH:

WHAT NEEDS USER CONFIRMATION:

EXPECTED RESULT:

CHECKS:

FILES TO UPDATE:

REPORT BACK TO CHATGPT:

Важно:
- старую Малярку пока считать архивом;
- не трогать .env, orders.db, .git, токены, Telegram, Vision, API без отдельного разрешения;
- если нужна работа Codex, готовь сразу один большой BATCH_PACKET, а не несколько мелких сообщений.
```

