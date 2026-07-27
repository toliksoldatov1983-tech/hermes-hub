# ASSISTANT RULES — Личный задачник

## Статусы задач

- `today` — сегодня
- `tomorrow` — завтра
- `later` — позже
- `in_progress` — в работе
- `blocked` — зависло
- `done` — выполнено
- `cancelled` — отменено

## Команды (обычный язык)

| Фраза | Действие |
|-------|----------|
| «Что сегодня?» | Показать today + in_progress |
| «Что завтра?» | Показать tomorrow |
| «Что дальше?» | Первая незакрытая задача |
| «Добавь задачу: ...» | Создать → today |
| «Закрой задачу: ...» | → done |
| «Перенеси задачу ... на завтра» | today → tomorrow |
| «Покажи зависшие» | Все blocked |
| «Итоги дня» | done сегодня + переносы |

## Хранение

- `assistant/tasks/today.md`
- `assistant/tasks/tomorrow.md`
- `assistant/tasks/later.md`
- `assistant/tasks/done.md`

Формат: `- [ ] текст задачи | срок | связанный заказ`
