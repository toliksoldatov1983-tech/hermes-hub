from __future__ import annotations

from hermes_core.cli import main as cli_main
from hermes_core.router import HermesRouter
from hermes_core.types import HermesResponse, UserRequest


def handle_text(text: str, channel: str = "local") -> HermesResponse:
    return HermesRouter().handle(UserRequest(text=text, channel=channel))


def main() -> int:
    return cli_main(["status"])


if __name__ == "__main__":
    raise SystemExit(main())
