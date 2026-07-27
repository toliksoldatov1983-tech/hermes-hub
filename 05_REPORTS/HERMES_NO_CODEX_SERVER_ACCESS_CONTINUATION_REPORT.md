# HERMES NO-CODEX SERVER ACCESS — REPORT

Дата: 2026-07-04 · Статус: **BLOCKED**

---

## Проверено

| Метод | Результат |
|-------|-----------|
| 12 SSH-комбинаций (ubuntu/root × 5 ключей) | Permission denied |
| hcloud CLI | Не установлен |
| Парольный вход | Отключён |
| SSH config | `hermes-server` → ubuntu@49.13.76.163 |

## Причина блокировки

Сервер не имеет ни одного из локальных публичных ключей в `authorized_keys`. Добавить ключ можно только:
- Через уже работающий SSH (нет)
- Через веб-панель Hetzner Cloud Console
- Через rescue mode

## Что нужно от пользователя

1. Зайти в Hetzner Cloud Console: https://console.hetzner.cloud
2. Выбрать сервер 49.13.76.163
3. Добавить публичный ключ Hermes в раздел SSH Keys:

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... (из hermes_clean_full_access_ed25519.pub)
```

После этого я подключусь сам и остановлю старый бот.

## Статус

**SERVER_PUBLIC_KEY_INSTALL_REQUIRES_PROVIDER_PANEL**
