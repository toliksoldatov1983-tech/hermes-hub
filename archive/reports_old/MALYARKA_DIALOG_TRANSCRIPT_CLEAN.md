# MALYARKA_DIALOG_TRANSCRIPT

Generated: 2026-07-01T21:39:36

## Safety

This report is local dry-run only.

It does not start Telegram, read tokens, read `.env`, call external APIs, touch real orders, write export files, change Google Drive, or touch old projects.

## Script

- name: `clean`
- commands: `4`
- final_status: `ok`
- final_export_ready: `true`
- final_pending_disputes: `0`

## Input Commands

1. `/order 1000 400 2\n700 300`
2. `/preview`
3. `/export`
4. `/report`

## Results

| # | command | status | confirmed | pending | resolved | export_ready | message |
|---|---|---|---:|---:|---:|---|---|
| 1 | `/order` | `ok` | 2 | 0 | 0 | `true` | order received |
| 2 | `/preview` | `ok` | 2 | 0 | 0 | `true` | preview generated |
| 3 | `/export` | `ok` | 2 | 0 | 0 | `true` | export policy ready |
| 4 | `/report` | `ok` | 2 | 0 | 0 | `true` | final report generated |

## Blocked Actions

- `live_telegram_send`
- `telegram_token_read`
- `external_api_call`
- `real_order_access`
- `file_export_write`
