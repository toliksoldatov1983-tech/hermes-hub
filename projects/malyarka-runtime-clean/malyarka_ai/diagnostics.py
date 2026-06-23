"""Safe diagnostic preview for the DeepSeek fallback path."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from malyarka_ai.bridge import prepare_order_analysis_with_fallback
from malyarka_ai.config import DeepSeekConfig


DEFAULT_DIAGNOSTIC_SAMPLE = "1000*400\n1000*600"


def build_deepseek_fallback_diagnostic_preview(
    text: str | None,
    config: DeepSeekConfig | None = None,
) -> dict[str, Any]:
    """Return a safe diagnostic view of local fallback and prepared AI prompt."""

    fallback = prepare_order_analysis_with_fallback(text, config)

    return {
        "provider": fallback["provider"],
        "model": fallback["model"],
        "real_ai_enabled": fallback["real_ai_enabled"],
        "external_api_called": fallback["external_api_called"],
        "fallback_used": fallback["fallback_used"],
        "fallback_reason": fallback["fallback_reason"],
        "export_allowed": fallback["export_allowed"],
        "disputed_rows": fallback["disputed_rows"],
        "local_preview": fallback["local_preview"],
        "local_corel_lines": fallback["local_result"]["corel_lines"],
        "prepared_ai_prompt": fallback["prepared_ai_prompt"],
        "prepared_ai_analysis": fallback["prepared_ai_analysis"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Print safe DeepSeek fallback diagnostics."
    )
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "--sample",
        action="store_true",
        help="use a built-in safe sample order",
    )
    input_group.add_argument(
        "--text",
        help="order text to diagnose without calling external APIs",
    )
    input_group.add_argument(
        "--stdin",
        action="store_true",
        help="read order text from standard input",
    )
    input_group.add_argument(
        "--text-file",
        help="read order text from a UTF-8 text file",
    )
    parser.add_argument(
        "--format",
        choices=("json", "summary"),
        default="json",
        help="output format, default: json",
    )
    args = parser.parse_args(argv)

    text = _read_cli_text(args)
    preview = build_deepseek_fallback_diagnostic_preview(text, DeepSeekConfig())
    if args.format == "summary":
        print(_format_summary(preview))
    else:
        print(json.dumps(preview, ensure_ascii=False, indent=2))
    return 0


def _read_cli_text(args: argparse.Namespace) -> str:
    if args.sample:
        return DEFAULT_DIAGNOSTIC_SAMPLE
    if args.text is not None:
        return args.text
    if args.stdin:
        return sys.stdin.read()
    if args.text_file:
        return Path(args.text_file).read_text(encoding="utf-8")
    return ""


def _format_summary(preview: dict[str, Any]) -> str:
    lines = [
        f"export_allowed: {str(preview['export_allowed']).lower()}",
        f"fallback_used: {str(preview['fallback_used']).lower()}",
        f"external_api_called: {str(preview['external_api_called']).lower()}",
        "local_corel_lines:",
    ]
    corel_lines = preview["local_corel_lines"]
    if corel_lines:
        lines.extend(f"- {line}" for line in corel_lines)
    else:
        lines.append("-")

    disputed_rows = preview["disputed_rows"]
    lines.append("disputed_rows:")
    lines.append(f"- count: {disputed_rows['count']}")
    for item in disputed_rows["items"]:
        lines.append(f"- {item['raw']}: {item['reason']}")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
