from __future__ import annotations

import sys

from hermes_core.telegram.dry_run_gateway import TelegramDryRunGateway
from hermes_core.telegram.message_contract import TelegramMessage


def main() -> int:
    message = " ".join(sys.argv[1:]) or "/статус"
    result = TelegramDryRunGateway().simulate_incoming(TelegramMessage(message))
    print(result.planned_response)
    print(result.next_step)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
