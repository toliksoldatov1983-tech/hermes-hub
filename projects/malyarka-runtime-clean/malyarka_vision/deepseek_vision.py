"""DeepSeek Vision recognizer for order photo parsing.

Sends images to the DeepSeek API for OCR + structured extraction of
facade-order rows. Falls back gracefully when the API is unreachable or the
key is missing.
"""

from __future__ import annotations

import base64
import json
import os
from pathlib import Path
from typing import Any

# Load DEEPSEEK_API_KEY from Hermes secrets file at import time
def _load_api_key_from_file() -> str | None:
    import os
    paths = [
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes", ".env"),
        os.path.join(os.path.dirname(__file__), "..", "..", ".env"),
    ]
    for p in paths:
        try:
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("DEEPSEEK_API_KEY="):
                        val = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if val and val != "***":
                            return val
        except (OSError, UnicodeDecodeError):
            continue
    return None

from malyarka_vision.config import (
    DEFAULT_DEEPSEEK_VISION_MODEL,
    DEEPSEEK_VISION_API_URL,
    DEEPSEEK_VISION_KEY_ENV_VAR,
    VisionConfig,
    check_vision_ready,
)

os.environ.setdefault(DEEPSEEK_VISION_KEY_ENV_VAR, _load_api_key_from_file() or "")

VISION_SYSTEM_PROMPT = """...
Return ONLY a JSON object (no markdown, no code fences, no explanation):

{
  "order_items": [
    {"height": 500, "width": 700, "quantity": 2},
    {"height": 300, "width": 400, "quantity": 1}
  ],
  "disputed_items": [
    {"raw": "unclear facade text", "reason": "no dimensions found"}
  ],
  "notes": "any observations about the photo"
}

Rules:
- First number = height, second number = width, third number = quantity.
- If no quantity given, quantity = 1.
- If dimensions are unclear, put in disputed_items.
- Never guess materials, colors, or prices.
- Use millimeters for dimensions."""


def _photo_to_base64_data_url(photo: str | bytes | Path) -> str:
    """Convert any photo input to a base64 data URL."""

    if isinstance(photo, bytes):
        b64 = base64.b64encode(photo).decode("ascii")
        return f"data:image/jpeg;base64,{b64}"

    if isinstance(photo, Path):
        raw = photo.read_bytes()
        b64 = base64.b64encode(raw).decode("ascii")
        suffix = photo.suffix.lstrip(".").lower()
        mime = "png" if suffix == "png" else "jpeg"
        return f"data:{mime};base64,{b64}"

    # string — could be a path or already base64
    maybe_path = Path(photo)
    if maybe_path.exists():
        raw = maybe_path.read_bytes()
        b64 = base64.b64encode(raw).decode("ascii")
        suffix = maybe_path.suffix.lstrip(".").lower()
        mime = "png" if suffix == "png" else "jpeg"
        return f"data:{mime};base64,{b64}"

    if photo.startswith("data:"):
        return photo

    return f"data:image/jpeg;base64,{photo}"


def _call_deepseek_vision(
    *,
    image_data_url: str,
    prompt: str,
    config: VisionConfig,
) -> dict[str, Any]:
    """Call the DeepSeek API with an image and a prompt. Returns parsed JSON."""

    api_key = config.api_key or os.getenv(DEEPSEEK_VISION_KEY_ENV_VAR)

    if not api_key:
        return {
            "status": "missing_api_key",
            "message": f"{DEEPSEEK_VISION_KEY_ENV_VAR} is not configured.",
            "external_api_called": False,
        }

    payload = {
        "model": config.model or DEFAULT_DEEPSEEK_VISION_MODEL,
        "messages": [
            {"role": "system", "content": VISION_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_data_url}},
                    {"type": "text", "text": prompt or "Распознай размеры с этого фото заказа."},
                ],
            },
        ],
        "temperature": 0.0,
        "max_tokens": 2000,
    }

    try:
        import urllib.request

        req = urllib.request.Request(
            config.vision_api_url or DEEPSEEK_VISION_API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))

        content = body["choices"][0]["message"]["content"]
        parsed = json.loads(content)

        return {
            "status": "ok",
            "message": "Photo recognized via DeepSeek Vision.",
            "external_api_called": True,
            "model": config.model,
            "order_items": parsed.get("order_items", []),
            "disputed_items": parsed.get("disputed_items", []),
            "notes": parsed.get("notes", ""),
        }

    except Exception as exc:
        return {
            "status": "api_error",
            "message": f"DeepSeek Vision call failed: {exc}",
            "external_api_called": True,
            "order_items": [],
            "disputed_items": [],
            "raw_error": str(exc)[:500],
        }


def recognize_order_with_deepseek(
    photo_input: str | bytes | Path | None = None,
    *,
    config: VisionConfig | None = None,
    prompt: str | None = None,
) -> dict[str, Any]:
    """Recognize order items from a photo using DeepSeek Vision."""

    runtime_config = VisionConfig() if config is None else config
    readiness = check_vision_ready(runtime_config)

    if photo_input is None:
        return {
            "status": "no_input",
            "message": "No photo provided.",
            "external_api_called": False,
            "readiness": readiness,
            "confirmed_items": [],
            "disputed_items": [],
        }

    if not runtime_config.real_recognition_enabled:
        return {
            "status": "disabled",
            "message": "Real DeepSeek Vision recognition is disabled.",
            "external_api_called": False,
            "readiness": readiness,
            "confirmed_items": [],
            "disputed_items": [],
        }

    image_data_url = _photo_to_base64_data_url(photo_input)
    effective_prompt = runtime_config.prompt_override or prompt or "Распознай размеры с этого фото."

    result = _call_deepseek_vision(
        image_data_url=image_data_url,
        prompt=effective_prompt,
        config=runtime_config,
    )

    result["readiness"] = readiness
    return result
