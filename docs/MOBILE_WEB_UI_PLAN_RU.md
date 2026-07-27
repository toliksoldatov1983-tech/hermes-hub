# План Mobile Web UI для Hermes-Clean

> Будущий web-интерфейс для управления Hermes-Clean со смартфона.

## Текущий статус

- Mobile Gateway готов (BATCH_094)
- Local API server работает на 127.0.0.1:8514
- 11 JSON endpoint'ов (GET + POST)
- Safe-local only

## Будущий Web UI (BATCH_095)

### Главный экран

- Заголовок: "Hermes-Clean"
- Индикатор статуса: зелёный (OK) / красный (ATTENTION)
- Кнопки быстрого доступа
- Последнее обновление

### Разделы

| Раздел | API endpoint | Описание |
|--------|-------------|----------|
| Ассистент | /api/daily-assistant | Полный снимок проекта |
| Малярка | /api/malyarka/status | Статус модуля |
| AI Provider | /api/ai-provider/status | Статус AI провайдеров |
| Проверки | /api/local-health | Здоровье проекта |
| Следующий шаг | /api/what-next | Что делать дальше |
| Dashboard | /api/dashboard | Панель управления |

### Дизайн

- Минималистичный, тёмная тема
- Оптимизирован для мобильного (max-width 480px)
- Навигация: нижняя панель с иконками
- Работает офлайн (все данные локальные)

### Технологии

- HTML5 + CSS3 + Vanilla JS
- Никаких framework'ов (низкая зависимость)
- Fetch API для запросов к localhost
- Автообновление каждые 30 секунд

### Безопасность

- Только localhost (127.0.0.1)
- Устройство должно быть в той же сети или localhost
- В будущем: Tailscale/VPN для удалённого доступа

## Будущее Android WebView приложение (BATCH_096)

```
Android Shell App
    └── WebView
        └── http://127.0.0.1:8514 (или Tailscale IP)
```

- Минимальное Android-приложение (WebView wrapper)
- Запускает локальный сервер при старте
- Показывает Web UI в WebView
- Не требует Google Play
- APK-сборка через Android Studio

## Цепочка BATCH'ей

```
BATCH_094 → Mobile Gateway + Local API (ГОТОВО)
BATCH_095 → Mobile Web UI (HTML/CSS/JS)
BATCH_096 → Android WebView Shell App
```
