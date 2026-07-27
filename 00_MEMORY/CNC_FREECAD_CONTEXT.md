# CNC, FreeCAD и ось Z

Обновлено: 2026-07-24
Статус: подтверждённый технический контекст.

## Станок

- LNC MW2200 / MW2200A, BAOYUAN/RuiJie.
- Трёхосевой фрезерный станок.
- Серво: YAKOTEC ES3-15BAI-MG01.
- Электронная редукция: 1072:1.
- Параметр `P04-21=2`.
- ArtCAM → постпроцессор RuiJie-multitool1 → `.cnc`.
- Сглаживание: `G64 P0.05`.
- Для 3D: LINEAR 100–120 мс, BELL 60–80 мс.
- CABINET/DOOR синхронизировать с `IPATH PARA` и `AX.PARAM`.
- Резервная копия: `github.com/HA-HUB-I/LNC-MW2200-BACKUP`.

## Ось Z фрезерного стола

- Фрезер: Alteco FR 2200.
- Джог: ZK-SMC01.
- Драйвер: DM556.
- Двигатель: Nema23.
- Модуль: GGP80 SFU1605.
- Ход: 200 мм.
- Шаг ШВП: 5 мм.
- DRO: Shahe 5403F, 150 мм.
- Питание: 48 V / 500 W, 12 V / 1 A, 5 V.
- Концевик: LJ12A3-4-Z/BX.
- Z-probe подключается к ENA для автостопа.
- Нужны хомут для FR 2200 и крепёж модуля.

## FreeCAD

- Версия при последней фиксации: FreeCAD 1.1.1.
- FreeCADMCP: `%APPDATA%\FreeCAD\Mod\`.
- Настройки: `freecad_mcp_settings.json` в каталоге `v1-1`.
- MCP-сервер: `uvx freecad-mcp`.
- Модель стула: `C:\Users\user\Desktop\Stul.fcstd`.
- Референсы: `C:\Users\user\Desktop\stul_ref\`.
- Для вычитания `Part.Cut` надёжнее `Part.Face`.
- После трёх неудачных сравнений нужен новый исходный снимок.
- Нужен постпроцессор RuiJie.

## Зубчатое колесо

- API: `from fcgear.fcgear import makeGear` и `makeGear(m, z, 20, split=False)`.
- Последовательность: Wire → Part.Face → extrude → fuse hub → cut bore.
- Модуль 4, 28 зубьев, наружный диаметр 120 мм.
- Ступица Ø48×26 мм, отверстие Ø30 мм, толщина 20 мм.
