# Order Copy Manifest Template

Date: 2026-06-17

```yaml
manifest:
  order_id: "SAFE-001"
  original_source: "описание откуда копия (без пути)"
  copy_date: "2026-06-17"
  copied_by: "user"
  is_safe_copy: true
  content_types:
    - "txt"  # описание заказа
    - "csv"  # таблица позиций (опционально)
  notes: ""
  sanctity_checked: false
```

Заполняется пользователем при размещении safe copy.
