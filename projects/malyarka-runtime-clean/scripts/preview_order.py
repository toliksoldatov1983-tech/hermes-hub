"""Print a CLI preview report for a text order file."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from malyarka_core.adapters.cli import preview_text_order


USAGE = "python scripts/preview_order.py path\\to\\order.txt"


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    args = sys.argv[1:] if argv is None else argv
    if not args:
        print(USAGE)
        return 0

    order_path = Path(args[0])
    try:
        text = order_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Файл не найден: {order_path}")
        return 1

    print(preview_text_order(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
