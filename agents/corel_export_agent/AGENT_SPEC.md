# Corel Export Agent — AGENT_SPEC

Date: 2026-06-17
Status: `accepted` (not active)
Registry: `agents/AGENT_REGISTRY.md` (#3)
Position: #3 в цепочке (после Malyarka Agent)
Export contract spec only | Corel: NOT launching | Real files: NOT creating

---

## Роль

**Corel Export Agent** — третий агент в цепочке. Принимает Order Result от Malyarka Agent и готовит чистый export contract для CorelDRAW.

## Цель

```text
Order Result → Export Contract (.cdr preparation data)
```

## Входные данные

```yaml
source: Malyarka Agent
order_result:
  confirmed_rows:
    - height_mm, width_mm, quantity, material, color, finish
  total_area_m2: float
  export_blocked: bool
```

## Выходные данные

```yaml
export_contract:
  items:
    - width_mm, height_mm, quantity, label, material_note, color_note
  total_area_m2: float
  ready_for_corel: bool
```

## Что делает

1. Трансформирует confirmed_rows в формат для Corel
2. Подготавливает текстовые метки (размеры, цвет, материал)
3. Проверяет `export_blocked` — если true, не готовит экспорт

## Что запрещено

- ❌ Запускать CorelDRAW
- ❌ Создавать реальные .cdr файлы
- ❌ Работать с реальными производственными заказами
- ❌ Трогать сервер / live / secrets
- ❌ Отправлять файлы клиенту без разрешения
- ❌ Выходить за рамки export contract (только подготовка данных)

## Статус

`accepted` (not active) — спецификация принята пользователем.
Код не писать. Corel не запускать. Экспорт не выполнять.
