# BATCH_117 — REAL FOLDER PREFLIGHT HOLD

## HOLD Status

- **Status:** HOLD
- **Причина:** нет точной approval-фразы от пользователя
- **Требуемая фраза:** «ОДОБРЯЮ BATCH_117 MALYARKA REAL FOLDER PREFLIGHT»

## Разрешённые безопасные действия (сейчас)

- Проверка staging-файлов внутри Hermes-Clean ✅
- Чтение manifest/checklist/preflight package внутри Hermes-Clean ✅
- Обновление документации внутри Hermes-Clean ✅
- Локальные тесты (без доступа к E:\Заказы) ✅

## Запрещённые действия (сейчас)

- Чтение E:\Заказы ❌
- Проверка существования E:\Заказы ❌
- Создание папок в E:\Заказы ❌
- Копирование файлов в E:\Заказы ❌
- Overwrite / delete ❌
- CorelDRAW / ArtCAM / CNC / Google Drive ❌
- Telegram live / polling / webhook ❌
- Внешние API ❌
- Production database ❌
- Сеть / Tailscale / LAN / firewall ❌

## Когда HOLD будет снят

HOLD снимается только после того, как пользователь явно напишет точную approval-фразу отдельным сообщением.

Упоминание фразы в отчёте НЕ является approval.
