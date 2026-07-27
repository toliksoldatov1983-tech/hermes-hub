# MALYARKA_DIALOG_TRANSCRIPT

Generated: 2026-07-02T03:12:34

## Safety

This report is local dry-run only.

It does not start Telegram, read tokens, read `.env`, call external APIs, touch real orders, write export files, change Google Drive, or touch old projects.

## Script

- name: `clean`
- commands: `4`
- final_status: `ok`
- final_export_ready: `true`
- final_pending_disputes: `0`

- main_module: `hermes_modules.malyarka`

## Input Commands

1. `/order paint | 2 | bucket\nroller | 3 | piece`
2. `/preview`
3. `/export`
4. `/report`

## Results

| # | command | status | confirmed | pending | resolved | export_ready | message |
|---|---|---|---:|---:|---:|---|---|
| 1 | `/order` | `ok` | 2 | 0 | 0 | `true` | Заказ принят. Спорных строк нет. |
| 2 | `/preview` | `ok` | 2 | 0 | 0 | `true` | Preview: confirmed=2; disputed=0; final_ready=True. |
| 3 | `/export` | `ok` | 2 | 0 | 0 | `true` | READY: export contract can proceed in a future approved block. |
| 4 | `/report` | `ok` | 2 | 0 | 0 | `true` | Итог: confirmed=2; disputed=0; export=READY: export contract can proceed in a future approved block. |

## Blocked Actions

- `live_telegram_send`
- `telegram_token_read`
- `external_api_call`
- `real_order_access`
- `file_export_write`
