# BATCH_117 — OPERATOR DECISION PACKAGE

## Current Status

- BATCH_114: staging files created (4 files in 06_EXPORT_STAGING)
- BATCH_115: staging reviewed, real folder write plan ready
- BATCH_116: preflight package ready (source lock, dry-run mapping, risk register)

## Staging / Preflight Package Status

| Component | Status |
|-----------|--------|
| Corel TXT (demo_order_corel.txt) | ✅ Created & Verified |
| Excel XLSX (demo_order_malyarka.xlsx) | ✅ Created & Verified |
| Preview JSON | ✅ Created |
| Export Report MD | ✅ Created |
| Staging Manifest | ✅ Created |
| Operator Checklist | ✅ Created |
| Source Lock Snapshot | ✅ Ready |
| Dry-Run Mapping | ✅ Ready (3 files mapped) |
| Copy Plan (without copy) | ✅ Ready |
| Risk Register (10 risks) | ✅ Ready |

## Blocked Transition

Переход к E:\Заказы **ЗАБЛОКИРОВАН** до точной approval-фразы.

Причина: пользователь НЕ дал явное разрешение на доступ к E:\Заказы.

## What Next Approval Allows

Фраза «ОДОБРЯЮ BATCH_117 MALYARKA REAL FOLDER PREFLIGHT» разрешит:

- ТОЛЬКО controlled preflight (проверка плана без записи)
- НЕ копирование файлов в E:\Заказы
- НЕ создание папок в E:\Заказы
- НЕ overwrite / delete
- НЕ CorelDRAW / ArtCAM / Google Drive / Telegram live

## Operator Decision Options

| Вариант | Действие |
|---------|----------|
| A | Оставить в HOLD (default, безопасно) |
| B | Дать approval: ОДОБРЯЮ BATCH_117 MALYARKA REAL FOLDER PREFLIGHT |
| C | Переключиться на другую линию проекта |
