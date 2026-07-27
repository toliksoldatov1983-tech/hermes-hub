# VISION RECOGNITION RULES

Дата: 2026-07-04

## Модель

Gemini 2.5 Flash (ключ из Google AI Studio)

## Порядок распознавания

1. Принять скриншот
2. Передать в Gemini 2.5 Flash напрямую через Python API
3. Получить список строк
4. Показать пользователю В ТОМ ЖЕ ПОРЯДКЕ как на скриншоте
5. Ждать подтверждения

## Формат вывода

- Одна строка = одна позиция
- Размеры как на скриншоте (H×W — Кол-во)
- Галочки, вопросы, зачёркивания — показать но не вычислять
- Сгруппировать по типу как на скриншоте (полотна, коробки, доборка)

## Ограничения

- Макс 3 попытки на один скриншот
- При ошибке — не гадать, спросить пользователя
- Галочки и помарки игнорировать при расчёте

## Технически

```python
import requests, base64
key = open('gemini_key.txt').read().strip()
img_b64 = base64.b64encode(open('image.png','rb').read()).decode()
r = requests.post(
    f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}',
    json={'contents': [{'parts': [
        {'text': 'Read ALL handwritten numbers...'},
        {'inline_data': {'mime_type': 'image/png', 'data': img_b64}}
    ]}]})
```
