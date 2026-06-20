# Sales + Client Intake Agent — INTAKE CARD TEMPLATE

Date: 2026-06-17
Agent: Sales + Client Intake Agent (AGENT_SPEC.md)

## Intake Card

После сбора всей информации от клиента агент заполняет эту карточку.

```yaml
# === Intake Card ===
intake_id: "INT-2026-XXXX"       # авто-генерируется
created_at: "2026-06-17T..."     # timestamp создания
status: "ready_for_review"       # needs_more_info | ready_for_review | ready_for_malyarka | client_declined | blocked

# === Клиент ===
client:
  name: "Иван"                   # имя клиента
  telegram_id: "@ivan123"        # или None для ручного ввода
  city: "Москва"                 # город

# === Изделия ===
items:
  - item_number: 1
    height_mm: 1000              # высота в мм
    width_mm: 400                # ширина в мм
    quantity: 2                  # количество
    material: "МДФ"              # дерево, МДФ, металл, пластик, другое
    surface_ready: false         # поверхность подготовлена?
    color: "RAL 9010"            # цвет (RAL или описание)
    finish: "матовый"            # матовый/глянцевый
    needs_primer: true           # нужна грунтовка?
    notes: ""                    # особые заметки

  - item_number: 2
    height_mm: 600
    width_mm: 300
    quantity: 1
    material: "МДФ"
    surface_ready: true
    color: "RAL 9010"
    finish: "матовый"
    needs_primer: false
    notes: ""

# === Срочность ===
urgency:
  requested: "обычный"           # обычный | срочно | очень срочно
  deadline_requested: ""         # что сказал клиент (без обещаний)

# === Дополнительно ===
extra:
  special_requirements: ""       # особые требования
  delivery_needed: false         # нужна доставка?
  packaging_needed: false        # нужна упаковка?
  notes: ""                      # любые заметки агента

# === Флаги эскалации ===
flags:
  material_question: false        # клиент задал вопрос по материалу, требующий уточнения
  technical_advice_requested: false  # клиент просит техническую рекомендацию → менеджеру
  discount_request: false         # клиент просит скидку → зафиксировано, менеджеру
  manager_review_required: false  # Intake Card требует внимания менеджера перед расчётом

# === История диалога ===
dialogue:
  messages_received: 5           # сколько сообщений от клиента
  questions_asked: 3             # сколько вопросов задал агент
  raw_summary: "Клиент прислал список размеров..."  # краткое саммари
```

## Пример заполнения

### Сообщение клиента:
```
1000 400 2 шт МДФ белый матовый
600 300 дерево коричневый глянцевый
```

### Intake Card после обработки:

```yaml
intake_id: "INT-2026-0001"
status: "ready_for_review"
client:
  name: "Иван"
  telegram_id: "@ivan123"
  city: "Москва"                # спросили
items:
  - item_number: 1
    height_mm: 1000
    width_mm: 400
    quantity: 2
    material: "МДФ"
    surface_ready: false         # спросили
    color: "белый"               # уточнили: RAL 9010
    finish: "матовый"
    needs_primer: true           # спросили
  - item_number: 2
    height_mm: 600
    width_mm: 300
    quantity: 1
    material: "дерево"
    surface_ready: true          # клиент сказал «уже шлифованное»
    color: "коричневый"
    finish: "глянцевый"
    needs_primer: false
urgency:
  requested: "обычный"
extra:
  delivery_needed: false
  packaging_needed: false
flags:
  material_question: false
  technical_advice_requested: false
  discount_request: false
  manager_review_required: false
dialogue:
  messages_received: 7
  questions_asked: 4
  raw_summary: "Клиент прислал 2 позиции. Уточнили материал, грунтовку, цвет RAL, город."
```

## Проверка перед handoff

Перед передачей Malyarka Agent проверить:
- [ ] Все размеры в мм, целые числа > 0
- [ ] Материал указан для каждой позиции
- [ ] Цвет указан (RAL или описание)
- [ ] Клиент подтвердил карточку («да», «всё верно», «ок»)
- [ ] Статус: `ready_for_malyarka`
- [ ] Если `manager_review_required: true` — передать менеджеру ДО расчёта
- [ ] Если `technical_advice_requested: true` — менеджер должен ответить клиенту
