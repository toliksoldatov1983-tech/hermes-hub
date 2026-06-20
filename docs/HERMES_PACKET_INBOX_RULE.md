# HERMES PACKET INBOX RULE

Date: 2026-06-20

Status: active transfer rule

## Purpose

`HERMES_PACKET_INBOX` is a transfer channel for large or risky-by-size tasks.

This rule does not mean that every task must be packed into ZIP.
Codex/Hermes must first choose the transfer method by task size and risk of truncation.

## Transfer Algorithm

1. If the task is short and fits into one normal chat message without truncation risk:
   - send it as plain chat text.

2. If the task is medium-sized or there is doubt whether it will fit into the Codex/Hermes window:
   - first send a short check:

```text
Можешь принять задание объёмом примерно N символов в одном сообщении? Если нет — работаем через ZIP через HERMES_PACKET_INBOX.
```

3. If Codex/Hermes confirms that it can accept the task:
   - send the task as plain chat text.

4. If Codex/Hermes says the task is too large, risky, may not fit, or is better as a file:
   - create a ZIP package;
   - place it here:

```text
C:\Users\user\Desktop\HERMES_PACKET_INBOX\01_INBOX_ZIP
```

   - run:

```text
C:\Users\user\Desktop\HERMES_PACKET_INBOX\RUN_HERMES_PACKET_INBOX.cmd
```

   - read the task path from:

```text
C:\Users\user\Desktop\HERMES_PACKET_INBOX\LATEST_TASK_PATH.txt
```

5. If the task is clearly large in advance, do not ask again. Use ZIP immediately.

Large-in-advance examples:

- long project history;
- transfer between chats;
- large markdown;
- many files;
- many prohibitions;
- long server-work context;
- text larger than one convenient window;
- user already said the text does not fit in the window.

6. If an attempt to paste the task already failed or the window cannot accept the full text:
   - do not shorten important context;
   - do not ask the user to paste it in many parts;
   - immediately repackage it as a ZIP.

## Final Rule

Codex/Hermes first estimates the task size.

ZIP is not the default for every task. ZIP is used only when the task is large, risky by volume, or does not fit into the chat window.

Small tasks are transferred as normal chat text.

