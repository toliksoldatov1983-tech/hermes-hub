# SSH Access Recovery — User Steps

Date: 2026-06-17

## Что проверить в Hetzner/серверной панели

1. Сервер включён и работает (IP: 49.13.76.163)
2. SSH порт 22 открыт в firewall
3. Пользователь ubuntu существует на сервере

## Что проверить на сервере

Если есть доступ через Hetzner console:
```bash
cat /home/ubuntu/.ssh/authorized_keys
```
Убедиться, что публичный ключ из `hetzner_hermes.pub` присутствует.

## Если ключ отсутствует

Добавить публичный ключ вручную:
```bash
echo "ssh-ed25519 AAAA..." >> /home/ubuntu/.ssh/authorized_keys
```

## После восстановления доступа

1. Проверить: `ssh -i ~/.ssh/hetzner_hermes ubuntu@49.13.76.163 pwd`
2. Сообщить Hermes: «SSH доступ восстановлен, продолжай SERVER_READ_ONLY_GATE_1»

## Нельзя

- ❌ Присылать private key в чат
- ❌ Отправлять содержимое .env / token
- ❌ Менять серверные файлы
