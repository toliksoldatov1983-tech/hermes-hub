# BATCH_012 — Regression Tests: Corel Excel + Малярка Файл

Дата: 2026-06-24
Для: Codex

## Цель

После перехода на новый конвейер (BATCH_021) проверить что экспорт работает правильно.

## Тест 1 — Corel Excel

На сервере выполнить:
```python
from malyarka_core.parsing import parse_sizes_text
from malyarka_core.exports.corel import build_corel_workbook

text = """700 500 2
300 400 1
800 600"""
draft = parse_sizes_text(text)
wb = build_corel_workbook(draft)
```

Проверить:
- Workbook создан
- Лист «Подтверждено»: 3 строки, колонки высота/ширина/количество/площадь
- Лист «Спорно»: 0 строк (все чистые)
- Итого: площадь суммируется правильно

## Тест 2 — Малярка Файл

```python
from malyarka_core.exports.malyarka_file import build_malyarka_file

text = """700 500 2
300 400 1
800x600"""
draft = parse_sizes_text(text)
content = build_malyarka_file(draft)
```

Проверить:
- Секция «подтверждено» с размерами
- Секция «итого подтверждено» с площадью и количеством
- Русские заголовки

## Тест 3 — Спорный заказ

```python
text = """700 500 2
abc def
300 400 1
8?0 600"""
draft = parse_sizes_text(text)
```

Проверить:
- confirmed: 2 строки
- disputed: 2 строки (abc def и 8?0 600)
- Причины спора указаны

## Как выполнять

1. SSH: root@178.104.95.187, ключ hetzner_hermes
2. cd /opt/malyarka-telegram-bot
3. .venv/bin/python -c "..." — каждый тест
4. Результат записать в отчёт

## Результат

Создать `E:\Hermes-Hub\reports\REGRESSION_TEST_2026-06-24.md` с выводами всех трёх тестов.
