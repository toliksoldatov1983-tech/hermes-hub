# Sales + Client Intake Agent — Demo Outputs (Golden Cases)

Date: 2026-06-17
Source: demo_inputs.md (15 сценариев)

## Формат

Для каждого сценария:
- `input` — сообщение клиента
- `status` — статус Intake Card
- `ready` — ready_for_malyarka_agent?
- `manager` — manager_review_required?
- `flags` — флаги
- `response` — suggested response (первые 2 строки)

---

### Сценарий 1 — Цена без размеров

```yaml
input: "Сколько стоит покрасить фасады?"
status: needs_more_info
ready: false
manager: true
flags:
  discount_request: true
response: |
  Итоговую стоимость и возможные условия подтвердит менеджер после уточнения заказа.
```

### Сценарий 2 — Размеры без материала

```yaml
input: "1000 400 2 шт\n600 300 1 шт"
status: needs_more_info
ready: false
manager: false
flags:
  discount_request: false
response: |
  Какой материал? МДФ, дерево (массив/шпон), металл, пластик, другое?
```

### Сценарий 3 — «Фасады белые»

```yaml
input: "Нужны фасады белые"
status: needs_more_info
ready: false
manager: false
flags:
  material_question: false
response: |
  Подскажите размеры: высоту и ширину в миллиметрах. Например: 1000 400.
```

### Сценарий 4 — Фрезеровка без типа

```yaml
input: "Фрезеровка + покраска фасадов МДФ 800 500 4 шт"
status: needs_more_info
ready: false
manager: true
flags:
  technical_advice_requested: true
  manager_review_required: true
response: |
  Я передал ваш вопрос менеджеру. С вами свяжутся.
```

### Сценарий 5 — Скидка

```yaml
input: "1000 400 МДФ белый. Скидка будет если 10 штук?"
status: ready_for_review
ready: false
manager: true
flags:
  discount_request: true
response: |
  Итоговую стоимость и возможные условия подтвердит менеджер после уточнения заказа.
```

### Сценарий 6 — «Какой материал лучше?»

```yaml
input: "Что лучше для кухни — МДФ или массив?"
status: needs_more_info
ready: false
manager: true
flags:
  technical_advice_requested: true
  manager_review_required: true
response: |
  Я передал ваш вопрос менеджеру. С вами свяжутся.
```

### Сценарий 7 — Сроки

```yaml
input: "За сколько сделаете?"
status: needs_more_info
ready: false
manager: true
flags:
  manager_review_required: true
response: |
  Подскажите размеры: высоту и ширину в миллиметрах.
```

### Сценарий 8 — Неполное описание

```yaml
input: "Покрасить надо"
status: needs_more_info
ready: false
manager: false
flags:
  discount_request: false
response: |
  Подскажите размеры: высоту и ширину в миллиметрах. Например: 1000 400.
```

### Сценарий 9 — Только покраска ✅

```yaml
input: "Только покраска. Фасады уже есть. 1000 400 4 шт МДФ белый матовый"
status: ready_for_review
ready: true
manager: false
flags:
  discount_request: false
response: |
  Проверьте, пожалуйста, всё верно?
    1. 1000×400 мм, 4 шт, МДФ, белый, матовый
```

### Сценарий 10 — Переделка старых (hardened: дерево ambiguous)

```yaml
input: "Старые фасады перекрасить. Дерево. 600 400 5 шт в белый"
status: needs_more_info
ready: false
manager: false
flags:
  material_question: true
  discount_request: false
response: |
  Вы написали «дерево». Уточните: это массив, шпон или МДФ под дерево?
```

### Сценарий 11 — Под ключ

```yaml
input: "Нужны фасады под ключ. Кухня 5 фасадов. Размеры уточню."
status: needs_more_info
ready: false
manager: false
flags:
  discount_request: false
response: |
  Подскажите размеры: высоту и ширину в миллиметрах. Например: 1000 400.
```

### Сценарий 12 — Цвет без RAL

```yaml
input: "1000 400 3 шт МДФ цвет кофе с молоком"
status: ready_for_review
ready: true
manager: false
flags:
  discount_request: false
response: |
  Проверьте, пожалуйста, всё верно?
    1. 1000×400 мм, 3 шт, МДФ, кофе с молоком
```

### Сценарий 13 — «Примерно 20 штук»

```yaml
input: "Фасады МДФ белые примерно 20 штук, размеры разные"
status: needs_more_info
ready: false
manager: false
flags:
  discount_request: false
response: |
  Подскажите размеры: высоту и ширину в миллиметрах. Например: 1000 400.
```

### Сценарий 14 — «Посчитайте кухню»

```yaml
input: "Посчитайте мне кухню"
status: needs_more_info
ready: false
manager: false
flags:
  discount_request: false
response: |
  Подскажите размеры: высоту и ширину в миллиметрах. Например: 1000 400.
```

### Сценарий 15 — Все данные (hardened: дерево ambiguous)

```yaml
input: |
  1000 400 4 шт МДФ белый матовый RAL 9010
  600 300 2 шт дерево коричневый глянцевый
  Нужна грунтовка для МДФ. Поверхность готова.
  Санкт-Петербург.
status: needs_more_info
ready: false
manager: false
flags:
  material_question: true
  discount_request: false
location: Санкт-Петербург
response: |
  Вы написали «дерево». Уточните: это массив, шпон или МДФ под дерево?
```

---

## Сводка

| # | Статус | Готов | Manager | Ключевой флаг |
|---|--------|-------|---------|--------------|
| 1 | needs_more_info | ❌ | ✅ | discount_request |
| 2 | needs_more_info | ❌ | ❌ | — |
| 3 | needs_more_info | ❌ | ❌ | — |
| 4 | needs_more_info | ❌ | ✅ | technical_advice |
| 5 | ready_for_review | ❌ | ✅ | discount_request |
| 6 | needs_more_info | ❌ | ✅ | technical_advice |
| 7 | needs_more_info | ❌ | ✅ | manager_review |
| 8 | needs_more_info | ❌ | ❌ | — |
| 9 | ready_for_review | ✅ | ❌ | — |
| 10 | needs_more_info | ❌ | ❌ | material_question |
| 11 | needs_more_info | ❌ | ❌ | — |
| 12 | ready_for_review | ✅ | ❌ | — |
| 13 | needs_more_info | ❌ | ❌ | — |
| 14 | needs_more_info | ❌ | ❌ | — |
| 15 | needs_more_info | ❌ | ❌ | material_question |
