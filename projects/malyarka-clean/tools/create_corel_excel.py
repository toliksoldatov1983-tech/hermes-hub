"""Create a local Corel .xlsx file from ORDER_INPUT.txt when the order is clean."""

from pathlib import Path
import argparse
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
HERMES_ROOT = PROJECT_ROOT.parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
DEFAULT_INPUT_PATH = HERMES_ROOT / "inputs" / "ORDER_INPUT.txt"
DEFAULT_OUTPUT_PATH = HERMES_ROOT / "outputs" / "COREL_EXPORT.xlsx"
sys.path.insert(0, str(SRC_ROOT))

from malyarka_clean_core import build_corel_export_model, build_order_result, create_corel_excel  # noqa: E402
from user_order_input import _format_result, _save_result  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="Create safe local Corel .xlsx export.")
    parser.add_argument("--input-file", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--output-file", type=Path, default=DEFAULT_OUTPUT_PATH)
    args = parser.parse_args()

    raw_text = _read_order_file(args.input_file)
    order_result = build_order_result(raw_text, source="corel_excel_export")
    corel_model = build_corel_export_model(order_result)
    result_text = _format_result(raw_text, order_result, corel_model)
    _save_result(result_text)

    export_result = create_corel_excel(order_result, args.output_file)

    print()
    print(result_text)
    print()
    if export_result["created"]:
        print(f"Excel для Corel создан: {export_result['output_path']}")
        return 0

    print("Excel для Corel не создан.")
    print(f"Причина блокировки: {export_result['reason']}")
    print("Обычный текстовый результат сохранён в LAST_ORDER_RESULT.txt")
    return 2


def _read_order_file(path):
    input_path = path if path.is_absolute() else DEFAULT_INPUT_PATH.parent / path
    if not input_path.exists():
        raise SystemExit(f"Файл заказа не найден: {input_path}")

    return input_path.read_text(encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
