# TELEGRAM_ROUTE_MAP_BEFORE_CLEANUP

Date: 2026-07-03

Scope: Hermes-Clean / Malyarka Telegram production single-user routing cleanup.

## Live Process Snapshot

- Active gateway-like process found: `hermes gateway run`.
- Process chain:
  - PID 20840: `bash.exe -lic "set +m; hermes gateway run 2>&1"`
  - PID 12188: child `bash.exe`
  - PID 10024: child `bash.exe`
  - PID 17796: `hermes.exe gateway run`
  - PID 17256: `python.exe ... hermes.exe gateway run`
  - PID 10100: `python.exe ... hermes.exe gateway run`
- No separate `malyarka_telegram/app.py --run-polling` or `bot.py` polling process was visible in the Windows process list.
- Working directory for the running gateway was not reliably available from WMI without attaching to/restarting the process.

## Routes Found

| Route | File | Function / class | Phrases caught | Active before cleanup | Priority before cleanup | Risk for Hermes-Clean |
|---|---|---|---|---|---:|---|
| owner/auth check | `[удалённый архив]` | `build_live_text_response` / owner guard | all incoming Telegram text | active | 1 | low, required |
| hard safety gate | `malyarka_hermes\safety.py` + `malyarka_telegram\handlers.py` | `is_dangerous_text`, `dangerous_response`, `build_text_response` | `.env`, token, delete/remove, git, DB, Vision-like unsafe phrases | partially active | 2 | medium: handler path missed some free-chat cases before cleanup |
| status handler | `malyarka_telegram\router.py` | legacy intent path via `_route_neutral_text` | project/status-like phrases | active | after generic intent | high: `"Покажи статус"` could become old project fallback |
| next-step handler | `malyarka_telegram\router.py` | legacy intent path / task fallback | `"Что дальше?"`, task/project text | active | after generic intent | medium: could return old project fallback |
| order intake | `malyarka_telegram\handlers.py` + `malyarka_core\adapters\telegram.py` | `_looks_like_order`, `build_order_preview_from_text` | size lines such as `1000*400`; inline order phrases were weak | active | after free chat in one path | medium: `"Есть заказ: ... 720x400 2 шт"` needed explicit inline extraction |
| correction mode | not a dedicated old route | old fallback/free text | `"Исправь"`, `"Не так"`, `"Я имел в виду"`, `"Запомни"` | inactive/diffuse | n/a | medium: could be swallowed by generic fallback |
| price draft | not a dedicated old route | old fallback/free text | `"Поставь цену..."` | inactive/diffuse | n/a | medium: could be swallowed by generic fallback |
| LKM draft | not a dedicated old route | old fallback/free text | `PGP301`, `ЛКМ`, `г/м²`, `расход` | inactive/diffuse | n/a | medium: could be swallowed by generic fallback |
| backup request | not a dedicated old route | old fallback/free text | `"Сделай backup"`, `"бэкап"`, `"резерв..."` | inactive/diffuse | n/a | medium: needed safe acknowledgement only |
| generic assistant fallback | `malyarka_telegram\handlers.py` + `malyarka_telegram\general_ai.py` | `handle_text_message_with_router`, `answer_general_ai` | unknown free text | active | before router in some neutral/order cases | high: could intercept Hermes-Clean phrases before direct intents |
| old task/project fallback | `malyarka_telegram\router.py` | `_route_neutral_text`, `suggest_engineer_mode` | task/project/status-like phrases | active | before cleanup could answer status-like text | high: source of old text `"Понял, это вопрос по задачам или проекту..."` |
| legacy commands/help/status | `malyarka_telegram\handlers.py` | `build_text_response`, command sets | `/start`, `/help`, `статус`, stop/help/order format commands | active | local legacy path | medium: direct Hermes-Clean status needed to run before this on live router path |

## Required Priority After Cleanup

1. owner chat_id check
2. hard safety gates:
   - delete forbidden
   - overwrite forbidden
   - Vision disabled
   - Drive disabled
   - git push disabled
   - access changes forbidden
3. Hermes-Clean direct intents:
   - status
   - next step
   - order intake
   - correction mode
   - price draft
   - LKM draft
   - backup request
4. legacy routes only when no Hermes-Clean direct intent matched
5. generic assistant fallback last

## Legacy Interceptors

- `malyarka_telegram\handlers.py::handle_text_message_with_router` tried `answer_free_text()` before router matching for neutral/order text.
- `malyarka_telegram\router.py::_route_neutral_text` contained the old task/project fallback text.
- `malyarka_telegram\general_ai.py::answer_general_ai` remained the final generic fallback.

## Cleanup Disposition

- No files were deleted.
- Legacy fallback code was not removed.
- Hermes-Clean direct intents were inserted before free chat and before generic router fallback.
- Dangerous phrases were moved ahead of free chat/general fallback in the live handler path.
