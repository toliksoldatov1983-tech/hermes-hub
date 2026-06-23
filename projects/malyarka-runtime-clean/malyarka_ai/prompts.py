"""Prompt builders for future DeepSeek order analysis."""

from __future__ import annotations

import json

from malyarka_ai.contracts import DEEPSEEK_ORDER_RESPONSE_CONTRACT


def build_deepseek_order_prompt(text: str) -> str:
    """Build a strict JSON-only prompt for order text analysis."""

    contract = json.dumps(
        DEEPSEEK_ORDER_RESPONSE_CONTRACT,
        ensure_ascii=False,
        indent=2,
    )
    return f"""Ты разбираешь текст заказа для проекта "Малярка".

Строгие правила:
- ничего не додумывать;
- не исправлять размеры от себя;
- если строка непонятная или неполная — вернуть type="disputed";
- для размеров первое число = height;
- для размеров второе число = width;
- для размеров третье число = quantity;
- если quantity нет — quantity = 1;
- если есть спорность — reason обязателен для disputed;
- confirmed rows возвращать как type="row";
- disputed rows возвращать как type="disputed";
- info rows возвращать как type="info";
- scheme rows возвращать как type="scheme";
- source/raw должны сохранять источник и исходную строку;
- вернуть только JSON по контракту;
- не писать пояснения вне JSON.

Контракт ответа:
{contract}

Текст заказа:
{text}
"""
