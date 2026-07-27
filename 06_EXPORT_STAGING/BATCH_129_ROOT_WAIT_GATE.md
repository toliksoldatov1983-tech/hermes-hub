# BATCH_129 — ROOT WAIT GATE

## Status

- ROOT_READY: **НЕ предоставлен**
- Real-folder chain: **HOLD**
- Причина: E:\Заказы unavailable, альтернативный root не указан

## Правила Hermes

- Hermes НЕ выбирает root самостоятельно
- Hermes НЕ сканирует диски
- Hermes НЕ ищет реальные заказы
- E:\Заказы НЕ трогается
- Реальные заказы НЕ трогаются

## Следующий шаг

Real-chain возможен только после:
1. ROOT_READY от пользователя (точный путь)
2. Controlled preflight указанного root (не сразу copy)
