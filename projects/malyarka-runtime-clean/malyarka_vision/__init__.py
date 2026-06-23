"""Safe placeholder layer for future Malyarka photo recognition.

Importing this package does not read environment variables, secrets, files, or
network resources.
"""

from malyarka_vision.config import (
    DEFAULT_VISION_PROVIDER,
    VisionConfig,
    check_vision_ready,
)
from malyarka_vision.gemini import recognize_order_photo, recognize_order_photo_stub

__all__ = [
    "DEFAULT_VISION_PROVIDER",
    "VisionConfig",
    "check_vision_ready",
    "recognize_order_photo",
    "recognize_order_photo_stub",
]
