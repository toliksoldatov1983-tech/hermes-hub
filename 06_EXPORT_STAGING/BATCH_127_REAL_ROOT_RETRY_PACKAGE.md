# BATCH_127 — REAL ROOT RETRY PACKAGE

## Status

- Real-folder chain: **HOLD**
- Причина: E:\Заказы unavailable (BATCH_119)
- Safe-local simulation: **PASS** (BATCH_123/124/125)
- Copy/manifest/verification mechanics: **PROVEN**

## Future Retry

- Разрешён только при наличии валидного target root
- Hermes НЕ выбирает root автоматически
- Root должен быть явно указан пользователем или восстановлен как E:\Заказы

## Conditions

1. Target root доступен и проверен (read-only preflight)
2. Target parent folder существует
3. Copy only, no-overwrite, no-delete, no-move
4. Source staging files unchanged
5. Manifest + verification after copy
