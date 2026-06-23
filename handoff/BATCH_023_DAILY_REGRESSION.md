# BATCH_023 — Ежедневник + Регрессия

Дата: 2026-06-24
Для: Codex (3% лимита — всё в одном проходе)

---

## Часть 1 — Ежедневник

### 1.1 Шаблон дня в Obsidian

Создать `E:\Hermes-General\obsidian-long-memory\01_Daily\Шаблон_дня.md`:

```markdown
# {{date}}

## Заказы
| № | Размеры | Материал | Статус |
|---|---------|----------|--------|

## Заметки
- 

## Материалы / цены
- 

## Итог дня
- Площадь: 
- Сумма: 
- Заказов:
```

### 1.2 Авто-запись из бота

В handlers.py добавить функцию `save_daily_note(text: str)`. Когда пользователь говорит что-то про заказ/материал/цену — сохранять в Obsidian daily note.

### 1.3 Авто-итог дня

Cron на сервере: каждый день в 21:00 бот собирает всё за день и присылает пользователю:
- Заказы за сегодня
- Общая площадь
- Общая сумма
- Новые материалы/цены

### 1.4 Понимание с обычной речи

Hermes-чат уже понимает смысл. Добавить в system prompt:
"Если пользователь говорит о размерах — это заказ. Если о материале — запомни в каталог. Если спрашивает об итогах — собери за сегодня."

---

## Часть 2 — Регрессионные тесты

### Тест 1 — Corel Excel
```python
from malyarka_core.parsing import parse_sizes_text
from malyarka_core.exports.corel import build_corel_workbook
text = "700 500 2\n300 400 1\n800 600"
draft = parse_sizes_text(text)
wb = build_corel_workbook(draft)
# Проверить: 3 строки confirmed, лист Спорно пуст, итоги считаются
```

### Тест 2 — Малярка Файл
```python
from malyarka_core.exports.malyarka_file import build_malyarka_file
content = build_malyarka_file(draft)
# Проверить: русские заголовки, секции подтверждено/спорно
```

### Тест 3 — Спорный заказ
```python
text = "700 500 2\nabc def\n300 400 1\n8?0 600"
draft = parse_sizes_text(text)
# Проверить: 2 confirmed, 2 disputed, причины спора
```

### Тест 4 — Экономист
```python
from malyarka_core.economy import calculate_order_cost
cost = calculate_order_cost(draft)
# Проверить: cost > 0, есть итог и маржа
```

Результаты тестов записать в `E:\Hermes-Hub\reports\REGRESSION_2026-06-24.md`.

---

## Сервер

root@178.104.95.187, ключ hetzner_hermes
Путь: /opt/malyarka-telegram-bot/
Бэкап: `/opt/malyarka-telegram-bot/backups/batch_023_дата/`

## Разрешено

- Править handlers.py (save_daily_note, авто-итог)
- Создавать .md в Obsidian
- Настроить cron (21:00 daily summary)
- Запускать тесты на сервере

## Запрещено

- .env, tokens, keys
- router.py, session.py, app.py
- production-данные
- git push
