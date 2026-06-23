# MALYARKA CURRENT STATE

Clean runtime candidate created on 2026-06-23.

Status:

- Source base: `C:\Users\user\Desktop\malyarka_codex_work`
- Clean runtime path: `E:\Hermes-Hub\projects\malyarka-runtime-clean`
- Server runtime path: `/opt/malyarka-telegram-bot`
- Server bot status: service is active, Telegram token was revoked/replaced, fresh logs are clean
- Deployment: clean runtime is deployed to `/opt/malyarka-telegram-bot`
- Polling tuning: use Telegram short polling timeout to avoid stale long-poll conflict tails

## 16. Следующий шаг

Сделать clean runtime candidate стабильным: tests green, русские заголовки Файла Малярки закреплены тестами, Telegram polling diagnostics сохранены, серверные экспериментальные `hermes_chat.py` и `openai_vision.py` не деплоить без отдельного решения.

После этого: проверить бота вручную в Telegram и закрепить clean runtime в git, чтобы больше не возвращаться к ручному копированию `/opt/malyarka-telegram-bot`.
