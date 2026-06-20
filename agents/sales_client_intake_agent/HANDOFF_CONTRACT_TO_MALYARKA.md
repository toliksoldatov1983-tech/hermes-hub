# Sales → Malyarka — HANDOFF CONTRACT

Date: 2026-06-17
From: Sales + Client Intake Agent (#1, `accepted`)
To: Malyarka Agent (#2, `accepted_as_spec`)

## Условия handoff

Передача Intake Card от Sales Agent к Malyarka Agent возможна **только** при выполнении ВСЕХ условий:

- [ ] `ready_for_malyarka_agent: true`
- [ ] `discount_request: false`
- [ ] `technical_advice_requested: false`
- [ ] `manager_review_required: false`
- [ ] `material_question: false`
- [ ] Все позиции имеют `material_confirmed: true`
- [ ] Все позиции имеют height_mm, width_mm, quantity > 0
- [ ] Все позиции имеют material и color
- [ ] Intake Card имеет статус `ready_for_review` + подтверждение клиента

## Протокол

```text
1. Sales Agent проверяет все blocking flags → все false
2. Sales Agent проверяет material_confirmed → все true
3. Sales Agent проверяет статус → ready_for_review + клиент подтвердил
4. Sales Agent формирует handoff_package (см. INTAKE_CONTRACT.md)
5. Sales Agent передаёт handoff_package → Malyarka Agent
6. Sales Agent обновляет статус Intake Card → transferred
7. Malyarka Agent принимает и начинает обработку
```

## Блокировка

Если любое условие нарушено — handoff **не выполняется**. Sales Agent:
- Оставляет статус `needs_more_info`
- При `discount_request` или `manager_review_required` — эскалирует менеджеру
- При `material_question` — запрашивает уточнение у клиента

## Статус

Локальный markdown contract. Код не писать. Handoff не активировать без разрешения.
