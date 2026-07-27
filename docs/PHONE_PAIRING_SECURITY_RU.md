# Phone Pairing Security

## Текущий режим

- **Pairing:** DRY-RUN ONLY (mock, без реальных токенов)
- **Real token:** НЕ создаётся
- **Real device:** НЕ привязан
- **Real connection:** НЕ установлен

## Pairing Contract

```json
{
  "device_id": "dry-run-device-001",
  "device_name": "Dry-Run Phone",
  "pairing_mode": "dry-run",
  "connection_status": "disconnected",
  "tier": "localhost_only",
  "api_base_url": "http://127.0.0.1:8514",
  "is_real": false,
  "is_dry_run": true,
  "audit_metadata": {
    "real_token": false,
    "real_connection": false,
    "safe_local": true
  }
}
```

## Будущие уровни pairing

1. **DRY-RUN** (сейчас) — mock, без реальных данных
2. **DEVICE_ID** — уникальный ID устройства
3. **TOKEN** — одноразовый токен привязки
4. **PIN** — подтверждение на обоих устройствах
5. **QR** — сканирование QR-кода с экрана ПК

## Что запрещено

- Сохранение токенов в открытом виде
- Передача токенов по HTTP (нужен HTTPS для реального pairing)
- Автоматическое pairing без подтверждения
- Pairing по публичному IP
