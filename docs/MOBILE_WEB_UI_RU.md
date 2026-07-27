# Mobile Web UI — инструкция

## Как открыть

1. Запустить API сервер:
```cmd
scripts\hermes.cmd mobile-api-server-check
```

2. Открыть Web UI в браузере:
```
file:///C:/Users/user/Desktop/Hermes-Clean/web/mobile/index.html
```

Или через CLI:
```cmd
scripts\hermes.cmd mobile-web-preview
```

## Экраны

| Экран | API | Описание |
|-------|-----|----------|
| Главная | /api/dashboard | Статус, быстрые кнопки |
| Ассистент | /api/daily-assistant | Полный снимок проекта |
| Малярка | /api/malyarka/status, /api/malyarka/dialog | Разбор заказов (dry-run) |
| Статус | /api/status | Статус проекта |
| Проверки | /api/local-health, /api/dashboard | Health + smoke + audit |
| AI Provider | /api/ai-provider/status | Статус провайдеров |
| Safety | /api/bridge/status | Approval gates |
| Настройки | — | API URL, информация |

## Почему пока не Android-приложение

BATCH_095 — это только Web UI. Android WebView shell app будет в BATCH_096.

## Почему пока 127.0.0.1

Safe-local mode. LAN/external доступ отключён.
Для доступа с телефона потребуется:
1. BATCH_096 (Android WebView shell)
2. LAN mode approval
3. Или Tailscale/VPN

## Что доступно

- ✅ Просмотр статуса проекта
- ✅ Daily assistant
- ✅ Malyarka dry-run
- ✅ AI Provider статус
- ✅ Safety gates просмотр
- ❌ Live Telegram
- ❌ Google Drive
- ❌ Внешние API
- ❌ Реальные заказы

## Проверка

```cmd
scripts\hermes.cmd mobile-web-self-check
scripts\hermes.cmd mobile-web-status
scripts\hermes.cmd mobile-web-files
```
