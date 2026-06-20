# Expected Input Format

Date: 2026-06-17

## What Sales Agent needs

```yaml
order_text: |
  Фасады МДФ 1000×400 4 шт RAL 9010 матовый
  600×300 2 шт дерево коричневый
```

## What Malyarka Agent needs

```yaml
intake_card:
  items:
    - height_mm: 1000, width_mm: 400, quantity: 4, material: "МДФ", color: "RAL 9010"
  flags: {}
```

## What Corel Export needs

```yaml
preliminary_result:
  confirmed_rows: [...]
  disputed_rows: [...]
  export_blocked: false
```

## Current limitation

На Gate 1 агенты НЕ запускаются. Только подготовка зоны.
