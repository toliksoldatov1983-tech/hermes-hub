# Malyarka Agent — AGENT_SPEC

Date: 2026-06-17
Status: `accepted` (not active)
Registry: `agents/AGENT_REGISTRY.md` (#2)
Position: #2 в цепочке (после Sales Intake)
Spec accepted: ✅ | Implementation: NOT started | Real orders: FORBIDDEN without permission

---

## Роль

**Malyarka Agent** — второй агент в цепочке. Принимает структурированную Intake Card от Sales Intake Agent и выполняет техническую обработку заказа.

## Цель

```text
Intake Card → парсинг размеров → расчёт площади → Order Result
```

## Входные данные

```yaml
source: Sales + Client Intake Agent
intake_card:
  client:
    name: str
    location: str
  items:
    - height_mm: int
      width_mm: int
      quantity: int
      material: str
      material_confirmed: bool
      color: str
      color_structured: str | null
      finish: str
  urgency:
    requested: str
  flags:
    discount_request: bool
    technical_advice_requested: bool
    manager_review_required: bool
```

## Выходные данные

```yaml
order_result:
  status: clean | has_disputes | empty_or_invalid
  confirmed_rows: list
  disputed_rows: list
  total_area_m2: float
  export_blocked: bool
  short_summary: str
  dispute_reasons: list
```

## Правила обработки

1. Распарсить размеры: высота × ширина × количество
2. Разделить на confirmed_rows и disputed_rows
3. Рассчитать площадь: `area_m2 = h * w * qty / 1_000_000`
4. Только confirmed_rows входят в расчёт площади
5. Если есть disputed_rows → export_blocked = true
6. Не считать стоимость
7. Не считать цены
8. Не считать LKM
9. Не считать материалы

## Что запрещено

- ❌ Работать с реальными заказами без разрешения
- ❌ Трогать сервер / live Telegram
- ❌ Читать secrets / token / .env
- ❌ Считать финальную стоимость без подтверждённых правил
- ❌ Отправлять результат клиенту без разрешения
- ❌ Принимать заказ в производство
- ❌ Додумывать спорные данные — disputed остаются disputed
- ❌ Выдавать предварительный результат как финальный заказ

## Статусы результата

| Статус | Значение |
|--------|---------|
| `needs_clarification` | Не хватает данных — вернуть Sales Intake |
| `preliminary_result` | Расчёт выполнен, но требуется human review |
| `ready_for_human_review` | Все проверки пройдены, ждать подтверждения |
| `blocked_disputed_data` | Есть спорные строки — экспорт заблокирован |

## Статус

`accepted` (not active) — спецификация принята пользователем.
Код не писать. Не активировать. Реальные заказы — только с отдельного разрешения.
