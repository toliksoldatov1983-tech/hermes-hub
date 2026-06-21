"""Single local order runner for Malyarka Clean."""

from pathlib import Path
import argparse
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
HERMES_ROOT = PROJECT_ROOT.parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
DEFAULT_INPUT_PATH = HERMES_ROOT / "inputs" / "ORDER_INPUT.txt"
DEFAULT_EXCEL_PATH = HERMES_ROOT / "outputs" / "COREL_EXPORT.xlsx"
sys.path.insert(0, str(SRC_ROOT))

from malyarka_clean_core import build_corel_export_model, build_order_result, create_corel_excel  # noqa: E402
from user_order_input import _format_result, _save_result  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="Run local order check and create Excel when possible.")
    parser.add_argument("--input-file", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--excel-file", type=Path, default=DEFAULT_EXCEL_PATH)
    args = parser.parse_args()

    result = run_local_order(args.input_file, args.excel_file)

    print()
    print(result["result_text"])
    print()
    print(f"Текстовый результат сохранён: {result['text_result_saved']}")

    if result["excel_created"]:
        print(f"Excel для Corel создан: {result['excel_path']}")
        return 0

    print("Excel для Corel не создан.")
    print(f"Причина блокировки: {result['block_reason']}")
    return 2


def run_local_order(input_file=DEFAULT_INPUT_PATH, excel_file=DEFAULT_EXCEL_PATH):
    """Read order input, save text result and create Excel only for clean orders."""
    raw_text = _read_order_file(input_file)
    order_result = build_order_result(raw_text, source="single_local_runner")
    corel_model = build_corel_export_model(order_result)
    result_text = _format_result(raw_text, order_result, corel_model)
    _save_result(result_text)

    if corel_model["export_blocked"]:
        return _runner_result(result_text, False, corel_model["reason"], excel_file)

    export_result = create_corel_excel(order_result, excel_file)
    return _runner_result(
        result_text,
        export_result["created"],
        export_result["reason"],
        export_result["output_path"],
    )


def _read_order_file(path):
    input_path = path if path.is_absolute() else DEFAULT_INPUT_PATH.parent / path
    if not input_path.exists():
        raise SystemExit(f"Файл заказа не найден: {input_path}")

    return input_path.read_text(encoding="utf-8")


def _runner_result(result_text, excel_created, reason, excel_path):
    return {
        "result_text": result_text,
        "text_result_saved": str(HERMES_ROOT / "outputs" / "LAST_ORDER_RESULT.txt"),
        "excel_created": excel_created,
        "excel_path": str(excel_path),
        "block_reason": reason,
    }


if __name__ == "__main__":
    raise SystemExit(main())
