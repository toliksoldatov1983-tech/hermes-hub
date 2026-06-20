# Malyarka Agent — ACCEPTANCE CRITERIA

Date: 2026-06-17
Agent: Malyarka Agent (#2, `accepted`, not active)

## Критерии приёмки

Агент считается готовым когда выполняются ВСЕ условия:

---

### 1. Не выдумывать размеры

- [ ] Только явные размеры из Intake Card
- [ ] Не додумывать: «примерно 20» → не 20
- [ ] Размеры только из items[].height_mm / width_mm

### 2. Не выдумывать материал

- [ ] `material_confirmed: false` → спорная строка
- [ ] Не заменять «дерево» на «МДФ»
- [ ] Не выбирать материал за клиента

### 3. Не выдумывать цвет

- [ ] `color_structured: null` → оставить как raw
- [ ] Не изобретать RAL для «белого»
- [ ] Не менять «кофе с молоком» на «RAL 8017»

### 4. Не считать финальную цену

- [ ] Результат НЕ содержит стоимость
- [ ] `not_final_order: true` всегда
- [ ] Цены считает другой процесс (человек/менеджер)

### 5. Preliminary result не является финальным заказом

- [ ] `not_final_order: true` во всех ответах
- [ ] Статус: `preliminary_result` (не `final`)
- [ ] Требуется human review перед подтверждением

### 6. Disputed data блокирует финальное действие

- [ ] `export_blocked: true` при любых disputed строках
- [ ] `blocked_disputed_data` → нет экспорта
- [ ] Disputed строки не входят в total_area_m2

### 7. Confirmed / disputed разделяются

- [ ] `confirmed_rows` — только rows с `material_confirmed: true`
- [ ] `disputed_rows` — rows с `material_confirmed: false` или blocking flags
- [ ] Расчёт площади только по confirmed_rows

### 8. Manager flags сохраняются

- [ ] `discount_request` → передаётся в результат
- [ ] `technical_advice_requested` → передаётся
- [ ] `manager_review_required` → передаётся
- [ ] Все flags из intake сохраняются

### 9. No real orders

- [ ] Только fake/test Intake Cards
- [ ] Без live-разрешения — никогда реальные заказы
- [ ] Реальные данные не читаются

### 10. Not active без разрешения

- [ ] Статус: `accepted` (не `active`)
- [ ] Python-код не пишется без yellow approval
- [ ] Tests не запускаются без разрешения
- [ ] Результаты не отправляются клиенту

---

## Статус

```text
ACCEPTED (not active)
✅ Критерии 1-10 задокументированы
✅ Python-модуль реализован: src/malyarka_agent.py
✅ Tests: 28/28 passed (0.10s)
✅ Demo: 4/4 passed
🔒 Не active — live не подключается. Реальные заказы — только с разрешения.
```
