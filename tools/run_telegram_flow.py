from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from hermes_clean.telegram_flow_runner import format_run_result, run_telegram_flow_case, run_telegram_flow_text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run local Telegram flow dry-run scenarios")
    parser.add_argument("--case", choices=["clean", "disputed"], default="disputed")
    parser.add_argument("--text", default="")
    args = parser.parse_args(argv)

    if args.text:
        result = run_telegram_flow_text(args.text, auto_delete_disputes=True)
    else:
        result = run_telegram_flow_case(args.case)

    print(format_run_result(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
