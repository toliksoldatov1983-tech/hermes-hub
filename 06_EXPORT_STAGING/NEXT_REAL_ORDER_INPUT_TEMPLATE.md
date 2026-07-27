# NEXT REAL ORDER INPUT TEMPLATE

```
Заказ: <название>
Цвет: <RAL или название>
Материал: <МДФ/ЛДСП/...> <толщина>
Фрезеровка: <без фрезеровки / фаска / ...>
Модель / примечание: <если есть>

Размеры:
HxW — Qty
HxW — Qty
```

Пример:
```
720x300 — 2 шт
720x400 — 1 шт
596x396 — 3 шт
```

## Правила

- Disputed rows > 0 → export BLOCKED
- Все gates PASS → staging → controlled export
- No overwrite / delete / move
- Root: E:\РАБОТА\01_ЗАКАЗЫ
- Month: NN_Месяц (06_Июнь, 07_Июль)
- Manifest + close report обязательны
