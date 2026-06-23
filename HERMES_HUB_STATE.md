# Malyarka — State

Дата: 2026-06-24
Проект: Malyarka (ранее Hermes Hub)
Фаза: Phase 2 dry-run пройден, Production OFF

## Что работает

- 🤖 Telegram-бот: active, сервер 178.104.95.187
- 💬 Hermes-чат: без кнопок, авто-заказ
- 👁️ Vision: OpenAI GPT-4o-mini
- 🔄 GitHub: toliksoldatov1983-tech/hermes-hub
- 🔑 DeepSeek + OpenAI на сервере

## Что в работе

- BATCH_021: Full Core Connect (парсер → расчёт → экспорт)
- BATCH_015: Agents (Corel, File, Memory, Diagnostics)

## Структура

- `handoff/` — Codex-батчи
- `server_staging/` — код для деплоя на сервер
- `projects/malyarka-runtime-clean/` — чистый код
- `docs/` — документация
- `sync/` — состояние синхронизации

## Запреты

- .env, tokens, keys, orders.db, реальные заказы
- Phase 2 production
- git push без approval
