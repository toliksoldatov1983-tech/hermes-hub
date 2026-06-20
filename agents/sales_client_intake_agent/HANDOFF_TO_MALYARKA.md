# Sales + Client Intake Agent — HANDOFF TO MALYARKA

Date: 2026-06-17
Agent: Sales + Client Intake Agent (AGENT_SPEC.md)
Target: Malyarka Agent (будущий, #2 в реестре)

---

## Когда передавать

Intake Card передаётся Malyarka Agent когда:

- [x] Все размеры указаны в мм, числа > 0
- [x] Материал указан для каждой позиции
- [x] Цвет указан (RAL или описание)
- [x] Клиент подтвердил: «да», «всё верно», «ок», «подтверждаю»
- [x] Статус Intake Card: `ready_for_malyarka`
- [x] Город клиента известен

## Когда НЕ передавать

- [ ] Статус `needs_more_info` — ждать ответа клиента
- [ ] Статус `ready_for_review` — клиент ещё не подтвердил
- [ ] Статус `blocked` — нарушены SAFETY_RULES
- [ ] Статус `client_declined` — клиент ушёл

---

## Формат Handoff

```yaml
# === Handoff Package ===
handoff_id: "HO-2026-XXXX"
from_agent: "sales_client_intake_agent"
to_agent: "malyarka_agent"
timestamp: "2026-06-17T..."
intake_id: "INT-2026-0001"

# Полная Intake Card
intake_card:
  client:
    name: "Иван"
    telegram_id: "@ivan123"
    city: "Москва"
  items:
    - item_number: 1
      height_mm: 1000
      width_mm: 400
      quantity: 2
      material: "МДФ"
      surface_ready: false
      color: "RAL 9010"
      finish: "матовый"
      needs_primer: true
      notes: ""
  urgency:
    requested: "обычный"
  extra:
    special_requirements: ""
    delivery_needed: false
    packaging_needed: false

# Что Malyarka Agent должен сделать
instructions:
  - "Распарсить размеры → confirmed_rows / disputed_rows"
  - "Рассчитать площадь (area_m2 = h * w * qty / 1_000_000)"
  - "Сформировать Order Result"
  - "Показать результат клиенту (через Telegram Safe Agent)"
  - "НЕ считать стоимость"
  - "НЕ обещать сроки"
  - "НЕ отправлять в производство"
```

## После Handoff

1. Агент записывает в диалог: «Передаю заказ в расчёт. Ожидайте.»
2. Агент переводит Intake Card в статус `transferred` (внутренний)
3. Агент **не следит** за дальнейшей судьбой заказа
4. Если клиент пишет снова — агент отвечает: «Ваш заказ в расчёте. Если нужны изменения — напишите.»

## Ручной handoff (без Malyarka Agent)

Если Malyarka Agent ещё не реализован:
- Intake Card сохраняется как markdown-файл в `E:\Hermes-Hub\intake_cards\`
- Уведомление отправляется пользователю (человеку)
- Человек вручную передаёт заказ в расчёт
