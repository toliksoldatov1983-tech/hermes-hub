# Модель безопасности Mobile Gateway

## Текущий режим: SAFE-LOCAL

### Что включено

- Сервер слушает **только 127.0.0.1**
- Все ответы — JSON с audit_metadata
- X-Hermes-Mode: safe-local
- X-Bind-Address: 127.0.0.1
- Никаких внешних сетевых вызовов
- Никаких секретов в ответах
- Только read-only операции (кроме dry-run dialog)

### Что заблокировано

- 0.0.0.0 (весь интерфейс) — ЗАБЛОКИРОВАНО
- Внешний порт — ЗАБЛОКИРОВАНО
- Firewall — НЕ ТРОГАЕТСЯ
- Live Telegram — ЗАБЛОКИРОВАНО
- Google Drive — ЗАБЛОКИРОВАНО
- Внешние API — ЗАБЛОКИРОВАНО
- Реальные заказы — ЗАБЛОКИРОВАНО

### Endpoint'ы

| Endpoint | Метод | Доступ |
|----------|-------|--------|
| /api/status | GET | ✅ |
| /api/dashboard | GET | ✅ |
| /api/daily-report | GET | ✅ |
| /api/daily-assistant | GET | ✅ |
| /api/what-next | GET | ✅ |
| /api/local-health | GET | ✅ |
| /api/malyarka/status | GET | ✅ |
| /api/malyarka/dialog | POST | ✅ (dry-run) |
| /api/ai-provider/status | GET | ✅ |
| /api/bridge/status | GET | ✅ |
| /api/bridge/route | POST | ✅ (safe-local only) |

## Будущие уровни безопасности

### Уровень 1: Read-Only First (локально)

Сейчас активен. Только чтение, localhost.

### Уровень 2: LAN Mode (будущее)

- `APPROVE_LAN_MODE` gate
- Бинд на локальный IP (192.168.x.x)
- Доступ только из домашней сети
- Без внешнего интернета

### Уровень 3: Remote Mode (будущее)

- `APPROVE_REMOTE_ACCESS` gate
- Tailscale / WireGuard VPN
- Device token (сохранён на устройстве)
- PIN-код при запуске

### Уровень 4: Write Mode (будущее)

- `APPROVE_WRITE_MODE` gate
- Разрешение на запись (экспорт, изменение)
- Отдельный approval на каждую write-операцию

## Что НЕ делаем

- Не храним пароли в коде
- Не используем HTTP Basic Auth
- Не открываем порты на роутере
- Не делаем port forwarding
- Не публикуем в интернет
- Не используем ngrok/public URLs без VPN

## Аудит

Каждый ответ содержит:

```json
{
  "audit_metadata": {
    "mobile_gateway_version": "1.0",
    "safe_local": true,
    "bind_address": "127.0.0.1",
    "real_api_called": false,
    "env_read": false,
    "token_used": false,
    "network_called": false,
    "external_port_open": false
  }
}
```
