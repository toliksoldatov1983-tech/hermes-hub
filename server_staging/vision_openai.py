"""Vision: recognize order photos using OpenAI GPT-4o."""

from __future__ import annotations

import os
import json
import urllib.request
import base64
from pathlib import Path
from typing import Any


def _call_openai_vision(image_data: bytes, prompt: str) -> str:
    """Send image to OpenAI GPT-4o and return extracted text."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return "Vision недоступен (нет ключа API)."

    img_b64 = base64.b64encode(image_data).decode("utf-8")

    body = json.dumps({
        "model": "gpt-4o",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}},
            ],
        "max_tokens": 500,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Vision error: {e}"


def recognize_order_photo(photo_bytes: bytes) -> str:
    """Extract dimensions and notes from order photo."""
    prompt = (
        "На этом фото — заказ на изготовление изделий. "
        "Извлеки все размеры (ширина x высота, или диаметр) и количество. "
        "Также найди примечания, номера, названия деталей. "
        "Ответь на русском, только извлечённые данные, без лишних слов."
    )
    return _call_openai_vision(photo_bytes, prompt)
