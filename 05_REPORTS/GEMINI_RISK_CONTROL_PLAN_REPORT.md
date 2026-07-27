# BATCH_055_SAFE_LOCAL_GEMINI_RISK_CONTROL_PLAN

## Статус

Выполнено.

## Что добавлено

- `docs\GEMINI_RISK_CONTROL_PLAN.md`
- секция Gemini в `03_TASKS\PENDING_APPROVALS.md`

## Главные правила

- Gemini не подключён.
- Реальные ключи не читались.
- Реальный `.env` не создавался.
- API Gemini не запускался.
- Данные наружу не отправлялись.

## Требуемый gate

- `APPROVE_SECRET_SETUP`

## Безопасность

Не читались и не менялись:

- `.env`;
- токены;
- ключи;
- реальные заказы;
- клиентские документы;
- Google Drive;
- старые архивы;
- live Telegram.

## Проверки

- `scripts\hermes.cmd ai-provider --mode gemini-disabled` — OK, blocked.
- `scripts\hermes.cmd ai-provider --mode gemini` — OK, blocked без `APPROVE_SECRET_SETUP`.
- `scripts\hermes.cmd project-audit` — OK, 14 checks.
- `scripts\hermes.cmd smoke` — OK, 20 проверок.
- `scripts\run_tests.cmd` — OK, 104 теста.
