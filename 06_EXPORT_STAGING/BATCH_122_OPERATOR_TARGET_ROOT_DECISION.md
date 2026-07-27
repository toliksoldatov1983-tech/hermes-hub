# BATCH_122 — OPERATOR TARGET ROOT DECISION

E:\Заказы недоступен. Выберите вариант.

---

## Вариант A — Восстановить E:\Заказы

- Пользователь подключает / монтирует диск E:
- Затем можно повторить controlled preflight chain (BATCH_119→120→121)
- Copy всё равно только после PASS preflight

## Вариант B — Указать другой реальный root

- Пользователь явно пишет новый путь: например `D:\Заказы` или `C:\Заказы`
- Гермес НЕ выбирает путь автоматически
- После указания — новый controlled preflight для указанного root

## Вариант C — Safe-local fallback simulation

- Имитация real-folder copy внутри Hermes-Clean
- Target: `C:\Users\user\Desktop\Hermes-Clean\07_REAL_FOLDER_SIMULATION\demo_order\`
- Это НЕ реальная папка заказа
- Подходит только для проверки механики copy/manifest/verification
- Source: `06_EXPORT_STAGING\`

## Вариант D — HOLD

- Остановить real-folder chain
- Сохранить staging package как готовый
- Не делать дальнейших файловых операций

---

## Current State

- Staging files: ✅ intact in 06_EXPORT_STAGING
- BATCH_114–118: ✅ accepted
- BATCH_119: BLOCKED (E:\ unavailable)
- Tests: 822 collected, 809 pass
