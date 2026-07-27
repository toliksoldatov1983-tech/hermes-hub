# RULES MIGRATION — ЧТО ПЕРЕНЕСТИ В HERMES-CLEAN

Дата: 2026-07-04 · Источник: «Гермес Клин».zip [архив] + [архив] архивный zip-файл

---

## ✅ УЖЕ ЕСТЬ в Hermes-Clean

| Правило | Где |
|---------|-----|
| Спорные строки → export blocked | `dispute_resolver.py`, `export_gate.py` |
| Галочки/помарки игнорировать | memory + `VISION_RECOGNITION_RULES.md` |
| Не додумывать цену | `PRICE_AND_LKM_FROM_GOOGLE_DRIVE.md` |
| No-overwrite export | `export_gate.py` |
| Не трогать реальные заказы | `02_PROJECTS/malyarka/real_orders_rules.md` |
| Safety rules | `secret_guard.py`, `safety/` |

---

## ❌ НЕТ в Hermes-Clean (нужно перенести)

### 1. «Не выдумывать цифры» — для размеров и распознавания

**Где:** `[удалённый архив]/docs/MALYARKA_CLEAN_PARSER_RULES.md`, строка 5:
> Disputed data must not be guessed.

И `[удалённый архив]/agents/AGENT_FACTORY_RULES.md`:
> ❌ Выдумывать цены

**Что добавить:** правило «Если цифра не распознана — не выдумывать, строка → disputed, причина → unclear_quantity / missing_width / missing_height»

### 2. Коды причин спора

**Где:** `[удалённый архив]/docs/MALYARKA_CLEAN_PARSER_RULES.md`:
```
missing_height, missing_width, too_many_numbers, unclear_quantity,
unparsed_order_text, empty_or_garbage, unsupported_format
```

**Что добавить:** эти коды в `dispute_resolver.py` + новый код `unrecognized_digit` для vision

### 3. Глобальные запреты агентов

**Где:** `[удалённый архив]/agents/AGENT_FACTORY_RULES.md`:
```
❌ Выдумывать цены
❌ Обещать сроки
❌ Принимать заказ в производство
❌ Трогать сервер
❌ Читать secrets
❌ Работать с реальными заказами без разрешения
❌ Писать клиенту автоматически
❌ Делать commit/push
```

**Что добавить:** объединить с текущими safety rules в единый `GLOBAL_RED_LINES.md`

### 4. Парсер-правила

**Где:** `[удалённый архив]/docs/MALYARKA_CLEAN_PARSER_RULES.md`:
- Первое число = высота, второе = ширина, третье = количество
- Если количество не указано = 1
- Цены/материалы/комментарии не смешивать с размерами

**Что добавить:** в `validation.py` или отдельный `PARSER_RULES.md`
